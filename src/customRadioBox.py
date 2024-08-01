import wx
from .functions.rgb import rgb
from .functions.getThemeDict import getThemeDict
from .functions.dip import dip


class CustomRadioButton(wx.Control):
    """ Defines a custom radiobutton control that supports themes. """
    
    def __init__(self, parent, referenceBox:wx.Panel, id=wx.ID_ANY,
                 label:str="", value:bool=False,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.NO_BORDER, validator=wx.DefaultValidator,
                 name="CustomRadioButton", theme:str="lightTheme",
                 fontSize=8, faceName="Verdana"):
        super().__init__(parent, id, pos, size, style, validator, name)

        # -------------- ATTRIBUTES --------------

        self._Label = label
        self._Value = value
        self._Theme = theme
        self._ThemeDict = {}
        self._FontSize = fontSize
        self._FaceName = faceName
        self._ReferenceBox = referenceBox
        
        self._Enabled = True
        self._Pressed = False
        self._MouseHover = False
        

        # -------------- APPEARANCE --------------
        
        self._PaddingHorizontal = dip(5)
        self._PaddingVertical = dip(5)
        self._RadiusOuter = dip(7)
        self._RadiusInner = dip(3)        

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
        
        
    def SetValue(self, value:bool) -> None:
        """ Sets the value of the control. """
        self._Value = value
        self.Refresh()


    def SetLabel(self, label:str) -> None:
        """ Sets the text label on the control. """
        self._Label = label
        self.Refresh()


    def GetValue(self) -> bool:
        """ Returns the value of the control. """
        return self._Value
        

    def OnPaint(self, event) -> None:
        """ Handles the paint event. """
        
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        self.Draw(dc)
        

    def Draw(self, dc: wx.AutoBufferedPaintDC) -> None:
        """ Draw the control. """

        # get drawing area
        rect = self.GetClientRect()

        # make backgrund transparent
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour(), wx.BRUSHSTYLE_SOLID))
        #dc.SetBrush(wx.GREEN_BRUSH)
        dc.DrawRectangle(rect)

        # set font
        dc.SetFont(wx.Font(self._FontSize,
                           wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL,
                           faceName=self._FaceName))
        dc.SetTextForeground(rgb(self._ThemeDict["textForegroundDefault"]))

        # we first select the pens and brushes according to the states
        # of the control

        if not self._Enabled:
            penCheckBox = wx.Pen(rgb(self._ThemeDict["penDisabled"]))
            brushCheckBox = wx.Brush(rgb(self._ThemeDict["brushDisabled"]))
            textForeground = rgb(self._ThemeDict["textForegroundDisabled"])
            penSelection = wx.Pen(rgb(self._ThemeDict["penDisabled"]), 1)
            brushSelection = wx.Brush(rgb(self._ThemeDict["brushDisabled"]))
            
        else:
            textForeground = rgb(self._ThemeDict["textForegroundDefault"])
            penSelection = wx.Pen(rgb(self._ThemeDict["penPressed"]), 1)
            brushSelection = wx.Brush(rgb(self._ThemeDict["brushPressed"]))

            if self._Pressed:
                penCheckBox = wx.Pen(rgb(self._ThemeDict["penHover"]), width=3)
                brushCheckBox = wx.Brush(rgb(self._ThemeDict["brushDefault"]))            
            elif self._MouseHover:
                penCheckBox = wx.Pen(rgb(self._ThemeDict["penHover"]), width=2)
                brushCheckBox = wx.Brush(rgb(self._ThemeDict["brushDefault"]))

            else:
                penCheckBox = wx.Pen(rgb(self._ThemeDict["penDefault"]), width=1)
                brushCheckBox = wx.Brush(rgb(self._ThemeDict["brushDefault"]))
            
        # draw radio circle
        dc.SetPen(penCheckBox)
        dc.SetBrush(brushCheckBox)
        circleX = self._PaddingHorizontal + self._RadiusOuter
        circleY = self._PaddingVertical + (self._RadiusOuter)
        dc.DrawCircle(circleX, circleY, self._RadiusOuter)

        # draw label
        _, textHeight = dc.GetTextExtent(self._Label)
        textX = self._PaddingHorizontal*2 + (2*self._RadiusOuter)
        textY = (rect.GetHeight() // 2) - (textHeight//2)
        dc.SetTextForeground(textForeground)
        dc.DrawText(self._Label, textX, textY)

        if self._Value:
            dc.SetPen(penSelection)
            dc.SetBrush(brushSelection)
            # create smaller circle with same center
            dc.DrawCircle(circleX, circleY, self._RadiusInner)
            
             
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

        # get text width and height
        dc.SetFont(font)
        textWidth, textHeight = dc.GetTextExtent(self._Label)

        # dimensions
        width = (self._PaddingHorizontal*2) + (2*self._RadiusOuter) + textWidth + dip(5)
        height = (self._PaddingVertical*2) + max(2*self._RadiusOuter, textHeight)

        return wx.Size(width, height)    
    

    def OnLeftDown(self, event) -> None:
        self._Pressed = True
        self.Refresh()
        event.Skip()


    def OnLeftUp(self, event) -> None:
        # if previously pressed
        if self._Pressed:
            # change state
            self._Pressed = False
            # change control value
            self._Value = not self._Value
            # post event
            wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_RADIOBUTTON.typeId, self.GetId()))

        # redraw with changes
        self.Refresh()
        event.Skip()
        

    def OnMouseLeave(self, event) -> None:
        self._MouseHover = False
        self.Refresh()
        event.Skip()
        

    def OnMouseEnter(self, event) -> None:
        self._MouseHover = True
        self.Refresh()
        event.Skip()


    def AcceptsFocusFromKeyboard(self) -> bool:
        return False
        

    def Enable(self, enable:bool=True) -> None:
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


