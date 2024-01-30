from pygame import Vector2
from engine.objects.object import Object
from engine.renderer.renderable import Renderable
from engine.renderer.rendering_camera import RenderingCamera

class Camera(Object):
    def __init__(self, id: str, position: Vector2, camera : RenderingCamera) -> None:
        super().__init__(id, position, None)
        self.rendering_camera = camera
        self.speed = 0.2
        self.min_zoom = 0.0001
        self.max_zoom = 1000000

    def move(self, direction : Vector2):
        self.position += direction * self.speed * self.rendering_camera.zoom
    
    def zoom_in(self):
        self.rendering_camera.zoom = max(self.rendering_camera.zoom - (0.1 * self.rendering_camera.zoom), self.min_zoom)
    
    def zoom_out(self):
        self.rendering_camera.zoom = min(self.rendering_camera.zoom + (0.1 * self.rendering_camera.zoom), self.max_zoom)

    def update(self):
        if self.rendering_camera != None:
            self.rendering_camera.position = self.position
        return super().update()
    