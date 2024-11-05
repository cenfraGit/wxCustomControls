import wx

def dip(*args):
    """Returns size using device independent pixels."""
    if len(args) == 1:
        return wx.ScreenDC().FromDIP(wx.Size(args[0], 0))[0]
    elif len(args) == 2:
        return wx.ScreenDC().FromDIP(wx.Size(args[0], args[1]))
    else:
        raise ValueError("DIP: Exceeded number of arguments.")
