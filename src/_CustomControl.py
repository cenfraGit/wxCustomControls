# _customControl.py
# wxCustomControls
# This class holds the basic attributes and functionality of all
# custom controls. The other control classes will inherit from this
# class and modify it as needed.
# 28/oct/2024


import wx
from .functions.getConfig import getConfig
from .CustomConfig import CustomConfig


class CustomControl(wx.Control):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.NO_BORDER,
                 validator=wx.DefaultValidator,
                 name=wx.ControlNameStr, config=None, **kwargs):

        super().__init__(parent, id, pos, size, style, validator, name)

        # ----------------- check for config ----------------- #

        self._config = getConfig(config, self.__class__.__name__)
        self._config.Update(**kwargs)

            
        # -------------- control state booleans -------------- #

        self._Enabled = True
        self._Pressed = False
        self._Hover = False


        # ----------------------- setup ----------------------- #

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.SetInitialSize(size)

        
        # ---------------------- events ---------------------- #

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.__OnEraseBackground)
        self.Bind(wx.EVT_ENTER_WINDOW, self.__OnMouseEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.__OnMouseLeave)

        # self.Bind(wx.EVT_PAINT, self.__OnPaint)
        # self.Bind(wx.EVT_LEFT_DCLICK, self.__OnLeftDown)
        # self.Bind(wx.EVT_LEFT_DOWN, self.__OnLeftDown)
        # self.Bind(wx.EVT_LEFT_UP, self.__OnLeftUp)
        
        
    def SetConfig(self, config:CustomConfig):
        self._config = config
        self.Refresh()

        
    def GetConfig(self):
        return self._config


    def UpdateConfig(self, **kwargs):
        self._config.Update(**kwargs)
        self.Refresh()


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


    def GetBackgroundColour(self):
        return wx.Colour(*self._config.background_colour_default)


    def DoGetBestClientSize(self):
        pass


    def __OnPaint(self, event):
        pass


    def __OnEraseBackground(self, event):
        pass


    def __OnLeftDown(self, event):
        pass


    def __OnLeftUp(self, event):
        pass


    def __OnMouseEnter(self, event):
        self._Hover = True
        self.Refresh()
        event.Skip()


    def __OnMouseLeave(self, event):
        self._Hover = False
        self.Refresh()
        event.Skip()


    def AcceptsFocus(self) -> bool:
        return False


    def AcceptsFocusFromKeyboard(self) -> bool:
        return False


    def Enable(self, enable:bool=True) -> None:
        """Uses _Enabled to define if the widget is enabled or not
        instead of using default behavior (problems redrawing after
        modal dialogs).
        """
        self._Enabled = enable
        super().Enable(enable)
        self.Refresh()


    def Disable(self) -> None:
        self.Enable(False)
        
