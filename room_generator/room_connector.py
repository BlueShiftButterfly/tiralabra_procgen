import random
from room_generator.geometry import Point, Edge

class RoomConnector:
    def __init__(self, dead_end_edge_chance : float = 5, random_edge_add_chance : float = 10) -> None:
        self.dead_end_edge_chance = dead_end_edge_chance
        self.random_edge_add_chance = random_edge_add_chance

    def create_connections(self, seed : int, mst : list[Edge], triangulation : list[Edge]):
        adjacencies_mst = {}
        edges_dict = {}
        random.seed(seed)

        dead_ends_edges = []
        diagram : list[Edge] = [e for e in mst]

        for e in mst:
            pv0 = e.vertices[0]
            pv1 = e.vertices[1]

            if pv1.id not in adjacencies_mst.keys():
                adjacencies_mst[pv1.id] = [pv0]
            else:
                adjacencies_mst[pv1.id].append(pv0)
            
            if pv0.id not in adjacencies_mst.keys():
                adjacencies_mst[pv0.id] = [pv1]
            else:
                adjacencies_mst[pv0.id].append(pv1)
            
        for e in triangulation:
            pv0 = e.vertices[0]
            pv1 = e.vertices[1]

            if pv0.id not in edges_dict.keys():
                edges_dict[pv0.id] = [e]
            else:
                edges_dict[pv0.id].append(e)
            
            if pv1.id not in edges_dict.keys():
                edges_dict[pv1.id] = [e]
            else:
                edges_dict[pv1.id].append(e)
        
        for point_id in adjacencies_mst.keys():
            if len(adjacencies_mst[point_id]) == 1:
                #possibilities = []
                for e in edges_dict[point_id]:
                    if e not in diagram and e not in mst and len(adjacencies_mst[e.vertices[0].id]) < 3 and len(adjacencies_mst[e.vertices[1].id]) < 3:
                        #possibilities.append(e)
                        c = random.uniform(0, 100)
                        if c < self.dead_end_edge_chance:
                            diagram.append(e)
        for e in triangulation:
            if e not in mst and e not in diagram:
                c = random.uniform(0, 100)
                if c < self.random_edge_add_chance:
                    diagram.append(e)
        
        #print(len(dead_ends_edges))

        return diagram