import math

class Vertex:
    def __init__(self, x : float, y : float) -> None:
        self.x = x
        self.y = y
    
    def distance(self, other : "Vertex") -> float:
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

class Edge:
    def __init__(self, vertex0 : Vertex, vertex1 : Vertex) -> None:
        self.vertex0 = vertex0
        self.vertex1 = vertex1

class Triangle:
    def __init__(self, vertex0 : Vertex, vertex1 : Vertex, vertex2 : Vertex) -> None:
        self.vertex0 = vertex0
        self.vertex1 = vertex1
        self.vertex2 = vertex2

    def circumcenter(self):
        # From https://en.wikipedia.org/wiki/Circumcircle#Cartesian_coordinates_2
        d = 2 * (self.vertex0.x * (self.vertex1.y - self.vertex2.y) + self.vertex1.x * (self.vertex2.y - self.vertex0.y) + self.vertex2.x * (self.vertex0.y - self.vertex1.y))
        ux = (1 / d) * ((self.vertex0.x**2 + self.vertex0.y**2) * (self.vertex1.y - self.vertex2.y) + (self.vertex1.x**2 + self.vertex1.y**2) * (self.vertex2.y - self.vertex0.y) + (self.vertex2.x**2 + self.vertex2.y**2) * (self.vertex0.y - self.vertex1.y))
        uy = (1 / d) * ((self.vertex0.x**2 + self.vertex0.y**2) * (self.vertex2.x - self.vertex1.x) + (self.vertex1.x**2 + self.vertex1.y**2) * (self.vertex0.x - self.vertex2.x) + (self.vertex2.x**2 + self.vertex2.y**2) * (self.vertex1.x - self.vertex0.x))
        return Vertex(ux, uy)

class BowyerWatson:
    def __init__(self) -> None:
        pass


