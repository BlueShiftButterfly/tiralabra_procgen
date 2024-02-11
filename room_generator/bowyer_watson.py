import math
from room_generator.geometry import Point, Edge, Triangle

class BowyerWatson:
    """Implementation of the Bowyer-Watson algorithm. To triangulate points, use the triangulate_points function"""
    # Implementation of pseudocode from https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm
    # This is an inefficient algorithm with no optimizations

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
                try:
                    new_triangle = Triangle((edge.vertices[0], edge.vertices[1], point))
                except ValueError as e:
                    # TODO: Implement proper error handling/logging
                    print(e)
                    print(f"Invalid triangle {(edge.vertices[0], edge.vertices[1], point)}, skipping triangulation step...")
                if new_triangle not in triangles:
                    triangles.append(new_triangle)

        output = []
        for triangle in triangles:
            if not triangle.shares_vertex_with_triangle(super_triangle):
                for e in triangle.edges:
                    output.append(e)

        return output
    
    def create_supertriangle(self, minpoint : tuple[float, float], maxpoint : tuple[float, float]) -> Triangle:
        # !!!!!!!!! The circumcircles of the triangles have to also be inside the super triangle!
        # A large value is a hack, and should ideally use infinity when calculating.
        # I have no idea how to implement it, so this stays for now
        # Also floating point precision is an issue with very large triangles
        size_mult = 3000000
        avg_point = Point((minpoint[0]+maxpoint[0])*0.5, (minpoint[1]+maxpoint[1])*0.5)
        cc_radius = max(avg_point.get_distance_to(Point(maxpoint[0], maxpoint[1])), avg_point.get_distance_to(Point(minpoint[0], minpoint[1])))
        cc_radius *= size_mult
        tip = Point(avg_point.x, avg_point.y + cc_radius) 
        bottom_point = Point(avg_point.x, avg_point.y - cc_radius)
        height = tip.get_distance_to(bottom_point)
        height_vector_normal_down = ( 1, 0)
        height_vector_normal_up = ( -1, 0)
        point2 = Point((height_vector_normal_down[0] * height * (2/math.sqrt(3)) * 0.5) + bottom_point.x, height_vector_normal_down[1] * height * (2/math.sqrt(3)) * 0.5 + bottom_point.y)
        point3 = Point((height_vector_normal_up[0] * height * (2/math.sqrt(3)) * 0.5) + bottom_point.x, height_vector_normal_up[1] * height * (2/math.sqrt(3)) * 0.5 + bottom_point.y)

        return Triangle([tip, point2, point3])
