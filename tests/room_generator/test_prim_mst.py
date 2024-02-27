import unittest
from room_generator.prim_mst import PrimMinSpanningTree
from room_generator.geometry import Point, Edge

class TestPrimMinSpanningTree(unittest.TestCase):
    def test_prim_contains_all_points_simple(self):
        points = [Point(0, 0), Point(2, 2), Point(3, 0), Point(2, -3), Point(-1, -2)]
        triangulation = [Edge((points[0], points[1])), Edge((points[1], points[2])), Edge((points[2], points[0])), Edge((points[2], points[3])), Edge((points[3], points[0])), Edge((points[3], points[4])), Edge((points[4], points[0]))]
        mst = PrimMinSpanningTree().create_tree_from_edges(triangulation)
        points_in_mst = []
        for e in mst:
            for p in e.vertices:
                if p not in points_in_mst:
                    points_in_mst.append(p)
        expected = 5
        self.assertEqual(len(points_in_mst), expected)
    
    def test_prim_edge_count_minimum_simple(self):
        points = [Point(0, 0), Point(2, 2), Point(3, 0), Point(2, -3), Point(-1, -2)]
        triangulation = [Edge((points[0], points[1])), Edge((points[1], points[2])), Edge((points[2], points[0])), Edge((points[2], points[3])), Edge((points[3], points[0])), Edge((points[3], points[4])), Edge((points[4], points[0]))]
        mst = PrimMinSpanningTree().create_tree_from_edges(triangulation)
        expected = 4
        self.assertEqual(len(mst), expected)
    
    def test_prim_edges_no_duplicates_simple(self):
        points = [Point(0, 0), Point(2, 2), Point(3, 0), Point(2, -3), Point(-1, -2)]
        triangulation = [Edge((points[0], points[1])), Edge((points[1], points[2])), Edge((points[2], points[0])), Edge((points[2], points[3])), Edge((points[3], points[0])), Edge((points[3], points[4])), Edge((points[4], points[0]))]
        mst = PrimMinSpanningTree().create_tree_from_edges(triangulation)
        expected = True
        result = True
        for e in mst:
            if mst.count(e) > 1:
                result = False
        self.assertEqual(result, expected)
