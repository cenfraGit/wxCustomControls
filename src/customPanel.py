import wx
from .functions.dip import dip
from .controlConfig import ControlConfig
from .functions.getPenBrush import getPen, getBrush
from copy import copy


class CustomPanel(wx.Panel):
    """A panel that supports rounded corners, borders and gradient
    backgrounds."""

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, name=wx.PanelNameStr,
                 config=None, **kwargs):
    
        super().__init__(parent=parent, id=id, pos=pos, size=size,
                         style=style, name=name)

        # --------------- check for config --------------- #

        if config:
            self.config:ControlConfig = copy(config)
        else:
            self.config:ControlConfig = self.__GetDefaultConfig()

        if kwargs:
            self.config.update(**kwargs)
            

        # ------------------ appearance ------------------ #

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        

        # -------------------- events -------------------- #

        self.Bind(wx.EVT_PAINT, self.OnPaint)

        
    def __GetDefaultConfig(self) -> ControlConfig:
        return ControlConfig(
            bg_colour=(255, 255, 255),
            border_colour=(150, 150, 150),
            border_width=0,
            corner_radius=0)
    

    def UpdateConfig(self, **kwargs):
        self.config.update(**kwargs)
        self.Refresh()


    def GetConfig(self):
        return self.config


    def SetBackgroundColour(self, colour:wx.Colour):
        self.BackgroundColour = colour
        self.config.bg_colour = (colour.GetRed(),
                                 colour.GetGreen(),
                                 colour.GetBlue())
        self.Refresh()


    def GetBackgroundColour(self): 
        return wx.Colour(*self.config.bg_colour)


    def SetBorderColour(self, colour:wx.Colour):
        self.config.border_colour = (colour.GetRed(),
                                     colour.GetGreen(),
                                     colour.GetBlue())
        self.Refresh()


    def SetBorderWidth(self, width:int):
        self.config.border_width = width
        self.Refresh()


    def OnPaint(self, event):

        # --------------- create contexts --------------- #

        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()

        gc:wx.GraphicsContext = wx.GraphicsContext.Create(dc)

        
        # -------------- drawing rectangle -------------- #
        
        rect = self.GetClientRect()

        
        # ------------- background rectangle ------------- #
        
        gc.SetPen(wx.TRANSPARENT_PEN)
        gc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour()))
        
        gc.DrawRectangle(rect.GetX(),
                         rect.GetY(),
                         rect.GetWidth(),
                         rect.GetHeight())
        

        # --------------------- pen --------------------- #

        if self.config.border_width:
            pen = getPen("default", self.config)
        else:
            pen = wx.TRANSPARENT_PEN

        gc.SetPen(pen)

        
        # -------------------- brush -------------------- #

        gc.SetBrush(getBrush("default", self.config, gc))
        

        # ------------ drawing the rectangle ------------ #

        # deflate for correct border drawing
        panelRect = rect.Deflate(pen.GetWidth(),
                                 pen.GetWidth())

        gc.DrawRoundedRectangle(panelRect.GetX(),
                                panelRect.GetY(),
                                panelRect.GetWidth(),
                                panelRect.GetHeight(),
                                radius=self.config.corner_radius)
