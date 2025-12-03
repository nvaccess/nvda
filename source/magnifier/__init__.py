# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
NVDA Magnifier module.
Handles module initialization, configuration and settings interaction.
"""

import config

from .fullscreenMagnifier import FullScreenMagnifier

_magnifier: FullScreenMagnifier | None = None

# Configuration specification
confspec = {
    "magnifier": {
        "defaultZoomLevel": "float(min=1.0, max=10.0, default=2.0)",
        "defaultFullscreenMode": "string(default='center')",
        "defaultFilter": "string(default='normal')",
        "keepMouseCentered": "boolean(default=False)",
        "saveShortcutChanges": "boolean(default=False)",
    }
}

# Initialize configuration automatically on import
config.conf.spec.update(confspec)


def initialize():
    """
    Initialize the magnifier module.
    This is kept for compatibility but config is now initialized on import.
    """
    pass


def isActive() -> bool:
    """
    Check if magnifier is currently active for settings.
    """
    global _magnifier
    return _magnifier is not None and _magnifier.isActive


# Fullscreen magnifier instance while there is no other magnifier types
def getMagnifier() -> FullScreenMagnifier | None:
    """
    Get current magnifier
    """
    global _magnifier
    return _magnifier


def setMagnifier(magnifier: FullScreenMagnifier | None):
    """
    Set magnifier instance

    :param magnifier: The magnifier instance to set.
    """
    global _magnifier
    _magnifier = magnifier


def terminate():
    """
    Called when NVDA shuts down.
    """
    global _magnifier
    if _magnifier and _magnifier.isActive:
        _magnifier._stopMagnifier()
        _magnifier = None
