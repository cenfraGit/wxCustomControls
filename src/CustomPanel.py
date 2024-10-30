# CustomPanel.py
# wxCustomControls
# A panel that supports rounded corners, borders and gradient backgrounds.
# 28/oct/2024


import wx
from .utils.dip import dip
from .functions.getConfig import getConfig
from .CustomConfig import CustomConfig
from .functions.getStateDrawingProperties import getStateDrawingProperties


class CustomPanel(wx.Panel):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.NO_BORDER,
                 name=wx.PanelNameStr, config=None, **kwargs):

        # -------------------- init panel -------------------- #

        super().__init__(parent, id, pos, size, style, name)

        # ----------------- check for config ----------------- #

        self._config = getConfig(config, self.__class__.__name__)
        self._config.Update(**kwargs)
        
        # ----------------------- setup ----------------------- #

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        # ---------------------- events ---------------------- #

        self.Bind(wx.EVT_PAINT, self.__OnPaint)
        self.Bind(wx.EVT_SIZE, self.__OnSize)
        

    def SetConfig(self, config:CustomConfig):
        self._config = config
        self.Refresh()


    def GetConfig(self):
        return self._config


    def UpdateConfig(self, **kwargs):
        self._config.Update(**kwargs)
        self.Refresh()


    def SetBackgroundColour(self, colour:wx.Colour):
        self.BackgroundColour = colour
        self._config.background_colour_default = (colour.GetRed(),
                                                  colour.GetGreen(),
                                                  colour.GetBlue())
        self.Refresh()


    def SetBorderColour(self, colour:wx.Colour):
        self._config.border_colour_default = (colour.GetRed(),
                                              colour.GetGreen(),
                                              colour.GetBlue())
        self.Refresh()


    def SetBorderWidth(self, width:int):
        self._config.border_width_default = width
        self.Refresh()


    def GetBackgroundColour(self):
        return wx.Colour(*self._config.background_colour_default)

    
    def __OnPaint(self, event):

        # --------------------- contexts --------------------- #

        dc = wx.BufferedPaintDC(self)
        gcdc = wx.GCDC(dc)
        gc = gcdc.GetGraphicsContext()
        gcdc.Clear()

        # ------------ drawing area and background ------------ #

        controlRect = self.GetClientRect() # drawing area

        # drawing area background
        gcdc.SetPen(wx.TRANSPARENT_PEN)
        gcdc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour()))
        gcdc.DrawRectangle(controlRect)
        
        # ------------------- pen and brush ------------------- #

        # since its a panel, it will not have a control state
        # behavior. it has only a "default" state.
        drawing_properties = getStateDrawingProperties("default", self._config, gc)

        pen = drawing_properties["pen"]
        gcdc.SetPen(pen)        
        gc.SetBrush(drawing_properties["brush"])
        
        # ----------- drawing the panel's rectangle ----------- #

        panelRect = controlRect.Deflate(pen.GetWidth(),
                                        pen.GetWidth())
        
        gcdc.DrawRoundedRectangle(panelRect, radius=self._config.corner_radius_default)


    def __OnSize(self, event):
        self.Refresh()
        event.Skip()
        

        
        
        

        


"""


from .utils.defaultConfig import GetDefaultConfig
from .utils.getStateProperties import getPen, getBrush

class CustomPanel(wx.Panel):


    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, name=wx.PanelNameStr,
                 config=None, **kwargs):
    
        super().__init__(parent=parent, id=id, pos=pos, size=size,
                         style=style, name=name)

        # ----------------- check for config ------------------- #

        # the config is copied to prevent it from changing if the reference is modified.
        self._config:CustomConfig = copy(config) if config else GetDefaultConfig("CustomPanel")
        if kwargs:
            self._config.Update(**kwargs)
            
        # ------------------ appearance ------------------ #

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        
        # -------------------- events -------------------- #

        self.Bind(wx.EVT_PAINT, self.__OnPaint)
        #self.Bind(wx.EVT_SIZE, self.__OnSize)
    

    def UpdateConfig(self, **kwargs):
        self._config.Update(**kwargs)
        self.Refresh()


    def GetConfig(self):
        return self._config


    def SetBackgroundColour(self, colour:wx.Colour):
        self.BackgroundColour = colour
        self._config.bg_colour_default = (colour.GetRed(),
                                 colour.GetGreen(),
                                 colour.GetBlue())
        self.Refresh()


    def GetBackgroundColour(self): 
        return wx.Colour(*self._config.bg_colour_default)


    def SetBorderColour(self, colour:wx.Colour):
        self._config.border_colour_default = (colour.GetRed(),
                                              colour.GetGreen(),
                                              colour.GetBlue())
        self.Refresh()


    def SetBorderWidth(self, width:int):
        self._config.border_width_default = width
        self.Refresh()


    def __OnPaint(self, event):

        # ---------------------- contexts ------------------------ #

        dc = wx.BufferedPaintDC(self)
        gc = wx.GCDC(dc)
        gc.Clear()

        # -------------------- drawing area and background ---------------------- #

        # drawing area
        controlRect = self.GetClientRect()

        # drawing area background
        gc.SetPen(wx.TRANSPARENT_PEN)
        gc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour()))
        gc.DrawRectangle(controlRect)
        
        # --------------------- pen --------------------- #

        if self._config.border_width_default:
            pen = getPen("default", self._config)
        else:
            pen = wx.TRANSPARENT_PEN

        gc.SetPen(pen)
        
        # -------------------- brush -------------------- #

        gc.SetBrush(getBrush("default", self._config, gc))
        
        # ------------ drawing the rectangle ------------ #

        # deflate for correct border drawing
        panelRect = controlRect.Deflate(pen.GetWidth(),
                                        pen.GetWidth())
        
        gc.DrawRoundedRectangle(panelRect, radius=self._config.corner_radius_default)


    def __OnSize(self, event):
        self.Refresh()
        event.Skip()

"""
