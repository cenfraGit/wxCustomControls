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
        """ The idea is to have a list that contains the characters of
        the input string as elements. We do this in order to easily
        insert, pop (remove at index) and slice characters according
        to user input, which will be handled by both keyboard and
        mouse events. This character list is stored in self._Value."""
        self._Value = list(value.strip())
        self._Theme = theme # light or dark
        self._fontSize = fontSize

        # control state
        self._mouseHover = False
        self._hasFocus = False
        self._cursorBlinkStatus = True
        #self._cursorLocation = len(value)-1 if value.strip() != "" else 0
        self._cursorLocation = 0
        #self._cursorX = 0 # x position
        self._Enabled = True

        # used to shift all text if needed by caret.
        self.stringOffset = 0
        
        # control padding and margins
        self.leftPadding = dip(5)
        self.verticalPadding = dip(5)

        # initialize theme dictionary
        self.initializeTheme()

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
        
        
    def initializeTheme(self) -> None:
        """Sets up the theme dictionary that will be used during the
        drawing process."""
        
        if (self._Theme == "light"):
            self._themeDict = lightTheme
        elif (self._Theme == "blue"):
            self._themeDict = blueTheme
        else:
            # invalid theme
            self._themeDict = lightTheme


    def GetValue(self) -> str:
        """ Returns the input text as a string. """
        return "".join(self._Value)

        
    def SetValue(self, value: str) -> None:
        """ Sets the control's text value. """
        self._Value = list(value)
        self.Refresh()
        

    def OnPaint(self, event) -> None:
        """ Handles the paint event. """        
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        self.Draw(dc)
        

    def Draw(self, dc: wx.AutoBufferedPaintDC) -> None:
        """ Draws the control. """

        """The plan is to draw each character of the input
        (self._Value) and save its position and dimensions data as a
        rectangle which will be used to check where the mouse click
        occurred so we can place the caret accordingly. Both the
        keyboard and mouse events will be handled in their respective
        methods, so this drawing method only concerns drawing the
        characters (plus saving their position/dimension data) and
        displaying the caret correctly.

        We also must take into account if the text is longer than the
        text box. We must always display the character at the index
        pointed at by the caret, so we might have to shift the text
        position when draing.

        The TextCtrl will not have support for emacs keybindings,
        unfortunately.
        """

        
        # first we get our working area
        controlAreaRect = self.GetClientRect()

        
        # we will get the background color of the parent and draw a
        # rectangle just in case (useful if rounded corners will be
        # used)
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour(),
                             wx.BRUSHSTYLE_SOLID))
        dc.DrawRectangle(controlAreaRect)

        
        # we set the font that will be used (using the font size and
        # the face name parameters)
        dc.SetFont(wx.Font(self._fontSize,
                           wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL,
                           faceName=self._themeDict["fontFaceName"]))

        
        # set the text color according to theme's default
        dc.SetTextForeground(self._themeDict["textForegroundDefault"])

        
        # we initialize horizontalOffset, which will be an accumulator
        # variable that saves the X position offset that each
        # character should have upon rendering. It starts with the
        # left padding value.
        horizontalOffset = self.leftPadding

        
        # if the control is not enabled, we draw the control with
        # 'disabled' colors and instead of drawing character by
        # character, we just draw the complete string (since we do not
        # need to save the character data because the user will not
        # have the ability to edit)
        if not self._Enabled:
            dc.SetPen(wx.Pen(self._themeDict["penDisabled"], 1))
            dc.SetBrush(wx.Brush(self._themeDict["brushDisabled"]))
            dc.SetTextForeground(self._themeDict["textForegroundDisabled"])
            dc.DrawRectangle(controlAreaRect)
            textWidth, textHeight = dc.GetTextExtent(self.GetValue())
            dc.DrawText(self.GetValue(), horizontalOffset, (controlAreaRect.GetHeight()//2 - (textHeight//2)))
            return # return because no further processing is needed

        
        # if we got here, it means that the control is enabled. we now
        # draw the text box according to the following states (in
        # order):
        # 1. we check if it has focus
        # 2. we check if the mouse is hovering
        # 3. if none of the above, draw with default colors
        if self._hasFocus:
            dc.SetPen(wx.Pen(self._themeDict["penHover"], 3))
            dc.SetBrush(wx.Brush(self._themeDict["brushDefault"], wx.BRUSHSTYLE_SOLID))
        elif self._mouseHover:
            dc.SetPen(wx.Pen(self._themeDict["penHover"], 1))
            dc.SetBrush(wx.Brush(self._themeDict["brushDefault"], wx.BRUSHSTYLE_SOLID))
        else:
            dc.SetPen(wx.Pen(self._themeDict["penDefault"], 1))
            dc.SetBrush(wx.Brush(self._themeDict["brushDefault"], wx.BRUSHSTYLE_SOLID))

            
        # we draw the rectangle with selected pen and brush
        dc.DrawRectangle(controlAreaRect)

        
        # now we draw the input characters. We first must check if the
        # entire string fits within the text box (in case the user
        # specified a smaller control size manually):
        # we get the entire string dimensions
        textWidth, textHeight = dc.GetTextExtent(self.GetValue())
        # we check if the string fits
        entireTextFits = textWidth < (controlAreaRect.GetWidth() - self.leftPadding*2)

        #print("fits", entireTextFits)

        # we will now choose a slice of characters that will be
        # drawn. If the text doesnt fit, the slice will be characters
        # that are close to the caret. If the text fits, the slice will be all characters.

        #dc.DrawText(self.GetValue(), horizontalOffset, 10)

        # first iterate through all characters and get their width, height and rectangle.
        # then, if caret is moving right and showing more characters, draw backwards?
        # if caret is moving left and showing, draw frontwards?

        # we will draw all characters, but shift the horizontal offset so that there is a 'movable window'

        # self.stringOffset
        


        # save character rectangles and dimensions: create list where
        # data will be stored. this list will keep the data once the
        # rendering is over, so the rectangle data can be analized
        # from the keyboard and mouse events
        self.characterRectangles = []
        for character in self._Value:
            # get width and height of the character
            textWidth, textHeight = dc.GetTextExtent(character)
            # append tuple at index
            self.characterRectangles.append(
                # append the character and its dimensions rectangle
                (character, wx.Rect(horizontalOffset,
                                    (controlAreaRect.GetHeight()//2 - (textHeight//2)),
                                    textWidth,
                                    textHeight)))
            # increase offset accumulator by character's width
            horizontalOffset += textWidth

            
        # NOTE: if the cursorLocation is 3, its location will be
        # before 2 and 3. Meaning, it points to the character before
        # the third character in the self.characterRectangles list.

        
        # draw characters, each with the string offset
        for character, rectangle in self.characterRectangles:
            dc.DrawText(character, rectangle.GetX() + self.stringOffset, rectangle.GetY())

        # ------------------- DRAW CARET --------------------
        
        # _caretX: the X coordinate of the beginning of the character
        # (meaning it points to the previous character)
        #if list is not empty, use cursor location
        if self.characterRectangles:
            # if the cursor (caret) location is pointing at the end of 
            if (self._cursorLocation == len(self.characterRectangles)):
                # if the caret is at the end of the string, since the
                # caret always gets the x coordinate of the left side
                # of the next rectangle (since it is usually between
                # two characters, or rectangles), this time it will
                # take the right side X coordinate of the character's
                # rectangle before itself.
                self._caretX = self.characterRectangles[self._cursorLocation-1][1].GetTopRight()[0]
                print("new", self.characterRectangles[self._cursorLocation-1])
            else:
                self._caretX = self.characterRectangles[self._cursorLocation][1].GetX()
        # else, just draw at poisition 0
        else:
            self._caretX = self.leftPadding
        # draw caret considering string offset
        dc.SetPen(wx.Pen(self._themeDict["penDefault"], 1))
        dc.DrawLine(self._caretX+self.stringOffset,
                    self.verticalPadding,
                    self._caretX+self.stringOffset,
                    self.verticalPadding+textHeight)



        """
        
        for index, character in enumerate(self._Value):

            textWidth, textHeight = dc.GetTextExtent(character)

            textY =  (rect.GetHeight()//2 - (textHeight//2)) # the Y coordinate for the text
            dc.DrawText(character, horizontalOffset, textY)

            # draw caret
            if self._hasFocus and (self._cursorLocation == index) and self._cursorBlinkStatus:
                dc.SetPen(wx.Pen(self._themeDict["penPressed"], 2))
                dc.DrawLine(horizontalOffset, textY, horizontalOffset, textY + textHeight)
                
            


            horizontalOffset += textWidth

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
        self._cursorBlinkStatus = not self._cursorBlinkStatus
        self.Refresh()
        

    def OnMouseLeave(self, event) -> None:
        self._mouseHover = False
        self.Refresh()
        event.Skip()
        

    def OnMouseEnter(self, event) -> None:
        self._mouseHover = True
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

            # the caretX will be out of bounds if its less than 0, so
            # no variable is declared
            caretXAbsolute = self._caretX + self.stringOffset - self.leftPadding
            # if its out of bounds to the left (we do not want the
            # cursor moving more than the left padding)
            if (caretXAbsolute < self.leftPadding):
                self.stringOffset += self.characterRectangles[self._cursorLocation][1].GetWidth()

            #print(caretXAbsolute)
            print(self._cursorLocation)

                
            # draw cursor and reset timer
            self.timer.Stop()
            self._cursorBlinkStatus = True
            self.timer.Start(self.timerBlinkMS)
            
            # exit
            event.Skip()
            self.Refresh()
            return
        
        # check if right arrow
        elif (specialKey == wx.WXK_RIGHT):

            # move cursor to the left
            if (self._cursorLocation < len(self._Value)):
                self._cursorLocation += 1

            # check if out of bounds (to the right side)
            clientRightX = self.GetClientRect().GetTopRight()[0]
            widthTraveled = self.characterRectangles[self._cursorLocation-1][1].GetWidth()
            caretXAbsolute = self._caretX + self.stringOffset + widthTraveled
            if (caretXAbsolute > clientRightX-self.leftPadding):
                self.stringOffset -= widthTraveled


            print(self._cursorLocation)
            
            # draw cursor and reset timer
            self.timer.Stop()
            self._cursorBlinkStatus = True
            self.timer.Start(self.timerBlinkMS)

            # exit
            event.Skip()
            self.Refresh()
            return
        
        # check if delete character
        elif (specialKey == wx.WXK_BACK):
            # delete character before cursor
            if self._cursorLocation > 0:
                self._Value.pop(self._cursorLocation-1)
                self._cursorLocation -= 1
            # draw cursor and reset timer
            self.timer.Stop()
            self._cursorBlinkStatus = True
            self.timer.Start(self.timerBlinkMS)
            # exit
            event.Skip()
            self.Refresh()
            return
    


        # ----------- CHARACTERS -------------

        # draw character
        self._Value.insert(self._cursorLocation, character)
        # move cursor to the right (along inserted character)
        self._cursorLocation += 1

        # check if out of bounds
        clientWidth = self.GetClientRect().GetWidth()
        if (self._caretX > clientWidth - (2*self.leftPadding)):
            self.stringOffset -= self.characterRectangles[self._cursorLocation][1].GetWidth()




        
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
