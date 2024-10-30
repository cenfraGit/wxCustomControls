# preview.py
# wxCustomControls

# ---------------------- modules ---------------------- #

import wx

from src import CustomPanel
from src import CustomButton

# necessary for high dpi displays (windows)
from src import dip
from src import setDpiAwareness
setDpiAwareness()


class PreviewFrame(wx.Frame):
    def __init__(self, *args, **kwargs):

        # -------------------- initialize -------------------- #
        
        super().__init__(*args, **kwargs)
        

        # -------------------- frame setup -------------------- #

        self.SetTitle("Custom Controls Preview")
        self.SetInitialSize(dip(700, 500))
        

        # ------------------------ gui ------------------------ #

        self.initialize_ui()
        

    def initialize_ui(self):

        P_main = wx.Panel(self)
        S_main = wx.BoxSizer(wx.VERTICAL)
        P_main.SetSizer(S_main)

        P_main.SetBackgroundColour(wx.GREEN)

        CustomPanel(P_main, size=wx.Size(100, 100), pos=wx.Point(50, 50),
                    border_width_default=1,
                    corner_radius_default=10)

        CustomButton(P_main, size=(50, 20), pos=(50, 150), label="test")
    
        

        
if __name__ == "__main__":
    app = wx.App()
    preview_frame = PreviewFrame(None)
    preview_frame.Show()
    app.MainLoop()
