# CustomScrolledWindow.py
# wxCustomControls
# A scrolled window with customizable scrollbars.
# 6/nov/2024


import wx
from copy import copy
from .utils.dip import dip
from .base._CustomObject import CustomObject
from wx.lib.scrolledpanel import ScrolledPanel


class CustomScrolledWindow(wx.Window, CustomObject):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,name=wx.PanelNameStr, config=None, **kwargs):

        # ---------------- init custom object ---------------- #
        
        super().__init__(parent, id, pos, size, style, name)
        CustomObject.__init__(self, config, **kwargs)

        # for bottom right square
        self.SetBackgroundColour(self._config.background_colour_default)

        # ------------ create scrolled panel ------------ #

        self._scrolledPanel = ScrolledPanel(self)
        self._scrolledPanel.SetupScrolling(self._config.scrollX, 
                                           self._config.scrollY, 
                                           self._config.scrollUnitsX, 
                                           self._config.scrollUnitsY)
        #self._scrolledPanel.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_NEVER)
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

        self._Enabled = True ###
        self._Pressed = False
        self._Hover = False


        # ---------------- default values ---------------- #
        
        self._ScrollbarWidth = self._config.scrollbar_width if self._config.scrollbar_width else dip(15)
        self._ScrollbarPadding = self._config.scrollbar_padding if self._config.scrollbar_padding else dip(3)

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
        self._VerticalScrollbar.Bind(wx.EVT_MOTION, self.__OnMotionVerticalScrollbar)


        self._VerticalScrollbar.Bind(wx.EVT_LEFT_DOWN, self.__OnLeftDown)
        self._VerticalScrollbar.Bind(wx.EVT_LEFT_UP, self.__OnLeftUp)
        self._VerticalScrollbar.Bind(wx.EVT_LEAVE_WINDOW, self.__OnLeave)

        # horizontal scrollbar events
        self._HorizontalScrollbar.Bind(wx.EVT_PAINT, self.__OnPaintHorizontalScrollbar)
        self._HorizontalScrollbar.Bind(wx.EVT_MOTION, self.__OnMotionHorizontalScrollbar)


        self._HorizontalScrollbar.Bind(wx.EVT_LEFT_DOWN, self.__OnLeftDown)
        self._HorizontalScrollbar.Bind(wx.EVT_LEFT_UP, self.__OnLeftUp)
        self._HorizontalScrollbar.Bind(wx.EVT_LEAVE_WINDOW, self.__OnLeave)

        self._scrolledPanel.Bind(wx.EVT_MOUSEWHEEL, self.__OnScroll)

        self.Layout()


    def GetPanel(self):
        """ Returns the scrolled panel to the user. """
        return self._scrolledPanel


    def GetStateAsString(self):
        """Returns the state as a string."""
        if not self._Enabled:
            return "disabled"
        else:
            if self._Pressed:
                return "pressed"
            elif self._Hover:
                return "hover"
            else:
                return "default"
            

    def __OnLeftDown(self, event:wx.MouseEvent):
        """Checks if user clicked on a scrollbar, performs click offset calculation and captures mouse for that window."""
        x, y = event.GetPosition()
        scrollbarWindow = event.GetEventObject()
        clickedOnScrollbar = self._VerticalScrollbarRectangle.Contains(x, y) or self._HorizontalScrollbarRectangle.Contains(x, y)

        if not clickedOnScrollbar:
            event.Skip()
            return
        
        self._Pressed = True
        scrollbarWindow.CaptureMouse()

        # mouse click offset calculation
        if (scrollbarWindow == self._VerticalScrollbar):
            self._VerticalDifference = (self._VerticalBarTopY) - y
        elif (scrollbarWindow == self._HorizontalScrollbar):
            self._HorizontalDifference = (self._HorizontalBarTopY) - x
        event.Skip()


    def __OnLeftUp(self, event:wx.MouseEvent):
        """Releases the mouse capture when click is up."""
        scrollbarWindow = event.GetEventObject()
        if scrollbarWindow.HasCapture():
            scrollbarWindow.ReleaseMouse()
            self._Pressed = False
            self._Hover = False
            self.Refresh()
        event.Skip()

    
    def __OnLeave(self, event:wx.MouseEvent):
        """Handles the hover attribute when the mouse leaves the scrollbar window."""
        scrollbarWindow = event.GetEventObject()
        if not scrollbarWindow.HasCapture():
            self._Pressed = False
            self._Hover = False
            scrollbarWindow.Refresh()
        event.Skip()
            

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
                self._Hover = True
                self._VerticalScrollbar.Refresh()
                #self.Refresh()
            else:
                self._Hover = False
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
                self._Hover = True
                self._HorizontalScrollbar.Refresh()
                #self.Refresh()
            else:
                self._Hover = False
                self._HorizontalScrollbar.Refresh()
                #self.Refresh()
        event.Skip()
        

    def __OnScroll(self, event:wx.MouseEvent):

        currentView = self._scrolledPanel.GetViewStart()
        
        x:int = 0
        y:int = 0

        if event.GetWheelAxis() == wx.MOUSE_WHEEL_VERTICAL:
            x = currentView[0]
            y = currentView[1] - (event.GetWheelRotation() / 8)
            #wx.CallAfter(self._VerticalScrollbar.Refresh)
            self._VerticalScrollbar.Refresh()
        elif event.GetWheelAxis() == wx.MOUSE_WHEEL_HORIZONTAL:
            x = currentView[0] - (event.GetWheelRotation() / 8)
            y = currentView[1]
            #wx.CallAfter(self._HorizontalScrollbar.Refresh)
            self._HorizontalScrollbar.Refresh()

        self._scrolledPanel.Scroll(int(x), int(y))


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


        # create contexts

        gcdc, gc = self._getDrawingContexts(self._VerticalScrollbar)

        # drawing properties

        drawing_properties = self._getStateDrawingProperties(self.GetStateAsString(), gc)

        # cursor

        self._VerticalScrollbar.SetCursor(drawing_properties["cursor"])

        # drawing area and background

        controlRect:wx.Rect = self._VerticalScrollbar.GetClientRect()

        gcdc.SetPen(wx.TRANSPARENT_PEN)
        gc.SetBrush(drawing_properties["brush_background"])
        gcdc.DrawRectangle(controlRect)

        # draw scroll rectangle

        gcdc.SetPen(drawing_properties["pen"])
        gc.SetBrush(drawing_properties["brush_foreground"])

        # save the rectangle data to check if the user clicks on it
        self._VerticalScrollbarRectangle = wx.Rect(0, int(topOfBarY),
                                                   self._ScrollbarWidth, int(barHeight))

        if (self._config.scrollbar_type == "rectangular"):
            gc.DrawRectangle(self._VerticalScrollbarRectangle.GetX() + self._ScrollbarPadding,
                             self._VerticalScrollbarRectangle.GetY(),
                             self._VerticalScrollbarRectangle.GetWidth() - (2 * self._ScrollbarPadding),
                             self._VerticalScrollbarRectangle.GetHeight())
        elif (self._config.scrollbar_type == "rounded"):
            cornerRadius = (self._ScrollbarWidth - 2 * self._ScrollbarPadding) // 2
            gc.DrawRoundedRectangle(self._VerticalScrollbarRectangle.GetX() + self._ScrollbarPadding,
                                    self._VerticalScrollbarRectangle.GetY(),
                                    self._VerticalScrollbarRectangle.GetWidth() - (2 * self._ScrollbarPadding),
                                    self._VerticalScrollbarRectangle.GetHeight(),
                                    cornerRadius)
        else:
            raise ValueError("Scrollbar Type: Only \"rectangular\" and \"rounded\" values are allowed.")


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


        # create contexts

        gcdc, gc = self._getDrawingContexts(self._HorizontalScrollbar)

        # drawing properties

        drawing_properties = self._getStateDrawingProperties(self.GetStateAsString(), gc)

        # cursor

        self._VerticalScrollbar.SetCursor(drawing_properties["cursor"])

        # drawing area and background

        controlRect:wx.Rect = self._HorizontalScrollbar.GetClientRect()

        gcdc.SetPen(wx.TRANSPARENT_PEN)
        gc.SetBrush(drawing_properties["brush_background"])
        gcdc.DrawRectangle(controlRect)

        # draw scroll rectangle

        gcdc.SetPen(drawing_properties["pen"])
        gc.SetBrush(drawing_properties["brush_foreground"])

        # save the rectangle data to check if the user clicks on it
        self._HorizontalScrollbarRectangle = wx.Rect(int(topOfBarY), 0, 
                                                     int(barHeight), self._ScrollbarWidth)

        if (self._config.scrollbar_type == "rectangular"):
            gc.DrawRectangle(self._HorizontalScrollbarRectangle.GetX(),
                             self._HorizontalScrollbarRectangle.GetY() + self._ScrollbarPadding,
                             self._HorizontalScrollbarRectangle.GetWidth(),
                             self._HorizontalScrollbarRectangle.GetHeight() - (2 * self._ScrollbarPadding))
        elif (self._config.scrollbar_type == "rounded"):
            cornerRadius = (self._ScrollbarWidth - 2 * self._ScrollbarPadding) // 2
            gc.DrawRoundedRectangle(self._HorizontalScrollbarRectangle.GetX(),
                                    self._HorizontalScrollbarRectangle.GetY() + self._ScrollbarPadding,
                                    self._HorizontalScrollbarRectangle.GetWidth(),
                                    self._HorizontalScrollbarRectangle.GetHeight() - (2 * self._ScrollbarPadding),
                                    cornerRadius)
        else:
            raise ValueError("Scrollbar Type: Only \"rectangular\" and \"rounded\" values are allowed.")


