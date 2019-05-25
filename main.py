""" the main program """
from typing import List

from mpl_toolkits.mplot3d import Axes3D

from nsga2.problem import Problem
from nsga2.evolution import Evolution
import matplotlib.pyplot as plt

from objective_functions import f1_energy_consumption as f1
from objective_functions import f2_aPMV as f2
from objective_functions import f3_economy as f3
from obj_func_preamble import preamble
from utils import discrete_interval


def main():
    """parameter"""
    outerwall = discrete_interval((1, 7))
    roof = discrete_interval((1, 7))
    window = discrete_interval((1, 3))
    easterate = (0.05, 0.3)
    westrate = (0.05, 0.3)
    southrate = (0.05, 0.3)
    northrate = (0.05, 0.3)
    direction = (0, 359)
    airchange = (0, 39)
    paras = [outerwall, roof, window, easterate, westrate, southrate,
             northrate, direction, airchange]
    """"""

    """Algorithm parameter"""

    MUTATION_PARAM = 2
    NUM_OF_GENERATIONS = 100
    NUM_OF_INDIVIDUALS = 10
    NUM_OF_TOUR_PARTICIPS = 2
    """"""

    # define problem.
    problem = Problem(num_of_variables=len(paras), objectives=[f1, f2, f3],
                      variables_range=paras, preamble=preamble)

    evo = Evolution(problem,
                    mutation_param=MUTATION_PARAM,
                    num_of_generations=NUM_OF_GENERATIONS,
                    num_of_individuals=NUM_OF_INDIVIDUALS,
                    num_of_tour_particips=NUM_OF_TOUR_PARTICIPS)
    func = [i.objectives for i in evo.evolve()]

    obj1 = [i[0] for i in func]
    obj2 = [i[1] for i in func]
    obj3 = [i[2] for i in func]

    for o in list(zip(obj1, obj2, obj3)):
        print(o)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(obj1, obj2, obj3, c='r', marker='o')
    plt.draw()
    plt.show()


if __name__ == "__main__":
    main()
