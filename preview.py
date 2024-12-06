# preview.py
# wxCustomControls
# Frame with a preview of the available controls.


import wx
import os
from src import CustomConfig
from src import CustomPanel
from src import CustomStaticBox
from src import CustomButton
from src import CustomCheckBox
from src import CustomRadioButton
from src import CustomScrolledWindow
from src import CustomComboBox
from src import dip
from src import setDpiAwareness
setDpiAwareness()


class PreviewFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.SetTitle("Custom Controls Preview")
        # self.SetInitialSize(dip(700, 800))
        self.initialize_ui()       

        
    def initialize_ui(self) -> None:

        # the custom controls have certain attributes that can be
        # changed optionally. You can do this either by passing them a
        # CustomConfig object or by passing the values to these
        # attributes as arguments directly.

        # creating a CustomConfig object with the values can be
        # convenient if you plan on creating several custom controls
        # that have the same look and feel. You can simply pass the
        # same CustomConfig to all your custom controls and that's it.

        # if you don't pass any of these customization attributes, the
        # custom control will get its default look, which you can also
        # change later.

        # NOTE: when you pass a CustomConfig object to a custom
        # control, it internally creates its own copy of the
        # CustomConfig object (essentially getting its value instead
        # of reference). This is done to prevent unwanted behavior
        # when altering the original CustomConfig object.

        # only the default appearance of the custom controls will be
        # changed in this preview, but modifying the appearance for
        # other control states is also possible (such as the control
        # being pressed).

        # ----------------- set up custom configs ----------------- #

        # this is the custom configuration for the panels that will
        # group the showcased controls throughout this preview. Will
        # be used multiple times.
        configPanel = CustomConfig(border_width_default=1,
                                   corner_radius_default=dip(5),
                                   background_colour_default=(255, 255, 255),
                                   border_colour_default=(150, 150, 150))

        # some custom control examples will involve images
        image = wx.Image(os.path.join("images", "t.png"))
        image_size = dip(50, 50)

        # -------------------- main panel -------------------- #

        P_main = wx.Panel(self)
        S_main = wx.BoxSizer(wx.VERTICAL)
        P_main.SetSizer(S_main)

        # CustomScrolledWindow: this is a window that contains the
        # scrolled panel and the scrollbars. In order to add items to
        # the scrollable panel, you must first get the reference to
        # the panel, assign a GRIDBAGSIZER to it, and then add the
        # items to the sizer. why use GridBagSizer? BoxSizer simply
        # didn't work well. I don't know why.

        sw = CustomScrolledWindow(P_main, scrollX=True, scrollY=True)

        P_scrolled = sw.GetPanel()
        S_scrolled = wx.GridBagSizer()
        P_scrolled.SetSizer(S_scrolled)

        S_main.Add(sw, 1, wx.EXPAND) # add the CustomScrolledWindow to
                                     # the main panel sizer.

        # --------------------- buttons panel --------------------- #
        # panel to showcase some button examples.
        
        P_buttons = CustomPanel(P_scrolled, config=configPanel)
        S_buttons = wx.GridBagSizer()
        P_buttons.SetSizer(S_buttons)

        buttonText = "Custom Button"

        # custom buttons examples: since the custom buttons are meant
        # to be different, we will opt for passing the appearance
        # attributes directly to them instead of creating a CustomConfig.
        
        button1 = CustomButton(P_buttons, label=buttonText)
        button2 = CustomButton(P_buttons, label=buttonText, size=dip(-1, 40),
                               background_colour_default=(255, 255, 255),
                               border_colour_default=(0, 0, 0),
                               border_width_default=2)
        button3 = CustomButton(P_buttons, label=buttonText,
                               background_linear_gradient_default=(0, 5, 0, 60, (180, 0, 180), (0, 180, 180)),
                               border_width_default=0, corner_radius_default=5)
        button4 = CustomButton(P_buttons, label=buttonText,
                               background_linear_gradient_default=(0, 5, 40, 100, (185, 43, 39), (21, 101, 192)),
                               border_width_default=0, corner_radius_default=10,
                               text_foreground_colour_default=(220, 220, 220))

        button5 = CustomButton(P_buttons, label=buttonText,
                               image_default=image, image_size_default=image_size)
        button6 = CustomButton(P_buttons, label=buttonText,
                               image_default=image, image_size_default=image_size, image_text_side="left")
        button7 = CustomButton(P_buttons, label=buttonText,
                               image_default=image, image_size_default=image_size, image_text_side="up")
        button8 = CustomButton(P_buttons, label=buttonText,
                               image_default=image, image_size_default=image_size, image_text_side="down")


        S_buttons.Add(button1, pos=(0, 0), flag=wx.EXPAND|wx.LEFT|wx.TOP, border=dip(9))
        S_buttons.Add(button2, pos=(0, 1), flag=wx.EXPAND|wx.LEFT|wx.TOP, border=dip(9))
        S_buttons.Add(button3, pos=(0, 2), flag=wx.EXPAND|wx.LEFT|wx.TOP, border=dip(9))
        S_buttons.Add(button4, pos=(0, 3), flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, border=dip(9))

        S_buttons.Add(button5, pos=(1, 0), flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, border=dip(9))
        S_buttons.Add(button6, pos=(1, 1), flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, border=dip(9))
        S_buttons.Add(button7, pos=(1, 2), flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, border=dip(9))
        S_buttons.Add(button8, pos=(1, 3), flag=wx.EXPAND|wx.ALL, border=dip(9))

        S_buttons.AddGrowableCol(0, 1)
        S_buttons.AddGrowableCol(1, 1)
        S_buttons.AddGrowableCol(2, 1)
        S_buttons.AddGrowableCol(3, 1)

        S_buttons.Layout()

        # --------------------- checkbox panel --------------------- #

        
        
        # c = CustomCheckBox(P_buttons,
        #                    label="test",
        #                    pos=(350, 100),
        #                    image_default=image,
        #                    image_size_default=image_size,
        #                    image_text_side="up",
        #                    checkbox_text_side="up",
        #                    switch_appearance=True)



        # -------------- add panels to scrolled sizer -------------- #

        # now we add all of the grouping panels to the scrolled
        # panel's sizer.
        
        S_scrolled.Add(P_buttons, pos=(0, 0), flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, border=dip(8))

        
        S_scrolled.AddGrowableCol(0, 1)

        

        
        

        

        # # ---------------------- buttons ---------------------- #

        # P_buttons = CustomPanel(P_main, config=config_panel)

        # image = wx.Image(os.path.join("images", "t.png"))
        


        # b = CustomButton(P_buttons,
        #                  label="test",
        #                  image_default=image,
        #                  image_size_default=image_size,
        #                  corner_radius_default=dip(10),
        #                  image_text_side="up",
        #                  pos=(250, 250))



        # c = CustomCheckBox(P_buttons,
        #                    label="test",
        #                    pos=(350, 100),
        #                    image_default=image,
        #                    image_size_default=image_size,
        #                    image_text_side="up",
        #                    checkbox_text_side="up",
        #                    switch_appearance=True)


        # r = CustomRadioButton(P_buttons,
        #                       label="testing",
        #                       pos=(400, 220),
        #                       style=wx.RB_GROUP)
        # r1 = CustomRadioButton(P_buttons,
        #                       label="testing1",
        #                       pos=(400, 250))
        # r2 = CustomRadioButton(P_buttons,
        #                       label="testing2",
        #                       pos=(400, 280))

        # t = CustomStaticBox(P_buttons, label="test", size=(100, 100))






        

        # self.sw = CustomScrolledWindow(P_main, pos=(0, 500), size=(300, 200), scrollX=True, scrollY=True)
        # sw_panel = self.sw.GetPanel()
        # sw_panel.SetBackgroundColour(wx.RED)
        # sw_sizer = wx.GridBagSizer()
        # sw_panel.SetSizer(sw_sizer)
        # for i in range(30):
        #     sw_sizer.Add(wx.Button(sw_panel, label="test"), pos=(i, i))
        # sw_sizer.Layout()
        

        # ------------- add panels to main sizer ------------- #
        

        # self.sw = CustomScrolledWindow(P_main, scrollX=True, scrollY=True)
        # sw_panel = self.sw.GetPanel()
        # sw_panel.SetBackgroundColour(wx.RED)
        # sw_sizer = wx.GridBagSizer()
        # sw_panel.SetSizer(sw_sizer)
        # for i in range(20):
        #     cb = CustomComboBox(sw_panel, value="test", choices=["one", "two", "three"])
        #     sw_sizer.Add(cb, pos=(i, i))
        # sw_sizer.Layout()


        # S_main.Add(P_buttons, 1, wx.EXPAND)

        # S_main.Add(sw, 1, wx.EXPAND)
        S_main.Layout()
        

                
if __name__ == "__main__":
    app = wx.App()
    preview_frame = PreviewFrame(None)
    preview_frame.Show()
    app.MainLoop()
