"""
preview.py: An application that previews the currently available custom controls.

Note: The sizer add flag wx.EXPAND can be changed to wx.ALIGN_CENTER for better view.

Self-note: change panel to a scrollable panel to display more controls.
"""

import wx
from src.dip import dip
from src.themes import lightTheme, blueTheme
from src import CustomButton, CustomChoice, CustomCheckBox
if wx.Platform == "__WXMSW__":
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)


class PreviewPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # available themes: "light", "blue"
        theme = "blue"

        # background panel color
        if theme=="light":
            backgroundColor = lightTheme["background"]
        elif theme == "blue":
            backgroundColor = blueTheme["background"]
        else:
            backgroundColor = lightTheme["background"]
        self.SetBackgroundColour(backgroundColor)
        
        # create sizer to position controls
        self.sizer = wx.GridBagSizer(vgap=dip(10), hgap=dip(10))

        # button
        controlButton = CustomButton(parent=self, label="Control Test", theme=theme)
        self.sizer.Add(controlButton, pos=(0, 0), flag=wx.EXPAND)

        # choice
        choices = [f"value{counter}" for counter in range(10)]
        controlChoices = CustomChoice(parent=self, choices=choices, theme=theme)
        self.sizer.Add(controlChoices, pos=(1, 0), flag=wx.EXPAND)

        # checkbox
        controlCheckBox = CustomCheckBox(parent=self, label="Control Test", state=False, theme=theme)
        self.sizer.Add(controlCheckBox, pos=(2, 0), flag=wx.ALIGN_CENTER)

        self.sizer.AddGrowableCol(0, 1)
        self.SetSizer(self.sizer)

        # refresh when the panel (and frame) changes size
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, event):
        self.Refresh()
        self.Layout()


app = wx.App()
f = wx.Frame(parent=None, title="Custom Controls Preview", size=dip(400, 400))
p = PreviewPanel(parent=f)
f.Show()
app.MainLoop()
