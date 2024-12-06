# CustomDropDown.py
# wxCustomControls
# A drop down pop up transient window that holds customizable controls.
# 11/nov/2024


import wx
from .base._CustomObject import CustomObject
from .base._CustomControl import CustomControl
from .CustomScrolledWindow import CustomScrolledWindow
from .utils.dip import dip


class CustomDropDown(wx.PopupTransientWindow, CustomObject):

    def __init__(self, parent, flags=0, config=None, size=wx.DefaultSize, **kwargs):

        # ---------------------- init custom object ------------------------ #

        super().__init__(parent, flags|wx.NO_BORDER)
        CustomObject.__init__(self, config, **kwargs)

        # ---------------------- setup ------------------------ #

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        # -------------------- setup -------------------- #

        self.p = wx.Panel(self)
        psizer = wx.BoxSizer(wx.VERTICAL)
        self.p.SetSizer(psizer)

        self.scrolled = CustomScrolledWindow(parent=self.p, scrollX=True, scrollY=True)
        self._Panel = self.scrolled.GetPanel()
        self._PanelSizer = wx.GridBagSizer()




        for i in range(20):
           self._PanelSizer.Add(wx.Button(self._Panel, label="Placeholder"), pos=(i, 0), flag=wx.EXPAND)
        
        # for index, value in enumerate(self._Choices):
        #     btn = CustomButton(self._Panel, label=value, config=self._config)
        #     self._PanelSizer.Add(btn, pos=(index, 0), flag=wx.EXPAND)
        #     #btn.Bind(wx.EVT_BUTTON, lambda event: print(event.GetId()))
        #     btn.Bind(wx.EVT_BUTTON, self.__OnButton)
            
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

    def GetPanel(self):
        return self._Panel
    


    # def __OnButton(self, event:wx.CommandEvent):

    #     # i think we need to find the window by id because the event
    #     # object is not configured correctly in custom button.
    #     buttonObject:CustomButton = wx.Window.FindWindowById(event.GetId())
    #     buttonLabel = buttonObject.GetLabel()

    #     # the parent is the actual combobox, so replace its value
    #     self.GetParent().SetValue(buttonLabel)

    #     # close this window
    #     self.Dismiss()


    # def DoGetBestClientSize(self):

    #     dc = wx.ClientDC(self)
    #     gc:wx.GraphicsContext = wx.GraphicsContext.Create(dc)

    #     gc.SetFont(wx.Font(self._config.font_size,
    #                        wx.FONTFAMILY_DEFAULT,
    #                        wx.FONTSTYLE_NORMAL,
    #                        wx.FONTWEIGHT_NORMAL, faceName=self._config.font_face_name), wx.BLACK)

        
    #     longestChoice = max([len(string) for string in self._Choices])

    #     newString = "".join(["A" for _ in range(longestChoice)])

    #     textWidth, textHeight, _, _ = gc.GetFullTextExtent(newString)

    #     fullHeight = len(self._Choices) * textHeight * 2

    #     maxHeight = 150

    #     width = textWidth * 5
    #     height =  fullHeight if (fullHeight < dip(maxHeight)) else dip(maxHeight)
        
    #     return wx.Size(int(width), int(height))

    def DoGetBestClientSize(self):
        return wx.Size(300, 300)

        
    def __OnLeftDown(self, event):
        pass


    def __OnMotion(self, event:wx.MouseEvent):

        #self.scrolled.SetClientSize(self.GetClientSize())
        self.scrolled.SetMinSize(wx.Size(300, 100))


        x, y = event.GetPosition()

        print(x, y)