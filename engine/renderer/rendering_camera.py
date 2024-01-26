from pygame.math import Vector2
import pygame

class RenderingCamera:
    def __init__(self, screen : pygame.Surface) -> None:
        self.position = Vector2(0,0)
        self.render_scale = 1
        self.__screen = screen
        self.camera_verts_world = self.__get_camera_verts()
    
    def screen_to_world_coordinates(self, screen_pos: Vector2) -> Vector2:
        screen_center = Vector2(self.__screen.get_width()/2, self.__screen.get_height()/2)
        world_coordinates = Vector2((screen_pos.x - screen_center.x) * self.render_scale + self.position.x, (screen_center.y-screen_pos.y) * self.render_scale + self.position.y)
        return world_coordinates

    def world_to_screen_coordinates(self, world_pos: Vector2) -> Vector2:
        screen_center = Vector2(self.__screen.get_width()/2, self.__screen.get_height()/2)
        screen_coordinates = Vector2(((world_pos.x - self.position.x) / self.render_scale) + screen_center.x, screen_center.y-((world_pos.y - self.position.y) / self.render_scale))   
        return screen_coordinates
    
    def __get_camera_verts(self):
        screen_verts = [
                        Vector2(0, 0),
                        Vector2(self.__screen.get_width(), 0),
                        Vector2(self.__screen.get_width(), self.__screen.get_height()),
                        Vector2(0, self.__screen.get_height())
                        ]
        world_verts = [self.screen_to_world_coordinates(sv) for sv in screen_verts]
        return world_verts