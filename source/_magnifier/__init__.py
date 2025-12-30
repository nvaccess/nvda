# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
NVDA Magnifier module.
Handles module initialization, configuration and settings interaction.
"""

from typing import TYPE_CHECKING
from .fullscreenMagnifier import FullScreenMagnifier

if TYPE_CHECKING:
	from .magnifier import Magnifier

_magnifier: "Magnifier | None" = None


def initialize():
	"""
	Initialize the magnifier module
	For now, only the full-screen magnifier is supported
	"""

	magnifier = FullScreenMagnifier()
	setMagnifier(magnifier)


def getDisplaySize() -> tuple[int, int]:
	"""
	Get the primary display size

	:returns: A tuple (width, height) representing the display size
	"""
	from winAPI._displayTracking import getPrimaryDisplayOrientation

	display = getPrimaryDisplayOrientation()
	return display.width, display.height


def isActive() -> bool:
	"""
	Check if magnifier is currently active for settings
	"""
	global _magnifier
	return _magnifier and _magnifier.isActive


def getMagnifier() -> "Magnifier | None":
	"""
	Get current magnifier
	"""
	global _magnifier
	return _magnifier


def setMagnifier(magnifier: "Magnifier") -> None:
	"""
	Set magnifier instance

	:param magnifier: The magnifier instance to set
	"""
	global _magnifier
	_magnifier = magnifier


def terminate():
	"""
	Called when NVDA shuts down
	"""
	global _magnifier
	if _magnifier and _magnifier.isActive:
		_magnifier._stopMagnifier()
		_magnifier = None
