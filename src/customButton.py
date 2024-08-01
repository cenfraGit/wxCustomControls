import wx
from .functions.rgb import rgb
from .functions.getThemeDict import getThemeDict
from .functions.dip import dip


class CustomButton(wx.Control):    
    """ Defines a custom button that supports themes. """
    
    def __init__(self, parent, id=wx.ID_ANY, label:str="",
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.NO_BORDER, validator=wx.DefaultValidator,
                 name="CustomButton", theme:str="lightTheme",
                 fontSize=8, faceName="Verdana"):
        super().__init__(parent, id, pos, size, style, validator, name)

        # -------------- ATTRIBUTES --------------
        
        self._Label = label
        self._Theme = theme
        self._ThemeDict = {}
        self._FontSize = fontSize
        self._FaceName = faceName

        self._Enabled = True
        self._Pressed = False
        self._MouseHover = False
        

        # -------------- APPEARANCE --------------
        
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

        
    def SetLabel(self, label:str) -> None:
        """ Sets the button's label text. """
        self._Label = label
        self.Refresh()
        

    def OnPaint(self, event) -> None:
        """ Handles the paint event. """

        # create device context
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()

        # create graphics context
        gc = wx.GraphicsContext.Create(dc)
        self.Draw(gc)
        

    def Draw(self, gc:wx.GraphicsContext) -> None:
        """ Draws the actual control. """

        # get drawing area
        rect = self.GetClientRect()

        # draw background with parent color (for rounded corners)
        gc.SetPen(wx.TRANSPARENT_PEN)
        gc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour(), wx.BRUSHSTYLE_SOLID))
        gc.DrawRectangle(rect.GetX(), rect.GetY(), rect.GetWidth(), rect.GetHeight())

        # 1. check if the button is enabled
        # 2. if it is, check if the button is pressed
        # 3. if its not pressed, check if cursor is hovering
        # 4. if not hovering, draw with default colors.

        textForeground = wx.BLACK

        if not self._Enabled:
            gc.SetPen(wx.Pen(rgb(self._ThemeDict["penDisabled"]), 1))
            gc.SetBrush(wx.Brush(rgb(self._ThemeDict["brushDisabled"]), wx.BRUSHSTYLE_SOLID))
            textForeground = rgb(self._ThemeDict["textForegroundDisabled"])
        else:
            if self._Pressed:
                gc.SetPen(wx.Pen(rgb(self._ThemeDict["penPressed"]), 1))
                gc.SetBrush(wx.Brush(rgb(self._ThemeDict["brushPressed"]), wx.BRUSHSTYLE_SOLID))
                textForeground = rgb(self._ThemeDict["textForegroundPressed"])
            elif self._MouseHover:
                gc.SetPen(wx.Pen(rgb(self._ThemeDict["penHover"]), 1))
                gc.SetBrush(wx.Brush(rgb(self._ThemeDict["brushHover"]), wx.BRUSHSTYLE_SOLID))
                textForeground = rgb(self._ThemeDict["textForegroundHover"])
            else:
                gc.SetPen(wx.Pen(rgb(self._ThemeDict["penDefault"]), 1))
                gc.SetBrush(wx.Brush(rgb(self._ThemeDict["brushDefault"]), wx.BRUSHSTYLE_SOLID))
                textForeground = rgb(self._ThemeDict["textForegroundDefault"])
            
        # draw border    
        gc.DrawRoundedRectangle(rect.GetX(), rect.GetY(), rect.GetWidth(), rect.GetHeight(), dip(6))

        # draw text (centered)
        gc.SetFont(wx.Font(self._FontSize,
                           wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL,
                           faceName=self._FaceName), textForeground)
        
        textWidth, textHeight, _, _= gc.GetFullTextExtent(self._Label)
        textX = rect.GetX() + (rect.GetWidth() // 2) - (textWidth // 2)
        textY = rect.GetY() + (rect.GetHeight() // 2) - (textHeight // 2)
        gc.DrawText(self._Label, textX, textY)
        

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
        dc.SetFont(font)

        # get label dimensions
        textWidth, textHeight = dc.GetTextExtent(self._Label)

        # margins for sides
        leftRightMargins = dip(20)
        topBottomMargins = dip(5)

        # final control dimensions
        width = leftRightMargins*2 + textWidth
        height = topBottomMargins*2 + textHeight

        # return best size
        return wx.Size(width, height)
    

    def OnLeftDown(self, event:wx.MouseEvent) -> None:
        self._Pressed = True
        self.Refresh()
        event.Skip()


    def OnLeftUp(self, event:wx.MouseEvent) -> None:
        if self._Pressed:
            self._Pressed = False
            self.Refresh()
            wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.GetId()))
        event.Skip()
        

    def OnMouseLeave(self, event:wx.MouseEvent) -> None:
        self._MouseHover = False
        self._Pressed = False
        self.Refresh()
        event.Skip()
        

    def OnMouseEnter(self, event:wx.MouseEvent) -> None:
        self._MouseHover = True
        self.Refresh()
        event.Skip()


    def AcceptsFocusFromKeyboard(self) -> bool:
        return False
        

    def Enable(self, enable:bool=True) -> None:
        """Uses _Enabled to define if the widget is enabled or not
        instead of using default behavior (problems redrawing after
        modal dialogs).
        """
        self._Enabled = enable
        super().Enable(enable)
        self.Refresh()
        

    def Disable(self) -> None:
        self.Enable(False)

