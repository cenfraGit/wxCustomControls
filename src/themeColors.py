"""
themeColors.py: Theme colors and drawing objects for the custom controls.

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
    "penDefault": wx.Pen(wx.Colour(150, 150, 150), width=1, style=wx.PENSTYLE_SOLID),
    "penPressed": wx.Pen(wx.Colour(8, 40, 107), width=1, style=wx.PENSTYLE_SOLID),
    "penHover": wx.Pen(wx.Colour(65, 26, 222), width=1, style=wx.PENSTYLE_SOLID),
    "penDisabled": wx.Pen(wx.Colour(220, 220, 220), width=1, style=wx.PENSTYLE_SOLID),
    # brushes
    "brushDefault": wx.Brush(wx.WHITE, wx.BRUSHSTYLE_SOLID),
    "brushPressed": wx.Brush(wx.Colour(76, 102, 156), wx.BRUSHSTYLE_SOLID),
    "brushHover": wx.Brush(wx.Colour(220, 220, 220), wx.BRUSHSTYLE_SOLID),
    "brushDisabled": wx.Brush(wx.Colour(200, 200, 200), wx.BRUSHSTYLE_SOLID)
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
    "penDefault": wx.Pen(wx.Colour(39, 62, 177), width=1, style=wx.PENSTYLE_SOLID),
    "penPressed": wx.Pen(wx.Colour(65, 26, 222), width=1, style=wx.PENSTYLE_SOLID),
    "penHover": wx.Pen(wx.Colour(65, 26, 222), width=1, style=wx.PENSTYLE_SOLID),
    "penDisabled": wx.Pen(wx.Colour(220, 220, 220), width=1, style=wx.PENSTYLE_SOLID),
    # brushes
    "brushDefault": wx.Brush(wx.Colour(19, 53, 122), wx.BRUSHSTYLE_SOLID),
    "brushPressed": wx.Brush(wx.Colour(16, 31, 110), wx.BRUSHSTYLE_SOLID),
    "brushHover": wx.Brush(wx.Colour(23, 53, 115), wx.BRUSHSTYLE_SOLID),
    "brushDisabled": wx.Brush(wx.Colour(200, 200, 200), wx.BRUSHSTYLE_SOLID)

    }
