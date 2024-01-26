from collections import deque
from engine.renderer.renderable import Renderable
from engine.renderer.rendering_camera import RenderingCamera
import pygame
from pygame.math import Vector2

class Renderer:
    def __init__(self, rendering_camera : RenderingCamera) -> None:
        self.__render_queue = deque()
        self.__screen = pygame.display.set_mode((1280, 720))
        self.__target_framerate = 60
        self.__frame_clock = pygame.time.Clock()

        self.__render_scale_modifier = 1
        self.__render_scale = self.__get_units_per_pixel() * self.__render_scale_modifier
        self.__rendering_camera = rendering_camera
        self.__rendering_camera_verts = self.__get_camera_verts()

    def set_resolution(self, resolution : tuple):
        self.__screen = pygame.display.set_mode(resolution)

    def add_to_queue(self, renderable : Renderable):
        self.__render_queue.append(renderable)

    def render(self):
        self.__frame_clock.tick(self.__target_framerate)
        for rendereable in self.__render_queue:
            pass
        #self.__screen.fill((0,0,0))
        #pygame.display.update()

    def __get_units_per_pixel(self):
        return 1 / (self.__screen.get_height() / 16)

    def sc_to_wc(self, screen_pos: Vector2) -> Vector2:
        """
        screen coordinates to world coordinates:
        s_x = (w_x - (screen_width/2)) * camera_scale + camera_x
        s_y = (-w_y + (screen_height/2)) * camera_scale + camera_y
        """
        cs = self.__render_scale
        sw_h = self.__screen.get_width()/2
        sh_h = self.__screen.get_height()/2
        c_x = self.__rendering_camera.position.x
        c_y = self.__rendering_camera.position.y
        wc = Vector2((screen_pos.x - sw_h) * cs + c_x, (sh_h-screen_pos.y) * cs + c_y)
        return wc

    def wc_to_sc(self, world_pos: Vector2) -> Vector2:
        """
        world coordinates to screen coordinates:
        w_x = ((s_x - camera_x) / camera_scale) + (screen.width/2)
        w_y = ((-s_y - camera_y) / camera_scale) + (screen.width/2)
        """
        cs = self.__render_scale
        sw_h = self.__screen.get_width()/2
        sh_h = self.__screen.get_height()/2
        c_x = self.__rendering_camera.position.x
        c_y = self.__rendering_camera.position.y
        sc = Vector2(((world_pos.x - c_x) / cs) + sw_h, sh_h-((world_pos.y - c_y) / cs))   
        return sc

    def set_render_scale(self, scale: float):
        self.__render_scale_modifier = scale
    
    def __get_camera_verts(self):
        screen_verts = [
                        Vector2(0, 0),
                        Vector2(self.__screen.get_width(), 0),
                        Vector2(self.__screen.get_width(), self.__screen.get_height()),
                        Vector2(0, self.__screen.get_height())
                        ]
        world_verts = [self.sc_to_wc(sv) for sv in screen_verts]
        return world_verts
    
    def is_object_inside_camera_view(self, renderable : Renderable):        
        buffer_amount_x = 20
        buffer_amount_y = 20

        if not self.__rendering_camera_verts[3].x-buffer_amount_x-1 < renderable.world_position.x < self.__rendering_camera_verts[1].x+buffer_amount_x:
            return False
        if not self.__rendering_camera_verts[3].y-buffer_amount_x-1 < renderable.world_position.y < self.__rendering_camera_verts[1].y+buffer_amount_y:
            return False    
        return True