"""
Module contains Room and RoomPlacer objects.
Used to generate random rooms in a grid.
"""

import random
from dataclasses import dataclass
from pygame import Rect
from room_generator.grid import Grid
from room_generator.geometry import Point

@dataclass
class Room:
    """
    Container object used to store information
    about a room in the generated environment.
    """
    width : int
    height : int
    bottom_left_point: Point = None
    _center_point : Point = None
    _north_entrance = None
    _east_entrance = None
    _south_entrance = None
    _west_entrance = None

    @property
    def north_entrance(self):
        if (
            self._center_point is not None
        ):
            self._north_entrance = (
                int(self._center_point.x),
                int(self.bottom_left_point.y+self.height)
            )
        return self._north_entrance

    @property
    def east_entrance(self):
        if (
            self._center_point is not None
        ):
            self._east_entrance = (
                int(self.bottom_left_point.x + self.width),
                int(self._center_point.y)
            )
        return self._east_entrance

    @property
    def south_entrance(self):
        if (
            self._center_point is not None
        ):
            self._south_entrance = (
                int(self._center_point.x),
                int(self.bottom_left_point.y)
            )
        return self._south_entrance

    @property
    def west_entrance(self):
        if (
            self._center_point is not None
        ):
            self._west_entrance = (
                int(self.bottom_left_point.x),
                int(self._center_point.y)
            )
        return self._west_entrance

    @property
    def center_point(self):
        if self.bottom_left_point is None:
            return None
        if self._center_point is None:
            self._center_point = Point(0,0)
        self._center_point.x = float(
            int(
                self.bottom_left_point.x + self.width // 2
            )
        )
        self._center_point.y = float(
            int(
                self.bottom_left_point.y + self.height // 2
            )
        )
        return self._center_point

