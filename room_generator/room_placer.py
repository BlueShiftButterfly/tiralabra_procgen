import random
from pygame import Rect
from room_generator.grid import Grid
from room_generator.geometry import Point
class Room:
    def __init__(self, center_point : Point, width : int, height : int, max_bounds : int) -> None:
        self.center_point = center_point
        self.width = width
        self.height = height
        self.max_bounds = max_bounds

class RoomPlacer:
    def generate_rooms(self, amount, grid: Grid, seed : int = None):
        room_min_area = 10
        room_max_area = 25
        room_min_width = 5
        room_max_width = 20
        min_room_buffer_distance = 4

        rooms_placed = 0
        new_grid = Grid(grid.size)

        rooms: list[Room] = []
        room_rects = []

        if seed is not None:
            random.seed(seed)
        for y in range(-new_grid.size // 2, new_grid.size //2):
            for x in range(-new_grid.size // 2, new_grid.size //2):
                new_grid.set_cell(x, y, "empty")
        
        for i in range(amount * 10):
            if rooms_placed >= amount:
                break

            room_width = random.randint(room_min_width, room_max_width)
            room_height = max(room_min_width ,random.randint(room_min_width, room_max_width))
            room_bounds_size = max(room_width // 2 + 1, room_height // 2 + 1)
            room_position = Point(
                random.randint(
                    -new_grid.size // 2 + (room_width // 2) + 5,
                    new_grid.size // 2 - (room_width // 2) - 5
                ),
                random.randint(
                    -new_grid.size // 2 + (room_height // 2) + 5,
                    new_grid.size // 2 - (room_height // 2) - 5
                )
            )
            room = Room(room_position, room_width, room_height, room_bounds_size)

            valid_placement = True
            room_rect = Rect(
                room.center_point.x - room.width // 2,
                room.center_point.y - room.height // 2,
                room.width + min_room_buffer_distance,
                room.height + min_room_buffer_distance
            )
            if not room_rect.collidelist(room_rects) == -1:
                valid_placement = False
            if valid_placement is False:
                continue

            rooms.append(room)
            room_rects.append(room_rect)
            rooms_placed += 1
            for y in range(room_height + 1):
                for x in range(room_width + 1):
                    if x == 0 or x == room_width or y == 0 or y == room_height:
                        new_grid.set_cell(
                            x + room_position.x - (room_width // 2),
                            y + room_position.y - (room_height // 2),
                            "room_wall"
                        )
                    else:
                        new_grid.set_cell(
                            x + room_position.x - (room_width // 2),
                            y + room_position.y - (room_height // 2),
                            "room_floor"
                        )
        print(len(rooms))
        return (new_grid, rooms)
