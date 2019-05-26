import wx
"""
The GUI for MOO.
"""


class OptimizerWindow(wx.Frame):
    """ The main window for this application"""
    def __init__(self, parent, title):
        super().__init__(parent=parent, title=title, size=(850, 700))
        title_panel = TitlePanel(self)


class HyperparameterPanel(wx.Panel):
    """ Panel for config hyperparameters of nsga2. """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        pass


class FeaturesPanel(wx.Panel):
    """ Panel for config the input parameter vector."""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        pass


class ControlPanel(wx.Panel):
    """ Panel to control the flow of the program."""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        pass


class ExtraParameters(wx.Panel):
    """ For extra constants."""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        pass


class ResultPanel(wx.Panel):
    """ To demonstrate the latest Result"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        pass

