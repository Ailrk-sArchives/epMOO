""" the main program """
from typing import List

from mpl_toolkits.mplot3d import Axes3D

from nsga2.problem import Problem
from nsga2.evolution import Evolution
import matplotlib.pyplot as plt

from objective_functions import f1_energy_consumption as f1
from objective_functions import f2_aPMV as f2
from objective_functions import f3_economy as f3
from utils import preamble


def main():
    """parameter config"""
    outerwall = (1, 7)
    roof = (1, 7)
    window = (1, 3)
    easterate = (0.05, 0.3)
    westrate = (0.05, 0.3)
    southrate = (0.05, 0.3)
    northrate = (0.05, 0.3)
    direction = (0, 359)
    airchange = (0, 39)
    paras = [outerwall, roof, window, easterate, westrate, southrate,
             northrate, direction, airchange]
    """"""

    # define problem.
    problem = Problem(num_of_variables=50, objectives=[f1, f2, f3],
                      variables_range=paras, preamble=preamble)

    evo = Evolution(problem, mutation_param=20, num_of_generations=500)
    func = [i.objectives for i in evo.evolve()]

    obj1 = [i[0] for i in func]
    obj2 = [i[1] for i in func]
    obj3 = [i[2] for i in func]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(obj1, obj2, obj3, c='r', marker='o')


if __name__ == "__main__":
    main()
