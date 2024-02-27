"""
Module containing the Grid class.
"""

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
            (size // 2-1, size // 2-1)
        )
        self.size = size

    def is_cell_in_bounds(self, x : int, y : int):
        """
        Checks if a given cell is inside the bounds of the grid.
        """
        return (
            self.bounds[1][1] >= y >= self.bounds[0][1] and
            self.bounds[1][1] >= x >= self.bounds[0][0]
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

    def get_cell_neighbours(self, x : int, y : int):
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
            north = self.cells[y+1][x]
        if self.is_cell_in_bounds(x+1, y):
            east = self.cells[y][x+1]
        if self.is_cell_in_bounds(x, y-1):
            south = self.cells[y-1][x]
        if self.is_cell_in_bounds(x-1, y):
            west = self.cells[y][x+1]
        return (north, east, south, west)
