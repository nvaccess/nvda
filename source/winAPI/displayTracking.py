# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
Tracking was introduced so that NVDA has a mechanism to announce changes to the device orientation.

When the display resolution changes, the new height and width is sent to NVDA,
and we notify the user of changes to the orientation.
"""

from dataclasses import dataclass
import enum

import ui
import winUser


class Orientation(enum.Enum):
	NOT_INITIALIZED = enum.auto()
	PORTRAIT = enum.auto()
	LANDSCAPE = enum.auto()


@dataclass
class OrientationState:
	width: int = 0
	height: int = 0
	style: Orientation = Orientation.NOT_INITIALIZED


_orientationState = OrientationState()


def reportScreenOrientationChange(heightWidth: int) -> None:
	"""
	Reports the screen orientation only if the screen orientation has changed.
	"""
	# Resolution detection comes from an article found at https://msdn.microsoft.com/en-us/library/ms812142.aspx.
	width = winUser.LOWORD(heightWidth)
	height = winUser.HIWORD(heightWidth)
	if width > height:
		# The new orientation is landscape
		if (
			# Orientation has changed
			_orientationState.style != Orientation.LANDSCAPE
			# If the height and width are the same, it's a screen flip
			or (_orientationState.height == height and _orientationState.width == width)
		):
			# Translators: The screen is oriented so that it is wider than it is tall.
			ui.message(_("Landscape"))
			_orientationState.style = Orientation.LANDSCAPE
	else:
		# The new orientation is portrait
		if (
			# Orientation has changed
			_orientationState.style != Orientation.PORTRAIT
			# If the height and width are the same, it's a screen flip
			or (_orientationState.height == height and _orientationState.width == width)
		):
			# Translators: The screen is oriented in such a way that the height is taller than it is wide.
			ui.message(_("Portrait"))
			_orientationState.style = Orientation.PORTRAIT

	_orientationState.height = height
	_orientationState.width = width
