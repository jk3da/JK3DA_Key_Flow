_MOUSE_MAP = {
    "LEFTMOUSE": "LMB",
    "RIGHTMOUSE": "RMB",
    "MIDDLEMOUSE": "MMB",
    "WHEELUPMOUSE": "Scroll ↑",
    "WHEELDOWNMOUSE": "Scroll ↓",
    "BUTTON4MOUSE": "MB4",
    "BUTTON5MOUSE": "MB5",
}

_KEY_LABEL_MAP = {
    "G": "Grab", "S": "Scale", "R": "Rotate",
    "E": "Extrude", "I": "Inset", "B": "Box Select",
    "C": "Circle Sel", "F": "Fill", "J": "Connect",
    "K": "Knife", "L": "Select Linked", "M": "Merge",
    "P": "Separate", "U": "UV Unwrap", "V": "Rip",
    "W": "Select All", "X": "Delete", "Y": "Split",
    "Z": "Wireframe", "A": "Select All", "H": "Hide",
    "N": "Sidebar", "O": "Proportional", "Q": "Quick Favs",
    "T": "Toolbar", "TAB": "Edit Mode", "DEL": "Delete",
    "SPACE": "Play/Search",
    "NUMPAD_1": "Front", "NUMPAD_3": "Right", "NUMPAD_7": "Top",
    "NUMPAD_5": "Ortho", "NUMPAD_0": "Camera",
    "F3": "Search", "F9": "Last Op", "F12": "Render",
    "RET": "Confirm", "NUMPAD_ENTER": "Confirm",
    "ESC": "Cancel", "BACK_SPACE": "Bksp",
}

_MODIFIER_KEYS = {
    "LEFT_SHIFT", "RIGHT_SHIFT",
    "LEFT_CTRL", "RIGHT_CTRL",
    "LEFT_ALT", "RIGHT_ALT",
    "OSKEY",
}

_IGNORE_KEYS = {
    "MOUSEMOVE", "INBETWEEN_MOUSEMOVE",
    "WINDOW_DEACTIVATE", "TIMER", "TIMER0", "TIMER1",
    "TIMER2", "TIMER_JOBS", "TIMER_SOUND",
    "TIMERREGION", "NONE",
}

_TRANSFORM_OPS = {"G", "S", "R"}
_AXIS_KEYS = {"X", "Y", "Z"}
_TRANSFORM_KEY_ID = "__transform__"

_NUM_KEY_MAP = {
    "ZERO": "0", "ONE": "1", "TWO": "2", "THREE": "3", "FOUR": "4",
    "FIVE": "5", "SIX": "6", "SEVEN": "7", "EIGHT": "8", "NINE": "9",
    "NUMPAD_0": "0", "NUMPAD_1": "1", "NUMPAD_2": "2", "NUMPAD_3": "3",
    "NUMPAD_4": "4", "NUMPAD_5": "5", "NUMPAD_6": "6", "NUMPAD_7": "7",
    "NUMPAD_8": "8", "NUMPAD_9": "9",
    "PERIOD": ".", "NUMPAD_PERIOD": ".",
    "MINUS": "-", "NUMPAD_MINUS": "-",
}

_TRANSFORM_LABELS = {"G": "Grab (G)", "S": "Scale (S)", "R": "Rotate (R)"}

_SNAP_POSITIONS = {
    "BOTTOM_LEFT": (0.0, 0.0),
    "BOTTOM_CENTER": (0.5, 0.0),
    "BOTTOM_RIGHT": (1.0, 0.0),
    "CENTER_LEFT": (0.0, 0.5),
    "CENTER": (0.5, 0.5),
    "CENTER_RIGHT": (1.0, 0.5),
    "TOP_LEFT": (0.0, 1.0),
    "TOP_CENTER": (0.5, 1.0),
    "TOP_RIGHT": (1.0, 1.0),
}

_POSITION_ITEMS = [
    ("BOTTOM_LEFT", "Bottom Left", ""),
    ("BOTTOM_CENTER", "Bottom", ""),
    ("BOTTOM_RIGHT", "Bottom Right", ""),
    ("CENTER_LEFT", "Left", ""),
    ("CENTER", "Center", ""),
    ("CENTER_RIGHT", "Right", ""),
    ("TOP_LEFT", "Top Left", ""),
    ("TOP_CENTER", "Top", ""),
    ("TOP_RIGHT", "Top Right", ""),
]

_AREA_CFG = {
    "VIEW_3D":         ("jk3da_kf_show_view3d",    "jk3da_kf_pos_view3d"),
    "IMAGE_EDITOR":    ("jk3da_kf_show_image",      "jk3da_kf_pos_image"),
    "NODE_EDITOR":     ("jk3da_kf_show_node",       "jk3da_kf_pos_node"),
    "SEQUENCE_EDITOR": ("jk3da_kf_show_seq",        "jk3da_kf_pos_seq"),
    "DOPESHEET_EDITOR": ("jk3da_kf_show_dopesheet", "jk3da_kf_pos_dopesheet"),
}

_TRANSFORM_KEY_ID = "__transform__"
