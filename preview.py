import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

import wx
from src.functions.dip import dip
from src.controlConfig import ControlConfig
from src import CustomButton
from src import CustomCheckBox
from src import CustomScrolledWindow

class PreviewFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.SetTitle("Custom Controls Preview")
        self.SetMinClientSize(dip(300, 300))


        a = CustomScrolledWindow(parent=self)
        panel = a.GetPanel()
        #panel.SetBackgroundColour(wx.GREEN)
        panelSizer = wx.GridBagSizer()
        for i in range(30):
            #panelSizer.Add(wx.Button(parent=panel, label="testing"), pos=(i, i), flag=wx.ALIGN_CENTER|wx.EXPAND)
            panelSizer.Add(CustomButton(parent=panel,
                                        label="testing",
                                        corner_radius=3,
                                        border_width_hover=1), pos=(i, i), flag=wx.ALIGN_CENTER|wx.EXPAND)
        panelSizer.AddGrowableCol(0, 1)
        panel.SetSizer(panelSizer)
        

        """
        panel = wx.Panel(self)


        config = ControlConfig(border_width=3,
                               border_colour=(0, 0, 0),
                               corner_radius=3,
                               corner_radius_hover=5,
                               corner_radius_pressed=10)


        
        a = CustomButton(parent=panel, label="Placeholder text", config=config, pos=(50, 50), font_size=20)
        a.Bind(wx.EVT_BUTTON, lambda e: print("button event"))

        b = CustomCheckBox(parent=panel, label="Placeholder text", config=config, pos=(50, 120),
                           textSide="right",
                           checkbox_width = 100,
                           font_size=33)

        """
        
        


app = wx.App()
f = PreviewFrame(parent=None)
f.Show()
app.MainLoop()
