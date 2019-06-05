from flexx import flx
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

from moo.utils import discrete_interval
from typing import Tuple


class Store(flx.JsComponent):
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

    weather_file_str = flx.StringProp('./WeatherData/CHN_Chongqing.Chongqing.Sh  apingba.575160_CSWD.epw', settable=True)
    idf_file_str = flx.StringProp('shading_model_6-0603-1.idf', settable=True)
    output_path_str = flx.StringProp('temp/', settable=True)


class ModelParametersWidget(flx.GroupWidget):

    def init(self):
        self.set_title("MODEL PARAMTERS")
        with flx.FormLayout() as self.model_params_form:
            flx.Widget(flex=1)
            self.exterior_wall = flx.LineEdit(title='Exterior Wall', text='{}'.format(tuple(self.root.store.exterior_wall_tuple)))
            self.exterior_roof = flx.LineEdit(title='Exterior Roof', text='{}'.format(tuple(self.root.store.exterior_roof_tuple)))
            self.exterior_window = flx.LineEdit(title='Exterior Window', text='{}'.format(tuple(self.root.store.exterior_window_tuple)))
            self.eastrate = flx.LineEdit(title='East winwall ratio', text='{}'.format(tuple(self.root.store.eastrate_tuple)))
            self.westrate = flx.LineEdit(title='West winwall ratio', text='{}'.format(tuple(self.root.store.westrate_tuple)))
            self.southrate = flx.LineEdit(title='South winwall ratio', text='{}'.format(tuple(self.root.store.southrate_tuple)))
            self.northrate = flx.LineEdit(title='North winwall ratio', text='{}'.format(tuple(self.root.store.northrate_tuple)))
            self.direction = flx.LineEdit(title='direction(deg)', text='{}'.format(tuple(self.root.store.direction_tuple)))
            self.airchange = flx.LineEdit(title='airchange', text='{}'.format(tuple(self.root.store.airchange_tuple)))
            self.cop = flx.LineEdit(title='cop', text='{}'.format(tuple(self.root.store.cop_tuple)))
            self.east_shading = flx.LineEdit(title='east shading', text='{}'.format(tuple(self.root.store.east_shading_tuple)))
            self.west_shading = flx.LineEdit(title='west shading', text='{}'.format(tuple(self.root.store.west_shading_tuple)))
            self.south_shading = flx.LineEdit(title='south shading', text='{}'.format(tuple(self.root.store.south_shading_tuple)))
            self.north_shading = flx.LineEdit(title='north shading', text='{}'.format(self.root.store.north_shading_tuple))
            self.infiltration_airchange = flx.LineEdit(title='infiltration airchange', text='{}'.format(self.root.store.infiltration_airchange_tuple))
            flx.Widget(flex=1)

    @flx.reaction('exterior_wall.text')
    def change_exterior_wall(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.exterior_wall.text.split(',')))
        self.root.store.set_exterior_wall_tuple(t)
        print(self.root.store.exterior_wall_tuple)

    @flx.reaction('exterior_roof.text')
    def change_exterior_roof(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.exterior_roof.text.split(',')))
        self.root.store.set_exterior_roof_tuple(t)
        print(self.root.store.exterior_roof_tuple)

    @flx.reaction('exterior_window.text')
    def change_exterior_window(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.exterior_window.text.split(',')))
        self.root.store.set_exterior_window_tuple(t)
        print(self.root.store.exterior_window_tuple)

    @flx.reaction('eastrate.text')
    def change_eastrate(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.exterior_wall.text.split(',')))
        self.root.store.set_eastrate_tuple(t)
        print(self.root.store.eastrate_tuple)

    @flx.reaction('westrate.text')
    def change_westrate(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.westrate.text.split(',')))
        self.root.store.set_westrate_tuple(t)
        print(self.root.store.westrate_tuple)

    @flx.reaction('southrate.text')
    def change_southrate(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.southrate.text.split(',')))
        self.root.store.set_southrate_tuple(t)
        print(self.root.store.sourthrate)

    @flx.reaction('northrate.text')
    def change_northrate(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.northrate.text.split(',')))
        self.root.store.set_northrate_tuple(t)

    @flx.reaction('direction.text')
    def change_direction(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.direction.text.split(',')))
        self.root.store.set_direction_tuple(t)

    @flx.reaction('airchange.text')
    def change_airchange(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.airchange.text.split(',')))

    @flx.reaction('cop.text')
    def change_cop(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.cop.text.split(',')))
        self.root.store.set_cop_tuple(t)

    @flx.reaction('east_shading.text')
    def change_east_shading(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.east_shading.text.split(',')))
        self.root.store.set_east_shading_tuple(t)

    @flx.reaction('west_shading.text')
    def change_west_shading(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.west_shading.text.split(',')))
        self.root.store.set_west_shading_tuple(t)

    @flx.reaction('south_shading.text')
    def change_south_shading(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.south_shading.text.split(',')))
        self.root.store.set_south_shading_tuple(t)

    @flx.reaction('north_shading.text')
    def change_north_shading(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.north_shading.text.split(',')))
        self.root.store.set_north_shading_tuple(t)

    @flx.reaction('infiltration_airchange.text')
    def change_infiltration_airchange(self, *events):
        t = tuple(map(lambda x: float(x.strip()), self.infiltration_airchange.text.split(',')))
        self.root.store.set_infiltration_airchange_tuple(t)


