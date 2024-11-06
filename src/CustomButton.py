# CustomButton.py
# wxCustomControls
# A customizable button.
# 29/oct/2024


import wx
from .base._CustomControl import CustomControl
from .utils.dip import dip


class CustomButton(CustomControl):
    def __init__(self, parent, id=wx.ID_ANY, label=wx.EmptyString,
                 pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.NO_BORDER,
                 validator=wx.DefaultValidator, name=wx.ControlNameStr,
                 config=None, **kwargs):

        # ---------------- control attributes ---------------- #
        
        kwargs["label"] = label

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

        # control background
        gcdc.SetPen(wx.TRANSPARENT_PEN)
        gcdc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour()))
        gcdc.DrawRectangle(controlRect)

        # ----------------- button rectangle ----------------- #

        buttonRectangle = controlRect.Deflate(drawing_properties["pen"].GetWidth(),
                                              drawing_properties["pen"].GetWidth())

        gcdc.SetPen(drawing_properties["pen"])
        gc.SetBrush(drawing_properties["brush_background"])
        gcdc.DrawRoundedRectangle(buttonRectangle, drawing_properties["corner_radius"])

        # ------------------ text dimensions ------------------ #
        
        textWidth, textHeight = self._getTextDimensions(gcdc, self._Label, drawing_properties)

        # ----------------- image dimensions ----------------- #
        
        imageWidth, imageHeight, bitmap = self._getBitmapAndDimensions(drawing_properties)

        # ----------------------- draw ----------------------- #

        self._drawImageTextRectangle(gcdc, buttonRectangle,
                                     self._Label,
                                     textWidth, textHeight,
                                     bitmap, imageWidth, imageHeight)


    def DoGetBestClientSize(self) -> wx.Size:
        
        dc = wx.ClientDC(self)
        gcdc:wx.GCDC = wx.GCDC(dc)

        # image = self._getIfImage()
        textWidth, textHeight = self._getDefaultTextExtent(gcdc, self._Label)
        imageWidth, imageHeight = self._getMaxDimensions("image")
        text_separation = self._config.image_text_separation if self._config.image_text_separation else dip(6)
        padding_horizontal = dip(10)
        padding_vertical = dip(5)

        width, height = self._getObjectSideDimensions(imageWidth, imageHeight,
                                                      textWidth, textHeight,text_separation,
                                                      self._config.image_text_side)
        width += 2 * padding_horizontal
        height += 2 * padding_vertical

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
            self.Refresh()
            if self._Hover:
                wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.GetId()))
        event.Skip()

