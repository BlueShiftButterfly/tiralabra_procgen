from pygame import Vector2

class Object:
    def __init__(self, object_id : str, position : Vector2 = Vector2(0,0), renderable_component = None) -> None:
        self.position = position
        self.id = object_id
        self.renderable_component = renderable_component

    def update(self, delta_time : float):
        if self.renderable_component is not None:
            self.renderable_component.position = self.position
