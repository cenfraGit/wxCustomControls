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
        

    def _getBrush(self, state:str, gc:wx.GraphicsContext) -> wx.Brush:
        gradient, background_colour = None, (255, 255, 255)
        if (state == "disabled"):
            gradient = self._config.background_linear_gradient_disabled
            background_colour = self._config.background_colour_disabled
        elif (state == "pressed"):
            gradient = self._config.background_linear_gradient_pressed
            background_colour = self._config.background_colour_pressed
        elif (state == "hover"):
            gradient = self._config.background_linear_gradient_hover
            background_colour = self._config.background_colour_hover
        elif (state == "default"):
            gradient = self._config.background_linear_gradient_default
            background_colour = self._config.background_colour_default

        if gradient:
            c1 = wx.Colour(*gradient[4])
            c2 = wx.Colour(*gradient[5])
            x1, y1, x2, y2, _, _ = gradient
            brush = gc.CreateLinearGradientBrush(x1, y1, x2, y2, c1, c2)
        else:
            brush = wx.Brush(background_colour)

        return brush


    def _getStateDrawingProperties(self, control_state:str, gc:wx.GraphicsContext):

        if control_state not in ["default", "pressed", "hover", "disabled"]:
            raise ValueError("getStateProperties::Invalid control_state.")

        pen = self._getPen(control_state) # takes care of borders
        brush = self._getBrush(control_state, gc) # takes care of background

        if (control_state == "default"):
            cursor = wx.Cursor(wx.CURSOR_ARROW)
            text_font_size = self._config.text_font_size_default
            text_font_facename = self._config.text_font_facename_default
            text_foreground_colour = self._config.text_foreground_colour_default
            corner_radius = self._config.corner_radius_default
            image = self._config.image_default
            image_channels = self._config.image_channels_default
            image_size = self._config.image_size_default
        elif (control_state == "pressed"):
            cursor = wx.Cursor(self._config.cursor_stockcursor_pressed)
            text_font_size = self._config.text_font_size_pressed
            text_font_facename = self._config.text_font_facename_pressed
            text_foreground_colour = self._config.text_foreground_colour_pressed
            corner_radius = self._config.corner_radius_pressed
            image = self._config.image_pressed
            image_channels = self._config.image_channels_pressed
            image_size = self._config.image_size_pressed
        elif (control_state == "hover"):
            cursor = wx.Cursor(self._config.cursor_stockcursor_hover)
            text_font_size = self._config.text_font_size_hover
            text_font_facename = self._config.text_font_facename_hover
            text_foreground_colour = self._config.text_foreground_colour_hover
            corner_radius = self._config.corner_radius_hover
            image = self._config.image_hover
            image_channels = self._config.image_channels_hover
            image_size = self._config.image_size_hover
        else: # disabled
            cursor = wx.Cursor(self._config.cursor_stockcursor_disabled)
            text_font_size = self._config.text_font_size_disabled
            text_font_facename = self._config.text_font_facename_disabled
            text_foreground_colour = self._config.text_foreground_colour_disabled
            corner_radius = self._config.corner_radius_disabled
            image = self._config.image_disabled
            image_channels = self._config.image_channels_disabled
            image_size = self._config.image_size_disabled

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


    def _getTextSideDimensions(self, text_separation:int, text_side,
                               textWidth:int, textHeight:int,
                               objectWidth:int, objectHeight:int):
        """Returns the dimensions of a rectangle depending on the
        arrangement of an object and its text_side (used in images and
        checkboxes)."""
        rectangleWidth, rectangleHeight = 0, 0
        if (text_side == "right" or text_side == "left"):
            rectangleWidth = objectWidth + text_separation + textWidth
            rectangleHeight = max(objectHeight, textHeight)
        elif (text_side == "up" or text_side == "down"):
            rectangleWidth = max(objectWidth, textWidth)
            rectangleHeight = objectHeight + text_separation + textHeight
        else:
            raise ValueError("text_side must be left, right, up or down.")
        return rectangleWidth, rectangleHeight


    def _performTextSideCalculation(self, drawing_rectangle:wx.Rect,
                                    text, text_separation:int, text_side,
                                    textWidth:int, textHeight:int,
                                    objectWidth:int, objectHeight:int):
        """Returns the coordinates for text and images/checkbox square
        depending on the text separation (the distance from the text
        to the the image or checkbox) and the side where the text
        should be displayed. The drawing rectangle is the rectangle
        area where the object and the text will be drawn.
        """

        textX, textY = 0, 0
        objectX, objectY = 0, 0

        r = drawing_rectangle # shorter alias for drawing rectangle
        
        # -------------------- if no text -------------------- #

        if (text == wx.EmptyString):
            # object in center if no text
            objectX = (r.GetWidth() // 2) - (objectWidth // 2)
            objectY = (r.GetHeight() // 2) - (objectHeight // 2)

        # ---------------- if dimensions are 0 ---------------- #

        elif (objectWidth == 0 or objectHeight == 0):
            # text in center if no object
            textX = r.GetX() + (r.GetWidth() // 2) - (textWidth // 2)
            textY = r.GetY() + (r.GetHeight() // 2) - (textHeight // 2)

        # -------------- if both text and object -------------- #

        else:

            text_separation = text_separation if text_separation else dip(6)
            
            if (text_side == "right"):
                objectX = (r.GetWidth() // 2) - ((objectWidth + textWidth + text_separation) // 2) 
                objectY = (r.GetHeight() // 2) - (objectHeight // 2)
                textX = objectX + objectWidth + text_separation
                textY = (r.GetHeight() // 2) - (textHeight // 2)
            elif (text_side == "left"):
                textX = (r.GetWidth() // 2) - ((objectWidth + textWidth + text_separation) // 2) 
                textY = (r.GetHeight() // 2) - (textHeight // 2)
                objectX = textX + textWidth + text_separation
                objectY = (r.GetHeight() // 2) - (objectHeight // 2)
            elif (text_side == "up"):
                textX = (r.GetWidth() // 2) - (textWidth // 2)
                textY = (r.GetHeight() // 2) - ((objectHeight + textHeight + text_separation) // 2)
                objectX = (r.GetWidth() // 2) - (objectWidth // 2)
                objectY = textY + textHeight + text_separation
            elif (text_side == "down"):
                objectX = (r.GetWidth() // 2) - (objectWidth // 2)
                objectY = (r.GetHeight() // 2) - ((objectHeight + textHeight + text_separation) // 2)
                textX = (r.GetWidth() // 2) - (textWidth // 2)
                textY = objectY + objectHeight
            else:
                raise ValueError("text_side must be left, right, up or down.")

        return textX, textY, objectX, objectY


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
                object1X = r.GetX() + (r.GetWidth() // 2) - ((object1Width + object1Width + separation) // 2)
                object1Y = r.GetY() + (r.GetHeight() // 2) - (object1Height // 2)
                object2X = object1X + object1Width + separation
                object2Y = r.GetY() + (r.GetHeight() // 2) - (object2Height // 2)
            elif (object2_side == "left"):
                object2X = r.GetX() + (r.GetWidth() // 2) - ((object1Width + object2Width + separation) // 2)
                object2Y = r.GetY() + (r.GetHeight() // 2) - (object2Height // 2)
                object1X = object2X + object2Width + separation
                object1Y = r.GetY() + (r.GetHeight() // 2) - (object1Height // 2)
            elif (object2_side == "up"):
                object2X = r.GetX() + (r.GetWidth() // 2) - (object2Width // 2)
                object2Y = r.GetY() + (r.GetHeight() // 2) - ((object1Height + object2Height + separation) // 2)
                object1X = r.GetX() + (r.GetWidth() // 2) - (object1Width // 2)
                object1Y = object1Y + object2Height + separation
            elif (object2_side == "down"):
                object1X = r.GetX() + (r.GetWidth() // 2) - (object1Width // 2)
                object1Y = r.GetY() + (r.GetHeight() // 2) - ((object1Height + object2Height + separation) // 2)
                object2X = r.GetX() + (r.GetWidth() // 2) - (object2Width // 2)
                object2Y = object1Y + object1Height
            else:
                raise ValueError("text_side must be left, right, up or down.")
            
        return object1X, object1Y, object2X, object2Y



    def _drawImageTextRectangle(self, rectangle:wx.Rect, text, textWidth, textHeight, bitmap, imageWidth, imageHeight, gcdc:wx.GCDC):
        """Draws an image and text (or either) in the specified rectangle. It assumes that the rectangle has enough space."""

        """

        textX, textY = 0, 0   # init 
        imageX, imageY = 0, 0 # init
        r = rectangle         # alias
        theresText:bool = (text != wx.EmptyString and text.strip() != "")
        theresImage:bool = (imageWidth != 0 and imageHeight != 0)

        if not theresText:
            # image in center
            imageX = r.GetX() + (r.GetWidth() // 2) - (imageWidth // 2)
            imageY = r.GetY() + (r.GetHeight() // 2) - (imageHeight // 2)

        elif not theresImage:
            # text in center
            textX = r.GetX() + (r.GetWidth() // 2) - (textWidth // 2)
            textY = r.GetY() + (r.GetHeight() // 2) - (textHeight // 2)

        else:
            
            text_separation = self._config.image_text_separation if self._config.image_text_separation else dip(6)
            
            if (self._config.image_text_side == "right"):
                imageX = r.GetX() + (r.GetWidth() // 2) - ((imageWidth + textWidth + text_separation) // 2)
                imageY = r.GetY() + (r.GetHeight() // 2) - (imageHeight // 2)
                textX = imageX + imageWidth + text_separation
                textY = r.GetY() + (r.GetHeight() // 2) - (textHeight // 2)
            elif (self._config.image_text_side == "left"):
                textX = r.GetX() + (r.GetWidth() // 2) - ((imageWidth + textWidth + text_separation) // 2)
                textY = r.GetY() + (r.GetHeight() // 2) - (textHeight // 2)
                imageX = textX + textWidth + text_separation
                imageY = r.GetY() + (r.GetHeight() // 2) - (imageHeight // 2)
            elif (self._config.image_text_side == "up"):
                textX = r.GetX() + (r.GetWidth() // 2) - (textWidth // 2)
                textY = r.GetY() + (r.GetHeight() // 2) - ((imageHeight + textHeight + text_separation) // 2)
                imageX = r.GetX() + (r.GetWidth() // 2) - (imageWidth // 2)
                imageY = textY + textHeight + text_separation
            elif (self._config.image_text_side == "down"):
                imageX = r.GetX() + (r.GetWidth() // 2) - (imageWidth // 2)
                imageY = r.GetY() + (r.GetHeight() // 2) - ((imageHeight + textHeight + text_separation) // 2)
                textX = r.GetX() + (r.GetWidth() // 2) - (textWidth // 2)
                textY = imageY + imageHeight
            else:
                raise ValueError("text_side must be left, right, up or down.")
        """

        imageX, imageY, textX, textY = self._performObjectSideCalculation(rectangle,
                                                                          imageWidth, imageHeight,
                                                                          textWidth, textHeight,
                                                                          self._config.image_text_separation,
                                                                          self._config.image_text_side)
        
        theresText:bool = (text != wx.EmptyString and text.strip() != "")
        theresImage:bool = (imageWidth != 0 and imageHeight != 0)
            
        # draw
        if theresText:
            gcdc.DrawText(text, textX, textY)
        if theresImage:
            gcdc.DrawBitmap(bitmap, imageX, imageY)



    def _getTextDimensions(self, string, gcdc, drawing_properties):        
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
        imageWidth, imageHeight = 0, 0
        bitmap = wx.Bitmap(1, 1)
        if drawing_properties["image"]:
            imageWidth, imageHeight = drawing_properties["image_size"]
            # convert image to bitmap
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


    def _getIfImage(self):
        """Returns True if an image is set for any control state."""
        if (self._config.image_default or
            self._config.image_pressed or
            self._config.image_hover or
            self._config.image_disabled):
            return True
        else:
            return False

