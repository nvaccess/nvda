# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022–2024 NV Access Limited, Bill Dengler
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
Tracking was introduced so that NVDA has a mechanism to announce changes to the device orientation.

When the display resolution changes, the new height and width is sent to NVDA,
and we notify the user of changes to the orientation.
"""

from ctypes import windll
from dataclasses import dataclass
import enum
from typing import (
	Optional,
)

from logHandler import log
import ui
import winUser

from .winUser.constants import SystemMetrics


class Orientation(enum.Enum):
	PORTRAIT = enum.auto()
	LANDSCAPE = enum.auto()


@dataclass
class OrientationState:
	width: int
	height: int
	style: Orientation


_orientationState: Optional[OrientationState] = None


def initialize():
	"""
	The NVDA message window only handles changes of state.
	As such, to correctly ignore an initial display change event,
	which does not change the orientation style (e.g. monitor change),
	we fetch the primary display orientation manually.
	"""
	global _orientationState
	_orientationState = getPrimaryDisplayOrientation()


def getPrimaryDisplayOrientation() -> OrientationState:
	width = windll.user32.GetSystemMetrics(SystemMetrics.CX_SCREEN)
	if width == 0:
		# If the function fails, the return value is 0.
		# GetLastError does not provide extended error information.
		log.error("Failed to get primary display width")
	height = windll.user32.GetSystemMetrics(SystemMetrics.CY_SCREEN)
	if height == 0:
		# If the function fails, the return value is 0.
		# GetLastError does not provide extended error information.
		log.error("Failed to get primary display height")
	return OrientationState(
		width,
		height,
		_getOrientationStyle(width=width, height=height)
	)


def _getOrientationStyle(height: int, width: int) -> Orientation:
	return Orientation.LANDSCAPE if width > height else Orientation.PORTRAIT


def _getNewOrientationStyle(
		previousState: OrientationState,
		height: int,
		width: int,
) -> Optional[Orientation]:
	"""
	@returns: Orientation if there has been an orientation state change, otherwise None
	"""
	heightAndWidthUnchanged = previousState.height == height and previousState.width == width
	newOrientation = _getOrientationStyle(height, width)
	if (
		# Orientation has changed
		previousState.style != newOrientation
		# If the height and width are the same, it's a screen flip
		# and the orientation state has changed.
		# Otherwise, it may be a change of display (e.g. monitor disconnected).
		or heightAndWidthUnchanged
	):
		return newOrientation
	return None


def reportScreenOrientationChange(heightWidth: int) -> None:
	"""
	Reports the screen orientation only if the screen orientation has changed.
	"""
	# Resolution detection comes from an article found at
	# https://msdn.microsoft.com/en-us/library/ms812142.aspx.
	height = winUser.HIWORD(heightWidth)
	width = winUser.LOWORD(heightWidth)
	newState = _getNewOrientationStyle(_orientationState, height, width)
	if newState:
		_orientationState.style = newState
		if _orientationState.style == Orientation.LANDSCAPE:
			# Translators: The screen is oriented so that it is wider than it is tall.
			ui.message(_("Landscape"))
		if _orientationState.style == Orientation.PORTRAIT:
			# Translators: The screen is oriented in such a way that the height is taller than it is wide.
			ui.message(_("Portrait"))

	_orientationState.height = height
	_orientationState.width = width
