import math
from collections import deque
import pygame
import pygame_gui
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
    def __init__(
            self,
            render_resolution: tuple[int, int] = (1280, 720),
            target_fps: int = 120,
            pygame_render_flags:int = 0,
            draw_debug_text: bool = False
        ) -> None:
        self.__render_queue = deque()
        self.__screen = pygame.display.set_mode(render_resolution, pygame_render_flags)
        self.__target_framerate = target_fps
        self.__frame_clock = pygame.time.Clock()
        self.__rendering_camera = RenderingCamera(self.__screen)
        self.__debug_font : pygame.font.Font = pygame.font.SysFont(pygame.font.get_default_font(), 24)
        self.__delta_time = 0
        self.draw_calls = 0
        self.ui_manager = None
        self.loading = False
        self.__loading_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.__load_image = None
        self.__load_rotation = 0
        self.__draw_debug_text = draw_debug_text

    @property
    def rendering_camera(self):
        return self.__rendering_camera

    @property
    def delta_time(self):
        return self.__delta_time

    def set_ui_manager(self, ui_manager):
        self.ui_manager = ui_manager

    def set_load_image(self, load_image: pygame.Surface):
        self.__load_image = load_image
        self.__loading_surface.blit(self.__load_image, (0,0))

    def add_to_queue(self, renderable):
        self.__render_queue.append(renderable)

    def add_list_to_queue(self, renderable_list):
        self.__render_queue.extend(renderable_list)

    def render(self):
        self.draw_calls = 0
        fps = self.__frame_clock.get_fps()
        if fps == 0:
            self.__delta_time = 99999999999
        else:
            self.__delta_time = (1 / self.__frame_clock.get_fps())
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

        if self.__draw_debug_text:
            self.__render_debug_text()
        
        self.__frame_clock.tick_busy_loop(self.__target_framerate)
        self.ui_manager.update(self.__delta_time)
        self.ui_manager.draw_ui(self.__screen)
        if self.loading:
            self.__load_rotation += 360 * self.__delta_time
            rotated_load_image = pygame.transform.rotate(self.__loading_surface, self.__load_rotation)
            new_load_rect = rotated_load_image.get_rect(center=self.__loading_surface.get_rect(topleft=(32, self.__screen.get_height()-48)).center)
            self.__screen.blit(rotated_load_image, new_load_rect)
        else:
            self.__load_rotation = 0
        pygame.display.update()
        self.__render_queue.clear()

    def __render_debug_text(self):
        self.__screen.blit(
            self.__debug_font.render(
                "FPS: "+str(self.__frame_clock.get_fps()),
                True,
                color_prefabs.WHITE
            ),
            (15, 25)
        )
        self.__screen.blit(
            self.__debug_font.render(
                "Frametime: "+str(self.__frame_clock.get_time()),
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
                "Draw calls: "+str(self.draw_calls),
                True,
                color_prefabs.WHITE
            ),
            (15, 105)
        )

    def __render_rect(self, rendereable_rect : RenderableRect):
        self.draw_calls += 1
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
        self.draw_calls += 1
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
        self.draw_calls += 1
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
                self.draw_calls += 1
            elif x % 10 == 0:
                pygame.draw.line(self.__screen, color_prefabs.GRAY, startpos, endpos)
                self.draw_calls += 1
            elif self.rendering_camera.total_render_scale < 0.1:
                pygame.draw.line(self.__screen, color_prefabs.DARK_GRAY, startpos, endpos)
                self.draw_calls += 1

        for y in range(-size, size+1):
            if not self.rendering_camera.is_rect_inside_bounds(Vector2(-size, y-0.1), Vector2(size, y+0.1)):
                continue
            startpos = self.__rendering_camera.world_to_screen_coordinates(Vector2(-size, y))
            endpos = self.__rendering_camera.world_to_screen_coordinates(Vector2(size, y))
            if y == 0:
                pygame.draw.line(self.__screen, color_prefabs.RED, startpos, endpos)
                self.draw_calls += 1
            elif y % 10 == 0:
                pygame.draw.line(self.__screen, color_prefabs.GRAY, startpos, endpos)
                self.draw_calls += 1
            elif self.rendering_camera.total_render_scale < 0.1:
                pygame.draw.line(self.__screen, color_prefabs.DARK_GRAY, startpos, endpos)
                self.draw_calls += 1

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
            self.draw_calls += 1
            self.__screen.blit(
                scaled_surf,
                self.rendering_camera.world_to_screen_coordinates(
                    Vector2(
                        tc.x * RenderableTilemap.TILE_CHUNK_SIZE + renderable_tilemap.position.x,
                        tc.y * RenderableTilemap.TILE_CHUNK_SIZE + RenderableTilemap.TILE_CHUNK_SIZE + renderable_tilemap.position.y
                    )
                )
            )
        