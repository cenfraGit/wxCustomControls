import os
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)


import wx
from src.functions.dip import dip
from src.controlConfig import ControlConfig
from src import CustomButton
from src import CustomCheckBox
from src import CustomScrolledWindow
from src import CustomStaticBox
from src import CustomPanel

class PreviewFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.SetTitle("Custom Controls Preview")


        # ------------------- configs ------------------- #

        panelConfig = ControlConfig(border_width=1,
                                    border_colour=(150, 150, 150),
                                    bg_colour=(255, 255, 255),
                                    corner_radius=5)


        # --------------- scrolled window --------------- #


        a = CustomScrolledWindow(parent=self, scrollbar_type="rectangular")
        panel = a.GetPanel()
        panelSizer = wx.GridBagSizer()
        panel.SetSizer(panelSizer)
        

        # ---------------- buttons panel ---------------- #

        buttonsText = "Button Text"
        image = wx.Image(os.path.join("images", "t.png"))
        image_size = dip(50, 50)

        p1 = CustomPanel(panel, config=panelConfig)
        p1_sizer = wx.GridBagSizer(hgap=dip(4), vgap=dip(4))
        p1.SetSizer(p1_sizer)
        
        b1 = CustomButton(parent=p1, label=buttonsText)
        b2 = CustomButton(parent=p1, label=buttonsText, corner_radius=dip(10))
        b3 = CustomButton(parent=p1, label=buttonsText,
                          bg_colour=(255, 255, 255), border_width=2,
                          border_colour=(0, 140, 0), font_face_name="Times New Roman")
        b4 = CustomButton(parent=p1, label=buttonsText, corner_radius=dip(4),
                          bg_linear_gradient=(0, 40, 7, 100, (150, 0, 0), (0, 0, 150)),
                          text_foreground_colour=(255, 255, 255))
        b5 = CustomButton(parent=p1, label=buttonsText,
                          image_default=image, image_default_size=image_size)
        b6 = CustomButton(parent=p1, label=buttonsText,
                          image_default=image, image_default_size=image_size,
                          corner_radius=5, bg_colour=(150, 0, 0), border_colour=(0, 0, 0),
                          border_width=2, text_side="left", font_size=16)
        b7 = CustomButton(parent=p1, label=buttonsText,
                          image_default=image, image_default_size=image_size, text_side="up",
                          bg_linear_gradient=(0, 40, 0, 100, (255, 255, 255), (130, 130, 130)),
                          text_foreground_colour=(130, 130, 130))
        b8 = CustomButton(parent=p1, label=buttonsText,
                          image_default=image, image_default_size=image_size, text_side="down",
                          bg_colour=(0, 0, 130), text_foreground_colour=(200, 200, 200))
        p1_sizer.Add(b1, pos=(0, 0), flag=wx.EXPAND|wx.TOP|wx.LEFT, border=dip(15))
        p1_sizer.Add(b2, pos=(0, 1), flag=wx.EXPAND|wx.TOP, border=dip(15))
        p1_sizer.Add(b3, pos=(0, 2), flag=wx.EXPAND|wx.TOP, border=dip(15))
        p1_sizer.Add(b4, pos=(0, 3), flag=wx.EXPAND|wx.TOP|wx.RIGHT, border=dip(15))
        p1_sizer.Add(b5, pos=(1, 0), flag=wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, border=dip(15))
        p1_sizer.Add(b6, pos=(1, 1), flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=dip(15))
        p1_sizer.Add(b7, pos=(1, 2), flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=dip(15))
        p1_sizer.Add(b8, pos=(1, 3), flag=wx.EXPAND|wx.TOP|wx.BOTTOM|wx.RIGHT, border=dip(15))

        p1_sizer.AddGrowableCol(0, 1)
        p1_sizer.AddGrowableCol(1, 1)
        p1_sizer.AddGrowableCol(2, 1)
        p1_sizer.AddGrowableCol(3, 1)
        
        p1_sizer.Layout()
        panelSizer.Add(p1, pos=(0, 0), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=dip(10))

        # ----------- custom static text panel ----------- #

        p2 = CustomPanel(panel, config=panelConfig)
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

        p3 = CustomPanel(panel, config=panelConfig)
        p3_sizer = wx.GridBagSizer(hgap=dip(4), vgap=dip(4))
        p3.SetSizer(p3_sizer)
        p3_sizer.Add(CustomCheckBox(p3, label="Placeholder"), pos=(0, 0), flag=wx.ALL|wx.EXPAND, border=dip(15))
        p3_sizer.AddGrowableCol(0, 1)
        p3_sizer.Layout()
        
        panelSizer.Add(p3, pos=(2, 0), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=dip(10))
        
        
        panelSizer.AddGrowableCol(0, 1)
        panelSizer.Layout()
        

        
        


app = wx.App()
f = PreviewFrame(parent=None)
f.Show()
app.MainLoop()
