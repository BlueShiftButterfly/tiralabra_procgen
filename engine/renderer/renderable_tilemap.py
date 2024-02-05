from pygame import Vector2
from pygame import Rect, Color
import pygame
import os
from engine.renderer.renderable_types import RenderableType
from engine.renderer.renderable import Renderable


class RenderableTilemap(Renderable):
    """Used to render rects by the render queue"""
    def __init__(self, position : Vector2) -> None:
        super().__init__()
        self.type = RenderableType.TILEMAP
        self.position = position
        self.base_sprite = pygame.transform.smoothscale(pygame.image.load(os.path.join(os.getcwd(), "assets", "tile.png")).convert(), (2, 2))
        self.sprites = []
        for y in range(0, 256):
            for x in range(0, 256):
                self.sprites.append((x,y))

        self.cached_surface = pygame.surface.Surface((256 * self.base_sprite.get_width(), 256 * self.base_sprite.get_height()))
        for pos in self.sprites:
            self.cached_surface.blit(self.base_sprite, (pos[0] * self.base_sprite.get_width(), pos[1] * self.base_sprite.get_height()))

    def __cmp___(self, other):
        return super().__cmp___(other)