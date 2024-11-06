# CustomPanel.py
# wxCustomControls
# A panel that supports rounded corners, borders and gradient backgrounds.
# 28/oct/2024


import wx
from .utils.dip import dip
from .base._CustomObject import CustomObject


class CustomPanel(wx.Panel, CustomObject):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.NO_BORDER,
                 name=wx.PanelNameStr, config=None, **kwargs):

        # ---------------- init custom object ---------------- #
        
        super().__init__(parent, id, pos, size, style, name)
        CustomObject.__init__(self, config, **kwargs)
        
        # ----------------------- setup ----------------------- #
        
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        # ---------------------- events ---------------------- #
        
        self.Bind(wx.EVT_PAINT, self.__OnPaint)
        self.Bind(wx.EVT_SIZE, self.__OnSize)


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
        
        gcdc, gc = self._getDrawingContexts()

        # ------------ drawing area and background ------------ #
        
        controlRect = self.GetClientRect() # drawing area

        # drawing area background
        gcdc.SetPen(wx.TRANSPARENT_PEN)
        gcdc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour()))
        gcdc.DrawRectangle(controlRect)
        
        # ------------------- pen and brush ------------------- #

        # since its a panel, it will not have a control state
        # behavior. it has only a "default" state.
        drawing_properties = self._getStateDrawingProperties("default", gc)

        pen = drawing_properties["pen"]
        gcdc.SetPen(pen)        
        gc.SetBrush(drawing_properties["brush_background"])
        
        # ----------- drawing the panel's rectangle ----------- #

        panelRect = controlRect.Deflate(pen.GetWidth(),
                                        pen.GetWidth())
        
        gcdc.DrawRoundedRectangle(panelRect, radius=self._config.corner_radius_default)


    def __OnSize(self, event):
        self.Refresh()
        event.Skip()
        
