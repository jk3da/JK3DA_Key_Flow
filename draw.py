import bpy
import gpu
import math
import time
import blf
from gpu_extras.batch import batch_for_shader
from .const import _SNAP_POSITIONS, _AREA_CFG
from .state import _active_keys, _purge_expired

def _draw_rounded_rect(x, y, w, h, r, color):
    r = min(r, w * 0.5, h * 0.5)
    seg = 8
    verts = []
    corners = [(x + r, y + r), (x + w - r, y + r), (x + w - r, y + h - r), (x + r, y + h - r)]
    angles = [math.pi, 1.5 * math.pi, 0, 0.5 * math.pi]
    for (cx, cy), a0 in zip(corners, angles):
        for i in range(seg + 1):
            a = a0 + i * (0.5 * math.pi / seg)
            verts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    cx, cy = x + w * 0.5, y + h * 0.5
    tris, n = [], len(verts)
    for i in range(n):
        tris.extend([(cx, cy), verts[i], verts[(i + 1) % n]])
    shader = gpu.shader.from_builtin("UNIFORM_COLOR")
    batch = batch_for_shader(shader, "TRIS", {"pos": tris})
    shader.bind()
    shader.uniform_float("color", color)
    gpu.state.blend_set("ALPHA")
    batch.draw(shader)
    gpu.state.blend_set("NONE")

def _draw_keyflow(context):
    addon = __package__.split(".")[0]
    prefs = context.preferences.addons[addon].preferences
    _purge_expired(prefs.fade_time)

    try:
        area = context.area
        if not area:
            return
        wm = context.window_manager
        cfg = _AREA_CFG.get(area.type)
        if not cfg:
            return
        toggle_prop, pos_prop = cfg
        if not getattr(wm, toggle_prop, False):
            return
        same = [a for a in context.screen.areas if a.type == area.type]
        if len(same) > 1 and area != same[0]:
            return
        snap_pos = getattr(wm, pos_prop, "BOTTOM_LEFT")
    except Exception:
        snap_pos = "BOTTOM_LEFT"

    if not _active_keys:
        return

    region = context.region
    vw, vh = region.width, region.height
    font_id = 0
    fs = prefs.font_size
    pad_x = int(fs * 0.7)
    pad_y = int(fs * 0.4)
    gap = int(fs * 0.35)
    xf, yf = _SNAP_POSITIONS.get(snap_pos, (0.0, 0.0))
    margin = prefs.margin

    blf.size(font_id, fs)
    entries = []
    now = time.time()

    for key in reversed(_active_keys):
        age = now - key["born"]
        hold = prefs.fade_time * 0.6
        if age < hold:
            alpha = 1.0
        else:
            alpha = max(0.0, 1.0 - (age - hold) / (prefs.fade_time * 0.4))

        base = (key["mods"] + " + " + key["label"]) if key["mods"] else key["label"]
        count = key.get("count", 1)
        full = f"{base}  ×{count}" if count > 1 else base
        tw, th = blf.dimensions(font_id, full)
        entries.append({"label": full, "alpha": alpha, "tw": tw, "th": th})

    if not entries:
        return

    max_w = max(e["tw"] for e in entries)
    row_h = entries[0]["th"] + pad_y * 2
    tot_h = len(entries) * (row_h + gap) - gap
    bx = margin + xf * (vw - max_w - pad_x * 2 - margin * 2)
    by_ = margin + yf * (vh - tot_h - margin * 2)

    for i, e in enumerate(reversed(entries)):
        ry = by_ + i * (row_h + gap)
        rw = e["tw"] + pad_x * 2
        bx_r = bx + (max_w + pad_x * 2 - rw) if xf > 0.4 else bx

        bg_a = e["alpha"] * prefs.bg_opacity
        if bg_a > 0.01:
            _draw_rounded_rect(bx_r, ry, rw, row_h, prefs.corner_radius,
                               (prefs.bg_color[0], prefs.bg_color[1],
                                prefs.bg_color[2], bg_a))

        blf.color(font_id, prefs.text_color[0], prefs.text_color[1],
                  prefs.text_color[2], e["alpha"])
        blf.position(font_id, bx_r + pad_x, ry + pad_y, 0)
        blf.draw(font_id, e["label"])

    try:
        for window in context.window_manager.windows:
            for a in window.screen.areas:
                if a.type == "VIEW_3D":
                    a.tag_redraw()
    except Exception:
        pass
