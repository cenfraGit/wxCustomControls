import wx
from .functions.rgb import rgb
from .functions.getThemeDict import getThemeDict
from .functions.dip import dip

class StaticBoxBorder(wx.Panel):
    pass

class CustomStaticBox(wx.Panel):
    """ Defines a custom static box that supports themes. """

    def __init__(self, label, size=(300, 300), theme="lightTheme", *args, **kwargs):
        super().__init__(*args, **kwargs)

        # -------------- ATTRIBUTES --------------

        self._Label = label
        self._Theme = theme
        self._ThemeDict = {}


        # -------------- APPEARANCE --------------

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
        """ Sets the button's label text. """
        self._Label = label
        self.Refresh()

        
    def OnPaint(self, event) -> None:

        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()

        dc.DrawCircle(10, 10, 10)

        pass
        
        
    
    
