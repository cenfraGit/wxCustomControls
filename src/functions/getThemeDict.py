import os
import json

def getThemeDict(themeString:str):

        """Returns a tuple containing the state of the operation (if
        it was successful or not) and the theme's dictionary. If the
        operation is unsuccessful (the specified theme was not found),
        the function will return the theme's dictionary from the first
        available theme (assuming at least one was found).
        """

        # we get the path of the themes directory within the package
        themesDirectory = os.path.join(os.path.dirname(__file__), "..", "themes")

        # function will not continue if path doesnt exist
        if not os.path.exists(themesDirectory):
            return False, {}

        # get available theme names (.json files)
        themeNames = [os.path.splitext(filename)[0] for filename in os.listdir(themesDirectory) if os.path.splitext(filename)[1] == ".json"]

        # function will not continue if no available themes were found
        # (program crashes because no themes can be used???)
        if not themeNames:
            return False, {}

        # if the theme exists, we use it.
        if themeString in themeNames:
            chosenTheme = themeString
            state = True
        # if the specified theme does not exist, we will use the first
        # available theme in the directory.
        else:
            chosenTheme = themeNames[0]
            state = False

        # open the json file that will be used
        with open(os.path.join(themesDirectory, f"{chosenTheme}.json")) as file:
            return state, json.load(file)
