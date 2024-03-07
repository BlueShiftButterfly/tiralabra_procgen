import unittest
from unittest.mock import Mock
from dungeon_generator.map_generator import MapGenerator
from dungeon_generator.geometry import Point, Edge
from dungeon_generator.undirected_graphing import BowyerWatson, PrimMinSpanningTree, RandomEdgeConnector
from dungeon_generator.room_placer import RoomPlacer

class TestMapGenerator(unittest.TestCase):
    #TODO: Remake tests to properly work
    pass