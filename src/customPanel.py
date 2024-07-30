import wx
from .functions.getThemeDict import getThemeDict
from .functions.rgb import rgb


class CustomPanel(wx.Panel):
    """ A custom panel that supports themes. """
    
    def __init__(self, theme:str="lightTheme", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._Theme = theme
        self._ThemeDict = {}

        # initialize the theme dictionary
        self.setTheme(self._Theme)

        # set the background color according to theme
        self.SetBackgroundColour(rgb(self._ThemeDict["panelBackground"]))


    def setTheme(self, themeString:str):
        """Sets the theme. If the theme is not valid, the first
        available theme will be chosen. Or if we definitely didnt find
        a theme, the rgb color will automatically display a random
        color.
        """

        # the getThemeDict returns the state of the operation and the
        # theme dictionary.
        _, self._ThemeDict = getThemeDict(themeString)

        self.Refresh()
