from pygame import Vector2
from engine.objects.object import Object
from engine.renderer.rendering_camera import RenderingCamera
from engine.input_handler.input_handler import InputHandler

class Camera(Object):
    def __init__(self, object_id: str, position: Vector2, camera : RenderingCamera) -> None:
        super().__init__(object_id, position, None)
        self.rendering_camera = camera
        self.speed = 10
        self.min_zoom = 0.3
        self.max_zoom = 20
        self.zoom_speed = 2

    def move(self, direction : Vector2, delta_time : float):
        self.position += direction.normalize() * self.speed * self.rendering_camera.zoom * delta_time

    def zoom_in(self, amount):
        self.rendering_camera.zoom = max(self.rendering_camera.zoom - (amount * self.rendering_camera.zoom), self.min_zoom)

    def zoom_out(self, amount):
        self.rendering_camera.zoom = min(self.rendering_camera.zoom + (amount * self.rendering_camera.zoom), self.max_zoom)

    def update(self, delta_time : float):
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
            self.move(move_direction, delta_time)
        if InputHandler.inputs["zoom_in"]:
            self.zoom_in(delta_time * self.zoom_speed)
        if InputHandler.inputs["zoom_out"]:
            self.zoom_out(delta_time * self.zoom_speed)
        if self.rendering_camera is not None:
            self.rendering_camera.position = self.position
        return super().update(delta_time)
