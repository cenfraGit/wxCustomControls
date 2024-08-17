import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

import wx
from src.functions.dip import dip
from src.controlConfig import ControlConfig
from src import CustomButton
from src import CustomCheckBox
from src import CustomScrolledWindow
from src import RoundedPanel
from src import CustomStaticBox

class PreviewFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.SetTitle("Custom Controls Preview")
        #self.SetMinClientSize(dip(300, 300))


        a = CustomScrolledWindow(parent=self)
        panel = a.GetPanel()
        panelSizer = wx.GridBagSizer()
        panel.SetSizer(panelSizer)
        

        # ---------------- buttons panel ---------------- #

        p1 = RoundedPanel(panel, border_colour=(150, 150, 150))
        p1_sizer = wx.GridBagSizer(hgap=dip(4), vgap=dip(4))
        p1.SetSizer(p1_sizer)
        p1_sizer.Add(CustomButton(parent=p1, label="Placeholder Text"), pos=(0, 0), flag=wx.TOP|wx.LEFT, border=dip(15))
        p1_sizer.Add(CustomButton(parent=p1, label="Placeholder Text"), pos=(1, 0), flag=wx.TOP|wx.LEFT, border=dip(15))
        p1_sizer.Layout()
        
        panelSizer.Add(p1, pos=(0, 0), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=dip(10))

        # ----------- custom static text panel ----------- #

        p2 = RoundedPanel(panel, border_colour=(150, 150, 150))
        p2_sizer = wx.GridBagSizer(hgap=dip(4), vgap=dip(4))
        p2.SetSizer(p2_sizer)
        staticbox = CustomStaticBox(p2, label="placeholder")
        staticboxPanel = staticbox.GetPanel()
        CustomButton(staticboxPanel, label='test')
        
        p2_sizer.Add(staticbox, pos=(0, 0), flag=wx.ALL|wx.EXPAND, border=dip(15))
        p2_sizer.AddGrowableCol(0, 1)
        p2_sizer.Layout()
        
        panelSizer.Add(p2, pos=(1, 0), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=dip(10))


        # -------------- custom check boxes -------------- #

        p3 = RoundedPanel(panel, border_colour=(150, 150, 150))
        p3_sizer = wx.GridBagSizer(hgap=dip(4), vgap=dip(4))
        p3.SetSizer(p3_sizer)
        p3_sizer.Add(CustomCheckBox(p3, label="Placeholder"), pos=(0, 0), flag=wx.ALL|wx.EXPAND, border=dip(15))
        p3_sizer.AddGrowableCol(0, 1)
        p3_sizer.Layout()
        
        panelSizer.Add(p3, pos=(2, 0), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=dip(10))
        





        

        
        panelSizer.AddGrowableCol(0, 1)
        panelSizer.Layout()
        

        """
        for i in range(30):
            #panelSizer.Add(wx.Button(parent=panel, label="testing"), pos=(i, i), flag=wx.ALIGN_CENTER|wx.EXPAND)
            panelSizer.Add(CustomButton(parent=panel,
                                        label="testing",
                                        corner_radius=3,
                                        border_width_hover=1), pos=(i, i), flag=wx.ALIGN_CENTER|wx.EXPAND)
        panelSizer.AddGrowableCol(0, 1)
        panel.SetSizer(panelSizer)
        """
        

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
