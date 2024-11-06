# _CustomObject.py
# wxCustomControls
# The base class for all custom objects. It sets up the config and
# includes functions used when drawing.
# 11/nov/2024


import wx
from copy import copy
from ..utils.dip import dip
from ..CustomConfig import CustomConfig
from ..functions.getDefaultConfig import getDefaultConfig


class CustomObject:
    def __init__(self, config, **kwargs):

        # --------- get the config for current object --------- #

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
        

    def _getDrawingContexts(self, window=None):
        window = window if window else self
        dc = wx.BufferedPaintDC(window)
        gcdc = wx.GCDC(dc)
        gc:wx.GraphicsContext = gcdc.GetGraphicsContext()
        gcdc.Clear()
        return gcdc, gc

    
    def _getPen(self, state:str) -> wx.Pen:
        """Returns a transparent pen if the border width is 0."""
        borderWidth, borderColour = 0, wx.BLACK
        if (state == "disabled"):
            borderWidth = self._config.border_width_disabled
            borderColour = self._config.border_colour_disabled
        elif (state == "pressed"):
            borderWidth = self._config.border_width_pressed
            borderColour = self._config.border_colour_pressed
        elif (state == "hover"):
            borderWidth = self._config.border_width_hover
            borderColour = self._config.border_colour_hover
        elif (state == "default"):
            borderWidth = self._config.border_width_default
            borderColour = self._config.border_colour_default
        # -------------------- return pen -------------------- #
        if borderWidth:
            return wx.Pen(borderColour, borderWidth)
        else:
            return wx.TRANSPARENT_PEN
        

    def _getBrush(self, state:str, layer:str, gc:wx.GraphicsContext) -> wx.Brush:
        gradient, colour = None, (255, 255, 255)
        if (state == "default"):
            gradient = self._config.background_linear_gradient_default if (layer == "background") else self._config.foreground_linear_gradient_default
            colour = self._config.background_colour_default if (layer == "background") else self._config.foreground_colour_default
        elif (state == "pressed"):
            gradient = self._config.background_linear_gradient_pressed if (layer == "background") else self._config.foreground_linear_gradient_pressed
            colour = self._config.background_colour_pressed if (layer == "background") else self._config.foreground_colour_pressed
        elif (state == "hover"):
            gradient = self._config.background_linear_gradient_hover if (layer == "background") else self._config.foreground_linear_gradient_hover
            colour = self._config.background_colour_hover if (layer == "background") else self._config.foreground_colour_hover
        elif (state == "disabled"):
            gradient = self._config.background_linear_gradient_disabled if (layer == "background") else self._config.foreground_linear_gradient_disabled
            colour = self._config.background_colour_disabled if (layer == "background") else self._config.foreground_colour_disabled

        if gradient:
            c1 = wx.Colour(*gradient[4])
            c2 = wx.Colour(*gradient[5])
            x1, y1, x2, y2, _, _ = gradient
            brush = gc.CreateLinearGradientBrush(x1, y1, x2, y2, c1, c2)
        else:
            brush = wx.Brush(colour)

        return brush


    def _getStateDrawingProperties(self, control_state:str, gc:wx.GraphicsContext):

        if control_state not in ["default", "pressed", "hover", "disabled"]:
            raise ValueError("getStateProperties::Invalid control_state.")

        pen = self._getPen(control_state) # takes care of borders
        brush_background = self._getBrush(control_state, "background", gc) # takes care of background
        brush_foreground = self._getBrush(control_state, "foreground", gc)

        if (control_state == "default"):
            cursor = wx.Cursor(wx.CURSOR_ARROW)
            text_font_size = self._config.text_font_size_default
            text_font_facename = self._config.text_font_facename_default
            text_foreground_colour = self._config.text_foreground_colour_default
            corner_radius = self._config.corner_radius_default
            image = self._config.image_default
            image_channels = self._config.image_channels_default
            image_size = self._config.image_size_default
            background_colour_active = self._config.background_colour_active_default
            foreground_colour_active = self._config.foreground_colour_active_default
        elif (control_state == "pressed"):
            cursor = wx.Cursor(self._config.cursor_stockcursor_pressed)
            text_font_size = self._config.text_font_size_pressed
            text_font_facename = self._config.text_font_facename_pressed
            text_foreground_colour = self._config.text_foreground_colour_pressed
            corner_radius = self._config.corner_radius_pressed
            image = self._config.image_pressed
            image_channels = self._config.image_channels_pressed
            image_size = self._config.image_size_pressed
            background_colour_active = self._config.background_colour_active_pressed
            foreground_colour_active = self._config.foreground_colour_active_pressed
        elif (control_state == "hover"):
            cursor = wx.Cursor(self._config.cursor_stockcursor_hover)
            text_font_size = self._config.text_font_size_hover
            text_font_facename = self._config.text_font_facename_hover
            text_foreground_colour = self._config.text_foreground_colour_hover
            corner_radius = self._config.corner_radius_hover
            image = self._config.image_hover
            image_channels = self._config.image_channels_hover
            image_size = self._config.image_size_hover
            background_colour_active = self._config.background_colour_active_hover
            foreground_colour_active = self._config.foreground_colour_active_hover
        else: # disabled
            cursor = wx.Cursor(self._config.cursor_stockcursor_disabled)
            text_font_size = self._config.text_font_size_disabled
            text_font_facename = self._config.text_font_facename_disabled
            text_foreground_colour = self._config.text_foreground_colour_disabled
            corner_radius = self._config.corner_radius_disabled
            image = self._config.image_disabled
            image_channels = self._config.image_channels_disabled
            image_size = self._config.image_size_disabled
            background_colour_active = self._config.background_colour_active_disabled
            foreground_colour_active = self._config.foreground_colour_active_disabled

        return {
            "pen": pen,
            "brush_background": brush_background,
            "brush_foreground": brush_foreground,
            "cursor": cursor,
            "text_font_size": text_font_size,
            "text_font_facename": text_font_facename,
            "text_foreground_colour": text_foreground_colour,
            "corner_radius": corner_radius,
            "image": image,
            "image_channels": image_channels,
            "image_size": image_size,
            "background_colour_active": background_colour_active,
            "foreground_colour_active": foreground_colour_active
        }


    def _getObjectSideDimensions(self,
                                 object1Width:int, object1Height:int,
                                 object2Width:int, object2Height:int,
                                 separation, object2_side):
        """Returns the dimensions of a rectangle depending on the
        arrangement of an object and its object2_side (used in images and
        checkboxes)."""
        rectangleWidth, rectangleHeight = 0, 0
        if (object2_side == "right" or object2_side == "left"):
            rectangleWidth = object1Width + separation + object2Width
            rectangleHeight = max(object1Height, object2Height)
        elif (object2_side == "up" or object2_side == "down"):
            rectangleWidth = max(object1Width, object2Width)
            rectangleHeight = object1Height + separation + object2Height
        else:
            raise ValueError("object2_side must be left, right, up or down.")
        return rectangleWidth, rectangleHeight


    def _performObjectSideCalculation(self, rectangle:wx.Rect, object1Width, object1Height, object2Width, object2Height, separation, object2_side):
        """Returns the coordinates for two objects depending on the side specified for object2."""

        object1X, object1Y = 0, 0 # init coords for object1 (main object)
        object2X, object2Y = 0, 0 # init coords for object2
        r = rectangle # alias
        theresObject1:bool = (object1Width != 0 and object1Height != 0)
        theresObject2:bool = (object2Width != 0 and object2Height != 0)

        if not theresObject2:
            # object1 in center of rectangle
            object1X = r.GetX() + (r.GetWidth() // 2) - (object1Width // 2)
            object1Y = r.GetY() + (r.GetHeight() // 2) - (object1Height // 2)

        elif not theresObject1:
            # object2 in center of rectangle
            object2X = r.GetX() + (r.GetWidth() // 2) - (object2Width // 2)
            object2Y = r.GetY() + (r.GetHeight() // 2) - (object2Height // 2)

        else:
            separation = separation if separation else dip(6)
            
            if (object2_side == "right"):
                object1X = r.GetX() + (r.GetWidth() // 2) - ((object1Width + separation + object2Width) // 2)
                object1Y = r.GetY() + (r.GetHeight() // 2) - (object1Height // 2)
                object2X = object1X + object1Width + separation
                object2Y = r.GetY() + (r.GetHeight() // 2) - (object2Height // 2)
            elif (object2_side == "left"):
                object2X = r.GetX() + (r.GetWidth() // 2) - ((object1Width + separation + object2Width) // 2)
                object2Y = r.GetY() + (r.GetHeight() // 2) - (object2Height // 2)
                object1X = object2X + object2Width + separation
                object1Y = r.GetY() + (r.GetHeight() // 2) - (object1Height // 2)
            elif (object2_side == "up"):
                object2X = r.GetX() + (r.GetWidth() // 2) - (object2Width // 2)
                object2Y = r.GetY() + (r.GetHeight() // 2) - ((object1Height + separation + object2Height) // 2)
                object1X = r.GetX() + (r.GetWidth() // 2) - (object1Width // 2)
                object1Y = object2Y + object2Height + separation
            elif (object2_side == "down"):
                object1X = r.GetX() + (r.GetWidth() // 2) - (object1Width // 2)
                object1Y = r.GetY() + (r.GetHeight() // 2) - ((object1Height + separation + object2Height) // 2)
                object2X = r.GetX() + (r.GetWidth() // 2) - (object2Width // 2)
                object2Y = object1Y + object1Height + separation
            else:
                raise ValueError("object2_side must be left, right, up or down.")
            
        return object1X, object1Y, object2X, object2Y


    def _drawImageTextRectangle(self, gcdc:wx.GCDC, rectangle:wx.Rect, text, textWidth, textHeight, bitmap, imageWidth, imageHeight,):
        """Draws an image and text (or either) in the specified rectangle. It assumes that the rectangle has enough space."""

        imageX, imageY, textX, textY = self._performObjectSideCalculation(rectangle,
                                                                          imageWidth, imageHeight,
                                                                          textWidth, textHeight,
                                                                          self._config.image_text_separation,
                                                                          self._config.image_text_side)
        
        theresText:bool = (text != wx.EmptyString and text.strip() != "")
        theresImage:bool = (imageWidth != 0 and imageHeight != 0)
            
        if theresText:
            gcdc.DrawText(text, textX, textY)
        if theresImage:
            gcdc.DrawBitmap(bitmap, imageX, imageY)


    def _getTextDimensions(self, gcdc, string, drawing_properties):        
        textWidth, textHeight = 0, 0
        if (string != wx.EmptyString):
            gcdc.GetGraphicsContext().SetFont(wx.Font(drawing_properties["text_font_size"],
                               wx.FONTFAMILY_DEFAULT,
                               wx.FONTSTYLE_NORMAL,
                               wx.FONTWEIGHT_NORMAL,
                               faceName=drawing_properties["text_font_facename"]), drawing_properties["text_foreground_colour"])
            textWidth, textHeight = gcdc.GetTextExtent(string)
        return textWidth, textHeight
    

    def _getBitmapAndDimensions(self, drawing_properties):
        if self._config.image_use_max_dimensions:
            imageWidth, imageHeight = self._getMaxDimensions("image")
        else:
            imageWidth, imageHeight = 0, 0
        bitmap = wx.Bitmap(1, 1)
        if drawing_properties["image"]:
            imageWidth, imageHeight = drawing_properties["image_size"]
            image:wx.Image = drawing_properties["image"].AdjustChannels(*drawing_properties["image_channels"])
            bitmap:wx.Bitmap = image.ConvertToBitmap()
            imageWidth, imageHeight = drawing_properties["image_size"]
            bitmap.SetSize(wx.Size(imageWidth, imageHeight))
        return imageWidth, imageHeight, bitmap


    def _getMaxDimensions(self, what:str):
        """what: image, border_width, """

        if (what == "image"):
            image_width = max(self._config.image_size_default[0],
                              self._config.image_size_pressed[0],
                              self._config.image_size_hover[0],
                              self._config.image_size_disabled[0])
            image_height = max(self._config.image_size_default[1],
                              self._config.image_size_pressed[1],
                              self._config.image_size_hover[1],
                              self._config.image_size_disabled[1])
            return image_width, image_height
        elif (what == "border_width"):
            return max(self._config.border_width_default,
                       self._config.border_width_hover,
                       self._config.border_width_pressed,
                       self._config.border_width_disabled)

        else:
            raise ValueError("_getMaxDimensions::Wrong \"what\" value.")


    def _getDefaultTextExtent(self, gcdc:wx.GCDC, text):
        """Get the text extent using the default font and facename."""
        gcdc.SetFont(wx.Font(self._config.text_font_size_default,
                             wx.FONTFAMILY_DEFAULT,
                             wx.FONTSTYLE_NORMAL,
                             wx.FONTWEIGHT_NORMAL,
                             faceName=self._config.text_font_facename_default))
        return gcdc.GetTextExtent(text)


    def unused_getIfImage(self):
        """Returns True if an image is set for any control state."""
        if (self._config.image_default or
            self._config.image_pressed or
            self._config.image_hover or
            self._config.image_disabled):
            return True
        else:
            return False
        