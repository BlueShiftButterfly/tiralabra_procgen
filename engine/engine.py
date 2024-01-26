import pygame
from engine.renderer.renderer import Renderer
from engine.input_handler.input_handler import InputHandler

class Engine:
    def __init__(self) -> None:
        pygame.init()
        self.__renderer = Renderer()
        self.__input_handler = InputHandler()
        self.__loop = True

    def run(self):
        while self.__loop:
            self.update()            

    def update(self):
        self.__input_handler.handle_events()
        self.__renderer.render()

    def halt(self):
        self.__loop = False

    def unhalt(self):
        self.__loop = True