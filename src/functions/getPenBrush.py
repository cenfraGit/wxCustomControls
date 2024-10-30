# getPenBrush.py
# wxCustomControls
# Functions to get pen and brush when drawing.
# 28/oct/2024


import wx
from ..CustomConfig import CustomConfig


def getPen(state:str, config:CustomConfig) -> wx.Pen:
    """Returns a transparent pen if the border width is 0."""
    borderWidth, borderColour = 0, wx.BLACK
    if (state == "disabled"):
        borderWidth = config.border_width_disabled
        borderColour = config.border_colour_disabled
    elif (state == "pressed"):
        borderWidth = config.border_width_pressed
        borderColour = config.border_colour_pressed
    elif (state == "hover"):
        borderWidth = config.border_width_hover
        borderColour = config.border_colour_hover
    elif (state == "default"):
        borderWidth = config.border_width_default
        borderColour = config.border_colour_default

    if borderWidth:
        return wx.Pen(borderColour, borderWidth)
    else:
        return wx.TRANSPARENT_PEN


def getBrush(state:str, config:CustomConfig, gc:wx.GraphicsContext) -> wx.Brush:
    if (state == "disabled"):
        gradient = config.background_linear_gradient_disabled
        background_colour = config.background_colour_disabled
    elif (state == "pressed"):
        gradient = config.background_linear_gradient_pressed
        background_colour = config.background_colour_pressed
    elif (state == "hover"):
        gradient = config.background_linear_gradient_hover
        background_colour = config.background_colour_hover
    elif (state == "default"):
        gradient = config.background_linear_gradient_default
        background_colour = config.background_colour_default

    if gradient:
        c1 = wx.Colour(*gradient[4])
        c2 = wx.Colour(*gradient[5])
        x1, y1, x2, y2, _, _ = gradient
        brush = gc.CreateLinearGradientBrush(x1, y1, x2, y2, c1, c2)
    else:
        brush = wx.Brush(background_colour)

    return brush
    
        
