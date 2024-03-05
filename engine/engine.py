import pygame
from pygame import Vector2
from engine.event_handler import EventHandler
from engine.ui_handler import UIHandler
from engine.renderer.renderer import Renderer
from engine.input_handler.input_handler import InputHandler
from engine.objects.object_handler import ObjectHandler
from engine.resource_loader.sprite_loader import SpriteLoader

class Engine:
    """Engine class is the main wrapper of the pygame based game engine. 
        All engine functionality initialized here, also runs main loop"""
    def __init__(self, render_resolution: tuple[int, int] = (1280, 720), target_fps: int = 120, pygame_render_flags = 0, draw_debug_text: bool = False) -> None:
        pygame.init()
        self.__ui_handler = UIHandler()
        self.__event_handler = EventHandler(ui_handler_reference=self.__ui_handler)
        self.__renderer = Renderer(
            render_resolution=render_resolution,
            target_fps=target_fps,
            pygame_render_flags=pygame_render_flags,
            draw_debug_text=draw_debug_text
        )
        self.__input_handler = InputHandler()
        self.__object_handler = ObjectHandler()
        self.__sprite_loader = SpriteLoader()
        self.__loop = True
        self.__renderer.set_load_image(self.__sprite_loader.sprites["load_img"])
        self.__renderer.set_ui_manager(self.__ui_handler.ui_manager)

    @property
    def renderer(self):
        """Read-only reference to the renderer"""
        return self.__renderer

    @property
    def input_handler(self):
        """Read-only reference to the input handler"""
        return self.__input_handler

    @property
    def object_handler(self):
        """Read-only reference to the object handler"""
        return self.__object_handler

    @property
    def sprite_loader(self):
        return self.__sprite_loader

    @property
    def event_handler(self):
        return self.__event_handler

    @property
    def ui_handler(self):
        return self.__ui_handler

    def run(self):
        """Starts the main loop"""
        while self.__loop:
            self.update()

    def update(self):
        """The main program loop. Runs every frame"""
        self.__event_handler.handle_events()
        self.__input_handler.handle_input()
        self.__object_handler.update_objects(self.renderer.delta_time)
        self.__renderer.loading = self.__object_handler.loading           
        self.__renderer.add_list_to_queue(self.__object_handler.get_rendering_components())
        self.__renderer.render()

    def halt(self):
        """Halts the main update loop"""
        self.__loop = False

    def unhalt(self):
        """Resumes the main loop"""
        self.__loop = True
