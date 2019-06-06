""" the main program """
import time
from typing import List, Dict
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from moo.nsga2.problem import Problem
from moo.nsga2.evolution import Evolution

from shading_obj_func import f1_energy_consumption as f1
from shading_obj_func import f2_aPMV as f2
from shading_obj_func import f3_economy as f3
# from obj_func_preamble import preamble
from shading_preamble import ShadingPreamble

from moo.utils import init
from moo.utils import discrete_interval
from moo.utils import scale_interval


def main():
    """parameter"""
    outerwall = discrete_interval((1, 10))  # yield 0-7
    roof = discrete_interval((1, 9))
    window = discrete_interval((1, 3))
    easterate = (0.05, 0.3)
    westrate = (0.05, 0.3)
    southrate = (0.05, 0.3)
    northrate = (0.05, 0.3)
    direction = (0, 359)
    airchange = (0, 39)
    cop = (2.0, 3.5)
    east_shading = discrete_interval((0, 1))
    west_shading = discrete_interval((0, 1))
    south_shading = discrete_interval((0, 1))
    north_shading = discrete_interval((0, 1))
    infiltration_air_change = discrete_interval(scale_interval((0.5, 1.0)))  # yield 5 - 10
    # shading_direction = discrete_interval((1, 4))  # shading in east, west, south, north respectively.
    paras = [outerwall, roof, window,
             easterate, westrate, southrate,
             northrate, direction, airchange,
             cop, east_shading, west_shading,
             south_shading, north_shading, infiltration_air_change]

    """Algorithm parameter"""
    hyperparameter = {
        "MUTATION_PARAM": 2,
        "NUM_OF_GENERATIONS": 3,
        "NUM_OF_INDIVIDUALS": 4,
        "NUM_OF_TOUR_PARTICIPS": 2,
        "CONCURRENCY": True,
        "MAX_PROC": 4
    }

    """other constants"""
    shading_model_constants: Dict = {
        "FLOOR_HEIGHT": 3,
        "WINDOW_HEIGHT": 1.5,
        "WINDOW_EDG_HEIGHT": 1,
        "HEATING_SETPOINT": 18,  # NOTE new param 2019-06-04
        "COOLING_SETPOINT": 26
    }

    """path constants"""
    shading_model_paths: Dict = {
        "WEATHER_FILE": "./WeatherData/CHN_Chongqing.Chongqing.Shapingba.575160_CSWD.epw",
        "IDF_FILE": "shading_model_6-0603-1.idf",
        "OUTPUT_PATH": "temp/",
    }

    # main
    moo(paras, hyperparameter, shading_model_constants, shading_model_paths)


def moo(paras: List, hyperparameter: Dict, constants: Dict, paths: Dict):
    init()

    # define problem.
    problem = Problem(num_of_variables=len(paras), objectives=[f1, f2, f3],
                      variables_range=paras,
                      preamble=ShadingPreamble(constants=constants, paths=paths))

    evo = Evolution(
        problem,
        mutation_param=hyperparameter["MUTATION_PARAM"],
        num_of_generations=hyperparameter["NUM_OF_GENERATIONS"],
        num_of_individuals=hyperparameter["NUM_OF_INDIVIDUALS"],
        num_of_tour_particips=hyperparameter["NUM_OF_TOUR_PARTICIPS"],
        concurrency=hyperparameter["CONCURRENCY"],
        max_proc=hyperparameter["MAX_PROC"])

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


if __name__ == "__main__":
    main()
