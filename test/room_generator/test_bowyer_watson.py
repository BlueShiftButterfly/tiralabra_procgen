import unittest
from room_generator.bowyer_watson.bowyer_watson import Point, Edge, Triangle

class TestBowyerWatsonPoint(unittest.TestCase):
    def test_point_distance_nonzero(self):
        point1 = Point(-5, 3.5)
        point2 = Point(1.1, -2)
        expected = 8.2134036793524
        result = point1.distance(point2)
        self.assertAlmostEqual(expected, result)
    
    def test_point_distance_zero(self):
        point1 = Point(-5, 3.5)
        point2 = Point(-5, 3.5)
        expected = 0
        result = point1.distance(point2)
        self.assertAlmostEqual(expected, result)

    def test_point_repr(self):
        point = Point(3.5, -1)
        expected = "Point<3.5, -1>"
        result = repr(point)

        self.assertEqual(expected, result)
    
    def test_are_points_equal(self):
        point1 = Point(1, 1)
        point2 = Point(1, 1)
        expected = True
        result = point1 == point2
        self.assertAlmostEqual(expected, result)
    
    def test_are_points_equal_precision(self):
        point1 = Point(1000.00432380430320, 1000.434321328402)
        point2 = Point(1000.00432380430320, 1000.434321328402)
        expected = True
        result = point1 == point2
        self.assertAlmostEqual(expected, result)

class TestBowyerWatsonEdge(unittest.TestCase):
    def test_edge_length_nonzero(self):
        point1 = Point(4, -7.1)
        point2 = Point(2, 3)
        edge = Edge((point1, point2))
        
        expected = 10.2961157724649
        result = edge.length()
        self.assertAlmostEqual(expected, result)
    
    def test_are_edges_equal(self):
        point1 = Point(4, -7.1)
        point2 = Point(2, 3)
        edge1 = Edge((point1, point2))
        edge2 = Edge((point2, point1))

        expected = True
        result = edge1 == edge2
        self.assertEqual(expected, result)
    
    def test_are_edges_not_equal(self):
        point1 = Point(4, -7.1)
        point2 = Point(2, 3)
        point3 = Point(0, 0)
        edge1 = Edge((point1, point2))
        edge2 = Edge((point3, point1))

        expected = False
        result = edge1 == edge2
        self.assertEqual(expected, result)
    
    def test_edge_repr(self):
        point1 = Point(4, -7.1)
        point2 = Point(2, 3)
        edge = Edge((point1, point2))
        expected = "Edge[Point<4, -7.1>, Point<2, 3>]"
        result = repr(edge)

        self.assertEqual(expected, result)

class TestBowyerWatsonTriangle(unittest.TestCase):
    def test_circumcenter(self):
        point1 = Point(-5, 3.5)
        point2 = Point(1.1, -2)
        point3 = Point(2, 3)
        triangle = Triangle((point1, point2, point3))

        expected = Point(-1.6552186177715, 1.0769393511989)
        result = triangle.get_circumcenter()

        self.assertAlmostEqual(expected.x, result.x)
        self.assertAlmostEqual(expected.y, result.y)
    
    def test_point_inside_circumcircle(self):
        point1 = Point(-5, 3.5)
        point2 = Point(1.1, -2)
        point3 = Point(2, 3)
        triangle = Triangle((point1, point2, point3))

        expected = True
        result = triangle.is_point_in_circumcircle(Point(1, 1))
        self.assertEqual(expected, result)
    
    def test_point_outside_circumcircle(self):
        point1 = Point(-5, 3.5)
        point2 = Point(1.1, -2)
        point3 = Point(2, 3)
        triangle = Triangle((point1, point2, point3))

        expected = False
        result = triangle.is_point_in_circumcircle(Point(-6, 1))
        self.assertEqual(expected, result)
    
    def test_circumcircle_radius(self):
        point1 = Point(-5, 3.5)
        point2 = Point(1.1, -2)
        point3 = Point(2, 3)
        triangle = Triangle((point1, point2, point3))

        expected = 4.1302282506746
        result = triangle.get_circumcircle_radius()
        self.assertAlmostEqual(expected, result)
    
    def test_has_vertex(self):
        point1 = Point(-5, 3.5)
        point2 = Point(1.1, -2)
        point3 = Point(2, 3)
        triangle = Triangle((point1, point2, point3))

        expected = True
        result = triangle.has_vertex(point1)
        self.assertEqual(expected, result)      

    def test_has_edge(self):
        point1 = Point(-5, 3.5)
        point2 = Point(1.1, -2)
        point3 = Point(2, 3)
        triangle = Triangle((point1, point2, point3))
        edge = Edge((point1, point2))

        expected = True
        result = triangle.has_edge(edge)
        self.assertEqual(expected, result)      
    
    def test_shares_vertex_with_other_triangle(self):
        point1 = Point(-5, 3.5)
        point2 = Point(1.1, -2)
        point3 = Point(2, 3)
        point4 = Point(0, 0)
        point5 = Point(-1, 4)
        triangle = Triangle((point1, point2, point3))
        triangle2 = Triangle((point3, point4, point5))

        expected = True
        result = triangle.shares_vertex_with_triangle(triangle2)
        self.assertEqual(expected, result)      
