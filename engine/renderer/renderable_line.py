from pygame import Vector2
from pygame import Color
from engine.renderer.renderable_types import RenderableType
from engine.renderer.renderable import Renderable

class RenderableLine(Renderable):
    """Used to render lines by the render queue"""
    def __init__(
            self,
            position : Vector2,
            end_position : Vector2,
            color : Color,
            width : float = 0,
            anti_aliased : bool = False
            ) -> None:
        super().__init__()
        self.type = RenderableType.LINE
        self.position = position
        self.end_position = end_position
        self.color = color
        self.width = width
        self.anti_aliased = anti_aliased
        self.bounding_box = (
            Vector2(min(position.x, end_position.x), min(position.y, end_position.y)),
            Vector2(max(position.x, end_position.x), max(position.y, end_position.y))
        )
