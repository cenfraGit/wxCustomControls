# CustomCheckBox.py
# wxCustomControls
# A customizable checkbox.
# 30/oct/2024


import wx
from copy import copy
from ._CustomControl import CustomControl
from .utils.dip import dip


class CustomCheckBox(CustomControl):
    def __init__(self, parent, id=wx.ID_ANY, label=wx.EmptyString,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.NO_BORDER, validator=wx.DefaultValidator,
                 name=wx.CheckBoxNameStr, value=False, config=None,
                 **kwargs):

        # ---------------- control attributes ---------------- #

        kwargs["label"] = label
        kwargs["value"] = value

        # ------------------- init control ------------------- #

        super().__init__(parent, id, pos, size, style, validator, name, config, **kwargs)

        # ---------------------- events ---------------------- #

        self.Bind(wx.EVT_PAINT, self.__OnPaint)
        self.Bind(wx.EVT_LEFT_DCLICK, self.__OnLeftDown)
        self.Bind(wx.EVT_LEFT_DOWN, self.__OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.__OnLeftUp)


    def __OnPaint(self, event):

        # --------------------- contexts --------------------- #
        
        gcdc, gc = self._getDrawingContexts()

        # ---------------- drawing properties ---------------- #

        drawing_properties = self._getStateDrawingProperties(self.GetStateAsString(), gc)

        # ---------------------- cursor ---------------------- #
        
        self.SetCursor(drawing_properties["cursor"])

        # ------------ drawing area and background ------------ #

        controlRect:wx.Rect = self.GetClientRect() # control area

        gcdc.SetPen(wx.TRANSPARENT_PEN)
        #gcdc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour()))
        gcdc.SetBrush(wx.GREEN_BRUSH)
        gcdc.DrawRectangle(controlRect)


        sidePadding = self._getMaxDimensions("border_width")

        # get text and image dimensions
        textWidth, textHeight = self._getTextDimensions(gcdc, self._Label,  drawing_properties)
        imageWidth, imageHeight, bitmap = self._getBitmapAndDimensions(drawing_properties)

        # get the dimensions of the rectangle with the image and text
        imageTextRectWidth, imageTextRectHeight = self._getTextSideDimensions(textWidth, textHeight, 
                                                                              imageWidth, imageHeight,
                                                                              self._config.image_text_separation, 
                                                                              self._config.image_text_side,)

        # get the dimensions of the current type of selector (checkbox or switch)
        selectorWidth  = self._config.switch_width  if self._config.switch_appearance else self._config.checkbox_width
        selectorHeight = self._config.switch_height if self._config.switch_appearance else self._config.checkbox_height

        # get coordinates of objects depending on the layout and dimensions
        selectorX, selectorY, imageTextRectX, imageTextRectY = self._performObjectSideCalculation(controlRect, 
                                                                                                  selectorWidth, selectorHeight, 
                                                                                                  imageTextRectWidth, imageTextRectHeight, 
                                                                                                  self._config.checkbox_text_separation, 
                                                                                                  self._config.checkbox_text_side)
        
        # create the rectangle for the text and the image
        imageTextRect = wx.Rect(imageTextRectX, imageTextRectY, imageTextRectWidth, imageTextRectHeight)

        # create the rectangle for the selector (either checkbox or switch)
        selectorRectangle = wx.Rect(selectorX, selectorY, selectorWidth, selectorHeight)

        
        self._drawImageTextRectangle(gcdc, imageTextRect, self._Label, textWidth, textHeight, bitmap, imageWidth, imageHeight)


        # ---------------------- draw background for selector depending on state ------------------------ #

        if self._Value:
            gcdc.SetPen(wx.TRANSPARENT_PEN)
            gc.SetBrush(wx.Brush(wx.Colour(drawing_properties["background_colour_active"])))
        else:
            gcdc.SetPen(drawing_properties["pen"])
            gc.SetBrush(drawing_properties["brush"])
        gcdc.DrawRoundedRectangle(selectorRectangle, radius=drawing_properties["corner_radius"])


        if (self._Value and not self._config.switch_appearance): # if checkbox is active
            # ------ checkmark rectangle delimiter (smaller) ------ #
            checkRect:wx.Rect = copy(selectorRectangle).Deflate(int(self._config.checkbox_active_deflate*1.2), 
                                                                int(self._config.checkbox_active_deflate*1.3))
            gcdc.SetPen(wx.Pen(wx.WHITE, width=2))
            gcdc.SetBrush(wx.TRANSPARENT_BRUSH)
            # draw checkmark
            path:wx.GraphicsPath = gc.CreatePath()
            path.MoveToPoint(checkRect.GetX(), checkRect.GetY() + (checkRect.GetHeight() // 1.5))
            path.AddLineToPoint(checkRect.GetX() + (checkRect.GetWidth() //2 ), checkRect.GetY() + checkRect.GetHeight())
            path.AddLineToPoint(*checkRect.GetTopRight())
            gc.StrokePath(path)
        
        if (self._config.switch_appearance):

            if self._Value: # draw switch indicator on the right side
                selectionX = selectorRectangle.GetX() + selectorRectangle.GetWidth() - self._config.switch_height
                selectionY = selectorRectangle.GetY()
            else: # draw to the left side
                selectionX = selectorRectangle.GetX()
                selectionY = selectorRectangle.GetY()

            # draw switch on/off indicator
            if self._config.switch_selector_border_width:
                pen = wx.Pen(wx.Colour(*self._config.switch_selector_border_colour),
                            width=self._config.switch_selector_border_width)
            else:
                pen = wx.TRANSPARENT_PEN
            
            gcdc.SetPen(pen)
            #gcdc.SetBrush(wx.Brush(wx.Colour(*drawing_properties["fg_colour"])))
            gcdc.SetBrush(wx.Brush(wx.WHITE))
            
            if self._config.switch_rounded:
                gcdc.DrawEllipse(selectionX + self._config.switch_selector_padding,
                            selectionY + self._config.switch_selector_padding,
                            self._config.switch_height - (2 * self._config.switch_selector_padding),
                            self._config.switch_height - (2 * self._config.switch_selector_padding))
            else:
                gcdc.DrawRoundedRectangle(selectionX + self._config.switch_selector_padding,
                                        selectionY + self._config.switch_selector_padding,
                                        self._config.switch_height - (2 * self._config.switch_selector_padding),
                                        self._config.switch_height - (2 * self._config.switch_selector_padding),
                                        self._config.switch_radius)








    def DoGetBestClientSize(self):
        # helps sizer determine correct size of control.
        pass

        # # contexts
        # dc = wx.ClientDC(self)
        # gcdc:wx.GCDC = wx.GCDC(dc)

        # # set font to get dimensions
        # gcdc.SetFont(wx.Font(self._config.text_font_size_default,
        #                      wx.FONTFAMILY_DEFAULT,
        #                      wx.FONTSTYLE_NORMAL,
        #                      wx.FONTWEIGHT_NORMAL,
        #                      faceName=self._config.text_font_facename_default))
        # textWidth, textHeight = gcdc.GetTextExtent(self.__Label)

        # # get dimensions from largest image

        # image = self._config.image_default or self._config.image_pressed or self._config.image_hover or self._config.image_disabled
        # image_width = max(self._config.image_size_default[0],
        #                   self._config.image_size_pressed[0],
        #                   self._config.image_size_hover[0],
        #                   self._config.image_size_disabled[0])
        # image_height = max(self._config.image_size_default[1],
        #                    self._config.image_size_pressed[1],
        #                    self._config.image_size_hover[1],
        #                    self._config.image_size_disabled[1])
        
        # # separation between image and text
        # text_separation = self._config.image_text_separation if self._config.image_text_separation else dip(6)

        # padding_horizontal = dip(10)
        # padding_vertical = dip(5)

        # if image:
        #     if (self._config.text_side == "left") or (self._config.text_side == "right"):
        #         width = image_width + text_separation + textWidth + (2 * padding_horizontal)
        #         height = max(image_height, textHeight) + (2 * padding_vertical)
        #     elif (self._config.text_side == "up") or (self._config.text_side == "down"):
        #         width = max(image_width, textWidth) + (2 * padding_horizontal)
        #         height = image_height + text_separation + textHeight + (2 * padding_vertical)
        #     else:
        #         raise ValueError("text_side must be left, right, up or down.")
        # else:
        #     width = padding_horizontal * 2 + textWidth
        #     height = padding_vertical * 2 + textHeight

        # return wx.Size(int(width), int(height))


    def __OnLeftDown(self, event):
        if not self._Pressed:
            self.CaptureMouse()
            self._Pressed = True
            self.Refresh()
        event.Skip()


    def __OnLeftUp(self, event):
        if self._Pressed:
            self.ReleaseMouse()
            self._Pressed = False
            if self._Hover:
                self._Value = not self._Value
                wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_CHECKBOX.typeId, self.GetId()))                
            self.Refresh()
        event.Skip()
                 
    