class AlgoParamWidget(flx.GroupWidget):

    def init(self):
        self.set_title("ALGORITHM PARAMETERS")
        with flx.FormLayout() as self.algo_params_model:
            self.mutation_param = flx.LineEdit(title='Mutation Parameter', text='3')
            self.num_of_generation = flx.LineEdit(title='Num of genertion', text='50')
            self.num_of_individual = flx.LineEdit(title='Num of individual', text='50')
            self.num_of_tour_particps = flx.LineEdit(title='Num of tournament participents', text='1,10')
            self.max_proc = flx.LineEdit(title='max process in parallel', text='8')

    @flx.reaction('mutation_param.text')
    def change_mutation_param(self, *events):
        i = int(self.mutation_param.text.strip())
        self.root.store.set_mutation_param_int(i)

    @flx.reaction('num_of_generation.text')
    def change_num_of_generation(self, *events):
        i = int(self.num_of_generation.text.strip())
        self.root.store.set_num_of_generation_int(i)

    @flx.reaction('num_of_individual.text')
    def change_num_of_individual(self, *events):
        i = int(self.num_of_individual.text.strip())
        self.root.store.set_num_of_individual_int(i)

    @flx.reaction('num_of_tour_particps.text')
    def change_num_of_tour_particps(self, *events):
        i = int(self.num_of_tour_particps.text.strip())
        self.root.store.set_num_of_tour_particps_int(i)

    @flx.reaction('max_proc.text')
    def change_max_proc(self, *events):
        i = int(self.max_proc.text.strip())
        self.root.store.set_max_proc_int(i)


class ConstantsParamWidget(flx.GroupWidget):

    def init(self):
        self.set_title("CONSTANTS")
        with flx.FormLayout(flex=1) as self.other_constants_model:
            self.floor_height = flx.LineEdit(title='Floor Height', text='2.8')
            self.window_height = flx.LineEdit(title='Window Height', text='1.5')
            self.window_edge_height = flx.LineEdit(title='Window edge height', text='1')
            self.heating_setpoint = flx.LineEdit(title='Heating setpoint', text='18')
            self.cooling_setpoint = flx.LineEdit(title='Cooling setpoint', text='26')

    @flx.reaction('floor_height.text')
    def change_floor_height(self, *events):
        i = float(self.floor_height.text.strip())
        self.root.store.set_floor_height_float(i)

    @flx.reaction('window_height.text')
    def change_window_height(self, *events):
        i = float(self.window_height.text.strip())
        self.root.store.set_window_height_float(i)

    @flx.reaction('window_edge_height.text')
    def change_window_edge_height(self, *events):
        i = float(self.window_edge_height.text.strip())
        self.root.store.set_window_edge_height_float(i)

    @flx.reaction('heating_setpoint.text')
    def change_heating_setpoint(self, *events):
        i = float(self.heating_setpoint.text.strip())
        self.root.store.set_heating_setpoint_float(i)

    @flx.reaction('cooling_setpoint.text')
    def change_cooling_setpoint(self, *events):
        i = float(self.cooling_setpoint.text.strip())
        self.root.store.set_cooling_setpoint_float(i)


