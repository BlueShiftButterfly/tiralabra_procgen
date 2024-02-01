import unittest
from room_generator.bowyer_watson.bowyer_watson import Point, Edge, Triangle

class TestBowyerWatsonPoint(unittest.TestCase):
    def test_point_distance(self):
        point1 = Point(-5, 3.5)
        point2 = Point(1.1, -2)
        expected = 8.2134036793524
        result = point1.distance(point2)
        self.assertAlmostEqual(expected, result)

    def test_point_repr(self):
        point = Point(3.5, -1)
        expected = "Point<3.5, -1>"
        result = repr(point)

        self.assertEqual(expected, result)

class TestBowyerWatsonEdge(unittest.TestCase):
    def test_edge_length(self):
        point1 = Point(4, -7.1)
        point2 = Point(2, 3)
        edge = Edge((point1, point2))
        
        expected = 10.2961157724649
        result = edge.length()
        self.assertAlmostEqual(expected, result)

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
        result = triangle.circumcircle_radius
        self.assertAlmostEqual(expected, result)
    
        
