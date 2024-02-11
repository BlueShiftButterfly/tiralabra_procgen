from pygame import Vector2
from engine.objects.object import Object

class GeneratorObject(Object):
    def __init__(self, id: str, position: Vector2 = Vector2(0,0), generator_object = None) -> None:
        super().__init__(id, position, None)
        self.generator_object = generator_object
    
    def generate(self):
        if self.generator_object != None:
            self.generator_object.generate()

    def update(self):
        return super().update()
    