import pygame
from engine.renderer.renderer import Renderer
from engine.input_handler.input_handler import InputHandler

class Engine:
    """Engine class is the main wrapper of the pygame based game engine. 
        All engine functionality initialized here, also runs main loop"""
    def __init__(self) -> None:
        pygame.init()
        self.__renderer = Renderer()
        self.__input_handler = InputHandler()
        self.__loop = True

    @property
    def renderer(self):
        """Read-only reference to the renderer"""
        return self.__renderer

    @property
    def input_handler(self):
        """Read-only reference to the input handler"""
        return self.__input_handler

    def run(self):
        """Starts the main loop"""
        while self.__loop:
            self.update()

    def update(self):
        """The main program loop. Runs every frame"""
        self.__input_handler.handle_events()
        self.__renderer.render()

    def halt(self):
        """Halts the main update loop"""
        self.__loop = False

    def unhalt(self):
        """Resumes the main loop"""
        self.__loop = True
