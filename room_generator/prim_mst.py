from room_generator.geometry import Edge

class PrimMinSpanningTree:
    """
    Implementation of Prim's algorithm. Used to generate a minimum spanning tree.
    """
    def create_tree_from_edges(self, edges : list[Edge]) -> list[Edge]:
        """
        Generates a minimum spanning tree from a list of given edges.

        Args:
            edges: List of edges that the minimum spanning tree is created from.

        Returns:
            List of edges contained in the minimum spanning tree.
        """
        if len(edges) <= 0:
            return []

        adjacencies = {}
        edges_dict = {}
        visited = set()
        edge_forest = set()

        for e in edges:
            pv0 = e.vertices[0]
            pv1 = e.vertices[1]

            if pv1.point_id not in adjacencies.keys():
                adjacencies[pv1.point_id] = [pv0]
            else:
                adjacencies[pv1.point_id].append(pv0)

            if pv0.point_id not in adjacencies.keys():
                adjacencies[pv0.point_id] = [pv1]
            else:
                adjacencies[pv0.point_id].append(pv1)

            if pv0.point_id not in edges_dict.keys():
                edges_dict[pv0.point_id] = [e]
            else:
                edges_dict[pv0.point_id].append(e)

            if pv1.point_id not in edges_dict.keys():
                edges_dict[pv1.point_id] = [e]
            else:
                edges_dict[pv1.point_id].append(e)

        queue : list[Edge] = []
        queue.append(edges[0])

        while len(queue) > 0:
            queue.sort(key=lambda e : e.get_length(), reverse=True)
            edge = queue.pop()
            if edge.vertices[0].point_id in visited and edge.vertices[1].point_id in visited:
                continue
            edge_forest.add(edge.edge_id)
            visited.add(edge.vertices[0].point_id)
            visited.add(edge.vertices[1].point_id)
            for potential_edge in edges_dict[edge.vertices[0].point_id]:
                if potential_edge == edge:
                    continue
                if potential_edge.vertices[0].point_id in visited and potential_edge.vertices[1].point_id not in visited:
                    queue.append(potential_edge)
                if potential_edge.vertices[1].point_id in visited and potential_edge.vertices[0].point_id not in visited:
                    queue.append(potential_edge)
            for potential_edge in edges_dict[edge.vertices[1].point_id]:
                if potential_edge == edge:
                    continue
                if potential_edge.vertices[0].point_id in visited and potential_edge.vertices[1].point_id not in visited:
                    queue.append(potential_edge)
                if potential_edge.vertices[1].point_id in visited and potential_edge.vertices[0].point_id not in visited:
                    queue.append(potential_edge)

        mst_edges = []
        for e in edges:
            if e.edge_id in edge_forest:
                mst_edges.append(e)

        return mst_edges
