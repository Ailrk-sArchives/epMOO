from flexx import flx
from typing import List, Dict
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import time
import sys

from moo.nsga2.problem import Problem
from moo.nsga2.evolution import Evolution

from wkx2132_obj_func import f1_energy_consumption as f1
from wkx2132_obj_func import f2_aPMV as f2
from wkx2132_obj_func import f3_economy as f3
# from obj_func_preamble import preamble
from wkx2132_preamble import Wkx2132Preamble

from moo.utils import discrete_interval
from moo.utils import scale_interval
from moo.utils import init
from typing import Tuple


class ModelParametersWidget(flx.GroupWidget):

    def init(self):
        self.set_title("MODEL PARAMTERS")
        with flx.FormLayout() as self.model_params_form:
            flx.Widget(flex=1)
            self.exterior_wall = flx.LineEdit(title='Exterior Wall', text='{}'.format(tuple(self.root.exterior_wall_tuple)))
            self.exterior_roof = flx.LineEdit(title='Exterior Roof', text='{}'.format(tuple(self.root.exterior_roof_tuple)))
            self.exterior_window = flx.LineEdit(title='Exterior Window', text='{}'.format(tuple(self.root.exterior_window_tuple)))
            self.eastrate = flx.LineEdit(title='East winwall ratio', text='{}'.format(tuple(self.root.eastrate_tuple)))
            self.westrate = flx.LineEdit(title='West winwall ratio', text='{}'.format(tuple(self.root.westrate_tuple)))
            self.southrate = flx.LineEdit(title='South winwall ratio', text='{}'.format(tuple(self.root.southrate_tuple)))
            self.northrate = flx.LineEdit(title='North winwall ratio', text='{}'.format(tuple(self.root.northrate_tuple)))
            self.direction = flx.LineEdit(title='direction(deg)', text='{}'.format(tuple(self.root.direction_tuple)))
            self.airchange = flx.LineEdit(title='airchange', text='{}'.format(tuple(self.root.airchange_tuple)))
            self.cop = flx.LineEdit(title='cop', text='{}'.format(tuple(self.root.cop_tuple)))
            self.east_shading = flx.LineEdit(title='east shading', text='{}'.format(tuple(self.root.east_shading_tuple)))
            self.west_shading = flx.LineEdit(title='west shading', text='{}'.format(tuple(self.root.west_shading_tuple)))
            self.south_shading = flx.LineEdit(title='south shading', text='{}'.format(tuple(self.root.south_shading_tuple)))
            self.north_shading = flx.LineEdit(title='north shading', text='{}'.format(self.root.north_shading_tuple))
            self.infiltration_airchange = flx.LineEdit(title='infiltration airchange', text='{}'.format(self.root.infiltration_airchange_tuple))
            flx.Widget(flex=1)

    @flx.reaction('exterior_wall.text')
    def change_exterior_wall(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.exterior_wall.text.split(',')))
        self.root.set_exterior_wall_tuple(t)
        print(self.root.exterior_wall_tuple)

    @flx.reaction('exterior_roof.text')
    def change_exterior_roof(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.exterior_roof.text.split(',')))
        self.root.set_exterior_roof_tuple(t)
        print(self.root.exterior_roof_tuple)

    @flx.reaction('exterior_window.text')
    def change_exterior_window(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.exterior_window.text.split(',')))
        self.root.set_exterior_window_tuple(t)
        print(self.root.exterior_window_tuple)

    @flx.reaction('eastrate.text')
    def change_eastrate(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.eastrate.text.split(',')))
        self.root.set_eastrate_tuple(t)
        print(self.root.eastrate_tuple)

    @flx.reaction('westrate.text')
    def change_westrate(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.westrate.text.split(',')))
        self.root.set_westrate_tuple(t)
        print(self.root.westrate_tuple)

    @flx.reaction('southrate.text')
    def change_southrate(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.southrate.text.split(',')))
        self.root.set_southrate_tuple(t)
        print(self.root.sourthrate)

    @flx.reaction('northrate.text')
    def change_northrate(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.northrate.text.split(',')))
        self.root.set_northrate_tuple(t)
        print(self.root.northrate_tuple)

    @flx.reaction('direction.text')
    def change_direction(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.direction.text.split(',')))
        self.root.set_direction_tuple(t)
        print(self.root.direction_tuple)

    @flx.reaction('airchange.text')
    def change_airchange(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.airchange.text.split(',')))
        self.root.set_airchange_tuple(t)
        print(self.root.airchange_tuple)

    @flx.reaction('cop.text')
    def change_cop(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.cop.text.split(',')))
        self.root.set_cop_tuple(t)
        print(self.root.cop_tuple)

    @flx.reaction('east_shading.text')
    def change_east_shading(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.east_shading.text.split(',')))
        self.root.set_east_shading_tuple(t)
        print(self.root.east_shading_tuple)

    @flx.reaction('west_shading.text')
    def change_west_shading(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.west_shading.text.split(',')))
        self.root.set_west_shading_tuple(t)
        print(self.root.west_shading_tuple)

    @flx.reaction('south_shading.text')
    def change_south_shading(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.south_shading.text.split(',')))
        self.root.set_south_shading_tuple(t)
        print(self.root.south_shading_tuple)

    @flx.reaction('north_shading.text')
    def change_north_shading(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.north_shading.text.split(',')))
        self.root.set_north_shading_tuple(t)
        print(self.root.north_shading_tuple)

    @flx.reaction('infiltration_airchange.text')
    def change_infiltration_airchange(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.infiltration_airchange.text.split(',')))
        self.root.set_infiltration_airchange_tuple(t)
        print(self.root.infiltration_airchange_tuple)


