# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import ctypes
from ctypes import wintypes
from logHandler import log
from enum import Enum
from .magnifier import Magnifier
from .utils.filterHandler import filter, filterMatrix

class FullScreenMode(Enum):
	CENTER = "center"
	BORDER = "border"
	RELATIVE = "relative"

class FullScreenMagnifier(Magnifier):
	def __init__(
		self,
		zoomLevel: float = 2.0,
		fullscreenMode: FullScreenMode = FullScreenMode.CENTER,
		filter: filter = filter.NORMAL,
	):
		super().__init__(zoomLevel=zoomLevel, filter = filter)
		self._fullscreenMode = fullscreenMode
		self._currentCoordinates: tuple[int, int] = (0, 0)
		self._startMagnifier()
		self._applyFilter()

	@property
	def fullscreenMode(self) -> FullScreenMode:
		return self._fullscreenMode

	@fullscreenMode.setter
	def fullscreenMode(self, value: FullScreenMode) -> None:
		self._fullscreenMode = value

	@property
	def currentCoordinates(self) -> tuple[int, int]:
		return self._currentCoordinates

	@currentCoordinates.setter
	def currentCoordinates(self, value: tuple[int, int]) -> None:
		self._currentCoordinates = value

	def _startMagnifier(self) -> None:
		"""Start the Fullscreen magnifier using windows DLL."""
		super()._startMagnifier()
		log.info(f"Starting magnifier with zoom level {self.zoomLevel} and filter {self.filter} and fullscreen mode {self.fullscreenMode}")
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

	def _applyFilter(self) -> None:
		"""Apply the current color filter to the fullscreen magnifier."""
		if self.filter == filter.NORMAL:
			ctypes.windll.magnification.MagSetFullscreenColorEffect(filterMatrix.NORMAL.value)
		elif self.filter == filter.GREYSCALE:
			ctypes.windll.magnification.MagSetFullscreenColorEffect(filterMatrix.GREYSCALE.value)
		elif self.filter == filter.INVERTED:
			ctypes.windll.magnification.MagSetFullscreenColorEffect(filterMatrix.INVERTED.value)
		else:
			log.info(f"Unknown color filter: {self.filter}")


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

		Args:
			coordinates: Raw coordinates (x, y)

		Returns:
			Adjusted coordinates according to fullscreen mode
		"""
		x, y = coordinates

		if self._fullscreenMode == FullScreenMode.RELATIVE:
			return self._relativePos(x, y)
		elif self._fullscreenMode == FullScreenMode.BORDER:
			# For border mode, use the current position as reference
			return self._borderPos(x, y)
		else:  # CENTER mode
			return coordinates

	def _borderPos(self, focusX: int, focusY: int) -> tuple[int, int]:
		"""
		Check if focus is near magnifier border and adjust position accordingly.
		Returns adjusted position to keep focus within margin limits.

		Args:
			focusX (int): The x-coordinate of the focus point.
			focusY (int): The y-coordinate of the focus point.

		Returns:
			lastScreenPosition (tuple[int, int]): The adjusted position (x, y) of the focus point.
		"""

		lastLeft, lastTop, visibleWidth, visibleHeight = self._getMagnifierPosition(
			self.lastScreenPosition[0], self.lastScreenPosition[1]
		)

		minX = lastLeft + self._MARGIN_BORDER
		maxX = lastLeft + visibleWidth - self._MARGIN_BORDER
		minY = lastTop + self._MARGIN_BORDER
		maxY = lastTop + visibleHeight - self._MARGIN_BORDER

		dx = 0
		dy = 0

		if focusX < minX:
			dx = focusX - minX
		elif focusX > maxX:
			dx = focusX - maxX

		if focusY < minY:
			dy = focusY - minY
		elif focusY > maxY:
			dy = focusY - maxY

		if dx != 0 or dy != 0:
			return self.lastScreenPosition[0] + dx, self.lastScreenPosition[1] + dy
		else:
			return self.lastScreenPosition

	def _relativePos(self, mouseX: int, mouseY: int) -> tuple[int, int]:
		"""
		Calculate magnifier center maintaining mouse relative position.
		Handles screen edges to prevent going off-screen.

		Args:
			mouseX (int): The x-coordinate of the mouse pointer.
			mouseY (int): The y-coordinate of the mouse pointer.

		Returns:
			tuple[int, int]: The (x, y) coordinates of the magnifier center.
		"""
		zoom = self.zoomLevel

		screenWidth = self._SCREEN_WIDTH
		screenHeight = self._SCREEN_HEIGHT
		visibleWidth = screenWidth / zoom
		visibleHeight = screenHeight / zoom
		margin = int(zoom * 10)

		# Calculate left/top maintaining mouse relative position
		left = mouseX - (mouseX / screenWidth) * (visibleWidth - margin)
		top = mouseY - (mouseY / screenHeight) * (visibleHeight - margin)

		# Clamp to screen boundaries
		left = max(0, min(left, screenWidth - visibleWidth))
		top = max(0, min(top, screenHeight - visibleHeight))

		# Return center of zoom window
		centerX = int(left + visibleWidth / 2)
		centerY = int(top + visibleHeight / 2)
		self.lastScreenPosition = (centerX, centerY)
		return self.lastScreenPosition
