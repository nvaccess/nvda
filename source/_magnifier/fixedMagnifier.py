# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Fixed magnifier module.
"""

from .magnifier import Magnifier
from .utils.types import Coordinates, MagnifierType, MagnifierParameters
from .utils.windowCreator import WindowCreator

import wx


class FixedMagnifier(Magnifier):
	def __init__(self):
		super().__init__()
		self._magnifierType = MagnifierType.FIXED
		self._currentCoordinates = Coordinates(0, 0)
		self._window: None | wx.Frame = None
		self.params = MagnifierParameters(
			magnifierWidth=300,
			magnifierHeight=300,
			coordinates=(0, 0),
			styles=wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR,
		)

	def _startMagnifier(self) -> None:
		super()._startMagnifier()
		self._window = WindowCreator.createMagnifierWindow(
			parent=None,
			title="Fixed Magnifier",
			frameType="fixedMagnifier",
			screenSize=self._displayOrientation,
			magnifierParameters=self.params,
		)

	def _stopMagnifier(self) -> None:
		self._window.Destroy()
		super()._stopMagnifier()

	def _doUpdate(self):
		self._window.Refresh()
