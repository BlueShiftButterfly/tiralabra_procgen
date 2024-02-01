import unittest
from room_generator.bowyer_watson.bowyer_watson import Point

class TestBowyerWatsonPoint(unittest.TestCase):
    def test_point_distance(self):
        point1 = Point(-5, 3.5)
        point2 = Point(1.1, -2)
        expected = 8.2134036793524
        result = point1.distance(point2)
        self.assertAlmostEqual(expected, result)