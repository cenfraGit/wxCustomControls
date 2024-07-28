import wx
if __name__ == "__main__":
    from dip import dip
    from themes import lightTheme, blueTheme
else:
    from .dip import dip
    from .themes import lightTheme, blueTheme


class CustomCheckBox(wx.Control):    
    """ Defines a custom checkbox control that supports themes. """
    
    def __init__(self, parent, id=wx.ID_ANY, label:str="", state=False, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.NO_BORDER, validator=wx.DefaultValidator,
                 name="CustomCheckBox", theme:str="light", fontSize=8):
        super().__init__(parent, id, pos, size, style, validator, name)

        # control attributes
        self._label = label
        self._Theme = theme # light or dark
        self._Enabled = True
        self._fontSize = fontSize

        # state attributes
        self._state = state # the actual state of the checkbutton
        self.mouseHover = False
        
        # control appearance attributes
        self.checkBoxLeftMargin = dip(5)
        self.checkBoxTopMargin = dip(5)
        self.checkBoxSquareSize = dip(15)
        self.checkBoxSquareSelectedSize = dip(10)

        # initialize control colors
        self.initializeColors()

        # initial size
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
        
        
    def initializeColors(self) -> None:
        """ Initializes the button's colors according to theme. """
        
        if (self._Theme == "light"):
            self._themeDict = lightTheme
        elif (self._Theme == "blue"):
            self._themeDict = blueTheme
        else:
            # invalid theme
            self._themeDict = lightTheme


    def GetValue(self) -> None:
        """ Return the state of the checkbox. """
        return self._state

        
    def SetValue(self, state: bool) -> None:
        self._state = state
        self.Refresh()


    def SetLabel(self, label) -> None:
        self._label = label
        self.Refresh()
        

    def OnPaint(self, event) -> None:
        """ Handles the paint event. """        
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        self.Draw(dc)
        

    def Draw(self, dc: wx.AutoBufferedPaintDC):
        """ Draw the control. """
        
        rect = self.GetClientRect()

        # make backgrund transparent
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour(), wx.BRUSHSTYLE_SOLID))
        #dc.SetBrush(wx.Brush(wx.GREEN))
        dc.DrawRectangle(rect)

        # set font
        dc.SetFont(wx.Font(self._fontSize,
                           wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL,
                           faceName=self._themeDict["fontFaceName"]))
        dc.SetTextForeground(self._themeDict["textForegroundDefault"])

        #if not self._Enabled:

        if not self._Enabled:
            # draw checkbox
            dc.SetPen(wx.Pen(self._themeDict["penDisabled"], width=1))
            dc.SetBrush(wx.Brush(self._themeDict["brushDisabled"], wx.BRUSHSTYLE_SOLID))
            dc.DrawRectangle(self.checkBoxLeftMargin, self.checkBoxTopMargin, self.checkBoxSquareSize, self.checkBoxSquareSize)
            # draw label
            _, textHeight = dc.GetTextExtent(self._label)
            textX = self.checkBoxLeftMargin*2 + self.checkBoxSquareSize
            textY = (rect.GetHeight() // 2) - (textHeight//2)
            dc.SetTextForeground(self._themeDict["textForegroundDisabled"])
            dc.DrawText(self._label, textX, textY)

            if self._state:
                dc.SetPen(wx.Pen(self._themeDict["penDisabled"], 1))
                dc.SetBrush(wx.Brush(self._themeDict["brushDisabled"]))
                # create offsets so that rect is centered
                leftOffset = self.checkBoxLeftMargin + ((self.checkBoxSquareSize - self.checkBoxSquareSelectedSize) // 2)
                topOffset = self.checkBoxTopMargin + ((self.checkBoxSquareSize - self.checkBoxSquareSelectedSize) // 2)
                selectionRect = wx.Rect(leftOffset, topOffset, self.checkBoxSquareSelectedSize, self.checkBoxSquareSelectedSize)
                dc.DrawRectangle(selectionRect)

        else:
            

            dc.SetPen(wx.Pen(self._themeDict["penDefault"], width=1))
            dc.SetBrush(wx.Brush(self._themeDict["brushDefault"], wx.BRUSHSTYLE_SOLID))
            dc.DrawRectangle(self.checkBoxLeftMargin, self.checkBoxTopMargin, self.checkBoxSquareSize, self.checkBoxSquareSize)

            # draw label
            _, textHeight = dc.GetTextExtent(self._label)
            textX = self.checkBoxLeftMargin*2 + self.checkBoxSquareSize
            textY = (rect.GetHeight() // 2) - (textHeight//2)
            dc.DrawText(self._label, textX, textY)

            # draw selector
            
            if self.mouseHover:

                # if user is about to select
                if not self._state:
                    dc.SetPen(wx.Pen(self._themeDict["penHover"], 1))
                    dc.SetBrush(wx.Brush(self._themeDict["brushHover"]))
                    # create offsets so that rect is centered
                    leftOffset = self.checkBoxLeftMargin + ((self.checkBoxSquareSize - self.checkBoxSquareSelectedSize) // 2)
                    topOffset = self.checkBoxTopMargin + ((self.checkBoxSquareSize - self.checkBoxSquareSelectedSize) // 2)
                    selectionRect = wx.Rect(leftOffset, topOffset, self.checkBoxSquareSelectedSize, self.checkBoxSquareSelectedSize)
                    dc.DrawRectangle(selectionRect)

                # if user is about to de-select
                else: 
                    dc.SetPen(wx.Pen(self._themeDict["penPressed"], 1))
                    dc.SetBrush(wx.Brush(self._themeDict["penPressed"]))
                    # create offsets so that rect is centered
                    leftOffset = self.checkBoxLeftMargin + ((self.checkBoxSquareSize - self.checkBoxSquareSelectedSize) // 2)
                    topOffset = self.checkBoxTopMargin + ((self.checkBoxSquareSize - self.checkBoxSquareSelectedSize) // 2)
                    selectionRect = wx.Rect(leftOffset, topOffset, self.checkBoxSquareSelectedSize, self.checkBoxSquareSelectedSize)
                    dc.DrawRectangle(selectionRect)
                    
                
            else:

                if self._state:
                    
                    dc.SetPen(wx.Pen(self._themeDict["penPressed"], 1))
                    dc.SetBrush(wx.Brush(self._themeDict["brushPressed"]))
                    # create offsets so that rect is centered
                    leftOffset = self.checkBoxLeftMargin + ((self.checkBoxSquareSize - self.checkBoxSquareSelectedSize) // 2)
                    topOffset = self.checkBoxTopMargin + ((self.checkBoxSquareSize - self.checkBoxSquareSelectedSize) // 2)
                    selectionRect = wx.Rect(leftOffset, topOffset, self.checkBoxSquareSelectedSize, self.checkBoxSquareSelectedSize)
                    dc.DrawRectangle(selectionRect)

        
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

        # get text width and height
        dc.SetFont(font)
        textWidth, textHeight = dc.GetTextExtent(self._label)

        # dimensions
        width = (self.checkBoxLeftMargin*2) + self.checkBoxSquareSize + textWidth + dip(5)
        height = (self.checkBoxTopMargin*2) + max(self.checkBoxSquareSize, textHeight)

        return wx.Size(width, height)    
    

    def OnLeftDown(self, event) -> None:
        """ Handler for when the checkbox is clicked. """
        
        # invert status
        self._state = not self._state
        # redraw
        self.Refresh()
        event.Skip()


    def OnLeftUp(self, event) -> None:
        """ ? """
        if self._state:
            pass
            #self.Refresh()
            #wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.GetId()))
        event.Skip()
        

    def OnMouseLeave(self, event) -> None:
        self.mouseHover = False
        self.Refresh()
        event.Skip()
        

    def OnMouseEnter(self, event) -> None:
        self.mouseHover = True
        self.Refresh()
        event.Skip()
        

    def Enable(self, enable=True) -> None:
        """
        Uses _Enable to define if the widget is enabled or not,
        instead of default behavior (problems redrawing after modal
        dialogs).
        """
        self._Enabled = enable
        super().Enable(enable)
        self.Refresh()
        

    def Disable(self) -> None:
        self.Enable(False)

        

        


# for testing control directly
if __name__ == "__main__":

    #from customButton import CustomButton
    if (wx.Platform == "__WXMSW__"):
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    from customButton import CustomButton
    
    class MyFrame(wx.Frame):
        def __init__(self):
            super().__init__(None, title="control test")
            self.SetMinClientSize(dip(400, 400))

            theme = "light"
            
            panel = wx.Panel(self)
            panel.SetBackgroundColour(lightTheme["background"] if theme=="light" else blueTheme["background"])

            self.control = CustomCheckBox(panel, label="testing", state=False, pos=wx.Point(50, 50), theme=theme)
            #self.control.Disable()

            self.btn = CustomButton(panel, label="Print state", pos=wx.Point(300, 50), size=wx.Size(140, 40), theme=theme)
            self.btn.Bind(wx.EVT_BUTTON, lambda e: print(self.control.GetValue()))
            

            self.Show()

            

    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()
