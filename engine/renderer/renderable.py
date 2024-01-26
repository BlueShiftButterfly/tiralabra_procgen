from pygame.math import Vector2

class Renderable:
    def __init__(self) -> None:
        self.visual_rect = None
        self.world_position = Vector2(0,0)
