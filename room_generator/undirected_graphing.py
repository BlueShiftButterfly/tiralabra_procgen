"""
Module contains classes to create and manipulate undirected graphs.
"""
import math
import random
from room_generator.geometry import Point, Edge, Triangle

def get_point_edge_refs(
        edges: list[Edge]
    ) -> dict:
    """
    Creates a dictionary of point ids and
    edges to which said points are connected to.

    Args:
        edges: List of edges to create references from.

    Returns:
        A dictionary with a point ids as keys
        and a list of edges as values.
    """
    point_edge_references = {}
    for edge in edges:
        point_edge_references[edge.vertices[0].point_id] = []
        point_edge_references[edge.vertices[1].point_id] = []

    for edge in edges:
        point_edge_references[edge.vertices[0].point_id].append(edge)
        point_edge_references[edge.vertices[1].point_id].append(edge)

    return point_edge_references

def get_edge_id_dict(
        edges: list[Edge]
    ) -> dict:
    edge_dict = {}
    for edge in edges:
        edge_dict[edge.edge_id] = edge
    return edge_dict

class BowyerWatson:
    """
    Implementation of the Bowyer-Watson algorithm for creating
    a Delaunay triangulation from a set of points.
    """
    # Implementation of pseudocode from
    # https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm
    # Also inspired by
    # https://www.gorillasun.de/blog/bowyer-watson-algorithm-for-delaunay-triangulation/
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
        if len(points) <= 1:
            return []
        points_to_triangulate = points
        bounds_max_point = points[0]
        bounds_min_point = points[1]

        for point in points_to_triangulate:
            bounds_max_point = Point(
                max(bounds_max_point.x, point.x),
                max(bounds_max_point.y, point.y)
            )
            bounds_min_point = Point(
                min(bounds_min_point.x, point.x),
                min(bounds_min_point.y, point.y)
            )

        super_triangle = self.create_supertriangle(
            bounds_min_point,
            bounds_max_point
        )
        triangles : list[Triangle] = []
        triangles.append(super_triangle)

        for point in points_to_triangulate:
            bad_triangles : list[Triangle] = []
            for triangle in triangles:
                if triangle.is_point_in_circumcircle(point):
                    bad_triangles.append(triangle)

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
                    new_triangle = Triangle(
                        (
                            edge.vertices[0],
                            edge.vertices[1],
                            point
                        )
                    )
                except ValueError as error:
                    # TODO: Implement proper error handling/logging
                    print(error)
                    print(f"Invalid triangle {(edge.vertices[0], edge.vertices[1], point)}, skipping triangulation step...")
                if new_triangle not in triangles:
                    triangles.append(new_triangle)

        output = []
        for triangle in triangles:
            if not triangle.shares_vertex_with_triangle(super_triangle):
                for error in triangle.edges:
                    output.append(error)

        return output

    def create_supertriangle(
            self,
            min_point: Point,
            max_point: Point
        ) -> Triangle:
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
        # !!!!!!!!! The circumcircles of the triangles
        # have to also be inside the super triangle!
        # A large value is a hack,
        # and should ideally use infinity when calculating.
        # I have no idea how to implement it, so this stays for now
        # Also floating point precision is an issue with very large triangles
        size_mult = 3000000
        avg_point = Point(
            (min_point.x+max_point.x)*0.5,
            (min_point.y+max_point.y)*0.5
        )
        cc_radius = max(
            avg_point.get_distance_to(max_point),
            avg_point.get_distance_to(min_point)
        )
        cc_radius *= size_mult
        tip = Point(avg_point.x, avg_point.y + cc_radius)
        bottom_point = Point(avg_point.x, avg_point.y - cc_radius)
        height = tip.get_distance_to(bottom_point)
        down_vector = ( 1, 0)
        up_vector = ( -1, 0)
        point2 = Point(
            (down_vector[0] * height * (2/math.sqrt(3)) / 2) + bottom_point.x,
            down_vector[1] * height * (2/math.sqrt(3)) / 2 + bottom_point.y
        )
        point3 = Point(
            (up_vector[0] * height * (2/math.sqrt(3)) / 2) + bottom_point.x,
            up_vector[1] * height * (2/math.sqrt(3)) / 2 + bottom_point.y
        )

        return Triangle([tip, point2, point3])


