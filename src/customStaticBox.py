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

        if config:
            self.config:ControlConfig = copy(config)
        else:
            self.config:ControlConfig = self.__GetDefaultConfig()

        if kwargs:
            self.config.update(**kwargs)
        

        # ------------------ attributes ------------------ #

        self._Label = label

        # get text extent for panel top padding
        dc = wx.ScreenDC()
        dc.SetFont(wx.Font(self.config.font_size,
                           wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL,
                           faceName=self.config.font_face_name))
        _, self.textHeight = dc.GetTextExtent(self._Label)
        
        
        # ------------------ appearance ------------------ #

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.SetInitialSize(size)


        # ---------------- panel inside  ---------------- #

        padding_sides = self.config.padding_all_sides if self.config.padding_all_sides else dip(8)

        self._Panel = wx.Panel(parent=self)
        self._Panel.SetBackgroundColour(self.GetParent().GetBackgroundColour())

        # we create a sizer to ourselves and then add the panel with the inner padding
        self._Sizer = wx.BoxSizer(wx.VERTICAL)
        self._Sizer.AddSpacer(self.textHeight)
        self._Sizer.Add(self._Panel, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=padding_sides)
        self.SetSizer(self._Sizer)


        # -------------- EVENTS --------------

        self.Bind(wx.EVT_PAINT, self.OnPaint)


    def __GetDefaultConfig(self) -> ControlConfig:
        return ControlConfig(
            border_colour=(0, 0, 0),
            border_width=1,
            corner_radius=0)
    

    def SetBackgroundColour(self, colour:wx.Colour):
        self.BackgroundColour = colour
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

        # --------------- create contexts  --------------- #
        
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()

        gc:wx.GraphicsContext = wx.GraphicsContext.Create(dc)

        # -------------- drawing rectangle -------------- #

        rect = self.GetClientRect()

        
        # ------------- background rectangle ------------- #

        gc.SetPen(wx.TRANSPARENT_PEN)
        gc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour()))
        gc.DrawRectangle(rect.GetX(),
                         rect.GetY(),
                         rect.GetWidth(),
                         rect.GetHeight())

        
        # ------------------ pen border ------------------ #
        
        gc.SetPen(wx.Pen(wx.Colour(*self.config.border_colour), width=self.config.border_width))

        paddingSides = self.config.border_width
        paddingTop = self.textHeight//2


        gc.DrawRoundedRectangle(rect.GetX()+paddingSides,
                                rect.GetY()+paddingTop,
                                rect.GetWidth()-(2*paddingSides),
                                rect.GetHeight()-paddingTop-paddingSides,
                                self.config.corner_radius)
            

        # ------------------ draw label ------------------ #
        
        gc.SetPen(wx.TRANSPARENT_PEN)
        gc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour()))
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
        
