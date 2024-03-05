import unittest
from unittest.mock import Mock
from room_generator.map_generator import MapGenerator
from room_generator.geometry import Point, Edge
from room_generator.undirected_graphing import BowyerWatson, PrimMinSpanningTree, RandomEdgeConnector
from room_generator.room_placer import RoomPlacer

class TestMapGenerator(unittest.TestCase):
    #TODO: Remake tests to properly work
    pass