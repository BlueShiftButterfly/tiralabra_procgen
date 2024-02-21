import uuid
from pygame import Vector2, Color
from engine.objects.object import Object
from engine.renderer.renderable_line import RenderableLine
from engine.renderer.renderable_circle import RenderableCircle
from engine.renderer.renderable_debug_grid import RenderableDebugGrid
from engine.renderer.rendering_camera import RenderingCamera
from engine.renderer.renderable_tilemap import RenderableTilemap
from engine.objects.camera_object import Camera
from engine.objects.generator_object import GeneratorObject
from engine.objects.tilemap_object import TilemapObject
from engine.renderer import color_prefabs
from room_generator.grid import Grid

class ObjectHandler:
    def __init__(self) -> None:
        self.__objects : dict = {}
        self.__object_creation_queue = []
        self.__object_deletion_queue = []
        self.__builting_camera_id = "MAIN_CAMERA"

    def get_new_uuid(self) -> str:
        return str(uuid.uuid4())

    def create_line(self, start : Vector2, end : Vector2, color : Color = color_prefabs.GREEN):
        object_id = self.get_new_uuid()
        self.__object_creation_queue.append(
            Object(
                object_id,
                start,
                RenderableLine(
                    start,
                    end,
                    color=color
                )
            )
        )
        return object_id

    def create_point(self, position : Vector2, color : Color = color_prefabs.RED):
        object_id = self.get_new_uuid()
        self.__object_creation_queue.append(
            Object(
                object_id,
                position,
                RenderableCircle(
                    position,
                    color=color,
                    radius=0.1,
                    is_filled=True
                )
            )
        )
        return object_id

    def create_circle(self, position : Vector2, radius : float, border_width : float, is_filled : bool):
        object_id = self.get_new_uuid()
        self.__object_creation_queue.append(
            Object(
                object_id,
                position,
                RenderableCircle(
                    position,
                    color=color_prefabs.RED,
                    radius=radius,
                    border_width=border_width,
                    is_filled=is_filled
                )
            )
        )
        return object_id

    def create_debug_grid(self):
        object_id = self.get_new_uuid()
        self.__object_creation_queue.append(
            Object(
                object_id,
                Vector2(0,0),
                RenderableDebugGrid()
            )
        )
        return object_id

    def create_tilemap(self, grid : Grid, tilemap_palette : dict):
        object_id = self.get_new_uuid()
        self.__object_creation_queue.append(
            TilemapObject(
                object_id,
                Vector2(0,0),
                RenderableTilemap(
                    Vector2(0,0)
                ),
                grid,
                tilemap_palette
            )
        )
        return object_id

    def create_camera(self, position : Vector2, rendering_camera : RenderingCamera):
        object_id = self.__builting_camera_id
        self.__object_creation_queue.append(
            Camera(
                object_id,
                position,
                rendering_camera
            )
        )
        return object_id

    def create_generator_object(self, generator_object):
        object_id = self.get_new_uuid()
        self.__object_creation_queue.append(
            GeneratorObject(
                object_id,
                Vector2(0,0),
                generator_object
            )
        )
        return object_id

    def get_object_from_id(self, object_id : str):
        return self.__objects[object_id]

    def get_rendering_components(self) -> list:
        components = []
        for obj in self.__objects.values():
            if obj.renderable_component is not None:
                components.append(obj.renderable_component)
        return components

    def delete_object(self, object_id : str):
        if object_id not in self.__objects.keys():
            raise KeyError(f"The given id {object_id} does not exist in the current dict of objects!")
        self.__object_deletion_queue.append(object_id)

    def update_objects(self, delta_time : float):
        for object in self.__objects.values():
            object.update(delta_time)

        self.create_objects_from_creation_queue()
        self.delete_objects_from_deletion_queue()

    def create_objects_from_creation_queue(self):
        for obj in self.__object_creation_queue:
            self.__objects[obj.id] = obj
        self.__object_creation_queue.clear()

    def delete_objects_from_deletion_queue(self):
        for object_id in self.__object_deletion_queue:
            if object_id not in self.__objects.keys():
                continue
            del self.__objects[object_id]
