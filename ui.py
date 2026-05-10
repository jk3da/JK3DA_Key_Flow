import bpy
from .const import _AREA_CFG, _POSITION_ITEMS

class JK3DA_PT_KeyFlow(bpy.types.Panel):
    bl_label = "JK3DA KeyFlow"
    bl_idname = "JK3DA_PT_KeyFlow"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "JK3DA KeyFlow"

    def draw_header(self, context):
        self.layout.label(text="", icon="COLORSET_02_VEC")

    def draw(self, context):
        layout = self.layout
        addon = __package__.split(".")[0]
        prefs = context.preferences.addons[addon].preferences
        wm = context.window_manager

        row = layout.row()
        row.scale_y = 1.8
        if wm.jk3da_keyflow_active:
            row.alert = True
            row.operator("jk3da.keyflow_toggle", text="■  STOP KeyFlow", icon="PAUSE")
        else:
            row.operator("jk3da.keyflow_toggle", text="▶  START KeyFlow", icon="PLAY")

        layout.separator(factor=0.4)

        box = layout.box()
        box.label(text="Show in Editor", icon="WINDOW")
        _rows = [
            ("jk3da_kf_show_view3d", "jk3da_kf_pos_view3d", "3D Viewport"),
            ("jk3da_kf_show_image", "jk3da_kf_pos_image", "UV / Image Editor"),
            ("jk3da_kf_show_node", "jk3da_kf_pos_node", "Node Editor"),
            ("jk3da_kf_show_seq", "jk3da_kf_pos_seq", "VSE"),
            ("jk3da_kf_show_dopesheet", "jk3da_kf_pos_dopesheet", "Dope Sheet"),
        ]
        for tog, pos_p, lbl in _rows:
            row = box.row(align=True)
            row.prop(wm, tog, text=lbl)
            sub = row.row(align=True)
            sub.enabled = getattr(wm, tog, False)
            sub.prop(wm, pos_p, text="")
        box.prop(prefs, "margin", text="Margin")

        layout.separator(factor=0.4)

        box2 = layout.box()
        box2.label(text="Appearance", icon="RESTRICT_COLOR_OFF")
        row = box2.row(align=True)
        row.prop(prefs, "text_color", text="Text")
        row.prop(prefs, "bg_color", text="BG")
        box2.prop(prefs, "bg_opacity", text="Opacity")
        box2.prop(prefs, "font_size", text="Font Size")
        box2.prop(prefs, "corner_radius", text="Radius")

        layout.separator(factor=0.4)

        box3 = layout.box()
        box3.label(text="Behaviour", icon="TIME")
        box3.prop(prefs, "fade_time", text="Fade Duration")
        box3.prop(prefs, "max_keys", text="Max Keys")


class JK3DA_PT_KeyFlow_UV(bpy.types.Panel):
    bl_label = "JK3DA KeyFlow"
    bl_idname = "JK3DA_PT_KeyFlow_UV"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_category = "JK3DA KeyFlow"

    def draw_header(self, context):
        self.layout.label(text="", icon="COLORSET_02_VEC")

    def draw(self, context):
        layout = self.layout
        addon = __package__.split(".")[0]
        prefs = context.preferences.addons[addon].preferences
        wm = context.window_manager

        row = layout.row()
        row.scale_y = 1.6
        if wm.jk3da_keyflow_active:
            row.alert = True
            row.operator("jk3da.keyflow_toggle", text="■  STOP KeyFlow", icon="PAUSE")
        else:
            row.operator("jk3da.keyflow_toggle", text="▶  START KeyFlow", icon="PLAY")

        layout.separator(factor=0.4)
        box = layout.box()
        box.label(text="This Editor", icon="IMAGE")
        row = box.row(align=True)
        row.prop(wm, "jk3da_kf_show_image", text="Show here")
        sub = row.row()
        sub.enabled = wm.jk3da_kf_show_image
        sub.prop(wm, "jk3da_kf_pos_image", text="")

        layout.separator(factor=0.4)
        box2 = layout.box()
        box2.label(text="Appearance", icon="RESTRICT_COLOR_OFF")
        row = box2.row(align=True)
        row.prop(prefs, "text_color", text="Text")
        row.prop(prefs, "bg_color", text="BG")
        box2.prop(prefs, "font_size", text="Font Size")
        box2.prop(prefs, "fade_time", text="Fade Duration")
        box2.prop(prefs, "max_keys", text="Max Keys")
