# preview.py
# wxCustomControls
# Frame with a preview of the available controls.


# ---------------------- modules ---------------------- #

import wx
import os

from src import CustomConfig
from src import CustomPanel
from src import CustomButton
from src import CustomCheckBox

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


        image = wx.Image(os.path.join("images", "t.png"))
        image_size = dip(50, 50)


        b = CustomButton(P_buttons,
                         label="test",
                         image_default=image,
                         image_size_default=image_size,
                         corner_radius_default=dip(10),
                         text_side="up",
                         pos=(250, 250))

        c = CustomCheckBox(P_buttons,
                           label="test",
                           size=(80, 30),
                           pos=(500, 250),
                           switch_appearance=True),
        

        # ------------- add panels to main sizer ------------- #

        S_main.Add(P_buttons, 0, wx.EXPAND)
        S_main.Layout()
        

                
if __name__ == "__main__":
    app = wx.App()
    preview_frame = PreviewFrame(None)
    preview_frame.Show()
    app.MainLoop()
