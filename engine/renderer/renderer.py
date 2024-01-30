import math
from collections import deque
import pygame
from pygame import Vector2
from pygame import Rect

from engine.renderer.renderable_rect import RenderableRect
from engine.renderer.renderable_line import RenderableLine
from engine.renderer.rendering_camera import RenderingCamera
from engine.renderer.renderable_types import RenderableType
from engine.renderer.renderable_circle import RenderableCircle

from engine.renderer.colors import ColorPrefabs

class Renderer:
    """Class responsible for rendering objects using pygame, including handling framerate and resolution."""
    def __init__(self) -> None:
        self.__render_queue = deque()
        self.set_resolution((1280, 720))
        self.__target_framerate = 60
        self.__frame_clock = pygame.time.Clock()
        self.__rendering_camera = RenderingCamera(self.__screen)

    @property
    def rendering_camera(self):
        return self.__rendering_camera

    def set_resolution(self, resolution : tuple):
        self.__screen = pygame.display.set_mode(resolution)

    def add_to_queue(self, renderable):
        self.__render_queue.append(renderable)

    def add_list_to_queue(self, renderable_list):
        self.__render_queue.extend(renderable_list)

    def render(self):
        #print(len(self.__render_queue))
        self.__frame_clock.tick(self.__target_framerate)
        self.__screen.fill((0,0,0))

        for rendereable in sorted(self.__render_queue, key=lambda r: r.sorting_layer):
            if rendereable.type == RenderableType.RECT:
                self.__render_rect(rendereable)
            if rendereable.type == RenderableType.LINE:
                self.__render_line(rendereable)
            if rendereable.type == RenderableType.DEBUG_GRID:
                self.__draw_world_grid()
            if rendereable.type == RenderableType.CIRCLE:
                self.__draw_circle(rendereable)

        pygame.display.update()
        self.__render_queue.clear()

    def __render_rect(self, rendereable_rect : RenderableRect):
        screen_position = self.rendering_camera.world_to_screen_coordinates(rendereable_rect.position)
        return pygame.draw.rect(self.__screen,
                                rendereable_rect.color,
                                Rect(screen_position.x, screen_position.y - math.floor(rendereable_rect.height / self.rendering_camera.total_render_scale), rendereable_rect.width / self.rendering_camera.total_render_scale, rendereable_rect.height / self.rendering_camera.total_render_scale),
                                int(rendereable_rect.width / self.__rendering_camera.total_render_scale),
                                int(rendereable_rect.border_radius / self.__rendering_camera.total_render_scale))

    def __render_line(self, renderable_line : RenderableLine):
        if renderable_line.anti_aliased:
            return pygame.draw.aaline(self.__screen,
                                      renderable_line.color,
                                      self.__rendering_camera.world_to_screen_coordinates(renderable_line.position),
                                      self.__rendering_camera.world_to_screen_coordinates(renderable_line.end_position),
                                      max(1, int(renderable_line.width / self.rendering_camera.total_render_scale)))

        return pygame.draw.line(self.__screen,
                                renderable_line.color,
                                self.__rendering_camera.world_to_screen_coordinates(renderable_line.position),
                                self.__rendering_camera.world_to_screen_coordinates(renderable_line.end_position),
                                max(1, int(renderable_line.width / self.rendering_camera.total_render_scale)))
    
    def __draw_circle(self, renderable_circle : RenderableCircle):
        br = int(max(1, renderable_circle.border_width / self.rendering_camera.total_render_scale))
        if renderable_circle.is_filled:
            br = 0
        return pygame.draw.circle(self.__screen, 
                                renderable_circle.color,
                                self.rendering_camera.world_to_screen_coordinates(renderable_circle.position),
                                renderable_circle.radius / self.rendering_camera.total_render_scale,
                                br)

    def __draw_world_grid(self):
        size = 20
        for x in range(-math.floor(self.__rendering_camera.position.x) - size, math.ceil(self.__rendering_camera.position.x) + size+1):
            startpos = self.__rendering_camera.world_to_screen_coordinates(Vector2(x, -size))
            endpos = self.__rendering_camera.world_to_screen_coordinates(Vector2(x, size))
            if x == 0:
                pygame.draw.line(self.__screen, ColorPrefabs.GREEN, startpos, endpos)
            else:
                pygame.draw.line(self.__screen, ColorPrefabs.GRAY, startpos, endpos)

        for y in range(-math.floor(self.__rendering_camera.position.y) - size, math.ceil(self.__rendering_camera.position.y) + size+1):
            startpos = self.__rendering_camera.world_to_screen_coordinates(Vector2(-size, y))
            endpos = self.__rendering_camera.world_to_screen_coordinates(Vector2(size, y))
            if y == 0:
                pygame.draw.line(self.__screen, ColorPrefabs.RED, startpos, endpos)
            else:
                pygame.draw.line(self.__screen, ColorPrefabs.GRAY, startpos, endpos)
