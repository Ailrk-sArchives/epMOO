from utils import discrete_interval
from moo import moo

"""parameter"""
outerwall = discrete_interval((1, 8))  # yield 0-7
roof = discrete_interval((1, 8))
window = discrete_interval((1, 3))
easterate = (0.05, 0.3)
westrate = (0.05, 0.3)
southrate = (0.05, 0.3)
northrate = (0.05, 0.3)
direction = (0, 359)
airchange = (0, 39)
paras = [outerwall, roof, window, easterate, westrate, southrate,
         northrate, direction, airchange]

"""Algorithm parameter"""
hyperparameter = {
        "MUTATION_PARAM": 2,
        "NUM_OF_GENERATIONS": 50,
        "NUM_OF_INDIVIDUALS": 15,
        "NUM_OF_TOUR_PARTICIPS": 2
}

if __name__ == "__main__":
    moo(paras, hyperparameter)