class RoomPlacer:
    """
    Class responsible for randomly placing rooms of random
    size inside the bounds of the grid.
    """
    def __init__(self) -> None:
        self.room_min_side_length = 5
        self.room_max_side_length = 30
        self.min_room_buffer_distance = 6

    def generate_rooms(
            self,
            amount: int,
            grid: Grid,
            seed: int = None
        ) -> tuple[Grid, list[Room]]:
        """
        Generates a given number of random rooms onto a grid.

        Args:
            amount: Number of rooms to be generated.
            grid: The grid onto which rooms should be generated
            seed: Seed value for RNG.

        Returns:
            A tuple with new grid an list of generated rooms.
        """
        if seed is not None:
            random.seed(seed)
        new_grid = self.create_empty_grid(grid.size)
        rooms: list[Room] = []
        room_dict = {}

        for i in range(amount):
            new_room = self.create_random_room(seed+(2*i))
            success = self.try_to_place_room(new_room, rooms, new_grid, seed+i)
            if success:
                point_tuple = (new_room.center_point.x, new_room.center_point.y)
                rooms.append(new_room)
                room_dict[point_tuple] = new_room

        return (new_grid, room_dict)

    def create_empty_grid(self, size: int) -> Grid:
        """
        Creates an grid with values of "empty".

        Args:
            size: Size of the grid to be created.

        Returns:
            Grid of given size with all values as "empty".
        """
        new_grid = Grid(size)
        for y in range(-new_grid.size // 2, new_grid.size // 2):
            for x in range(-new_grid.size // 2, new_grid.size // 2):
                new_grid.set_cell(x, y, "empty")
        return new_grid

    def create_random_room(self, seed: int = None) -> Room:
        """
        Creates a randomly sized room object.

        Args:
            seed: A seed value for RNG.

        Returns:
            A room object with random height and width. It's position
            is not set.
        """
        if seed is not None:
            random.seed(seed)
        width = random.uniform(
            self.room_min_side_length,
            self.room_max_side_length
        )
        height = random.uniform(
            self.room_min_side_length,
            self.room_max_side_length
        )
        return Room(
            width,
            height
        )

    def try_to_place_room(
            self,
            room: Room,
            room_list: list[Room],
            grid: Grid,
            seed: int = None,
            maximum_attempts: int = 100
        ) -> bool:
        """
        Tries to place a room in a random position.

        Args:
            room: Room object to be placed.
            room_list: List of rooms already placed.
            grid: Grid onto which the room should be placed.
            seed: Seed value for RNG
            maximum_attempts: Maximum number of attempts before
            giving up on placing the room.

        Returns:
            A boolean on if the room was successfully generated.
        """
        for i in range(maximum_attempts):
            random_position = self.create_random_room_position(
                room,
                grid,
                seed+i
            )
            room.bottom_left_point = random_position
            if self.can_place_room(room, room_list, grid):
                self.place_room(room, grid)
                return True
        return False

    def place_room(self, room: Room, grid: Grid):
        """
        Sets values of grid cells according to
        room size and position.

        Args:
            room: Room to be placed.
            grid: Grid in which room is to be placed.

        """
        for y in range(
            int(room.bottom_left_point.y),
            int(room.bottom_left_point.y + room.height + 1)
        ):
            for x in range(
                int(room.bottom_left_point.x),
                int(room.bottom_left_point.x + room.width + 1)
            ):
                if (
                    x == int(room.bottom_left_point.x) or
                    x == int(room.bottom_left_point.x + room.width)
                ):
                    grid.set_cell(x, y, "room_wall")
                elif (
                    y == int(room.bottom_left_point.y) or
                    y == int(room.bottom_left_point.y + room.height)
                ):
                    grid.set_cell(x, y, "room_wall")
                else:
                    grid.set_cell(x, y, "room_floor")

    def can_place_room(
            self,
            room: Room,
            room_list: list[Room],
            grid: Grid
        ) -> bool:
        """
        Checks wether a room can be placed.

        Args:
            room: The room to check for.
            room_list: The list of other rooms already placed.
            grid: Grid where the room should be placed.

        Returns:
            A boolean on wether the current placement is valid. If it is,
            then returns True.
        """
        in_bounds = self.is_room_inside_bounds(room, grid)
        room_overlap = self.if_room_intersect_with_rooms(room, room_list)
        return in_bounds and not room_overlap

    def if_room_intersect_with_rooms(
            self,
            room: Room,
            room_list: list[Room]
        ) -> bool:
        """
        Checks wether a room intersects with a list of other rooms.

        Args:
            room: The room to check for intersection with.
            room_list: The list of rooms to compare with.

        Returns:
            A boolean on wether there is an intersection. If there is,
            then returns True.
        """
        rect_list = [
            Rect(
                other_room.bottom_left_point.x + self.min_room_buffer_distance,
                other_room.bottom_left_point.y + self.min_room_buffer_distance,
                other_room.width + self.min_room_buffer_distance,
                other_room.height + self.min_room_buffer_distance
            )
            for other_room in room_list
        ]
        room_rect = Rect(
            room.bottom_left_point.x + self.min_room_buffer_distance,
            room.bottom_left_point.y + self.min_room_buffer_distance,
            room.width + self.min_room_buffer_distance,
            room.height + self.min_room_buffer_distance
        )
        return room_rect.collidelist(rect_list) != -1

    def is_room_inside_bounds(self, room: Room, grid: Grid) -> bool:
        """
        Checks wether a room is inside the given grid's bounds.

        Args:
            room: Room object to be checked.
            grid: Grid in which to check if the room
            is inside it.

        Returns:
            A boolean if the room is inside the grid's
            bounds or not. If yes, then returns True.
        """
        bounds_x = (
            -grid.size // 2 + self.min_room_buffer_distance,
            grid.size // 2 - room.width - self.min_room_buffer_distance
        )
        bounds_y = (
            -grid.size // 2 + self.min_room_buffer_distance,
            grid.size // 2 - room.height - self.min_room_buffer_distance
        )
        return (
            bounds_x[0] <= room.bottom_left_point.x <= bounds_x[1] and
            bounds_y[0] <= room.bottom_left_point.y <= bounds_y[1]
        )

    def create_random_room_position(
            self,
            room: Room,
            grid: Grid,
            seed: int = None
        ) -> Point:
        """
        Creates a random position for a room that is inside
        of grid bounds.

        Args:
            room: The room which position should be created.
            grid: The grid in which the room is to be positioned.
            seed: Seed value for RNG.
        """
        if seed is not None:
            random.seed(seed)

        x = int(random.uniform(
            -int(grid.size // 2 + self.min_room_buffer_distance),
            int(grid.size // 2 - room.width - self.min_room_buffer_distance)
        ))
        y = int(random.uniform(
            -int(grid.size // 2 + self.min_room_buffer_distance),
            int(grid.size // 2 - room.height - self.min_room_buffer_distance)
        ))
        return Point(x, y)
