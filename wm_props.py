import bpy
from bpy.props import BoolProperty, EnumProperty
from .const import _POSITION_ITEMS

def _wm_props_register():
    wm = bpy.types.WindowManager
    wm.jk3da_keyflow_active = BoolProperty(name="KeyFlow Active", default=False)
    wm.jk3da_kf_show_view3d = BoolProperty(name="3D Viewport", default=True)
    wm.jk3da_kf_show_image = BoolProperty(name="UV / Image Editor", default=False)
    wm.jk3da_kf_show_node = BoolProperty(name="Node Editor", default=False)
    wm.jk3da_kf_show_seq = BoolProperty(name="VSE", default=False)
    wm.jk3da_kf_show_dopesheet = BoolProperty(name="Dope Sheet", default=False)
    for suffix in ["view3d", "image", "node", "seq", "dopesheet"]:
        setattr(wm, f"jk3da_kf_pos_{suffix}",
                EnumProperty(name="Position", items=_POSITION_ITEMS, default="BOTTOM_LEFT"))

def _wm_props_unregister():
    props = [
        "jk3da_keyflow_active",
        "jk3da_kf_show_view3d", "jk3da_kf_show_image", "jk3da_kf_show_node",
        "jk3da_kf_show_seq", "jk3da_kf_show_dopesheet",
        "jk3da_kf_pos_view3d", "jk3da_kf_pos_image", "jk3da_kf_pos_node",
        "jk3da_kf_pos_seq", "jk3da_kf_pos_dopesheet",
    ]
    for p in props:
        try: delattr(bpy.types.WindowManager, p)
        except AttributeError: pass
