import bpy
import time
from .const import _TRANSFORM_OPS, _AXIS_KEYS, _NUM_KEY_MAP
from .state import _active_keys, _transform_state, _reset_transform_state, _poll_transform
from .events import _format_event
from .draw import _draw_keyflow

class JK3DA_OT_KeyFlowRun(bpy.types.Operator):
    bl_idname = "jk3da.keyflow_run"
    bl_label = "KeyFlow Running"
    bl_options = {"INTERNAL"}

    _draw_handle = None
    _draw_handles = []

    @classmethod
    def is_running(cls):
        return cls._draw_handle is not None

    def invoke(self, context, _event):
        if JK3DA_OT_KeyFlowRun.is_running():
            return {"CANCELLED"}

        JK3DA_OT_KeyFlowRun._draw_handles = []
        for stype in [bpy.types.SpaceView3D, bpy.types.SpaceImageEditor,
                      bpy.types.SpaceNodeEditor, bpy.types.SpaceSequenceEditor]:
            try:
                h = stype.draw_handler_add(_draw_keyflow, (context,), "WINDOW", "POST_PIXEL")
                JK3DA_OT_KeyFlowRun._draw_handles.append((stype, h))
            except Exception:
                pass
        JK3DA_OT_KeyFlowRun._draw_handle = True

        context.window_manager.modal_handler_add(self)
        if context.area:
            context.area.tag_redraw()
        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        if not context.window_manager.jk3da_keyflow_active:
            self._stop(context)
            return {"CANCELLED"}

        t, v = event.type, event.value

        if t in {"MOUSEMOVE", "INBETWEEN_MOUSEMOVE"}:
            return {"PASS_THROUGH"}

        if t not in {"MOUSEMOVE", "INBETWEEN_MOUSEMOVE"}:
            self._handle_transform(event, context)
            label, mods = _format_event(event)
            if label:
                now = time.time()
                addon = __package__.split(".")[0]
                prefs = context.preferences.addons[addon].preferences
                is_real = event.value in {"PRESS", "CLICK"}
                if is_real:
                    if (_active_keys
                            and _active_keys[-1].get("label") == label
                            and _active_keys[-1].get("mods") == mods
                            and _active_keys[-1].get("id") is None
                            and now - _active_keys[-1]["born"] < prefs.fade_time):
                        _active_keys[-1]["count"] = _active_keys[-1].get("count", 1) + 1
                        _active_keys[-1]["born"] = now
                    else:
                        _active_keys.append({"label": label, "mods": mods,
                                             "born": now, "count": 1})
                    if len(_active_keys) > prefs.max_keys:
                        del _active_keys[:-prefs.max_keys]
                    if context.area:
                        context.area.tag_redraw()
                else:
                    _active_keys.append({"label": label, "mods": mods,
                                         "born": now, "count": 1})
                    if len(_active_keys) > prefs.max_keys:
                        del _active_keys[:-prefs.max_keys]
                    if context.area:
                        context.area.tag_redraw()

        return {"PASS_THROUGH"}

    def _handle_transform(self, event, context):
        t, v = event.type, event.value
        ts = _transform_state

        if t in _TRANSFORM_OPS and v in {"PRESS", "ANY"}:
            if not ts["active"]:
                _reset_transform_state()
                ts["active"] = True
                ts["op"] = t
                if not bpy.app.timers.is_registered(_poll_transform):
                    bpy.app.timers.register(_poll_transform, first_interval=0.05)
            return

        if not ts["active"]:
            return

        if t in _AXIS_KEYS and v in {"PRESS", "ANY"}:
            if event.shift:
                ts["axes"] = [ax for ax in "XYZ" if ax != t]
                ts["plane_constraint"] = True
            else:
                ts["axes"] = [] if ts["axes"] == [t] else [t]
                ts["plane_constraint"] = False
            ts["num_input"] = ""
            return

        digit = _NUM_KEY_MAP.get(t)
        if digit is not None and v in {"PRESS", "ANY"}:
            if digit == "-":
                ts["num_input"] = "-" if not ts["num_input"] else ""
            elif digit == "." and "." in ts["num_input"]:
                pass
            else:
                ts["num_input"] += digit

        if t == "BACK_SPACE" and v == "PRESS":
            ts["num_input"] = ts["num_input"][:-1]

        if t in {"RET", "NUMPAD_ENTER", "LEFTMOUSE"} and v in {"PRESS", "CLICK"}:
            from .state import _transform_label
            final_label = _transform_label()
            _reset_transform_state()
            if final_label:
                now = time.time()
                for k in _active_keys:
                    if k.get("id") == "__transform__":
                        k["label"] = final_label
                        k["born"] = now
                        break
                else:
                    _active_keys.append({
                        "id": "__transform__",
                        "label": final_label, "mods": "",
                        "born": now,
                    })
            else:
                _active_keys[:] = [k for k in _active_keys
                                   if k.get("id") != "__transform__"]

        if t in {"ESC", "RIGHTMOUSE"} and v in {"PRESS", "CLICK"}:
            _active_keys[:] = [k for k in _active_keys if k.get("id") != "__transform__"]
            _reset_transform_state()

    def _stop(self, context):
        for stype, h in getattr(JK3DA_OT_KeyFlowRun, '_draw_handles', []):
            try: stype.draw_handler_remove(h, "WINDOW")
            except: pass
        JK3DA_OT_KeyFlowRun._draw_handles = []
        JK3DA_OT_KeyFlowRun._draw_handle = None
        global _active_keys
        _active_keys = []
        _reset_transform_state()
        if context.area:
            context.area.tag_redraw()


class JK3DA_OT_KeyFlowToggle(bpy.types.Operator):
    bl_idname = "jk3da.keyflow_toggle"
    bl_label = "Toggle KeyFlow"

    def execute(self, context):
        wm = context.window_manager
        if JK3DA_OT_KeyFlowRun.is_running():
            wm.jk3da_keyflow_active = False
        else:
            wm.jk3da_keyflow_active = True
            bpy.ops.jk3da.keyflow_run("INVOKE_DEFAULT")
        return {"FINISHED"}


class JK3DA_OT_KeyFlowSetPosition(bpy.types.Operator):
    bl_idname = "jk3da.keyflow_set_position"
    bl_label = "Set Position"
    position: bpy.props.StringProperty()

    def execute(self, context):
        wm = context.window_manager
        area = context.area
        if area and area.type in {"VIEW_3D", "IMAGE_EDITOR", "NODE_EDITOR", "SEQUENCE_EDITOR", "DOPESHEET_EDITOR"}:
            _, pos_prop = _AREA_CFG[area.type]
            try:
                setattr(wm, pos_prop, self.position)
            except Exception:
                pass
        if context.area:
            context.area.tag_redraw()
        return {"FINISHED"}
