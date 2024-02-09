import math

class Point:
    """Point class used in Triangulation that contains useful functions for working with points"""
    def __init__(self, x : float, y : float) -> None:
        self.x = x
        self.y = y
    
    def distance(self, other : "Point") -> float:
        return math.sqrt(abs(self.x - other.x)**2 + abs(self.y - other.y)**2)
    
    def __repr__(self) -> str:
        return f"Point<{self.x}, {self.y}>"
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Point):
            return False
        if math.isclose(self.x, __value.x) and math.isclose(self.y, __value.y):
            return True
        return False

class Edge:
    """Edge class used in Triangulation that contains useful functions for the Bowyer-Watson algorithm"""
    def __init__(self, vertices : tuple[Point, Point]) -> None:
        self.vertices = vertices

    def length(self):
        return self.vertices[0].distance(self.vertices[1])
    
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

class Triangle:
    """Triangle class used in Triangulation that contains useful functions for the Bowyer-Watson algorithm, 
    such as calculating circumcircles"""
    def __init__(self, vertices : tuple[Point, Point, Point]) -> None:
        self.vertices = vertices
        self.edges = (Edge((vertices[0], vertices[1])), Edge((vertices[1], vertices[2])), Edge((vertices[2], vertices[0])))
    
    def get_circumcircle_radius(self):
        return self.vertices[0].distance(self.get_circumcenter())

    def get_circumcenter(self) -> Point:
        # Formula from https://en.wikipedia.org/wiki/Circumcircle#Cartesian_coordinates_2
        d = 2 * (self.vertices[0].x * (self.vertices[1].y - self.vertices[2].y) + self.vertices[1].x * (self.vertices[2].y - self.vertices[0].y) + self.vertices[2].x * (self.vertices[0].y - self.vertices[1].y))
        ux = (1 / d) * ((self.vertices[0].x**2 + self.vertices[0].y**2) * (self.vertices[1].y - self.vertices[2].y) + (self.vertices[1].x**2 + self.vertices[1].y**2) * (self.vertices[2].y - self.vertices[0].y) + (self.vertices[2].x**2 + self.vertices[2].y**2) * (self.vertices[0].y - self.vertices[1].y))
        uy = (1 / d) * ((self.vertices[0].x**2 + self.vertices[0].y**2) * (self.vertices[2].x - self.vertices[1].x) + (self.vertices[1].x**2 + self.vertices[1].y**2) * (self.vertices[0].x - self.vertices[2].x) + (self.vertices[2].x**2 + self.vertices[2].y**2) * (self.vertices[1].x - self.vertices[0].x))
        return Point(ux, uy)
    
    def is_point_in_circumcircle(self, point : Point) -> bool:
        if (self.get_circumcenter().distance(point) < self.get_circumcircle_radius()):
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

class BowyerWatson:
    """Implementation of the Bowyer-Watson algorithm. To triangulate points, use the triangulate_points function"""
    # Implementation of pseudocode from https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm
    # This is an inefficient algorithm with no optimizations
    # Also this implementation only returns triangles, not edges. Will be changes in the future
    def triangulate_points(self, points : list[tuple[float, float]]):
        points_to_triangulate = [Point(p[0], p[1]) for p in points]
        bounds_max_point = Point(points[0][0], points[0][1])
        bounds_min_point = Point(points[0][0], points[0][1])

        for p in points_to_triangulate:
            bounds_max_point.x = max(bounds_max_point.x, p.x)
            bounds_max_point.y = max(bounds_max_point.y, p.y)
            bounds_min_point.x = min(bounds_min_point.x, p.x)
            bounds_min_point.y = min(bounds_min_point.y, p.y)

        super_triangle = self.create_supertriangle((bounds_min_point.x, bounds_min_point.y), (bounds_max_point.x, bounds_max_point.y))
        triangles : list[Triangle] = []
        triangles.append(super_triangle)

        for point in points_to_triangulate:
            bad_triangles : list[Triangle] = []
            for t in triangles:
                if t.is_point_in_circumcircle(point):
                    bad_triangles.append(t)

            polygon : list[Edge] = []
            for bad_triangle in bad_triangles:
                for edge in bad_triangle.edges:
                    valid = True
                    for other_bad_triangle in bad_triangles:
                        if other_bad_triangle == bad_triangle:
                            continue
                        if other_bad_triangle.has_edge(edge):
                            valid = False
                            break
                    if edge not in polygon and valid:
                        polygon.append(edge)

            for bad_triangle in bad_triangles:
                triangles.remove(bad_triangle)

            for edge in polygon:
                new_triangle = Triangle((edge.vertices[0], edge.vertices[1], point))
                if new_triangle not in triangles:
                    triangles.append(new_triangle)

        output = []
        for triangle in triangles:
            if not triangle.shares_vertex_with_triangle(super_triangle):
                for e in triangle.edges:
                    output.append( ((e.vertices[0].x, e.vertices[0].y), (e.vertices[1].x, e.vertices[1].y)) )

        return output
    
    def create_supertriangle(self, minpoint : tuple[float, float], maxpoint : tuple[float, float]) -> Triangle:
        # !!!!!!!!! The circumcircles of the triangles have to also be inside the super triangle!
        # A large value is a hack, and should ideally use infinity when calculating.
        # I have no idea how to implement it, so this stays for now
        # Also floating point precision is an issue with very large triangles
        size_mult = 3000000
        avg_point = Point((minpoint[0]+maxpoint[0])*0.5, (minpoint[1]+maxpoint[1])*0.5)
        cc_radius = max(avg_point.distance(Point(maxpoint[0], maxpoint[1])), avg_point.distance(Point(minpoint[0], minpoint[1])))
        cc_radius *= size_mult
        tip = Point(avg_point.x, avg_point.y + cc_radius) 
        bottom_point = Point(avg_point.x, avg_point.y - cc_radius)
        height = tip.distance(bottom_point)
        height_vector_normal_down = ( 1, 0)
        height_vector_normal_up = ( -1, 0)
        point2 = Point((height_vector_normal_down[0] * height * (2/math.sqrt(3)) * 0.5) + bottom_point.x, height_vector_normal_down[1] * height * (2/math.sqrt(3)) * 0.5 + bottom_point.y)
        point3 = Point((height_vector_normal_up[0] * height * (2/math.sqrt(3)) * 0.5) + bottom_point.x, height_vector_normal_up[1] * height * (2/math.sqrt(3)) * 0.5 + bottom_point.y)

        return Triangle([tip, point2, point3])
