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

        # ---------------- checkbox or switch ---------------- #

        sidePadding = self._getMaxDimensions("border_width")




        # do performTextSideCalculation without text

        # checkbox symbol -> objectWidth, objectHeight
        # image text rectangle -> textWidth, textHeight
        # checkbox separation -> text_separation
        # checkbox_text_side -> text_side

        textWidth, textHeight = self._getTextDimensions(self._Label, gcdc, drawing_properties)

        imageWidth, imageHeight, bitmap = self._getBitmapAndDimensions(drawing_properties)

        imageTextRectWidth, imageTextRectHeight = self._getTextSideDimensions(self._config.image_text_separation, 
                                                                              self._config.image_text_side, 
                                                                              textWidth, textHeight, 
                                                                              imageWidth, imageHeight)

        checkboxX, checkBoxY, imageTextRectX, imageTextRectY = self._performObjectSideCalculation(controlRect, 
                                                                                                  self._config.checkbox_width, self._config.checkbox_height, 
                                                                                                  imageTextRectWidth, imageTextRectHeight, 
                                                                                                  self._config.checkbox_text_separation, 
                                                                                                  self._config.checkbox_text_side)

        if self._config.switch_appearance:
            pass
        else:

            # --- calculate checkbox position based on textside --- #
            #boxX = sidePadding if (self._config.checkbox_text_side == "right") else (controlRect.GetWidth() - sidePadding - self._config.checkbox_width)
            #boxY = (controlRect.GetHeight() // 2) - (self._config.checkbox_height // 2)

            boxX = checkboxX
            boxY = checkBoxY

            # -- create the rectangle representing the checkbox -- #
            boxRectangle = wx.Rect(boxX, boxY, self._config.checkbox_width, self._config.checkbox_height)

            # -------------- if checkbox is selected -------------- #
            if self._Value:

                # -------------- draw selected rectangle -------------- #
                gcdc.SetPen(wx.TRANSPARENT_PEN) 
                gc.SetBrush(wx.Brush(wx.Colour(self._config.background_colour_active_default)))
                gcdc.DrawRoundedRectangle(boxRectangle, radius=drawing_properties["corner_radius"])

                # ------ checkmark rectangle delimiter (smaller) ------ #
                checkRect:wx.Rect = copy(boxRectangle).Deflate(int(self._config.checkbox_active_deflate*1.2),
                                                               int(self._config.checkbox_active_deflate*1.3))

                # ------------- check mark pen and brush ------------- #
                gcdc.SetPen(wx.Pen(wx.WHITE, width=2))
                gcdc.SetBrush(wx.TRANSPARENT_BRUSH)
                
                # --------------- draw check with path --------------- #
                path:wx.GraphicsPath = gc.CreatePath()
                path.MoveToPoint(checkRect.GetX(), checkRect.GetY() + (checkRect.GetHeight() // 1.5))
                path.AddLineToPoint(checkRect.GetX() + (checkRect.GetWidth() //2 ), checkRect.GetY() + checkRect.GetHeight())
                path.AddLineToPoint(*checkRect.GetTopRight())
                gc.StrokePath(path)
                
            # --------------- draw normal checkbox --------------- #
            else:
                gcdc.SetPen(drawing_properties["pen"])
                gc.SetBrush(drawing_properties["brush"])
                gcdc.DrawRoundedRectangle(boxRectangle, radius=drawing_properties["corner_radius"])


        new = wx.Rect(imageTextRectX, imageTextRectY, imageTextRectWidth, imageTextRectHeight)


        self._drawImageTextRectangle(new, self._Label, textWidth, textHeight, bitmap, imageWidth, imageHeight, gcdc)








        """
        
        
        # -------------- if checkbox appearance -------------- #
        if not self._config.switch_appearance:

            # --- calculate checkbox position based on textside --- #
            boxX = sidePadding if (self._config.checkbox_text_side == "right") else (controlRect.GetWidth() - sidePadding - self._config.checkbox_width)
            boxY = (controlRect.GetHeight() // 2) - (self._config.checkbox_height // 2)
            # -- create the rectangle representing the checkbox -- #
            boxRectangle = wx.Rect(boxX, boxY, self._config.checkbox_width, self._config.checkbox_height)

            # -------------- if checkbox is selected -------------- #
            if self._Value:

                # -------------- draw selected rectangle -------------- #
                gcdc.SetPen(wx.TRANSPARENT_PEN) 
                gc.SetBrush(wx.Brush(wx.Colour(self._config.background_colour_active_default)))
                gcdc.DrawRoundedRectangle(boxRectangle, radius=drawing_properties["corner_radius"])

                # ------ checkmark rectangle delimiter (smaller) ------ #
                checkRect:wx.Rect = copy(boxRectangle).Deflate(int(self._config.checkbox_active_deflate*1.2),
                                                               int(self._config.checkbox_active_deflate*1.3))

                # ------------- check mark pen and brush ------------- #
                gcdc.SetPen(wx.Pen(wx.WHITE, width=2))
                gcdc.SetBrush(wx.TRANSPARENT_BRUSH)
                
                # --------------- draw check with path --------------- #
                path:wx.GraphicsPath = gc.CreatePath()
                path.MoveToPoint(checkRect.GetX(), checkRect.GetY() + (checkRect.GetHeight() // 1.5))
                path.AddLineToPoint(checkRect.GetX() + (checkRect.GetWidth() //2 ), checkRect.GetY() + checkRect.GetHeight())
                path.AddLineToPoint(*checkRect.GetTopRight())
                gc.StrokePath(path)
                
            # --------------- draw normal checkbox --------------- #
            else:
                gcdc.SetPen(drawing_properties["pen"])
                gc.SetBrush(drawing_properties["brush"])
                gcdc.DrawRoundedRectangle(boxRectangle, radius=drawing_properties["corner_radius"])
                

        # --------------- if switch appearance --------------- #
        else: # if switch appearance

            # calculate switch position based on textside
            boxX = sidePadding if (self._config.checkbox_text_side == "right") else (controlRect.GetWidth() - sidePadding - self._config.switch_width)
            boxY = (controlRect.GetHeight() // 2) - (self._config.switch_height // 2)
            # create rectangle representing switch
            boxRectangle = wx.Rect(boxX, boxY, self._config.switch_width, self._config.switch_height)

            # draw switch background
            gcdc.SetPen(drawing_properties["pen"])
            if self._Value:
                gcdc.SetBrush(wx.Brush(wx.Colour(self._config.bg_active_default)))
            else:
                gcdc.SetBrush(drawing_properties["brush"])
            gcdc.DrawRoundedRectangle(boxRectangle, radius=drawing_properties["corner_radius"])
            
            if self._Value: # draw switch indicator on the right side
                selectionX = boxRectangle.GetX() + boxRectangle.GetWidth() - self._config.switch_height
                selectionY = boxRectangle.GetY()
            else: # draw to the left side
                selectionX = boxRectangle.GetX()
                selectionY = boxRectangle.GetY()

            # draw switch on/off indicator
            if self._config.switch_selector_border_width:
                pen = wx.Pen(wx.Colour(*self._config.switch_selector_border_colour),
                             width=self._config.switch_selector_border_width)
            else:
                pen = wx.TRANSPARENT_PEN
            
            gcdc.SetPen(pen)
            gcdc.SetBrush(wx.Brush(wx.Colour(*drawing_properties["fg_colour"])))
            
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

        # -------------------- text dimensions ---------------------- #

        textWidth, textHeight = self._getTextDimensions(self._Label, gcdc, drawing_properties)

        # ----------------- image dimensions ----------------- #
        
        imageWidth, imageHeight, bitmap = self._getBitmapAndDimensions(drawing_properties)

        # ----------------------- draw ----------------------- #


        maxWidth, maxHeight = self._getMaxDimensions("image")

        

        if self._config.switch_appearance:
            selectorWidth = self._config.switch_width
            selectorHeight = self._config.switch_height
        else:
            selectorWidth = self._config.checkbox_width
            selectorHeight = self._config.checkbox_height

        if (self._config.checkbox_text_side == "right"):
            textImageRectangleX = sidePadding + selectorWidth + self._config.checkbox_text_separation
            textImageRectangleY = sidePadding


        # ------- calculate text image rectangle width ------- #

        textImageRectangleWidth, textImageRectangleHeight = self._getTextSideDimensions(self._config.image_text_separation,
                                                                                        self._config.image_text_side,
                                                                                        textWidth, textHeight,
                                                                                        imageWidth, imageHeight)
        
        textImageRectangle = wx.Rect(textImageRectangleX,
                                     textImageRectangleY,
                                     textImageRectangleWidth,
                                     textImageRectangleHeight)
        
        
        gc.SetPen(wx.BLUE_PEN)
        gcdc.SetBrush(wx.BLUE_BRUSH)
        gcdc.DrawRectangle(textImageRectangle)

        self._drawImageTextRectangle(textImageRectangle,
                                     self._Label,
                                     textWidth, textHeight,
                                     bitmap, imageWidth, imageHeight,
                                     gcdc)


        """
        


        
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
                 
    
