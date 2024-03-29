from pygame import Vector2
import pygame

class RenderingCamera:
    """Responsible for camera functionality when rendering
        and calculating object coordinates independent of resolution and camera position"""
    def __init__(self, screen : pygame.Surface) -> None:
        self.position = Vector2(0,0)
        self.__screen = screen
        self.screen_center = Vector2(self.__screen.get_width()/2, self.__screen.get_height()/2)
        self.__units_per_pixel = 1 / (self.__screen.get_height() / 16)
        self.zoom = 1
        self.camera_verts_world = self.__get_camera_verts()

    @property
    def total_render_scale(self):
        return (self.zoom) * self.__units_per_pixel

    def __get_camera_verts(self):
        screen_verts = [
            Vector2(0, 0),
            Vector2(self.__screen.get_width(), 0),
            Vector2(self.__screen.get_width(), self.__screen.get_height()),
            Vector2(0, self.__screen.get_height())
            ]
        world_verts = [self.screen_to_world_coordinates(sv) for sv in screen_verts]
        return world_verts

    def screen_to_world_coordinates(self, screen_pos: Vector2) -> Vector2:
        """Converts pygame screen coordinates to custom 2D world coordinate system"""
        screen_center = self.screen_center
        world_coordinates = Vector2((screen_pos.x - screen_center.x) * self.total_render_scale + self.position.x,
                                    (screen_center.y-screen_pos.y) * self.total_render_scale + self.position.y)
        return world_coordinates

    def world_to_screen_coordinates(self, world_pos: Vector2) -> Vector2:
        """Converts custom 2D world coordinate system to pygame screen coordinates"""
        screen_center = self.screen_center
        screen_coordinates = Vector2(((world_pos.x - self.position.x) / self.total_render_scale) + screen_center.x,
                                        screen_center.y-((world_pos.y - self.position.y) / self.total_render_scale))
        return screen_coordinates

    def is_rect_inside_bounds(self, min_pos : Vector2, max_pos : Vector2):
        self.camera_verts_world = self.__get_camera_verts()
        if (min_pos.x <= self.camera_verts_world[1].x and
            max_pos.x >= self.camera_verts_world[3].x and
            min_pos.y <= self.camera_verts_world[1].y and
            max_pos.y >= self.camera_verts_world[3].y):
            return True
        
        return False
