from engine.engine import Engine
from pygame import Vector2
from room_generator.computing.bowyer_watson.bowyer_watson import BowyerWatson, Point, Triangle, Edge
from engine.renderer.colors import ColorPrefabs
import math

if __name__ == "__main__":
    e = Engine()

    e.object_handler.create_camera(Vector2(0,0), e.renderer.rendering_camera)
    e.object_handler.create_debug_grid()

    points = [(0,0), (1,1), (-1, 2), (1, 0), (2, 0), (-3, 1), (-1, -10)]
    for p in points:
        e.object_handler.create_point(Vector2(p[0], p[1]))
    t = BowyerWatson().triangulate_points(points)
    for p in t.vertices:
        e.object_handler.create_point(Vector2(p.x, p.y), ColorPrefabs.BLUE)
    for p in t.edges:
        e.object_handler.create_line(Vector2(p.vertices[0].x, p.vertices[0].y), Vector2(p.vertices[1].x, p.vertices[1].y))
    e.object_handler.create_circle(Vector2(t.circumcenter.x, t.circumcenter.y), t.circumcircle_radius, 0, False)
    
    e.run()
    