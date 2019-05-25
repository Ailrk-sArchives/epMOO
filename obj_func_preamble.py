from typing import List, Tuple
import os
import subprocess
import idf_handler as Idfh

"""
There will be a new class handle this type of jobs exclusively for idf format.
"""


"""path parameters."""
W_PATH = "./WeatherData/CHN_Chongqing.Chongqing.Shapingba.575160_CSWD.epw"
OUTPUT_PATH = os.path.abspath("./temp/")
IDF_FILE = os.path.abspath("./jizhun.idf")
RUN_IDF_FILE = os.path.abspath("./temp.idf")
W_DATA = os.path.abspath(W_PATH)


"""function parameters"""
FLOOR_HEIGHT = 2.8
WINDOW_HEIGHT = 1.5
WINDOW_EDGT_HEIGHT = 1


def run_energy_plus():
    subprocess.run([
            "energyplus",
            "-w", W_DATA,
            "-r",
            "-d", OUTPUT_PATH,
            RUN_IDF_FILE
        ])


def generate_struct(direction: str, floor_num: str, pos: List[tuple], rate: float) -> List[str]:
    # convert pos from string to float
    # pos = [(x1, y1, z1)
    #        (x2, y2, z2)
    #        (x3, y3, z3)
    #        (x4, y4, z4)]

    data = []
    pos = [tuple([float(e.strip()) for e in one_point]) for one_point in pos]

    p1 = 0.0
    p2 = 0.0

    if direction == "east" or direction == "west":
        p1 = min(list(zip(*pos))[1])  # get max and min Y positions
        p2 = max(list(zip(*pos))[1])
    else:
        p1 = min(list(zip(*pos))[2])  # get max and min Z positions
        p2 = max(list(zip(*pos))[2])

    wall_length = abs(p2 - p1)

    floor = int(floor_num.split(".")[0])  # get floor number.

    # calculate coordinate for window according to coordinate for wall.
    CB: List = [0, 0, 0, 0]
    wall_area = wall_length * FLOOR_HEIGHT
    window_area = wall_area * rate

    window_length = window_area / WINDOW_HEIGHT

    CB[0] = (wall_length - window_length) / 2 + p1  # win x axis1
    CB[1] = p2 - (wall_length - window_length) / 2  # win x axis2
    CB[2] = (floor - 1) * FLOOR_HEIGHT + WINDOW_EDGT_HEIGHT  # win y axis1
    CB[3] = CB[2] + WINDOW_HEIGHT  # win y axis2

    new_coord: List = [[], [], [], []]

    # calculate the coordiate according to the direction.
    if direction == "east":
        new_coord[0] = [pos[0][0], CB[0], CB[3]]
        new_coord[1] = [pos[1][0], CB[0], CB[2]]
        new_coord[2] = [pos[2][0], CB[1], CB[2]]
        new_coord[3] = [pos[3][0], CB[1], CB[3]]

    elif direction == "west":
        new_coord[0] = [pos[0][0], CB[1], CB[3]]
        new_coord[1] = [pos[1][0], CB[1], CB[2]]
        new_coord[2] = [pos[2][0], CB[0], CB[2]]
        new_coord[3] = [pos[3][0], CB[0], CB[3]]

    elif direction == "south":
        new_coord[0] = [CB[0], pos[0][1], CB[3]]
        new_coord[1] = [CB[0], pos[1][1], CB[2]]
        new_coord[2] = [CB[1], pos[2][1], CB[2]]
        new_coord[3] = [CB[1], pos[3][1], CB[3]]

    elif direction == "north":
        new_coord[0] = [CB[1], pos[0][1], CB[3]]
        new_coord[1] = [CB[1], pos[1][1], CB[2]]
        new_coord[2] = [CB[0], pos[2][1], CB[2]]
        new_coord[3] = [CB[0], pos[3][1], CB[3]]

    # construct the data.
    data.append("\n")
    data.append("FenestrationSurface:Detailed,\n")
    data.append("    " + direction + "window" + floor_num + ",           \n")
    data.append("    Window,                  !- Surface Type\n")
    data.append("    Exterior Window,         !- Construction Name\n")
    data.append("    " + direction + "wall" + floor_num + ",           !- Name\n")
    data.append("    ,                        !- Outside Boundary Condition Object\n")
    data.append("    ,                        !- View Factor to Ground\n")
    data.append("    ,                        !- Shading Control Name\n")
    data.append("    ,                        !- Frame and Divider Name\n")
    data.append("    ,                        !- Multiplier\n")
    data.append("    4,                       !- Number of Vertices\n")

    data.append("    " + "{:.12f}, {:.12f}, {:.12f},\n".format(
                            new_coord[0][0], new_coord[0][1], new_coord[0][2]))
    data.append("                                        !- X,Y,Z  1 {m}\n")
    data.append("    " + "{:.12f}, {:.12f}, {:.12f},\n".format(
                            new_coord[1][0], new_coord[1][1], new_coord[1][2]))
    data.append("                                        !- X,Y,Z  2 {m}\n")
    data.append("    " + "{:.12f}, {:.12f}, {:.12f},\n".format(
                            new_coord[2][0], new_coord[2][1], new_coord[2][2]))
    data.append("                                        !- X,Y,Z  3 {m}\n")
    data.append("    " + "{:.12f}, {:.12f}, {:.12f};\n".format(
                            new_coord[3][0], new_coord[3][1], new_coord[3][2]))
    data.append("                                        !- X,Y,Z  4 {m}\n")
    return data


