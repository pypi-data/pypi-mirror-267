import random
import numpy as np
import networkx as nx
#from shapely.geometry import LineString
#from sympy import Point3D, Line3D
#from sympy.abc import t

import mesa
import mesa_geo as mg

from scicom.historicalletters.utils import getRegion, getPositionOnLine


class SenderAgent(mg.GeoAgent):
    """The agent sending letters.
    
    On initialization an agent is places in a geographical coordinate.
    Each agent can send letters to other agents within a distance
    determined by the letterRange. Agents can also move to new positions
    within the moveRange. 

    Agents keep track of their changing "interest" by having a vector
    of all held positions in topic space. 
    """
    def __init__(
        self, unique_id, model, geometry, crs, updateTopic, similarityThreshold, moveRange, letterRange
    ):
        super().__init__(unique_id, model, geometry, crs)
        self.region_id = ''
        self.activationWeight = 1
        # Not implemented:
        # The updating is a random walk along a line between receiver and sender.
        # The strength of adaption is therefore random.
        # self.updateTopic = updateTopic
        self.similarityThreshold = similarityThreshold
        self.moveRange = moveRange
        self.letterRange = letterRange
        self.topicLedger = []
        self.numLettersReceived = 0
        self.numLettersSend = 0

    def move(self, neighbors):
        """The agent can randomly move to neighboring positions."""
        if neighbors:
            # Random decision to move or not, weights are 10% moving, 90% staying.
            move = random.choices([0, 1], weights=[0.9, 0.1], k=1)
            if move[0] == 1:
                self.model.movements += 1
                weights = []
                possible_steps = []
                # Weighted random choice to target of moving.
                # Strong receivers are more likely targets.
                # This is another Polya Urn-like process.
                for n in neighbors:
                    if n != self:
                        possible_steps.append(n.geometry)
                        weights.append(n.numLettersReceived)
                # Capture cases where no possible steps exist.
                if possible_steps:
                    if sum(weights) > 0:
                        lineEndPoint = random.choices(possible_steps, weights, k=1)
                    else:
                        lineEndPoint = random.choices(possible_steps, k=1)
                    next_position = getPositionOnLine(self.geometry, lineEndPoint[0])
                    # Capture cases where next position has no overlap with region shapefiles.
                    # TODO: Is there a more clever way to find nearby valid regions?
                    try:
                        regionID = getRegion(next_position, self.model)
                        self.model.space.move_sender(self, next_position, regionID)
                    except IndexError:
                        if self.model.debug:
                            print(f"No overlap for {next_position}, aborting movement.")
                        pass


    @property
    def has_topic(self):
        """Current topic of the agent."""
        return self.topicVec

    def has_letter_contacts(self, neighbors=False):
        """List of already established and potential contacts.

        Implements the ego-reinforcing by allowing mutliple entries
        of the same agent. In neighbourhoods agents are added proportional
        to the number of letters they received, thus increasing the reinforcement.
        The range of the visible neighborhood is defined by the letterRange parameter
        during model initialization.

        For neigbors in the social network (which can be long-tie), the same process 
        applies. Here, at the begining of each step a list of currently valid scalings
        is created, see step function in model.py. This prevents updating of 
        scales during the random activations of agents in one step. 
        """
        contacts = []
        # Social contacts 
        socialNetwork = [x for x in self.model.G.neighbors(self.unique_id)]
        scaleSocial = {}
        for x, y in self.model.scaleSendInput.items():
            if y != 0:
                scaleSocial.update({x: y})
            else:
                scaleSocial.update({x: 1})
        reinforceSocial = [x for y in [[x]*scaleSocial[x] for x in socialNetwork] for x in y]
        contacts.extend(reinforceSocial)
        # Geographical neighbors
        if neighbors:
            neighborRec = []
            for n in neighbors:
                if n != self:
                    if n.numLettersReceived > 0:
                        nMult = [n] * n.numLettersReceived
                        neighborRec.extend(nMult)
                    else:
                        neighborRec.append(n)
            contacts.extend(neighborRec)
        return contacts

    def chooses_topic(self, receiver):
        """Choose the topic to write about in the letter.

        Agents can choose to write a topic from their own ledger or
        in relation to the topics of the receiver. The choice is random.
        """
        topicChoices = self.topicLedger.copy()
        topicChoices.extend(receiver.topicLedger.copy())
        if topicChoices:
            initTopic = random.choice(topicChoices)
        else:
            initTopic = self.topicVec
        return initTopic

    def sendLetter(self, neighbors):
        """Sending a letter based on an urn model."""
        contacts = self.has_letter_contacts(neighbors)
        if contacts:
            # Randomly choose from the list of possible receivers
            receiver = random.choice(contacts)
            if isinstance(receiver, SenderAgent) and receiver != self:
                initTopic = self.chooses_topic(receiver)
                # Calculate distance between own chosen topic 
                # and current topic of receiver.
                distance = np.linalg.norm(np.array(receiver.topicVec) - np.array(initTopic))
                # If the calculated distance falls below a similarityThreshold,
                # send the letter.
                if distance < self.similarityThreshold:
                    receiver.numLettersReceived += 1
                    self.numLettersSend += 1
                    # Update model social network
                    self.model.G.add_edge(
                        self.unique_id,
                        receiver.unique_id,
                        step=self.model.schedule.time
                    )
                    self.model.G.nodes()[self.unique_id]['numLettersSend'] = self.numLettersSend
                    self.model.G.nodes()[receiver.unique_id]['numLettersReceived'] = receiver.numLettersReceived
                    # Update receivers topic vector as a random movement
                    # in 3D space on the line between receivers current topic
                    # and the senders chosen topic vectors. An amount of 1 would
                    # correspond to a complete addaption of the senders chosen topic
                    # vector by the receiver. An amount of 0 means the 
                    # receiver is not influencend by the sender at all.
                    # If both topics coincide nothing is changing. 
                    start = receiver.topicVec
                    end = initTopic
                    if not start == end:
                        updatedTopicVec = getPositionOnLine(start, end, returnType="coords")
                    else:
                        updatedTopicVec = initTopic
                    # The letter sending process is complet and the chosen topic of the letter is put into a ledger entry.
                    self.model.letterLedger.append(
                        (
                            self.unique_id, receiver.unique_id, self.region_id, receiver.region_id,
                            initTopic, self.model.schedule.steps
                        )
                    )
                    # Take note of the influence the letter had on the receiver. 
                    # This information is used in the step function to update all
                    # agent's currently held topic positions.  
                    self.model.updatedTopicsDict.update(
                        {receiver.unique_id: updatedTopicVec}
                    )
                    self.model.updatedTopic += 1

    def step(self):
        self.topicVec = self.model.updatedTopicsDict[self.unique_id]
        self.topicLedger.append(
            self.topicVec
        )
        currentActivation = random.choices(
            population=[0, 1],
            weights=[1 - self.activationWeight, self.activationWeight],
            k=1  
        )
        if currentActivation[0] == 1:
            neighborsMove = [
                x for x in self.model.space.get_neighbors_within_distance(
                    self,
                    distance=self.moveRange * self.model.meandistance,
                    center=False
                ) if isinstance(x, SenderAgent)
            ]
            neighborsSend = [
                x for x in self.model.space.get_neighbors_within_distance(
                    self,
                    distance=self.letterRange * self.model.meandistance,
                    center=False
                ) if isinstance(x, SenderAgent)
            ]
            self.sendLetter(neighborsSend)
            self.move(neighborsMove)


