"""
Module for generating a map on a separate thread
and generating visualization objects for a map.
"""

import threading
from pygame import Vector2
from engine.objects.object_handler import ObjectHandler
from engine.renderer import color_prefabs
from engine.resource_loader.sprite_loader import SpriteLoader
from room_generator.geometry import Point, Edge
from room_generator.grid import Grid
from room_generator.map_generator import MapGenerator, Map
from room_generator.undirected_graphing import BowyerWatson, RandomEdgeConnector, PrimMinSpanningTree
from room_generator.room_placer import RoomPlacer

class GeneratorThread(threading.Thread):
    """
    Custom Thread class used for generating the map on a separate thread.
    """
    def __init__(
            self,
            generator: MapGenerator,
            seed: int = None,
            size: int = 256,
            amount: int = 64
        ):
        threading.Thread.__init__(self, daemon=True)
        self.generator = generator
        self.daemon = True
        self.generated_map : Map = None
        self.seed = seed
        self.size = size
        self.amount = amount

    def run(self) -> None:
        self.generated_map = self.generator.generate(
            self.seed,
            self.size,
            self.amount
        )

class MapGeneratorVisualizer:
    """
    Class handles integration with graphics engine.
    Creates the map on a separate thread
    and then visualizes it in engine.
    """
    def __init__(
            self,
            object_handler: ObjectHandler,
            sprite_loader: SpriteLoader
        ) -> None:
        self.object_handler = object_handler
        self.sprite_loader = sprite_loader
        self.object_id_set = []
        self.is_generating = False
        self.map_thread = None

    def start_generation_thread(self) -> None:
        """
        Starts a separate thread for generating a map.
        """
        self.delete_objects()
        map_generator = MapGenerator(
            RoomPlacer(),
            BowyerWatson(),
            PrimMinSpanningTree(),
            RandomEdgeConnector()
        )
        self.map_thread = GeneratorThread(map_generator)
        self.map_thread.start()
        self.is_generating = True

    def update_generation_thread_status(self) -> bool:
        """
        Checks if the currently running is still running.
        If generation has concluded, automatically joins the thread.
        Returns a bool wether the thread is still running or not
        """
        is_running = self.map_thread.is_alive()
        if is_running is False:
            self.stop_generation_thread()
        return is_running

    def stop_generation_thread(self) -> None:
        """
        Stops the generation thread.
        """
        self.is_generating = False
        self.map_thread.join()
        generated_map = self.map_thread.generated_map
        self.create_objects_from_map(generated_map)

    def create_objects_from_map(self, generated_map : Map):
        """
        Creates all visualization objects from generated map object.
        """
        palette = {
            "room_wall" : self.sprite_loader.sprites["room_wall"],
            "room_floor" : self.sprite_loader.sprites["room_floor"],
            "empty" : self.sprite_loader.sprites["empty"],
            "empty2" : self.sprite_loader.sprites["tile"],
            "corridor_wall" : self.sprite_loader.sprites["corridor_wall"],
            "corridor_floor" : self.sprite_loader.sprites["corridor_floor"]
        }
        self.create_tilemap_object(generated_map.grid, palette)
        #self.create_line_objects_from_edges(generated_map.map_diagram)
        #self.create_point_objects_from_list(generated_map.points)

    def delete_objects(self):
        """
        Delete all visualization objects created by this object.
        """
        for object_id in self.object_id_set:
            if object_id is None:
                continue
            self.object_handler.delete_object(object_id)
        self.object_id_set.clear()

    def create_line_objects_from_edges(self, edge_list : list[Edge]):
        """
        Creates visual line objects in the engine from a list of edge objects.
        """
        for edge in edge_list:
            self.object_id_set.append(
                self.object_handler.create_line(
                    Vector2(edge.vertices[0].x, edge.vertices[0].y),
                    Vector2(edge.vertices[1].x, edge.vertices[1].y),
                    color_prefabs.YELLOW
                )
            )

    def create_point_objects_from_list(self, point_list : list[Point]):
        """
        Creates visual point objects in the engine
        from a list of point objects.
        """
        for point in point_list:
            self.object_id_set.append(
                self.object_handler.create_point(
                    Vector2(point.x, point.y),
                    color_prefabs.RED
                )
            )

    def create_tilemap_object(self, grid : Grid, palette : dict):
        """
        Creates a visual tilemap object from a grid and a palette object.
        """
        self.object_id_set.append(
            self.object_handler.create_tilemap(grid, palette)
        )
