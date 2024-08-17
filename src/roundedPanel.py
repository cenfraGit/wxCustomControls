import wx
from .functions.dip import dip
from .controlConfig import ControlConfig
from .functions.getPenBrush import getPen, getBrush
from copy import copy


class RoundedPanel(wx.Panel):
    """ A panel with rounded corners. """

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, name=wx.PanelNameStr, config=None,
                 **kwargs):
    
        super().__init__(parent=parent, id=id, pos=pos, size=size, style=style, name=name)

        # --------------- check for config --------------- #
        # if the user does not specify a config object, create
        # one and update with kwargs
        self.config:ControlConfig = copy(config) if config else self.__GetDefaultConfig()
        if kwargs:
            self.config.update(**kwargs)

        # ------------------ attributes ------------------ #

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        # -------------------- events -------------------- #

        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def __GetDefaultConfig(self) -> ControlConfig:
        return ControlConfig(
            # default colors
            bg_colour=(255, 255, 255),
            border_colour=(0, 0, 0),
            border_width=1,
            corner_radius=5
        )
    

    def UpdateConfig(self, **kwargs):
        self.config.update(**kwargs)
        self.Refresh()


    def GetConfig(self):
        return self.config


    def SetBackgroundColour(self, colour:wx.Colour):
        self.config.bg_colour = (colour.GetRed(), colour.GetGreen(), colour.GetBlue())
        self.Refresh()


    def GetBackgroundColour(self): 
        return wx.Colour(*self.config.bg_colour)


    def SetBorderColour(self, colour:wx.Colour):
        self.config.border_colour = (colour.GetRed(), colour.GetGreen(), colour.GetBlue())
        self.Refresh()


    def SetBorderWidth(self, width:int):
        """Sets the width of the border. Set to 0 if you want no
        border."""
        # we will use a _BorderWidth of 0 to indicate that a
        # TRANSPARENT_PEN should be used when drawing
        self.config.border_width = width
        self.Refresh()


    def OnPaint(self, event):
        """ Handles the paint event. """

        # create device context
        dc = wx.AutoBufferedPaintDC(self)
        #dc.Clear()

        # create graphics context
        gc = wx.GraphicsContext.Create(dc)

        # get panel rectangle 
        rect = self.GetClientRect()
        
        # convert to values used by gc
        x, y = rect.GetX(), rect.GetY()
        width, height = rect.GetWidth(), rect.GetHeight()

        # draw the background (for the corners)
        gc.SetPen(wx.TRANSPARENT_PEN)
        gc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour()))
        gc.DrawRectangle(x, y, width, height)

        # --------------------- pen --------------------- #

        # if the border width is 0, we will simply not draw a border
        # by using a transparent pen.

        if not self.config.border_width:
            pen = wx.TRANSPARENT_PEN
        else:
            pen = getPen("default", self.config)

        gc.SetPen(pen)


        # -------------------- brush -------------------- #

        gc.SetBrush(getBrush("default", self.config, gc))

        # ------------ drawing the rectangle ------------ #

        # we will create a smaller rectangle in order for it to be
        # rendered correctly.
        panelRect = rect.Deflate(self.config.border_width,
                                 self.config.border_width)

        gc.DrawRoundedRectangle(panelRect.GetX(),
                                panelRect.GetY(),
                                panelRect.GetWidth(),
                                panelRect.GetHeight(),
                                radius=self.config.corner_radius)
