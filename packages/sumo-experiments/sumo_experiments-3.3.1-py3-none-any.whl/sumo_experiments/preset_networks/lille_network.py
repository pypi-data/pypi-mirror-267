import os
import xml.etree.ElementTree as ET
from sumo_experiments.components import InfrastructureBuilder, FlowBuilder, DetectorBuilder


class LilleNetwork:
    """
    Create the SUMO network and flows for the city of Lille.
    """

    NET_FILE = 'lille/lille.net.xml'

    def __init__(self):
        self.TL_JUNCTIONS = self.get_tl_junctions()


    def get_tl_junctions(self):
        tree = ET.parse(self.NET_FILE)
        junctions = tree.iter('junction')
        traffic_lights = []
        for junction in junctions:
            if junction.get('type') == 'traffic_light':
                traffic_lights.append(junction)
        return traffic_lights

    def get_edges_to_tl(self):
        tree = ET.parse(self.NET_FILE)
        edges = tree.iter('edge')
        tl_to_edges = {}
        for junction in self.TL_JUNCTIONS:
            tl_to_edges[junction.get('id')] = []
        for edge in edges:
            if edge.get('to') in tl_to_edges:
                tl_to_edges[edge.get('to')].append(edge)
        print(len(tl_to_edges))


if __name__ == '__main__':
    lille = LilleNetwork()
    lille.get_edges_to_tl()

