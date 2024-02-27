import time
import random
from room_generator.geometry import Point, Edge
from room_generator.grid import Grid

class Map:
    """
    Container object used to store information about a generated map.
    """
    def __init__(
            self,
            size : int,
            points : list[Point],
            edges : list[Edge],
            minimum_spanning_tree : list[Edge],
            map_diagram : list[Edge],
            grid : Grid
        ) -> None:
        self.size = size
        self.points = points
        self.edges = edges
        self.minimum_spanning_tree = minimum_spanning_tree 
        self.map_diagram = map_diagram
        self.grid = grid

class MapGenerator:
    """
    Responsible for generating maps using the given generators.

    Args:
        point_generator: Generator class responsible for creating
        a random set of points over an area.
        triangulator: Generator class responsible for creating
        a Delaunay triangulation of the points from the point generator.
        min_tree_generator: Generator Class responsible for crating
        a Minimum spanning tree from the Delaunay triangulation.
    """
    def __init__(self, room_placer, triangulator, min_tree_generator, room_connector) -> None:
        self.room_placer = room_placer
        self.triangulator = triangulator
        self.min_tree_generator = min_tree_generator
        self.room_connector = room_connector

    def generate(self, seed : int = None, size : int = 64, amount : int = 32) -> Map:
        """
        Generates a map object using given settings.

        Args: 
            size: Size of the map to be generated.
            Currently the side length of square bounds that the map is generated in.
            amount: How many points are generated inside the bounds.

        Returns:
            Map object containing generated points, edges, MST, etc.
        """
        total_start = time.time()
        random.seed(seed)
        print("Generating points...")
        points = []
        grid = Grid(size)
        rp = self.room_placer.generate_rooms(amount, grid, seed)
        rooms = rp[1]
        new_grid = rp[0]
        for room in rooms:
            points.append(room.center_point)
        edges = []
        print("Points generated")
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
        total_end = time.time()
        print(f"Map took {total_end-total_start} seconds to generate")
        return Map(size, points, edges, mst, complete_map_diagram, new_grid)
