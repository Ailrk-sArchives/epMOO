""" the main program """
from typing import List, Dict
import time

from mpl_toolkits.mplot3d import Axes3D

from nsga2.problem import Problem
from nsga2.evolution import Evolution
import matplotlib.pyplot as plt

from objective_functions import f1_energy_consumption as f1
from objective_functions import f2_aPMV as f2
from objective_functions import f3_economy as f3
# from obj_func_preamble import preamble
from jizhun_preamble import JizhunPreamble, jizhun_paths, jizhun_constants

from utils import init


def moo(paras: List, hyperparameter: Dict):
    init()

    # define problem.
    problem = Problem(num_of_variables=len(paras), objectives=[f1, f2, f3],
                      variables_range=paras,
                      preamble=JizhunPreamble(constants=jizhun_constants, paths=jizhun_paths))

    evo = Evolution(
            problem,
            mutation_param=hyperparameter["MUTATION_PARAM"],
            num_of_generations=hyperparameter["NUM_OF_GENERATIONS"],
            num_of_individuals=hyperparameter["NUM_OF_INDIVIDUALS"],
            num_of_tour_particips=hyperparameter["NUM_OF_TOUR_PARTICIPS"],
            concurrency=hyperparameter["CONCURRENCY"])

    # draw the last one with 3d box.
    func = [i.objectives for i in evo.evolve()]

    obj1 = [i[0] for i in func]
    obj2 = [i[1] for i in func]
    obj3 = [i[2] for i in func]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(obj1, obj2, obj3, c='r', marker='o')
    plt.draw()
    plt.savefig('results/epMOO_fig.png')
    plt.show()

    print("<Finished>{}".format(time.ctime()))
