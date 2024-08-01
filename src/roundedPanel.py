import wx
from .functions.dip import dip


class RoundedPanel(wx.Panel):
    """ A panel with rounded corners. """

    def __init__(self, radius:int=5,
                 backgroundColour:wx.Colour=wx.WHITE,
                 borderColour:wx.Colour=wx.WHITE, borderWidth:int=1,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ------------------ attributes ------------------ #
        
        self._Radius = dip(radius)
        self._BackgroundColour = backgroundColour
        self._BorderColour = borderColour
        self._BorderWidth = borderWidth
        
        self._MarginAllSides = self._BorderWidth

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        # -------------------- events -------------------- #

        self.Bind(wx.EVT_PAINT, self.OnPaint)


    def GetBackgroundColour(self):
        return self._BackgroundColour


    def SetBackgroundColour(self, colour:wx.Colour):
        self._BackgroundColour = colour
        self.Refresh()


    def SetBorderColour(self, colour:wx.Colour):
        self._BorderColour = colour
        self.Refresh()


    def SetBorderWidth(self, width:int):
        """Sets the width of the border. Set to 0 if you want no
        border."""
        # we will use a _BorderWidth of 0 to indicate that a
        # TRANSPARENT_PEN should be used when drawing
        self._BorderWidth = width
        self.Refresh()


    def OnPaint(self, event):
        """ Handles the paint event. """

        # create device context
        dc = wx.AutoBufferedPaintDC(self)
        #dc.Clear()

        # create graphics context
        gc = wx.GraphicsContext.Create(dc)

        # get panel rectangle 
        rect = self.GetClientRect()
        
        # convert to values used by gc
        x, y = rect.GetX(), rect.GetY()
        width, height = rect.GetWidth(), rect.GetHeight()

        # draw the background (for the corners)
        gc.SetPen(wx.TRANSPARENT_PEN)
        gc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour()))
        gc.DrawRectangle(x, y, width, height)

        

        # --------------------- pen --------------------- #

        # if the border width is 0, we will simply not draw a border
        # by using a transparent pen.

        if (self._BorderWidth == 0):
            gc.SetPen(wx.TRANSPARENT_PEN)
        else:
            gc.SetPen(wx.Pen(colour=self._BorderColour,
                             width=self._BorderWidth))

        # -------------------- brush -------------------- #

        gc.SetBrush(wx.Brush(self._BackgroundColour))

        # ------------ drawing the rectangle ------------ #

        # we will create a smaller rectangle in order for it to be
        # rendered correctly.
        panelRect = rect.Deflate(self._MarginAllSides,
                                 self._MarginAllSides)

        gc.DrawRoundedRectangle(panelRect.GetX(),
                                panelRect.GetY(),
                                panelRect.GetWidth(),
                                panelRect.GetHeight(),
                                radius=self._Radius)

        
