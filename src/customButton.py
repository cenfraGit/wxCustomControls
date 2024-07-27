import wx
from dip import dip
from themeColors import lightTheme, blueTheme


class customButton(wx.Control):    
    """ Defines a custom button that supports themes. """
    
    def __init__(self, parent, id=wx.ID_ANY, label:str="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.NO_BORDER, validator=wx.DefaultValidator,
                 name="customButton", theme:str="light"):
        super().__init__(parent, id, pos, size, style, validator, name)

        # control attributes
        self.label = label
        self._Theme = theme
        self._Enabled = True

        # state attributes
        self.pressed = False
        self.mouseHover = False

        # initialize control colors
        self.initializeColors()
        
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
        
        
    def initializeColors(self):
        """ Chooses a colors dictionary according to theme. """

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
            dc.SetPen(self._themeDict["penDisabled"])
            dc.SetBrush(self._themeDict["brushDisabled"])
            dc.SetTextForeground(self._themeDict["textForegroundDisabled"])
        else:
            if self.pressed:
                dc.SetPen(self._themeDict["penPressed"])
                dc.SetBrush(self._themeDict["brushPressed"])
                dc.SetTextForeground(self._themeDict["textForegroundPressed"])
            elif self.mouseHover:
                dc.SetPen(self._themeDict["penHover"])
                dc.SetBrush(self._themeDict["brushHover"])
                dc.SetTextForeground(self._themeDict["textForegroundHover"])
            else:
                dc.SetPen(self._themeDict["penDefault"])
                dc.SetBrush(self._themeDict["brushDefault"])
                dc.SetTextForeground(self._themeDict["textForegroundDefault"])
            
        # draw border    
        dc.DrawRoundedRectangle(rect, dip(6))

        # draw text (centered)
        textWidth, textHeight = dc.GetTextExtent(self.label)
        textX = rect.GetX() + (rect.GetWidth() // 2) - (textWidth // 2)
        textY = rect.GetY() + (rect.GetHeight() // 2) - (textHeight // 2)
        dc.DrawText(self.label, textX, textY)
        

    def OnEraseBackground(self, event) -> None:
        """ Bound to prevent flickering. """
        pass
    

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
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    
    class MyFrame(wx.Frame):
        
        def __init__(self):
            super().__init__(None, title="custom control test")
            panel = wx.Panel(self)
            panel.SetBackgroundColour(blueTheme["background"])

            # custom control
            self.button = customButton(panel, label="Click Me", pos=wx.Point(50, 50), size=wx.Size(300, 40), theme="blue")
            # native control
            wx.Button(panel, label="Click Me", pos=(50, 100), size=(300, 40)) 

            #self.Bind(wx.EVT_BUTTON, self.OnButtonClicked, self.button)
            self.Show()
            

        def OnButtonClicked(self, event) -> None:
            wx.MessageBox("Button clicked!", parent=self)
            

    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()
