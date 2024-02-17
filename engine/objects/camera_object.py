from pygame import Vector2
from engine.objects.object import Object
from engine.renderer.rendering_camera import RenderingCamera
from engine.input_handler.input_handler import InputHandler

class Camera(Object):
    def __init__(self, object_id: str, position: Vector2, camera : RenderingCamera) -> None:
        super().__init__(object_id, position, None)
        self.rendering_camera = camera
        self.speed = 0.2
        self.min_zoom = 0.3
        self.max_zoom = 20

    def move(self, direction : Vector2):
        self.position += direction.normalize() * self.speed * self.rendering_camera.zoom

    def zoom_in(self):
        self.rendering_camera.zoom = max(self.rendering_camera.zoom - (0.1 * self.rendering_camera.zoom), self.min_zoom)

    def zoom_out(self):
        self.rendering_camera.zoom = min(self.rendering_camera.zoom + (0.1 * self.rendering_camera.zoom), self.max_zoom)

    def update(self):
        move_direction = Vector2(0,0)
        if InputHandler.inputs["up"]:
            move_direction.y += 1
        if InputHandler.inputs["down"]:
            move_direction.y += -1
        if InputHandler.inputs["left"]:
            move_direction.x += -1
        if InputHandler.inputs["right"]:
            move_direction.x += 1
        if move_direction != Vector2(0,0):
            self.move(move_direction)
        if InputHandler.inputs["zoom_in"]:
            self.zoom_in()
        if InputHandler.inputs["zoom_out"]:
            self.zoom_out()
        if self.rendering_camera is not None:
            self.rendering_camera.position = self.position
        return super().update()
