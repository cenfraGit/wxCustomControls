# getDefaultConfig.py
# wxCustomControls
# Function that returns default configurations for controls.
# 28/oct/2024


from ..utils.dip import dip
from ..CustomConfig import CustomConfig


def getDefaultConfig(object_type:str) -> CustomConfig:
    """Returns the default configuration for the specified control."""
    
    configurations = {
        "CustomPanel": {
            "background_colour_default": (255, 255, 255),
            "border_colour_default": (150, 150, 150),
            "border_width_default": 0,
            "corner_radius_default": 0
            },
        "CustomStaticBox": {
            "background_colour_default": (255, 255, 255),
            "border_colour_default": (200, 200, 200),
            "border_width_default": 1,
            "corner_radius_default": 0,
            "padding_all_sides": dip(8)
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
            },
        "CustomCheckBox": {
            # checkbox options
            "checkbox_width": dip(20),
            "checkbox_height": dip(20),
            # switch options
            "switch_width": dip(50),
            "switch_height": dip(20),
            "switch_radius": dip(4),
            "switch_selector_padding": dip(3),
            "switch_rounded": False,
            # corner radius
            "corner_radius_default": dip(3),
            "corner_radius_pressed": dip(3),
            "corner_radius_hover": dip(3),
            # background colour inactive
            "background_colour_default": (230, 230, 230),
            "background_colour_pressed": (210, 210, 210),
            "background_colour_hover": (220, 220, 220),
            # background colour active
            "background_colour_active_default": (57, 117, 186),
            "background_colour_active_pressed": (44, 91, 143),
            "background_colour_active_hover": (52, 107, 169),
            # border colour
            "border_colour_default": (200, 200, 200),
            "border_colour_pressed": (180, 180, 180),
            "border_colour_hover": (190, 190, 190),
            # border width
            "border_width_default": dip(1),
            "border_width_pressed": dip(1),
            "border_width_hover": dip(1),
            # other
            "image_text_separation": dip(6),
            "text_foreground_colour_default": (20, 20, 20),
        },
        "CustomRadioButton": {
            # circle diameter
            "radiobutton_diameter": dip(20),
            # background colour inactive
            "background_colour_default": (230, 230, 230),
            "background_colour_pressed": (210, 210, 210),
            "background_colour_hover": (220, 220, 220),
            # background colour active
            "background_colour_active_default": (57, 117, 186),
            "background_colour_active_pressed": (44, 91, 143),
            "background_colour_active_hover": (52, 107, 169),
            # border colour
            "border_colour_default": (200, 200, 200),
            "border_colour_pressed": (180, 180, 180),
            "border_colour_hover": (190, 190, 190),
            # border width
            "border_width_default": dip(1),
            "border_width_pressed": dip(1),
            "border_width_hover": dip(1),
            # other
            "image_text_separation": dip(6),
            "text_foreground_colour_default": (20, 20, 20),
        },
        "CustomScrolledWindow": {
            "background_colour_default": (255, 0, 0),
            "background_colour_pressed": (255,0, 0),
            "background_colour_hover": (200,0, 0),
            "foreground_colour_default": (0, 200, 0),
            "foreground_colour_pressed": (0, 180, 0),
            "foreground_colour_hover": (0, 180, 0),

            "scrollbar_width": dip(15),
            "scrollbar_padding": dip(2)
        }

        
    }

    if object_type not in configurations.keys():
        print("GetDefaultConfig::Incorrect control type. Returning base config.")
        return CustomConfig()

    # unpack dictionary to create config
    return CustomConfig(**configurations[object_type])

    

    
    
