# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import ctypes
from ctypes import wintypes
from logHandler import log
from .magnifier import NVDAMagnifier


class FullScreenMagnifier(NVDAMagnifier):
	def __init__(
		self,
		zoomLevel: float = 2.0,
	):
		super().__init__(zoomLevel=zoomLevel)
		self._currentCoordinates: tuple[int, int] = (0, 0)
		self._startMagnifier()

	@property
	def currentCoordinates(self) -> tuple[int, int]:
		return self._currentCoordinates

	@currentCoordinates.setter
	def currentCoordinates(self, value: tuple[int, int]) -> None:
		self._currentCoordinates = value

	def _startMagnifier(self) -> None:
		"""Start the Fullscreen magnifier using windows DLL."""
		super()._startMagnifier()
		self._loadMagnifierApi()
		self._startTimer(self._updateMagnifier)

	def _doUpdate(self):
		"""Perform the actual update of the magnifier."""
		# Calculate new position based on focus mode
		x, y = self._getCoordinatesForMode(self.currentCoordinates)
		# Always save screen position for mode continuity
		self.lastScreenPosition = (x, y)
		# Apply transformation
		self._fullscreenMagnifier(x, y)

	def _stopMagnifier(self) -> None:
		"""Stop the Fullscreen magnifier using windows DLL."""
		super()._stopMagnifier()
		try:
			# Get MagSetFullscreenTransform function from magnification API
			MagSetFullscreenTransform = self._getMagnificationApi()
			# Reset fullscreen magnifier: 1.0 zoom, 0,0 position
			MagSetFullscreenTransform(ctypes.c_float(1.0), ctypes.c_int(0), ctypes.c_int(0))
		except AttributeError:
			log.info("Magnification API not available")
		self._stopMagnifierApi()

	def _loadMagnifierApi(self) -> None:
		"""Initialize the Magnification API."""
		try:
			# Attempt to access the magnification DLL
			ctypes.windll.magnification
		except Exception as e:
			# If the DLL is not available, log this and exit the function
			log.error(f"Magnification API not available with error {e}")
			return
		# Try to initialize the magnification API
		# MagInitialize returns 0 if already initialized or on failure
		if ctypes.windll.magnification.MagInitialize() == 0:
			log.info("Magnification API already initialized")
			return
		# If initialization succeeded, log success
		log.info("Magnification API initialized")

	def _stopMagnifierApi(self) -> None:
		"""Stop the Magnification API."""
		try:
			ctypes.windll.magnification
		except Exception as e:
			log.error(f"Magnification API not available with error {e}")
			return
		if ctypes.windll.magnification.MagUninitialize() == 0:
			log.info("Magnification API already uninitialized")
			return
		log.info("Magnification API uninitialized")

	def _getMagnificationApi(self):
		"""Get Windows Magnification API function."""
		MagSetFullscreenTransform = ctypes.windll.magnification.MagSetFullscreenTransform
		MagSetFullscreenTransform.restype = wintypes.BOOL
		MagSetFullscreenTransform.argtypes = [ctypes.c_float, ctypes.c_int, ctypes.c_int]
		return MagSetFullscreenTransform

	def _fullscreenMagnifier(self, x: int, y: int) -> None:
		"""Apply fullscreen magnification at given coordinates.

		:param x: The x-coordinate for the magnifier.
		:param y: The y-coordinate for the magnifier.
		"""
		left, top, visibleWidth, visibleHeight = self._getMagnifierPosition(x, y)
		try:
			MagSetFullscreenTransform = self._getMagnificationApi()
			result = MagSetFullscreenTransform(
				ctypes.c_float(self.zoomLevel), ctypes.c_int(left), ctypes.c_int(top)
			)
			if not result:
				log.info("Failed to set fullscreen transform")
		except AttributeError:
			log.info("Magnification API not available")

	def _getCoordinatesForMode(self, coordinates: tuple[int, int]) -> tuple[int, int]:
		"""Get coordinates adjusted for the current fullscreen mode.

		:param coordinates: Raw coordinates (x, y)

		Returns:
			Adjusted coordinates according to fullscreen mode
		"""
		return coordinates
