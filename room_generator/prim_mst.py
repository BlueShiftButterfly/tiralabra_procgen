"""
Module implementing prim's algorithm
for generating a minimum spanning tree.
"""

from room_generator.geometry import Edge

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
        points_edge_references = self.get_point_edge_references(
            triangulation_edges
        )

        queue : list[Edge] = []
        queue.append(triangulation_edges[0])

        while len(queue) > 0:
            queue.sort(key=lambda e : e.get_length(), reverse=True)
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

    def get_point_edge_references(
            self,
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
