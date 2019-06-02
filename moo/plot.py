from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from typing import List


def plot(name: str, front: List):
    func = [i.objectives for i in front]
    dimension = len(func[0])
    objs = [[obj[i] for obj in func] for i in range(dimension)]

    if dimension == 2:
        plt.xlabel("E", fontsize=15)
        plt.ylabel("aPMV", fontsize=15)
        plt.scatter(*objs, c='r', marker='o')
        plt.draw()
        plt.savefig(f'results/{name}.png')
    elif dimension == 3:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(*objs, c='r', marker='o')
        plt.draw()
        plt.savefig(f'results/{name}.png')

    else:
        print("Error in plot.py: dimension higher then 3 or is 1.")
    plt.close()
