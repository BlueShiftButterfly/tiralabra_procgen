from pygame import Vector2
from engine.input_handler.input_handler import InputHandler
from engine.objects.object import Object

class GeneratorObject(Object):
    def __init__(self, id: str, position: Vector2 = Vector2(0,0), generator_object = None) -> None:
        super().__init__(id, position, None)
        self.generator_object = generator_object
        self.input_mod = 0 # TODO: Remove this and replace with proper handling for inputs that should fire only once when button pressed
    
    def generate(self):
        if self.generator_object != None:
            self.generator_object.generate()

    def update(self):
        if self.input_mod > 0:
            self.input_mod +=1
        if InputHandler.inputs["space"]:
            self.input_mod = 1
        if self.input_mod == 1:
            self.generate()
        if self.input_mod > 15:
            self.input_mod = 0

        return super().update()
    