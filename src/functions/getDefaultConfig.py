# getDefaultConfig.py
# wxCustomControls
# Function that returns default configurations for controls.
# 28/oct/2024


from ..utils.dip import dip
from ..CustomConfig import CustomConfig


def getDefaultConfig(control_type:str) -> CustomConfig:
    """Returns the default configuration for the specified control."""
    
    configurations = {
        "CustomPanel": {
            "background_colour_default": (255, 255, 255),
            "border_colour_default": (150, 150, 150),
            "border_width_default": 0,
            "corner_radius_default": 0
            },
        "CustomButton": {
            # background
            "background_colour_default": (240, 240, 240),
            "background_colour_hover": (227, 238, 248),
            "background_colour_pressed": (137, 192, 246),
            "background_colour_disabled": (179, 179, 179),
            # border colour
            "border_colour_default": (200, 200, 200),
            "border_colour_hover": (145, 200, 255),
            "border_colour_pressed": (77, 149, 221),
            # border width
            "border_width_default": dip(1),
            "border_width_hover": dip(1),
            "border_width_pressed": dip(1),
            "border_width_disabled": 0,
            # text foreground
            "text_foreground_colour_default": (20, 20, 20),
            "text_foreground_colour_hover": (20, 20, 20),
            "text_foreground_colour_pressed": (20, 20, 20),
            "text_foreground_colour_disabled": (133, 133, 133),
            
            }
    }

    if control_type not in configurations.keys():
        raise ValueError("GetDefaultConfig::Incorrect control type.")

    # unpack dictionary to create config
    return CustomConfig(**configurations[control_type])

    

    
    
