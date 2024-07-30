"""
preview.py: An application that previews the currently available custom controls.

Note: The sizer add flag wx.EXPAND can be changed to wx.ALIGN_CENTER for better view.

Self-note: change panel to a scrollable panel to display more controls.
"""

import wx
#from src.dip import dip
#from src.themes import lightTheme, blueTheme
#from src import CustomButton, CustomChoice, CustomCheckBox, CustomTextCtrl

from src.functions.dip import dip
from src import CustomPanel
from src import CustomButton
from src import CustomChoice

if wx.Platform == "__WXMSW__":
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)


class PreviewPanel(CustomPanel):
    def __init__(self, theme="lightTheme", *args, **kwargs):
        super().__init__(theme, *args, **kwargs)
        
        # create sizer to position controls
        self.sizer = wx.GridBagSizer(vgap=dip(10), hgap=dip(10))

        # # button
        controlButton = CustomButton(parent=self, label="Control Test", theme=theme)
        self.sizer.Add(controlButton, pos=(0, 0), flag=wx.EXPAND)

        # choice
        choices = [f"value{counter}" for counter in range(10)]
        controlChoice = CustomChoice(parent=self, choices=choices, theme=theme)
        self.sizer.Add(controlChoice, pos=(1, 0), flag=wx.EXPAND)

        # # checkbox
        # controlCheckBox = CustomCheckBox(parent=self, label="Control Test", state=False, theme=theme)
        # self.sizer.Add(controlCheckBox, pos=(2, 0), flag=wx.ALIGN_CENTER)

        # # textctrl
        # controlTextCtrl = CustomTextCtrl(parent=self, value="testingvalues", theme=theme)
        # #controlTextCtrl.Disable()
        # self.sizer.Add(controlTextCtrl, pos=(3, 0), flag=wx.ALIGN_CENTER)

        self.sizer.AddGrowableCol(0, 1)
        self.SetSizer(self.sizer)

        # -------------- TEST EVENTS --------------
        
        self.Bind(wx.EVT_BUTTON, lambda e: print("button event"), controlButton)
        self.Bind(wx.EVT_CHOICE, lambda e: print("choice event"), controlChoice)
        

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
