from copy import deepcopy

from DataAnalyzer import DataAnalyzer
from GeneticAlgorithmEngine import GeneticAlgorithmEngine
import random
from deap import tools
from deap import base, creator


class TrafficEnvGAEngine(GeneticAlgorithmEngine):
    def __init__(self, config_file, generation, population, cxpb, mutpb, elitpb, sd):
        # TODO: ga_config_file_to_values 구현 후 파라미터 수정
        num_gen, num_pop, cross_prob, mut_prob, elit_prob = self.ga_config_file_to_values(config_file)
        num_gen, num_pop, cross_prob, mut_prob, elit_prob = generation, population, cxpb, mutpb, elitpb
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

    # TODO: implementation
    def ga_config_file_to_values(self, config_file):
        """
        read GA configuration file and return values
        :param config_file: GA configuration file
        :return: tuple of values of the configuration
        """
        configurations = (0, 0, 0, 0, 0)
        return configurations

    def selection(self, population):
        offspring = self.toolbox.select(population, int(len(population)*self.elitpb))
        new_offspring = self.toolbox.population(self.population-len(offspring))
        offspring = offspring + new_offspring
        return offspring

    def mutation(self, population):
        offspring = [self.toolbox.clone(ind) for ind in population]
        # Apply mutation on the offspring
        for i in range(len(offspring)):
            if random.random() < self.mutpb:
                offspring[i], = self.toolbox.mutate(offspring[i])
                del offspring[i].fitness.values
        return offspring

    def crossover(self, population):
        offspring = [self.toolbox.clone(ind) for ind in population]
        # Apply crossover on the offspring
        for i in range(1, len(offspring), 2):
            if random.random() < self.cxpb:
                offspring[i - 1], offspring[i] = self.toolbox.mate(offspring[i - 1], offspring[i])
                del offspring[i - 1].fitness.values, offspring[i].fitness.values
        return offspring

    def representation_to_output_flow_config(self, representation):
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

    def fitness_function(self, args):   # Gene is a SystemDynamicsGene configuration. Goal is a data. Fitness is an error.
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
        invalid_ind = [(ind, goal) for ind in population if not ind.fitness.valid]
        fitnesses = self.toolbox.map(self.toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind[0].fitness.values = fit

    def criteria_data_generation(self, goal_data_files):
        # TODO: output 식 생성 후 기존 식 삭제
        analyzer = DataAnalyzer()
        equation = analyzer.csv_data_to_equation(goal_data_files)

        equation = [
            [-1.00308443955e-06, 0.000109319671245, -0.00511030917602, 0.134225942574, -2.17652896364, 22.4438785859,
             -144.621055537, 532.931223015, -818.252752483, -135.884983131, 1687.82024869],
            [3.70204557043e-07, -4.30527893412e-05, 0.00207358064481, -0.0530091207001, 0.759046553612, -5.72292919652,
             15.6502621843, 43.4033809984, -251.353170233, 211.970138972, 185.741847391],
            [-6.81077097341e-07, 7.05429933723e-05, -0.00312725239443, 0.0786490224715, -1.26071509318, 13.651295323,
             -99.5380490007, 436.79472203, -807.739766424, 63.9682286788, 1491.71184382],
            [1.10815138667e-06, -0.000127221738881, 0.00611596653591, -0.159159351009, 2.41585005985, -21.3919198483,
             103.592131637, -232.82263525, 188.347476486, -78.1087346542, 400.365041013]
        ]

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
        goal_data = self.criteria_data_generation(goal_data_files)
        best_individual = None
        errors = []
        states = []

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

            # update system dynamics model to the next time using the searched best configuration.
            self.systemDynamics.set_config(self.representation_to_output_flow_config(best_individual))
            self.systemDynamics.update()
            states.append(self.systemDynamics.get_state())
            errors.append(best_individual.fitness.values[0])

        return states, errors
