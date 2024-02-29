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
from engine.renderer.renderable_tilemap import RenderableTilemap

from engine.renderer import color_prefabs

class Renderer:
    """Class responsible for rendering objects using pygame,
    including handling framerate and resolution."""
    def __init__(self) -> None:
        self.__render_queue = deque()
        self.set_resolution((1280, 720))
        self.target_framerate = 300
        self.frame_clock = pygame.time.Clock()
        self.__rendering_camera = RenderingCamera(self.__screen)
        self.__debug_font : pygame.font.Font = pygame.font.SysFont(pygame.font.get_default_font(), 24)
        self.__delta_time = 0

    @property
    def rendering_camera(self):
        return self.__rendering_camera

    @property
    def delta_time(self):
        return self.__delta_time

    def set_resolution(self, resolution : tuple):
        self.__screen = pygame.display.set_mode(resolution)

    def add_to_queue(self, renderable):
        self.__render_queue.append(renderable)

    def add_list_to_queue(self, renderable_list):
        self.__render_queue.extend(renderable_list)

    def render(self):
        fps = self.frame_clock.get_fps()
        if fps == 0:
            self.__delta_time = 99999999999
        else:
            self.__delta_time = (1 / self.frame_clock.get_fps())
        self.__screen.fill((0,0,0))

        for rendereable in sorted(self.__render_queue, key=lambda r: r.sorting_layer):
            if (not self.rendering_camera.is_rect_inside_bounds(
                rendereable.bounding_box[0],
                rendereable.bounding_box[1]
                )):
                continue
            if rendereable.type == RenderableType.RECT:
                self.__render_rect(rendereable)
            if rendereable.type == RenderableType.LINE:
                self.__render_line(rendereable)
            if rendereable.type == RenderableType.DEBUG_GRID:
                self.__render_world_grid()
            if rendereable.type == RenderableType.CIRCLE:
                self.__render_circle(rendereable)
            if rendereable.type == RenderableType.TILEMAP:
                self.__render_tilemap(rendereable)

        self.__screen.blit(
            self.__debug_font.render(
                "FPS: "+str(self.frame_clock.get_fps()),
                True,
                color_prefabs.WHITE
            ),
            (15, 25)
        )
        self.__screen.blit(
            self.__debug_font.render(
                "Frametime: "+str(self.frame_clock.get_time()),
                True,
                color_prefabs.WHITE
            ),
            (15, 45)
        )
        self.__screen.blit(
            self.__debug_font.render(
                "Frametime custom: "+str(self.__delta_time),
                True,
                color_prefabs.WHITE
            ),
            (15, 65)
        )
        self.__screen.blit(
            self.__debug_font.render(
                str(self.rendering_camera.total_render_scale),
                True,
                color_prefabs.WHITE
            ),
            (15, 85)
        )
        self.__screen.blit(
            self.__debug_font.render(
                "SPACE: generate map     ESC: quit program     W/A/S/D: move camera     Q/E:zoom in/out",
                True,
                color_prefabs.WHITE
            ),
            (15, 5)
        )

        pygame.display.update()
        self.__render_queue.clear()
        self.frame_clock.tick_busy_loop(self.target_framerate)

    def __render_rect(self, rendereable_rect : RenderableRect):
        screen_position = self.rendering_camera.world_to_screen_coordinates(rendereable_rect.position)
        return pygame.draw.rect(
            self.__screen,
            rendereable_rect.color,
            Rect(
                screen_position.x,
                screen_position.y - math.floor(rendereable_rect.height / self.rendering_camera.total_render_scale),
                rendereable_rect.width / self.rendering_camera.total_render_scale,
                rendereable_rect.height / self.rendering_camera.total_render_scale
            ),
            int(rendereable_rect.width / self.__rendering_camera.total_render_scale),
            int(rendereable_rect.border_radius / self.__rendering_camera.total_render_scale)
        )

    def __render_line(self, renderable_line : RenderableLine):
        if renderable_line.anti_aliased:
            return pygame.draw.aaline(
                self.__screen,
                renderable_line.color,
                self.__rendering_camera.world_to_screen_coordinates(renderable_line.position),
                self.__rendering_camera.world_to_screen_coordinates(renderable_line.end_position),
                max(1, int(renderable_line.width / self.rendering_camera.total_render_scale))
            )
        return pygame.draw.line(
            self.__screen,
            renderable_line.color,
            self.__rendering_camera.world_to_screen_coordinates(renderable_line.position),
            self.__rendering_camera.world_to_screen_coordinates(renderable_line.end_position),
            max(1, int(renderable_line.width / self.rendering_camera.total_render_scale))
        )

    def __render_circle(self, renderable_circle : RenderableCircle):
        br = int(max(1, renderable_circle.border_width / self.rendering_camera.total_render_scale))
        if renderable_circle.is_filled:
            br = 0
        return pygame.draw.circle(
            self.__screen,
            renderable_circle.color,
            self.rendering_camera.world_to_screen_coordinates(renderable_circle.position),
            renderable_circle.radius / self.rendering_camera.total_render_scale,
            br
        )

    def __render_world_grid(self):
        size = 256
        for x in range(-size, size+1):
            if not self.rendering_camera.is_rect_inside_bounds(Vector2(x-0.1, -size), Vector2(x+0.1, size)):
                continue
            startpos = self.__rendering_camera.world_to_screen_coordinates(Vector2(x, -size))
            endpos = self.__rendering_camera.world_to_screen_coordinates(Vector2(x, size))
            if x == 0:
                pygame.draw.line(self.__screen, color_prefabs.GREEN, startpos, endpos)
            elif x % 10 == 0:
                pygame.draw.line(self.__screen, color_prefabs.GRAY, startpos, endpos)
            elif self.rendering_camera.total_render_scale < 0.1:
                pygame.draw.line(self.__screen, color_prefabs.DARK_GRAY, startpos, endpos)

        for y in range(-size, size+1):
            if not self.rendering_camera.is_rect_inside_bounds(Vector2(-size, y-0.1), Vector2(size, y+0.1)):
                continue
            startpos = self.__rendering_camera.world_to_screen_coordinates(Vector2(-size, y))
            endpos = self.__rendering_camera.world_to_screen_coordinates(Vector2(size, y))
            if y == 0:
                pygame.draw.line(self.__screen, color_prefabs.RED, startpos, endpos)
            elif y % 10 == 0:
                pygame.draw.line(self.__screen, color_prefabs.GRAY, startpos, endpos)
            elif self.rendering_camera.total_render_scale < 0.1:
                pygame.draw.line(self.__screen, color_prefabs.DARK_GRAY, startpos, endpos)

    def __render_tilemap(self, renderable_tilemap : RenderableTilemap): 
        for tc in renderable_tilemap.chunk_cache.values():
            if (not self.rendering_camera.is_rect_inside_bounds(
                Vector2(
                    tc.x * RenderableTilemap.TILE_CHUNK_SIZE + renderable_tilemap.position.x,
                    tc.y * RenderableTilemap.TILE_CHUNK_SIZE + renderable_tilemap.position.y
                ),
                Vector2(
                    tc.x * RenderableTilemap.TILE_CHUNK_SIZE + RenderableTilemap.TILE_CHUNK_SIZE + renderable_tilemap.position.x,
                    tc.y * RenderableTilemap.TILE_CHUNK_SIZE + RenderableTilemap.TILE_CHUNK_SIZE + renderable_tilemap.position.y
                )
            )):
                continue
            scaled_surf = pygame.transform.scale(
                tc.surface,
                (
                    RenderableTilemap.TILE_CHUNK_SIZE // self.rendering_camera.total_render_scale+1,
                    RenderableTilemap.TILE_CHUNK_SIZE // self.rendering_camera.total_render_scale+1
                )
            )
            self.__screen.blit(
                scaled_surf,
                self.rendering_camera.world_to_screen_coordinates(
                    Vector2(
                        tc.x * RenderableTilemap.TILE_CHUNK_SIZE + renderable_tilemap.position.x,
                        tc.y * RenderableTilemap.TILE_CHUNK_SIZE + RenderableTilemap.TILE_CHUNK_SIZE + renderable_tilemap.position.y
                    )
                )
            )
        