import wx
from .controlConfig import ControlConfig
from .functions.getPenBrush import getPen, getBrush
from .functions.dip import dip
from copy import copy


class CustomStaticBox(wx.Panel):

    def __init__(self, parent, id=wx.ID_ANY, label=wx.EmptyString,
                 pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                 name=wx.PanelNameStr, config=None, **kwargs):
    
        super().__init__(parent=parent, id=id, pos=pos, size=size,
                         style=style, name=name)

        # --------------- check for config --------------- #
        # if the user does not specify a config object, create
        # one and update with kwargs
        self.config:ControlConfig = copy(config) if config else self.__GetDefaultConfig()
        if kwargs:
            self.config.update(**kwargs)
        

        # -------------- ATTRIBUTES --------------

        self._Label = label

        # get text extent for panel top padding
        dc = wx.ScreenDC()
        dc.SetFont(wx.Font(self.config.font_size,
                           wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL,
                           faceName=self.config.font_face_name))
        _, textHeight = dc.GetTextExtent(self._Label)
        
        # -------------- APPEARANCE --------------

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.SetInitialSize(size)


        # ---------------- panel inside  ---------------- #

        self._Panel = wx.Panel(parent=self)
        #self._Panel.SetBackgroundColour(wx.RED)
        self._Panel.SetBackgroundColour(self.GetParent().GetBackgroundColour())

        # we create a sizer to ourselves and then add the panel
        self._Sizer = wx.BoxSizer(wx.VERTICAL)

        self._Sizer.AddSpacer(textHeight)
        self._Sizer.Add(self._Panel, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=dip(10))
        self.SetSizer(self._Sizer)
        

        # -------------- EVENTS --------------

        self.Bind(wx.EVT_PAINT, self.OnPaint)


    def __GetDefaultConfig(self) -> ControlConfig:
        return ControlConfig(
            border_colour=(0, 0, 0),
            border_width=1,
            corner_radius=1
        )
    

    def SetBackgroundColour(self, colour:wx.Colour):
        self.config.bg_colour = (colour.GetRed(), colour.GetGreen(), colour.GetBlue())
        self.Refresh()


    def GetBackgroundColour(self): 
        return wx.Colour(*self.config.bg_colour)


    def UpdateConfig(self, **kwargs):
        self.config.update(**kwargs)
        self.Refresh()


    def GetPanel(self):
        """ Returns the panel inside the staticbox.. """
        return self._Panel


    def SetLabel(self, label:str) -> None:
        self._Label = label
        self.Refresh()

        
    def OnPaint(self, event) -> None:

        # create dc
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()

        gc = wx.GraphicsContext.Create(dc)

        # get panel area
        rect = self.GetClientRect()

        brushBackground = wx.Brush(self.GetParent().GetBackgroundColour())

        # set background pen
        gc.SetBrush(brushBackground)

        # draw background
        gc.SetPen(wx.TRANSPARENT_PEN)
        gc.DrawRectangle(rect.GetX(), rect.GetY(),
                         rect.GetWidth(), rect.GetHeight())
        # draw rounded border
        penBorder = wx.Pen(wx.Colour(*self.config.border_colour), width=self.config.border_width)
        gc.SetPen(penBorder)

        paddingSides = penBorder.GetWidth()
        paddingTop = 10

        if self.config.corner_radius:
            gc.DrawRoundedRectangle(rect.GetX()+paddingSides,
                                    rect.GetY()+paddingTop,
                                    rect.GetWidth()-(2*paddingSides),
                                    rect.GetHeight()-paddingTop-paddingSides,
                                    dip(5))
        else:
            gc.DrawRectangle(rect.GetX()+paddingSides,
                             rect.GetY()+paddingTop,
                             rect.GetWidth()-(2*paddingSides),
                             rect.GetHeight()-paddingTop-paddingSides)
                             

        # draw label
        gc.SetPen(wx.TRANSPARENT_PEN)
        gc.SetBrush(brushBackground)
        gc.SetFont(wx.Font(self.config.font_size,
                           wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL,
                           faceName=self.config.font_face_name),
                   wx.Colour(*self.config.text_foreground_colour))
        textWidth, textHeight, _, _ = gc.GetFullTextExtent(self._Label)
        # centered values
        textX = (rect.GetWidth() // 2) - (textWidth // 2)
        textY = (paddingTop - textHeight//2)
        # draw text background
        lateralOffset = dip(5)
        gc.DrawRectangle(textX-lateralOffset, textY, textWidth+(2*lateralOffset), textHeight)
        # draw text
        gc.DrawText(self._Label, textX, textY)
        
