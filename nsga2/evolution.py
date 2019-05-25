from nsga2.utils import NSGA2Utils
from nsga2.population import Population
import time
import os

class Evolution:

    def __init__(self, problem, num_of_generations=1000, num_of_individuals=100, num_of_tour_particips=2, tournament_prob=0.9, crossover_param=2, mutation_param=5):
        self.utils = NSGA2Utils(problem, num_of_individuals, num_of_tour_particips, tournament_prob, crossover_param, mutation_param)
        self.population = None
        self.num_of_generations = num_of_generations
        self.on_generation_finished = []
        self.num_of_individuals = num_of_individuals

    def evolve(self):
        self.population = self.utils.create_initial_population()
        self.utils.fast_nondominated_sort(self.population)
        for front in self.population.fronts:
            self.utils.calculate_crowding_distance(front)
        children = self.utils.create_children(self.population)
        returned_population = None

        for i in range(self.num_of_generations):
            print("Generation {} startde at {}".format(i, time.ctime()))  # DEBUG info

            self.population.extend(children)
            self.utils.fast_nondominated_sort(self.population)
            new_population = Population()
            front_num = 0
            while len(new_population) + len(self.population.fronts[front_num]) <= self.num_of_individuals:
                self.utils.calculate_crowding_distance(self.population.fronts[front_num])
                new_population.extend(self.population.fronts[front_num])
                front_num += 1
            self.utils.calculate_crowding_distance(self.population.fronts[front_num])
            self.population.fronts[front_num].sort(key=lambda individual: individual.crowding_distance, reverse=True)
            new_population.extend(self.population.fronts[front_num][0:self.num_of_individuals-len(new_population)])
            returned_population = self.population
            self.population = new_population
            self.utils.fast_nondominated_sort(self.population)
            for front in self.population.fronts:
                self.utils.calculate_crowding_distance(front)
            children = self.utils.create_children(self.population)

            self.log(i, returned_population, "results")  # log out. 2019-05-24
        return returned_population.fronts[0]

    def log(self, current_gen, returned_population, path):
        log_path = os.path.join(os.path.abspath(path), str(current_gen) + ".txt")
        log = "Generation {} at {}\n".format(current_gen, time.ctime())
        for individual in returned_population.fronts[0]:  # log output.
            log += "parameters:\n"
            for para in individual.features:
                log += str(para) + ", "
            log += "\nobjectives:\n"
            for obj in individual.objectives:
                log += str(obj) + ", "
            log += "\n\n"
        with open(log_path, "w") as f:
            f.write(log)