# getImageTextCoordinates.py
# wxCustomControls
# Function that returns the top left coordinates for both an image and
# text (when they are drawn together).
# 30/oct/2024


import wx
from ..CustomConfig import CustomConfig
from ..utils.dip import dip


def getImageTextCoordinates(rectangle:wx.Rect,
                            text, config:CustomConfig,
                            imageWidth:int, imageHeight:int,
                            textWidth:int, textHeight:int):

    textX, textY = 0, 0
    imageX, imageY = 0, 0

    # -------------------- if no text -------------------- #
    
    if (text == wx.EmptyString):
        # image in center if no text
        imageX = (rectangle.GetWidth() // 2) - (imageWidth // 2)
        imageY = (rectangle.GetHeight() // 2) - (imageHeight // 2)

    # ------------- if no image (dimensions) ------------- #

    elif (imageWidth == 0 or imageHeight == 0):
        # calculate center
        textX = rectangle.GetX() + (rectangle.GetWidth() // 2) - (textWidth // 2)
        textY = rectangle.GetY() + (rectangle.GetHeight() // 2) - (textHeight // 2)

    # -------------- if both image and text -------------- #
    
    else:
        text_separation = config.image_text_separation if config.image_text_separation else dip(6)
        if (config.text_side == "right"):
            imageX = (rectangle.GetWidth() // 2) - ((imageWidth + textWidth + text_separation) // 2) 
            imageY = (rectangle.GetHeight() // 2) - (imageHeight // 2)
            textX = imageX + imageWidth + text_separation
            textY = (rectangle.GetHeight() // 2) - (textHeight // 2)
        elif (config.text_side == "left"):
            textX = (rectangle.GetWidth() // 2) - ((imageWidth + textWidth + text_separation) // 2) 
            textY = (rectangle.GetHeight() // 2) - (textHeight // 2)
            imageX = textX + textWidth + text_separation
            imageY = (rectangle.GetHeight() // 2) - (imageHeight // 2)
        elif (config.text_side == "up"):
            textX = (rectangle.GetWidth() // 2) - (textWidth // 2)
            textY = (rectangle.GetHeight() // 2) - ((imageHeight + textHeight + text_separation) // 2)
            imageX = (rectangle.GetWidth() // 2) - (imageWidth // 2)
            imageY = textY + textHeight + text_separation
        elif (config.text_side == "down"):
            imageX = (rectangle.GetWidth() // 2) - (imageWidth // 2)
            imageY = (rectangle.GetHeight() // 2) - ((imageHeight + textHeight + text_separation) // 2)
            textX = (rectangle.GetWidth() // 2) - (textWidth // 2)
            textY = imageY + imageHeight
        else:
            raise ValueError("text_side must be left, right, up or down.")
        
    return imageX, imageY, textX, textY



    
