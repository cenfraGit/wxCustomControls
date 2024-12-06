# CustomComboBox.py
# wxCustomControls
# A customizable combobox.
# 7/nov/2024


import wx
from .base._CustomControl import CustomControl
from .CustomDropDown import CustomDropDown
from .CustomScrolledWindow import CustomScrolledWindow
from .CustomButton import CustomButton
from .utils.dip import dip


# class CustomComboBoxDropDown(CustomDropDown):
#     def __init__(self, parent, choices, flags, config, size):

#         super().__init__(parent, flags, config, size)

#         self._Choices = choices



#         pass




#         for index, value in enumerate(self._Choices):
#             btn = CustomButton(self._Panel, label=value, config=self._config)
#             self._PanelSizer.Add(btn, pos=(index, 0), flag=wx.EXPAND)
#             #btn.Bind(wx.EVT_BUTTON, lambda event: print(event.GetId()))
#             btn.Bind(wx.EVT_BUTTON, self.__OnButton)

from .CustomConfig import CustomConfig
from .functions.getDefaultConfig import getDefaultConfig

class CustomComboBoxValuesPanel(wx.PopupTransientWindow):

    def __init__(self, parent, config, flags=wx.NO_BORDER, choices=[], size=wx.DefaultSize):

        super().__init__(parent=parent, flags=flags)

        
        # ------------------ attributes ------------------ #

        self._Choices = choices
        self._config:CustomConfig = config

        self.SetBackgroundColour(wx.GREEN)

        # -------------------- setup -------------------- #

        self.p = wx.Panel(self)
        psizer = wx.BoxSizer(wx.VERTICAL)
        self.p.SetSizer(psizer)

        self.scrolled = CustomScrolledWindow(parent=self.p)
        self._Panel = self.scrolled.GetPanel()
    
        #self._Panel.SetBackgroundColour(wx.CYAN)
        
        self._PanelSizer = wx.GridBagSizer()
        #for i in range(10):
        #    self._PanelSizer.Add(CustomButton(self._Panel, label="Placeholder"), pos=(i, 0), flag=wx.EXPAND)
        
        for index, value in enumerate(self._Choices):
            btn = CustomButton(self._Panel, label=value, config=self._config)
            self._PanelSizer.Add(btn, pos=(index, 0), flag=wx.EXPAND)
            #btn.Bind(wx.EVT_BUTTON, lambda event: print(event.GetId()))
            btn.Bind(wx.EVT_BUTTON, self.__OnButton)
            
        self._PanelSizer.AddGrowableCol(0, 1)
        self._Panel.SetSizer(self._PanelSizer)

        #self._Panel.SetClientSize((300, 300))
        #self.scrolled.SetClientSize((300, 300))
        #self._PanelSizer.Fit(self)

        #self._PanelSizer.Fit(self.scrolled)
        #self._PanelSizer.Layout()
        self.Layout()

        psizer.Add(self.scrolled, flag=wx.EXPAND, proportion=1)
        #psizer.Fit(self._Panel)
        #psizer.Fit(p)
        #p.Fit()
        #psizer.Fit(self)
        #psizer.FitInside(self)
        #self.scrolled.SetClientSize(self.GetClientSize())
        self.Layout()

        # dictionary where choice rectangle areas are saved (for mouse
        # events)
        #self._ChoiceRectangles = {}

        self._PaddingHorizontal = dip(14)
        self._PaddingVertical = dip(7)

        self.SetInitialSize(size)

        #self.scrolled.SetMinSize(wx.Size(300, 300))
        #clientSize = self.GetClientSize()
        self.scrolled.SetMinSize(self.GetClientSize())
        #self.scrolled.SetMinSize(wx.Size(clientSize))
        self.p.Fit()
        self.p.Layout()

        # -------------------- events -------------------- #

        self.Bind(wx.EVT_MOTION, self.__OnMotion)


    def __OnButton(self, event:wx.CommandEvent):

        # i think we need to find the window by id because the event
        # object is not configured correctly in custom button.
        buttonObject:CustomButton = wx.Window.FindWindowById(event.GetId())
        buttonLabel = buttonObject.GetLabel()

        # the parent is the actual combobox, so replace its value
        #self.GetParent().SetValue(buttonLabel)

        # close this window
        self.Dismiss()


    def DoGetBestClientSize(self):

        dc = wx.ClientDC(self)
        gc:wx.GraphicsContext = wx.GraphicsContext.Create(dc)

        gc.SetFont(wx.Font(self._config.text_font_size_default,
                           wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL, faceName=self._config.text_font_facename_default), wx.BLACK)

        
        longestChoice = max([len(string) for string in self._Choices])

        newString = "".join(["A" for _ in range(longestChoice)])

        textWidth, textHeight, _, _ = gc.GetFullTextExtent(newString)

        fullHeight = len(self._Choices) * textHeight * 2

        maxHeight = 150

        width = textWidth * 5
        height =  fullHeight if (fullHeight < dip(maxHeight)) else dip(maxHeight)
        
        return wx.Size(int(width), int(height))

        
    def __OnLeftDown(self, event):
        pass


    def __OnMotion(self, event:wx.MouseEvent):

        #self.scrolled.SetClientSize(self.GetClientSize())
        self.scrolled.SetMinSize(wx.Size(300, 100))


        x, y = event.GetPosition()

        print(x, y)