class AlgoParamWidget(flx.GroupWidget):

    def init(self):
        self.set_title("ALGORITHM PARAMETERS")
        with flx.FormLayout() as self.algo_params_model:
            self.mutation_param = flx.LineEdit(title='Mutation Parameter', text='{}'.format(int(self.root.mutation_param_int)))
            self.num_of_generation = flx.LineEdit(title='Num of genertion', text='{}'.format(int(self.root.num_of_generation_int)))
            self.num_of_individual = flx.LineEdit(title='Num of individual', text='{}'.format(int(self.root.num_of_individual_int)))
            self.num_of_tour_particps = flx.LineEdit(title='Num of tournament participents', text='{}'.format(int(self.root.num_of_tour_particps_int)))
            self.max_proc = flx.LineEdit(title='max process in parallel', text='{}'.format(int(self.root.max_proc_int)))

    @flx.reaction('mutation_param.text')
    def change_mutation_param(self, *events):
        i = int(self.mutation_param.text.strip())
        self.root.set_mutation_param_int(i)

    @flx.reaction('num_of_generation.text')
    def change_num_of_generation(self, *events):
        i = int(self.num_of_generation.text.strip())
        self.root.set_num_of_generation_int(i)

    @flx.reaction('num_of_individual.text')
    def change_num_of_individual(self, *events):
        i = int(self.num_of_individual.text.strip())
        self.root.set_num_of_individual_int(i)

    @flx.reaction('num_of_tour_particps.text')
    def change_num_of_tour_particps(self, *events):
        i = int(self.num_of_tour_particps.text.strip())
        self.root.set_num_of_tour_particps_int(i)

    @flx.reaction('max_proc.text')
    def change_max_proc(self, *events):
        i = int(self.max_proc.text.strip())
        self.root.set_max_proc_int(i)


class ConstantsParamWidget(flx.GroupWidget):

    def init(self):
        self.set_title("CONSTANTS")
        with flx.FormLayout(flex=1) as self.other_constants_model:
            self.floor_height = flx.LineEdit(title='Floor Height', text='{}'.format(int(self.root.floor_height_float)))
            self.window_height = flx.LineEdit(title='Window Height', text='{}'.format(int(self.root.window_height_float)))
            self.window_edge_height = flx.LineEdit(title='Window edge height', text='{}'.format(int(self.root.window_edge_height_float)))
            self.heating_setpoint = flx.LineEdit(title='Heating setpoint', text='{}'.format(int(self.root.heating_setpoint_float)))
            self.cooling_setpoint = flx.LineEdit(title='Cooling setpoint', text='{}'.format(int(self.root.cooling_setpoint_float)))

    @flx.reaction('floor_height.text')
    def change_floor_height(self, *events):
        i = float(self.floor_height.text.strip())
        self.root.set_floor_height_float(i)

    @flx.reaction('window_height.text')
    def change_window_height(self, *events):
        i = float(self.window_height.text.strip())
        self.root.set_window_height_float(i)

    @flx.reaction('window_edge_height.text')
    def change_window_edge_height(self, *events):
        i = float(self.window_edge_height.text.strip())
        self.root.set_window_edge_height_float(i)

    @flx.reaction('heating_setpoint.text')
    def change_heating_setpoint(self, *events):
        i = float(self.heating_setpoint.text.strip())
        self.root.set_heating_setpoint_float(i)

    @flx.reaction('cooling_setpoint.text')
    def change_cooling_setpoint(self, *events):
        i = float(self.cooling_setpoint.text.strip())
        self.root.set_cooling_setpoint_float(i)


