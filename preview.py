# preview.py
# wxCustomControls

# ---------------------- modules ---------------------- #

import wx

from src import CustomConfig
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

        # ------------------ set up configs ------------------ #

        config_panel = CustomConfig(border_width_default=1,
                                    corner_radius_default=dip(5),
                                    background_colour_default=(255, 255, 255),
                                    border_colour_default=(150, 150, 150))

        # -------------------- main panel -------------------- #

        P_main = wx.Panel(self)
        S_main = wx.BoxSizer(wx.VERTICAL)
        P_main.SetSizer(S_main)
        P_main.SetBackgroundColour(wx.GREEN)

        # ---------------------- buttons ---------------------- #

        P_buttons = CustomPanel(P_main, config=config_panel)

        wx.Button(P_buttons, label="test")

        b = CustomButton(P_buttons, label="test", size=(100, 30), pos=(250, 250))


        # ------------- add panels to main sizer ------------- #

        S_main.Add(P_buttons, 0, wx.EXPAND)
        S_main.Layout()
        

                
if __name__ == "__main__":
    app = wx.App()
    preview_frame = PreviewFrame(None)
    preview_frame.Show()
    app.MainLoop()
