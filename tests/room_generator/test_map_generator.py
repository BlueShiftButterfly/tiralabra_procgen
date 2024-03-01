import unittest
from unittest.mock import Mock
from room_generator.map_generator import MapGenerator
from room_generator.geometry import Point, Edge
from room_generator.undirected_graphing import BowyerWatson, PrimMinSpanningTree, RandomEdgeConnector
from room_generator.room_placer import RoomPlacer

class TestMapGenerator(unittest.TestCase):
    def test_map_generator_outputs_empty_diagram_with_empty_points(self):
        room_generator_mock = Mock()
        room_generator_mock.generate_rooms.return_value = ([], [])
        triangulator_mock = Mock()
        triangulator_mock.triangulate_points.return_value = []
        min_tree_generator_mock = Mock()
        min_tree_generator_mock.create_tree_from_edges.return_value = []
        room_connector_mock = Mock()
        room_connector_mock.create_connections.return_value = []

        mg = MapGenerator(room_generator_mock, triangulator_mock, min_tree_generator_mock, room_connector_mock)
        result = mg.generate().map_diagram
        expected = []
        self.assertEqual(result, expected)

    def test_map_generator_outputs_correct_diagram(self):
        room_generator_mock = Mock()
        room_generator_mock.generate_rooms.return_value = ([], [])
        triangulator_mock = Mock()
        triangulator_mock.triangulate_points.return_value = []
        min_tree_generator_mock = Mock()
        min_tree_generator_mock.create_tree_from_edges.return_value = []
        point1 = Point(-5, 3.5)
        point2 = Point(1.1, -2)
        point3 = Point(2, 3)
        room_connector_mock = Mock()
        room_connector_mock.create_connections.return_value = [Edge((point1, point2)), Edge((point2, point3)), Edge((point1, point3))]

        mg = MapGenerator(room_generator_mock, triangulator_mock, min_tree_generator_mock, room_connector_mock)
        result = mg.generate().map_diagram
        expected = [Edge((point1, point2)), Edge((point2, point3)), Edge((point1, point3))]
        self.assertEqual(result, expected)

    def test_map_generator_outputs_equal_map_diagrams_same_parameters(self):
        mg1 = MapGenerator(RoomPlacer(), BowyerWatson(), PrimMinSpanningTree(), RandomEdgeConnector())
        map1 = mg1.generate(10, 128, 16)
        mg2 = MapGenerator(RoomPlacer(), BowyerWatson(), PrimMinSpanningTree(), RandomEdgeConnector())
        map2 = mg2.generate(10, 128, 16)
        self.assertEqual(map1.map_diagram, map2.map_diagram)