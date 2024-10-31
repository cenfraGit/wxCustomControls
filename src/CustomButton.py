# CustomButton.py
# wxCustomControls
# A customizable button.
# 29/oct/2024


import wx
from ._CustomControl import CustomControl
from .utils.dip import dip
from .functions.getConfig import getConfig
from .functions.getStateDrawingProperties import getStateDrawingProperties
from .functions.getImageTextCoordinates import getImageTextCoordinates


class CustomButton(CustomControl):
    def __init__(self, parent, id=wx.ID_ANY, label=wx.EmptyString,
                 pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.NO_BORDER,
                 validator=wx.DefaultValidator, name=wx.ControlNameStr,
                 config=None, **kwargs):

        # ---------------- control attributes ---------------- #

        self.__Label = label

        # ------------------- init control ------------------- #

        super().__init__(parent, id, pos, size, style, validator, name, config, **kwargs)

        # ---------------------- events ---------------------- #

        self.Bind(wx.EVT_PAINT, self.__OnPaint)
        self.Bind(wx.EVT_LEFT_DCLICK, self.__OnLeftDown)
        self.Bind(wx.EVT_LEFT_DOWN, self.__OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.__OnLeftUp)


    def SetLabel(self, label:str):
        self.__Label = label
        self.Refresh()


    def GetLabel(self):
        return self.__Label


    def __OnPaint(self, event):

        # --------------------- contexts --------------------- #

        dc = wx.BufferedPaintDC(self)
        gcdc = wx.GCDC(dc)
        gc:wx.GraphicsContext = gcdc.GetGraphicsContext()
        gcdc.Clear()

        # ---------------- drawing properties ---------------- #
        # get drawing properties depending on state

        drawing_properties = getStateDrawingProperties(self.GetStateAsString(),
                                                       self._config, gc)

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
        # we set the brush to the gc because the gcdc api does not
        # support gradient brushes.
        gc.SetBrush(drawing_properties["brush"])

        gcdc.DrawRoundedRectangle(buttonRectangle, drawing_properties["corner_radius"])

        # ------------------ text dimensions ------------------ #

        textWidth, textHeight = 0, 0
        if (self.__Label != wx.EmptyString):
            gc.SetFont(wx.Font(drawing_properties["text_font_size"],
                               wx.FONTFAMILY_DEFAULT,
                               wx.FONTSTYLE_NORMAL,
                               wx.FONTWEIGHT_NORMAL,
                               faceName=drawing_properties["text_font_facename"]), drawing_properties["text_foreground_colour"])
            textWidth, textHeight = gcdc.GetTextExtent(self.__Label)

        # ----------------- image dimensions ----------------- #

        imageWidth, imageHeight = 0, 0
        bitmap = None
        if drawing_properties["image"]:
            imageWidth, imageHeight = drawing_properties["image_size"]
            # convert image to bitmap
            image:wx.Image = drawing_properties["image"].AdjustChannels(*drawing_properties["image_channels"])
            bitmap:wx.Bitmap = image.ConvertToBitmap()
            imageWidth, imageHeight = drawing_properties["image_size"]
            bitmap.SetSize(wx.Size(imageWidth, imageHeight))

        # ----------------------- draw ----------------------- #

        imageX, imageY, textX, textY = getImageTextCoordinates(buttonRectangle,
                                                               self.__Label, self._config,
                                                               imageWidth, imageHeight,
                                                               textWidth, textHeight)

        if (self.__Label != wx.EmptyString):
            gcdc.DrawText(self.__Label, textX, textY)

        if drawing_properties["image"]:
            gcdc.DrawBitmap(bitmap, imageX, imageY)

        

    def DoGetBestClientSize(self):
        pass


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
        event.Skip()


    # def __OnMouseCaptureLost(self, event):
    #     if self._Pressed:
    #         self._Pressed = False
    #         print("Mouse capture lost")
    #     event.Skip()

    
