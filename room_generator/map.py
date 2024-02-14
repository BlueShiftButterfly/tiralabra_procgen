from room_generator.geometry import Point, Edge

class Map:
    """
    Container object used to store information about a generated map.
    """
    def __init__(self, size : int, points : list[Point], edges : list[Edge], minimum_spanning_tree : list[Edge], map_diagram : list[Edge]) -> None:
        self.size = size
        self.points = points
        self.edges = edges
        self.minimum_spanning_tree = minimum_spanning_tree 
        self.map_diagram = map_diagram