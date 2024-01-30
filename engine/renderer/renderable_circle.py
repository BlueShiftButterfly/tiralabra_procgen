from pygame import Vector2
from pygame import Color
from engine.renderer.renderable_types import RenderableType
from engine.renderer.renderable import Renderable

class RenderableCircle(Renderable):
    """Used to render rects by the render queue"""
    def __init__(self, position : Vector2, color : Color, radius : float, border_width : float = 0, is_filled = True) -> None:
        super().__init__()
        self.type = RenderableType.CIRCLE
        self.position = position
        self.color = color
        self.radius = radius
        self.border_width = border_width
        self.is_filled = is_filled

    def __cmp___(self, other):
        return super().__cmp___(other)