from typing import Tuple
import os
import sys
import glob
import subprocess


def init():
    # init the directory.
    if not os.path.exists("results"):
        os.mkdir("results")

    try:
        if glob.glob("*.idf") == []:
            raise IOError

        subprocess.call(["energyplus", "--help"], stdout=subprocess.DEVNULL)
    except IOError:
        print("[X] cannot find idf file.")
        sys.exit(1)
    except OSError:
        print("[X] cannot detect energyplus. Please make sure it is in the environment path.")
        sys.exit(1)

    if os.listdir("./results") != []:
        clear_results_flag = input("Detected files in {}. Delete?(Y/n)".format(os.path.abspath('./results')))
        if clear_results_flag == "Y":
            for f in os.listdir("./results"):  # clean up.
                os.remove(os.path.abspath(os.path.join('./results', f)))


def discrete_interval(t: Tuple[int, int]):
    # Create the correct boundary for interger only interval.
    # NOTE: The algorithm still yields a float, so it is
    #   required to manually convert it into int when the parameter
    #   is used.
    # ex. (1, 8) become (-0.99, 7.99), so int get (0 - 7)
    lower, upper = t
    return (lower - 1.01, upper - 0.01)
