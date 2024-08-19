import wx
from ..controlConfig import ControlConfig


def getPen(state:str, config:ControlConfig) -> wx.Pen:

    """Returns a transparent pen if the border width is 0,
    otherwise it returns the pen with the respective
    colour. states: disabled, pressed, hover, default.
    """

    if state == "disabled":
        borderWidth = config.border_width_disabled
        borderColour = config.border_colour_disabled
    elif state == "pressed":
        borderWidth = config.border_width_pressed
        borderColour = config.border_colour_pressed
    elif state == "hover":
        borderWidth = config.border_width_hover
        borderColour = config.border_colour_hover
    else: # default
        borderWidth = config.border_width
        borderColour = config.border_colour

    # set a transparent pen if the width is 0
    if borderWidth:
        return wx.Pen(borderColour, borderWidth)
    else:
        return wx.TRANSPARENT_PEN



def getBrush(state:str, config:ControlConfig, gc:wx.GraphicsContext) -> wx.Brush:

        if state == "disabled":
            gradient = config.bg_linear_gradient_disabled
            bg_colour = config.bg_colour_disabled
        elif state == "pressed":
            gradient = config.bg_linear_gradient_pressed
            bg_colour = config.bg_colour_pressed
        elif state == "hover":
            gradient = config.bg_linear_gradient_hover
            bg_colour = config.bg_colour_hover
        else:
            gradient = config.bg_linear_gradient
            bg_colour = config.bg_colour
            
        if gradient:
            c1, c2 = wx.Colour(*gradient[4]), wx.Colour(*gradient[5])
            x1, y1, x2, y2, _, _ = gradient
            brush = gc.CreateLinearGradientBrush(x1, y1, x2, y2, c1, c2)
        else:
            brush = wx.Brush(wx.Colour(*bg_colour))
            
        return brush
