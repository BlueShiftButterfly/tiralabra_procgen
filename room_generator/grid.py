"""
Module containing the Grid class.
"""
import math
import enum
from pygame import Vector2
from room_generator.geometry import Edge

class Direction(enum.Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class Grid:
    """
    Grid objects that is a 2D-array containing values in a grid.
    The values can be of any type.
    """
    def __init__(self, size : int) -> None:
        self.cells = {}
        for y in range((-size // 2), (size // 2)):
            self.cells[y] = {}
            for x in range((-size // 2), (size // 2)):
                self.cells[y][x] = None
        self.bounds = (
            (-size // 2, -size // 2),
            ((size // 2)-1, (size // 2)-1)
        )
        self.size = size

    def is_cell_in_bounds(self, x : int, y : int):
        """
        Checks if a given cell is inside the bounds of the grid.
        """
        return (
            self.bounds[1][1] >= y >= self.bounds[0][1] and
            self.bounds[1][0] >= x >= self.bounds[0][0]
        )

    def get_cell(self, x : int, y : int):
        """
        Gets the cell's value in the specified coordinates.
        If cell does not exist, returns None.
        """
        if not self.is_cell_in_bounds(x, y):
            return None
        return self.cells[y][x]

    def set_cell(self, x : int, y : int, cell_value):
        """
        Sets the value in a cell in the specied coordinates.
        If the cell position is not inside of the grid bounds,
        returns False. Otherwise returns True.
        """
        if not self.is_cell_in_bounds(x, y):
            return False
        self.cells[y][x] = cell_value
        return True

    def get_cell_neighbours(self, x : int, y : int) -> tuple:
        """
        Returns the North, East, South and West neighbours
        of the cell in the given position.
        If a neighour does not exist in the grid bounds,
        returns None for that neighbour.
        """
        if not self.is_cell_in_bounds(x, y):
            return None
        north, east, south, west = None, None, None, None
        if self.is_cell_in_bounds(x, y+1):
            north = (x, y+1)
        if self.is_cell_in_bounds(x+1, y):
            east = (x+1, y)
        if self.is_cell_in_bounds(x, y-1):
            south = (x, y-1)
        if self.is_cell_in_bounds(x-1, y):
            west = (x-1, y)
        return (north, east, south, west)

    def get_full_cell_neighbours(self, x : int, y : int) -> list:
        """
        Returns 8 neighbours
        of the cell in the given position.
        If a neighour does not exist in the grid bounds,
        returns None for that neighbour.
        """
        if not self.is_cell_in_bounds(x, y):
            return None
        neighbors = []
        for i in range(y-1, y+2):
            for j in range(x-1, x+2):
                if j == x and i == y:
                    continue
                if self.is_cell_in_bounds(j, i):
                    neighbors.append((j, i))
                else:
                    neighbors.append(None)
        return neighbors

class AStar:
    def __init__(
            self,
            grid: Grid,
            allowed_path_cell_values: list[str] = [
                "empty",
                "corridor_floor",
                "corridor_wall"
            ]
        ) -> None:
        self.grid = grid
        self.allowed_path_cell_values = allowed_path_cell_values

    def paths_for_rooms(self, room_dict: dict, edges: list[Edge]):
        for edge in edges:
            point_tuple0 = (edge.vertices[0].x, edge.vertices[0].y)
            point_tuple1 = (edge.vertices[1].x, edge.vertices[1].y)
            room0 = room_dict[point_tuple0]
            room1 = room_dict[point_tuple1]
            start = room0.north_entrance
            end = room1.north_entrance
            dir = self.get_direction_from_edge(edge)
            if dir == Direction.NORTH:
                start = (room0.north_entrance[0], room0.north_entrance[1] + 2)
                end = (room1.south_entrance[0], room1.south_entrance[1] - 2)
                self.grid.set_cell(
                    room0.north_entrance[0],
                    room0.north_entrance[1],
                    "corridor_floor"
                )
                self.grid.set_cell(
                    room1.south_entrance[0],
                    room1.south_entrance[1],
                    "corridor_floor"
                )
                self.grid.set_cell(
                    room0.north_entrance[0],
                    room0.north_entrance[1]+1,
                    "corridor_floor"
                )
                self.grid.set_cell(
                    room1.south_entrance[0],
                    room1.south_entrance[1]-1,
                    "corridor_floor"
                )
            if dir == Direction.EAST:
                start = (room0.east_entrance[0] + 2, room0.east_entrance[1])
                end = (room1.west_entrance[0] - 2, room1.west_entrance[1])
                self.grid.set_cell(
                    room0.east_entrance[0],
                    room0.east_entrance[1],
                    "corridor_floor"
                )
                self.grid.set_cell(
                    room1.west_entrance[0],
                    room1.west_entrance[1],
                    "corridor_floor"
                )
                self.grid.set_cell(
                    room0.east_entrance[0]+1,
                    room0.east_entrance[1],
                    "corridor_floor"
                )
                self.grid.set_cell(
                    room1.west_entrance[0]-1,
                    room1.west_entrance[1],
                    "corridor_floor"
                )
            if dir == Direction.WEST:
                start = (room0.west_entrance[0] - 2, room0.west_entrance[1])
                end = (room1.east_entrance[0] + 2, room1.east_entrance[1])
                self.grid.set_cell(
                    room0.west_entrance[0],
                    room0.west_entrance[1],
                    "corridor_floor"
                )
                self.grid.set_cell(
                    room1.east_entrance[0],
                    room1.east_entrance[1],
                    "corridor_floor"
                )
                self.grid.set_cell(
                    room0.west_entrance[0]-1,
                    room0.west_entrance[1],
                    "corridor_floor"
                )
                self.grid.set_cell(
                    room1.east_entrance[0]+1,
                    room1.east_entrance[1],
                    "corridor_floor"
                )
            elif dir == Direction.SOUTH:
                start = (room0.south_entrance[0], room0.south_entrance[1] - 2)
                end = (room1.north_entrance[0], room1.north_entrance[1] + 2)
                self.grid.set_cell(
                    room0.south_entrance[0],
                    room0.south_entrance[1],
                    "corridor_floor"
                )
                self.grid.set_cell(
                    room1.north_entrance[0],
                    room1.north_entrance[1],
                    "corridor_floor"
                )
                self.grid.set_cell(
                    room0.south_entrance[0],
                    room0.south_entrance[1]-1,
                    "corridor_floor"
                )
                self.grid.set_cell(
                    room1.north_entrance[0],
                    room1.north_entrance[1]+1,
                    "corridor_floor"
                )
            self.grid.set_cell(start[0], start[1], "corridor_floor")
            self.grid.set_cell(end[0], end[1], "corridor_floor")
            tiles = self.find_path((start[0], start[1]), (end[0], end[1]))
            for tile in tiles:
                self.grid.set_cell(tile[0], tile[1], "corridor_floor")
                for neighbor_tile in self.grid.get_full_cell_neighbours(tile[0], tile[1]):
                    if self.grid.get_cell(neighbor_tile[0], neighbor_tile[1]) == "empty":
                        self.grid.set_cell(neighbor_tile[0], neighbor_tile[1], "corridor_wall")

    def get_direction_from_edge(self, edge: Edge):
        edge_dir_vector = Vector2(
            edge.vertices[1].x - edge.vertices[0].x,
            edge.vertices[1].y - edge.vertices[0].y
        )
        angle = edge_dir_vector.as_polar()[1]
        if 45 <= angle <= 135:
            return Direction.NORTH
        elif 135 < angle or -135 > angle:
            return Direction.WEST
        elif 45 > angle or -45 < angle:
            return Direction.EAST
        elif -45 >= angle >= -135:
            return Direction.SOUTH
        else:
            return Direction.NORTH

    def reconstruct_path(self, last: tuple[int, int], previous_nodes: dict):
        path = []
        prev = last
        for _ in range(len(previous_nodes.keys())):
            path.append(prev)
            prev = previous_nodes[prev]
            if prev is None:
                break
        return path

    def find_path(self, start: tuple[int, int], end: tuple[int, int]):
        # https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
        queue = []
        queue.append(start)
        previous_cheapest_node = {}
        cheapest_path_score = {}
        estimate_path_score = {}
        for y in range((-self.grid.size // 2), (self.grid.size // 2)):
            for x in range((-self.grid.size // 2), (self.grid.size // 2)):
                cheapest_path_score[(x, y)] = 99999999999999
                estimate_path_score[(x, y)] = 99999999999999
        cheapest_path_score[start] = 0
        estimate_path_score[start] = self.calculate_heuristic_score(start, end)
        previous_cheapest_node[start] = None
        for _ in range(100000):
            if len(queue) == 0:
                break
            queue.sort(key=lambda cell : estimate_path_score[cell], reverse=True)
            current = queue.pop()
            if current == end:
                return self.reconstruct_path(current, previous_cheapest_node)
            neighbor_cells = self.get_valid_neighbors(
                self.grid.get_cell_neighbours(current[0], current[1])
            )
            for neighbor in neighbor_cells:
                tentative_score = cheapest_path_score[current] + 1
                if tentative_score < cheapest_path_score[neighbor]:
                    previous_cheapest_node[neighbor] = current
                    cheapest_path_score[neighbor] = tentative_score
                    estimate_path_score[neighbor] = (
                        tentative_score + self.calculate_heuristic_score(neighbor, end)
                    )
                    if neighbor not in queue:
                        queue.append(neighbor)

        return []

    def calculate_heuristic_score(self, cell: tuple[int, int], goal: tuple[int, int]) -> int:
        return int(math.dist(cell, goal))

    def get_valid_neighbors(self, neighbours: tuple[tuple[int, int]]):
        valid_neighbours = []
        for neighbour in neighbours:
            if neighbour is None:
                continue
            valid = True
            if self.grid.get_cell(neighbour[0], neighbour[1]) in self.allowed_path_cell_values:
                for other_neighbor in self.grid.get_full_cell_neighbours(neighbour[0], neighbour[1]):
                    if other_neighbor is None:
                        continue
                    if (self.grid.get_cell(other_neighbor[0], other_neighbor[1]) not in self.allowed_path_cell_values):
                        valid = False
                if valid:
                    valid_neighbours.append(neighbour)
        return valid_neighbours
