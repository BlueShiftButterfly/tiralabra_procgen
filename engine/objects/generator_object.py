from pygame import Vector2
from engine.input_handler.input_handler import InputHandler
from engine.objects.object import Object

class GeneratorObject(Object):
    def __init__(self, id: str, position: Vector2 = Vector2(0,0), generator_object = None) -> None:
        super().__init__(id, position, None)
        self.generator_object = generator_object
        self.input_mod = 0 # TODO: Remove this and replace with proper handling for inputs that should fire only once when button pressed
        self.__thread_check_timer = 0 # Also make this a more elegant solution at some point
    
    def generate(self):
        if self.generator_object != None:
            if self.generator_object.is_generating == False:
                self.generator_object.start_generation()
                self.__thread_check_timer = 1

    def update(self):
        if self.__thread_check_timer > 0:
            self.__thread_check_timer +=1
        if self.__thread_check_timer > 30:
            if self.generator_object.is_generating == False:
                self.__thread_check_timer = 0
            else:
                self.__thread_check_timer = 1
        if self.generator_object.is_generating and self.__thread_check_timer == 1:
            self.generator_object.check_generation()
        if self.input_mod > 0:
            self.input_mod +=1
        if InputHandler.inputs["space"] and self.generator_object.is_generating == False:
            self.input_mod = 1
        if self.input_mod == 1:
            self.generate()
        if self.input_mod > 15:
            self.input_mod = 0
        return super().update()
    