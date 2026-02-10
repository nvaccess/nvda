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
)
from .utils.windowCreator import WindowedMagnifier

import wx


class FixedMagnifier(Magnifier, WindowedMagnifier):
	def __init__(self):
		windowParameters = WindowMagnifierParameters(
			title="NVDA Fixed Magnifier",
			windowSize=Size(300, 300),
			windowPosition=Coordinates(0, 0),
			styles=wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP,
		)
		Magnifier.__init__(self)
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
		if self._isActive:
			self._applyFilter()

	def event_gainFocus(
		self,
		obj,
		nextHandler,
	):
		log.debug("Full-screen Magnifier gain focus event")
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
