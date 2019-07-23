"""
Reshape the result of epMOO into csv
"""
import getopt
import sys
import csv
from typing import TextIO, List, Tuple, Callable, Optional
from collections import namedtuple


Objectives = namedtuple('Objectives', ("Energy", "apmv", "LCC"))
Parameters = namedtuple('Parameters',
                        ("exterior_wall", "exterior_roof", "exterior_window",
                         "eastrate", "westrate", "southrate", "northrate",
                         "direction", "airchange", "cop", "east", "west",
                         "south", "north", "infiltration"))

ResTuple = Tuple[Objectives, Parameters]

res: List[ResTuple] = []


def res_to_csv(res: List[ResTuple]):
    with open('out.csv', 'w', newline='') as csvfile:
        fieldnames: List = ["Energy", "apmv", "LCC", "","exterior_wall",
                            "exterior_roof", "exterior_window", "eastrate",
                            "westrate", "southrate", "northrate", "direction",
                            "airchange", "cop", "east", "west", "south", "north",
                            "infiltration"]
        obj_header: slice = slice(0, 3)
        para_header: slice = slice(4, None)

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for o, p in res:
            odict = dict(zip(fieldnames[obj_header], o))
            spacedict = {"": " "}
            pdict = dict(zip(fieldnames[para_header], p))
            writer.writerow({**odict, **pdict, **spacedict})


def make_res_tuple(params: Parameters) -> Callable:
    def get_objs(objectives: Objectives) -> ResTuple:
        return (objectives, params)
    return get_objs


if __name__ == "__main__":
    filename: str = ""

    try:
        # Short option syntax: "hv:"
        # Long option syntax: "help" or "verbose="
        opts, args = getopt.getopt(sys.argv[1:], "hf:", ["help", "file="])

    except getopt.GetoptError as err:
        # Print debug info
        print(err)

    for option, argument in opts:
        if option in ("-h", "--help"):
            print("Reshape the result of epMOO output")
            print("usage: python reshape.py -f <filename>")

        elif option in ("-f", "--file"):
            filename = str(argument)

    with open(filename, 'r') as f:
        p: Optional[Parameters] = None
        o: Optional[Objectives] = None
        period: int = 2
        seq: int = 0

        for line in f.readlines():
            if "parameters" in line and seq % period == 0:
                tmp_list = line.split('[')[1].split(']')[0].split(',')
                para_list = [n.strip() for n in tmp_list]

                p = Parameters(*para_list)
                seq += 1

            elif "objectives" in line and seq % period == 1:
                tmp_list = line.split('[')[1].split(']')[0].split(',')
                obj_list = [n.strip() for n in tmp_list]

                o = Objectives(*obj_list)
                seq += 1

                if p and o:
                    rtuple = make_res_tuple(p)(o)
                    p = o = None

                    res.append(rtuple)

    res_to_csv(res)
