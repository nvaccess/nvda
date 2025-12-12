# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
NVDA Magnifier module
Handles module initialization, configuration and settings interaction
"""

_magnifier = None


def initialize():
	"""
	Initialize the magnifier module
	This is kept for compatibility but config is now initialized on import
	"""
	from .fullscreenMagnifier import FullScreenMagnifier

	magnifier = FullScreenMagnifier()
	setMagnifier(magnifier)


def isActive() -> bool:
	"""
	Check if magnifier is currently active for settings
	"""
	global _magnifier
	return _magnifier and _magnifier.isActive


def getMagnifier():
	"""
	Get current magnifier
	"""
	global _magnifier
	return _magnifier


def setMagnifier(magnifier):
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
