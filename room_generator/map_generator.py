"""
Module containing Map dataclass and Map generator class.
The latter is used to generate a 2d map procedurally.
"""

import random
from dataclasses import dataclass
from room_generator.geometry import Point, Edge
from room_generator.grid import Grid, AStar
from room_generator.undirected_graphing import RandomEdgeConnector, PrimMinSpanningTree, BowyerWatson
from room_generator.room_placer import RoomPlacer

@dataclass
class Map:
    """
    Container object used to store information about a generated map.
    """
    size: int
    points: list[Point]
    triangulation: list[Edge]
    minimum_spanning_tree: list[Edge]
    map_diagram: list[Edge]
    grid: Grid

class MapGenerator:
    """
    Responsible for generating maps using the given generators.

    Args:
        room_placer: Generator class responsible for creating
        a random set of rooms in random locations.
        triangulator: Generator class responsible for creating
        a Delaunay triangulation of the points from the rooms'
        center points.
        min_tree_generator: Generator Class responsible for crating
        a Minimum spanning tree from the Delaunay triangulation.
        room_connector: Class responsible for adding random edges
        to the MST.
    """
    def __init__(
            self,
            room_placer,
            triangulator,
            min_tree_generator,
            room_connector
        ) -> None:
        self.room_placer = room_placer
        self.triangulator = triangulator
        self.min_tree_generator = min_tree_generator
        self.room_connector = room_connector
        self.pather = None

    def generate(
            self,
            seed : int = None,
            size : int = 64,
            amount : int = 32
        ) -> Map:
        """
        Generates a map dataclass using given settings.

        Args:
            size: Size of the map to be generated.
            Currently the side length of square
            bounds that the map is generated in.
            amount: How many points are generated
            inside the bounds.

        Returns:
            Map dataclass containing generated points, edges, MST, etc.
            See Map documentation for more details.
        """
        random.seed(seed)
        grid = Grid(size)
        room_grid_tuple = self.room_placer.generate_rooms(
            amount,
            grid,
            seed
        )
        rooms: dict = room_grid_tuple[1]
        new_grid = room_grid_tuple[0]
        self.pather = AStar(new_grid)
        points = [room.center_point for room in rooms.values()]
        triangulation_edges = self.triangulator.triangulate_points(
            points
        )
        mst = self.min_tree_generator.create_tree_from_edges(
            triangulation_edges
        )
        complete_map_diagram = self.room_connector.create_connections(
            seed,
            mst,
            triangulation_edges
        )
        print("POINTS", len(points))
        self.pather.paths_for_rooms(rooms, complete_map_diagram)
        for y in range((-size // 2), (size // 2)):
            for x in range((-size // 2), (size // 2)):
                if grid.get_cell(x, y) == "empty2":
                    grid.set_cell(x, y, "empty")
        return Map(
            size,
            points,
            triangulation_edges,
            mst,
            complete_map_diagram,
            new_grid
        )