class PathsParamWidget(flx.GroupWidget):
    def init(self):
        self.set_title("PATHS")
        with flx.FormLayout() as self.path_constants_model:
            self.weather_file = flx.LineEdit(title='Weather File', text='{}'.format(self.root.weather_file_str))
            self.idf_file = flx.LineEdit(title='Idf file', text='{}'.format(self.root.idf_file_str))
            self.output_path = flx.LineEdit(title='Output directory', text='{}'.format(self.root.output_path_str))

    @flx.reaction('weather_file.text')
    def change_weather_file(self, *events):
        s = self.weather_file.text.strip()
        self.root.set_weather_file_str(s)

    @flx.reaction('idf_file.text')
    def change_idf_file(self, *events):
        s = self.idf_file.text.strip()
        self.root.set_idf_file_str(s)

    @flx.reaction('output_path.text')
    def change_output_path(self, *events):
        s = self.output_path.text.strip()
        self.root.set_output_path_str(s)


class MooWidget(flx.Widget):
    CSS = """
    .flx-Button {
        background: #9d9;
    }
    .flx-LineEdit {
        border: 2px solid #9d9;
    }
    """

    def init(self, py):
        self.py = py
        print(self.py)

        with flx.HFix(flex=3):
            with flx.VBox(title='leftside'):
                # Model para
                self.model_params = ModelParametersWidget(minsize=(300, 500), maxsize=(300, 500))
                with flx.HBox():
                    self.run_button = flx.Button(text='RUN', flex=1)
                    self.stop_button = flx.Button(text='STOP', flex=1)
            flx.Widget(flex=1, maxsize=(20, 1000))
            with flx.VBox(title='rightside'):
                # algo param widget
                self.algo_params = AlgoParamWidget(minsize=(200, 200))

                # constants
                self.constant_params = ConstantsParamWidget(minsize=(120, 200))
                # paths
                self.path_params = PathsParamWidget(minsize=(120, 120))

    @flx.reaction('run_button.pointer_click')
    def run_button_onclick(self, *events):
        print("ONCLICK!")
        self.py.run_moo()

    @flx.reaction('stop_button.pointer_click')
    def stop_button_onclick(self, *events):
        print("Stop the program.........")
        self.py.stop()


