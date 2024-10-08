"""
controlConfig.py: Class for handling control appearance configuration.

wxCustomControls
"""

class ControlConfig:
    """This class holds the appearance configuration for the
    controls. Keyword arguments will update the default value for each
    attribute.
    """
    def __init__(self, **kwargs):

        # font
        self.font_size = kwargs.get("font_size", 8)
        self.font_face_name = kwargs.get("font_face_name", "Verdana")

        # text foreground
        self.text_foreground_colour = kwargs.get("text_foreground_colour", (0, 0, 0))
        self.text_foreground_colour_hover = kwargs.get("text_foreground_colour_hover", (0, 0, 0))
        self.text_foreground_colour_pressed = kwargs.get("text_foreground_colour_pressed", (0, 0, 0))
        self.text_foreground_colour_disabled = kwargs.get("text_foreground_colour_disabled", (0, 0, 0))

        self.text_side = kwargs.get("text_side", "right")
        
        # background colours
        self.bg_colour = kwargs.get("bg_colour", (150, 150, 150))
        self.bg_colour_hover = kwargs.get("bg_colour_hover", (150, 150, 150))
        self.bg_colour_pressed = kwargs.get("bg_colour_pressed", (150, 150, 150))
        self.bg_colour_disabled = kwargs.get("bg_colour_disabled", (150, 150, 150))

        # border colours
        self.border_colour = kwargs.get("border_colour", (0, 0, 0))
        self.border_colour_hover = kwargs.get("border_colour_hover", (0, 0, 0))
        self.border_colour_pressed = kwargs.get("border_colour_pressed", (0, 0, 0))
        self.border_colour_disabled = kwargs.get("border_colour_disabled", (0, 0, 0))

        # border widths
        self.border_width = kwargs.get("border_width", 0)
        self.border_width_hover = kwargs.get("border_width_hover", 0)
        self.border_width_pressed = kwargs.get("border_width_pressed", 0)
        self.border_width_disabled = kwargs.get("border_width_disabled", 0)

        # gradients
        self.bg_linear_gradient = kwargs.get("bg_linear_gradient", None)
        self.bg_linear_gradient_hover = kwargs.get("bg_linear_gradient_hover", None)
        self.bg_linear_gradient_pressed = kwargs.get("bg_linear_gradient_pressed", None)
        self.bg_linear_gradient_disabled = kwargs.get("bg_linear_gradient_disabled", None)
        
        self.fg_linear_gradient = kwargs.get("fg_linear_gradient", None)
        self.fg_linear_gradient_hover = kwargs.get("fg_linear_gradient_hover", None)
        self.fg_linear_gradient_pressed = kwargs.get("fg_linear_gradient_pressed", None)

        # corners
        self.corner_radius = kwargs.get("corner_radius", 0)
        self.corner_radius_hover = kwargs.get("corner_radius_hover", 0)
        self.corner_radius_pressed = kwargs.get("corner_radius_pressed", 0)
        self.corner_radius_disabled = kwargs.get("corner_radius_disabled", 0)

        # active colors (for checkbox selection)
        self.bg_active = kwargs.get("bg_active", (0, 0, 255))
        self.bg_active_pressed = kwargs.get("bg_active_pressed", (0, 0, 255))
        self.bg_active_hover = kwargs.get("bg_active_hover", (0, 0, 255))
        self.bg_active_disabled = kwargs.get("bg_active_disabled", (0, 0, 255))

        self.switch_appearance = kwargs.get("switch_appearance", False)
        self.switch_width = kwargs.get("switch_width", None)
        self.switch_height = kwargs.get("switch_height", None)
        self.switch_radius = kwargs.get("switch_radius", 0)
        self.switch_selector_padding = kwargs.get("switch_selector_padding", 0)
        self.switch_selector_border_colour = kwargs.get("switch_selector_border_colour", (150, 150, 150))
        self.switch_selector_border_width = kwargs.get("switch_selector_border_width", 0)
        self.switch_rounded = kwargs.get("switch_rounded", False)

        self.checkbox_width = kwargs.get("checkbox_width", None)
        self.checkbox_height = kwargs.get("checkbox_height", None)
        self.checkbox_active_deflate = kwargs.get("checkbox_active_deflate", None)
        self.checkbox_text_separation = kwargs.get("checkbox_text_separation", None)

        # scrollbar
        self.scrollbar_type = kwargs.get("scrollbar_type", "rectangular")
        self.scrollbar_width = kwargs.get("scrollbar_width", None)
        self.scrollbar_padding = kwargs.get("scrollbar_padding", None)

        # foreground colour (scrollbar)
        self.fg_colour = kwargs.get("fg_colour", (255, 255, 255))
        self.fg_colour_hover = kwargs.get("fg_colour_hover", (255, 255, 255))
        self.fg_colour_pressed = kwargs.get("fg_colour_pressed", (255, 255, 255))
        self.fg_colour_disabled = kwargs.get("fg_colour_disabled", (255, 255, 255))

        self.scrollX = kwargs.get("scrollX", True)
        self.scrollY = kwargs.get("scrollY", True)
        self.scrollUnitsX = kwargs.get("scrollUnitsX", 15)
        self.scrollUnitsY = kwargs.get("scrollUnitsY", 15)

        # images
        self.image_default = kwargs.get("image_default", None)
        self.image_hover = kwargs.get("image_hover", None)
        self.image_pressed = kwargs.get("image_pressed", None)
        self.image_disabled = kwargs.get("image_disabled", None)

        self.image_default_channels = kwargs.get("image_default_channels", (1.0, 1.0, 1.0, 1.0))
        self.image_hover_channels = kwargs.get("image_hover_channels", (1.0, 1.0, 1.0, 1.0))
        self.image_pressed_channels = kwargs.get("image_pressed_channels", (1.0, 1.0, 1.0, 1.0))
        self.image_disabled_channels = kwargs.get("image_disabled_channels", (1.0, 1.0, 1.0, 1.0))

        self.image_default_size = kwargs.get("image_default_size", (0, 0))
        self.image_pressed_size = kwargs.get("image_default_size", (0, 0))
        self.image_hover_size = kwargs.get("image_default_size", (0, 0))
        self.image_disabled_size = kwargs.get("image_default_size", (0, 0))

        self.image_text_separation = kwargs.get("image_text_separation", None)

        
        # self.top_padding = kwargs.get("top_padding", 0)
        # self.bottom_padding = kwargs.get("bottom_padding", 0)
        # self.left_padding = kwargs.get("left_padding", 0)
        # self.right_padding = kwargs.get("right_padding", 0)

        self.padding_all_sides = kwargs.get("padding_all_sides", None)


        # cursors
        self.cursor_pressed = kwargs.get("cursor_pressed", None)
        self.cursor_hover = kwargs.get("cursor_hover", None)
        self.cursor_disabled = kwargs.get("cursor_disabled", None)

        
        
        
        
        
        

        
    def update(self, **kwargs):
        """Updates existing attributes or creates them if they don't
        exist."""
        for key, value in kwargs.items():
            setattr(self, key, value)
