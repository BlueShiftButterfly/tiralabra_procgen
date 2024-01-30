from pygame import Vector2, Color
import uuid
from engine.objects.object import Object
from engine.renderer.renderable import Renderable
from engine.renderer.renderable_line import RenderableLine
from engine.renderer.renderable_rect import RenderableRect
from engine.renderer.renderable_circle import RenderableCircle
from engine.renderer.renderable_debug_grid import RenderableDebugGrid
from engine.renderer.rendering_camera import RenderingCamera
from engine.objects.camera_object import Camera
from engine.renderer.colors import ColorPrefabs

class ObjectHandler:
    def __init__(self) -> None:
        self.__objects : dict = {}
        self.__builting_camera_id = "MAIN_CAMERA"
    
    def get_new_uuid(self) -> str:
        return str(uuid.uuid4())

    def create_line(self, start : Vector2, end : Vector2):
        id = self.get_new_uuid()
        self.__objects[id] = Object(id, start, RenderableLine(start, end, color=ColorPrefabs.GREEN))
        return id

    def create_point(self, position : Vector2, color : Color = ColorPrefabs.RED):
        id = self.get_new_uuid()
        self.__objects[id] = Object(id, position, RenderableCircle(position, color=color, radius=0.1, is_filled=True))
        return 
    
    def create_circle(self, position : Vector2, radius : float, border_width : float, is_filled : bool):
        id = self.get_new_uuid()
        self.__objects[id] = Object(id, position, RenderableCircle(position, color=ColorPrefabs.RED, radius=radius, border_width=border_width, is_filled=is_filled))
        return id
    
    def create_debug_grid(self):
        id = self.get_new_uuid()
        self.__objects[id] = Object(id, Vector2(0,0), RenderableDebugGrid())
        return id

    def create_camera(self, position : Vector2, rendering_camera : RenderingCamera):
        id = self.__builting_camera_id
        self.__objects[id] = Camera(id, position, rendering_camera)
        return id

    def get_object_from_id(self, id : str):
        return self.__objects[id]
    
    def get_rendering_components(self) -> list:
        components = []
        for object in self.__objects.values():
            if object.renderable_component is not None:
                components.append(object.renderable_component)
        return components

    def delete_object(self, id : str):
        self.__objects.pop(id)

    def update_objects(self):
        #print(len(self.__objects))
        for object in self.__objects.values():
            object.update()