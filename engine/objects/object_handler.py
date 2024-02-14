from pygame import Vector2, Color
import uuid
from engine.objects.object import Object
from engine.renderer.renderable import Renderable
from engine.renderer.renderable_line import RenderableLine
from engine.renderer.renderable_rect import RenderableRect
from engine.renderer.renderable_circle import RenderableCircle
from engine.renderer.renderable_debug_grid import RenderableDebugGrid
from engine.renderer.rendering_camera import RenderingCamera
from engine.renderer.renderable_tilemap import RenderableTilemap
from engine.objects.camera_object import Camera
from engine.objects.generator_object import GeneratorObject
from engine.renderer.colors import ColorPrefabs

class ObjectHandler:
    def __init__(self) -> None:
        self.__objects : dict = {}
        self.__object_creation_queue = []
        self.__object_deletion_queue = []
        self.__builting_camera_id = "MAIN_CAMERA"
    
    def get_new_uuid(self) -> str:
        return str(uuid.uuid4())

    def create_line(self, start : Vector2, end : Vector2, color : Color = ColorPrefabs.GREEN):
        id = self.get_new_uuid()
        self.__object_creation_queue.append(Object(id, start, RenderableLine(start, end, color=color)))
        return id

    def create_point(self, position : Vector2, color : Color = ColorPrefabs.RED):
        id = self.get_new_uuid()
        self.__object_creation_queue.append(Object(id, position, RenderableCircle(position, color=color, radius=0.1, is_filled=True)))
        return id
    
    def create_circle(self, position : Vector2, radius : float, border_width : float, is_filled : bool):
        id = self.get_new_uuid()
        self.__object_creation_queue.append(Object(id, position, RenderableCircle(position, color=ColorPrefabs.RED, radius=radius, border_width=border_width, is_filled=is_filled)))
        return id
    
    def create_debug_grid(self):
        id = self.get_new_uuid()
        self.__object_creation_queue.append(Object(id, Vector2(0,0), RenderableDebugGrid()))
        return id
    
    def create_tilemap(self):
        id = self.get_new_uuid()
        self.__object_creation_queue.append(Object(id, Vector2(0,0), RenderableTilemap(Vector2(0,0))))
        return id

    def create_camera(self, position : Vector2, rendering_camera : RenderingCamera):
        id = self.__builting_camera_id
        self.__object_creation_queue.append(Camera(id, position, rendering_camera))
        return id
    
    def create_generator_object(self, generator_object):
        id = self.get_new_uuid()
        self.__object_creation_queue.append(GeneratorObject(id, Vector2(0,0), generator_object))
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
        if id not in self.__objects.keys():
            raise KeyError(f"The given id {id} does not exist in the current dict of objects!")
        self.__object_deletion_queue.append(id)

    def update_objects(self):
        for object in self.__objects.values():
            object.update()

        self.create_objects_from_creation_queue()
        self.delete_objects_from_deletion_queue()

    def create_objects_from_creation_queue(self):
        for object in self.__object_creation_queue:
            self.__objects[object.id] = object
        self.__object_creation_queue.clear()
    
    def delete_objects_from_deletion_queue(self):
        for id in self.__object_deletion_queue:
            if id not in self.__objects.keys():
                #raise KeyError(f"The given id {id} does not exist in the current list of objects to be deleted!")
                continue
            del self.__objects[id]