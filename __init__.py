bl_info = {
    "name":        "JK3DA KeyFlow",
    "author":      "JK3DA (https://jk3da.com) — AI-assisted development",
    "version":     (1, 0, 0),
    "blender":     (4, 0, 0),
    "category":    "System",
    "description": "Display keyboard and mouse inputs in the viewport.",
    "doc_url":     "https://jk3da.com",
}

from .prefs import JK3DAKeyFlowPrefs
from .operators import (
    JK3DA_OT_KeyFlowRun,
    JK3DA_OT_KeyFlowToggle,
    JK3DA_OT_KeyFlowSetPosition,
)
from .ui import JK3DA_PT_KeyFlow, JK3DA_PT_KeyFlow_UV
from .wm_props import _wm_props_register, _wm_props_unregister

classes = [
    JK3DAKeyFlowPrefs,
    JK3DA_OT_KeyFlowRun,
    JK3DA_OT_KeyFlowToggle,
    JK3DA_OT_KeyFlowSetPosition,
    JK3DA_PT_KeyFlow,
    JK3DA_PT_KeyFlow_UV,
]

import bpy

_addon_keymaps = []


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    _wm_props_register()
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new("jk3da.keyflow_toggle", "K", "PRESS", shift=True, alt=True)
        _addon_keymaps.append((km, kmi))


def unregister():
    for km, kmi in list(_addon_keymaps):
        km.keymap_items.remove(kmi)
    _addon_keymaps.clear()
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    _wm_props_unregister()

_addon_keymaps = []
