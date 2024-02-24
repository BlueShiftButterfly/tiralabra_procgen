import unittest
from unittest.mock import Mock
from room_generator.map_generator import Map, MapGenerator
from room_generator.geometry import Point, Edge
from room_generator.bowyer_watson import BowyerWatson
from room_generator.prim_mst import PrimMinSpanningTree
from room_generator.room_connector import RoomConnector
from room_generator.random_point_distributor import RandomPointDistributor

class TestMapGenerator(unittest.TestCase):
    def test_map_generator_outputs_empty_diagram_with_empty_points(self):
        point_generator_mock = Mock()
        point_generator_mock.generate_points.return_value = []
        triangulator_mock = Mock()
        triangulator_mock.triangulate_points.return_value = []
        min_tree_generator_mock = Mock()
        min_tree_generator_mock.create_tree_from_edges.return_value = []
        room_connector_mock = Mock()
        room_connector_mock.create_connections.return_value = []

        mg = MapGenerator(point_generator_mock, triangulator_mock, min_tree_generator_mock, room_connector_mock)
        result = mg.generate().map_diagram
        expected = []
        self.assertEqual(result, expected)

    def test_map_generator_outputs_correct_diagram(self):
        point_generator_mock = Mock()
        point_generator_mock.generate_points.return_value = []
        triangulator_mock = Mock()
        triangulator_mock.triangulate_points.return_value = []
        min_tree_generator_mock = Mock()
        min_tree_generator_mock.create_tree_from_edges.return_value = []
        point1 = Point(-5, 3.5)
        point2 = Point(1.1, -2)
        point3 = Point(2, 3)
        room_connector_mock = Mock()
        room_connector_mock.create_connections.return_value = [Edge((point1, point2)), Edge((point2, point3)), Edge((point1, point3))]

        mg = MapGenerator(point_generator_mock, triangulator_mock, min_tree_generator_mock, room_connector_mock)
        result = mg.generate().map_diagram
        expected = [Edge((point1, point2)), Edge((point2, point3)), Edge((point1, point3))]
        self.assertEqual(result, expected)

    def test_map_generator_outputs_equal_map_diagrams_same_parameters(self):
        mg1 = MapGenerator(RandomPointDistributor(), BowyerWatson(), PrimMinSpanningTree(), RoomConnector())
        map1 = mg1.generate(10, 32, 16)
        mg2 = MapGenerator(RandomPointDistributor(), BowyerWatson(), PrimMinSpanningTree(), RoomConnector())
        map2 = mg2.generate(10, 32, 16)
        self.assertEqual(map1.map_diagram, map2.map_diagram)