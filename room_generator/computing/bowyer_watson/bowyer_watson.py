import math

class Point:
    def __init__(self, x : float, y : float) -> None:
        self.x = x
        self.y = y
    
    def distance(self, other : "Point") -> float:
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

class Edge:
    def __init__(self, vertex0 : Point, vertex1 : Point) -> None:
        self.vertex0 = vertex0
        self.vertex1 = vertex1

class Triangle:
    def __init__(self, vertex0 : Point, vertex1 : Point, vertex2 : Point) -> None:
        self.vertex0 = vertex0
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.circumcenter = self.get_circumcenter()
        self.circumcircle_radius = self.vertex0.distance(self.circumcenter)

    def get_circumcenter(self) -> Point:
        # From https://en.wikipedia.org/wiki/Circumcircle#Cartesian_coordinates_2
        d = 2 * (self.vertex0.x * (self.vertex1.y - self.vertex2.y) + self.vertex1.x * (self.vertex2.y - self.vertex0.y) + self.vertex2.x * (self.vertex0.y - self.vertex1.y))
        ux = (1 / d) * ((self.vertex0.x**2 + self.vertex0.y**2) * (self.vertex1.y - self.vertex2.y) + (self.vertex1.x**2 + self.vertex1.y**2) * (self.vertex2.y - self.vertex0.y) + (self.vertex2.x**2 + self.vertex2.y**2) * (self.vertex0.y - self.vertex1.y))
        uy = (1 / d) * ((self.vertex0.x**2 + self.vertex0.y**2) * (self.vertex2.x - self.vertex1.x) + (self.vertex1.x**2 + self.vertex1.y**2) * (self.vertex0.x - self.vertex2.x) + (self.vertex2.x**2 + self.vertex2.y**2) * (self.vertex1.x - self.vertex0.x))
        return Point(ux, uy)
    
    def is_point_in_circumcircle(self, point : Point) -> bool:
        if (self.circumcenter.distance(point) <= self.circumcircle_radius):
            return True
        return False

class BowyerWatson:
    def __init__(self) -> None:
        pass


