import wx
from random import randint

def rgb(valueList) -> wx.Colour:
    # if the input list is a valid rgb color, we return the correct wx.Colour object.
    # if the input is invalid, we return a wx.Colour object with a random rgb value.
    # 1. if the valueList is not a list (it can be None if a theme dictionary was not found)
    # 2. if the length of the list is not 3
    # 3. if the elements of the list are not integers
    if (not isinstance(valueList, list)) or (len(valueList) != 3) or (not all(isinstance(num, int) for num in valueList)):
        return wx.Colour(randint(0, 255), randint(0, 255), randint(0, 255))

    # return correct rgb color
    return wx.Colour(valueList[0], valueList[1], valueList[2])
