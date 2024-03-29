from pygame import Vector2
import pygame
from engine.renderer.renderable_types import RenderableType
from engine.renderer.renderable import Renderable

class VisualTile:
    def __init__(self, x : int, y : int, surface : pygame.Surface) -> None:
        self.x = x
        self.y = y
        self.surface = surface

class RenderableTilemap(Renderable):
    TILE_CHUNK_SIZE = 8
    """Used to render rects by the render queue"""
    def __init__(self, position : Vector2, tiles : list[VisualTile] = []) -> None:
        super().__init__()
        self.type = RenderableType.TILEMAP
        self.position = position
        self.update_chunk_cache = True
        self.chunk_cache = {}
        self.tiles = tiles
        self.tile_size = self.get_tile_size()
        self.bounding_box = self.calculate_bounds()
        self.generate_chunks()

    def set_tiles(self, tiles : list[VisualTile]):
        self.tiles = tiles
        self.tile_size = self.get_tile_size()
        self.bounding_box = self.calculate_bounds()
        self.generate_chunks()

    def calculate_bounds(self) -> tuple[Vector2, Vector2]:
        bounding_box = None
        if len(self.tiles) > 0:
            bounding_box = (
                Vector2(
                    self.tiles[0].x + self.position.x,
                    self.tiles[0].y + self.position.y
                ),
                Vector2(
                    self.tiles[0].x + self.position.x,
                    self.tiles[0].y + self.position.y
                )
            )
        else:
            return (self.position, self.position)
        for t in self.tiles:
            bounding_box = (
                Vector2(
                    min(bounding_box[0].x, t.x + self.position.x),
                    min(bounding_box[0].y, t.y + self.position.y)
                ),
                Vector2(
                    max(bounding_box[1].x, t.x + self.position.x),
                    max(bounding_box[1].y, t.y + self.position.y)
                )
            )
        return bounding_box

    def get_tile_size(self) -> int:
        return 32

    def generate_chunks(self):
        for t in self.tiles:
            chunk_pos = (
                (t.x // RenderableTilemap.TILE_CHUNK_SIZE),
                (t.y // RenderableTilemap.TILE_CHUNK_SIZE)
            )
            chunk_inside_pos = (
                t.x % RenderableTilemap.TILE_CHUNK_SIZE,
                t.y % RenderableTilemap.TILE_CHUNK_SIZE
            )
            chunk_key = str(chunk_pos)
            if chunk_key in self.chunk_cache.keys():
                self.chunk_cache[chunk_key].surface.blit(
                    t.surface,
                    (
                        self.tile_size *
                        chunk_inside_pos[0],
                        self.tile_size *
                        (self.TILE_CHUNK_SIZE - chunk_inside_pos[1] - 1)
                    )
                )
            else:
                self.chunk_cache[chunk_key] = VisualTile(
                    chunk_pos[0],
                    chunk_pos[1],
                    pygame.Surface(
                        (
                            RenderableTilemap.TILE_CHUNK_SIZE * self.tile_size,
                            RenderableTilemap.TILE_CHUNK_SIZE * self.tile_size
                        )
                    )
                )
                self.chunk_cache[chunk_key].surface.blit(
                    t.surface,
                    (
                        self.tile_size * chunk_inside_pos[0],
                        self.tile_size * (self.TILE_CHUNK_SIZE - chunk_inside_pos[1] -1)
                    )
                )
