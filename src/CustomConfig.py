# controlConfig.py
# wxCustomControls
# Class for handling control appearance configuration. Sets default
# valuesif not specified as keyword arguments.
# 28/oct/2024


import wx


class CustomConfig:
    def __init__(self, **kwargs):

        # ---------------------- cursor ---------------------- #

        self.cursor_stockcursor_pressed  = kwargs.get("cursor_stockcursor_pressed",  wx.CURSOR_ARROW)
        self.cursor_stockcursor_hover    = kwargs.get("cursor_stockcursor_hover",    wx.CURSOR_ARROW)
        self.cursor_stockcursor_disabled = kwargs.get("cursor_stockcursor_disabled", wx.CURSOR_ARROW)

        # ----------------------- text ----------------------- #

        self.text_font_size_default  = kwargs.get("text_font_size_default",  8)
        self.text_font_size_pressed  = kwargs.get("text_font_size_pressed",  8)
        self.text_font_size_hover    = kwargs.get("text_font_size_hover",    8)
        self.text_font_size_disabled = kwargs.get("text_font_size_disabled", 8)
        
        self.text_font_facename_default  = kwargs.get("text_font_facename_default",  "Verdana")
        self.text_font_facename_pressed  = kwargs.get("text_font_facename_pressed",  "Verdana")
        self.text_font_facename_hover    = kwargs.get("text_font_facename_hover",    "Verdana")
        self.text_font_facename_disabled = kwargs.get("text_font_facename_disabled", "Verdana")

        self.text_foreground_colour_default  = kwargs.get("text_foreground_colour_default",  (0, 0, 0))
        self.text_foreground_colour_pressed  = kwargs.get("text_foreground_colour_pressed",  (0, 0, 0))
        self.text_foreground_colour_hover    = kwargs.get("text_foreground_colour_hover",    (0, 0, 0))
        self.text_foreground_colour_disabled = kwargs.get("text_foreground_colour_disabled", (0, 0, 0))

        # -------------------- background -------------------- #

        self.background_colour_default  = kwargs.get("background_colour_default",  (255, 255, 255))
        self.background_colour_pressed  = kwargs.get("background_colour_pressed",  (255, 255, 255))
        self.background_colour_hover    = kwargs.get("background_colour_hover",    (255, 255, 255))
        self.background_colour_disabled = kwargs.get("background_colour_disabled", (255, 255, 255))

        self.foreground_colour_default  = kwargs.get("foreground_colour_default",  (255, 255, 255))
        self.foreground_colour_pressed  = kwargs.get("foreground_colour_pressed",  (255, 255, 255))
        self.foreground_colour_hover    = kwargs.get("foreground_colour_hover",    (255, 255, 255))
        self.foreground_colour_disabled = kwargs.get("foreground_colour_disabled", (255, 255, 255))

        # --------------------- gradients --------------------- #

        self.background_linear_gradient_default  = kwargs.get("background_linear_gradient_default",  None)
        self.background_linear_gradient_pressed  = kwargs.get("background_linear_gradient_pressed",  None)
        self.background_linear_gradient_hover    = kwargs.get("background_linear_gradient_hover",    None)
        self.background_linear_gradient_disabled = kwargs.get("background_linear_gradient_disabled", None)

        self.foreground_linear_gradient_default  = kwargs.get("foreground_linear_gradient_default",  None)
        self.foreground_linear_gradient_pressed  = kwargs.get("foreground_linear_gradient_pressed",  None)
        self.foreground_linear_gradient_hover    = kwargs.get("foreground_linear_gradient_hover",    None)
        self.foreground_linear_gradient_disabled = kwargs.get("foreground_linear_gradient_disabled", None)

        # ---------------------- borders ---------------------- #

        self.border_colour_default  = kwargs.get("border_colour_default",  (0, 0, 0))
        self.border_colour_pressed  = kwargs.get("border_colour_pressed",  (0, 0, 0))
        self.border_colour_hover    = kwargs.get("border_colour_hover",    (0, 0, 0))
        self.border_colour_disabled = kwargs.get("border_colour_disabled", (0, 0, 0))

        self.border_width_default  = kwargs.get("border_width_default",  0)
        self.border_width_pressed  = kwargs.get("border_width_pressed",  0)
        self.border_width_hover    = kwargs.get("border_width_hover",    0)
        self.border_width_disabled = kwargs.get("border_width_disabled", 0)

        # ---------------------- corners ---------------------- #

        self.corner_radius_default  = kwargs.get("corner_radius_default",  0)
        self.corner_radius_pressed  = kwargs.get("corner_radius_pressed",  0)
        self.corner_radius_hover    = kwargs.get("corner_radius_hover",    0)
        self.corner_radius_disabled = kwargs.get("corner_radius_disabled", 0)

        # ---------------------- images ---------------------- #

        self.image_default  = kwargs.get("image_default",  None)
        self.image_pressed  = kwargs.get("image_pressed",  None)
        self.image_hover    = kwargs.get("image_hover",    None)
        self.image_disabled = kwargs.get("image_disabled", None)

        self.image_channels_default  = kwargs.get("image_channels_default",  (1.0, 1.0, 1.0, 1.0))
        self.image_channels_pressed  = kwargs.get("image_channels_pressed",  (1.0, 1.0, 1.0, 1.0))
        self.image_channels_hover    = kwargs.get("image_channels_hover",    (1.0, 1.0, 1.0, 1.0))
        self.image_channels_disabled = kwargs.get("image_channels_disabled", (1.0, 1.0, 1.0, 1.0))

        self.image_size_default  = kwargs.get("image_size_default",  (0, 0))
        self.image_size_pressed  = kwargs.get("image_size_pressed",  (0, 0))
        self.image_size_hover    = kwargs.get("image_size_hover",    (0, 0))
        self.image_size_disabled = kwargs.get("image_size_disabled", (0, 0))

        self.image_text_separation = kwargs.get("image_text_separation", None)
        self.image_text_side       = kwargs.get("image_text_side", "right")

        self.image_use_max_dimensions = kwargs.get("image_use_max_dimensions", True)

        # ---------------- checkbox and switch ---------------- #

        self.checkbox_width  = kwargs.get("checkbox_width",  None)
        self.checkbox_height = kwargs.get("checkbox_height", None)

        self.checkbox_active_deflate = kwargs.get("checkbox_active_deflate", 5)
        
        self.checkbox_text_separation = kwargs.get("checkbox_text_separation", 5)
        self.checkbox_text_side       = kwargs.get("checkbox_text_side", "right")

        self.background_colour_active_default  = kwargs.get("background_colour_active_default",  (0, 0, 255))
        self.background_colour_active_pressed  = kwargs.get("background_colour_active_pressed",  (0, 0, 255))
        self.background_colour_active_hover    = kwargs.get("background_colour_active_hover",    (0, 0, 255))
        self.background_colour_active_disabled = kwargs.get("background_colour_active_disabled", (0, 0, 255))

        self.foreground_colour_active_default  = kwargs.get("foreground_colour_active_default",  (0, 0, 255))
        self.foreground_colour_active_pressed  = kwargs.get("foreground_colour_active_pressed",  (0, 0, 255))
        self.foreground_colour_active_hover    = kwargs.get("foreground_colour_active_hover",    (0, 0, 255))
        self.foreground_colour_active_disabled = kwargs.get("foreground_colour_active_disabled", (0, 0, 255))

        self.switch_appearance = kwargs.get("switch_appearance", False)
        self.switch_rounded    = kwargs.get("switch_rounded",    False)
        self.switch_width      = kwargs.get("switch_width",      None)
        self.switch_height     = kwargs.get("switch_height",     None)
        self.switch_radius     = kwargs.get("switch_radius",     0)
        
        self.switch_selector_padding       = kwargs.get("switch_selector_padding",       0)
        self.switch_selector_border_colour = kwargs.get("switch_selector_border_colour", (150, 150, 150))
        self.switch_selector_border_width  = kwargs.get("switch_selector_border_width",  0)

        # -------------------- radiobutton -------------------- #

        self.radiobutton_diameter = kwargs.get("radiobutton_diameter", 0)

        # ---------------------- combobox ------------------------ #

        self.arrow_width  = kwargs.get("arrow_width",  None)
        self.arrow_height = kwargs.get("arrow_height", None)
        self.arrow_colour = kwargs.get("arrow_colour", None)
        self.arrow_text_separation = kwargs.get("arrow_text_separation", None)
        self.arrow_text_side       = kwargs.get("arrow_text_side", "right")

        # ---------------------- scrollbar ------------------------ #

        self.scrollX = kwargs.get("scrollX", True)
        self.scrollY = kwargs.get("scrollY", True)
        self.scrollUnitsX = kwargs.get("scrollUnitsX", 15)
        self.scrollUnitsY = kwargs.get("scrollUnitsY", 15)
        self.scrollbar_type = kwargs.get("scrollbar_type", "rectangular")
        self.scrollbar_width = kwargs.get("scrollbar_width", None)
        self.scrollbar_padding = kwargs.get("scrollbar_padding", None)

        # ----------------------- other ----------------------- #

        self.padding_all_sides = kwargs.get("padding_all_sides", None)

        # ----------- warn user if wrong arguments ----------- #

        self.__CheckWrongArguments(kwargs)


    def __CheckWrongArguments(self, kwargs:dict):
        # checks if the user entered a wrong argument
        attributes = self.__dict__.keys()
        for key in kwargs.keys():
            if key not in attributes:
                print(f"CustomConfig::Key \"{key}\" not in attributes.")

        
    def Update(self, **kwargs):
        """Updates existing attributes (or creates them if
        non-existent)."""
        for key, value in kwargs.items():
            setattr(self, key, value)

        

        
