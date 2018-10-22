from abc import *


class GeneticAlgorithmEngine(metaclass=ABCMeta):
    def __init__(self, generation, population):
        # later, use configuraiton file not parameters
        self.generation = generation
        self.population = population

    @abstractmethod
    def mutation(self, input_gene):
        pass    # return mutated output_gene

    @abstractmethod
    def crossover(self, gene1, gene2):
        pass    # crossover two gene

    @abstractmethod
    def selection(self, population):
        pass    # select subset of population

    @abstractmethod
    def search(self):
        pass    # perform genetic algorithm utilizing mutation, crossover, selection