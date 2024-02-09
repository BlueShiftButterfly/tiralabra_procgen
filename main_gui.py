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
    amount = 64
    points = []
    random.seed(24)
    for i in range(amount):
        newp = random.randint(-size, size), random.randint(-size, size)
        if newp not in points:
            points.append(newp)
    for p in points:
        e.object_handler.create_point(Vector2((p[0]), p[1]))

    starttime = time.time()
    tris = []
    tris = BowyerWatson().triangulate_points(points)
    endtime = time.time()
    print(f"Creating triangulation for {amount} vertices took {endtime-starttime} seconds")
    for p in tris:
        e.object_handler.create_line(Vector2(p[0][0], p[0][1]), Vector2(p[1][0], p[1][1]))

    e.object_handler.create_line(Vector2(size, size), Vector2(-size, size), color=ColorPrefabs.ORANGE)
    e.object_handler.create_line(Vector2(-size, size), Vector2(-size, -size), color=ColorPrefabs.ORANGE)
    e.object_handler.create_line(Vector2(-size, -size), Vector2(size, -size), color=ColorPrefabs.ORANGE)
    e.object_handler.create_line(Vector2(size, -size), Vector2(size, size), color=ColorPrefabs.ORANGE)
    print(f"Generated {len(tris)} edges")
    e.run()
    

if __name__ == "__main__":
    main()