from engine.engine import Engine
from pygame import Vector2
from room_generator.bowyer_watson.bowyer_watson import BowyerWatson, Point, Triangle, Edge
from engine.renderer.colors import ColorPrefabs
import math
import random
import time

def main():
    e = Engine()
    e.object_handler.create_camera(Vector2(0,0), e.renderer.rendering_camera)
    e.object_handler.get_object_from_id("MAIN_CAMERA").rendering_camera.zoom = 3
    size = 20
    amount = 200
    points = []
    for i in range(amount):
        points.append((random.uniform(-size, size), random.uniform(-size, size)))
    for p in points:
        e.object_handler.create_point(Vector2(p[0], p[1]))

    starttime = time.time()
    tris = BowyerWatson().triangulate_points(points)
    endtime = time.time()
    print(f"Creating triangulation for {amount} vertices took {endtime-starttime} seconds")
    vertex_count = 0
    for t in tris:
        for p in t.edges:
            e.object_handler.create_line(Vector2(p.vertices[0].x, p.vertices[0].y), Vector2(p.vertices[1].x, p.vertices[1].y))

    e.object_handler.create_line(Vector2(size, size), Vector2(-size, size), color=ColorPrefabs.ORANGE)
    e.object_handler.create_line(Vector2(-size, size), Vector2(-size, -size), color=ColorPrefabs.ORANGE)
    e.object_handler.create_line(Vector2(-size, -size), Vector2(size, -size), color=ColorPrefabs.ORANGE)
    e.object_handler.create_line(Vector2(size, -size), Vector2(size, size), color=ColorPrefabs.ORANGE)
    print(f"Generated {len(tris)} triangles")
    e.run()
    

if __name__ == "__main__":
    main()