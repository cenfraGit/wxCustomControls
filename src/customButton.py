import wx

from .controlConfig import ControlConfig
from .functions.getPenBrush import getPen, getBrush
from .functions.dip import dip
from copy import copy

class CustomButton(wx.Control):
        
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.NO_BORDER, validator=wx.DefaultValidator, label=wx.EmptyString,
                 name=wx.ControlNameStr, config=None, **kwargs):

        # initialize control
        super().__init__(parent=parent, id=id, pos=pos, style=style, validator=validator, name=name)


        # --------------- check for config --------------- #
        # if the user does not specify a config object, create
        # one and update with kwargs
        self.config:ControlConfig = copy(config) if config else ControlConfig()
        if kwargs:
            self.config.update(**kwargs)

            
        # -------------- control attributes -------------- #

        self._Label = label

        self._Enabled = True
        self._Pressed = False
        self._MouseHover = False

        self._MarginAllSides = dip(1)
        self._PaddingHorizontal = dip(10)
        self._PaddingVertical = dip(5)

        
        # -------------------- setup -------------------- #

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.SetInitialSize(size)

        
        # -------------------- events -------------------- #

        self.Bind(wx.EVT_PAINT, self.__OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.__OnEraseBackground)
        self.Bind(wx.EVT_LEFT_DOWN, self.__OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.__OnLeftUp)
        if (wx.Platform == "__WXMSW__"):
            self.Bind(wx.EVT_LEFT_DCLICK, self.__OnLeftDown)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.__OnMouseLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self.__OnMouseEnter)


    def SetBackgroundColour(self, colour:wx.Colour):
        self.config.bg_colour = colour
        self.Refresh()


    def UpdateConfig(self, **kwargs):
        self.config.update(**kwargs)
        self.Refresh()


    def SetLabel(self, label:str):
        self._Label = label
        self.Refresh()


    def GetLabel(self):
        return self._Label


    def GetConfig(self):
        return self.config


    def __OnPaint(self, event):

        # --------------- create contexts --------------- #
        
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()

        gc: wx.GraphicsContext = wx.GraphicsContext.Create(dc)

        # ---------------- initial setup ---------------- #

        controlRect = self.GetClientRect()

        # ------------- background rectangle ------------- #

        gc.SetPen(wx.TRANSPARENT_PEN)
        gc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour()))

        gc.DrawRectangle(controlRect.GetX(),
                         controlRect.GetY(),
                         controlRect.GetWidth(),
                         controlRect.GetHeight())

        # ------------ draw button rectangle ------------ #

        if not self._Enabled:
            pen = getPen("disabled", self.config)
            brush = getBrush("disabled", self.config, gc)
            cr = self.config.corner_radius_disabled
            textForeground = self.config.text_foreground_colour_disabled
        else:
            if self._Pressed:
                pen = getPen("pressed", self.config)
                brush = getBrush("pressed", self.config, gc)
                cr = self.config.corner_radius_pressed
                textForeground = self.config.text_foreground_colour_pressed
            elif self._MouseHover:
                pen = getPen("hover", self.config)
                brush = getBrush("hover", self.config, gc)
                cr = self.config.corner_radius_hover
                textForeground = self.config.text_foreground_colour_hover
            else:
                pen = getPen("default", self.config)
                brush = getBrush("default", self.config, gc)
                cr = self.config.corner_radius
                textForeground = self.config.text_foreground_colour

        # set brush and rectangle
        gc.SetPen(pen)
        gc.SetBrush(brush)

        paddingAllSides = pen.GetWidth()
        buttonRectangle = controlRect.Deflate(paddingAllSides,
                                              paddingAllSides)

        # draw button rectangle
        if cr:
            gc.DrawRoundedRectangle(buttonRectangle.GetX(),
                                    buttonRectangle.GetY(),
                                    buttonRectangle.GetWidth(),
                                    buttonRectangle.GetHeight(),
                                    radius=cr)
        else:
            gc.DrawRectangle(buttonRectangle.GetX(),
                             buttonRectangle.GetY(),
                             buttonRectangle.GetWidth(),
                             buttonRectangle.GetHeight())

        # -------------- drawing the label -------------- #

        if self._Label == wx.EmptyString or self._Label.strip() == "":
            return

        # create and set the font
        gc.SetFont(wx.Font(self.config.font_size,
                           wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL,
                           faceName=self.config.font_face_name), textForeground)

        # get text dimensions
        textWidth, textHeight, _, _ = gc.GetFullTextExtent(self._Label)
        # calculate center
        textX = buttonRectangle.GetX() + (buttonRectangle.GetWidth() // 2) - (textWidth // 2)
        textY = buttonRectangle.GetY() + (buttonRectangle.GetHeight() // 2) - (textHeight // 2)
        # draw label
        gc.DrawText(self._Label, textX, textY)


    def DoGetBestClientSize(self) -> wx.Size:
        """ Helps the sizers determine the best control size. """
        
        # create font
        font = wx.Font(self.config.font_size,
                       wx.FONTFAMILY_DEFAULT,
                       wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_NORMAL, faceName=self.config.font_face_name)
        # crete device and graphic contexts and set font
        dc = wx.ClientDC(self)
        gc: wx.GraphicsContext = wx.GraphicsContext.Create(dc)
        gc.SetFont(font, wx.BLACK)
        # get label dimensions
        textWidth, textHeight, _, _ = gc.GetFullTextExtent(self._Label)
        # add padding
        width = self._PaddingHorizontal * 2 + textWidth
        height = self._PaddingVertical * 2 + textHeight
        return wx.Size(int(width), int(height))
    

    def __OnEraseBackground(self, event):
        # to prevent flickering
        pass

    
    def __OnLeftDown(self, event):

        self._Pressed = True
        self.Refresh()
        event.Skip()

    
    def __OnLeftUp(self, event):
        if self._Pressed:
            self._Pressed = False
            self.Refresh()
            wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.GetId()))
        event.Skip()
        

    def __OnMouseEnter(self, event):
        self._MouseHover = True
        self.Refresh()
        event.Skip()

        
    def __OnMouseLeave(self, event):
        self._MouseHover = False
        self._Pressed = False
        self.Refresh()
        event.Skip()


    def AcceptsFocusFromKeyboard(self):
        return False


    def Enable(self, enable:bool=True) -> None:
        """Uses _Enabled to define if the widget is enabled or not
        instead of using default behavior (problems redrawing after
        modal dialogs).
        """
        self._Enabled = enable
        super().Enable(enable)
        self.Refresh()
        

    def Disable(self) -> None:
        self.Enable(False)

