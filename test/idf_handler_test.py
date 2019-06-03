import sys
from typing import List
sys.path.append("../")
from moo.idfhandler import IdfIOStream
from shading_preamble import generate_struct

winwallrate = [0.15, 0.34, 0.23, 0.11]
args = [1, 1, 1]
direction = 300
airchange = 19

with IdfIOStream("../shading_model.idf", "newbase.idf", "idf") as idf:
    east_list: List = []
    west_list: List = []
    south_list: List = []
    north_list: List = []

    def op(lines: List[str], idx: int):
        wall_str = r"(.*)Exterior Wall" + str(args[0])  # re.sub
        roof_str = r"(.*)Exterior Roof" + str(args[1])
        win_str = r"(.*)Exterior Window" + str(args[2])
        coord_str = [r"[\s]+(-?(?:[\d+]|\d+\.[\de-]+))[,;].*Vertex .*"] * 3

        idf.sub([wall_str], r"\1Exterior Wall", lines, idx)  # DONE
        idf.sub([roof_str], r"\1Exterior Roof", lines, idx)  # DONE
        idf.sub([win_str], r"\1Exterior Window", lines, idx)  # DONE

        idf.grap(east_list, [r"[\s]+eastwall(.*\..*),", *coord_str,
                 *coord_str, *coord_str, *coord_str], lines, idx,
                 grouping=(1, 3, 3, 3, 3))
        idf.grap(west_list, [r"[\s]+westwall(.*\..*),", *coord_str,
                 *coord_str, *coord_str, *coord_str], lines, idx,
                 grouping=(1, 3, 3, 3, 3))
        idf.grap(south_list, [r"[\s]+southwall(.*\..*),", *coord_str,
                 *coord_str, *coord_str, *coord_str], lines, idx,
                 grouping=(1, 3, 3, 3, 3))
        idf.grap(north_list, [r"[\s]+northwall(.*\..*),", *coord_str,
                 *coord_str, *coord_str, *coord_str], lines, idx,
                 grouping=(1, 3, 3, 3, 3))

        idf.sub([r"(.*)\d+.\d+(.*North Axis.*)"], r"\g<1>{}\2".format(direction),
                lines, idx)
        idf.sub([r".*tongfengcishubianliang", r"([\s]+)\d+(.*Air Changes per Hour.*)"],
                r"\g<1>{}\2".format(str(airchange)), lines, idx)

    idf.apply(op)

    for w in east_list:
        idf.append(generate_struct("east", w[0], w[1:], winwallrate[0]))
    for w in west_list:
        idf.append(generate_struct("west", w[0], w[1:], winwallrate[0]))
    for w in south_list:
        idf.append(generate_struct("south", w[0], w[1:], winwallrate[0]))
    for w in north_list:
        idf.append(generate_struct("north", w[0], w[1:], winwallrate[0]))

    for line in idf.idf_lines:
        print(line)
