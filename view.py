import wx

"""
the GUI is MVC structure.
"""


class OptimizerWindow(wx.Frame):
    """
    The main window for this application.
    """
    def __init__(self, parent, title):
        super().__init__(parent=parent, title=title, size=(850, 700))
        # create panels.
        title_panel = TitlePanel(self)
        loc_panel = LocPanel(self)
        target_para_panel = TargetParaPanel(self)
        algo_para_panel = AlgoParaPanel(self)
        func_para_panel = FuncParaPanel(self)

        # organize panels with Sizers.
        top_sizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer.Add(title_panel, 0, wx.EXPAND | wx.ALL, 3)
        top_sizer.Add(loc_panel, 0, wx.EXPAND | wx.ALL, 3)
        top_sizer.Add(target_para_panel, 1, wx.EXPAND | wx.ALL, 3)
        top_sizer.Add(algo_para_panel, 1, wx.EXPAND | wx.ALL, 3)
        top_sizer.Add(func_para_panel, 1, wx.EXPAND | wx.ALL, 3)

        # done
        self.SetSizer(top_sizer)
        self.Centre()
        self.Show()


class TitlePanel(wx.Panel):
    """
    Panel for holding the title.
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        # Assetes.
        font_big = wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL)

        # Title
        title_txt = wx.StaticText(
            self, 1, "Optimizer", style=wx.ALIGN_CENTRE, size=(30, 30),
            pos=(300, 0))
        title_txt.SetFont(font_big)


class LocPanel(wx.Panel):
    """
    Panel for inputing location.
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        font = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL)

        # title label.
        label = wx.StaticText(self, -1, "Location", size=(50, 40), pos=(0, 5))
        label.SetFont(font)
        # loc_entry = wx.TextCtrl(self, -1, "", style=wx.TE_LEFT, size=(500, 30), pos=(100, 4))

        select_button = wx.Button(self, label="Select", pos=(620, 0))
        select_button.Bind(wx.EVT_BUTTON, self.onSelect)

    def onSelect(self):
        pass


class TargetParaPanel(wx.Panel):
    """
    Panel for target parameters.
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        gbox = wx.FlexGridSizer(cols=8, hgap=2, vgap=8)
        vbox = wx.BoxSizer(wx.VERTICAL)

        font = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL)
        label = wx.StaticText(self, -1, "Parameter", size=(200, 30))
        label.SetFont(font)

        paras = [
                "outerwall", "roof", "window", "direction",
                "eastrate", "westrate", "southrate", "northrate",
                "airchanges"
                ]
        add_to_hbox = []

        # create (StaticText, TextCtrl) in pair.
        for n in paras:
            add_to_hbox.append((wx.StaticText(
                self, -1, n, size=(110, 30), style=wx.ALIGN_CENTER),
                0, wx.ALIGN_CENTER))

            add_to_hbox.append((wx.TextCtrl(
                self, -1, "", size=(80, 30)),
                0, wx.ALIGN_CENTER))

        gbox.AddMany(add_to_hbox)

        # form the box
        vbox.Add(label, 0, wx.ALIGN_LEFT)
        vbox.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(gbox, 0, wx.ALIGN_LEFT)

        self.SetSizer(vbox)


class AlgoParaPanel(wx.Panel):
    """
    Panel for algorithm parameters.
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        gbox = wx.FlexGridSizer(cols=8, hgap=2, vgap=8)
        vbox = wx.BoxSizer(wx.VERTICAL)

        font = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL)
        label = wx.StaticText(self, -1, "Algorithm Parameter", size=(200, 30))
        label.SetFont(font)

        paras = ["nPop", "MaxIt", "gGap", "pCrossover", "pMutation"]
        add_to_hbox = []

        # create (StaticText, TextCtrl) in pair.
        for n in paras:
            add_to_hbox.append((wx.StaticText(
                self, -1, n, size=(110, 30), style=wx.ALIGN_CENTER),
                0, wx.ALIGN_CENTER))

            add_to_hbox.append((wx.TextCtrl(
                self, -1, "", size=(80, 30)),
                0, wx.ALIGN_CENTER))

        gbox.AddMany(add_to_hbox)

        vbox.Add(label, 0, wx.ALIGN_LEFT)
        vbox.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(gbox, 0, wx.ALIGN_LEFT)

        self.SetSizer(vbox)


class FuncParaPanel(wx.Panel):
    """
    Panel for algorithm parameters.
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        gbox = wx.FlexGridSizer(cols=8, hgap=2, vgap=8)
        vbox = wx.BoxSizer(wx.VERTICAL)

        font = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL)

        label = wx.StaticText(self, -1, "Function Parameter", size=(200, 30))
        label.SetFont(font)

        paras = ["layerHeight", "winHeight", "winEdgeHeight", "EER", "COP",
                 "SumberLambda", "WinterLambda"]
        add_to_hbox = []

        # create StaticText and TextCtrl in pair.
        for n in paras:
            add_to_hbox.append((wx.StaticText(
                self, -1, n, size=(110, 30), style=wx.ALIGN_CENTER),
                0, wx.ALIGN_CENTER))

            add_to_hbox.append((wx.TextCtrl(  # note it is a tuple.
                self, -1, "", size=(80, 30)),
                0, wx.ALIGN_CENTER))

        run_button = wx.Button(
            self, 0, "Run", pos=(650, 150))
        run_button.Bind(wx.EVT_BUTTON, self.onRun)

        gbox.AddMany(add_to_hbox)
        vbox.Add(label, 0, wx.ALIGN_LEFT)
        vbox.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(gbox, 0, wx.ALIGN_LEFT)

        self.SetSizer(vbox)

    def onRun(self):
        pass


if __name__ == "__main__":
    app = wx.App(False)
    frame = OptimizerWindow(None, "Optimizer")
    app.MainLoop()
