import wx
from .functions.rgb import rgb
from .functions.getThemeDict import getThemeDict
from .functions.dip import dip


class CustomStaticText(wx.Control):    
    """ Defines a custom static text that supports themes, wordrap, and some font styles. """
    
    def __init__(self, parent, id=wx.ID_ANY, label:str="",
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.NO_BORDER, validator=wx.DefaultValidator,
                 name="CustomStaticText", theme:str="lightTheme",
                 fontSize=8, faceName="Verdana"):
        super().__init__(parent, id, pos, size, style, validator, name)

        # -------------- ATTRIBUTES --------------
        
        self._Label = label
        self._Theme = theme
        self._ThemeDict = {}
        self._FontSize = fontSize
        self._FaceName = faceName

        self._LineSpacing = dip(10)
        self._Bold = False
        self._Italic = False
        self._Underline = False

        self._NewWord = False
        self._CurrentWordString = ""
        self._CurrentWordRectangles = []
        

        # -------------- APPEARANCE --------------
        
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.setTheme(self._Theme)
        self.SetInitialSize(size)
        

        # -------------- EVENTS --------------
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        

    def setTheme(self, themeString:str) -> None:
        """Sets the theme. If the theme is not valid, the first
        available theme will be chosen. Or if we definitely didnt find
        a theme, the rgb color will automatically display a random
        color.
        """
        
        # the getThemeDict returns the state of the operation and the
        # theme dictionary. we do not need the state right now.
        _, self._ThemeDict = getThemeDict(themeString)

        # refresh with changes
        self.Refresh()

        
    def SetLabel(self, label:str) -> None:
        """ Sets the control's label text. """
        self._Label = label
        self.Refresh()
        

    def OnPaint(self, event) -> None:
        """ Handles the paint event. """
        
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        self.Draw(dc)
        

    def Draw(self, dc:wx.AutoBufferedPaintDC) -> None:
        """ Draws the actual control. """

        # get drawing area
        rect = self.GetClientRect()

        # horizontal offset accumulator
        horizontalOffset = 0
        # vertical offset (line spacing)
        verticalOffset = 0

        listOfCharacters = list(self._Label)

        # we will use backlash as an indicator that the next character
        # should be rendered as is. 

        for index, character in enumerate(listOfCharacters):

            # next iteration we will take care of drawing the next
            # symbol
            if (character == "\\"):
                continue

            # check if character is new word
            if (listOfCharacters[index-1] == " "):
                self._NewWord = True
                # reset current word
                self._CurrentWordString = "" + character

            # if character in the middle of the word
            # if the next index exists and it is not space
            if (listOfCharacters[index-1] != " ") and (index+1 < len(listOfCharacters) and listOfCharacters[index+1] != " "):
                self._CurrentWordString += character

            # check if this character is the end of the word
            # if the next index exists and it is not space
            if (index+1 < len(listOfCharacters) and listOfCharacters[index+1] == " "):
                self._CurrentWordString += character
                self._NewWord = False
                print(self._CurrentWordString)
                
                

            # draw next character as is if: the previous character is
            # a backslash or if the previous character is not a
            # backslash but the character is not an indicator symbol
            # either
            if (listOfCharacters[index-1] == "\\") or (listOfCharacters[index-1] != "\\" and character not in ['*', '#']):
                
                # first assign fontStyle and fontWeight according to values
                fontStyle = wx.FONTSTYLE_ITALIC if self._Italic else wx.FONTSTYLE_NORMAL
                fontWeight = wx.FONTWEIGHT_BOLD if self._Bold else wx.FONTWEIGHT_NORMAL

                # create font
                font = wx.Font(self._FontSize,
                               wx.FONTFAMILY_DEFAULT,
                               fontStyle,
                               fontWeight,
                               faceName=self._FaceName)
                dc.SetFont(font)

                # draw character
                textWidth, textHeight = dc.GetTextExtent(character)
                dc.DrawText(character, horizontalOffset, verticalOffset)
                
                # increase offset for next character
                horizontalOffset += textWidth
                
                # next iteration
                continue
                
            
            # check if the character is a font type indicator
            if (character == "*"):
                self._Bold = not self._Bold
            elif (character == "#"):
                self._Italic = not self._Italic
            elif (character == "_"):
                self._Underline = not self._Underline


    def DrawCharacter(self, dc:wx.AutoBufferedPaintDC, character:str, x, y):
        
        # first assign fontStyle and fontWeight according to values
        fontStyle = wx.FONTSTYLE_ITALIC if self._Italic else wx.FONTSTYLE_NORMAL
        fontWeight = wx.FONTWEIGHT_BOLD if self._Bold else wx.FONTWEIGHT_NORMAL

        # create font
        font = wx.Font(self._FontSize,
                       wx.FONTFAMILY_DEFAULT,
                       fontStyle,
                       fontWeight,
                       faceName=self._FaceName)
        dc.SetFont(font)

        # draw character
        textWidth, textHeight = dc.GetTextExtent(character)
        dc.DrawText(character, x, y)
        

    def OnEraseBackground(self, event) -> None:
        """ Bound to prevent flickering. """
        pass


    def DoGetBestClientSize(self) -> wx.Size:
        """ Determines the best size for the control. """

        
        # # create font
        # font = wx.Font(self._FontSize,
        #                wx.FONTFAMILY_DEFAULT,
        #                wx.FONTSTYLE_NORMAL,
        #                wx.FONTWEIGHT_NORMAL,
        #                faceName=self._FaceName)

        # # create device context and set font to determine text dimensions
        # dc = wx.ClientDC(self)
        # dc.SetFont(font)

        # # get label dimensions
        # textWidth, textHeight = dc.GetTextExtent(self._Label)

        # # margins for sides
        # leftRightMargins = dip(20)
        # topBottomMargins = dip(5)

        # # final control dimensions
        # width = leftRightMargins*2 + textWidth
        # height = topBottomMargins*2 + textHeight

        # # return best size
        # return wx.Size(width, height)

        return wx.Size(300, 300)
    

    def AcceptsFocusFromKeyboard(self) -> bool:
        return False
    
