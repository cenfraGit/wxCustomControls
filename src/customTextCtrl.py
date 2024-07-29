import wx
from .dip import dip
from .themes import lightTheme, blueTheme


class CustomTextCtrl(wx.Control):    
    """ Defines a custom text control that supports themes. """
    
    def __init__(self, parent, id=wx.ID_ANY, value:str="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.NO_BORDER|wx.WANTS_CHARS, validator=wx.DefaultValidator,
                 name="CustomTextCtrl", theme:str="light", fontSize=8):
        super().__init__(parent, id, pos, size, style, validator, name)

        # control attributes
        self._value = list(value.strip()) # a list of characters ['a', 'b', 'c']
        self._Theme = theme # light or dark
        self._Enabled = True
        self._fontSize = fontSize

        # state attributes
        self.mouseHover = False
        self._hasFocus = False
        self.cursorBlinkStatus = True
        self._cursorLocation = len(value)-1 if value.strip() != "" else 0
        
        # control appearance attributes
        self.leftPadding = dip(5)
        self.verticalPadding = dip(5)

        # initialize control colors
        self.initializeColors()

        # initial size
        self.SetInitialSize(size)

        # set up autobufferedpaintdc
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        # change mouse cursor
        self.SetCursor(wx.Cursor(wx.CURSOR_IBEAM))

        # set timer for blinking cursor
        self.timer = wx.Timer(self)
        self.timerBlinkMS = 600
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

        # bind control events
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        if (wx.Platform == "__WXMSW__"):
            self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)

        # control focus
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)

        # keyboard events
        #self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_CHAR, self.OnChar)
        
        
    def initializeColors(self) -> None:
        """ Initializes the button's colors according to theme. """
        
        if (self._Theme == "light"):
            self._themeDict = lightTheme
        elif (self._Theme == "blue"):
            self._themeDict = blueTheme
        else:
            # invalid theme
            self._themeDict = lightTheme


    def GetValue(self) -> str:
        """ Return the state of the control. """
        # convert list of characters to string
        return "".join(self._value)

        
    def SetValue(self, value: str) -> None:
        self._value = list(value)
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
        dc.DrawRectangle(rect)

        # set font and foreground color
        dc.SetFont(wx.Font(self._fontSize,
                           wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL,
                           faceName=self._themeDict["fontFaceName"]))
        dc.SetTextForeground(self._themeDict["textForegroundDefault"])

        # get max text height and vertical offset
        #_, maxTextHeight = dc.GetTextExtent("A")
        #verticalOffset = (((self.verticalPadding*2) + maxTextHeight) // 2) - (maxTextHeight//2) # ?

        # horizontal character offset (for each letter)
        horizontalOffset = self.leftPadding

        # draw border
        if not self._Enabled:
            dc.SetPen(wx.Pen(self._themeDict["penDisabled"], 1))
            dc.SetBrush(wx.Brush(self._themeDict["brushDisabled"]))
            dc.DrawRoundedRectangle(rect, 10)
            dc.SetTextForeground(self._themeDict["textForegroundDisabled"])
            textWidth, textHeight = dc.GetTextExtent(self.GetValue())
            dc.DrawText(self.GetValue(), horizontalOffset, (rect.GetHeight()//2 - (textHeight//2)))
            return

        if self._hasFocus:
            dc.SetPen(wx.Pen(self._themeDict["penHover"], 3))
            dc.SetBrush(wx.Brush(self._themeDict["brushDefault"], wx.BRUSHSTYLE_SOLID))
            #dc.DrawRoundedRectangle(rect, 10) # weird rounded corners
            dc.DrawRectangle(rect)
        elif self.mouseHover:
            dc.SetPen(wx.Pen(self._themeDict["penHover"], 1))
            dc.SetBrush(wx.Brush(self._themeDict["brushDefault"], wx.BRUSHSTYLE_SOLID))
            #dc.DrawRoundedRectangle(rect, 10)
            dc.DrawRectangle(rect)
        else:
            dc.SetPen(wx.Pen(self._themeDict["penDefault"], 1))
            dc.SetBrush(wx.Brush(self._themeDict["brushDefault"], wx.BRUSHSTYLE_SOLID))
            #dc.DrawRoundedRectangle(rect, 10)
            dc.DrawRectangle(rect)


        # draw text
        for index, character in enumerate(self._value):

            textWidth, textHeight = dc.GetTextExtent(character)

            textY =  (rect.GetHeight()//2 - (textHeight//2)) # the Y coordinate for the text
            dc.DrawText(character, horizontalOffset, textY)

            # draw caret
            if self._hasFocus and (self._cursorLocation == index) and self.cursorBlinkStatus:
                dc.SetPen(wx.Pen(self._themeDict["penPressed"], 2))
                dc.DrawLine(horizontalOffset, textY, horizontalOffset, textY + textHeight)
                
            


            horizontalOffset += textWidth


        """

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

        """

        
    def OnEraseBackground(self, event) -> None:
        """ Bound to prevent flickering. """
        pass


    def DoGetBestClientSize(self) -> wx.Size:
        """ Determines the best size for the control. """
        
        # create device context and set font to determine text dimensions
        dc = wx.ClientDC(self)
        
        # create font
        font = wx.Font(self._fontSize,
                       wx.FONTFAMILY_DEFAULT,
                       wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_NORMAL,
                       faceName=self._themeDict["fontFaceName"])
        dc.SetFont(font)


        # get text width and height
        textWidth, textHeight = dc.GetTextExtent(self.GetValue())

        # dimensions
        width = (self.leftPadding*2) + textWidth
        height = (self.verticalPadding*2) + textHeight

        return wx.Size(width, height)


        
    

    def OnLeftDown(self, event) -> None:
        """ Handler for when the control is clicked. """
        
        # invert status
        #self._state = not self._state
        # redraw

        self.Refresh()
        event.Skip()


    def OnLeftUp(self, event) -> None:
        """ ? """
        pass
            #self.Refresh()
            #wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.GetId()))
        event.Skip()


    def OnSetFocus(self, event):
        self._hasFocus = True
        self.timer.Start(self.timerBlinkMS)
        self.Refresh()


    def OnKillFocus(self, event):
        self._hasFocus = False
        self.timer.Stop()
        self.Refresh()


    def OnTimer(self, event):
        self.cursorBlinkStatus = not self.cursorBlinkStatus
        self.Refresh()
        

    def OnMouseLeave(self, event) -> None:
        self.mouseHover = False
        self.Refresh()
        event.Skip()
        

    def OnMouseEnter(self, event) -> None:
        self.mouseHover = True
        self.Refresh()
        event.Skip()

     
    def OnChar(self, event:wx.KeyEvent):
        """ Handles a character event (in order to move cursor or insert text). """
        
        # get character
        unicodeKey = event.GetUnicodeKey() # for characters
        specialKey = event.GetKeyCode()    # for arrow keys
        character = chr(unicodeKey)

        # ----------- SPECIAL KEYS -------------

        # check if left arrow
        if (specialKey == wx.WXK_LEFT):
            # move cursor to the left
            if (self._cursorLocation > 0):
                self._cursorLocation -= 1
            # draw cursor and reset timer
            self.timer.Stop()
            self.cursorBlinkStatus = True
            self.timer.Start(self.timerBlinkMS)
            # exit
            event.Skip()
            self.Refresh()
            return
        # check if right arrow
        elif (specialKey == wx.WXK_RIGHT):
            # move cursor to the left
            if (self._cursorLocation < len(self._value)):
                self._cursorLocation += 1
            # draw cursor and reset timer
            self.timer.Stop()
            self.cursorBlinkStatus = True
            self.timer.Start(self.timerBlinkMS)
            # exit
            event.Skip()
            self.Refresh()
            return
        # check if delete character
        elif (specialKey == wx.WXK_BACK):
            # delete character before cursor
            if self._cursorLocation > 0:
                self._value.pop(self._cursorLocation-1)
                self._cursorLocation -= 1
            # draw cursor and reset timer
            self.timer.Stop()
            self.cursorBlinkStatus = True
            self.timer.Start(self.timerBlinkMS)
            # exit
            event.Skip()
            self.Refresh()
            return
    


        # ----------- CHARACTERS -------------

        # draw character
        self._value.insert(self._cursorLocation, character)
        # move cursor to the right (along inserted character)
        self._cursorLocation += 1




        
        print("cursor location:", self._cursorLocation)
        event.Skip()
        self.Refresh()


        
    def AcceptsFocusFromKeyboard(self) -> bool:
        return False


    def AcceptsFocus(self):
        return True
        

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