class PrimMinSpanningTree:
    """
    Implementation of Prim's algorithm.
    Used to generate a minimum spanning tree.
    """
    def create_tree_from_edges(
            self,
            triangulation_edges: list[Edge]
        ) -> list[Edge]:
        """
        Generates a minimum spanning tree from a list of given edges
        that form a Delaunay triangulation.

        Args:
            edges: List of edges that
            the minimum spanning tree is created from.

        Returns:
            List of edges contained in the minimum spanning tree.
        """
        if len(triangulation_edges) == 0:
            return []

        visited_vertex_ids = set()
        edge_id_forest = set()
        points_edge_references = get_point_edge_refs(
            triangulation_edges
        )

        queue : list[Edge] = []
        queue.append(triangulation_edges[0])

        while len(queue) > 0:
            queue.sort(key=lambda edge : edge.get_length(), reverse=True)
            edge = queue.pop()

            if (
                edge.vertices[0].point_id in visited_vertex_ids and
                edge.vertices[1].point_id in visited_vertex_ids
            ):
                continue

            edge_id_forest.add(edge.edge_id)
            visited_vertex_ids.add(edge.vertices[0].point_id)
            visited_vertex_ids.add(edge.vertices[1].point_id)
            queue.extend(
                self.get_potential_unvisited_edges(
                    points_edge_references[edge.vertices[0].point_id],
                    visited_vertex_ids,
                    edge
                )
            )
            queue.extend(
                self.get_potential_unvisited_edges(
                    points_edge_references[edge.vertices[1].point_id],
                    visited_vertex_ids,
                    edge
                )
            )

        mst_edges = []
        for edge in triangulation_edges:
            if edge.edge_id in edge_id_forest:
                mst_edges.append(edge)

        return mst_edges

    def get_potential_unvisited_edges(
            self,
            edges: list[Edge],
            visited_point_ids: set,
            current_edge: Edge
        ):
        """
        Creates a list of edges that contain unvisited points.

        Args:
            edges: List of edges to check for potentially
            unvisited points.
            visited_point_ids: Set of point ids that
            have been visited in prim's algorithm.
            current_edge: The currently evaluated edge that should
            be ignored for new potential edges.

        Returns:
            List of edges that contain unvisited points.
        """
        potential_edges = []
        for potential_edge in edges:
            if potential_edge == current_edge:
                continue
            if (
                potential_edge.vertices[0].point_id not in visited_point_ids or
                potential_edge.vertices[1].point_id not in visited_point_ids
            ):
                potential_edges.append(potential_edge)
        return potential_edges


class RandomEdgeConnector:
    """
    Class responsible for adding random edges to a
    minimum spanning tree.
    """
    def __init__(
            self,
            dead_end_edge_chance: float = 5,
            random_edge_add_chance: float = 10
        ) -> None:
        self.dead_end_edge_chance = dead_end_edge_chance
        self.random_edge_add_chance = random_edge_add_chance

    def create_connections(
            self,
            seed: int,
            minimum_spanning_tree: list[Edge],
            triangulation: list[Edge]
        ) -> list[Edge]:
        """
        Creates random connections using separate % chances
        defined in the class instance variables.

        Args:
            seed: Seed number to be used for RNG.
            minimum_spanning_tree: List of edges forming
            an MST of the triangulation.
            triangulation: List of edges forming
            a Delaunay triangulation.

        Returns:
            List of edges forming a graph with random edges added
            on top of the MST.
        """
        random.seed(seed)
        mst_point_edge_references = get_point_edge_refs(minimum_spanning_tree)
        tri_point_edge_references = get_point_edge_refs(triangulation)
        diagram : list[Edge] = minimum_spanning_tree.copy()
        dead_end_edge_connector_candidates = self.get_dead_end_edge_candidates(
            self.get_dead_end_point_ids(
                mst_point_edge_references
            ),
            minimum_spanning_tree,
            tri_point_edge_references
        )
        dead_end_edge_connector_candidates.sort(
            key=lambda edge: edge.get_length(),
            reverse=True
        )
        for edge in dead_end_edge_connector_candidates:
            chance_value = random.uniform(0, 100)
            if chance_value < self.dead_end_edge_chance:
                diagram.append(edge)

        for potential_new_edge in triangulation:
            if (
                potential_new_edge not in minimum_spanning_tree and
                potential_new_edge not in diagram
            ):
                chance_value = random.uniform(0, 100)
                if chance_value < self.random_edge_add_chance:
                    diagram.append(potential_new_edge)

        return diagram

    def get_dead_end_point_ids(self, mst_point_edge_references: dict):
        """
        Gets all point ids that contain only a single edge
        as a connection.

        Args:
            mst_point_edge_references: A dictionary with point ids as keys
            and lists of edges connected to said points. Only from
            the MST.

        Returns:
            A list of point ids that are concidered dead-ends.
        """
        dead_ends = []
        for point_id, edge_list in mst_point_edge_references.items():
            if len(edge_list) == 1:
                dead_ends.append(point_id)
        return dead_ends

    def get_dead_end_edge_candidates(
            self,
            dead_end_point_ids: list[str],
            minimum_spanning_tree: list[Edge],
            tri_point_edge_reference: dict
        ) -> list[Edge]:
        """
        Gets edges that are valid new connections to a dead-end.

        Args:
            dead_end_point_ids: List of ids of points that
            are considered dead-ends.
            minimum_spanning_tree: List of edges contained
            in the MST.
            tri_point_edge_reference: A dictionary with point ids as keys
            and lists of edges connected to said points. Only
            from the triangulation

        Returns:
            List of edges that are valid connections to dead-end points.
        """
        edges: list[Edge] = []
        mst_edge_ids = set(get_edge_id_dict(minimum_spanning_tree).keys())
        for point_id in dead_end_point_ids:
            for edge in tri_point_edge_reference[point_id]:
                if edge.edge_id in mst_edge_ids:
                    continue
                edges.append(edge)
        return edges
