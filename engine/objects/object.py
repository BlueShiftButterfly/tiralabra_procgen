from pygame.math import Vector2

class Object:
    def __init__(self, position : Vector2 = Vector2(0,0)) -> None:
        self.position = position