class CustomComboBox(CustomControl):
    def __init__(self, parent, id=wx.ID_ANY, value=wx.EmptyString, choices=None,
                 pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.NO_BORDER,
                 validator=wx.DefaultValidator, name=wx.ComboBoxNameStr,
                 config=None, **kwargs):
        
        # choices can be a list or a dict.
        # a list is used when no images are needed to be displayed
        # a dict is used as a {value: image} key-value pair

        # control attributes

        kwargs["value"] = value
        kwargs["choices"] = choices

        # init control

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

        # ----------------- combobox rectangle ----------------- #

        comboboxRectangle = controlRect.Deflate(drawing_properties["pen"].GetWidth(),
                                              drawing_properties["pen"].GetWidth())

        gcdc.SetPen(drawing_properties["pen"])
        gc.SetBrush(drawing_properties["brush_background"])
        gcdc.DrawRoundedRectangle(comboboxRectangle, drawing_properties["corner_radius"])

        # ---------------------- get dimensions ------------------------ #
        
        textWidth, textHeight = self._getTextDimensions(gcdc, self._Value, drawing_properties)
        imageWidth, imageHeight, bitmap = self._getBitmapAndDimensions(drawing_properties)
        imageTextRectWidth, imageTextRectHeight = self._getObjectSideDimensions(imageWidth, imageHeight,
                                                                                textWidth, textHeight, 
                                                                                self._config.image_text_separation, 
                                                                                self._config.image_text_side)
        
        arrowX, arrowY, imageTextRectX, imageTextRectY = self._performObjectSideCalculation(controlRect, 
                                                                                            self._config.arrow_width, self._config.arrow_height, 
                                                                                            imageTextRectWidth, imageTextRectHeight, 
                                                                                            self._config.arrow_text_separation, 
                                                                                            self._config.arrow_text_side)
        
        # ---------------------- create rectangles ------------------------ #

        # temp hackathon
        imageTextRectX = dip(5) if (self._config.arrow_text_side == "left") else comboboxRectangle.GetWidth() - dip(5) - imageTextRectWidth

        imageTextRect = wx.Rect(imageTextRectX, imageTextRectY, imageTextRectWidth, imageTextRectHeight)
        arrowRectangle = wx.Rect(arrowX, arrowY, self._config.arrow_width, self._config.arrow_height)

        # ---------------------- draw arrow ------------------------ #

        gc.SetPen(wx.Pen(wx.Colour(*self._config.arrow_colour)))
        path:wx.GraphicsPath = gc.CreatePath()
        path.MoveToPoint(arrowRectangle.GetX(), arrowRectangle.GetY())
        path.AddLineToPoint(arrowRectangle.GetX() + arrowRectangle.GetWidth()//2, arrowRectangle.GetY() + arrowRectangle.GetHeight())
        path.AddLineToPoint(arrowRectangle.GetX() + arrowRectangle.GetWidth(), arrowRectangle.GetY())
        gc.StrokePath(path)

        # ----------------------- draw ----------------------- #

        self._drawImageTextRectangle(gcdc, imageTextRect,
                                     self._Value,
                                     textWidth, textHeight,
                                     bitmap, imageWidth, imageHeight)

    
    def DoGetBestClientSize(self) -> wx.Size:
        
        dc = wx.ClientDC(self)
        gcdc:wx.GCDC = wx.GCDC(dc)

        # image = self._getIfImage()
        textWidth, textHeight = self._getDefaultTextExtent(gcdc, self._Value)
        imageWidth, imageHeight = self._getMaxDimensions("image")
        text_separation = self._config.image_text_separation if self._config.image_text_separation else dip(6)
        padding_horizontal = dip(10)
        padding_vertical = dip(5)

        width, height = self._getObjectSideDimensions(imageWidth, imageHeight,
                                                      textWidth, textHeight,text_separation,
                                                      self._config.image_text_side)
        width += 2 * padding_horizontal
        height += 2 * padding_vertical

        # add arrow width
        width += self._config.arrow_width + self._config.arrow_text_separation

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
                wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_COMBOBOX.typeId, self.GetId()))

            try:
                self._ChoicesPanel = CustomComboBoxValuesPanel(self, choices=self._Choices, config=getDefaultConfig("CustomButton"))
                ctrl = event.GetEventObject()
                pos = ctrl.ClientToScreen((0, 0))
                sz = ctrl.GetSize()
                self._ChoicesPanel.Position(pos, (0, sz[1]))
                self._ChoicesPanel.Popup()
            except Exception as e:
                print(e)


        event.Skip()

