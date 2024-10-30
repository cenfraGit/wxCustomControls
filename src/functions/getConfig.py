# getConfig.py
# wxCustomControls
# Returns the CustomConfig for the control.
# 28/oct/2024


from copy import copy
from ..CustomConfig import CustomConfig
from .getDefaultConfig import getDefaultConfig


def getConfig(config, control_type:str) -> CustomConfig:
    if config:
        # copy the CustomConfig instead of referencing it
        return copy(config)
    else:
        # get default CustomConfig for the control type
        return getDefaultConfig(control_type)
