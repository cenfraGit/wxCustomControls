import wx
from dip import dip


class cCheckBox(wx.Control):
    
    """ Defines a custom checkbox control that supports themes. """
    
    def __init__(self, parent, id=wx.ID_ANY, value:str="", choices:list=[], pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.NO_BORDER, validator=wx.DefaultValidator,
                 name="cChoice", theme:str="light"):
        super().__init__(parent, id, pos, size, style, validator, name)

        # control attributes
        self._value = value
        self._choices = choices
        self._Theme = theme # light or dark
        self._Enabled = True

        # state attributes
        self.pressed = False
        self.mouseHover = False

        # initialize control colors
        self.initializeColors()
        
        # set up autobufferedpaintdc
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        # bind control events
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        
        
    def initializeColors(self):

        """ Initializes the button's colors according to theme. """
        

        # get parent background color (for corners)
        self.penBackground = wx.TRANSPARENT_PEN
        self.brushBackground = wx.Brush(self.GetParent().GetBackgroundColour(), wx.BRUSHSTYLE_SOLID)
        

        if (self._Theme == "light"):

            # text
            self.colorTextForegroundDefault = wx.BLACK
            self.colorTextForegroundPressed = wx.WHITE
            self.colorTextForegroundHover = wx.BLACK
            self.colorTextForegroundDisabled = wx.Colour(170, 170, 170)
            # pens
            self.penDefault = wx.Pen(wx.Colour(150, 150, 150), width=1, style=wx.PENSTYLE_SOLID)
            self.penPressed = wx.Pen(wx.Colour(8, 40, 107), width=1, style=wx.PENSTYLE_SOLID)
            self.penHover = wx.Pen(wx.Colour(65, 26, 222), width=1, style=wx.PENSTYLE_SOLID)
            self.penDisabled = wx.Pen(wx.Colour(220, 220, 220), width=1, style=wx.PENSTYLE_SOLID)
            # brushes
            self.brushPressed = wx.Brush(wx.Colour(76, 102, 156), wx.BRUSHSTYLE_SOLID)
            self.brushHover = wx.Brush(wx.Colour(220, 220, 220), wx.BRUSHSTYLE_SOLID)
            self.brushDefault = wx.Brush(wx.WHITE, wx.BRUSHSTYLE_SOLID)
            self.brushDisabled = wx.Brush(wx.Colour(200, 200, 200), wx.BRUSHSTYLE_SOLID)
            
        elif (self._Theme == "blue"):

            # text
            self.colorTextForegroundDefault = wx.Colour(190, 190, 190)
            self.colorTextForegroundPressed = wx.WHITE
            self.colorTextForegroundHover = wx.Colour(200, 200, 200)
            self.colorTextForegroundDisabled = wx.Colour(170, 170, 170)
            # pens
            self.penDefault = wx.Pen(wx.Colour(39, 62, 177), width=1, style=wx.PENSTYLE_SOLID)
            self.penPressed = wx.Pen(wx.Colour(65, 26, 222), width=1, style=wx.PENSTYLE_SOLID)
            self.penHover = wx.Pen(wx.Colour(65, 26, 222), width=1, style=wx.PENSTYLE_SOLID)
            self.penDisabled = wx.Pen(wx.Colour(220, 220, 220), width=1, style=wx.PENSTYLE_SOLID)
            # brushes
            self.brushPressed = wx.Brush(wx.Colour(16, 31, 110), wx.BRUSHSTYLE_SOLID)
            self.brushHover = wx.Brush(wx.Colour(23, 53, 115), wx.BRUSHSTYLE_SOLID)
            self.brushDefault = wx.Brush(wx.Colour(19, 53, 122), wx.BRUSHSTYLE_SOLID)
            self.brushDisabled = wx.Brush(wx.Colour(200, 200, 200), wx.BRUSHSTYLE_SOLID)
            
        else:
            raise ValueError("Invalid theme.")

        
    def SetValue(self, value):
        self.value = value
        self.Refresh()
        

    def OnPaint(self, event):

        """ Handles the paint event. """
        
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        self.Draw(dc)
        

    def Draw(self, dc: wx.AutoBufferedPaintDC):

        """ Draw the actual button. """
        
        rect = self.GetClientRect()

        # make backgrund transparent
        dc.SetPen(self.penBackground)
        dc.SetBrush(self.brushBackground)
        dc.DrawRectangle(rect)
        
        # check if the button is enabled, then check if pressed. if
        # not, check if the mouse cursor is hovering on top of
        # it. if not, draw with default colors.

        if not self._Enabled:
            dc.SetPen(self.penDisabled)
            dc.SetBrush(self.brushDisabled)
            dc.SetTextForeground(self.colorTextForegroundDisabled)
        else:
            dc.SetPen(self.penDefault)
            dc.SetBrush(self.brushDefault)
            dc.SetTextForeground(self.colorTextForegroundDefault)
            """
            if self.pressed:
                dc.SetPen(self.penPressed)
                dc.SetBrush(self.brushPressed)
                dc.SetTextForeground(self.colorTextForegroundPressed)
            elif self.mouseHover:
                dc.SetPen(self.penHover)
                dc.SetBrush(self.brushHover)
                dc.SetTextForeground(self.colorTextForegroundHover)
            else:
                dc.SetPen(self.penDefault)
                dc.SetBrush(self.brushDefault)
                dc.SetTextForeground(self.colorTextForegroundDefault)
            """
            
        # draw border    
        dc.DrawRoundedRectangle(rect, 6)

        # draw text (to the left)
        leftMargin = dip(10)
        textWidth, textHeight = dc.GetTextExtent(self._value)
        textX = leftMargin
        textY = rect.GetY() + (rect.GetHeight() // 2) - (textHeight // 2)
        dc.DrawText(self._value, textX, textY)
        
        # draw drop down arrow
        rightMargin = dip(6)
        width, height = dip(16), dip(4)
        rectPosX = rect.GetWidth() - width - rightMargin
        rectPosY = (rect.GetHeight() // 2) - (height // 2)
        arrowRectangle = wx.Rect(rectPosX, rectPosY, width, height)
        #dc.DrawRectangle(arrowRectangle)
        dc.DrawLine(rectPosX, rectPosY, rectPosX+(width//2), rectPosY+height)
        dc.DrawLine(rectPosX+(width//2), rectPosY+height, *arrowRectangle.GetTopRight())

        
    def OnEraseBackground(self, event):
        """ Bound to prevent flickering. """
        pass
    

    def OnLeftDown(self, event):

        # invert status
        self.pressed = not self.pressed

        if self.pressed:
            # open choices panel
            self.createChoicesPanel()
        else:
            # destroy choices panel
            try:
                self.destroyChoicesPanel()
            except:
                pass
        
        self.Refresh()
        event.Skip()


    def OnLeftUp(self, event):
        if self.pressed:
            pass
            #self.Refresh()
            #wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.GetId()))
        event.Skip()
        

    def OnMouseLeave(self, event):
        self.mouseHover = False
        self.Refresh()
        event.Skip()
        

    def OnMouseEnter(self, event):
        self.mouseHover = True
        self.Refresh()
        event.Skip()
        

    def Enable(self, enable=True):
        """
        Uses _Enable to define if the widget is enabled or not,
        instead of default behavior (problems redrawing after modal
        dialogs).
        """
        self._Enabled = enable
        super().Enable(enable)
        self.Refresh()
        

    def Disable(self):
        self.Enable(False)


    def createChoicesPanel(self):
        
        """ Creates and displays the drop down menu that displays the choices. """

        # return if choices list is empty
        if len(self._choices) == 0:
            return

        rect = self.GetClientRect()
        
        self.choicesPanel = ChoicesPanel(parent=self.GetParent(),
                                         size=(500, 500), pos=(50, 50+rect.GetHeight()),
                                         choices=self._choices, theme=self._Theme, reference=self)
        #self.choicesPanel.SetBackgroundColour(wx.GREEN)
        self.GetParent().Refresh()

    def destroyChoicesPanel(self):
        """ Destroys the existing reference to the choices panel. """
        self.choicesPanel.Destroy()
        self.GetParent().Refresh()

        

        


# for testing control directly
if __name__ == "__main__":
    import ctypes
    from themeColors import backgroundBlue, backgroundLight
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    
    class MyFrame(wx.Frame):
        def __init__(self):
            super().__init__(None, title="Custom Example")
            panel = wx.Panel(self)
            panel.SetBackgroundColour(backgroundLight)


            values = ["test1", "car1", "car2", "computer", "messageboxtext"]
            self.choice = cChoice(panel, choices=values, value="computer", pos=wx.Point(50, 50), size=wx.Size(300, 40), theme="light")

            wx.StaticText(panel, label="placeholder", pos=(55, 100))
            wx.StaticText(panel, label="placeholder", pos=(55, 150))

            self.Show()

            

    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()
