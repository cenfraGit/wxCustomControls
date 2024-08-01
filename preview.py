"""
preview.py: An application that previews the currently available custom controls.

Note: The sizer add flag wx.EXPAND can be changed to wx.ALIGN_CENTER for better view.

Self-note: change panel to a scrollable panel to display more controls.
"""

import wx

from src.functions.dip import dip
#from src import CustomPanel

from src import RoundedPanel
from src import CustomButton
#from src import CustomChoice
#from src import CustomCheckBox
#from src import CustomStaticText
#from src import CustomStaticBox
#from src import CustomRadioBox


if wx.Platform == "__WXMSW__":
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

theme = "lightTheme"
#theme = "blueTheme"

class PreviewPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # create sizer to position controls
        self.sizer = wx.BoxSizer(orient=wx.VERTICAL)

        # buttons panel
        buttonsPanel = RoundedPanel(parent=self, backgroundColour=wx.Colour(140, 140, 140), radius=10)
        buttonsPanelSizer = wx.GridBagSizer(hgap=dip(5))
        button1 = CustomButton(buttonsPanel, label="Custom Button 1")
        button2 = CustomButton(buttonsPanel, label="Custom Button 2")
        button3 = CustomButton(buttonsPanel, label="Custom Button 3")
        buttonsPanelSizer.Add(button1, pos=(0, 0), flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.EXPAND, border=dip(10))
        buttonsPanelSizer.Add(button2, pos=(0, 1), flag=wx.TOP|wx.BOTTOM|wx.EXPAND, border=dip(10))
        buttonsPanelSizer.Add(button3, pos=(0, 2), flag=wx.TOP|wx.BOTTOM|wx.RIGHT|wx.EXPAND, border=dip(10))
        buttonsPanelSizer.AddGrowableCol(0, 1)
        buttonsPanelSizer.AddGrowableCol(1, 1)
        buttonsPanelSizer.AddGrowableCol(2, 1)
        buttonsPanel.SetSizer(buttonsPanelSizer)
        self.sizer.Add(window=buttonsPanel, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=dip(10))
        
        
        
        # button
        #controlButton = CustomButton(parent=self, label="Control Test")
        #self.sizer.Add(controlButton, pos=(0, 0), flag=wx.ALIGN_CENTER)

        # choice
        #choices = [f"value{counter}" for counter in range(10)]
        #controlChoice = CustomChoice(parent=self, choices=choices, theme=theme)
        #self.sizer.Add(controlChoice, pos=(1, 0), flag=wx.EXPAND)

        # checkbox
        #controlCheckBox = CustomCheckBox(parent=self, label="Control Test", value=False, theme=theme)
        #self.sizer.Add(controlCheckBox, pos=(2, 0), flag=wx.ALIGN_CENTER)

        # # textctrl
        # controlTextCtrl = CustomTextCtrl(parent=self, value="testingvalues", theme=theme)
        # #controlTextCtrl.Disable()
        # self.sizer.Add(controlTextCtrl, pos=(3, 0), flag=wx.ALIGN_CENTER)

        # statictext
        #text = r"""Freedom or jail, clips inserted, a baby's being born same time a man is #murdered#, the *beginning* and end, as far as rap go, it's only *#natural*#, I explain my plateau and also, what *defines* my name"""
        #controlStaticText = CustomStaticText(parent=self, label=text, theme=theme, parentWordWrap=True)
        #self.sizer.Add(controlStaticText, pos=(4, 0), flag=wx.EXPAND)

        # staticboxbox
        #panelStaticText = CustomStaticBox(parent=self, label="Control Test", theme=theme, size=dip(-1, 50))
        #self.sizer.Add(panelStaticText, pos=(5, 0), flag=wx.EXPAND)
        #self.sizer.AddGrowableRow(5, 1)

        
        #controlRadio = CustomRadioButton(parent=self, label="Control test", theme=theme)
        #self.sizer.Add(controlRadio, pos=(6, 0), flag=wx.ALIGN_CENTER)

        #controlRadioBox = CustomRadioBox(parent=self, labels=["value1", "value2", "value3", "testingbatman"], value="value2", orientation="horizontal")
        #self.sizer.Add(controlRadioBox, pos=(6, 0), flag=wx.ALIGN_CENTER)
        
        
        #self.sizer.AddGrowableCol(0, 1)
        self.SetSizer(self.sizer)

        # -------------- TEST EVENTS --------------
        
        #self.Bind(wx.EVT_BUTTON, lambda e: print("button event"), controlButton)
        #self.Bind(wx.EVT_CHOICE, lambda e: print("choice event"), controlChoice)
        #self.Bind(wx.EVT_CHECKBOX, lambda e: print("checkbox event"), controlCheckBox)
        
        # refresh when the panel (and frame) changes size
        
        self.Bind(wx.EVT_SIZE, self.OnSize)



        

    def OnSize(self, event):
        self.Refresh()
        self.Layout()


app = wx.App()
f = wx.Frame(parent=None, title="Custom Controls Preview", size=dip(400, 400))
f.SetMinClientSize(dip(500, 500))
p = PreviewPanel(parent=f)
f.Show()
app.MainLoop()
