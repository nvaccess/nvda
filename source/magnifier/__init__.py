# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
NVDA Magnifier module.
Handles module initialization, configuration and settings interaction.
"""

import config

from .fullscreenMagnifier import FullScreenMagnifier

# Variables globales du module
_magnifier: FullScreenMagnifier | None = None

# Configuration specification
confspec = {
    "magnifier": {
        "defaultZoomLevel": "float(min=1.0, max=10.0, default=2.0)",
    }
}

def initialize():
    """Initialize the magnifier module."""
    # Add config specification
    config.conf.spec.update(confspec)

def getDefaultZoomLevel():
    """Get default zoom level from config."""
    try:
        zoomLevel = config.conf["magnifier"]["defaultZoomLevel"]
        # Ensure it's a float
        return float(zoomLevel)
    except (KeyError, ValueError, TypeError):
        return 2.0

def getCurrentZoomLevel():
    """Get current zoom level for settings."""
    global _magnifier
    if _magnifier and _magnifier.isActive:
        return float(_magnifier.zoomLevel)  # Ensure float
    return getDefaultZoomLevel()

def setDefaultZoomLevel(zoomLevel: float):
    """Set default zoom level from settings."""
    # Validate zoom level and ensure it's a float
    try:
        zoomLevel = float(zoomLevel)
        zoomLevel = max(1.0, min(10.0, zoomLevel))
    except (ValueError, TypeError):
        zoomLevel = 2.0
    
    # Ensure config section exists
    if "magnifier" not in config.conf:
        config.conf["magnifier"] = {}
    
    # Save to config as float
    config.conf["magnifier"]["defaultZoomLevel"] = zoomLevel

def isActive():
    """Check if magnifier is currently active for settings."""
    global _magnifier
    return _magnifier is not None and _magnifier.isActive

def getMagnifier():
    """Get current magnifier"""
    global _magnifier
    return _magnifier

def setMagnifier(magnifier: FullScreenMagnifier | None):
    """Set magnifier instance"""
    global _magnifier
    _magnifier = magnifier

def terminate():
    """Called when NVDA shuts down."""
    global _magnifier
    if _magnifier and _magnifier.isActive:
        _magnifier._stopMagnifier()
        _magnifier = None
    
    # Clean up the API
    from .fullscreenMagnifier import cleanup
    cleanup()
