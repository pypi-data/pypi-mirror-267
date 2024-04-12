
import random
from pathlib import Path
#from statistics import mean
from tqdm import tqdm
from numpy import mean

import mesa
import networkx as nx
import mesa_geo as mg
from shapely import contains

from scicom.utilities.statistics import prune
from scicom.historicalletters.utils import createData

from scicom.historicalletters.agents import SenderAgent, RegionAgent
from scicom.historicalletters.space import Nuts2Eu


def getPrunedLedger(model):
    """Model reporter for simulation of archiving.
    
    Returns statistics of ledger network of model run
    and various iterations of statistics of pruned networks. 
    """
    # TODO: Add all model params
    if model.runPruning is True:
        ledgerColumns = ['sender', 'receiver', 'sender_location', 'receiver_location', 'topic', 'step']
        modelparams = {
            "population": model.population,
            "moveRange": model.moveRange,
            "letterRange": model.letterRange,
            "useActivation": model.useActivation,
            "useSocialNetwork": model.useSocialNetwork,
        }
        result = prune(
            modelparameters=modelparams,
            network=model.letterLedger,
            columns=ledgerColumns
        )
    else:
        result = model.letterLedger
    return result

def getComponents(model):
    """Model reporter to get number of components.
    
    The MultiDiGraph is converted to undirected, 
    considering only edges that are reciprocal, ie.
    edges are established if sender and receiver have 
    exchanged at least a letter in each direction.
    """
    newG = model.G.to_undirected(reciprocal=True)
    comp = nx.number_connected_components(newG)
    return comp


