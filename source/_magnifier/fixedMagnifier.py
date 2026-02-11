# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Fixed magnifier module.
"""

from logHandler import log
from .magnifier import Magnifier
from .utils.types import (
	Coordinates,
	Size,
	MagnifierType,
	WindowMagnifierParameters,
	Filter,
	FixedWindowPosition,
)
from .utils.windowCreator import WindowedMagnifier
from .config import getDefaultFixedWindowWidth, getDefaultFixedWindowHeight, getDefaultFixedWindowPosition

import wx


class FixedMagnifier(Magnifier, WindowedMagnifier):
	def __init__(self):
		Magnifier.__init__(self)
		windowParameters = self._getWindowParameters()
		WindowedMagnifier.__init__(self, windowParameters)
		self._magnifierType = MagnifierType.FIXED
		self._currentCoordinates = Coordinates(0, 0)
		self._windowParameters = windowParameters

	@property
	def filterType(self) -> Filter:
		return self._filterType

	@filterType.setter
	def filterType(self, value: Filter) -> None:
		self._filterType = value

	def event_gainFocus(
		self,
		obj,
		nextHandler,
	):
		log.debug("Fixed Magnifier gain focus event")
		nextHandler()

	def _startMagnifier(self) -> None:
		"""
		Start the Fixed magnifier by creating a window and starting the update timer.
		"""
		super()._startMagnifier()
		self._startTimer(self._updateMagnifier)
		log.debug(
			f"Starting fixed magnifier position:{self._windowParameters.windowPosition} size:{self._windowParameters.windowSize}\n with zoom level {self.zoomLevel} and filter {self.filterType}",
		)

	def _doUpdate(self):
		params = self._getMagnifierParameters(self._currentCoordinates, self._windowParameters.windowSize)
		super()._setContent(params, self.zoomLevel)

	def _stopMagnifier(self) -> None:
		super()._destroyWindow()
		super()._stopMagnifier()

	def _getWindowParameters(self) -> WindowMagnifierParameters:
		"""
		Get the parameters for the magnifier window from configuration.

		:return: The parameters for the magnifier window
		"""
		case = getDefaultFixedWindowPosition()
		windowSize = Size(getDefaultFixedWindowWidth(), getDefaultFixedWindowHeight())
		displaySize = Size(self._displayOrientation.width, self._displayOrientation.height)
		log.info(
			f"Getting window parameters for fixed magnifier with position {case}, window size {windowSize}",
		)

		match case:
			case FixedWindowPosition.TOP_LEFT:
				position = Coordinates(0, 0)
			case FixedWindowPosition.TOP_RIGHT:
				position = Coordinates(displaySize.width - windowSize.width, 0)
			case FixedWindowPosition.BOTTOM_LEFT:
				position = Coordinates(0, displaySize.height - windowSize.height)
			case FixedWindowPosition.BOTTOM_RIGHT:
				position = Coordinates(
					displaySize.width - windowSize.width,
					displaySize.height - windowSize.height,
				)

		return WindowMagnifierParameters(
			title="NVDA Fixed Magnifier",
			windowSize=windowSize,
			windowPosition=position,
			styles=wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP,
		)
