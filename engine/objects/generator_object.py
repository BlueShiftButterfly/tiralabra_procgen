from pygame import Vector2
from engine.input_handler.input_handler import InputHandler
from engine.objects.object import Object

class GeneratorObject(Object):
    def __init__(self, object_id: str, position: Vector2 = Vector2(0,0), generator_object = None) -> None:
        super().__init__(object_id, position, None)
        self.generator_object = generator_object
        # TODO: Remove this and replace with proper handling for inputs that should fire only once when button pressed
        self.input_mod = 0
        # TODO: Also make this a more elegant solution at some point
        self.__thread_check_timer = 0

    def generate(self, seed: int = None, size: int = 256, amount: int = 64):
        if self.generator_object is not None:
            if self.generator_object.is_generating is False:
                self.generator_object.start_generation_thread(seed=seed, size=size, amount=amount)
                self.__thread_check_timer = 1

    def update(self, delta_time : float):
        if self.__thread_check_timer > 0:
            self.__thread_check_timer +=1
        if self.__thread_check_timer > 30:
            if self.generator_object.is_generating is False:
                self.__thread_check_timer = 0
            else:
                self.__thread_check_timer = 1
        if self.generator_object.is_generating and self.__thread_check_timer == 1:
            self.generator_object.update_generation_thread_status()
        if self.input_mod > 0:
            self.input_mod +=1
        #if InputHandler.inputs["space"] and self.generator_object.is_generating is False:
        #    self.input_mod = 1
        if self.input_mod == 1:
            self.generate()
        if self.input_mod > 15:
            self.input_mod = 0
        return super().update(delta_time)
