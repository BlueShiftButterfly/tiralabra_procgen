from collections import deque
from engine.renderer.renderable_rect import RenderableRect
from engine.renderer.renderable_line import RenderableLine
from engine.renderer.renderable_debug_grid import RenderableDebugGrid
from engine.renderer.rendering_camera import RenderingCamera
import pygame
from pygame.math import Vector2
from engine.renderer.renderable_types import RenderableType
from pygame import Rect
from engine.renderer.colors import ColorPrefabs
import math

class Renderer:
    def __init__(self) -> None:
        self.__render_queue = deque()
        self.set_resolution((1280, 720))
        self.__target_framerate = 60
        self.__frame_clock = pygame.time.Clock()
        self.__rendering_camera = RenderingCamera(self.__screen)

    def set_resolution(self, resolution : tuple):
        self.__screen = pygame.display.set_mode(resolution)

    def add_to_queue(self, renderable):
        self.__render_queue.append(renderable)

    def render(self):
        self.__frame_clock.tick(self.__target_framerate)
        self.__screen.fill((0,0,0))
        
        for rendereable in sorted(self.__render_queue):
            if rendereable.type == RenderableType.RECT:
                self.__render_rect(rendereable)
            if rendereable.type == RenderableType.LINE:
                self.__render_line(rendereable)
            if rendereable.type == RenderableType.DEBUG_GRID:
                self.__draw_world_grid(rendereable)

        self.__render_queue.clear()
        pygame.display.update()

    def __render_rect(self, rendereable_rect : RenderableRect):
        return pygame.draw.rect(self.__screen, rendereable_rect.color, self.__world_to_screen_rect(rendereable_rect.rect), int(rendereable_rect.width * self.__rendering_camera.total_render_scale), int(rendereable_rect.border_radius * self.__rendering_camera.total_render_scale))

    def __render_line(self, renderable_line : RenderableLine):
        if renderable_line.anti_aliased:
            return pygame.draw.aaline(self.__screen, renderable_line.color, self.__rendering_camera.world_to_screen_coordinates(renderable_line.start_position), self.__rendering_camera.world_to_screen_coordinates(renderable_line.end_position), renderable_line.width)
        else:
            return pygame.draw.line(self.__screen, renderable_line.color, self.__rendering_camera.world_to_screen_coordinates(renderable_line.start_position), self.__rendering_camera.world_to_screen_coordinates(renderable_line.end_position), renderable_line.width)

    def __world_to_screen_rect(self, rect : Rect):
        pos = self.__rendering_camera.world_to_screen_coordinates(Vector2(rect.left, rect.top))
        return Rect(pos.x, pos.y, int(rect.width * self.__rendering_camera.total_render_scale), int(rect.height * self.__rendering_camera.total_render_scale))

    def __draw_world_grid(self, renderable_world_grid : RenderableDebugGrid):
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
        
