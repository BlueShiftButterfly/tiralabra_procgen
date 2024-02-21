class Grid:
    def __init__(self, size : int) -> None:
        self.cells = {}
        for y in range((-size // 2), (size // 2)):
            self.cells[y] = {}
            for x in range((-size // 2), (size // 2)):
                self.cells[y][x] = None
        self.bounds = (((-size // 2), (-size // 2)), ((size // 2)-1, (size // 2)-1))

    def is_cell_in_bounds(self, x : int, y : int):
        return (
            y >= self.bounds[0][1] and
            y <= self.bounds[1][1] and
            x >= self.bounds[0][0] and
            x <= self.bounds[1][1]
        )

    def get_cell(self, x : int, y : int):
        if not self.is_cell_in_bounds(x, y):
            return None
        return self.cells[y][x]

    def set_cell(self, x : int, y : int, cell_value):
        if not self.is_cell_in_bounds(x, y):
            return
        self.cells[y][x] = cell_value

    def get_cell_neighbours(self, x : int, y : int):
        if not self.is_cell_in_bounds(x, y):
            return
        north, east, south, west = None
        if self.is_cell_in_bounds(x, y+1):
            north = self.cells[y+1][x]
        if self.is_cell_in_bounds(x+1, y):
            east = self.cells[y][x+1]
        if self.is_cell_in_bounds(x, y-1):
            south = self.cells[y-1][x]
        if self.is_cell_in_bounds(x-1, y):
            west = self.cells[y][x+1]
        return (north, east, south, west)
