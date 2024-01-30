from pygame import Vector2
from engine.objects.object import Object
from engine.renderer.renderable import Renderable
from engine.renderer.rendering_camera import RenderingCamera

class Camera(Object):
    def __init__(self, id: str, position: Vector2, camera : RenderingCamera) -> None:
        super().__init__(id, position, None)
        self.rendering_camera = camera
    
    def update(self):
        if self.rendering_camera != None:
            self.rendering_camera.position = self.position
        return super().update()
    