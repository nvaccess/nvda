# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
NVDA Magnifier module.
Handles module initialization, configuration and settings interaction.
"""

from typing import TYPE_CHECKING

from .config import getDefaultMagnifierType
from .utils.types import MagnifierType

if TYPE_CHECKING:
	from .magnifier import Magnifier

_magnifier: "Magnifier | None" = None


def createMagnifier(magnifierType: MagnifierType) -> "Magnifier":
	"""
	Create a magnifier instance based on the specified type.

	:param magnifierType: The type of magnifier to create
	:return: The created magnifier instance
	:raises ValueError: If the magnifier type is not supported
	"""
	match magnifierType:
		case MagnifierType.FULLSCREEN:
			from .fullscreenMagnifier import FullScreenMagnifier

			return FullScreenMagnifier()
		case MagnifierType.FIXED:
			from .fixedMagnifier import FixedMagnifier

			return FixedMagnifier()
		case MagnifierType.DOCKED:
			from .dockedMagnifier import DockedMagnifier

			return DockedMagnifier()
		case MagnifierType.LENS:
			from .lensMagnifier import LensMagnifier

			return LensMagnifier()
		case _:
			raise ValueError(f"Unsupported magnifier type: {magnifierType}")


def _setMagnifierType(magnifierType: MagnifierType) -> None:
	"""
	Set the magnifier type, stopping the current one if active and creating a new instance.

	:param magnifierType: The type of magnifier to set
	"""
	global _magnifier

	# Stop current magnifier if active
	if _magnifier and _magnifier._isActive:
		_magnifier._stopMagnifier()

	# Create and set new magnifier instance
	_magnifier = createMagnifier(magnifierType)


def initialize() -> None:
	"""
	Initialize the magnifier module with the default magnifier type from config.
	"""
	magnifierType = getDefaultMagnifierType()
	_setMagnifierType(magnifierType)
	_magnifier._startMagnifier()


def isActive() -> bool:
	"""
	Check if magnifier is currently active.

	:return: True if magnifier is active, False otherwise
	"""
	global _magnifier
	return _magnifier is not None and _magnifier._isActive


def changeMagnifierType(magnifierType: MagnifierType) -> None:
	"""
	Change the magnifier type at runtime.
	Stops the current magnifier and starts a new one of the specified type.

	:param magnifierType: The new magnifier type to use
	:raises RuntimeError: If no magnifier is currently active
	"""
	global _magnifier
	if not _magnifier or not _magnifier._isActive:
		raise RuntimeError("Cannot change magnifier type: magnifier is not active")

	_setMagnifierType(magnifierType)
	_magnifier._startMagnifier()


def getMagnifier() -> "Magnifier | None":
	"""
	Get current magnifier instance.

	:return: The current magnifier instance or None if not initialized
	"""
	global _magnifier
	return _magnifier


def terminate() -> None:
	"""
	Terminate the magnifier module.
	Called when NVDA shuts down.
	"""
	global _magnifier
	if _magnifier and _magnifier._isActive:
		_magnifier._stopMagnifier()
	_magnifier = None