class RegionAgent(mg.GeoAgent):
    """The region keeping track of contained agents.
    
    This agent type is introduced for visualization purposes.
    SenderAgents are linked to regions by calculation of a 
    geographic overlap of the region shape with the SenderAgent
    position. 
    At initialization, the regions are populated with SenderAgents
    giving rise to a dictionary of the contained SenderAgent IDs and
    their initial topic. 
    At each movement, the SenderAgent might cross region boundaries. 
    This reqieres a re-calculation of the potential overlap. 
    """

    def __init__(self, unique_id, model, geometry, crs):
        super().__init__(unique_id, model, geometry, crs)
        self.senders_in_region = dict()

    def has_main_topic(self):
        if len(self.senders_in_region) > 0:
            topics = [y[0] for x,y in self.senders_in_region.items()]
            total = [y[1] for x,y in self.senders_in_region.items()]
            if sum(total) > 0:
                weight = [x / sum(total) for x in total]
            else:
                weight = [1/len(topics)] * len(topics)
            mixed_colors = np.sum([np.multiply(weight[i], topics[i]) for i in range(len(topics))], axis=0)
            colors_inverse = np.subtract((1, 1, 1), mixed_colors)
            return colors_inverse
        else:
            return (0.5, 0.5, 0.5)
    
    def add_sender(self, sender):
        receivedLetters = sender.numLettersReceived
        if receivedLetters > 0:
            scale = receivedLetters
        else: 
            scale = 1
        self.senders_in_region.update(
            {sender.unique_id: (sender.topicVec, scale)}
        )

    def remove_sender(self, sender):
        del self.senders_in_region[sender.unique_id]
