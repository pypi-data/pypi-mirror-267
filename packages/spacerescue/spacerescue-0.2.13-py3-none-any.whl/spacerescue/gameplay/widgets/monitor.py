import pyray as pr

from spacerescue.render.camera import Camera
from spacerescue.render.widget import Widget
from spacerescue.resources import SCENE_RESOURCES


class Monitor(Widget):
    
    FONT_SPACING = 2
    FONT_SIZE = 28
    FONT_CHAR_WIDTH = (FONT_SIZE + FONT_SPACING) / 2
    FONT_COLOR = pr.Color(255, 255, 255, 255)
    FOOTER_SIZE = FONT_SIZE + FONT_SPACING
    BG_COLOR = pr.Color(64, 191, 182, 192)
    SCANLINE_COLOR = pr.Color(255, 255, 255, 96)

    def __init__(
        self,
        id: str,
        widget: Widget,
        caption: str | None = None,
        border_size: int = 10,
    ):
        super().__init__(id, widget.bound)
        self.widget = widget
        self.caption = caption
        self.border_size = border_size
        
        self.scanline = SCENE_RESOURCES.load_texture("scanline")
        pr.set_texture_wrap(self.scanline, pr.TextureWrap.TEXTURE_WRAP_REPEAT)
        self.font = SCENE_RESOURCES.load_font("mono_font28")
    
    def update(self):
        self.widget.update()
        
    def draw(self, camera: Camera | None=None):
        outer_bound = self._get_outer_bound()
        pr.draw_rectangle_rec(outer_bound, Monitor.BG_COLOR)
        
        pr.begin_scissor_mode(
            int(self.bound.x),
            int(self.bound.y),
            int(self.bound.width),
            int(self.bound.height),
        )
        self.widget.draw(camera)
        pr.end_scissor_mode()
        
        if self.caption is not None:
            pr.draw_text_ex(
                self.font,
                self.caption,
                pr.Vector2(
                    self.bound.x,
                    self.bound.y + self.bound.height + Monitor.FONT_SPACING,
                ),
                Monitor.FONT_SIZE,
                Monitor.FONT_SPACING,
                Monitor.FONT_COLOR,
            )
        
        pr.draw_texture_pro(
            self.scanline,
            pr.Rectangle(0, 0, outer_bound.width, outer_bound.height),
            outer_bound,
            pr.vector2_zero(),
            0.0,
            Monitor.SCANLINE_COLOR,
        )
        
    def _get_outer_bound(self) -> pr.Rectangle:
        if self.caption is not None:
            return pr.Rectangle(
                int(self.bound.x - self.border_size),
                int(self.bound.y - self.border_size),
                int(self.bound.width + self.border_size * 2),
                int(self.bound.height + self.border_size * 2 + Monitor.FOOTER_SIZE),
            )
        else:
            return pr.Rectangle(
                int(self.bound.x - self.border_size),
                int(self.bound.y - self.border_size),
                int(self.bound.width + self.border_size * 2),
                int(self.bound.height + self.border_size * 2),
            )