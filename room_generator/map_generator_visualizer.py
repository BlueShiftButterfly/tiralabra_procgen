import threading
from engine.objects.object_handler import ObjectHandler
from pygame import Vector2, Color
from engine.renderer.colors import ColorPrefabs
from room_generator.map_generator import MapGenerator, Map
from room_generator.bowyer_watson import BowyerWatson
from room_generator.prim_mst import PrimMinSpanningTree
from room_generator.random_point_distributor import RandomPointDistributor
from room_generator.room_connector import RoomConnector

class GeneratorThread(threading.Thread):
    def __init__(self, generator : MapGenerator, seed : int = None, size : int = 64, amount : int = 128):
        threading.Thread.__init__(self, daemon=True)
        self.generator = generator
        self.daemon = True
        self.generated_map : Map = None
        self.seed = seed
        self.size = size
        self.amount = amount
    
    def run(self):
        print("THREAD: Started generating")
        self.generated_map = self.generator.generate(self.seed, self.size, self.amount)
        print("THREAD: Done generating")

class MapGeneratorVisualizer:
    def __init__(self, object_handler: ObjectHandler) -> None:
        self.object_handler = object_handler
        self.object_id_set = []
        self.is_generating = False
        self.is_done_generating = True
        self.map_thread = None

    def start_generation(self):
        self.delete_objects()
        print("Starting generation on separate thread")
        map_generator = MapGenerator(RandomPointDistributor(), BowyerWatson(), PrimMinSpanningTree(), RoomConnector())
        self.map_thread = GeneratorThread(map_generator)
        self.map_thread.start()
        self.is_generating = True
        self.is_done_generating = False

    def check_generation(self):
        is_running = self.map_thread.is_alive()
        if is_running == False:
            self.is_generating = False
            self.map_thread.join()
            map = self.map_thread.generated_map
            self.create_objects_from_map(map)
            self.is_done_generating = True
            print("Generator thread concluded")

    def create_objects_from_map(self, map : Map):
        size = map.size

        self.object_id_set.append(self.object_handler.create_line(Vector2(size // 2, size // 2), Vector2(-size // 2, size // 2), color=ColorPrefabs.GRAY))
        self.object_id_set.append(self.object_handler.create_line(Vector2(-size // 2, size // 2), Vector2(-size // 2, -size // 2), color=ColorPrefabs.GRAY))
        self.object_id_set.append(self.object_handler.create_line(Vector2(-size // 2, -size // 2), Vector2(size // 2, -size // 2), color=ColorPrefabs.GRAY))
        self.object_id_set.append(self.object_handler.create_line(Vector2(size // 2, -size // 2), Vector2(size // 2, size // 2), color=ColorPrefabs.GRAY))

        for edge in map.edges:
            if edge in map.minimum_spanning_tree:
                continue
            self.object_id_set.append(self.object_handler.create_line(Vector2(edge.vertices[0].x, edge.vertices[0].y), Vector2(edge.vertices[1].x, edge.vertices[1].y), Color(100, 30, 30)))

        for edge in map.minimum_spanning_tree:
            if edge in map.map_diagram:
                self.object_id_set.append(self.object_handler.create_line(Vector2(edge.vertices[0].x, edge.vertices[0].y), Vector2(edge.vertices[1].x, edge.vertices[1].y), ColorPrefabs.ORANGE))
        for edge in map.map_diagram:
            if edge in map.minimum_spanning_tree:
                continue
            self.object_id_set.append(self.object_handler.create_line(Vector2(edge.vertices[0].x, edge.vertices[0].y), Vector2(edge.vertices[1].x, edge.vertices[1].y), ColorPrefabs.YELLOW))
        
        for point in map.points:
            self.object_id_set.append(self.object_handler.create_point(Vector2(point.x, point.y), ColorPrefabs.RED))

    def delete_objects(self):
        for id in self.object_id_set:
            if id == None:
                continue
            self.object_handler.delete_object(id)
        self.object_id_set.clear()
