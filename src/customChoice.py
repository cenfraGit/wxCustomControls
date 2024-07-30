import wx
from .functions.rgb import rgb
from .functions.getThemeDict import getThemeDict
from .functions.dip import dip


class ChoicesPanel(wx.Panel):
    """ Defines a panel that represents the drop down menu containing
    the choices in the cChoice control. """

    def __init__(self, reference, choices:list=[],
                 size=wx.DefaultSize, theme:str="lightTheme", *args,
                 **kwargs):
        super().__init__(*args, **kwargs)

        # -------------- ATTRIBUTES --------------

        self._Choices = choices
        self._Theme = theme
        self._ThemeDict = {}
        self._Reference = reference

        # dictionary where choice rectangles area are saved (for
        # checking user clicks)
        self.choiceRectangles = {}

        # -------------- APPEARANCE --------------

        self._PaddingVerticalRectangle = dip(7)
        self._PaddingHorizontal = dip(14)

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.setTheme(self._Theme)
        self.SetInitialSize(size)

        self.SetBackgroundColour(rgb(self._ThemeDict["brushDefault"]))

        # used for when drawing in case the mouse is hovering
        self.choiceBackgroundColors = [rgb(self._ThemeDict["brushDefault"]) for _ in self._Choices]

        # -------------- EVENTS --------------

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)

        
    def setTheme(self, themeString:str) -> None:
        """Sets the theme. If the theme is not valid, the first
        available theme will be chosen. Or if we definitely didnt find
        a theme, the rgb color will automatically display a random
        color.
        """
        
        # the getThemeDict returns the state of the operation and the
        # theme dictionary. we do not need the state right now.
        _, self._ThemeDict = getThemeDict(themeString)

        # refresh with changes
        self.Refresh()
            

    def OnPaint(self, event):
        """ Handles the paint event. """
        
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        self.Draw(dc)
        

    def Draw(self, dc:wx.AutoBufferedPaintDC):

        # set choices font
        dc.SetTextForeground(rgb(self._ThemeDict["textForegroundDefault"]))
        dc.SetFont(wx.Font(self._Reference._FontSize,
                           wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL,
                           faceName=self._Reference._FaceName))

        # reset rectangles?
        self.choiceRectangles = {}

        # get control rect
        workingAreaRect = self.GetClientRect()
 
        # rectangle height
        textWidth, textHeight = dc.GetTextExtent("A")
        rectangleHeight = 2 * self._PaddingVerticalRectangle + textHeight


        # variable for tracking Y position for drawing (with initial
        # offset)
        verticalOffset = 0


        for index, choice in enumerate(self._Choices):

            # get rectangle area
            rect = wx.Rect(0, verticalOffset, workingAreaRect.GetWidth(), rectangleHeight)
            #rect = wx.Rect(0, verticalOffset, workingAreaRect.GetWidth(), textHeight+(2*rectangleVerticalMargins))

            # save rectangle to dictionary
            self.choiceRectangles[choice] = rect

            # draw color
            dc.SetPen(wx.TRANSPARENT_PEN)
            dc.SetBrush(wx.Brush(colour=self.choiceBackgroundColors[index], style=wx.BRUSHSTYLE_SOLID))
            dc.DrawRectangle(rect)
            
            # draw choice
            _, textHeight = dc.GetTextExtent(choice)
            dc.DrawText(choice, self._PaddingHorizontal, verticalOffset + (rectangleHeight//2) - (textHeight//2))

            # offset
            verticalOffset += rectangleHeight

            if (index == len(self._Choices)-1):
                break
            
        # draw borders
        dc.SetPen(wx.Pen(self._ThemeDict["penDefault"], 1, wx.PENSTYLE_SOLID))
        # left line
        dc.DrawLine(0, 0, 0, verticalOffset)
        # right line
        dc.DrawLine(self._Reference.GetClientSize()[0]-1, 0, self._Reference.GetClientSize()[0]-1, verticalOffset)
        # bottom line
        dc.DrawLine(0, verticalOffset-1, self._Reference.GetClientSize()[0]-1, verticalOffset-1)
            
        # update size in case the reference changed sizes
        self.SetClientSize(self._Reference.GetClientSize()[0], verticalOffset)
            
        
    def OnLeftDown(self, event:wx.MouseEvent):
        """ Checks what choice was clicked by the user. """

        x, y = event.GetPosition()

        # check which choice's rectangle was clicked
        for choice, rectangle in self.choiceRectangles.items():

            if rectangle.Contains(x, y):

                #self._Reference._Value = choice
                self._Reference.SetValue(choice)
                self._Reference.Refresh()
                self._Reference._Pressed = False
                # post choice event
                wx.PostEvent(self._Reference, wx.PyCommandEvent(wx.EVT_CHOICE.typeId, self._Reference.GetId()))
                # close drop down menu
                self.Destroy()


    def OnMouseMotion(self, event:wx.MouseEvent):
        """Changes color of selection when the mouse hovers the
        choice option."""

        # reset colors
        self.choiceBackgroundColors = [rgb(self._ThemeDict["brushDefault"]) for _ in self._Choices]
        
        x, y = event.GetPosition()

        for index, pair in enumerate(self.choiceRectangles.items()):

            # if rectangle (second key) contains cursor coords
            if pair[1].Contains(x, y):

                # change color (applied when drawn)
                self.choiceBackgroundColors[index] = rgb(self._ThemeDict["brushPressed"])

        # make sure panel is in front
        self.Raise()
        self.Refresh()


    def DoGetBestClientSize(self) -> wx.Size:
        """ Determines the best size for the control. """

        # create dc and font to measure text extents
        dc = wx.ClientDC(self)
        dc.SetFont(wx.Font(self._Reference._FontSize,
                           wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL,
                           faceName=self._Reference._FaceName))

        # the width will be the same as the choices control
        width = self._Reference.GetClientRect().GetWidth()

        # for the height, we must get one rectangle's height and then
        # multiply it by the amount of choices there are, assuming
        # that the textHeight will be the same for all strings

        # first we get the height from an arbitrary character
        _, textHeight = dc.GetTextExtent("A")
        # then we calculate the height for a single rectangle
        rectangleHeight = 2 * self._PaddingVerticalRectangle + textHeight
        # then we calculate the total height
        height = rectangleHeight * len(self._Choices)
        # return best size
        return wx.Size(width, height)


class CustomChoice(wx.Control):    
    """ Defines a custom choice control that supports themes. """
    
    def __init__(self, parent, id=wx.ID_ANY, value:str="",
                 choices:list=[], pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.NO_BORDER,
                 validator=wx.DefaultValidator, name="CustomChoice",
                 theme:str="lightTheme", fontSize=8, faceName="Verdana"):
        super().__init__(parent, id, pos, size, style, validator, name)

        # -------------- ATTRIBUTES --------------

        self._Value = value
        self._Choices = choices
        self._Theme = theme
        self._ThemeDict = {}
        self._FontSize = fontSize
        self._FaceName = faceName

        self._Enabled = True
        self._Pressed = False
        self._MouseHover = False
        

        # -------------- APPEARANCE --------------

        self._PaddingHorizontal = dip(10)
        self._PaddingVertical = dip(5)
        self._PaddingHorizontalArrow = dip(7)   
        self.arrowWidth, self.arrowHeight = dip(10), dip(3)

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.setTheme(self._Theme)
        self.SetInitialSize(size)
        
        
        # -------------- EVENTS --------------
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        if (wx.Platform == "__WXMSW__"):
            self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        

    def setTheme(self, themeString:str) -> None:
        """Sets the theme. If the theme is not valid, the first
        available theme will be chosen. Or if we definitely didnt find
        a theme, the rgb color will automatically display a random
        color.
        """
        
        # the getThemeDict returns the state of the operation and the
        # theme dictionary. we do not need the state right now.
        _, self._ThemeDict = getThemeDict(themeString)

        # refresh with changes
        self.Refresh()


    def SetValue(self, value:str):
        """ Sets the value of the control. """
        self._Value = value
        self.Refresh()
 
    def GetValue(self):
        return self._Value       

    def OnPaint(self, event):
        """ Handles the paint event. """
        
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        self.Draw(dc)
        

    def Draw(self, dc:wx.AutoBufferedPaintDC) -> None:
        """ Draw the control. """
        
        rect = self.GetClientRect()

        # draw background with parent color
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour(), wx.BRUSHSTYLE_SOLID))
        dc.DrawRectangle(rect)
        
        # check if control is enabled
        # if not, check if pressed
        # if not, check if mouse is hovering
        # if not, draw with default colors

        if not self._Enabled:
            dc.SetPen(wx.Pen(rgb(self._ThemeDict["penDisabled"]), 1))
            dc.SetBrush(wx.Brush(rgb(self._ThemeDict["brushDisabled"]), wx.BRUSHSTYLE_SOLID))
            dc.SetTextForeground(rgb(self._ThemeDict["textForegroundDisabled"]))
        else:
            dc.SetPen(wx.Pen(rgb(self._ThemeDict["penDefault"]), 1))
            dc.SetBrush(wx.Brush(rgb(self._ThemeDict["brushDefault"]), wx.BRUSHSTYLE_SOLID))
            dc.SetTextForeground(rgb(self._ThemeDict["textForegroundDefault"]))
            
        # draw border
        dc.DrawRectangle(rect)

        # draw text (to the left)
        dc.SetFont(wx.Font(self._FontSize, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName=self._FaceName))
        textWidth, textHeight = dc.GetTextExtent(self._Value)
        textX = self._PaddingHorizontal
        textY = rect.GetY() + (rect.GetHeight() // 2) - (textHeight // 2)
        dc.SetTextForeground(wx.BLACK)
        dc.DrawText(self._Value, textX, textY)
        
        # draw drop down arrow
        rectPosX = rect.GetWidth() - self.arrowWidth - self._PaddingHorizontalArrow
        rectPosY = (rect.GetHeight() // 2) - (self.arrowHeight // 2)
        # define icon area
        arrowRectangle = wx.Rect(rectPosX, rectPosY, self.arrowWidth, self.arrowHeight)
        dc.SetPen(wx.Pen(self._ThemeDict["textForegroundDefault"], 2, wx.PENSTYLE_SOLID))        
        dc.DrawLine(rectPosX, rectPosY, rectPosX+(self.arrowWidth//2), rectPosY+self.arrowHeight)
        dc.DrawLine(rectPosX+(self.arrowWidth//2), rectPosY+self.arrowHeight, arrowRectangle.GetTopRight()[0], arrowRectangle.GetTopRight()[1])

        
    def OnEraseBackground(self, event):
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

        # the witdh of the control will be the width of the longest
        # string in the choices list.

        maxWidth = 0
        maxHeight = 0

        for choice in self._Choices:
            # get dimensions
            textWidth, textHeight = dc.GetTextExtent(choice)
            # replace values
            maxWidth = textWidth if (textWidth > maxWidth) else maxWidth
            maxHeight = textHeight if (textHeight > maxHeight) else maxHeight        

        # final control dimensions
        width = self._PaddingHorizontal + maxWidth + (self._PaddingHorizontalArrow*3)
        height = self._PaddingVertical*2 + maxHeight
        return wx.Size(width, height)
    

    def OnLeftDown(self, event):

        # invert status
        self._Pressed = not self._Pressed

        if self._Pressed:
            # open choices panel
            self.createChoicesPanel()
        else:
            # destroy choices panel
            try:
                self.destroyChoicesPanel()
            except:
                pass
        
        #self.Refresh()
        event.Skip()


    def OnLeftUp(self, event):
        event.Skip()


    def OnMouseEnter(self, event):
        self._MouseHover = True
        self.Refresh()
        event.Skip()
        

    def OnMouseLeave(self, event):
        self._MouseHover = False
        self.Refresh()
        event.Skip()
        

    def AcceptsFocusFromKeyboard(self) -> bool:
        return False
        

    def Enable(self, enable:bool=True):
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
        if len(self._Choices) == 0:
            return

        rect = self.GetClientRect()

        # get choice position to place panel beneath it
        controlPosition = self.GetPosition()

        self.choicesPanel = ChoicesPanel(parent=self.GetParent(),
                                         choices=self._Choices,
                                         theme=self._Theme,
                                         reference=self,
                                         pos=(controlPosition[0], controlPosition[1]+rect.GetHeight()))
        

    def destroyChoicesPanel(self):
        """ Destroys the existing reference to the choices panel. """
        self.choicesPanel.Destroy()
        
