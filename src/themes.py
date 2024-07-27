"""
themeColors.py: Theme colors for the custom controls.

Currently defined themes:
- light
- blue
""" 

import wx


# need to create app first!
a = wx.App()


# ------------------- LIGHT THEME -------------------------

lightTheme = {
    # background
    "background": wx.Colour(240, 240, 240),
    # text
    "textForegroundDefault": wx.BLACK,
    "textForegroundPressed": wx.WHITE,
    "textForegroundHover": wx.BLACK,
    "textForegroundDisabled": wx.Colour(170, 170, 170),
    # pens
    "penDefault": wx.Colour(150, 150, 150),
    "penPressed": wx.Colour(8, 40, 107),
    "penHover": wx.Colour(65, 26, 222),
    "penDisabled": wx.Colour(220, 220, 220),
    # brushes
    "brushDefault": wx.WHITE,
    "brushPressed": wx.Colour(76, 102, 156),
    "brushHover": wx.Colour(220, 220, 220),
    "brushDisabled": wx.Colour(200, 200, 200),
    # font
    "fontFaceName": "Verdana",
}

# ------------------- BLUE THEME -------------------------

blueTheme = {
    # background
    "background": wx.Colour(0, 15, 93),
    # text
    "textForegroundDefault": wx.Colour(190, 190, 190),
    "textForegroundPressed": wx.WHITE,
    "textForegroundHover": wx.Colour(200, 200, 200),
    "textForegroundDisabled": wx.Colour(170, 170, 170),
    # pens
    "penDefault": wx.Colour(39, 62, 177),
    "penPressed": wx.Colour(65, 26, 222),
    "penHover": wx.Colour(65, 26, 222),
    "penDisabled": wx.Colour(220, 220, 220),
    # brushes
    "brushDefault": wx.Colour(19, 53, 122),
    "brushPressed": wx.Colour(16, 31, 110),
    "brushHover": wx.Colour(23, 53, 115),
    "brushDisabled": wx.Colour(200, 200, 200),
    # font
    "fontFaceName": "Verdana",
    }