def preamble(*args):
    # defines args names

    print("=========================initializing============================>")
    winwallrate = args[3:7]
    direction = args[7]
    airchange = args[8]
    with Idfh.IdfIOStream(IDF_FILE, "idf") as idf:  # take idf template and modify
        # define op: Operator.

        east_list: List = []
        west_list: List = []
        south_list: List = []
        north_list: List = []

        def op(lines: List[str], idx: int):
            # TODO organize capture_list order.
            # change Exterior Wall
            wall_str = r"(.*)Exterior Wall" + str(int(args[0]))  # re.sub
            roof_str = r"(.*)Exterior Roof" + str(int(args[1]))
            win_str = r"(.*)Exterior Window" + str(int(args[2]))
            coord_str = r"[\s]+(\d+\.\d+),.*(\d+\.\d+),.*(\d+\.\d+)[,;]"

            idf.sub([wall_str], r"\1Exterior Wall", lines, idx)  # DONE
            idf.sub([roof_str], r"\1Exterior Roof", lines, idx)  # DONE
            idf.sub([win_str], r"\1Exterior Window", lines, idx)  # DONE

            idf.grap(east_list, [r"[\s]+eastwall(.*\..*),", coord_str,
                     coord_str, coord_str, coord_str], lines, idx)
            idf.grap(west_list, [r"[\s]+westwall(.*\..*),", coord_str,
                     coord_str, coord_str, coord_str], lines, idx)
            idf.grap(south_list, [r"[\s]+southwall(.*\..*),", coord_str,
                     coord_str, coord_str, coord_str], lines, idx)
            idf.grap(north_list, [r"[\s]+northwall(.*\..*),", coord_str,
                     coord_str, coord_str, coord_str], lines, idx)

            idf.sub([r"(.*)\d+.\d+(.*North Axis.*)"], r"\g<1>{}\2".format(direction),
                    lines, idx)
            idf.sub([r".*tongfengcishubianliang", r"([\s]+)\d+(.*Air Changes per Hour.*)"], r"\g<1>{}\2".format(str(airchange)), lines, idx)

        idf.apply(op)  # apply operator.

        # appaned newly calculated structures.
        for w in east_list:
            data = generate_struct("east", w[0], w[1:], winwallrate[0])
            idf.append(data)
        for w in west_list:
            data = generate_struct("west", w[0], w[1:], winwallrate[1])
            idf.append(data)
        for w in south_list:
            data = generate_struct("south", w[0], w[1:], winwallrate[2])
            idf.append(data)
        for w in north_list:
            data = generate_struct("north", w[0], w[1:], winwallrate[3])
            idf.append(data)

    run_energy_plus()
