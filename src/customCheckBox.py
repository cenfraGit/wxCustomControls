import wx

from .controlConfig import ControlConfig
from .functions.getPenBrush import getPen, getBrush
from .functions.dip import dip
from copy import copy


class CustomCheckBox(wx.Control):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.NO_BORDER,
                 validator=wx.DefaultValidator, label=wx.EmptyString,
                 name=wx.ControlNameStr, textSide="right", value=False, config=None, **kwargs):

        # initialize control
        super().__init__(parent=parent, id=id, pos=pos, style=style, validator=validator, name=name)

        # --------------- check for config --------------- #
        # if the user does not specify a config object, create
        # one and update with kwargs
        self.config:ControlConfig = copy(config) if config else ControlConfig()
        if kwargs:
            self.config.update(**kwargs)

        # -------------- control attributes -------------- #

        self._Value = value

        self._Label = label
        self._TextSide = textSide

        self._Enabled = True
        self._Pressed = False
        self._MouseHover = False

        self._BoxTextSeparation = self.config.checkbox_text_separation if self.config.checkbox_text_separation else dip(5)
        self._BoxWidth = self.config.checkbox_width if self.config.checkbox_width else dip(20)
        self._BoxHeight = self.config.checkbox_height if self.config.checkbox_height else dip(20)
        self._DeflateSelection = self.config.checkbox_active_deflate if self.config.checkbox_active_deflate else dip(5)

        self._PaddingAllSides = dip(3)

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

    
    def GetValue(self):
        return self._Value

    
    def SetValue(self, value:bool):
        self._Value = value

    
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

        # set pen and brush for checkbox rectangle
        gc.SetPen(pen)
        gc.SetBrush(brush)

        #checkBoxSidePadding = pen.GetWidth()
        checkBoxSidePadding = max(self.config.border_width,
                                  self.config.border_width_hover,
                                  self.config.border_width_pressed,
                                  self.config.border_width_disabled)

        # calculate checkbox position based on textside
        checkBoxX = checkBoxSidePadding if (self._TextSide == "right") else (controlRect.GetWidth() - checkBoxSidePadding - self._BoxWidth)
        checkBoxY = (controlRect.GetHeight() // 2) - (self._BoxHeight // 2)

        checkBoxRectangle = wx.Rect(checkBoxX, checkBoxY, self._BoxWidth, self._BoxHeight)

        # draw checkbox
        gc.DrawRectangle(checkBoxRectangle.GetX(),
                         checkBoxRectangle.GetY(),
                         checkBoxRectangle.GetWidth(),
                         checkBoxRectangle.GetHeight())

        # ------------------ selection ------------------ #

        selectionBox = checkBoxRectangle.Deflate(self._DeflateSelection,
                                                 self._DeflateSelection)

        if self._Value:
            gc.SetPen(wx.TRANSPARENT_PEN)
            gc.SetBrush(wx.Brush(wx.Colour(self.config.bg_active)))
            gc.DrawRectangle(selectionBox.GetX(),
                             selectionBox.GetY(),
                             selectionBox.GetWidth(),
                             selectionBox.GetHeight())

            
        # -------------- drawing the label -------------- #
        # calculate textposition based on textside and text separation

        if self._Label == wx.EmptyString or self._Label.strip() == "":
            return
        
        gc.SetFont(wx.Font(self.config.font_size,
                           wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL,
                           faceName=self.config.font_face_name), textForeground)
        
        # get text dimensions
        textWidth, textHeight, _, _ = gc.GetFullTextExtent(self._Label)

        # calculate text position

        if self._TextSide == "left":        
            textX = controlRect.GetWidth() - checkBoxSidePadding - self._BoxWidth - self._BoxTextSeparation - textWidth
        else: # if right
            textX = checkBoxSidePadding + self._BoxWidth + self._BoxTextSeparation
            
        textY = (controlRect.GetHeight() // 2) - (textHeight // 2)

        # draw text
        gc.DrawText(self._Label, textX, textY)


    def __OnEraseBackground(self, event):
        # to prevent flickering
        pass

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

        # checkbox side padding
        checkBoxSidePadding = max(self.config.border_width,
                                  self.config.border_width_hover,
                                  self.config.border_width_pressed,
                                  self.config.border_width_disabled)

        width = checkBoxSidePadding + self._BoxWidth + self._BoxTextSeparation + textWidth + self._PaddingAllSides
        height = max(self._BoxHeight, textHeight) + self._PaddingAllSides
        return wx.Size(int(width), int(height))
        

    def __OnLeftDown(self, event):
        self._Pressed = True
        self.Refresh()
        event.Skip()

    def __OnLeftUp(self, event):
        if self._Pressed:
            self._Pressed = False
            self._Value = not self._Value
            wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_CHECKBOX.typeId, self.GetId()))
        self.Refresh()
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

