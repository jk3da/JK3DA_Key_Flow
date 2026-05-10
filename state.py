import time
from .const import _TRANSFORM_KEY_ID

_active_keys = []

_transform_state = {
    "active": False,
    "op": None,
    "axes": [],
    "num_input": "",
    "plane_constraint": False,
}

def _reset_transform_state():
    _transform_state["active"] = False
    _transform_state["op"] = None
    _transform_state["axes"] = []
    _transform_state["num_input"] = ""
    _transform_state["plane_constraint"] = False

def _transform_label():
    ts = _transform_state
    if not ts["active"] or not ts["op"]:
        return None
    from .const import _TRANSFORM_LABELS
    op_lbl = _TRANSFORM_LABELS.get(ts["op"], ts["op"])
    axes = ts["axes"]
    num = ts["num_input"]
    plane = ts["plane_constraint"]

    if axes:
        ax_str = "".join(axes)
        display = f"[~{ax_str}]" if plane else f"[{ax_str}]"
        return f"{op_lbl}  {display}: {num}" if num else f"{op_lbl}  {display}"
    return f"{op_lbl}  {num}" if num else op_lbl

def _purge_expired(fade_time):
    now = time.time()
    global _active_keys
    _active_keys = [
        k for k in _active_keys
        if k.get("id") == "__transform__"
        or now - k["born"] < fade_time
    ]

def _poll_transform():
    try:
        import bpy
        wm = bpy.context.window_manager
        if not wm.jk3da_keyflow_active or not _transform_state["active"]:
            return None

        label = _transform_label()
        if not label:
            return None

        now = time.time()
        for k in _active_keys:
            if k.get("id") == _TRANSFORM_KEY_ID:
                k["label"] = label
                k["born"] = now + 9999
                break
        else:
            _active_keys.append({
                "id": _TRANSFORM_KEY_ID,
                "label": label, "mods": "",
                "born": now + 9999,
            })

        for window in wm.windows:
            for area in window.screen.areas:
                if area.type == "VIEW_3D":
                    area.tag_redraw()
        return 0.05

    except Exception:
        _reset_transform_state()
        return None
