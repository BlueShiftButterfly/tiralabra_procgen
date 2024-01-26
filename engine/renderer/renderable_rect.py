from pygame.math import Vector2
from pygame import Rect, Color
from engine.renderer.renderable_types import RenderableType
from engine.renderer.renderable import Renderable

class RenderableRect(Renderable):
    def __init__(self, position : Vector2, rect : Rect, color : Color, width : int = 0, border_radius : int = 0) -> None:
        super().__init__()
        self.type = RenderableType.RECT
        self.position = position
        self.rect = rect
        self.color = color
        self.width = width
        self.border_radius = border_radius
    