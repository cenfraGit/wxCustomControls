# CustomStaticBox.py
# wxCustomControls
# A staticbox that supports rounded corners.
# 6/nov/2024


import wx
from .utils.dip import dip
from .base._CustomObject import CustomObject
from .CustomPanel import CustomPanel


class CustomStaticBox(wx.Panel, CustomObject):
    def __init__(self, parent, id=wx.ID_ANY, label=wx.EmptyString, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0,
                 name=wx.StaticBoxNameStr, config=None, **kwargs):

        # -------------------- attributes -------------------- #

        self._Label = label

        # ---------------- init custom object ---------------- #
        
        super().__init__(parent, id, pos, size, style, name)
        CustomObject.__init__(self, config, **kwargs)
        
        # ----------------------- setup ----------------------- #
        
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        # ------------------- content panel ------------------- #

        # get the text height to correctly offset the content panel
        # from the top.
        dc = wx.ScreenDC()
        dc.SetFont(wx.Font(self._config.text_font_size_default,
                           wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                           faceName=self._config.text_font_facename_default))
        _, self.textHeight = dc.GetTextExtent(self._Label)

        # create content panel
        #self.__Panel = wx.Panel(parent=self)
        self.__Panel = CustomPanel(self)
        self.__Panel.SetBackgroundColour(self.GetParent().GetBackgroundColour())
        self.__Panel.SetBackgroundColour(wx.YELLOW) # debug

        # create a sizer to ourselves and then add the panel with the correct paddings
        self.__Sizer = wx.BoxSizer(wx.VERTICAL)
        self.__Sizer.AddSpacer(self.textHeight)
        self.__Sizer.Add(self.__Panel, 
                         proportion=1,
                         flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,
                         border=self._config.padding_all_sides)
        self.SetSizer(self.__Sizer)

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

        # ---------------- staticbox rectangle ---------------- #

        paddingSides = self._config.border_width_default
        paddingTop = self.textHeight // 2

        gc.DrawRoundedRectangle(controlRect.GetX() + paddingSides,
                                controlRect.GetY() + paddingTop,
                                controlRect.GetWidth() - (2 * paddingSides),
                                controlRect.GetHeight() - paddingTop - paddingSides,
                                self._config.corner_radius_default)

        # -------------------- draw label -------------------- #
        
        gc.SetPen(wx.TRANSPARENT_PEN)
        gc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour()))
        gc.SetBrush(wx.RED_BRUSH)
        gc.SetFont(wx.Font(self._config.text_font_size_default,
                           wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                           faceName=self._config.text_font_facename_default),
                   wx.Colour(*self._config.text_foreground_colour_default))
        textWidth, textHeight, _, _ = gc.GetFullTextExtent(self._Label)
        # centered values
        textX = (controlRect.GetWidth() // 2) - (textWidth // 2)
        textY = (paddingTop - textHeight//2)
        # draw text background
        lateralOffset = dip(5)
        gc.DrawRectangle(textX-lateralOffset, textY, textWidth+(2*lateralOffset), textHeight)
        # draw text
        gc.DrawText(self._Label, textX, textY)

        # -------------- make panel update size -------------- #

        self.Layout()


    def __OnSize(self, event):
        self.Refresh()
        event.Skip()
        
