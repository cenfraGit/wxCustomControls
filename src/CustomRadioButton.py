# CustomCheckButton.py
# wxCustomControls
# A customizable radiobutton.
# 6/nov/2024


import wx
from copy import copy
from .base._CustomControl import CustomControl
from .utils.dip import dip
import builtins


class CustomRadioButton(CustomControl):

    groups = {} # keep track of radio button groups

    def __init__(self, parent, id=wx.ID_ANY, label=wx.EmptyString,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=0, validator=wx.DefaultValidator,
                 name=wx.RadioButtonNameStr, value=False, config=None,
                 **kwargs):

        # ---------------- control attributes ---------------- #

        kwargs["label"] = label
        kwargs["value"] = value

        # ------------------- init control ------------------- #

        super().__init__(parent, id, pos, size, style, validator, name, config, **kwargs)

        # ------------ check if starts a new group ------------ #

        if style & wx.RB_GROUP or not CustomRadioButton.groups:
            self.group_id = builtins.id(self)
            CustomRadioButton.groups[self.group_id] = []
        else:
            self.group_id = list(CustomRadioButton.groups.keys())[-1]

        CustomRadioButton.groups[self.group_id].append(self)

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
        gcdc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour()))
        gcdc.DrawRectangle(controlRect)

        # ------------------ get dimensions ------------------ #

        textWidth, textHeight = self._getTextDimensions(gcdc, self._Label,  drawing_properties)
        imageWidth, imageHeight, bitmap = self._getBitmapAndDimensions(drawing_properties)
        imageTextRectWidth, imageTextRectHeight = self._getObjectSideDimensions(imageWidth, imageHeight,
                                                                                textWidth, textHeight, 
                                                                                self._config.image_text_separation, 
                                                                                self._config.image_text_side)

        # get coordinates of selector and imageTextRect depending on the layout and dimensions
        radiobuttonX, radiobuttonY, imageTextRectX, imageTextRectY = self._performObjectSideCalculation(controlRect, 
                                                                                                  self._config.radiobutton_diameter,
                                                                                                  self._config.radiobutton_diameter,
                                                                                                  imageTextRectWidth, imageTextRectHeight, 
                                                                                                  self._config.checkbox_text_separation, 
                                                                                                  self._config.checkbox_text_side)
        
        # ----------------- create rectangles ----------------- #
        
        imageTextRect = wx.Rect(imageTextRectX, imageTextRectY, imageTextRectWidth, imageTextRectHeight)
        radiobuttonRectangle = wx.Rect(radiobuttonX, radiobuttonY, self._config.radiobutton_diameter, self._config.radiobutton_diameter)

        # ------------------ draw rectangles ------------------ #

        # draw text and image
        self._drawImageTextRectangle(gcdc, imageTextRect, self._Label, textWidth, textHeight, bitmap, imageWidth, imageHeight)

        # draw background for selector depending on state
        if self._Value:
            gcdc.SetPen(wx.TRANSPARENT_PEN)
            gc.SetBrush(wx.Brush(wx.Colour(drawing_properties["background_colour_active"])))
        else:
            gcdc.SetPen(drawing_properties["pen"])
            gc.SetBrush(drawing_properties["brush_background"])

        # calculate the center of the radiobutton circle
        radiobuttonCenterX = radiobuttonRectangle.GetX() + self._config.radiobutton_diameter//2
        radiobuttonCenterY = radiobuttonRectangle.GetY() + self._config.radiobutton_diameter//2        
        gcdc.DrawCircle(radiobuttonCenterX, radiobuttonCenterY, self._config.radiobutton_diameter//2)

        if self._Value:
            gc.SetBrush(drawing_properties["brush_foreground"])
            gcdc.DrawCircle(radiobuttonCenterX, radiobuttonCenterY, self._config.radiobutton_diameter//5)
            

    def DoGetBestClientSize(self) -> wx.Size:

        dc = wx.ClientDC(self)
        gcdc:wx.GCDC = wx.GCDC(dc)

        textWidth, textHeight = self._getDefaultTextExtent(gcdc, self._Label)
        imageWidth, imageHeight = self._getMaxDimensions("image")
        sidePadding = self._getMaxDimensions("border_width")
        text_separation = self._config.image_text_separation if self._config.image_text_separation else dip(6)
        textImageWidth, textImageHeight = self._getObjectSideDimensions(imageWidth, imageHeight,
                                                                        textWidth, textHeight,
                                                                        text_separation,
                                                                        self._config.image_text_side)
        # dimensions for whole control
        width, height = self._getObjectSideDimensions(self._config.radiobutton_diameter,
                                                      self._config.radiobutton_diameter,
                                                      textImageWidth, textImageHeight,
                                                      self._config.checkbox_text_separation, 
                                                      self._config.checkbox_text_side)
        width += 2 * sidePadding
        height += 2 * sidePadding
        return wx.Size(int(width), int(height))


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
                # deselect other radio buttons in group
                for rb in CustomRadioButton.groups[self.group_id]:
                    if rb._Value:
                        rb._Value = False
                        rb.Refresh()
                # set the value of this radiobutton to true
                self._Value = True
                wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_RADIOBUTTON.typeId, self.GetId()))
            self.Refresh()
        event.Skip()

