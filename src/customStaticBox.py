import wx
from .functions.rgb import rgb
from .functions.getThemeDict import getThemeDict
from .functions.dip import dip
import copy

class CustomStaticBox(wx.Panel):

    
    def __init__(self, parent, label:str="", size=wx.DefaultSize,
                 theme:str="lightTheme", fontSize:int=8,
                 faceName:str="Verdana", *args, **kwargs):
        
        super().__init__(parent, *args, **kwargs)

        # -------------- ATTRIBUTES --------------

        self._Label = label
        self._Theme = theme
        self._ThemeDict = {}
        self._FontSize = fontSize
        self._FaceName = faceName
        

        # -------------- APPEARANCE --------------

        self._MarginTop = dip(self._FontSize)

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.setTheme(self._Theme)
        self.SetInitialSize(size)
        

        # -------------- EVENTS --------------

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        

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
        self._Label = label
        self.Refresh()

        
    def OnPaint(self, event) -> None:

        # create dc
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()

        # get panel area
        rect = self.GetClientRect()

        brushBackground = wx.Brush(self.GetParent().GetBackgroundColour())
        #brushBackground = wx.GREEN_BRUSH

        # set background pen
        dc.SetBrush(brushBackground)

        # draw background
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle(rect)
        # draw rounded border
        dc.SetPen(wx.Pen(rgb(self._ThemeDict["penDefault"])))
        dc.DrawRoundedRectangle(rect.GetX(), rect.GetY()+self._MarginTop, rect.GetWidth(), rect.GetHeight()-self._MarginTop, dip(5))

        # draw label
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(brushBackground)
        dc.SetFont(wx.Font(self._FontSize, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName=self._FaceName))
        dc.SetTextForeground(rgb(self._ThemeDict["textForegroundDefault"]))
        textWidth, textHeight = dc.GetTextExtent(self._Label)
        # centered values
        textX = (rect.GetWidth() // 2) - (textWidth // 2)
        textY = (self._MarginTop - textHeight//2)
        # draw text background
        lateralOffset = dip(5)
        dc.DrawRectangle(textX-lateralOffset, textY, textWidth+(2*lateralOffset), textHeight)
        # draw text
        dc.DrawText(self._Label, textX, textY)
        
