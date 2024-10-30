# controlConfig.py
# wxCustomControls
# Class for handling control appearance configuration. Sets default
# valuesif not specified as keyword arguments.
# 28/oct/2024


class CustomConfig:
    def __init__(self, **kwargs):

        # ----------------------- text ----------------------- #

        self.text_font_size = kwargs.get("text_font_size", 8)
        self.text_font_face_name = kwargs.get("text_font_face_name", "Verdana")
        self.text_foreground_colour_default = kwargs.get("text_foreground_colour_default", (0, 0, 0))
        self.text_foreground_colour_pressed = kwargs.get("text_foreground_colour_pressed", (0, 0, 0))
        self.text_foreground_colour_hover = kwargs.get("text_foreground_colour_hover", (0, 0, 0))
        self.text_foreground_colour_disabled = kwargs.get("text_foreground_colour_disabled", (0, 0, 0))
        self.text_side = kwargs.get("text_side", "right") # when using images

        # -------------------- background -------------------- #

        self.background_colour_default = kwargs.get("background_colour_default", (150, 150, 150))
        self.background_colour_pressed = kwargs.get("background_colour_pressed", (150, 150, 150))
        self.background_colour_hover = kwargs.get("background_colour_hover", (150, 150, 150))
        self.background_colour_disabled = kwargs.get("background_colour_disabled", (150, 150, 150))

        # --------------------- gradients --------------------- #

        self.background_linear_gradient_default = kwargs.get("background_linear_gradient_default", None)
        self.background_linear_gradient_pressed = kwargs.get("background_linear_gradient_pressed", None)
        self.background_linear_gradient_hover = kwargs.get("background_linear_gradient_hover", None)
        self.background_linear_gradient_disabled = kwargs.get("background_linear_gradient_disabled", None)

        # ---------------------- borders ---------------------- #

        self.border_colour_default = kwargs.get("border_colour_default", (0, 0, 0))
        self.border_colour_pressed = kwargs.get("border_colour_pressed", (0, 0, 0))
        self.border_colour_hover = kwargs.get("border_colour_hover", (0, 0, 0))
        self.border_colour_disabled = kwargs.get("border_colour_disabled", (0, 0, 0))

        self.border_width_default = kwargs.get("border_width_default", 0)
        self.border_width_pressed = kwargs.get("border_width_pressed", 0)
        self.border_width_hover = kwargs.get("border_width_hover", 0)
        self.border_width_disabled = kwargs.get("border_width_disabled", 0)

        # ---------------------- corners ---------------------- #

        self.corner_radius_default = kwargs.get("corner_radius_default", 0)
        self.corner_radius_pressed = kwargs.get("corner_radius_pressed", 0)
        self.corner_radius_hover = kwargs.get("corner_radius_hover", 0)
        self.corner_radius_disabled = kwargs.get("corner_radius_disabled", 0)

        

    def Update(self, **kwargs):
        """Updates existing attributes (or creates them if
        non-existent)."""
        for key, value in kwargs.items():
            setattr(self, key, value)

        

        
