import bpy
from bpy.props import FloatProperty, IntProperty, FloatVectorProperty

class JK3DAKeyFlowPrefs(bpy.types.AddonPreferences):
    bl_idname = "JK3DA_Key_Flow"

    text_color: FloatVectorProperty(
        name="Text Color", subtype="COLOR_GAMMA", size=3,
        min=0.0, max=1.0, default=(1.0, 1.0, 1.0),
    )
    bg_color: FloatVectorProperty(
        name="Background Color", subtype="COLOR_GAMMA", size=3,
        min=0.0, max=1.0, default=(0.9, 0.38, 0.0),
    )
    bg_opacity: FloatProperty(name="Opacity", min=0.0, max=1.0, default=0.85)
    font_size: IntProperty(name="Font Size", min=8, max=72, default=22)
    corner_radius: IntProperty(name="Corner Radius", min=0, max=30, default=8)
    fade_time: FloatProperty(name="Fade Duration", min=0.3, max=120.0, default=1.5)
    max_keys: IntProperty(name="Max Keys", min=1, max=20, default=8)
    margin: IntProperty(name="Margin", min=0, max=200, default=30)

    def draw(self, _context):
        layout = self.layout
        box = layout.box()
        box.label(text="Appearance", icon="RESTRICT_COLOR_OFF")
        row = box.row(align=True)
        row.prop(self, "text_color", text="Text")
        row.prop(self, "bg_color", text="Background")
        box.prop(self, "bg_opacity")
        row2 = box.row(align=True)
        row2.prop(self, "font_size")
        row2.prop(self, "corner_radius")
        layout.separator(factor=0.5)
        box2 = box = layout.box()
        box2.label(text="Behaviour", icon="TIME")
        box2.prop(self, "fade_time")
        box2.prop(self, "max_keys")
        box2.prop(self, "margin")
