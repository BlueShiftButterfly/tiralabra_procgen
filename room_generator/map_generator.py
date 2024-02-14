import time
from room_generator.map import Map
import random

class MapGenerator:
    """
    Responsible for generating maps using the given generators.

    Args:
        point_generator: Generator class responsible for creating a random set of points over an area.
        triangulator: Generator class responsible for creating a Delaunay triangulation of the points from the point generator.
        min_tree_generator: Generator Class responsible for crating a Minimum spanning tree from the Delaunay triangulation.
    """
    def __init__(self, point_generator, triangulator, min_tree_generator, room_connector) -> None:
        self.point_generator = point_generator
        self.triangulator = triangulator
        self.min_tree_generator = min_tree_generator
        self.room_connector = room_connector

    def generate(self, seed : int = None, size : int = 50, amount : int = 128) -> Map:
        """
        Generates a map object using given settings.

        Args: 
            size: Size of the map to be generated. Currently the side length of square bounds that the map is generated in.
            amount: How many points are generated inside the bounds.

        Returns:
            Map object containing generated points, edges, MST, etc.
        """
        random.seed(seed)
        points = self.point_generator.generate_points(amount, (-size, -size), (size, size), seed, minimum_distance = 4)
        edges = []

        print("Generating points...")
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

        complete_map_diagram = self.room_connector.create_connections(seed, mst, edges)

        return Map(size, points, edges, mst, complete_map_diagram)