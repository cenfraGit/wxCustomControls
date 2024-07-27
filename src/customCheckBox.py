import wx
from dip import dip
from themeColors import lightTheme, blueTheme


class CustomCheckBox(wx.Control):
    
    """ Defines a custom checkbox control that supports themes. """
    
    def __init__(self, parent, id=wx.ID_ANY, label:str="", state=False, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.NO_BORDER, validator=wx.DefaultValidator,
                 name="CustomCheckBox", theme:str="light"):
        super().__init__(parent, id, pos, size, style, validator, name)

        # control attributes
        self._label = label
        self._Theme = theme # light or dark
        self._Enabled = True

        # state attributes
        self._state = state # the actual state of the checkbutton
        self.mouseHover = False

        # initialize control colors
        self.initializeColors()

        # set up attributes
        self.setUpControlAttributes()
        
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
        """ Initializes the button's colors according to theme. """
        
        if (self._Theme == "light"):
            self._themeDict = lightTheme
        elif (self._Theme == "blue"):
            self._themeDict = blueTheme
        else:
            # invalid theme
            self._themeDict = lightTheme


    def GetValue(self):
        """ Return the state of the checkbox. """
        return self._state

        
    def SetValue(self, state: bool):
        self._state = state
        self.Refresh()


    def SetLabel(self, label):
        self._label = label
        self.Refresh()
        

    def OnPaint(self, event):
        """ Handles the paint event. """        
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        self.Draw(dc)


    def paintFirstTimeToDetermineDimensions(self):
        """ Paints the control one time to get text dimensions """
        #dc = wx.AutoBufferedPaintDC(self)
        
        #dc.SetFont()


    def setUpControlAttributes(self):
        """ Control appearance attributes used in the drawing loop. """
        self.checkBoxLeftMargin = dip(5)
        self.checkBoxTopMargin = dip(5)
        self.checkBoxSquareSize = dip(15)
        

    def Draw(self, dc: wx.AutoBufferedPaintDC):
        """ Draw the control. """
        
        rect = self.GetClientRect()

        # make backgrund transparent
        dc.SetPen(wx.TRANSPARENT_PEN)
        #dc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour(), wx.BRUSHSTYLE_SOLID))
        dc.SetBrush(wx.Brush(wx.GREEN))
        dc.DrawRectangle(rect)

        #if not self._Enabled:

        dc.SetPen(wx.Pen(self._themeDict["penDefault"], width=1))
        dc.SetBrush(wx.Brush(self._themeDict["brushDefault"], wx.BRUSHSTYLE_SOLID))
        dc.DrawRectangle(self.checkBoxLeftMargin, self.checkBoxTopMargin, self.checkBoxSquareSize, self.checkBoxSquareSize)

        dc.DrawText(self._label, self.checkBoxLeftMargin*2+self.checkBoxSquareSize, 0)

        if self._state:
            dc.SetPen(wx.Pen(self._themeDict["penPressed"], 1))
            dc.SetBrush(wx.Brush(self._themeDict["brushPressed"]))
            dc.DrawRectangle(self.checkBoxLeftMargin, self.checkBoxTopMargin, self.checkBoxSquareSize, self.checkBoxSquareSize)

            


        """
        
        # check if control is enabled
        # if not, check if pressed
        # if not, check if mouse is hovering
        # if not, draw with default colors

        if not self._Enabled:
            dc.SetPen(wx.Pen(self._themeDict["penDisabled"], 1))
            dc.SetBrush(wx.Brush(self._themeDict["brushDisabled"], wx.BRUSHSTYLE_SOLID))
            dc.SetTextForeground(self._themeDict["textForegroundDisabled"])
        else:
            dc.SetPen(wx.Pen(self._themeDict["penDefault"], 1))
            dc.SetBrush(wx.Brush(self._themeDict["brushDefault"], wx.BRUSHSTYLE_SOLID))
            dc.SetTextForeground(self._themeDict["textForegroundDefault"])
            
        # draw border
        dc.DrawRectangle(rect)

        # draw text (to the left)
        leftMargin = dip(10)
        dc.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        textWidth, textHeight = dc.GetTextExtent(self._value)
        textX = leftMargin
        textY = rect.GetY() + (rect.GetHeight() // 2) - (textHeight // 2)
        dc.DrawText(self._value, textX, textY)
        
        # draw drop down arrow
        rightMargin = dip(6)
        width, height = dip(10), dip(4)
        rectPosX = rect.GetWidth() - width - rightMargin
        rectPosY = (rect.GetHeight() // 2) - (height // 2)
        # define icon area
        arrowRectangle = wx.Rect(rectPosX, rectPosY, width, height)
        dc.SetPen(wx.Pen(self._themeDict["textForegroundDefault"], 1, wx.PENSTYLE_SOLID))
        dc.DrawLine(rectPosX+1, rectPosY, rectPosX+(width//2), rectPosY+height)
        dc.DrawLine(rectPosX+(width//2), rectPosY+height, arrowRectangle.GetTopRight()[0], arrowRectangle.GetTopRight()[1]-1)
        """

        
    def OnEraseBackground(self, event):
        """ Bound to prevent flickering. """
        pass
    

    def OnLeftDown(self, event):
        """ Handler for when the checkbox is clicked. """
        
        # invert status
        self._state = not self._state
        # redraw
        self.Refresh()
        event.Skip()


    def OnLeftUp(self, event):
        """ ? """
        if self._state:
            pass
            #self.Refresh()
            #wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.GetId()))
        event.Skip()
        

    def OnMouseLeave(self, event):
        self.mouseHover = False
        self.Refresh()
        event.Skip()
        

    def OnMouseEnter(self, event):
        self.mouseHover = True
        self.Refresh()
        event.Skip()
        

    def Enable(self, enable=True):
        """
        Uses _Enable to define if the widget is enabled or not,
        instead of default behavior (problems redrawing after modal
        dialogs).
        """
        self._Enabled = enable
        super().Enable(enable)
        self.Refresh()
        

    def Disable(self):
        self.Enable(False)

        

        


# for testing control directly
if __name__ == "__main__":

    #from customButton import CustomButton
    if (wx.Platform == "__WXMSW__"):
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    
    class MyFrame(wx.Frame):
        def __init__(self):
            super().__init__(None, title="control test")
            self.SetMinClientSize(dip(400, 400))

            theme = "light"
            
            panel = wx.Panel(self)
            panel.SetBackgroundColour(lightTheme["background"] if theme=="light" else blueTheme["background"])

            self.control = CustomCheckBox(panel, label="testing", state=False, pos=wx.Point(50, 50), size=wx.Size(200, 40), theme=theme)



            #self.btn = CustomButton(panel, label="Print value", pos=wx.Point(300, 50), size=wx.Size(140, 40), theme="blue")
            #self.btn.Bind(wx.EVT_BUTTON, lambda e: print(self.choice.GetValue()))
            

            self.Show()

            

    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()
