import os
import pygame

class SpriteLoader:
    """Class responsible for loading sprites from asset folder"""
    def __init__(self) -> None:
        self.__valid_image_formats = [".png"]
        self.__asset_folder = os.path.join(os.getcwd(), "assets")
        self.__sprites = self.load_all_sprites_in_folder(self.__asset_folder)

    @property
    def sprites(self):
        return self.__sprites

    def load_sprite(self, path : str) -> pygame.Surface:
        if ((not os.path.isfile(path)) or os.path.splitext(path)[1].lower() not in self.__valid_image_formats):
            return None
        return pygame.image.load(path)

    def get_all_filenames_in_folder(self, path : str) -> list[str]:
        return [
            filename
            for filename in os.listdir(path)
            if os.path.isfile(os.path.join(path, filename))
        ]

    def load_all_sprites_in_folder(self, path : str) -> dict:
        sprites = {}
        filenames = self.get_all_filenames_in_folder(path)
        for filename in filenames:
            full_path = os.path.join(path, filename)
            surface = self.load_sprite(full_path)
            if surface is None:
                continue
            sprite_id = os.path.splitext(filename)[0]
            sprites[sprite_id] = surface
        return sprites
