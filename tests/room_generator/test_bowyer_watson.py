import unittest
from room_generator.undirected_graphing import BowyerWatson
from room_generator.geometry import Point, Edge

class TestBowyerWatson(unittest.TestCase):
    def test_triangulate_three_valid_points(self):
        point1 = Point(-5, 3.5)
        point2 = Point(1.1, -2)
        point3 = Point(2, 3)
        point_list = [point1, point2, point3]

        expected_edges = [Edge((point1, point2)), Edge((point2, point3)), Edge((point1, point3))]
        result_edges = BowyerWatson().triangulate_points(point_list)
        contain_same_edges = len(expected_edges) == len(result_edges)
        for e in expected_edges:
            if e not in result_edges:
                contain_same_edges = False
                break

        expected = True
        result = contain_same_edges
        self.assertEqual(expected, result)
    
    def test_triangulate_three_points_on_same_line_return_empty(self):
        point1 = Point(0, 1)
        point2 = Point(0, -2)
        point3 = Point(0, 3)
        point_list = [point1, point2, point3]

        expected = []
        result = BowyerWatson().triangulate_points(point_list)
        self.assertEqual(expected, result)
