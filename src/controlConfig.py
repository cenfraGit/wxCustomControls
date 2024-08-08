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
        self.text_foreground_colour = kwargs.get("text_foreground_colour", ())
        self.text_foreground_colour_hover = kwargs.get("text_foreground_colour_hover", ())
        self.text_foreground_colour_pressed = kwargs.get("text_foreground_colour_pressed", ())
        self.text_foreground_colour_disabled = kwargs.get("text_foreground_colour_disabled", ())
        
        # background colours
        self.bg_colour = kwargs.get("bg_colour", ())
        self.bg_colour_hover = kwargs.get("bg_colour_hover", ())
        self.bg_colour_pressed = kwargs.get("bg_colour_pressed", ())
        self.bg_colour_disabled = kwargs.get("bg_colour_disabled", ())

        # border colours
        self.border_colour = kwargs.get("border_colour", ())
        self.border_colour_hover = kwargs.get("border_colour_hover", ())
        self.border_colour_pressed = kwargs.get("border_colour_pressed", ())
        self.border_colour_disabled = kwargs.get("border_colour_disabled", ())

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
        self.linear_gradient_behind = kwargs.get("linear_gradient_behind", None)

        # corners
        self.corner_radius = kwargs.get("corner_radius", 0)
        self.corner_radius_hover = kwargs.get("corner_radius_hover", 0)
        self.corner_radius_pressed = kwargs.get("corner_radius_pressed", 0)
        self.corner_radius_disabled = kwargs.get("corner_radius_disabled", 0)

        
    def update(self, **kwargs):
        """Updates existing attributes or creates them if they don't
        exist."""
        for key, value in kwargs.items():
            setattr(self, key, value)