class PathsParamWidget(flx.GroupWidget):
    def init(self):
        self.set_title("PATHS")
        with flx.FormLayout() as self.path_constants_model:
            self.weather_file = flx.LineEdit(title='Weather File', text='./WeatherData/CHN_Chongqing.Chongqing.Sh  apingba.575160_CSWD.epw')
            self.idf_file = flx.LineEdit(title='Idf file', text='shading_model_6-0603-1.idf')
            self.output_path = flx.LineEdit(title='Output directory', text='temp/')

    @flx.reaction('weather_file.text')
    def change_weather_file(self, *events):
        s = self.weather_file.text.strip()
        self.root.store.set_weather_file_str(s)

    @flx.reaction('idf_file.text')
    def change_idf_file(self, *events):
        s = self.idf_file.text.strip()
        self.root.store.set_idf_file_str(s)

    @flx.reaction('output_path.text')
    def change_output_path(self, *events):
        s = self.output_path.text.strip()
        self.root.store.set_output_path_str(s)


class MooWidget(flx.Widget):
    CSS = """
    .flx-Button {
        background: #9d9;
    }
    .flx-LineEdit {
        border: 2px solid #9d9;
    }
    """
    store = flx.ComponentProp()

    def init(self):
        self._mutate_store(Store())

        with flx.HFix(flex=3):
            with flx.VBox(title='leftside'):
                # Model para
                self.model_params = ModelParametersWidget(minsize=(300, 500), maxsize=(300, 500))
                self.run_button = flx.Button(text='RUN')
            flx.Widget(flex=1, maxsize=(20, 1000))
            with flx.VBox(title='rightside'):
                # algo param widget
                self.algo_params = AlgoParamWidget(minsize=(200, 200))

                # constants
                self.constant_params = ConstantsParamWidget(minsize=(120, 200))
                # paths
                self.path_params = PathsParamWidget(minsize=(120, 120))

    @flx.reaction('run_button.pointer_click')
    def run_moo(self):



class Run(flx.PyComponent):

    @flx.action
    def run_moo(self, store):
        paras = [
            discrete_interval(self.store.exterior_window_tuple),
            discrete_interval(self.store.exterior_roof_tuple),
            discrete_interval(self.store.exterior_window_tuple),
            self.store.eastrate_tuple,
            self.store.westrate_tuple,
            self.store.southrate_tuple,
            self.store.northrate_tuple,
            self.store.direction_tuple,
            self.store.airchange_tuple,
            self.store.cop_tuple,
            discrete_interval(self.store.east_shading_tuple),
            discrete_interval(self.store.west_shading_tuple),
            discrete_interval(self.store.south_shading_tuple),
            discrete_interval(self.store.north_shading_tuple),
            self.infiltration_airchange_tuple
        ]

        """Algorithm parameter"""
        hyperparameter: Dict = {
            "MUTATION_PARAM": self.store.mutation_param_int,
            "NUM_OF_GENERATIONS": self.store.num_of_generation_int,
            "NUM_OF_INDIVIDUALS": self.store.num_of_individual_int,
            "NUM_OF_TOUR_PARTICIPS": self.store.num_of_tour_particps_int,
            "CONCURRENCY": True,
            "MAX_PROC": self.store.max_proc_int
        }

        """other constants"""
        constants: Dict = {
            "FLOOR_HEIGHT": self.store.floor_height_float,
            "WINDOW_HEIGHT": self.store.window_height_float,
            "WINDOW_EDG_HEIGHT": self.store.window_edge_height_float,
            "HEATING_SETPOINT": self.store.heating_setpoint_float,
            "COOLING_SETPOINT": self.store.cooling_setpoint_float
        }

        """path constants"""
        paths: Dict = {
            "WEATHER_FILE": self.store.weather_file_str,
            "IDF_FILE": self.store.idf_file_str,
            "OUTPUT_PATH": self.store.output_path_str
        }

        moo(paras, hyperparameter, constants, paths)


def moo(paras, hyperparameter, constants, paths):
    """The main entrance of the optimizer."""

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

    print("<Finished, you are patient enough, Congradulation! Author: Jimmy Yao; From github.com/jummy233/epMOO>{}".format(time.ctime()))


if __name__ == "__main__":
    app = flx.launch(MooWidget, 'app')
    flx.run()
