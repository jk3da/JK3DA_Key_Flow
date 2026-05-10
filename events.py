from .const import (
    _IGNORE_KEYS, _MOUSE_MAP, _KEY_LABEL_MAP, _MODIFIER_KEYS,
    _NUM_KEY_MAP, _TRANSFORM_OPS, _AXIS_KEYS
)

def _format_event(event):
    t = event.type
    v = event.value

    if t in _IGNORE_KEYS:
        return None, None
    if v == "RELEASE":
        return None, None

    if t in _MOUSE_MAP:
        if t in {"WHEELUPMOUSE", "WHEELDOWNMOUSE"}:
            return (_MOUSE_MAP[t], "") if v == "PRESS" else (None, None)
        return (_MOUSE_MAP[t], "") if v == "CLICK" else (None, None)

    if t in _MODIFIER_KEYS:
        if v in {"PRESS", "ANY"}:
            lbl = t.replace("LEFT_", "").replace("RIGHT_", "").replace("OSKEY", "OS").title()
            return lbl, ""
        return None, None

    if v not in {"PRESS", "CLICK", "ANY"}:
        return None, None

    mods = []
    if event.ctrl: mods.append("Ctrl")
    if event.shift: mods.append("Shift")
    if event.alt: mods.append("Alt")
    mods_str = " + ".join(mods)

    digit = _NUM_KEY_MAP.get(t)
    if digit is not None:
        return digit, mods_str

    raw = (t.replace("_", " ").title()
           .replace("Numpad ", "Num ")
           .replace("Return", "Enter")
           .replace("Back Space", "Bksp")
           .replace("Escape", "Esc"))

    friendly = _KEY_LABEL_MAP.get(t)
    if friendly and friendly != raw:
        label = f"{friendly} ({raw})"
    else:
        label = raw

    return label, mods_str
