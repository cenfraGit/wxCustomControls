import wx
from .functions.rgb import rgb
from .functions.getThemeDict import getThemeDict
from .functions.dip import dip
import copy


class CustomCheckBox(wx.Control):    
    """ Defines a custom checkbox control that supports themes. """
    
    def __init__(self, parent, id=wx.ID_ANY, label:str="", value:bool=False, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.NO_BORDER, validator=wx.DefaultValidator,
                 name="CustomCheckBox", theme:str="lightTheme", fontSize=8, faceName="Verdana"):
        super().__init__(parent, id, pos, size, style, validator, name)

        # -------------- ATTRIBUTES --------------

        self._Label = label
        self._Value = value
        self._Theme = theme
        self._ThemeDict = {}
        self._FontSize = fontSize
        self._FaceName = faceName
        
        self._Enabled = True
        self._Pressed = False
        self._MouseHover = False
        

        # -------------- APPEARANCE --------------
        
        self._PaddingHorizontal = dip(5)
        self._PaddingVertical = dip(5)
        self._WidthHeightCheckBox = dip(15)
        self._DeflateSelection = dip(3)

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
            
        # draw checkbox
        dc.SetPen(penCheckBox)
        dc.SetBrush(brushCheckBox)
        rectangleCheckBox = wx.Rect(self._PaddingHorizontal,
                                    self._PaddingVertical,
                                    self._WidthHeightCheckBox,
                                    self._WidthHeightCheckBox)
        dc.DrawRectangle(rectangleCheckBox)

        # draw label
        _, textHeight = dc.GetTextExtent(self._Label)
        textX = self._PaddingHorizontal*2 + self._WidthHeightCheckBox
        textY = (rect.GetHeight() // 2) - (textHeight//2)
        dc.SetTextForeground(textForeground)
        dc.DrawText(self._Label, textX, textY)

        if self._Value:
            dc.SetPen(penSelection)
            dc.SetBrush(brushSelection)
            # shallow copy
            newRectangle = copy.copy(rectangleCheckBox)
            # make rectangle smaller
            newRectangle.Deflate(self._DeflateSelection,
                                 self._DeflateSelection)
            # draw selection indicator
            dc.DrawRectangle(newRectangle)
            
        
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
        width = (self._PaddingHorizontal*2) + self._WidthHeightCheckBox + textWidth + dip(5)
        height = (self._PaddingVertical*2) + max(self._WidthHeightCheckBox, textHeight)

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
            wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_CHECKBOX.typeId, self.GetId()))
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

