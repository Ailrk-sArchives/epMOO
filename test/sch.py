"""
The classic sch problem
It is used for verifying the correctness of the alogirhm.
"""
import os
import sys
sys.path.append("../")
from moo.nsga2.problem import Problem
from moo.nsga2.evolution import Evolution
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


if os.path.exists("results") and os.listdir("./results") != []:
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
evo = Evolution(problem, num_of_generations=40, num_of_individuals=100, concurrency=True)
evol = evo.evolve()

func = [i.objectives for i in evol]

obj1 = [i[0] for i in func]
obj2 = [i[1] for i in func]
obj3 = [i[2] for i in func]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(obj1, obj2, obj3, c='r', marker='o')

plt.draw()
plt.savefig('results/good.png')
plt.show()