class HistoricalLetters(mesa.Model):
    """A letter sending model with historical informed initital positions.
    
    Each agent has an initial topic vector, expressed as a RGB value. The 
    initial positions of the agents is based on a weighted random draw
    based on data from [1]
    
    Each step, agents generate two neighbourhoods for sending letters and 
    potential targets to move towards. The probability to send letters is 
    a self-reinforcing process. During each sending the internal topic of 
    the sender is updated as a random rotation towards the receivers topic.

    [1] J. Lobo et al, Population-Area Relationship for Medieval European Cities,
        PLoS ONE 11(10): e0162678.
    """
    def __init__(
        self,
        population: int = 100,
        moveRange: float = 0.05,
        letterRange: float = 0.2,
        similarityThreshold: float = 0.2,
        updateTopic: float = 0.1,
        useActivation=False,
        useSocialNetwork=False,
        longRangeNetworkFactor=0.3,
        shortRangeNetworkFactor=0.8,
        runPruning=False,
        regionData: str = Path(Path(__file__).parent.parent.resolve(), "data/NUTS_RG_60M_2021_3857_LEVL_2.geojson"),
        populationDistributionData: str = Path(Path(__file__).parent.parent.resolve(), "data/pone.0162678.s003.csv"),
        tempfolder: str = "./",
        debug=False
    ):
        super().__init__()

        # Control variables
        self.population = population
        self.moveRange = moveRange
        self.letterRange = letterRange
        self.useActivation = useActivation
        # Initialize social network
        self.useSocialNetwork = useSocialNetwork
        self.G = nx.MultiDiGraph()
        self.longRangeNetworkFactor = longRangeNetworkFactor
        self.shortRangeNetworkFactor = shortRangeNetworkFactor
        # Collected output variables
        self.letterLedger = []
        self.runPruning = runPruning
        self.movements = 0
        self.updatedTopic = 0
        # Internal variables
        self.schedule = mesa.time.RandomActivation(self)
        self.scaleSendInput = {}
        self.updatedTopicsDict = {}
        self.space = Nuts2Eu()
        self.personRegionMap = {}
        self.tempfolder = tempfolder
        self.debug = debug

        initSenderGeoDf = createData(
            population,
            populationDistribution=populationDistributionData
        )

        # Calculate mean of mean distances for each agent. 
        # This is used as a measure for the range of exchanges.
        distances = []
        for idx, row in initSenderGeoDf.iterrows():
            p1 = row['geometry']
            distances.append(
                initSenderGeoDf.geometry.apply(lambda x: p1.distance(x)).mean()
            )
        self.meandistance = mean(distances)

        self.factors = dict(
            updateTopic=updateTopic,
            similarityThreshold=similarityThreshold,
            moveRange=moveRange,
            letterRange=letterRange,
        )

        # Set up the grid with patches for every NUTS region
        ac = mg.AgentCreator(RegionAgent, model=self)
        self.regions = ac.from_file(
            regionData,
            unique_id="NUTS_ID"
        )
        self.space.add_regions(self.regions)

        # Set up agent creator for senders
        ac_senders = mg.AgentCreator(
            SenderAgent,
            model=self,
            agent_kwargs=self.factors
        )

        # Create agents based on random coordinates generated 
        # in the createData step above, see util.py file.
        senders = ac_senders.from_GeoDataFrame(
            initSenderGeoDf,
            unique_id="unique_id"
        )

        # Create random set of initial topic vectors.
        topics = [
            tuple(
                [random.random() for x in range(3)]
            ) for x in range(self.population)
        ]

        # Attach topic and activationWeight to each agent,
        # connect to social network graph.
        for idx, sender in enumerate(senders):
            self.G.add_node(
                sender.unique_id,
                numLettersSend=0,
                numLettersReceived=0    
            )
            sender.topicVec = topics[idx]
            # Add current topic to dict
            self.updatedTopicsDict.update(
                {sender.unique_id: topics[idx]}
            )
            if useActivation is True:
                sender.activationWeight = random.random()

        for agent in senders:
            regionID = [
                x.unique_id for x in self.regions if contains(x.geometry, agent.geometry)
            ]
            try:
                self.space.add_sender(agent, regionID[0])
            except IndexError:
                raise IndexError(f"Problem finding region for {agent.geometry}.")
            self.schedule.add(agent)

        # Add graph to network grid for potential visualization.
        # TODO: Not yet implemented. Maybe use Solara backend for this? 
        self.grid = mesa.space.NetworkGrid(self.G)

        # Create social network
        if useSocialNetwork is True:
            for agent in self.schedule.agents:
                if isinstance(agent, SenderAgent):
                    self._createSocialEdges(agent, self.G)

        # TODO: What comparitive values are useful for visualizations?
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Ledger": getPrunedLedger,
                "Letters": lambda x: len(self.letterLedger),
                "Movements": lambda x: self.movements,
                "Clusters": getComponents
            },
        )

    def _createSocialEdges(self, agent, graph):
        """Create social edges with the different wiring factors.

        Define a close range by using the moveRange parameter. Among
        these neighbors, create a connection with probability set by
        the shortRangeNetworkFactor. 

        For all other agents, that are not in this closeRange group,
        create a connection with the probability set by the longRangeNetworkFactor.
        """
        closerange = [x for x in self.space.get_neighbors_within_distance(
            agent,
            distance=self.moveRange * self.meandistance,
            center=False
        ) if isinstance(x, SenderAgent)]
        for neighbor in closerange:
            if neighbor.unique_id != agent.unique_id:
                connect = random.choices(
                    population=[True, False],
                    weights=[self.shortRangeNetworkFactor, 1 - self.shortRangeNetworkFactor],
                    k=1
                )
                if connect[0] is True:
                    graph.add_edge(agent.unique_id, neighbor.unique_id, step=0)
                    graph.add_edge(neighbor.unique_id, agent.unique_id, step=0)
        longrange = [x for x in self.schedule.agents if x not in closerange and isinstance(x, SenderAgent)]
        for neighbor in longrange:
            if neighbor.unique_id != agent.unique_id:
                connect = random.choices(
                    population=[True, False],
                    weights=[self.longRangeNetworkFactor, 1 - self.longRangeNetworkFactor],
                    k=1
                )
                if connect[0] is True:
                    graph.add_edge(agent.unique_id, neighbor.unique_id, step=0)
                    graph.add_edge(neighbor.unique_id, agent.unique_id, step=0)

    def step(self):
        self.scaleSendInput.update(
            **{x.unique_id: x.numLettersReceived for x in self.schedule.agents}
        )
        self.schedule.step()
        self.datacollector.collect(self)

    def run(self, n):
        """Run the model for n steps."""
        if self.debug is True:
            for _ in tqdm(range(n)):
                self.step()
        else:
            for _ in range(n):
                self.step()
