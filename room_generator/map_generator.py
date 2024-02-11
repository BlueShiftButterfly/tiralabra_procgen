import random
import time
from room_generator.bowyer_watson import BowyerWatson
from room_generator.prim_mst import PrimMinSpanningTree
from room_generator.geometry import Point
from room_generator.map import Map

class MapGenerator:
    def __init__(self, triangulator, min_tree_generator) -> None:
        self.triangulator = triangulator
        self.min_tree_generator = min_tree_generator

    def generate(self, size : int = 50, amount : int = 128) -> Map:
        points = []
        edges = []

        print("Generating points...")
        for i in range(amount):
            newp = random.randint(-size, size), random.randint(-size, size)
            if newp not in points:
                points.append(newp)
            else:
                amount += 1

        points_converted = [Point(p[0], p[1]) for p in points]

        print("Triangulating points...")
        starttime = time.time()
        edges = self.triangulator.triangulate_points(points)
        endtime = time.time()
        print(f"Creating triangulation of {len(edges)} edges for {len(points)} vertices took {endtime-starttime} seconds")

        print("Creating Minimum Spanning Tree for triangulation...")
        starttime = time.time()
        mst = self.min_tree_generator.create_tree_from_edges(edges)
        endtime = time.time()
        print(f"Creating MST for {len(points)} vertices with {len(mst)} edges took {endtime-starttime} seconds")

        return Map(size, points_converted, edges, mst)