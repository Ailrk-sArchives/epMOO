from flexx import flx


class ModelParametersWidget(flx.GroupWidget):
    def init(self):
        self.set_title("MODEL PARAMTERS")
        with flx.FormLayout() as self.model_params_form:
            flx.Widget(flex=1)
            self.exterior_wall = flx.LineEdit(title='Exterior Wall', text='1, 10')
            self.exterior_roof = flx.LineEdit(title='Exterior Roof', text='1, 9')
            self.exterior_window = flx.LineEdit(title='Exterior Window', text='1, 3')
            self.eastrate = flx.LineEdit(title='East winwall ratio', text='0.05, 0.3')
            self.westrate = flx.LineEdit(title='West winwall ratio', text='0.05, 0.3')
            self.southrate = flx.LineEdit(title='South winwall ratio', text='0.05, 0.3')
            self.northrate = flx.LineEdit(title='North winwall ratio', text='0.05, 0.3')
            self.direction = flx.LineEdit(title='direction(deg)', text='0, 359')
            self.airchange = flx.LineEdit(title='airchange', text='0, 39')
            self.cop = flx.LineEdit(title='cop', text='2.0, 3.5')
            self.east_shading = flx.LineEdit(title='east shading', text='0, 1')
            self.west_shading = flx.LineEdit(title='west shading', text='0, 1')
            self.south_shading = flx.LineEdit(title='south shading', text='0, 1')
            self.north_shading = flx.LineEdit(title='north shading', text='0, 1')
            flx.Widget(flex=1)


class ControlPanelWidget(flx.GroupWidget):
    def init(self):
        self.set_title("CONTROL PANEL")
        self.run_button = flx.Button(text='Run')


class AlgoParamWidget(flx.GroupWidget):
    def init(self):
        self.set_title("ALGORITHM PARAMETERS")
        with flx.FormLayout() as self.algo_params_model:
            self.mutation_param = flx.LineEdit(title='Mutation Parameter', text='3')
            self.num_of_generation = flx.LineEdit(title='Num of genertion', text='50')
            self.num_of_individual = flx.LineEdit(title='Num of individual', text='50')
            self.num_of_tour_particps = flx.LineEdit(title='Num of tournament participents', text='1,10')
            self.max_proc = flx.LineEdit(title='max process in parallel', text='8')


class ConstantsParamWidget(flx.GroupWidget):
    def init(self):
        self.set_title("CONSTANTS")
        with flx.FormLayout(flex=1) as self.other_constants_model:
            self.floor_height = flx.LineEdit(title='Floor Height', text='2.8')
            self.window_height = flx.LineEdit(title='Window Height', text='1.5')
            self.window_edge_height = flx.LineEdit(title='Window edge height', text='1')


class PathsParamWidget(flx.GroupWidget):
    def init(self):
        self.set_title("PATHS")
        with flx.FormLayout() as self.path_constants_model:
            self.weather_file = flx.LineEdit(title='Weather File', text='./WeatherData/CHN_Chongqing.Chongqing.Sh  apingba.575160_CSWD.epw')
            self.idf_file = flx.LineEdit(title='Idf file', text='shading_model_6-0603-1.idf')
            self.output_path = flx.LineEdit(title='Output directory', text='temp/')


class MooWidget(flx.Widget):
    CSS = """
    .flx-Button {
        background: #9d9;
    }
    .flx-LineEdit {
        border: 2px solid #9d9;
    }
    """

    def init(self):
        with flx.HFix(flex=3):
            with flx.VBox(title='leftside'):
                # Model para
                ModelParametersWidget(minsize=(300, 470), maxsize=(300, 470))
                # Control panel
                ControlPanelWidget()
            flx.Widget(flex=1, maxsize=(20, 1000))
            with flx.VBox(title='rightside'):
                # algo param widget
                AlgoParamWidget(minsize=(200, 200))

                # constants
                ConstantsParamWidget(minsize=(120, 120))
                # paths
                PathsParamWidget(minsize=(120, 120))

if __name__ == "__main__":
    app = flx.launch(MooWidget, 'app')
    flx.run()
