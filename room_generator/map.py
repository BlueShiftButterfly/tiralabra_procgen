from room_generator.geometry import Point, Edge

class Map:
    def __init__(self, size : int, points : list[Point], edges : list[Edge], minimum_spanning_tree : list[Edge]) -> None:
        self.size = size
        self.points = points
        self.edges = edges
        self.minimum_spanning_tree = minimum_spanning_tree 