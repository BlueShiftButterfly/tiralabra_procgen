from collections import deque
from engine.renderer.renderable_rect import RenderableRect
from engine.renderer.rendering_camera import RenderingCamera
import pygame
from pygame.math import Vector2
from engine.renderer.renderable_types import RenderableType
from pygame import Rect

class Renderer:
    def __init__(self) -> None:
        self.__render_queue = deque()
        self.set_resolution((1280, 720))
        self.__target_framerate = 60
        self.__frame_clock = pygame.time.Clock()
        self.rendering_camera = RenderingCamera(self.__screen)
        self.total_render_scale = self.rendering_camera.render_scale * self.__get_pixels_per_unit()

    def set_resolution(self, resolution : tuple):
        self.__screen = pygame.display.set_mode(resolution)

    def add_to_queue(self, renderable : RenderableRect):
        self.__render_queue.append(renderable)

    def render(self):
        self.__frame_clock.tick(self.__target_framerate)
        self.__screen.fill((0,0,0))

        for rendereable in self.__render_queue:
            
            if rendereable.type == RenderableType.RECT:
                self.__render_rect(rendereable)
        self.__render_queue.clear()
        pygame.display.update()

    def __render_rect(self, rendereable_rect : RenderableRect):
        return pygame.draw.rect(self.__screen, rendereable_rect.color, self.__world_to_screen_rect(rendereable_rect.rect), int(rendereable_rect.width * self.total_render_scale), int(rendereable_rect.border_radius * self.total_render_scale))

    def __world_to_screen_rect(self, rect : Rect):
        pos = self.rendering_camera.world_to_screen_coordinates(Vector2(rect.left, rect.top))
        return Rect(pos.x, pos.y, int(rect.width * self.total_render_scale), int(rect.height * self.total_render_scale))

    def __get_units_per_pixel(self):
        return 1 / (self.__screen.get_height() / 16)
    
    def __get_pixels_per_unit(self):
        return self.__screen.get_height() / 16