from pygame.math import Vector2
from pygame import Color
from engine.renderer.renderable_types import RenderableType

class RenderableLine:
    def __init__(self, start_position : Vector2, end_position : Vector2, color : Color, width : int = 1, anti_aliased : bool = False) -> None:
        self.type = RenderableType.LINE
        self.start_position = start_position
        self.end_position = end_position
        self.color = color
        self.width = width
        self.anti_aliased = anti_aliased