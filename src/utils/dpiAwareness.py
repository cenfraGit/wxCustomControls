import ctypes
import platform

def setDpiAwareness():
    if platform.system() == "Windows":
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
