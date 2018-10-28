from copy import deepcopy

from DataAnalyzer import DataAnalyzer
from GeneticAlgorithmEngine import GeneticAlgorithmEngine
import random
from deap import tools
from deap import base, creator


class TrafficEnvGAEngine(GeneticAlgorithmEngine):
    def __init__(self, config_file, sd):
        num_gen, num_pop, cross_prob, mut_prob, elit_prob = self.ga_config_file_to_values(config_file)
        GeneticAlgorithmEngine.__init__(self, num_gen, num_pop)
        self.cxpb = cross_prob
        self.mutpb = mut_prob
        self.elitpb = elit_prob
        self.systemDynamics = sd

        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        IND_SIZE = 12   # 12 constants in the SD model
        self.toolbox = base.Toolbox()
        self.toolbox.register("attribute", random.random)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attribute, n=IND_SIZE)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutPolynomialBounded, eta=0, low=0, up=1, indpb=0.1)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        self.toolbox.register("evaluate", self.fitness_function)

    def ga_config_file_to_values(self, config_file):
        """
        read GA configuration file and return values
        :param config_file: GA configuration file
        :return: tuple of values of the configuration
        """
        configurations = []
        configuration_list = open(config_file, "r")
        for i in range(2):
            line = configuration_list.readline()
            if not line:
                break
            line = line.split(': ')
            configurations.append(int(line[1]))
        while True:
            line = configuration_list.readline()
            if not line:
                break
            line = line.split(': ')
            configurations.append(float(line[1]))
        configuration_list.close()
        return tuple(configurations)

    def selection(self, population):
        """
        Select offspring among population
        :param population: List of genes
        :return: List of genes which is selected among initial population
        """
        offspring = self.toolbox.select(population, int(len(population)*self.elitpb))
        new_offspring = self.toolbox.population(self.population-len(offspring))
        offspring = offspring + new_offspring
        return offspring

    def mutation(self, population):
        """
        Mutate population by mutation probability of this GA Engine.
        :param population: List of genes
        :return: List of genes after mutation
        """
        offspring = [self.toolbox.clone(ind) for ind in population]
        # Apply mutation on the offspring
        for i in range(len(offspring)):
            if random.random() < self.mutpb:
                offspring[i], = self.toolbox.mutate(offspring[i])
                del offspring[i].fitness.values
        return offspring

    def crossover(self, population):
        """
        Crossover genes by crossover probability of this GA engine.
        :param population: List of genes.
        :return: List of genes after crossover between two gene.
        """
        offspring = [self.toolbox.clone(ind) for ind in population]
        # Apply crossover on the offspring
        for i in range(1, len(offspring), 2):
            if random.random() < self.cxpb:
                offspring[i - 1], offspring[i] = self.toolbox.mate(offspring[i - 1], offspring[i])
                del offspring[i - 1].fitness.values, offspring[i].fitness.values
        return offspring

    def representation_to_output_flow_config(self, representation):
        """
        Make a configuration based on representation - gene and return it.
        :param representation: List of 12 float variables - gene.
        :return: List of configuration
        """
        # representation is list of 12 float variables.
        # outputFlowConfig is a list of 12 configuration lists
        config = []
        for i in range(12):
            if i < 8:
                if i % 2 is 0:
                    ii = int(i / 2)
                    config.append([representation[ii * 3], representation[ii * 3 + 1], representation[ii * 3 + 2]])
                else:
                    config.append([1])
            else:
                config.append(None)
        return config

    def fitness_function(self, args):
        """
        Fitness evaluation function for this GA engine.
        :param args: List that includes gene and goal data.
        :return: fitness value calculated based on goal data.
        """
        # Gene is a SystemDynamicsGene configuration. Goal is a data. Fitness is an error.
        #   args = (gene_configuration = float[12], goal = float[4])
        gene = args[0]
        goal_data = args[1]
        configuration = self.representation_to_output_flow_config(gene)
        sd = deepcopy(self.systemDynamics)
        sd.set_config(configuration)

        sd.update()
        states = sd.get_state()
        # print("states", sd_gene.sd.get_state())

        abs_error = 0
        for i in range(4):
            abs_error = abs_error + abs(states[i*2+1] - goal_data[i])

        avg_abs_error = abs_error/4
        # print(avg_abs_error)
        return (avg_abs_error,)

    def evaluation(self, population, goal):
        """
        Evaluate each gene in population by using goal data and store the fitness value in gene.
        :param population: List of genes.
        :param goal: Goal data that using for fitness evaluation
        :return: None.
        """
        invalid_ind = [(ind, goal) for ind in population if not ind.fitness.valid]
        fitnesses = self.toolbox.map(self.toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind[0].fitness.values = fit

    def criteria_data_generation(self, goal_data_files):
        """
        Make a goal data - criteria data from list of files.
        Make equations based on files, and make a data from that equation.
        :param goal_data_files: List of name of files includes data
        :return: List of lists includes target data
        """
        analyzer = DataAnalyzer()
        equation = analyzer.csv_data_to_equation(goal_data_files)

        total_goal = []
        for e in equation:
            goal = []
            for t in range(24):
                set_variable = 0
                for c in range(len(e)):
                    set_variable = set_variable + e[-1 - c] * (t ** c)
                goal.append(set_variable)
            total_goal.append(goal)
        return total_goal

    def best_individual_in_population(self, population):
        """
        Find the gene that has best fitness value in this population
        :param population: List of genes
        :return: Gene that has best fitness value in this population
        """
        best_fitness = None
        best_index = None
        for i in range(len(population)):
            if best_fitness is None:
                best_fitness = population[i].fitness.values[0]
                best_index = i
            else:
                if population[i].fitness.values[0] < best_fitness:
                    best_fitness = population[i].fitness.values[0]
                    best_index = i
        return population[best_index]

    def search(self, goal_data_files):
        """
        Search coefficient by using GA
        :param goal_data_files: List of name of files that includes data goal.
        :return state: List of states from the best result searched by GA
        :return error: List of errors from the best result searched by GA
        """
        goal_data = self.criteria_data_generation(goal_data_files)
        best_individual = None
        errors = []
        states = []
        states30 = []
        states60 = []

        for t in range(24):
            # generate sub goal for fitness evaluation
            subgoal_data = [goal_data[i][t] for i in range(len(goal_data))]

            # initial population generation
            pop = self.toolbox.population(self.population)
            if best_individual is not None:     # best output configuration of previous time is reused.
                pop[0] = best_individual
            self.evaluation(pop, subgoal_data)

            for g in range(self.generation):
                # selection
                offspring = self.selection(pop)
                # Clone the selected individuals
                offspring = map(self.toolbox.clone, offspring)  # individual clone list

                # Apply crossover and mutation on the offspring
                offspring = self.crossover(offspring)
                offspring = self.mutation(offspring)

                # Evaluate the individuals with an invalid fitness
                self.evaluation(offspring, subgoal_data)

                # The population is entirely replaced by the offspring
                pop[:] = offspring

                # find the best individual after the whole generations
                best_individual = self.best_individual_in_population(pop)

                if g == 1:
                    self.systemDynamics.set_config30(self.representation_to_output_flow_config(best_individual))
                    self.systemDynamics.update30()
                    states30.append(self.systemDynamics.get_state30())
                elif g == 30:
                    self.systemDynamics.set_config60(self.representation_to_output_flow_config(best_individual))
                    self.systemDynamics.update60()
                    states60.append(self.systemDynamics.get_state60())

            # find the best individual after the whole generations
            best_individual = self.best_individual_in_population(pop)

            # update system dynamics model to the next time using the searched best configuration.
            self.systemDynamics.set_config(self.representation_to_output_flow_config(best_individual))
            self.systemDynamics.update()
            states.append(self.systemDynamics.get_state())
            errors.append(best_individual.fitness.values[0])

        return states, errors, states30, states60
