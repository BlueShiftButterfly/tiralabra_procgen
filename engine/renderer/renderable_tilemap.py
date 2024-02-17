import os
from pygame import Vector2
from pygame import Rect
import pygame
from engine.renderer.renderable_types import RenderableType
from engine.renderer.renderable import Renderable

class Tile:
    def __init__(self, x : int, y : int, surface : pygame.Surface) -> None:
        self.x = x
        self.y = y
        self.surface = surface

class TileChunk:
    def __init__(self, x : int, y : int, surface : pygame.Surface) -> None:
        self.x = x
        self.y = y
        self.surface = surface

class RenderableTilemap(Renderable):
    TILE_CHUNK_SIZE = 16
    """Used to render rects by the render queue"""
    def __init__(self, position : Vector2, tiles : list[Tile] = []) -> None:
        super().__init__()
        self.type = RenderableType.TILEMAP
        self.position = position
        self.update_chunk_cache = True
        self.chunk_cache = {}
        self.tiles = tiles
        # WIP
        size = 128
        for y in range(size):
            for x in range(size):
                img = pygame.image.load(os.path.join(os.getcwd(), "assets", "tile.png"))
                pygame.draw.rect(img, (abs(x) * (255 // size), abs(y) * (255 // size), 64), Rect(0, 0, 32, 32))
                self.tiles.append(Tile(x, y, img))
        self.tile_size = self.tiles[0].surface.get_width()
        self.bounding_box = (Vector2(-size, -size), Vector2(size, size))
        print(self.tile_size)
