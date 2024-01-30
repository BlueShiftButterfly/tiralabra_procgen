from pygame import Vector2

class Object:
    def __init__(self, id : str, position : Vector2 = Vector2(0,0), renderable_component = None) -> None:
        self.position = position
        self.id = id
        self.renderable_component = renderable_component
    
    def update(self):
        if self.renderable_component != None:
            self.renderable_component.position = self.position
