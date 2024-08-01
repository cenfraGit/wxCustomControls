import wx
from .functions.dip import dip


class CustomButton(wx.Control):
    """ Defines a custom button. """
    
    def __init__(self, parent, id=wx.ID_ANY,
                 label:str="",
                 pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 validator=wx.DefaultValidator,
                 fontSize=8,
                 faceName="Verdana",
                 cornerRadius=0,
                 # normal colors
                 backgroundColour=wx.Colour(240, 240, 240),
                 borderColour=wx.Colour(200, 200, 200),
                 backgroundLinearGradient=None,
                 textForegroundColour=wx.Colour(20, 20, 20),
                 borderWidth:int=1, 
                 # mouse hover colors
                 hoverBackgroundColour=wx.Colour(240, 240, 240),
                 hoverBorderColour=wx.Colour(160, 160, 160),
                 hoverBackgroundLinearGradient=None,
                 hoverTextForegroundColour=wx.BLACK,
                 hoverBorderWidth:int=2,
                 # button pressed colors
                 pressedBackgroundColour=wx.Colour(180, 180, 180),
                 pressedBorderColour=wx.Colour(80, 80, 80),
                 pressedTextForegroundColour=wx.BLACK,
                 pressedBackgroundLinearGradient=None,
                 pressedBorderWidth:int=2,
                 # button disabled colors
                 disabledBackgroundColour=wx.BLACK,
                 disabledBorderColour=wx.BLACK,
                 disabledTextForegroundColour=wx.WHITE,
                 disabledBackgroundLinearGradient=None,
                 disabledBorderWidth:int=0,
                 # behind background (for gradients)
                 behindBackgroundLinearGradient=None,
                 ):
        
        super().__init__(parent, id, pos, size, wx.NO_BORDER, validator, "CustomButton")

        # -------------- ATTRIBUTES --------------
        
        self._Label = label
        self._FontSize = fontSize
        self._FaceName = faceName
        self._CornerRadius = dip(cornerRadius)

        # -------------------- colors -------------------- #

        # default
        self._BackgroundColour = backgroundColour
        self._BorderColour = borderColour
        self._BackgroundLinearGradient = backgroundLinearGradient
        self._TextForegroundColour = textForegroundColour
        self._BorderWidth = borderWidth
        # mouse hover
        self._HoverBackgroundColour = hoverBackgroundColour
        self._HoverBorderColour = hoverBorderColour
        self._HoverBackgroundLinearGradient = hoverBackgroundLinearGradient
        self._HoverTextForegroundColour = hoverTextForegroundColour
        self._HoverBorderWidth = hoverBorderWidth
        # button pressed
        self._PressedBackgroundColour = pressedBackgroundColour
        self._PressedBorderColour = pressedBorderColour
        self._PressedBackgroundLinearGradient = pressedBackgroundLinearGradient
        self._PressedTextForegroundColour = pressedTextForegroundColour
        self._PressedBorderWidth = pressedBorderWidth
        # disabled
        self._DisabledBackgroundColour = disabledBackgroundColour
        self._DisabledBorderColour = disabledBorderColour
        self._DisabledBackgroundLinearGradient = disabledBackgroundLinearGradient
        self._DisabledTextForegroundColour = disabledTextForegroundColour
        self._DisabledBorderWidth = disabledBorderWidth

        # behind background
        self._BehindBackgroundLinearGradient = behindBackgroundLinearGradient
        
        # control states
        self._Enabled = True
        self._Pressed = False
        self._MouseHover = False
        

        # -------------- APPEARANCE --------------
        
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.SetInitialSize(size)

        #self._MarginAllSides = dip(1) #dip(self._BorderWidth) if (self._BorderWidth != 0) else dip(1)
        self._MarginAllSides = self._BorderWidth if (self._BehindBackgroundLinearGradient) else dip(1)

        # -------------- EVENTS --------------
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        if (wx.Platform == "__WXMSW__"):
            self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)


    def SetBackgroundColour(self, colour):
        self._BackgroundColour = colour
        self.Refresh()


    def SetBorderColour(self, colour):
        self._BorderColour = colour
        self.Refresh() 


    def SetBorderWidth(self, width):
        self._BorderWidth = width
        self.Refresh() 


    def SetCornerRadius(self, radius):
        self._CornerRadius = radius
        self.Refresh() 


    def GetBackgroundColour(self):
        return self._BackgroundColour


    def GetBorderColour(self):
        return self._BorderColour


    def GetBorderWidth(self):
        return self._BorderWidth


    def GetBorderLinearGradient(self):
        return self._BackgroundLinearGradient


    def GetLabel(self):
        return self._Label

        
    def SetLabel(self, label:str) -> None:
        """ Sets the button's label text. """
        self._Label = label
        self.Refresh()
        

    def OnPaint(self, event) -> None:
        """ Handles the paint event. """

        # -------------- creating contexts -------------- #
        
        # create device context
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()

        # create graphics context (to use gdi+)
        gc = wx.GraphicsContext.Create(dc)

        # ---------------- initial setup ---------------- #
    
        # we get our drawing area as a rectangle
        controlRect = self.GetClientRect()

        # ------------- background rectangle ------------- #

        # when drawing a rounded button, the corners will allow us to
        # see the color that's 'behind' the button. we want this
        # background color to be the same as the parent's background
        # to give the illusion that there's no separation between this
        # background and the parent's.

        # if the user specified a value for the
        # "behindBackgroundLinearGradient", we will use this gradient
        # as a brush to draw this background rectangle.

        # we are not interested in the borders, so we use a
        # transparent pen.
        gc.SetPen(wx.TRANSPARENT_PEN)

        # also, if the user is using a background gradient (which
        # represent a gradient border), we will also have to use this
        # background rectangle to substitute for the borders of the
        # button.

        # then we set the background brush
        if self._BehindBackgroundLinearGradient:
            if self._Pressed:
                gc.SetBrush(wx.Brush(self._PressedBorderColour))
            elif self._MouseHover:
                gc.SetBrush(wx.Brush(self._HoverBorderColour))
            else:
                gc.SetBrush(gc.CreateLinearGradientBrush(*self._BehindBackgroundLinearGradient))
        else:
            gc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour(), wx.BRUSHSTYLE_SOLID))
            
        #gc.SetBrush(wx.GREEN_BRUSH)

        # finally, we draw the background rectangle
        gc.DrawRectangle(controlRect.GetX(),
                         controlRect.GetY(),
                         controlRect.GetWidth(),
                         controlRect.GetHeight())

        # -------------- drawing the button -------------- #

        # we will first create a rectangle that will represent the
        # button. it will be slightly smaller thatn the client's
        # rectangle because if it were to occupy the same size, some
        # of the borders may not appear correctly.

        buttonRectangle = controlRect.Deflate(self._MarginAllSides,
                                              self._MarginAllSides)

        # we will now draw the button depending on the current states
        # of the control.

        # 1. we check if the button is enabled
        # 2. if it is, check if the button is pressed
        # 3. if its not pressed, check if cursor is hovering
        # 4. if not hovering, draw with default colors.

        # --------------- pens and brushes --------------- #

        if not self._Enabled:
            
            # set a transparent pen if the width is 0
            if (not self._DisabledBorderWidth) or (self._BehindBackgroundLinearGradient):
                pen = wx.TRANSPARENT_PEN
            else:
                pen = wx.Pen(self._DisabledBorderColour, self._DisabledBorderWidth)

            # create a gradient if specified
            if self._DisabledBackgroundLinearGradient:
                brush = gc.CreateLinearGradientBrush(*self._DisabledBackgroundLinearGradient)
            else:
                brush = wx.Brush(self._DisabledBackgroundColour)

            # set foreground color
            textForeground = self._DisabledTextForegroundColour
            
        else:
            if self._Pressed:
                
                # set a transparent pen if the width is 0
                if (not self._PressedBorderWidth) or (self._BehindBackgroundLinearGradient):
                    pen = wx.TRANSPARENT_PEN
                else:
                    pen = wx.Pen(self._PressedBorderColour, self._PressedBorderWidth)

                # create a gradient if specified
                if self._PressedBackgroundLinearGradient:
                    brush = gc.CreateLinearGradientBrush(*self._PressedBackgroundLinearGradient)
                else:
                    brush = wx.Brush(self._PressedBackgroundColour)

                # set foreground color
                textForeground = self._PressedTextForegroundColour
                
            elif self._MouseHover:

                # set a transparent pen if the width is 0
                if (not self._HoverBorderWidth) or (self._BehindBackgroundLinearGradient):
                    pen = wx.TRANSPARENT_PEN
                else:
                    pen = wx.Pen(self._HoverBorderColour, self._HoverBorderWidth)

                # create a gradient if specified
                if self._HoverBackgroundLinearGradient:
                    brush = gc.CreateLinearGradientBrush(*self._HoverBackgroundLinearGradient)
                else:
                    brush = wx.Brush(self._HoverBackgroundColour)
                    
                # set foreground color
                textForeground = self._HoverTextForegroundColour
                
            else:

                # set a transparent pen if the width is 0
                if (not self._BorderWidth) or (self._BehindBackgroundLinearGradient):
                    pen = wx.TRANSPARENT_PEN
                else:
                    pen = wx.Pen(self._BorderColour, self._BorderWidth)
                    
                # create a gradient if specified
                if self._BackgroundLinearGradient:
                    brush = gc.CreateLinearGradientBrush(*self._BackgroundLinearGradient)
                else:
                    brush = wx.Brush(self._BackgroundColour)

                # set foreground color
                textForeground = self._TextForegroundColour
                

        # we then set the pen and brush and draw the rectangle.
        gc.SetPen(pen)
        gc.SetBrush(brush)

        # if a corner radius value was specified, we will draw a
        # rounded rectangle. if not, we will draw a normal rectangle.

        if self._CornerRadius:
            gc.DrawRoundedRectangle(buttonRectangle.GetX(),
                                    buttonRectangle.GetY(),
                                    buttonRectangle.GetWidth(),
                                    buttonRectangle.GetHeight(),
                                    radius=self._CornerRadius)
        else:
            gc.DrawRectangle(buttonRectangle.GetX(),
                             buttonRectangle.GetY(),
                             buttonRectangle.GetWidth(),
                             buttonRectangle.GetHeight())
        

        # -------------- drawing the label -------------- #

        # we first se the font to get the text extent of the label
        # text (to draw centered)
        gc.SetFont(wx.Font(self._FontSize,
                           wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL,
                           faceName=self._FaceName), textForeground)

        textWidth, textHeight, _, _ = gc.GetFullTextExtent(self._Label)

        # we now use these values to calculate the x and y coordinates
        # that would correspond to a centered label
        textX = buttonRectangle.GetX() + (buttonRectangle.GetWidth() // 2) - (textWidth // 2)
        textY = buttonRectangle.GetY() + (buttonRectangle.GetHeight() // 2) - (textHeight // 2)
        # finally, we draw the label.
        gc.DrawText(self._Label, textX, textY)
        

    def OnEraseBackground(self, event) -> None:
        """ Bound to prevent flickering. """
        pass


    def DoGetBestClientSize(self) -> wx.Size:
        """ Determines the best size for the control. """

        # create font
        font = wx.Font(self._FontSize,
                       wx.FONTFAMILY_DEFAULT,
                       wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_NORMAL,
                       faceName=self._FaceName)

        # create device context and set font to determine text dimensions
        dc = wx.ClientDC(self)
        dc.SetFont(font)

        # get label dimensions
        textWidth, textHeight = dc.GetTextExtent(self._Label)

        # margins for sides
        leftRightMargins = dip(20)
        topBottomMargins = dip(5)

        # final control dimensions
        width = leftRightMargins*2 + textWidth
        height = topBottomMargins*2 + textHeight

        # return best size
        return wx.Size(width, height)
    

    def OnLeftDown(self, event:wx.MouseEvent) -> None:
        self._Pressed = True
        self.Refresh()
        event.Skip()


    def OnLeftUp(self, event:wx.MouseEvent) -> None:
        if self._Pressed:
            self._Pressed = False
            self.Refresh()
            wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.GetId()))
        event.Skip()
        

    def OnMouseLeave(self, event:wx.MouseEvent) -> None:
        self._MouseHover = False
        self._Pressed = False
        self.Refresh()
        event.Skip()
        

    def OnMouseEnter(self, event:wx.MouseEvent) -> None:
        self._MouseHover = True
        self.Refresh()
        event.Skip()


    def AcceptsFocusFromKeyboard(self) -> bool:
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

