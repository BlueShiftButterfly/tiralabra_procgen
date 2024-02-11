import math
import uuid

class Point:
    """
    Point class that contains useful functions for working with points.
    """
    def __init__(self, x : float, y : float) -> None:
        self.id = uuid.uuid4()
        self.x = x
        self.y = y
    
    def get_distance_to(self, other : "Point") -> float:
        return math.sqrt(abs(self.x - other.x)**2 + abs(self.y - other.y)**2)
    
    def __repr__(self) -> str:
        return f"Point<{self.x}, {self.y}>"
    
    def __str__(self) -> str:
        return f"Point<{self.x}, {self.y}>"
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Point):
            return False
        if math.isclose(self.x, __value.x) and math.isclose(self.y, __value.y):
            return True
        return False

class Edge:
    """
    Edge class that contains useful functions for working with edges.
    """
    def __init__(self, vertices : tuple[Point, Point]) -> None:
        if vertices[0].get_distance_to(vertices[1]) == 0:
            raise ValueError("Distance between given vertices is 0. Only edges of non-zero length are considered valid.")
        self.vertices = vertices
        self.id = uuid.uuid4()

    def get_length(self):
        return self.vertices[0].get_distance_to(self.vertices[1])
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Edge):
            return False
        if self.vertices[0] == __value.vertices[0] and self.vertices[1] == __value.vertices[1]:
            return True
        if self.vertices[0] == __value.vertices[1] and self.vertices[1] == __value.vertices[0]:
            return True
        return False
    
    def __repr__(self) -> str:
        return f"Edge[{self.vertices[0]}, {self.vertices[1]}]"
    
    def __str__(self) -> str:
        return f"Edge[{self.vertices[0]}, {self.vertices[1]}]"

class Triangle:
    """
    Triangle class that contains useful functions for working with triangles.
    """
    def __init__(self, vertices : tuple[Point, Point, Point]) -> None:
        if vertices[0] == vertices[1] or vertices[0] == vertices[2] or vertices[1] == vertices[2]:
            raise ValueError("Created triangle contains identical points. Only triangles with a non-zero area are considered valid.")
        # Check cross product of vertices to check if the 3 given points are on a single line, and thus making an invalid triangle
        if (vertices[1].x - vertices[0].x) * (vertices[2].y - vertices[0].y) - (vertices[1].y - vertices[0].y) * (vertices[2].x - vertices[0].x) == 0:
            raise ValueError("Created triangle has all 3 points on a single line. Only triangles with a non-zero area are considered valid.")
        self.vertices = vertices
        self.edges = (Edge((vertices[0], vertices[1])), Edge((vertices[1], vertices[2])), Edge((vertices[2], vertices[0])))
        self.id = uuid.uuid4()
    
    def get_circumcircle_radius(self):
        return self.vertices[0].get_distance_to(self.get_circumcenter())

    def get_circumcenter(self) -> Point:
        d = 2 * (self.vertices[0].x * (self.vertices[1].y - self.vertices[2].y) + self.vertices[1].x * (self.vertices[2].y - self.vertices[0].y) + self.vertices[2].x * (self.vertices[0].y - self.vertices[1].y))
        ux = (1 / d) * ((self.vertices[0].x**2 + self.vertices[0].y**2) * (self.vertices[1].y - self.vertices[2].y) + (self.vertices[1].x**2 + self.vertices[1].y**2) * (self.vertices[2].y - self.vertices[0].y) + (self.vertices[2].x**2 + self.vertices[2].y**2) * (self.vertices[0].y - self.vertices[1].y))
        uy = (1 / d) * ((self.vertices[0].x**2 + self.vertices[0].y**2) * (self.vertices[2].x - self.vertices[1].x) + (self.vertices[1].x**2 + self.vertices[1].y**2) * (self.vertices[0].x - self.vertices[2].x) + (self.vertices[2].x**2 + self.vertices[2].y**2) * (self.vertices[1].x - self.vertices[0].x))
        return Point(ux, uy)
    
    def is_point_in_circumcircle(self, point : Point) -> bool:
        if (self.get_circumcenter().get_distance_to(point) < self.get_circumcircle_radius()):
            return True
        return False
    
    def has_edge(self, edge : Edge) -> bool:
        for own_edge in self.edges:
            if edge == own_edge:
                return True
        return False
    
    def has_vertex(self, vertex : Point) -> bool:
        for own_vertex in self.vertices:
            if vertex == own_vertex:
                return True
        return False
    
    def shares_vertex_with_triangle(self, triangle : "Triangle") -> bool:
        for vertex in self.vertices:
            if triangle.has_vertex(vertex):
                return True
        return False
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Triangle):
            return False
        for e in self.edges:
            if not __value.has_edge(e):
                return False
        return True
    
    def __repr__(self) -> str:
        return f"Triangle[{self.edges[0]}, {self.edges[1]}, {self.edges[2]}]"