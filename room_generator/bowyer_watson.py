import math
from room_generator.geometry import Point, Edge, Triangle

class BowyerWatson:
    """
    Implementation of the Bowyer-Watson algorithm. To triangulate points, use the triangulate_points function.
    """
    # Implementation of pseudocode from https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm
    # This is an inefficient algorithm with no optimizations
    def triangulate_points(self, points : list[Point]) -> list[Edge]:
        """
        Triangulates a given set of points using the Bowyer-Watson algorithm.

        Args:
            points: List of points that should be triangulated in tuple format.
            Multiple points should not occupy the same space.

        Returns:
            Returns the Delaunay triangulation as a list of edges.
        """
        points_to_triangulate = points
        bounds_max_point = points[0]
        bounds_min_point = points[1]

        for p in points_to_triangulate:
            bounds_max_point = Point(max(bounds_max_point.x, p.x), max(bounds_max_point.y, p.y))
            bounds_min_point = Point(min(bounds_min_point.x, p.x), min(bounds_min_point.y, p.y))

        super_triangle = self.create_supertriangle(bounds_min_point, bounds_max_point)
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

    def create_supertriangle(self, min_point : Point, max_point : Point) -> Triangle:
        """
        Creates a triangle encompassing a set of points and the 
        possible circumcircles of triangles made of said points.

        Args:
            min_point: The point located at the south-west corner
            of a set of bounds encompassing the points to triangulate.
            max_point: The point located at the north-east corner
            of a set of bounds encompassing the points to triangulate.

        Returns:
            A triangle encompassing the given bounds.
        """
        # !!!!!!!!! The circumcircles of the triangles have to also be inside the super triangle!
        # A large value is a hack, and should ideally use infinity when calculating.
        # I have no idea how to implement it, so this stays for now
        # Also floating point precision is an issue with very large triangles
        size_mult = 3000000
        avg_point = Point((min_point.x+max_point.x)*0.5, (min_point.y+max_point.y)*0.5)
        cc_radius = max(avg_point.get_distance_to(max_point), avg_point.get_distance_to(min_point))
        cc_radius *= size_mult
        tip = Point(avg_point.x, avg_point.y + cc_radius)
        bottom_point = Point(avg_point.x, avg_point.y - cc_radius)
        height = tip.get_distance_to(bottom_point)
        height_vector_normal_down = ( 1, 0)
        height_vector_normal_up = ( -1, 0)
        point2 = Point(
                        (height_vector_normal_down[0] * height * (2/math.sqrt(3)) * 0.5) + bottom_point.x,
                        height_vector_normal_down[1] * height * (2/math.sqrt(3)) * 0.5 + bottom_point.y
                    )
        point3 = Point(
                        (height_vector_normal_up[0] * height * (2/math.sqrt(3)) * 0.5) + bottom_point.x,
                        height_vector_normal_up[1] * height * (2/math.sqrt(3)) * 0.5 + bottom_point.y
                    )

        return Triangle([tip, point2, point3])
