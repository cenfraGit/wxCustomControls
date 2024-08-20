import wx

from .controlConfig import ControlConfig
from .functions.getPenBrush import getPen, getBrush
from .functions.dip import dip
from copy import copy


class CustomCheckBox(wx.Control):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.NO_BORDER,
                 validator=wx.DefaultValidator, label=wx.EmptyString,
                 name=wx.ControlNameStr, value=False, config=None,
                 **kwargs):

        # initialize control
        super().__init__(parent=parent, id=id, pos=pos, style=style,
                         validator=validator, name=name)

        # --------------- check for config --------------- #

        if config:
            self.config:ControlConfig = copy(config)
        else:
            self.config:ControlConfig = self.__GetDefaultConfig()

        if kwargs:
            self.config.update(**kwargs)

        # -------------- control attributes -------------- #

        self._Value = value

        self._Label = label

        self._Enabled = True
        self._Pressed = False
        self._MouseHover = False

        self._CheckDeflate = self.config.checkbox_active_deflate if self.config.checkbox_active_deflate else dip(5)
        self._BoxTextSeparation = self.config.checkbox_text_separation if self.config.checkbox_text_separation else dip(5)
        self._BoxWidth = self.config.checkbox_width if self.config.checkbox_width else dip(20)
        self._BoxHeight = self.config.checkbox_height if self.config.checkbox_height else dip(20)
        self._SwitchWidth = self.config.switch_width if self.config.switch_width else dip(50)
        self._SwitchHeight = self.config.switch_height if self.config.switch_height else dip(20)

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


    def __GetDefaultConfig(self) -> ControlConfig:
        """ Returns the default configuration for this control. """
        return ControlConfig(
            # default colors
            bg_colour=(240, 240, 240),
            border_colour=(200, 200, 200),
            border_width=1,
            text_foreground_colour=(20, 20, 20),
            # pressed
            bg_colour_pressed=(180, 180, 180),
            border_colour_pressed=(0, 0, 0),
            border_width_pressed=0,
            # hover
            bg_colour_hover=(240, 240, 240),
            border_colour_hover=(0, 0, 0),
            border_width_hover=1,
            corner_radius=dip(3),
            bg_active=(57, 117, 186),
            
            switch_radius=dip(3),
            switch_selector_padding=dip(1),
            switch_selector_width=2
        
        )
    
        

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

        gc:wx.GraphicsContext = wx.GraphicsContext.Create(dc)

        # ---------------- initial setup ---------------- #

        controlRect = self.GetClientRect()

        # ------------- background rectangle ------------- #

        gc.SetPen(wx.TRANSPARENT_PEN)
        gc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour()))
        #gc.SetBrush(wx.GREEN_BRUSH)

        gc.DrawRectangle(controlRect.GetX(),
                         controlRect.GetY(),
                         controlRect.GetWidth(),
                         controlRect.GetHeight())

        # -------------- draw box rectangle -------------- #

        if not self._Enabled:
            pen = getPen("disabled", self.config)
            brush = getBrush("disabled", self.config, gc)
            cr = self.config.corner_radius_disabled
            textForeground = self.config.text_foreground_colour_disabled
            image = self.config.image_disabled
            image_channels = self.config.image_disabled_channels
            image_size = self.config.image_disabled_size
            cursor = wx.Cursor(self.config.cursor_disabled) if self.config.cursor_disabled else wx.Cursor(wx.CURSOR_ARROW)
            bg_active = self.config.bg_active_disabled
            fg_colour = self.config.fg_colour_disabled
        else:
            if self._Pressed:
                pen = getPen("pressed", self.config)
                brush = getBrush("pressed", self.config, gc)
                cr = self.config.corner_radius_pressed
                textForeground = self.config.text_foreground_colour_pressed
                image = self.config.image_pressed
                image_channels = self.config.image_pressed_channels
                image_size = self.config.image_pressed_size
                cursor = wx.Cursor(self.config.cursor_pressed) if self.config.cursor_pressed else wx.Cursor(wx.CURSOR_ARROW)
                bg_active = self.config.bg_active_pressed
                fg_colour = self.config.fg_colour_pressed
            elif self._MouseHover:
                pen = getPen("hover", self.config)
                brush = getBrush("hover", self.config, gc)
                cr = self.config.corner_radius_hover
                textForeground = self.config.text_foreground_colour_hover
                image = self.config.image_hover
                image_channels = self.config.image_hover_channels
                image_size = self.config.image_hover_size
                cursor = wx.Cursor(self.config.cursor_hover) if self.config.cursor_hover else wx.Cursor(wx.CURSOR_ARROW)
                bg_active = self.config.bg_active_hover
                fg_colour = self.config.fg_colour_hover
            else:
                pen = getPen("default", self.config)
                brush = getBrush("default", self.config, gc)
                cr = self.config.corner_radius
                textForeground = self.config.text_foreground_colour
                image = self.config.image_default
                image_channels = self.config.image_default_channels
                image_size = self.config.image_default_size
                cursor = wx.Cursor(wx.CURSOR_ARROW)
                bg_active = self.config.bg_active
                fg_colour = self.config.fg_colour

        # ---------- choose checkbox or switch ---------- #

        sidePadding = max(self.config.border_width,
                          self.config.border_width_hover,
                          self.config.border_width_pressed,
                          self.config.border_width_disabled)

        if not self.config.switch_appearance:

            # calculate checkbox position based on textside
            boxX = sidePadding if (self.config.text_side == "right") else (controlRect.GetWidth() - sidePadding - self._BoxWidth)
            boxY = (controlRect.GetHeight() // 2) - (self._BoxHeight // 2)

            boxRectangle = wx.Rect(boxX, boxY, self._BoxWidth, self._BoxHeight)

            gc.SetPen(pen)
            gc.SetBrush(brush)

            if self._Value:
                # draw selected background
                gc.SetPen(wx.TRANSPARENT_PEN)
                gc.SetBrush(wx.Brush(wx.Colour(self.config.bg_active)))
                gc.DrawRoundedRectangle(boxRectangle.GetX(),
                                        boxRectangle.GetY(),
                                        boxRectangle.GetWidth(),
                                        boxRectangle.GetHeight(), self.config.corner_radius)

                # checkRectangle
                cRect = copy(boxRectangle).Deflate(self._CheckDeflate,
                                                      self._CheckDeflate)
                
                # draw check
                gc.SetPen(wx.Pen(wx.WHITE, width=2))
                gc.SetBrush(wx.TRANSPARENT_BRUSH)
                path = gc.CreatePath()
                path.MoveToPoint(cRect.GetX(), cRect.GetY() + (cRect.GetHeight() // 2))
                path.AddLineToPoint(cRect.GetX() + (cRect.GetWidth() //2 ), cRect.GetY() + cRect.GetHeight())
                path.AddLineToPoint(*cRect.GetTopRight())
                gc.StrokePath(path)
                

                # reset pen
                gc.SetPen(pen)


            

            # draw checkbox
            gc.DrawRoundedRectangle(boxRectangle.GetX(),
                                    boxRectangle.GetY(),
                                    boxRectangle.GetWidth(),
                                    boxRectangle.GetHeight(), self.config.corner_radius)

        else: # if switch
            
            boxX = sidePadding if (self.config.text_side == "right") else (controlRect.GetWidth() - sidePadding - self._SwitchWidth)
            boxY = (controlRect.GetHeight() // 2) - (self._SwitchHeight // 2)
            boxRectangle = wx.Rect(boxX, boxY, self._SwitchWidth, self._SwitchHeight)

            # draw switch background
            gc.SetPen(pen)
            if self._Value:
                gc.SetBrush(wx.Brush(wx.Colour(self.config.bg_active)))
            else:
                gc.SetBrush(brush)
            gc.DrawRoundedRectangle(boxRectangle.GetX(),
                                    boxRectangle.GetY(),
                                    boxRectangle.GetWidth(),
                                    boxRectangle.GetHeight(), self.config.corner_radius)

            if self._Value: # draw to the right side
                selectionX = boxRectangle.GetX() + boxRectangle.GetWidth() - self._SwitchHeight
                selectionY = boxRectangle.GetY()
            else: # draw to the left side    
                selectionX = boxRectangle.GetX()
                selectionY = boxRectangle.GetY()

            # draw indicator
            if self.config.switch_selector_border_width:
                pen = wx.Pen(wx.Colour(*self.config.switch_selector_border_colour), width=self.config.switch_selector_border_width)
            else:
                pen = wx.TRANSPARENT_PEN
            gc.SetPen(pen)
            gc.SetBrush(wx.Brush(wx.Colour(*fg_colour)))
            if self.config.switch_rounded:
                gc.DrawEllipse(selectionX + self.config.switch_selector_padding,
                               selectionY + self.config.switch_selector_padding,
                               self._SwitchHeight - (2 * self.config.switch_selector_padding),
                               self._SwitchHeight - (2 * self.config.switch_selector_padding))
            else:
                gc.DrawRoundedRectangle(selectionX + self.config.switch_selector_padding,
                                        selectionY + self.config.switch_selector_padding,
                                        self._SwitchHeight - (2 * self.config.switch_selector_padding),
                                        self._SwitchHeight - (2 * self.config.switch_selector_padding),
                                        self.config.switch_radius)

        # ------------- get text dimensions ------------- #
        # used in both image and label drawing process

        textWidth, textHeight = 0, 0
        if self._Label != wx.EmptyString:
            gc.SetFont(wx.Font(self.config.font_size,
                               wx.FONTFAMILY_DEFAULT,
                               wx.FONTSTYLE_NORMAL,
                               wx.FONTWEIGHT_NORMAL,
                               faceName=self.config.font_face_name), textForeground)
            # get text dimensions
            textWidth, textHeight, _, _ = gc.GetFullTextExtent(self._Label)
        

        # -------------- drawing the image -------------- #

        if image:
            image:wx.Image = image.AdjustChannels(*image_channels)
            bitmap = gc.CreateBitmapFromImage(image)

            text_separation = self.config.image_text_separation if self.config.image_text_separation else dip(6)

            if self.config.text_side == "right":
                imageX = boxRectangle.GetX() + boxRectangle.GetWidth() + text_separation
                imageY = (controlRect.GetHeight() // 2) - (image_size[1] // 2)
            elif self.config.text_side == "left":
                imageX = boxRectangle.GetX() - text_separation - (image_size[0])
                imageY = (controlRect.GetHeight() // 2) - (image_size[1] // 2)
            else:
                raise ValueError("Text side must be right or left only.")

            gc.DrawBitmap(bitmap, imageX, imageY, *image_size)

            
        # -------------- drawing the label -------------- #
        # calculate textposition based on textside and text separation

        if self._Label != wx.EmptyString:
            
            # calculate text position
            if self.config.text_side == "right":
                textX = sidePadding + boxRectangle.GetWidth() + image_size[0] + self._BoxTextSeparation
            elif self.config.text_side == "left":        
                textX = controlRect.GetWidth() - sidePadding - boxRectangle.GetWidth() - image_size[1] - self._BoxTextSeparation - textWidth
            else:
                raise ValueError("Text side must be right or left only.")
            
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

        # pen width for padding
        sidePadding = max(self.config.border_width,
                          self.config.border_width_hover,
                          self.config.border_width_pressed,
                          self.config.border_width_disabled)

        max_image_width = max(self.config.image_disabled_size[0],
                              self.config.image_pressed_size[0],
                              self.config.image_hover_size[0],
                              self.config.image_default_size[0])

        max_image_height = max(self.config.image_disabled_size[1],
                               self.config.image_pressed_size[1],
                               self.config.image_hover_size[1],
                               self.config.image_default_size[1])

        if self.config.switch_appearance:
            boxWidth = self._SwitchWidth
            boxHeight = self._SwitchHeight
        else:
            boxWidth = self._BoxWidth
            boxHeight = self._BoxHeight

        width = sidePadding + boxWidth + self._BoxTextSeparation + max_image_width + textWidth + self._PaddingAllSides 
        height = max(boxHeight, textHeight, max_image_height) + self._PaddingAllSides
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

