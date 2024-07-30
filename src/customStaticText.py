import wx
from .functions.rgb import rgb
from .functions.getThemeDict import getThemeDict
from .functions.dip import dip


class CustomStaticText(wx.Control):    
    """Defines a custom static text that supports themes, wordrap,
    and some font styles."""
    
    def __init__(self, parent, id=wx.ID_ANY, label:str="",
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.NO_BORDER, validator=wx.DefaultValidator,
                 name="CustomStaticText", theme:str="lightTheme",
                 fontSize=8, faceName="Verdana", parentWordWrap=False):
        super().__init__(parent, id, pos, size, style, validator, name)


        """ If you want to use wordwrap, set the sizer flag to
        wx.EXPAND and set parentWordWrap to True.  """


        """ The idea is to have a wordwrapped statictext that works
        independently of the size of the string. It will also support
        bold and italic font styles. The plan is to go character by
        character to look for font style change indicators, which are
        the symbols '*' for bold, and '#' for italic. Whenever one of
        these symbols change, their respective attributes will be
        toggled. These attributes are used during the drawing process
        to use the correct font style for each character."""

        """ For the wordwrap feature, the control will keep track of
        the the top left coordinate of the first character of the
        current word (the first character after a space). It will then
        save the data of each character of the current word in the
        list self.CurrentWordCharacters, where each element is a
        dictionary that contains the character itself and its font. If
        during the drawing process the control detects that rendering
        the character would exceed the parent's width, it will:

        1. Clear the area from the beginning of the word up to the
           current character (already drawn characters)
        
        2. Increment self._VerticalOffset to draw in the next line
        
        3. Reset the horizontalOffset accumulator

        4. Redraw every character from the word up to this point (with
           its respective font style)

        5. Draw the new character.

        This ensures that the word begins in a new line while
        mantaining the font style properties for each character.

        There is flickering in the control when resizing the window.
        I may or not fix it.
        """
        

        # -------------- ATTRIBUTES --------------
        
        self._Label = label
        self._Theme = theme
        self._ThemeDict = {}
        self._FontSize = fontSize
        self._FaceName = faceName
        self._Size = size
        self._ParentWordWrap = parentWordWrap

        self._LineSpacing = dip(10)
        self._Bold = False
        self._Italic = False
        self._Underline = False

        self._CurrentWordCharacters = []
        self._CurrentWordWidth = 0
        self._BeginningTopLeft = [0, 0]
        self._VerticalOffset = 0
        

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
        # get the parent width
        parentWidth = self.GetParent().GetClientSize()[0] if (self._Size == wx.DefaultSize) else self._Size[0]

        # make backgrund 'transparent'
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour(), wx.BRUSHSTYLE_SOLID))
        #dc.SetBrush(wx.GREEN_BRUSH)
        dc.DrawRectangle(rect)

        # set text foreground
        dc.SetTextForeground(self._ThemeDict["textForegroundDefault"])

        # offset accumulators these offsets control the position of
        # the characters. the horizontalOffset controls the horizontal
        # position of each character and the vertical offset basically
        # controls the line where the chacater is being drawn (used in
        # wordwrap).

        # horizontal offset accumulator
        horizontalOffset = 0
        # vertical offset (line spacing)
        self._VerticalOffset = 0


        # we iterate through each character in the string
        
        for index, character in enumerate(self._Label):

            # if the symbol is a backlash, we will render the next
            # character as is. we will not do anything if the current
            # character is a backlash. this will be handled in the
            # next iteration
            if (character == "\\"):
                continue

            # this is the next iteration. if the previous characater
            # was a backlash (or if it is not a backlash, but the
            # current character is not a font style change indicator,
            # meaning that it is a normal character), we will draw the
            # character as is.
            if (self._Label[index-1] == "\\") or (self._Label[index-1] != "\\" and character not in ['*', '#']):
                
                # we first define fontStyle and fontWeight according
                # to the current attribute values
                fontStyle = wx.FONTSTYLE_ITALIC if self._Italic else wx.FONTSTYLE_NORMAL
                fontWeight = wx.FONTWEIGHT_BOLD if self._Bold else wx.FONTWEIGHT_NORMAL

                # we create a font with the correct font style
                font = wx.Font(self._FontSize,
                               wx.FONTFAMILY_DEFAULT,
                               fontStyle,
                               fontWeight,
                               faceName=self._FaceName)
                
                # we get the character dimensions
                dc.SetFont(font)
                textWidth, textHeight = dc.GetTextExtent(character)


                # if the character is the beginning of a new word
                if (self._Label[index-1] == " ") or (self._Label[index-1] == "\\" and self._Label[index-1] == " "):
                    # save top left position of word beginning
                    self._BeginningTopLeft = [horizontalOffset, self._VerticalOffset]
                    # reset current word characters data and add this character
                    self._CurrentWordCharacters = [{"character": character, "font": font}]
                    # reset word width and add current beginning of word
                    self._CurrentWordWidth = textWidth
                # if the character is not the beginning of a new word,
                # append to the current word characters
                else:
                    # append to new list
                    self._CurrentWordCharacters.append({"character": character, "font": font})
                    # add width to current word width
                    self._CurrentWordWidth += textWidth
                
                # we now check if drawing the character would exceed
                # the parent width (in case of working with wordwrap)
                
                if (horizontalOffset + textWidth >= parentWidth):

                    # if the word is as big as the line, just dont do anything
                    if (self._CurrentWordWidth > parentWidth):
                        horizontalOffset += textWidth
                        continue

                    # if the character exceeds the width, we will
                    # clear the already drawn characters from the
                    # current word, draw them in the next line and
                    # keep drawing from there: clear from the
                    # beginning of the current word (top left) to this
                    # character's bottom right. Then we change the
                    # linespacing, reset the horizontalOffset (the X
                    # accumulator) so that the text is rendered at the
                    # next line

                    # clear already drawn characters from the current
                    # word
                    dc.SetPen(wx.TRANSPARENT_PEN)
                    dc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour(), wx.BRUSHSTYLE_SOLID))
                    dc.DrawRectangle(*self._BeginningTopLeft, self._CurrentWordWidth, textHeight)

                    # modify accumulators
                    horizontalOffset = 0
                    self._VerticalOffset += self._LineSpacing + textHeight

                    # draw the word characters in the next line
                    for data in self._CurrentWordCharacters:
                        dc.SetFont(data["font"])
                        textWidth, textHeight = dc.GetTextExtent(data["character"])
                        dc.DrawText(data["character"], horizontalOffset, self._VerticalOffset)
                        horizontalOffset += textWidth

                    # go to next itertion of the loop
                    continue
                    

                # if drawing the character would not exceed the
                # parent's width, draw normally
                dc.DrawText(character, horizontalOffset, self._VerticalOffset)
                
                # increase offset for next character
                horizontalOffset += textWidth
                
                # next iteration
                continue
                
            
            # if we got here, it means that the current character is
            # an indicator for a font style change. we just need to
            # toggle its respective attribute.
            if (character == "*"):
                self._Bold = not self._Bold
            elif (character == "#"):
                self._Italic = not self._Italic

        # if we are using wordwrap, we need to dynamically change the
        # control's width and height to be displayed properly. we
        # create a new rectangle area and sets its width to the
        # parent's width and the height as the verticalOffset (the
        # total height of the wordwrapped text). we finally set it to
        # our control's client rectangle.
        if (self._ParentWordWrap):
            newRect = wx.Rect(0, 0, self.GetParent().GetClientSize()[0], self._VerticalOffset+textHeight)
            self.SetClientRect(newRect)


    def DrawCharacter(self, dc:wx.AutoBufferedPaintDC, character:str, x, y):

        """ Used to draw the character during the text rendering process. """
        
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
        #textWidth, textHeight = dc.GetTextExtent(character)
        dc.DrawText(character, x, y)
        

    def OnEraseBackground(self, event) -> None:
        """ Bound to prevent flickering. """
        pass


    def DoGetBestClientSize(self) -> wx.Size:
        """ Determines the best size for the control. """

        """The label will use the parent's width as its width, unless
        a different size is specified.
        """
        
        # create font
        font = wx.Font(self._FontSize,
                       wx.FONTFAMILY_DEFAULT,
                       wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_NORMAL,
                       faceName=self._FaceName)

        # create device context and set font to determine text dimensions
        dc = wx.ClientDC(self)
        dc.SetFont(font)

        # get label dimensions
        textWidth, textHeight = dc.GetTextExtent(self._Label)
        
        #width = textWidth if self._UseTextWidth else self.GetParent().GetClientSize()[0]
        width = self.GetParent().GetClientSize()[0] if (self._ParentWordWrap) else textWidth
        height = textHeight

        return wx.Size(width, height)

    

    def AcceptsFocusFromKeyboard(self) -> bool:
        return False
    
