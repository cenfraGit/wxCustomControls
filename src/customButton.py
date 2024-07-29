import wx
if __name__ == "__main__":
    from dip import dip
    from themes import lightTheme, blueTheme
else:
    from .dip import dip
    from .themes import lightTheme, blueTheme


class CustomButton(wx.Control):    
    """ Defines a custom button that supports themes. """
    
    def __init__(self, parent, id=wx.ID_ANY, label:str="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.NO_BORDER, validator=wx.DefaultValidator,
                 name="CustomButton", theme:str="light", fontSize=8):
        super().__init__(parent, id, pos, size, style, validator, name)

        # control attributes
        self.label = label
        self._Theme = theme
        self._Enabled = True
        self._fontSize = fontSize

        # state attributes
        self.pressed = False
        self.mouseHover = False

        # initialize control properties from theme
        self.initializeProperties()

        # set up control size
        self.SetInitialSize(size)
        
        # set up autobufferedpaintdc
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        # bind control events
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        if (wx.Platform == "__WXMSW__"):
            self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        
        
    def initializeProperties(self):
        """ Chooses a properties dictionary according to theme. """

        if (self._Theme == "light"):
            self._themeDict = lightTheme
        elif (self._Theme == "blue"):
            self._themeDict = blueTheme
        else:
            # invalid theme
            self._themeDict = lightTheme

        
    def SetValue(self, value):
        self.label = value
        self.Refresh()
        

    def OnPaint(self, event):
        """ Handles the paint event. """
        
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        self.Draw(dc)
        

    def Draw(self, dc: wx.AutoBufferedPaintDC) -> None:
        """ Draws the actual control. """
        
        rect = self.GetClientRect()

        # draw background with parent color (for rounded corners)
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour(), wx.BRUSHSTYLE_SOLID))
        dc.DrawRectangle(rect)

        # 1. check if the button is enabled
        # 2. if it is, check if the button is pressed
        # 3. if its not pressed, check if cursor is hovering
        # 4. if not hovering, draw with default colors.

        if not self._Enabled:
            dc.SetPen(wx.Pen(self._themeDict["penDisabled"], 1))
            dc.SetBrush(wx.Brush(self._themeDict["brushDisabled"], wx.BRUSHSTYLE_SOLID))
            dc.SetTextForeground(self._themeDict["textForegroundDisabled"])
        else:
            if self.pressed:
                dc.SetPen(wx.Pen(self._themeDict["penPressed"], 1))
                dc.SetBrush(wx.Brush(self._themeDict["brushPressed"], wx.BRUSHSTYLE_SOLID))
                dc.SetTextForeground(self._themeDict["textForegroundPressed"])
            elif self.mouseHover:
                dc.SetPen(wx.Pen(self._themeDict["penHover"], 1))
                dc.SetBrush(wx.Brush(self._themeDict["brushHover"], wx.BRUSHSTYLE_SOLID))
                dc.SetTextForeground(self._themeDict["textForegroundHover"])
            else:
                dc.SetPen(wx.Pen(self._themeDict["penDefault"], 1))
                dc.SetBrush(wx.Brush(self._themeDict["brushDefault"], wx.BRUSHSTYLE_SOLID))
                dc.SetTextForeground(self._themeDict["textForegroundDefault"])
            
        # draw border    
        dc.DrawRoundedRectangle(rect, dip(6))

        # draw text (centered)
        dc.SetFont(wx.Font(self._fontSize,
                           wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL,
                           faceName=self._themeDict["fontFaceName"]))
        textWidth, textHeight = dc.GetTextExtent(self.label)
        textX = rect.GetX() + (rect.GetWidth() // 2) - (textWidth // 2)
        textY = rect.GetY() + (rect.GetHeight() // 2) - (textHeight // 2)
        dc.DrawText(self.label, textX, textY)
        

    def OnEraseBackground(self, event) -> None:
        """ Bound to prevent flickering. """
        pass


    def DoGetBestClientSize(self) -> wx.Size:

        """ Determines the best size for the control. """

        # create font
        font = wx.Font(self._fontSize,
                       wx.FONTFAMILY_DEFAULT,
                       wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_NORMAL,
                       faceName=self._themeDict["fontFaceName"])

        # create device context and set font to determine text dimensions
        dc = wx.ClientDC(self)
        dc.SetFont(font)

        # get label dimensions
        textWidth, textHeight = dc.GetTextExtent(self.label)

        # margins for sides
        leftRightMargins = dip(20)
        topBottomMargins = dip(5)

        # final control dimensions
        width = leftRightMargins*2 + textWidth
        height = topBottomMargins*2 + textHeight
        
        return wx.Size(width, height)
    

    def OnLeftDown(self, event) -> None:
        self.pressed = True
        self.Refresh()
        event.Skip()


    def OnLeftUp(self, event) -> None:
        if self.pressed:
            self.pressed = False
            self.Refresh()
            wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.GetId()))
        event.Skip()
        

    def OnMouseLeave(self, event) -> None:
        self.mouseHover = False
        if self.pressed:
            self.pressed = False
        self.Refresh()
        event.Skip()
        

    def OnMouseEnter(self, event) -> None:
        self.mouseHover = True
        self.Refresh()
        event.Skip()


    def AcceptsFocusFromKeyboard(self) -> bool:
        return False
        

    def Enable(self, enable=True) -> None:
        """Uses _Enabled to define if the widget is enabled or not
        instead of using default behavior (problems redrawing after
        modal dialogs).
        """
        self._Enabled = enable
        super().Enable(enable)
        self.Refresh()
        

    def Disable(self) -> None:
        self.Enable(False)

        
# testing
if __name__ == "__main__":

    if (wx.Platform == "__WXMSW__"):
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    
    class MyFrame(wx.Frame):
        
        def __init__(self):
            super().__init__(None, title="control test")
            panel = wx.Panel(self)
            panel.SetBackgroundColour(lightTheme["background"])

            # custom control
            #self.button = CustomButton(panel, label="Click Me", pos=wx.Point(50, 50), size=wx.Size(300, 40), theme="blue")
            self.button = CustomButton(panel, label="Click Me", pos=wx.Point(50, 50), theme="light")
            # native control
            #wx.Button(panel, label="Click Me", pos=(50, 100), size=(300, 40))
            wx.Button(panel, label="Click Me", pos=(50, 100)) 

            #self.Bind(wx.EVT_BUTTON, self.OnButtonClicked, self.button)
            self.Show()
            

        def OnButtonClicked(self, event) -> None:
            wx.MessageBox("Button clicked!", parent=self)
            

    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()
