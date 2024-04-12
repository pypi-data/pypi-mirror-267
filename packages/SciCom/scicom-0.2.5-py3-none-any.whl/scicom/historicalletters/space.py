import random
from typing import Dict, DefaultDict, Set
from collections import defaultdict

import mesa
import mesa_geo as mg
from shapely.geometry import Point

from scicom.historicalletters.agents import RegionAgent, SenderAgent


class Nuts2Eu(mg.GeoSpace):
    """Define regions containing senders of letters.
    
    This is modified from a mesa-geo example, here
    https://github.com/projectmesa/mesa-examples/blob/main/gis/geo_schelling_points/geo_schelling_points/space.py
    """
    _id_region_map: Dict[str, RegionAgent]

    def __init__(self):
        super().__init__(warn_crs_conversion=True)
        self._id_region_map = {}

    def add_regions(self, agents):
        super().add_agents(agents)
        total_area = 0
        for agent in agents:
            self._id_region_map[agent.unique_id] = agent

    def add_sender_to_region(self, agent, region_id):
        agent.region_id = region_id
        self._id_region_map[region_id].add_sender(agent)

    def remove_sender_from_region(self, agent):
        self._id_region_map[agent.region_id].remove_sender(agent)
        agent.region_id = None

    def add_sender(self, agent: SenderAgent, regionID: str) -> None:
        super().add_agents([agent])
        self.add_sender_to_region(agent, regionID)
        
    def move_sender(
        self, agent: SenderAgent, pos: mesa.space.FloatCoordinate, regionID: str
    ) -> None:
        self.__remove_sender(agent)
        agent.geometry = pos
        self.add_sender(agent, regionID)

    def __remove_sender(self, agent: SenderAgent) -> None:
        super().remove_agent(agent)
        self.remove_sender_from_region(agent)

