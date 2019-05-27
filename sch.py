"""
The classic sch problem
It is used for verifying the correctness of the alogirhm.
"""
from nsga2.problem import Problem
from nsga2.evolution import Evolution
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from utils import discrete_interval
from plot import plot
import os


if os.listdir("./results") != []:
    clear_results_flag = input("Detected files in {}. Delete?(Y/n)".format(os.path.abspath('./results')))
    if clear_results_flag == "Y":
        for f in os.listdir("./results"):  # clean up.
            os.remove(os.path.abspath(os.path.join('./results', f)))


def f1(x, y, z):
    return x**2 + y - z


def f2(x, y, z):
    return (x-2)**2 + y + z


def f3(x, y, z):
    return x**2 + 1 + y - z


problem = Problem(num_of_variables=3, objectives=[f1, f2, f3], variables_range=[(0, 55), (0, 100), (0, 20)])
evo = Evolution(problem, num_of_generations=40, num_of_individuals=500, concurrency=True)
evol = evo.evolve()

plot("good", evol)