class CustomRadioBox(wx.Panel):
    """ Panel containing radiobuttons. """

    """The GetValue method returns the label of the selected
    radiobutton. It will return None if none were selected."""
    
    def __init__(self, labels:list=[], value="",
                 theme:str="lightTheme", fontSize=8,
                 faceName="Verdana", orientation:str="vertical",
                 separation:int=10, size=wx.DefaultSize, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)

        # -------------- ATTRIBUTES --------------

        self._Labels = labels
        self._Value = value if (value in self._Labels) else None
        self._Theme = theme
        self._FontSize = fontSize
        self._FaceName = faceName
        self._Size = size
        self._Orientation = orientation    # box sizer orientation
        self._Separation = dip(separation) # separation between
                                           # controls

        self._Enabled = True

        # saves label and radiobutton object
        self._RadioButtonDict = {}
        # saves the radiobutton ids
        self._RadioButtonIds = []

        self._CustomRadioBoxSizer = wx.BoxSizer(orient=wx.VERTICAL if 
                                                self._Orientation == "vertical" else wx.HORIZONTAL)
        self.SetSizer(self._CustomRadioBoxSizer)

        # -------------- APPEARANCE --------------

        self._PaddingHorizontal = dip(5)
        self._PaddingVertical = dip(5)        

        self.SetBackgroundColour(self.GetParent().GetBackgroundColour())
        #self.SetBackgroundColour(wx.GREEN)
        self.SetInitialSize(size)

        

        # initialize radiobuttons
        self.init_radiobuttons()

        
    def OnRadio(self, event):
        """ Handles the event when a radiobutton is clicked on. """
        # we get the id of the selected radiobutton
        selectedRadioButtonId = event.GetId()
        # now we iterate through the radiobuttons and set their
        # respective values
        
        for label, radiobutton in self._RadioButtonDict.items():
            # if the current radiobutton matches the event id
            if radiobutton.GetId() == selectedRadioButtonId:
                radiobutton.SetValue(True)
                self._Value = label
            else:
                radiobutton.SetValue(False)
                
        # now we send a radiobox event
        wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_RADIOBOX.typeId, self.GetId()))


    def init_radiobuttons(self) -> None:

        # we create a temporary variable that will hold the maximum
        # dimensions
        maxWidth = 0
        maxHeight = 0

        if not self._Labels:
            return

        for label in self._Labels:

            # we create the radiobutton and add it to the dict
            self._RadioButtonDict[label] = CustomRadioButton(parent=self,
                                                             label=label,
                                                             value=True if (label.strip() == self._Value.strip()) else False,
                                                             theme=self._Theme,
                                                             fontSize=self._FontSize,
                                                             faceName=self._FaceName,
                                                             referenceBox=self)

            self._RadioButtonIds.append(self._RadioButtonDict[label].GetId())
            
            

            # bind event
            self._RadioButtonDict[label].Bind(wx.EVT_RADIOBUTTON, self.OnRadio)
            

            # we get the size of the radiobutton
            controlSize = self._RadioButtonDict[label].GetClientSize()
            

            # calculate dimensions
            if (self._Orientation == "vertical"):
                # we see if this should be the width
                if (controlSize[0] > maxWidth):
                    maxWidth = controlSize[0]
                # we add the height
                maxHeight += controlSize[1] + self._Separation
                
            elif (self._Orientation == "horizontal"):
                # we add the width
                maxWidth += controlSize[0] + self._Separation
                # we see if this should be the height
                if (controlSize[1] > maxHeight):
                    maxHeight = controlSize[1]
                    

            # we add the radiobutton to the sizer
            self._CustomRadioBoxSizer.Add(window=self._RadioButtonDict[label],
                                          proportion=0,
                                          flag=0,
                                          border=0)
            

            self._CustomRadioBoxSizer.AddSpacer(self._Separation)

        
        # set the size (automatically, not specified)
        if self._Size == wx.DefaultSize:
            self.SetMinClientSize(wx.Size(maxWidth, maxHeight))
            
        # display correctly
        self.Layout()

            
    def destroyRadioButtons(self) -> None:
        """ Should be called when setting new labels. """

        # destroy each radiobutton
        for label in self._RadioButtonDict.keys():
            self._RadioButtonDict[label].Destroy()

        # we clear the dictionary
        self._RadioButtonDict.clear()

        # clear the ids list
        self._RadioButtonIds.clear()


    def GetValue(self):
        """Returns the label from the currently selected
        radiobutton. Returns None if none selected. """
        return self._Value

    
    def GetValues(self):
        """ Returns a dictionary containing the states of each radiobutton. """
        # create dictionary
        valuesDict = {}
        for label in self._RadioButtonDict.keys():
            valuesDict[label] = self._RadioButtonDict[label].GetValue()
        return valuesDict

    
    def SetLabels(self, labels:list=[str]):
        """ Redraws the radiobuttons with these new labels. """
        # set attribute
        self._Labels = labels
        # clear drawn radiobuttons
        self.destroyRadioButtons()
        # redraw
        self.init_radiobuttons()
        

    def SetValue(self, value:str):
        """ Sets the selected radiobutton on. """
        if value not in self._Labels:
            return
        self._RadioButtonDict[value].SetValue(True)


    def updateEnabled(self):
        """ Actually enables or disables radiobuttons. """
        for radiobutton in self._RadioButtonDict.values():
            if self._Enabled:
                radiobutton.Enable()
            else:
                radiobutton.Disable()
            
        
    def Enable(self):
        """ Enables the radiobuttons. """
        self._Enabled = True
        self.updateEnabled()


    def Disable(self):
        """ Disables the radiobuttons. """
        self._Enabled = False
        self.updateEnabled()
        
