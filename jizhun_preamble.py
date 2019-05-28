from idfhandler import Preamble, override, IdfModel, IdfIOStream
from typing import Dict, Callable, List, Tuple
import os
import time
import subprocess


jizhun_paths: Dict = {
        "WEATHER_FILE":
        "./WeatherData/CHN_Chongqing.Chongqing.Shapingba.575160_CSWD.epw",
        "IDF_FILE": "jizhun.idf",
        "OUTPUT_PATH": "temp/",
        }

jizhun_constants: Dict = {
        "FLOOR_HEIGHT": 2.8,
        "WINDOW_HEIGHT": 1.5,
        "WINDOW_EDGT_HEIGHT": 1
        }


class JizhunPreamble(Preamble):
    """
    User defined preamble for jizhun idf.
    """
    def __init__(self, constants: Dict, paths: Dict, *args):
        super().__init__(constants=constants, paths=paths)
        self._output_idf_file = os.path.join(self._paths["OUTPUT_PATH"], self._pid + ".idf")
        self.east_list: List = []
        self.west_list: List = []
        self.south_list: List = []
        self.north_list: List = []

    @override
    def __call__(self, *args):
        super().__call__(*args)

        winwallrate = self._args[3:7]
        with IdfIOStream(input_path=self._paths["IDF_FILE"],
                         output_path=self._output_idf_file, mode="idf") as idf:

            print("applying preamble in {}".format(self._pid))
            idf.apply(self._operator)  # apply operator.

            # appaned newly calculated structures.
            for w in self.east_list:
                data = self.generate_struct("east", w[0], w[1:], winwallrate[0])
                idf.append(data)
            for w in self.west_list:
                data = self.generate_struct("west", w[0], w[1:], winwallrate[1])
                idf.append(data)
            for w in self.south_list:
                data = self.generate_struct("south", w[0], w[1:], winwallrate[2])
                idf.append(data)
            for w in self.north_list:
                data = self.generate_struct("north", w[0], w[1:], winwallrate[3])
                idf.append(data)
        self.run_energy_plus()

    @override
    def _operator(self, idf: IdfModel, lines: List[str], idx: int):
        direction = self._args[7]
        airchange = self._args[8]

        # change Exterior Wall
        wall_str = r"(.*)Exterior Wall" + str(int(self._args[0]))  # re.sub
        roof_str = r"(.*)Exterior Roof" + str(int(self._args[1]))
        win_str = r"(.*)Exterior Window" + str(int(self._args[2]))
        coord_str = r"[\s]+(\d+\.\d+),.*(\d+\.\d+),.*(\d+\.\d+)[,;]"

        idf.sub([wall_str], r"\1Exterior Wall", lines, idx)
        idf.sub([roof_str], r"\1Exterior Roof", lines, idx)
        idf.sub([win_str], r"\1Exterior Window", lines, idx)

        idf.grap(self.east_list, [r"[\s]+eastwall(.*\..*),", coord_str,
                 coord_str, coord_str, coord_str], lines, idx)
        idf.grap(self.west_list, [r"[\s]+westwall(.*\..*),", coord_str,
                 coord_str, coord_str, coord_str], lines, idx)
        idf.grap(self.south_list, [r"[\s]+southwall(.*\..*),", coord_str,
                 coord_str, coord_str, coord_str], lines, idx)
        idf.grap(self.north_list, [r"[\s]+northwall(.*\..*),", coord_str,
                 coord_str, coord_str, coord_str], lines, idx)

        idf.sub([r"(.*)\d+.\d+(.*North Axis.*)"], r"\g<1>{}\2".format(direction),
                lines, idx)
        idf.sub([r".*tongfengcishubianliang", r"([\s]+)\d+(.*Air Changes per Hour.*)"], r"\g<1>{}\2".format(str(airchange)), lines, idx)

    def generate_struct(self, direction: str, floor_num: str, pos: List[tuple], rate: float) -> List[str]:
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
        wall_area = wall_length * self._constants["FLOOR_HEIGHT"]
        window_area = wall_area * rate

        window_length = window_area / self._constants["WINDOW_HEIGHT"]

        CB[0] = (wall_length - window_length) / 2 + p1  # win x axis1
        CB[1] = p2 - (wall_length - window_length) / 2  # win x axis2
        CB[2] = (floor - 1) * self._constants["FLOOR_HEIGHT"] + self._constants["WINDOW_EDGT_HEIGHT"]
        CB[3] = CB[2] + self._constants["WINDOW_HEIGHT"]  # win y axis2

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

    def run_energy_plus(self):
        output_dir = os.path.join(self._paths["OUTPUT_PATH"], self._pid)
        run_idf_file = os.path.join(os.path.abspath("temp"), self._pid + ".idf")

        print("<start running ep in pid {} at {}>".format(self._pid, time.ctime()))
        subprocess.run([
                "energyplus",
                "-w", self._paths["WEATHER_FILE"],
                "-r",
                "-d", output_dir,
                run_idf_file  # THIS will break single proc
            ])
        print("<end ep in pid {} at {}>".format(self._pid, time.ctime()))

