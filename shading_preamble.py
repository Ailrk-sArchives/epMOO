from moo.idfhandler import Preamble, override, IdfModel, IdfIOStream, SearchAnchor, SubAnchor
from typing import Dict, List, Tuple
import os
import time
import subprocess


# paras = [outerwall, roof, window, easterate, westrate, southrate,
#          northrate, direction, airchange, cop, shading]


class ShadingPreamble(Preamble):
    """
    User defined preamble for shading idf.
    """
    def __init__(self, constants: Dict, paths: Dict, *args):
        super().__init__(constants=constants, paths=paths)
        self.east_list: List = []
        self.west_list: List = []
        self.south_list: List = []
        self.north_list: List = []

    @override
    def __call__(self, *args):
        super().__call__(*args)
        self.__create_pid_dir()
        self._output_idf_file = os.path.join(self._paths["OUTPUT_PATH"], self._pid, "in.idf")  # temp/pid/in.idf

        winwallrate = self._args[3:7]
        shading_dirs = self._args[10:14]

        with IdfIOStream(input_path=self._paths["IDF_FILE"],
                         output_path=self._output_idf_file, mode="idf") as idf:

            print("applying preamble in {}".format(self._pid))
            idf.apply(self._operator)  # apply operator.

            # appaned newly calculated structures.
            for w in self.east_list:
                data = self.generate_window("east", w[0], w[1:], winwallrate[0], shading_dirs)
                idf.append(data)
            for w in self.west_list:
                data = self.generate_window("west", w[0], w[1:], winwallrate[1], shading_dirs)
                idf.append(data)
            for w in self.south_list:
                data = self.generate_window("south", w[0], w[1:], winwallrate[2], shading_dirs)
                idf.append(data)
            for w in self.north_list:
                data = self.generate_window("north", w[0], w[1:], winwallrate[3], shading_dirs)
                idf.append(data)

        self.run_energy_plus()  # file will be written when out of the context manager.

    @override
    def _operator(self, idf: IdfModel, lines: List[str], idx: int):

        direction = self._args[7]
        infiltration_air_change = self._args[14]
        # airchange = self._args[8]

        # change Exterior Wall
        wall_str = r"(.*)Exterior Wall" + str(int(self._args[0]))  # re.sub
        roof_str = r"(.*)Exterior Roof" + str(int(self._args[1]))
        win_str = r"(.*)Exterior Window" + str(int(self._args[2]))
        coord_str = [r"[\s]+(-?(?:[\d+]|\d+\.[\de-]+))[,;].*Vertex .*"] * 3
        idf.sub(
            [
                wall_str
            ],
            r"\1Exterior Wall",
            lines, idx
        )
        idf.sub(
            [
                roof_str
            ],
            r"\1Exterior Roof",
            lines, idx
        )
        idf.sub(
            [
                win_str
            ],
            r"\1Exterior Window",
            lines, idx
        )

        # grap wall coordinates
        idf.grap(
            self.east_list,
            [
                r"[\s]+eastwall(.*\..*),",
                *coord_str,
                *coord_str,
                *coord_str,
                *coord_str
            ],
            lines, idx,
            grouping=(1, 3, 3, 3, 3)
        )

        idf.grap(
            self.west_list,
            [
                r"[\s]+westwall(.*\..*),",
                *coord_str,
                *coord_str,
                *coord_str,
                *coord_str
            ],
            lines, idx,
            grouping=(1, 3, 3, 3, 3)
        )

        idf.grap(
            self.south_list,
            [
                r"[\s]+southwall(.*\..*),",
                *coord_str,
                *coord_str,
                *coord_str,
                *coord_str
            ],
            lines, idx,
            grouping=(1, 3, 3, 3, 3)
        )

        idf.grap(
            self.north_list,
            [
                r"[\s]+northwall(.*\..*),",
                *coord_str,
                *coord_str,
                *coord_str,
                *coord_str
            ],
            lines, idx,
            grouping=(1, 3, 3, 3, 3)
        )

        idf.sub(
            [
                SubAnchor.numeric_value(r"North Axis")
            ],
            r"\g<1>{}\g<2>".format(direction),
            lines, idx
        )

        idf.sub(
            [

                SearchAnchor.bypass_anchor(r"ZoneInfiltration:DesignFlowRate"),
                SubAnchor.numeric_value(r" Air Changes per Hour \{1/hr\}")
            ],
            r"\g<1>{}\g<2>".format(infiltration_air_change),
            lines, idx
        )

        # set the a heating setpoint.
        idf.sub(
            [
                SearchAnchor.bypass_anchor("Heating setpoint"),
                SubAnchor.numeric_value("Field 4")
            ],
            r"\g<1>{}\g<2>".format(self._constants["HEATING_SETPOINT"]),
            lines, idx
        )

        idf.sub(
            [
                SearchAnchor.bypass_anchor("Heating setpoint"),
                SubAnchor.numeric_value("Field 6")
            ],
            r"\g<1>{}\g<2>".format(self._constants["HEATING_SETPOINT"]),
            lines, idx
        )

        idf.sub(
            [
                SearchAnchor.bypass_anchor("Heating setpoint"),
                SubAnchor.numeric_value("Field 14")
            ],
            r"\g<1>{}\g<2>".format(self._constants["HEATING_SETPOINT"]),
            lines, idx
        )

        idf.sub(
            [
                SearchAnchor.bypass_anchor("Heating setpoint"),
                SubAnchor.numeric_value("Field 16")
            ],
            r"\g<1>{}\g<2>".format(self._constants["HEATING_SETPOINT"]),
            lines, idx
        )

        # set the cooling set point.
        idf.sub(
            [
                SearchAnchor.bypass_anchor("Cooling setpoint"),
                SubAnchor.numeric_value("Field 4")
            ],
            r"\g<1>{}\g<2>".format(self._constants["COOLING_SETPOINT"]),
            lines, idx
        )

        idf.sub(
            [
                SearchAnchor.bypass_anchor("Cooling setpoint"),
                SubAnchor.numeric_value("Field 8")
            ],
            r"\g<1>{}\g<2>".format(self._constants["COOLING_SETPOINT"]),
            lines, idx
        )

        idf.sub(
            [
                SearchAnchor.bypass_anchor("Cooling setpoint"),
                SubAnchor.numeric_value("Field 12")
            ],
            r"\g<1>{}\g<2>".format(self._constants["COOLING_SETPOINT"]),
            lines, idx
        )

    def generate_window(self, direction: str, floor_num: str, pos: List[Tuple], rate: float, shading_dirs: List) -> List[str]:
        # convert pos from string to float
        # pos = [(x1, y1, z1)
        #        (x2, y2, z2)
        #        (x3, y3, z3)
        #        (x4, y4, z4)]
        data = []
        pos = [tuple([float(e.strip()) for e in one_point]) for one_point in pos]
        new_coord: List = [[], [], [], []]
        CB0, CB1, CB2, CB3 = self.__calculate_win_pos(direction, floor_num, pos, rate)
        shading = self.__shading_direction(direction, shading_dirs)

        # calculate the coordiate according to the direction.
        if direction == "east":
            new_coord[0] = [pos[0][0], CB0, CB3]
            new_coord[1] = [pos[1][0], CB0, CB2]
            new_coord[2] = [pos[2][0], CB1, CB2]
            new_coord[3] = [pos[3][0], CB1, CB3]

        elif direction == "west":
            new_coord[0] = [pos[0][0], CB1, CB3]
            new_coord[1] = [pos[1][0], CB1, CB2]
            new_coord[2] = [pos[2][0], CB0, CB2]
            new_coord[3] = [pos[3][0], CB0, CB3]

        elif direction == "south":
            new_coord[0] = [CB0, pos[0][1], CB3]
            new_coord[1] = [CB0, pos[1][1], CB2]
            new_coord[2] = [CB1, pos[2][1], CB2]
            new_coord[3] = [CB1, pos[3][1], CB3]

        elif direction == "north":
            new_coord[0] = [CB1, pos[0][1], CB3]
            new_coord[1] = [CB1, pos[1][1], CB2]
            new_coord[2] = [CB0, pos[2][1], CB2]
            new_coord[3] = [CB0, pos[3][1], CB3]

        # construct the data.
        data.append("\n")
        data.append("FenestrationSurface:Detailed,\n")
        data.append("    " + direction + "window" + floor_num + ",           \n")
        data.append("    Window,                  !- Surface Type\n")
        data.append("    Exterior Window,         !- Construction Name\n")
        data.append("    " + direction + "wall" + floor_num + ",           !- Name\n")
        data.append("    ,                        !- Outside Boundary Condition Object\n")
        data.append("    ,                        !- View Factor to Ground\n")
        data.append("    " + shading + "                        !- Shading Control Name\n")
        data.append("    ,                        !- Frame and Divider Name\n")
        data.append("    ,                        !- Multiplier\n")
        data.append("    4,                       !- Number of Vertices\n")

        data.append("    " + "{:.12f}, {:.12f}, {:.12f},\n".format(new_coord[0][0], new_coord[0][1], new_coord[0][2]))
        data.append("                                        !- X,Y,Z  1 {m}\n")
        data.append("    " + "{:.12f}, {:.12f}, {:.12f},\n".format(new_coord[1][0], new_coord[1][1], new_coord[1][2]))
        data.append("                                        !- X,Y,Z  2 {m}\n")
        data.append("    " + "{:.12f}, {:.12f}, {:.12f},\n".format(new_coord[2][0], new_coord[2][1], new_coord[2][2]))
        data.append("                                        !- X,Y,Z  3 {m}\n")
        data.append("    " + "{:.12f}, {:.12f}, {:.12f};\n".format(new_coord[3][0], new_coord[3][1], new_coord[3][2]))
        data.append("                                        !- X,Y,Z  4 {m}\n")

        return data

    def __calculate_win_pos(self, direction: str, floor_num: str, pos: List[Tuple], rate: float) -> Tuple:
        # calculate window coordinate base on the winwallrate, floor, and dir.
        assert len(pos) == 4, "pos has wrong dimension {}".format(len(pos))
        assert direction in ("east", "west", "south", "north")

        p1 = 0.0
        p2 = 0.0
        if direction == "east" or direction == "west":
            p1 = min(list(zip(*pos))[1])  # get max and min Y positions
            p2 = max(list(zip(*pos))[1])  # delta y
        else:
            p1 = min(list(zip(*pos))[0])  # get max and min X positions
            p2 = max(list(zip(*pos))[0])  # delta x
        wall_length = abs(p2 - p1)
        # floor = int(floor_num.split(".")[0])  # get floor number.

        # calculate coordinate for window according to wall coordinates.
        wall_area = wall_length * self._constants["FLOOR_HEIGHT"]
        window_area = wall_area * rate
        window_length = window_area / self._constants["WINDOW_HEIGHT"]
        CB0 = (wall_length - window_length) / 2 + p1  # win x axis on one side
        CB1 = p2 - (wall_length - window_length) / 2  # win x axis on the other side.
        # CB2 = (floor - 1) * self._constants["FLOOR_HEIGHT"] + self._constants["WINDOW_EDG_HEIGHT"]
        CB2 = self._constants["FLOOR_HEIGHT"] + self._constants["WINDOW_EDG_HEIGHT"]  # lower win y axis
        CB3 = CB2 + self._constants["WINDOW_HEIGHT"]  # upper win y axis

        return (CB0, CB1, CB2, CB3)

    def __shading_direction(self, direction, shading_dirs: List) -> str:
        # control the shading base on the direction.
        dir_map = {"east": 0, "west": 1, "south": 2, "north": 3}
        s = [int(n) for n in shading_dirs]
        return "external shading control," if s[dir_map[direction]] == 1 else ","

    def run_energy_plus(self):
        output_dir = os.path.join(os.path.abspath(self._paths["OUTPUT_PATH"]), self._pid)
        run_idf_file = os.path.join(os.path.abspath("temp"), self._pid, "run.idf")
        original_path = os.path.abspath(os.curdir)

        print("<running ExpandObjects in {} >".format(self._pid))
        os.chdir(output_dir)
        subprocess.run(["ExpandObjects"])
        try:
            os.rename("expanded.idf", "run.idf")
        except IOError:
            print("Error when running ExpandObjects. No idf file generated.")
            raise
        os.chdir(original_path)

        print("<start running ep in pid {} at {}>".format(self._pid, time.ctime()))
        subprocess.run([
            "energyplus",
            "-w", self._paths["WEATHER_FILE"],
            "-r",
            "-d", output_dir,
            run_idf_file  # THIS will break single proc
        ])
        print("<end ep in pid {} at {}>".format(self._pid, time.ctime()))

    def __create_pid_dir(self, ):
        pid_dir = os.path.join(self._paths["OUTPUT_PATH"], self._pid)  # temp/pid/in.idf
        if not os.path.exists(os.path.abspath('temp')):
            os.mkdir(os.path.mkdir(os.path.abspath('temp')))
        if not os.path.exists(pid_dir):
            os.mkdir(pid_dir)
        # shutil.copy('./Energy+.idd', pid_dir)

