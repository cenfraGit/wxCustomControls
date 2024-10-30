# CustomButton.py
# wxCustomControls
# A customizable button.
# 29/oct/2024


import wx
from ._CustomControl import CustomControl
from .utils.dip import dip
from .functions.getConfig import getConfig
from .functions.getPenBrush import getPen, getBrush


class CustomButton(CustomControl):
    def __init__(self, parent, id=wx.ID_ANY, label=wx.EmptyString,
                 pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.NO_BORDER,
                 validator=wx.DefaultValidator, name=wx.ControlNameStr,
                 config=None, **kwargs):

        # ---------------- control attributes ---------------- #

        self.__Label = label

        # ------------------- init control ------------------- #

        super().__init__(parent, id, pos, size, style, validator, name, config, **kwargs)

        # ---------------------- events ---------------------- #

        self.Bind(wx.EVT_PAINT, self.__OnPaint)
        self.Bind(wx.EVT_LEFT_DCLICK, self.__OnLeftDown)
        self.Bind(wx.EVT_LEFT_DOWN, self.__OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.__OnLeftUp)


    def SetLabel(self, label:str):
        self.__Label = label
        self.Refresh()


    def GetLabel(self):
        return self.__Label


    def __OnPaint(self, event):

        # --------------------- contexts --------------------- #

        dc = wx.BufferedPaintDC(self)
        gcdc = wx.GCDC(dc)
        gc:wx.GraphicsContext = gcdc.GetGraphicsContext()
        gcdc.Clear()

        # ---------------- drawing properties ---------------- #
        # get drawing properties depending on state

        state_properties = None

        # ---------------------- cursor ---------------------- #

        # self.SetCursor()

        # ------------ drawing area and background ------------ #

        controlRect:wx.Rect = self.GetClientRect() # control area

        # control background
        gcdc.SetPen(wx.TRANSPARENT_PEN)
        gcdc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour()))
        gcdc.DrawRectangle(controlRect)

        # ----------------- button rectangle ----------------- #


        # ------------------ text dimensions ------------------ #


        # ----------------------- image ----------------------- #


        # -------------------- text label -------------------- #
        
        


    def __OnLeftDown(self, event):
        pass


    def __OnLeftUp(self, event):
        pass




