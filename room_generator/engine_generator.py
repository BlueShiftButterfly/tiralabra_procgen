from engine.objects.object_handler import ObjectHandler
from pygame import Vector2, Color
from engine.renderer.colors import ColorPrefabs
from room_generator.map_generator import MapGenerator
from room_generator.bowyer_watson import BowyerWatson
from room_generator.prim_mst import PrimMinSpanningTree
from room_generator.random_point_distributor import RandomPointDistributor
from room_generator.room_connector import RoomConnector

class EngineGenerator:
    def __init__(self, object_handler: ObjectHandler) -> None:
        self.object_handler = object_handler
        self.object_id_set = []

    def generate(self):
        self.delete_objects()
        map_generator = MapGenerator(RandomPointDistributor(), BowyerWatson(), PrimMinSpanningTree(), RoomConnector())
        map = map_generator.generate(size=128, amount=128)
        size = map.size

        self.object_id_set.append(self.object_handler.create_line(Vector2(size, size), Vector2(-size, size), color=ColorPrefabs.GRAY))
        self.object_id_set.append(self.object_handler.create_line(Vector2(-size, size), Vector2(-size, -size), color=ColorPrefabs.GRAY))
        self.object_id_set.append(self.object_handler.create_line(Vector2(-size, -size), Vector2(size, -size), color=ColorPrefabs.GRAY))
        self.object_id_set.append(self.object_handler.create_line(Vector2(size, -size), Vector2(size, size), color=ColorPrefabs.GRAY))

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