class Run(flx.PyWidget):
    exterior_wall_tuple = flx.TupleProp((1, 10), settable=True)
    exterior_roof_tuple = flx.TupleProp((1, 9), settable=True)
    exterior_window_tuple = flx.TupleProp((1, 3), settable=True)
    eastrate_tuple = flx.TupleProp((0.05, 0.3), settable=True)
    westrate_tuple = flx.TupleProp((0.05, 0.3), settable=True)
    southrate_tuple = flx.TupleProp((0.05, 0.3), settable=True)
    northrate_tuple = flx.TupleProp((0.05, 0.3), settable=True)
    direction_tuple = flx.TupleProp((0, 359), settable=True)
    airchange_tuple = flx.TupleProp((0, 39), settable=True)
    cop_tuple = flx.TupleProp((2.0, 2.5), settable=True)
    east_shading_tuple = flx.TupleProp((0, 1), settable=True)
    west_shading_tuple = flx.TupleProp((0, 1), settable=True)
    south_shading_tuple = flx.TupleProp((0, 1), settable=True)
    north_shading_tuple = flx.TupleProp((0, 1), settable=True)
    infiltration_airchange_tuple = flx.TupleProp((0.3, 1.0), settable=True)

    mutation_param_int = flx.IntProp(4, settable=True)
    num_of_generation_int = flx.IntProp(50, settable=True)
    num_of_individual_int = flx.IntProp(50, settable=True)
    num_of_tour_particps_int = flx.IntProp(2, settable=True)
    max_proc_int = flx.IntProp(8, settable=True)

    floor_height_float = flx.FloatProp(2.8, settable=True)
    window_height_float = flx.FloatProp(1.5, settable=True)
    window_edge_height_float = flx.FloatProp(1, settable=True)
    heating_setpoint_float = flx.FloatProp(18, settable=True)
    cooling_setpoint_float = flx.FloatProp(26, settable=True)

    weather_file_str = flx.StringProp('../WeatherData/CHN_Chongqing.Chongqing.Shapingba.575160_CSWD.epw', settable=True)
    idf_file_str = flx.StringProp('./wkx2132+surface+20190618+second+3.idf', settable=True)
    output_path_str = flx.StringProp('temp/', settable=True)

    def init(self):
        self.moo = MooWidget(self)

    @flx.action
    def run_moo(self):
        paras = [
            discrete_interval(tuple(self.moo.root.exterior_wall_tuple)),
            discrete_interval(tuple(self.moo.root.exterior_roof_tuple)),
            discrete_interval(tuple(self.moo.root.exterior_window_tuple)),
            tuple(self.moo.root.eastrate_tuple),
            tuple(self.moo.root.westrate_tuple),
            tuple(self.moo.root.southrate_tuple),
            tuple(self.moo.root.northrate_tuple),
            tuple(self.moo.root.direction_tuple),
            tuple(self.moo.root.airchange_tuple),
            tuple(self.moo.root.cop_tuple),
            discrete_interval(tuple(self.moo.root.east_shading_tuple)),
            discrete_interval(tuple(self.moo.root.west_shading_tuple)),
            discrete_interval(tuple(self.moo.root.south_shading_tuple)),
            discrete_interval(tuple(self.moo.root.north_shading_tuple)),
            discrete_interval(scale_interval(tuple(self.moo.root.infiltration_airchange_tuple), 10))
        ]

        """Algorithm parameter"""
        hyperparameter: Dict = {
            "MUTATION_PARAM": int(self.moo.root.mutation_param_int),
            "NUM_OF_GENERATIONS": int(self.moo.root.num_of_generation_int),
            "NUM_OF_INDIVIDUALS": int(self.moo.root.num_of_individual_int),
            "NUM_OF_TOUR_PARTICIPS": int(self.moo.root.num_of_tour_particps_int),
            "CONCURRENCY": True,
            "MAX_PROC": int(self.moo.root.max_proc_int)
        }

        """other constants"""
        constants: Dict = {
            "FLOOR_HEIGHT": float(self.moo.root.floor_height_float),
            "WINDOW_HEIGHT": float(self.moo.root.window_height_float),
            "WINDOW_EDG_HEIGHT": float(self.moo.root.window_edge_height_float),
            "HEATING_SETPOINT": float(self.moo.root.heating_setpoint_float),
            "COOLING_SETPOINT": float(self.moo.root.cooling_setpoint_float)
        }

        """path constants"""
        paths: Dict = {
            "WEATHER_FILE": str(self.moo.root.weather_file_str),
            "IDF_FILE": str(self.moo.root.idf_file_str),
            "OUTPUT_PATH": str(self.moo.root.output_path_str)
        }

        __import__('pprint').pprint(paras)
        __import__('pprint').pprint(hyperparameter)
        __import__('pprint').pprint(constants)
        __import__('pprint').pprint(paths)

        moo_run(paras, hyperparameter, constants, paths)

    @flx.action
    def stop(self):
        sys.exit(0)


def moo_run(paras, hyperparameter, constants, paths):
    """The main entrance of the optimizer."""
    init()

    problem = Problem(num_of_variables=len(paras), objectives=[f1, f2, f3],
                      variables_range=paras,
                      preamble=Wkx2132Preamble(constants=constants, paths=paths))

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

    print("<Finished in {}, your patient is impressive, Congrads! Author: Jimmy Yao; From github.com/jummy233/epMOO>".format(time.ctime()))


if __name__ == "__main__":
    app = flx.App(Run)
    app.launch('app')
    flx.run()
