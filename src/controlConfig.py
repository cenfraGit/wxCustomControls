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
        self.bg_active = kwargs.get("bg_active", (0, 100, 255))

        self.checkbox_width = kwargs.get("checkbox_width", None)
        self.checkbox_height = kwargs.get("checkbox_height", None)
        self.checkbox_active_deflate = kwargs.get("checkbox_active_deflate", None)
        self.checkbox_text_separation = kwargs.get("checkbox_text_separation", None)

        # scrollbar
        self.scrollbar_type = kwargs.get("scrollbar_type", "rounded")
        self.scrollbar_width = kwargs.get("scrollbar_width", None)
        self.scrollbar_padding = kwargs.get("scrollbar_padding", None)

        # foreground colour (scrollbar)
        self.fg_colour = kwargs.get("fg_colour", (0, 0, 0))
        self.fg_colour_hover = kwargs.get("fg_colour_hover", (0, 0, 0))
        self.fg_colour_pressed = kwargs.get("fg_colour_pressed", (0, 0, 0))

        self.scrollX = kwargs.get("scrollX", True)
        self.scrollY = kwargs.get("scrollY", True)
        self.scrollUnitsX = kwargs.get("scrollUnitsX", 15)
        self.scrollUnitsY = kwargs.get("scrollUnitsY", 15)
        
        
        

        
    def update(self, **kwargs):
        """Updates existing attributes or creates them if they don't
        exist."""
        for key, value in kwargs.items():
            setattr(self, key, value)
