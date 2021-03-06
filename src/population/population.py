import sys
import numpy as np
from .agent import Agent

sys.path.append("..")
from config import POPULATION


class Population:
    """
    Population of agents, containing all evolved agents in multiple generations
    """

    def __init__(self, optimizer):
        """
        Initialize Population class

        :param optimizer: evolutionary based optimizer class
        """

        self.size = POPULATION.size
        self.max_generations = POPULATION.max_generations
        self.optimizer = optimizer
        weights_size = len(Agent().model.get_weights())
        self.agents_weights = np.empty((self.max_generations, self.size, weights_size), dtype=np.ndarray)
        self.scores = np.empty((self.max_generations, self.size), dtype=float)

    def create_population(self):
        """
        Create first generation of population

        :return:
        """
        return [Agent() for _ in range(self.size)]

    def evolve(self, save=True):
        """
        Evolve agents through genetic algorithm

        :param save: save agents weights and scores
        :type save: bool
        :return:
        """
        return self.optimizer.evolve(self, save)
