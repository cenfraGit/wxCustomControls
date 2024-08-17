import wx
from wx.lib.scrolledpanel import ScrolledPanel
from .controlConfig import ControlConfig
from .functions.getPenBrush import getPen, getBrush
from .functions.dip import dip
from copy import copy


class CustomScrolledWindow(wx.Window):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, 
                 config=None, **kwargs):
        
        super().__init__(parent=parent, id=id, pos=pos, style=style)

        # --------------- check for config --------------- #
        # if the user does not specify a config object, create
        # one and update with kwargs
        self.config:ControlConfig = copy(config) if config else self.__GetDefaultConfig()
        if kwargs:
            self.config.update(**kwargs)

        # for bottom right square
        self.SetBackgroundColour(self.config.bg_colour)

        # ------------ create scrolled panel ------------ #

        self._scrolledPanel = ScrolledPanel(parent=self)
        self._scrolledPanel.SetupScrolling(self.config.scrollX, self.config.scrollY, self.config.scrollUnitsX, self.config.scrollUnitsY)
        self._scrolledPanel.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_NEVER)
        self._scrolledPanel.SetBackgroundColour(wx.Colour(230, 230, 230))


        # ------------------ attributes ------------------ #
        
        self._LeftIsDownVertical = False
        self._LeftIsDownHorizontal = False

        self._VerticalScrollbarRectangle = wx.Rect(0, 0, 0, 0)
        self._HorizontalScrollbarRectangle = wx.Rect(0, 0, 0, 0)

        self._VerticalBarTopY = 0
        self._VerticalBarHeight = 0

        self._HorizontalBarTopY = 0
        self._HorizontalBarHeight = 0

        self._Pressed = False
        self._MouseHover = False


        # ---------------- default values ---------------- #
        
        self._ScrollbarWidth = self.config.scrollbar_width if self.config.scrollbar_width else dip(15)
        self._ScrollbarPadding = self.config.scrollbar_padding if self.config.scrollbar_padding else dip(3)


        # -------------- scrollbar windows -------------- #
        

        self._VerticalScrollbar = wx.Window(parent=self, size=(self._ScrollbarWidth, -1))
        self._VerticalScrollbar.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        
        self._HorizontalScrollbar = wx.Window(parent=self, size=(-1, self._ScrollbarWidth))
        self._HorizontalScrollbar.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        # -------------------- sizer -------------------- #

        self._sizer = wx.GridBagSizer()
        self._sizer.Add(self._scrolledPanel, pos=(0, 0), span=(1, 1), flag=wx.EXPAND)
        self._sizer.Add(window=self._VerticalScrollbar, pos=(0, 1), span=(1, 1), flag=wx.EXPAND)
        self._sizer.Add(window=self._HorizontalScrollbar, pos=(1, 0), span=(1, 1), flag=wx.EXPAND)

        self._sizer.AddGrowableCol(0, 1)
        self._sizer.AddGrowableRow(0, 1)

        self.SetSizer(self._sizer)

        # -------------------- events -------------------- #

        # bind size event to redraw scrollbars
        self.Bind(wx.EVT_SIZE, self.__OnSize)

        # vertical scrollbar events
        self._VerticalScrollbar.Bind(wx.EVT_PAINT, self.__OnPaintVerticalScrollbar)
        self._VerticalScrollbar.Bind(wx.EVT_LEFT_DOWN, self.__OnLeftDownVerticalScrollbar)
        self._VerticalScrollbar.Bind(wx.EVT_LEFT_UP, self.__OnLeftUpVerticalScrollbar)
        self._VerticalScrollbar.Bind(wx.EVT_MOTION, self.__OnMotionVerticalScrollbar)
        self._VerticalScrollbar.Bind(wx.EVT_LEAVE_WINDOW, self.__OnLeaveVerticalScrollbar)

        # horizontal scrollbar events
        self._HorizontalScrollbar.Bind(wx.EVT_PAINT, self.__OnPaintHorizontalScrollbar)
        self._HorizontalScrollbar.Bind(wx.EVT_LEFT_DOWN, self.__OnLeftDownHorizontalScrollbar)
        self._HorizontalScrollbar.Bind(wx.EVT_LEFT_UP, self.__OnLeftUpHorizontalScrollbar)
        self._HorizontalScrollbar.Bind(wx.EVT_MOTION, self.__OnMotionHorizontalScrollbar)
        self._HorizontalScrollbar.Bind(wx.EVT_LEAVE_WINDOW, self.__OnLeaveHorizontalScrollbar)

        # scroll event on scrolled panel
        self._scrolledPanel.Bind(wx.EVT_SCROLLWIN, self.__OnScroll)


    def __GetDefaultConfig(self) -> ControlConfig:
        return ControlConfig(
            # default colors
            bg_colour=(210, 210, 210),
            fg_colour=(150, 150, 150),
            border_colour=(0, 0, 0),
            border_width=0,
            # pressed
            bg_colour_pressed=(180, 180, 180),
            fg_colour_pressed=(70, 70, 70),
            border_colour_pressed=(0, 0, 0),
            border_width_pressed=0,
            # hover
            bg_colour_hover=(200, 200, 200),
            fg_colour_hover=(100, 100, 100),
            border_colour_hover=(0, 0, 0),
            border_width_hover=0,
            scrollbar_type="rounded"
        )

    
    def __OnLeftDownVerticalScrollbar(self, event):
        # if the user clicked on the scrollbar, we will save some data
        # and then give the window mouse capture. 
        x, y = event.GetPosition()
        if (self._VerticalScrollbarRectangle.Contains(x, y)):
            self._Pressed = True
            self._VerticalDifference = (self._VerticalBarTopY) - y # offset
            self._VerticalScrollbar.CaptureMouse()
        event.Skip()


    def __OnLeftDownHorizontalScrollbar(self, event):
        # if the user clicked on the scrollbar, we will save some data
        # and then give the window mouse capture. 
        x, y = event.GetPosition()
        if (self._HorizontalScrollbarRectangle.Contains(x, y)):
            self._Pressed = True
            self._HorizontalDifference = (self._HorizontalBarTopY) - x # offset
            self._HorizontalScrollbar.CaptureMouse()
        event.Skip()


    def __OnLeftUpVerticalScrollbar(self, event):
        if self._VerticalScrollbar.HasCapture():
            self._VerticalScrollbar.ReleaseMouse()
            # if the window had capture, it would have to be pressed
            self._Pressed = False
            self._MouseHover = False
            self.Refresh()
        event.Skip()


    def __OnLeftUpHorizontalScrollbar(self, event):
        if self._HorizontalScrollbar.HasCapture():
            self._HorizontalScrollbar.ReleaseMouse()
            # if the window had capture, it would have to be pressed
            self._Pressed = False
            self._MouseHover = False
            self.Refresh()
        event.Skip()


    def __OnLeaveVerticalScrollbar(self, event):
        if not self._VerticalScrollbar.HasCapture():
            self._Pressed = False
            self._MouseHover = False
            self._VerticalScrollbar.Refresh()

            
    def __OnLeaveHorizontalScrollbar(self, event):
        if not self._HorizontalScrollbar.HasCapture():
            self._Pressed = False
            self._MouseHover = False
            self._HorizontalScrollbar.Refresh()
            

    def __OnMotionVerticalScrollbar(self, event):

        x, y = event.GetPosition() 

        # we check if we have mouse capture. if we dont, just check if
        # the mouse is hovering the bar.
        
        if (self._VerticalScrollbar.HasCapture()):

            unitsX, unitsY = self._scrolledPanel.GetScrollPixelsPerUnit()

            # --------------------- plan --------------------- #
            
            # viewStart -> scroll Units
            # viewStart * scroll Units -> view start in pixels

            # viewStartPX / scroll Units -> viewStart

            # transform bar height into percentage of virtual size to
            # calculate max scroll range (to bottom of scrolled
            # panel).  virtual size -> 100% bar height -> 20%

            # transform range
            # 10 y in verticalscrollbar -> 40 view start in pixels

            # bottom of range -> 100% of virtual size range (not of
            # scrolled panel, but of scrollable range)

            #y (vertical difference) -> x of virtual size
            # then scroll to percentage of virtual size

            scrolledPanelFullHeightPX = self._scrolledPanel.GetVirtualSize()[1]
            scrollbarAreaHeightPX = self._VerticalScrollbar.GetClientSize()[1]

            # scrollbarAreaHeightPX -> scrolledPanelFullHeightPX
            # verticalBarHeight -> px

            verticalBarScrolledTransform = (self._VerticalBarHeight * scrolledPanelFullHeightPX) // scrollbarAreaHeightPX
            # the very bottom cannot be scrolled down to
            scrollableRangePX = scrolledPanelFullHeightPX - verticalBarScrolledTransform
            scrollbarClickRange = scrollbarAreaHeightPX - int(self._VerticalBarHeight)
            # scrollableRangePX -> 100
            # x -> y percentage
            # calculate click position percentage on scrollbar area range
            clickedIn = y + self._VerticalDifference
            percentage = clickedIn * 1 / scrollbarClickRange
            value = (percentage * scrollableRangePX) / unitsY
            # scroll
            self._scrolledPanel.Scroll(-1, int(value))
            self._VerticalScrollbar.Refresh()
        else:
            if self._VerticalScrollbarRectangle.Contains(x, y):
                self._MouseHover = True
                self._VerticalScrollbar.Refresh()
                #self.Refresh()
            else:
                self._MouseHover = False
                self._VerticalScrollbar.Refresh()
                #self.Refresh()
        event.Skip()


    def __OnMotionHorizontalScrollbar(self, event):

        x, y = event.GetPosition() 

        # we check if we have mouse capture. if we dont, just check if
        # the mouse is hovering the bar.
        
        if (self._HorizontalScrollbar.HasCapture()):

            unitsX, unitsY = self._scrolledPanel.GetScrollPixelsPerUnit()

            # --------------------- plan --------------------- #
            
            # viewStart -> scroll Units
            # viewStart * scroll Units -> view start in pixels

            # viewStartPX / scroll Units -> viewStart

            # transform bar height into percentage of virtual size to
            # calculate max scroll range (to bottom of scrolled
            # panel).  virtual size -> 100% bar height -> 20%

            # transform range
            # 10 y in verticalscrollbar -> 40 view start in pixels

            # bottom of range -> 100% of virtual size range (not of
            # scrolled panel, but of scrollable range)

            #y (vertical difference) -> x of virtual size
            # then scroll to percentage of virtual size

            scrolledPanelFullHeightPX = self._scrolledPanel.GetVirtualSize()[0]
            scrollbarAreaHeightPX = self._HorizontalScrollbar.GetClientSize()[0]

            # scrollbarAreaHeightPX -> scrolledPanelFullHeightPX
            # verticalBarHeight -> px

            horizontalBarScrolledTransform = (self._HorizontalBarHeight * scrolledPanelFullHeightPX) // scrollbarAreaHeightPX
            # the very bottom cannot be scrolled down to
            scrollableRangePX = scrolledPanelFullHeightPX - horizontalBarScrolledTransform
            scrollbarClickRange = scrollbarAreaHeightPX - int(self._HorizontalBarHeight)
            # scrollableRangePX -> 100
            # x -> y percentage
            # calculate click position percentage on scrollbar area range
            clickedIn = x + self._HorizontalDifference
            percentage = clickedIn * 1 / scrollbarClickRange
            value = (percentage * scrollableRangePX) / unitsX
            # scroll
            self._scrolledPanel.Scroll(int(value), -1)
            self._HorizontalScrollbar.Refresh()
        else:
            if self._HorizontalScrollbarRectangle.Contains(x, y):
                self._MouseHover = True
                self._HorizontalScrollbar.Refresh()
                #self.Refresh()
            else:
                self._MouseHover = False
                self._HorizontalScrollbar.Refresh()
                #self.Refresh()
        event.Skip()
        

    def __OnScroll(self, event):
        # refresh scrollbar based on the orientation
        if (event.GetOrientation() == wx.VERTICAL):
            wx.CallAfter(self._VerticalScrollbar.Refresh)
        else:
            wx.CallAfter(self._HorizontalScrollbar.Refresh)
        event.Skip()


    def __OnSize(self, event):
        """ Refreshes the scrollbars when the window is resized. """
        self._scrolledPanel.Refresh()
        self._VerticalScrollbar.Refresh()
        self._HorizontalScrollbar.Refresh()
        event.Skip()

        
    def __OnPaintVerticalScrollbar(self, event):

        # ------------- calculate bar height ------------- #

        clientSize = self._scrolledPanel.GetClientSize()
        virtualSize = self._scrolledPanel.GetVirtualSize()

        # the virtual size is the size of the complete panel. the
        # client size is the size of the panel that we see.
        realY = virtualSize[1]
        visibleY = clientSize[1]

        # if no need to scroll:
        if (visibleY / realY >= 1.0):
            self._VerticalScrollbar.SetSize((0, 0))

        # calculate the proportion
        barHeight = visibleY / realY
        # now we scale it
        barHeight *= self._VerticalScrollbar.GetClientSize()[1]

        self._VerticalBarHeight = barHeight

        # CalcScrolledPosition translates logical coordinates to
        # device ones. logical coordinates are independent of the
        # screen. device coordinates are the ones used by the screen
        # (pixels)

        # we need to translate the scrolled logical coordinates to
        # device ones, and then scale the device ones to match our
        # view of the scrollbar.

        fromTheTop = self._scrolledPanel.CalcScrolledPosition(0, 0)

        topOfBarY = -fromTheTop[1] * (visibleY/realY)

        # we will save this data
        self._VerticalBarTopY = topOfBarY
        

        # --------------- create contexts --------------- #

        # device context
        dc = wx.AutoBufferedPaintDC(self._VerticalScrollbar)
        dc.Clear()

        # graphics context
        gc:wx.GraphicsContext = wx.GraphicsContext.Create(dc)

        # ---------- draw background rectangle ---------- #

        # background rectangle
        backgroundRect = self._VerticalScrollbar.GetClientRect()

        # set background brush and pen
        gc.SetPen(wx.TRANSPARENT_PEN)

        if self._Pressed:
            brush = getBrush("pressed", self.config, gc)
        elif self._MouseHover:
            brush = getBrush("hover", self.config, gc)
        else:
            brush = getBrush("default", self.config, gc)
        
        gc.SetBrush(brush)
            
        gc.DrawRectangle(backgroundRect.GetX(),
                         backgroundRect.GetY(),
                         backgroundRect.GetWidth(),
                         backgroundRect.GetHeight())

        # ------------ draw scroll rectangle ------------ #

        if self._Pressed:
            pen = getPen("pressed", self.config)
            gradient = self.config.fg_linear_gradient_pressed
            brush = wx.Brush(wx.Colour(self.config.fg_colour_pressed))
        elif self._MouseHover:
            pen = getPen("hover", self.config)
            gradient = self.config.fg_linear_gradient_hover
            brush = wx.Brush(wx.Colour(self.config.fg_colour_hover))
        else:
            pen = getPen("default", self.config)
            gradient = self.config.fg_linear_gradient
            brush = wx.Brush(wx.Colour(self.config.fg_colour))

        if gradient:
            c1, c2 = wx.Colour(*gradient[4]), wx.Colour(*gradient[5])
            x1, y1, x2, y2, _, _ = gradient
            brush = gc.CreateLinearGradientBrush(x1, y1, x2, y2, c1, c2)
            
        gc.SetPen(pen)
        gc.SetBrush(brush)

        # save the rectangle data to check if the user clicks on it
        self._VerticalScrollbarRectangle = wx.Rect(0,
                                                   int(topOfBarY),
                                                   self._ScrollbarWidth,
                                                   int(barHeight))

        if (self.config.scrollbar_type == "rectangle"):
            gc.DrawRectangle(self._VerticalScrollbarRectangle.GetX()+self._ScrollbarPadding,
                             self._VerticalScrollbarRectangle.GetY(),
                             self._VerticalScrollbarRectangle.GetWidth()-(2*self._ScrollbarPadding),
                             self._VerticalScrollbarRectangle.GetHeight())
        else:
            cornerRadius = (self._ScrollbarWidth-2*self._ScrollbarPadding)//2
            gc.DrawRoundedRectangle(self._VerticalScrollbarRectangle.GetX()+self._ScrollbarPadding,
                                    self._VerticalScrollbarRectangle.GetY(),
                                    self._VerticalScrollbarRectangle.GetWidth()-(2*self._ScrollbarPadding),
                                    self._VerticalScrollbarRectangle.GetHeight(),
                                    cornerRadius)


    def __OnPaintHorizontalScrollbar(self, event):

        # ------------- calculate bar height ------------- #

        clientSize = self._scrolledPanel.GetClientSize()
        virtualSize = self._scrolledPanel.GetVirtualSize()

        # the virtual size is the size of the complete panel. the
        # client size is the size of the panel that we see.
        realY = virtualSize[0]
        visibleY = clientSize[0]

        # if no need to scroll:
        if (visibleY / realY >= 1.0):
            self._HorizontalScrollbar.SetSize((0, 0))

        # calculate the proportion
        barHeight = visibleY / realY
        # now we scale it
        barHeight *= self._HorizontalScrollbar.GetClientSize()[0]

        self._HorizontalBarHeight = barHeight

        # CalcScrolledPosition translates logical coordinates to
        # device ones. logical coordinates are independent of the
        # screen. device coordinates are the ones used by the screen
        # (pixels)

        # we need to translate the scrolled logical coordinates to
        # device ones, and then scale the device ones to match our
        # view of the scrollbar.

        fromTheTop = self._scrolledPanel.CalcScrolledPosition(0, 0)

        topOfBarY = -fromTheTop[0] * (visibleY/realY)

        # we will save this data
        self._HorizontalBarTopY = topOfBarY
        

        # --------------- create contexts --------------- #

        # device context
        dc = wx.AutoBufferedPaintDC(self._HorizontalScrollbar)
        dc.Clear()

        # graphics context
        gc:wx.GraphicsContext = wx.GraphicsContext.Create(dc)

        # ---------- draw background rectangle ---------- #

        # background rectangle
        backgroundRect = self._HorizontalScrollbar.GetClientRect()

        # set background brush and pen
        gc.SetPen(wx.TRANSPARENT_PEN)

        if self._Pressed:
            brush = getBrush("pressed", self.config, gc)
        elif self._MouseHover:
            brush = getBrush("hover", self.config, gc)
        else:
            brush = getBrush("default", self.config, gc)
        
        gc.SetBrush(brush)
            
        gc.DrawRectangle(backgroundRect.GetX(),
                         backgroundRect.GetY(),
                         backgroundRect.GetWidth(),
                         backgroundRect.GetHeight())

        # ------------ draw scroll rectangle ------------ #

        if self._Pressed:
            pen = getPen("pressed", self.config)
            gradient = self.config.fg_linear_gradient_pressed
            brush = wx.Brush(wx.Colour(self.config.fg_colour_pressed))
        elif self._MouseHover:
            pen = getPen("hover", self.config)
            gradient = self.config.fg_linear_gradient_hover
            brush = wx.Brush(wx.Colour(self.config.fg_colour_hover))
        else:
            pen = getPen("default", self.config)
            gradient = self.config.fg_linear_gradient
            brush = wx.Brush(wx.Colour(self.config.fg_colour))

        if gradient:
            c1, c2 = wx.Colour(*gradient[4]), wx.Colour(*gradient[5])
            x1, y1, x2, y2, _, _ = gradient
            brush = gc.CreateLinearGradientBrush(x1, y1, x2, y2, c1, c2)
            
        gc.SetPen(pen)
        gc.SetBrush(brush)

        # save the rectangle data to check if the user clicks on it
        self._HorizontalScrollbarRectangle = wx.Rect(int(topOfBarY), 0, int(barHeight), self._ScrollbarWidth)

        if (self.config.scrollbar_type == "rectangle"):
            gc.DrawRectangle(self._HorizontalScrollbarRectangle.GetX()+self._ScrollbarPadding,
                             self._HorizontalScrollbarRectangle.GetY(),
                             self._HorizontalScrollbarRectangle.GetWidth()-(2*self._ScrollbarPadding),
                             self._HorizontalScrollbarRectangle.GetHeight())
        else:
            cornerRadius = (self._ScrollbarWidth-2*self._ScrollbarPadding)//2
            gc.DrawRoundedRectangle(self._HorizontalScrollbarRectangle.GetX(),
                                    self._HorizontalScrollbarRectangle.GetY()+self._ScrollbarPadding,
                                    self._HorizontalScrollbarRectangle.GetWidth(),
                                    self._HorizontalScrollbarRectangle.GetHeight()-(2*self._ScrollbarPadding),
                                    cornerRadius)


    def GetPanel(self):
        """ Returns the scrolled panel to the user. """
        return self._scrolledPanel

