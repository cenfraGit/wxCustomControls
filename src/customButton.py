import wx
from .controlConfig import ControlConfig
from .functions.getPenBrush import getPen, getBrush
from .functions.dip import dip
from copy import copy


class CustomButton(wx.Control):
        
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.NO_BORDER,#|wx.TRANSPARENT_WINDOW,
                 validator=wx.DefaultValidator, label=wx.EmptyString,
                 name=wx.ControlNameStr, config=None, **kwargs):

        
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

        self._Label = label

        self._Enabled = True
        self._Pressed = False
        self._MouseHover = False

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
            fg_colour_pressed=(70, 70, 70),
            border_colour_pressed=(0, 0, 0),
            border_width_pressed=0,
            # hover
            bg_colour_hover=(200, 200, 200),
            fg_colour_hover=(100, 100, 100),
            border_colour_hover=(0, 0, 0),
            border_width_hover=0)


    def UpdateConfig(self, **kwargs):
        self.config.update(**kwargs)
        self.Refresh()


    def GetConfig(self):
        return self.config


    def SetBackgroundColour(self, colour:wx.Colour):
        self.config.bg_colour = (colour.GetRed(),
                                 colour.GetGreen(),
                                 colour.GetBlue())
        self.Refresh()


    def GetBackgroundColour(self):
        return wx.Colour(*self.config.bg_colour)


    def SetLabel(self, label:str):
        self._Label = label        
        self.Refresh()


    def GetLabel(self):
        return self._Label


    def __OnPaint(self, event):

        # --------------- create contexts --------------- #
        
        dc = wx.AutoBufferedPaintDC(self)
        #dc = wx.PaintDC(self)
        #dc.SetBackground(wx.TRANSPARENT_BRUSH)
        dc.Clear()
        gc:wx.GraphicsContext = wx.GraphicsContext.Create(dc)

        
        # -------------- drawing rectangle -------------- #
        
        controlRect = self.GetClientRect()

        
        # ------------- background rectangle ------------- #

        gc.SetPen(wx.TRANSPARENT_PEN)
        gc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour()))

        gc.DrawRectangle(controlRect.GetX(), controlRect.GetY(),
                         controlRect.GetWidth(), controlRect.GetHeight())
        

        # ------------ draw button rectangle ------------ #

        if not self._Enabled:
            pen = getPen("disabled", self.config)
            brush = getBrush("disabled", self.config, gc)
            cr = self.config.corner_radius_disabled
            textForeground = self.config.text_foreground_colour_disabled
            image = self.config.image_disabled
            image_channels = self.config.image_disabled_channels
            image_size = self.config.image_disabled_size
        else:
            if self._Pressed:
                pen = getPen("pressed", self.config)
                brush = getBrush("pressed", self.config, gc)
                cr = self.config.corner_radius_pressed
                textForeground = self.config.text_foreground_colour_pressed
                image = self.config.image_pressed
                image_channels = self.config.image_pressed_channels
                image_size = self.config.image_pressed_size
            elif self._MouseHover:
                pen = getPen("hover", self.config)
                brush = getBrush("hover", self.config, gc)
                cr = self.config.corner_radius_hover
                textForeground = self.config.text_foreground_colour_hover
                image = self.config.image_hover
                image_channels = self.config.image_hover_channels
                image_size = self.config.image_hover_size
            else:
                pen = getPen("default", self.config)
                brush = getBrush("default", self.config, gc)
                cr = self.config.corner_radius
                textForeground = self.config.text_foreground_colour
                image = self.config.image_default
                image_channels = self.config.image_default_channels
                image_size = self.config.image_default_size
                

        # set brush and rectangle
        gc.SetPen(pen)
        gc.SetBrush(brush)
        
        # deflate so that borders are drawn correctly
        buttonRectangle = controlRect.Deflate(pen.GetWidth(),
                                              pen.GetWidth())

        # draw button rectangle
        gc.DrawRoundedRectangle(buttonRectangle.GetX(),
                                buttonRectangle.GetY(),
                                buttonRectangle.GetWidth(),
                                buttonRectangle.GetHeight(),
                                radius=cr)


        # ------------- get text dimensions ------------- #
        # used in both image and label drawing process

        textWidth, textHeight = 0, 0
        if (self._Label != wx.EmptyString):
            # create and set the font
            gc.SetFont(wx.Font(self.config.font_size,
                               wx.FONTFAMILY_DEFAULT,
                               wx.FONTSTYLE_NORMAL,
                               wx.FONTWEIGHT_NORMAL,
                               faceName=self.config.font_face_name), textForeground)

            # get text dimensions
            textWidth, textHeight, _, _ = gc.GetFullTextExtent(self._Label)


        # ------------------ draw image ------------------ #

        if image:
            image:wx.Image = image.AdjustChannels(*image_channels)
            bitmap = gc.CreateBitmapFromImage(image)

            # calculate image coordinates
            
            if (self._Label == wx.EmptyString):
                # draw image in center if no text
                imageX = (controlRect.GetWidth() // 2) - (image_size[0] // 2)
                imageY = (controlRect.GetHeight() // 2) - (image_size[1] // 2)
            else:
                text_separation = self.config.image_text_separation if self.config.image_text_separation else dip(6)
                if (self.config.text_side == "right"):
                    imageX = (controlRect.GetWidth() // 2) - ((image_size[0] + textWidth + text_separation) // 2) 
                    imageY = (controlRect.GetHeight() // 2) - (image_size[1] // 2)
                    textX = imageX + image_size[0] + text_separation
                    textY = (controlRect.GetHeight() // 2) - (textHeight // 2)
                elif (self.config.text_side == "left"):
                    textX = (controlRect.GetWidth() // 2) - ((image_size[0] + textWidth + text_separation) // 2) 
                    textY = (controlRect.GetHeight() // 2) - (textHeight // 2)
                    imageX = textX + textWidth + text_separation
                    imageY = (controlRect.GetHeight() // 2) - (image_size[1] // 2)
                elif (self.config.text_side == "up"):
                    textX = (controlRect.GetWidth() // 2) - (textWidth // 2)
                    textY = (controlRect.GetHeight() // 2) - ((image_size[1] + textHeight + text_separation) // 2)
                    imageX = (controlRect.GetWidth() // 2) - (image_size[0] // 2)
                    imageY = textY + textHeight + text_separation
                elif (self.config.text_side == "down"):
                    imageX = (controlRect.GetWidth() // 2) - (image_size[0] // 2)
                    imageY = (controlRect.GetHeight() // 2) - ((image_size[1] + textHeight + text_separation) // 2)
                    textX = (controlRect.GetWidth() // 2) - (textWidth // 2)
                    textY = imageY + image_size[1]
                else:
                    raise ValueError("text_side must be \"right\", \"left\", \"up\" or \"down\".")
            
            gc.DrawBitmap(bitmap, imageX, imageY, image_size[0], image_size[1])
            if (self._Label != wx.EmptyString):
                gc.DrawText(self._Label, textX, textY)
            return # return since text was already drawn (if image)
            

        # -------------- drawing the label -------------- #
        # reaches this point if no image was drawn

        if (self._Label != wx.EmptyString):            
            # calculate center
            textX = buttonRectangle.GetX() + (buttonRectangle.GetWidth() // 2) - (textWidth // 2)
            textY = buttonRectangle.GetY() + (buttonRectangle.GetHeight() // 2) - (textHeight // 2)
            # draw label
            gc.DrawText(self._Label, textX, textY)
        

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

        # get image
        image = self.config.image_default or self.config.image_pressed or self.config.image_hover or self.config.image_disabled
        image_width = max(self.config.image_default_size[0],
                          self.config.image_pressed_size[0],
                          self.config.image_hover_size[0],
                          self.config.image_disabled_size[0])
        image_height = max(self.config.image_default_size[1],
                           self.config.image_pressed_size[1],
                           self.config.image_hover_size[1],
                           self.config.image_disabled_size[1])

        text_separation = self.config.image_text_separation if self.config.image_text_separation else dip(6)

        if image:
            if (self.config.text_side == "left") or (self.config.text_side == "right"):
                width = image_width + text_separation + textWidth + (2 * self._PaddingHorizontal)
                height = max(image_height, textHeight) + (2 * self._PaddingVertical)
            elif (self.config.text_side == "up") or (self.config.text_side == "down"):
                width = max(image_width, textWidth) + (2 * self._PaddingHorizontal)
                height = image_height + text_separation + textHeight + (2 * self._PaddingVertical)
            else:
                raise ValueError("text_side must be \"right\", \"left\", \"up\" or \"down\".")
        else:
            width = self._PaddingHorizontal * 2 + textWidth
            height = self._PaddingVertical * 2 + textHeight
        
        return wx.Size(int(width), int(height))


    def AcceptsFocusFromKeyboard(self):
        return False

    
    def AcceptsFocus(self):
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

