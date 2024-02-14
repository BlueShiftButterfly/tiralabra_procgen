from engine.engine import Engine
from pygame import Vector2, Color
from engine.renderer.colors import ColorPrefabs
from room_generator.map_generator import MapGenerator
from room_generator.bowyer_watson import BowyerWatson
from room_generator.prim_mst import PrimMinSpanningTree
from room_generator.random_point_distributor import RandomPointDistributor
from room_generator.room_connector import RoomConnector

def main():
    engine = Engine()
    map_generator = MapGenerator(RandomPointDistributor(), BowyerWatson(), PrimMinSpanningTree(), RoomConnector())
    map = map_generator.generate(size=128, amount=256)
    size = map.size

    engine.object_handler.create_camera(Vector2(0,0), engine.renderer.rendering_camera)
    engine.object_handler.get_object_from_id("MAIN_CAMERA").rendering_camera.zoom = 7

    engine.object_handler.create_line(Vector2(size, size), Vector2(-size, size), color=ColorPrefabs.GRAY)
    engine.object_handler.create_line(Vector2(-size, size), Vector2(-size, -size), color=ColorPrefabs.GRAY)
    engine.object_handler.create_line(Vector2(-size, -size), Vector2(size, -size), color=ColorPrefabs.GRAY)
    engine.object_handler.create_line(Vector2(size, -size), Vector2(size, size), color=ColorPrefabs.GRAY)

    for edge in map.edges:
        if edge in map.minimum_spanning_tree:
            continue
        engine.object_handler.create_line(Vector2(edge.vertices[0].x, edge.vertices[0].y), Vector2(edge.vertices[1].x, edge.vertices[1].y), Color(100, 30, 30))

    for edge in map.minimum_spanning_tree:
        if edge in map.map_diagram:
            engine.object_handler.create_line(Vector2(edge.vertices[0].x, edge.vertices[0].y), Vector2(edge.vertices[1].x, edge.vertices[1].y), ColorPrefabs.ORANGE)
    for edge in map.map_diagram:
        if edge in map.minimum_spanning_tree:
            continue
        engine.object_handler.create_line(Vector2(edge.vertices[0].x, edge.vertices[0].y), Vector2(edge.vertices[1].x, edge.vertices[1].y), ColorPrefabs.YELLOW)
    
    for point in map.points:
        engine.object_handler.create_point(Vector2(point.x, point.y), ColorPrefabs.RED)
    
    engine.run()

if __name__ == "__main__":
    main()