import wx
from dip import dip
from themes import lightTheme, blueTheme


class ChoicesPanel(wx.Panel):

    """ Defines a panel that represents the drop down menu containing
    the choices in the cChoice control. """

    def __init__(self, reference, choices:list=[], theme:str="light", *args, **kwargs):
        super().__init__(*args, **kwargs)

        #self.Raise()

        # attributse
        self._Choices = choices
        self._Theme = theme
        self._Reference = reference

        # dictionary where choice rectangles area are saved (for
        # checking user clicks)
        self.choiceRectangles = {}

        # set up buffered paint dc
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        # init colors
        self.InitializeColors()
        self.SetBackgroundColour(self._themeDict["brushDefault"])

        # used for when drawing in case the mouse is hovering
        self.choiceBackgroundColors = [self._themeDict["brushDefault"] for _ in self._Choices]

        # bind events
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)

        
    def InitializeColors(self):

        if (self._Theme == "light"):
            self._themeDict = lightTheme
        elif (self._Theme == "blue"):
            self._themeDict = blueTheme
        else:
            # invalid theme
            self._themeDict = lightTheme
            

    def OnPaint(self, event):
        """ Handles the paint event. """
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        self.Draw(dc)
        

    def Draw(self, dc: wx.AutoBufferedPaintDC):

        # set choices font
        dc.SetTextForeground(self._themeDict["textForegroundDefault"])
        dc.SetFont(wx.Font(self._Reference._fontSize,
                           wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL, False, self._themeDict["fontFaceName"]))

        # reset rectangles?
        self.choiceRectangles = {}

        workingAreaRect = self.GetClientRect()
 
        # rectangle height
        rectangleHeight = dip(35)

        # left text offset
        leftMargin = dip(14)

        # variable for tracking Y position for drawing (with initial
        # offset)
        verticalOffset = 0


        for index, choice in enumerate(self._Choices):

            # get rectangle area
            rect = wx.Rect(0, verticalOffset, workingAreaRect.GetWidth(), rectangleHeight)

            # save rectangle to dictionary
            self.choiceRectangles[choice] = rect

            # draw color
            dc.SetPen(wx.TRANSPARENT_PEN)
            dc.SetBrush(wx.Brush(colour=self.choiceBackgroundColors[index], style=wx.BRUSHSTYLE_SOLID))
            dc.DrawRectangle(rect)
            
            # draw choice
            _, textHeight = dc.GetTextExtent(choice)
            dc.DrawText(choice, leftMargin, verticalOffset + (rectangleHeight//2) - (textHeight//2))

            # offset
            verticalOffset += rectangleHeight

            if (index == len(self._Choices)-1):
                break
            
        # draw borders
        dc.SetPen(wx.Pen(self._themeDict["penDefault"], 1, wx.PENSTYLE_SOLID))
        # left line
        dc.DrawLine(0, 0, 0, verticalOffset)
        # right line
        dc.DrawLine(self._Reference.GetClientSize()[0]-1, 0, self._Reference.GetClientSize()[0]-1, verticalOffset)
        # bottom line
        dc.DrawLine(0, verticalOffset-1, self._Reference.GetClientSize()[0]-1, verticalOffset-1)
            
        # modify drop down menu size
        self.SetClientSize(self._Reference.GetClientSize()[0], verticalOffset)
            
        
    def OnLeftDown(self, event:wx.MouseEvent):
        """ Checks what choice was clicked by the user. """

        x, y = event.GetPosition()

        # check which choice's rectangle was clicked
        for choice, rectangle in self.choiceRectangles.items():

            if rectangle.Contains(x, y):

                # not good
                self._Reference._value = choice
                self._Reference.Refresh()
                self._Reference.pressed = False
                # close drop down menu
                self.Destroy()


    def OnMouseMotion(self, event:wx.MouseEvent):
        """Changes color of selection when the mouse hovers the
        choice option."""

        print(event.GetPosition())

        # reset colors
        self.choiceBackgroundColors = [self._themeDict["brushDefault"] for _ in self._Choices]
        
        x, y = event.GetPosition()

        for index, pair in enumerate(self.choiceRectangles.items()):

            # if rectangle (second key) contains cursor coords
            if pair[1].Contains(x, y):

                # change color (applied when drawn)
                self.choiceBackgroundColors[index] = self._themeDict["brushPressed"]

        self.Refresh()

    
            

class CustomChoice(wx.Control):    
    """ Defines a custom choice control that supports themes. """
    
    def __init__(self, parent, id=wx.ID_ANY, value:str="", choices:list=[], pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.NO_BORDER, validator=wx.DefaultValidator,
                 name="CustomChoice", theme:str="light", fontSize=8):
        super().__init__(parent, id, pos, size, style, validator, name)

        # control attributes
        self._value = value
        self._choices = choices
        self._Theme = theme # light or dark
        self._Enabled = True
        self._fontSize = fontSize

        # appearance
        self.leftMargin = dip(10)
        self.topBottomMargins = dip(5)

        self.rightArrowMargin = dip(7)
        self.arrowWidth, self.arrowHeight = dip(10), dip(3)

        # state attributes
        self.pressed = False
        self.mouseHover = False

        # initialize control colors
        self.initializeColors()

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
        return self._value

        
    def SetValue(self, value):
        self._value = value
        self.Refresh()
        

    def OnPaint(self, event):
        """ Handles the paint event. """
        
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        self.Draw(dc)
        

    def Draw(self, dc: wx.AutoBufferedPaintDC):
        """ Draw the actual button. """
        
        rect = self.GetClientRect()

        # make backgrund transparent
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour(), wx.BRUSHSTYLE_SOLID))
        dc.DrawRectangle(rect)
        
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
        dc.SetFont(wx.Font(self._fontSize, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        textWidth, textHeight = dc.GetTextExtent(self._value)
        textX = self.leftMargin
        textY = rect.GetY() + (rect.GetHeight() // 2) - (textHeight // 2)
        dc.DrawText(self._value, textX, textY)
        
        # draw drop down arrow
        rectPosX = rect.GetWidth() - self.arrowWidth - self.rightArrowMargin
        rectPosY = (rect.GetHeight() // 2) - (self.arrowHeight // 2)
        # define icon area
        arrowRectangle = wx.Rect(rectPosX, rectPosY, self.arrowWidth, self.arrowHeight)
        dc.SetPen(wx.Pen(self._themeDict["textForegroundDefault"], 2, wx.PENSTYLE_SOLID))        
        dc.DrawLine(rectPosX, rectPosY, rectPosX+(self.arrowWidth//2), rectPosY+self.arrowHeight)
        dc.DrawLine(rectPosX+(self.arrowWidth//2), rectPosY+self.arrowHeight, arrowRectangle.GetTopRight()[0], arrowRectangle.GetTopRight()[1])

        
    def OnEraseBackground(self, event):
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

        # the witdh of the control will be the width of the longest
        # string in the choices list.

        maxWidth = 0
        maxHeight = 0

        for choice in self._choices:
            # get dimensions
            textWidth, textHeight = dc.GetTextExtent(choice)
            # replace values
            maxWidth = textWidth if (textWidth > maxWidth) else maxWidth
            maxHeight = textHeight if (textHeight > maxHeight) else maxHeight        

        # final control dimensions
        width = self.leftMargin + maxWidth + (self.rightArrowMargin*3)
        height = self.topBottomMargins*2 + maxHeight
        return wx.Size(width, height)
    

    def OnLeftDown(self, event):

        # invert status
        self.pressed = not self.pressed

        if self.pressed:
            # open choices panel
            self.createChoicesPanel()
        else:
            # destroy choices panel
            try:
                self.destroyChoicesPanel()
            except:
                pass
        
        self.Refresh()
        event.Skip()


    def OnLeftUp(self, event):
        if self.pressed:
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


    def createChoicesPanel(self):
        
        """ Creates and displays the drop down menu that displays the choices. """

        # return if choices list is empty
        if len(self._choices) == 0:
            return

        rect = self.GetClientRect()

        # get choice position to place panel beneath it
        controlPosition = self.GetPosition()

        self.choicesPanel = ChoicesPanel(parent=self.GetParent(),
                                         choices=self._choices,
                                         theme=self._Theme,
                                         reference=self,
                                         pos=(controlPosition[0], controlPosition[1]+rect.GetHeight())
                                         )
        
        
        #self.GetParent().Refresh()


    def destroyChoicesPanel(self):
        """ Destroys the existing reference to the choices panel. """
        self.choicesPanel.Destroy()
        self.GetParent().Refresh()

    

        

        


# for testing control directly
if __name__ == "__main__":

    from customButton import CustomButton
    if (wx.Platform == "__WXMSW__"):
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    
    class MyFrame(wx.Frame):
        def __init__(self):
            super().__init__(None, title="control test")
            self.SetMinClientSize(dip(400, 400))
            
            panel = wx.Panel(self)
            panel.SetBackgroundColour(blueTheme["background"])


            values = ["test1", "car1", "car2", "computer", "messageboxtext"]
            self.choice = CustomChoice(panel, choices=values, value="computer", pos=wx.Point(50, 50), theme="blue")
            #self.choice.Disable()

            wx.StaticText(panel, label="placeholder", pos=(55, 100))
            wx.StaticText(panel, label="placeholder", pos=(55, 150))


            self.btn = CustomButton(panel, label="Print value", pos=wx.Point(300, 50), theme="blue")

            self.btn.Bind(wx.EVT_BUTTON, lambda e: print(self.choice.GetValue()))
            

            self.Show()

            

    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()
