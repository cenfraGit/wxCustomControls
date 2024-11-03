# _CustomObject.py
# wxCustomControls
# The base class for all custom objects. It sets up the config and
# includes functions used when drawing.
# 11/nov/2024


import wx
from copy import copy
from .utils.dip import dip
from .CustomConfig import CustomConfig
from .functions.getDefaultConfig import getDefaultConfig


class CustomObject:
    def __init__(self, config, **kwargs):

        # --------- get the config for current object --------- #
        #self._config = getConfig(config, self.__class__.__name__)

        if config:
            self._config:CustomConfig = copy(config)
        else:
            self._config:CustomConfig = getDefaultConfig(self.__class__.__name__)
        
        self._config.Update(**kwargs)


    def SetConfig(self, config:CustomConfig):
        self._config = config
        self.Refresh()

        
    def GetConfig(self):
        return self._config


    def UpdateConfig(self, **kwargs):
        self._config.Update(**kwargs)
        self.Refresh()


    def GetBackgroundColour(self):
        return wx.Colour(*self._config.background_colour_default)
        

    def _getDrawingContexts(self):
        dc = wx.BufferedPaintDC(self)
        gcdc = wx.GCDC(dc)
        gc:wx.GraphicsContext = gcdc.GetGraphicsContext()
        gcdc.Clear()
        return gcdc, gc

    
    def _getPen(self, state:str, config:CustomConfig) -> wx.Pen:
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
        # -------------------- return pen -------------------- #
        if borderWidth:
            return wx.Pen(borderColour, borderWidth)
        else:
            return wx.TRANSPARENT_PEN
        

    def _getBrush(self, state:str, config:CustomConfig, gc:wx.GraphicsContext) -> wx.Brush:
        gradient, background_colour = None, (255, 255, 255)
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


    def _getStateDrawingProperties(self, control_state:str, config:CustomConfig, gc):

        if control_state not in ["default", "pressed", "hover", "disabled"]:
            raise ValueError("getStateProperties::Invalid control_state.")

        pen = self._getPen(control_state, config) # takes care of borders
        brush = self._getBrush(control_state, config, gc) # takes care of background

        if (control_state == "default"):
            cursor = wx.Cursor(wx.CURSOR_ARROW)
            text_font_size = config.text_font_size_default
            text_font_facename = config.text_font_facename_default
            text_foreground_colour = config.text_foreground_colour_default
            corner_radius = config.corner_radius_default
            image = config.image_default
            image_channels = config.image_channels_default
            image_size = config.image_size_default
        elif (control_state == "pressed"):
            cursor = wx.Cursor(config.cursor_stockcursor_pressed)
            text_font_size = config.text_font_size_pressed
            text_font_facename = config.text_font_facename_pressed
            text_foreground_colour = config.text_foreground_colour_pressed
            corner_radius = config.corner_radius_pressed
            image = config.image_pressed
            image_channels = config.image_channels_pressed
            image_size = config.image_size_pressed
        elif (control_state == "hover"):
            cursor = wx.Cursor(config.cursor_stockcursor_hover)
            text_font_size = config.text_font_size_hover
            text_font_facename = config.text_font_facename_hover
            text_foreground_colour = config.text_foreground_colour_hover
            corner_radius = config.corner_radius_hover
            image = config.image_hover
            image_channels = config.image_channels_hover
            image_size = config.image_size_hover
        else: # disabled
            cursor = wx.Cursor(config.cursor_stockcursor_disabled)
            text_font_size = config.text_font_size_disabled
            text_font_facename = config.text_font_facename_disabled
            text_foreground_colour = config.text_foreground_colour_disabled
            corner_radius = config.corner_radius_disabled
            image = config.image_disabled
            image_channels = config.image_channels_disabled
            image_size = config.image_size_disabled

        return {
            "pen": pen,
            "brush": brush,
            "cursor": cursor,
            "text_font_size": text_font_size,
            "text_font_facename": text_font_facename,
            "text_foreground_colour": text_foreground_colour,
            "corner_radius": corner_radius,
            "image": image,
            "image_channels": image_channels,
            "image_size": image_size
        }


    def _getImageTextCoordinates(self, rectangle:wx.Rect,
                                text, config:CustomConfig,
                                imageWidth:int, imageHeight:int,
                                textWidth:int, textHeight:int):

        textX, textY = 0, 0
        imageX, imageY = 0, 0

        # -------------------- if no text -------------------- #

        if (text == wx.EmptyString):
            # image in center if no text
            imageX = (rectangle.GetWidth() // 2) - (imageWidth // 2)
            imageY = (rectangle.GetHeight() // 2) - (imageHeight // 2)

        # ------------- if no image (dimensions) ------------- #

        elif (imageWidth == 0 or imageHeight == 0):
            # calculate center
            textX = rectangle.GetX() + (rectangle.GetWidth() // 2) - (textWidth // 2)
            textY = rectangle.GetY() + (rectangle.GetHeight() // 2) - (textHeight // 2)

        # -------------- if both image and text -------------- #

        else:
            text_separation = config.image_text_separation if config.image_text_separation else dip(6)
            if (config.text_side == "right"):
                imageX = (rectangle.GetWidth() // 2) - ((imageWidth + textWidth + text_separation) // 2) 
                imageY = (rectangle.GetHeight() // 2) - (imageHeight // 2)
                textX = imageX + imageWidth + text_separation
                textY = (rectangle.GetHeight() // 2) - (textHeight // 2)
            elif (config.text_side == "left"):
                textX = (rectangle.GetWidth() // 2) - ((imageWidth + textWidth + text_separation) // 2) 
                textY = (rectangle.GetHeight() // 2) - (textHeight // 2)
                imageX = textX + textWidth + text_separation
                imageY = (rectangle.GetHeight() // 2) - (imageHeight // 2)
            elif (config.text_side == "up"):
                textX = (rectangle.GetWidth() // 2) - (textWidth // 2)
                textY = (rectangle.GetHeight() // 2) - ((imageHeight + textHeight + text_separation) // 2)
                imageX = (rectangle.GetWidth() // 2) - (imageWidth // 2)
                imageY = textY + textHeight + text_separation
            elif (config.text_side == "down"):
                imageX = (rectangle.GetWidth() // 2) - (imageWidth // 2)
                imageY = (rectangle.GetHeight() // 2) - ((imageHeight + textHeight + text_separation) // 2)
                textX = (rectangle.GetWidth() // 2) - (textWidth // 2)
                textY = imageY + imageHeight
            else:
                raise ValueError("text_side must be left, right, up or down.")

        return imageX, imageY, textX, textY
    
