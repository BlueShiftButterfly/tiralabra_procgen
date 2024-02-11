from engine.engine import Engine
from pygame import Vector2, Color
from room_generator.bowyer_watson import BowyerWatson
from room_generator.prim_mst import PrimMinSpanningTree
from engine.renderer.colors import ColorPrefabs
import math
import random
import time

def main():
    e = Engine()
    
    size = 50
    amount = 128
    points = []
    edges = []

    print("Generating points...")
    for i in range(amount):
        newp = random.randint(-size, size), random.randint(-size, size)
        if newp not in points:
            points.append(newp)
        else:
            amount += 1

    print("Triangulating points...")
    starttime = time.time()
    edges = BowyerWatson().triangulate_points(points)
    endtime = time.time()
    print(f"Creating triangulation of {len(edges)} edges for {len(points)} vertices took {endtime-starttime} seconds")
    
    print("Creating Minimum Spanning Tree for triangulation...")
    starttime = time.time()
    mst = PrimMinSpanningTree().create_tree_from_edges(edges)
    endtime = time.time()
    print(f"Creating MST for {len(points)} vertices with {len(mst)} edges took {endtime-starttime} seconds")

    e.object_handler.create_camera(Vector2(0,0), e.renderer.rendering_camera)
    e.object_handler.get_object_from_id("MAIN_CAMERA").rendering_camera.zoom = 7

    e.object_handler.create_line(Vector2(size, size), Vector2(-size, size), color=ColorPrefabs.GRAY)
    e.object_handler.create_line(Vector2(-size, size), Vector2(-size, -size), color=ColorPrefabs.GRAY)
    e.object_handler.create_line(Vector2(-size, -size), Vector2(size, -size), color=ColorPrefabs.GRAY)
    e.object_handler.create_line(Vector2(size, -size), Vector2(size, size), color=ColorPrefabs.GRAY)

    for p in edges:
        if p in mst:
            continue
        e.object_handler.create_line(Vector2(p.vertices[0].x, p.vertices[0].y), Vector2(p.vertices[1].x, p.vertices[1].y), Color(100, 30, 30))

    for p in mst:
        e.object_handler.create_line(Vector2(p.vertices[0].x, p.vertices[0].y), Vector2(p.vertices[1].x, p.vertices[1].y), ColorPrefabs.ORANGE)

    for p in points:
        e.object_handler.create_point(Vector2((p[0]), p[1]), ColorPrefabs.RED)
    
    e.run()

if __name__ == "__main__":
    main()