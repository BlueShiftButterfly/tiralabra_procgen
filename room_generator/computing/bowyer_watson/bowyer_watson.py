import math

class Point:
    def __init__(self, x : float, y : float) -> None:
        self.x = x
        self.y = y
    
    def distance(self, other : "Point") -> float:
        return math.sqrt(abs(self.x - other.x)**2 + abs(self.y - other.y)**2)
    
    def __repr__(self) -> str:
        return f"Point<{self.x}, {self.y}>"

class Edge:
    def __init__(self, vertices : tuple[Point, Point]) -> None:
        self.vertices = vertices

    def length(self):
        return self.vertices[0].distance(self.vertices[1])

class Triangle:
    def __init__(self, vertices : tuple[Point, Point, Point]) -> None:
        self.vertices = vertices
        self.edges = (Edge((vertices[0], vertices[1])), Edge((vertices[1], vertices[2])), Edge((vertices[2], vertices[0])))
        self.circumcenter = self.get_circumcenter()
        self.circumcircle_radius = self.vertices[0].distance(self.circumcenter)

    def get_circumcenter(self) -> Point:
        # From https://en.wikipedia.org/wiki/Circumcircle#Cartesian_coordinates_2
        d = 2 * (self.vertices[0].x * (self.vertices[1].y - self.vertices[2].y) + self.vertices[1].x * (self.vertices[2].y - self.vertices[0].y) + self.vertices[2].x * (self.vertices[0].y - self.vertices[1].y))
        ux = (1 / d) * ((self.vertices[0].x**2 + self.vertices[0].y**2) * (self.vertices[1].y - self.vertices[2].y) + (self.vertices[1].x**2 + self.vertices[1].y**2) * (self.vertices[2].y - self.vertices[0].y) + (self.vertices[2].x**2 + self.vertices[2].y**2) * (self.vertices[0].y - self.vertices[1].y))
        uy = (1 / d) * ((self.vertices[0].x**2 + self.vertices[0].y**2) * (self.vertices[2].x - self.vertices[1].x) + (self.vertices[1].x**2 + self.vertices[1].y**2) * (self.vertices[0].x - self.vertices[2].x) + (self.vertices[2].x**2 + self.vertices[2].y**2) * (self.vertices[1].x - self.vertices[0].x))
        return Point(ux, uy)
    
    def is_point_in_circumcircle(self, point : Point) -> bool:
        if (self.circumcenter.distance(point) <= self.circumcircle_radius):
            return True
        return False

class BowyerWatson:
    def __init__(self) -> None:
        pass

    def triangulate_points(self, points : list[tuple[float, float]]):
        bw_points = [Point(p[0], p[1]) for p in points]
        max_p = Point(points[0][0], points[0][1])
        min_p = Point(points[0][0], points[0][1])

        for p in bw_points:
            max_p.x = max(max_p.x, p.x)
            max_p.y = max(max_p.y, p.y)
            min_p.x = min(min_p.x, p.x)
            min_p.y = min(min_p.y, p.y)

        return self.create_supertriangle((min_p.x, min_p.y), (max_p.x, max_p.y))
    
    def create_supertriangle(self, minpoint : tuple[float, float], maxpoint : tuple[float, float]) -> Triangle:
        # Since in an equilateral triangle the sagitta ratio compared to the circumcircle radius is about 0.567, 
        # mutliplying the radious by 3 should be enough to encompass all points in the supertriangle, 
        # if they are inside the original circumcircle
        
        size_mult = 3 
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

    


