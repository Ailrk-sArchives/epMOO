from typing import Tuple
import os
import sys
import glob
import subprocess


def init():
    # init the directory.
    if not os.path.exists("results"):
        os.mkdir("results")
    if not os.path.exists("temp"):
        os.mkdir("temp")

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


def discrete_interval(t: Tuple[float, float]):
    # create close interval s.t boundary int can be reached.
    lower, upper = t
    return (lower, upper + 0.9999)


def interval_to_list_idx(n: float):
    # convert value generated from interval into list index.
    return int(n - 1)


def scale_interval(t: Tuple[float, float], coefficient: float):
    lower, upper = t
    lower = lower * coefficient
    upper = upper * coefficient
    return (lower, upper)

