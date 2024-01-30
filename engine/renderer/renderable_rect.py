from pygame import Vector2
from pygame import Rect, Color
from engine.renderer.renderable_types import RenderableType
from engine.renderer.renderable import Renderable

class RenderableRect(Renderable):
    """Used to render rects by the render queue"""
    def __init__(self, position : Vector2, height : float, width : float, color : Color, border_width : int = 0, border_radius : int = 0) -> None:
        super().__init__()
        self.type = RenderableType.RECT
        self.position = position
        self.height = height
        self.width = width
        self.color = color
        self.border_width = border_width
        self.border_radius = border_radius

    def __cmp___(self, other):
        return super().__cmp___(other)