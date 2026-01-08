# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Full-screen magnifier module.
"""

from logHandler import log
import screenCurtain
import winUser
from winBindings import magnification
from .magnifier import Magnifier
from .utils.filterHandler import FilterMatrix
from .utils.spotlightManager import SpotlightManager
from .utils.types import Filter, Coordinates, FullScreenMode, FocusType
from .config import getDefaultFullscreenMode, shouldKeepMouseCentered


class FullScreenMagnifier(Magnifier):
	def __init__(self):
		super().__init__()
		self._fullscreenMode = getDefaultFullscreenMode()
		self._currentCoordinates = Coordinates(0, 0)
		self._spotlightManager = SpotlightManager(self)
		self._startMagnifier()

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
		Start the Full-screen magnifier using windows DLL
		"""
		# Check if Screen Curtain is active
		if screenCurtain.screenCurtain and screenCurtain.screenCurtain.enabled:
			log.warning("Cannot start magnifier: Screen Curtain is active")
			raise RuntimeError("Screen Curtain is active")

		super()._startMagnifier()
		log.debug(
			f"Starting magnifier with zoom level {self.zoomLevel} and filter {self.filterType} and full-screen mode {self._fullscreenMode}",
		)
		# Initialize Magnification API if not already initialized
		try:
			magnification.MagInitialize()
			log.debug("Magnification API initialized")
		except Exception as e:
			# Already initialized or failed - continue anyway
			log.debug(f"MagInitialize result: {e}")

		if self._isActive:
			self._applyFilter()
		self._startTimer(self._updateMagnifier)

	def _doUpdate(self):
		"""
		Perform the actual update of the magnifier
		"""
		# Calculate new position based on focus mode
		coordinates = self._getCoordinatesForMode(self._currentCoordinates)
		# Always save screen position for mode continuity
		self._lastScreenPosition = coordinates

		if self._lastFocusedObject == FocusType.NVDA:
			if shouldKeepMouseCentered():
				self.moveMouseToScreen()
		self._fullscreenMagnifier(coordinates)

	def _stopMagnifier(self) -> None:
		"""
		Stop the Full-screen magnifier using windows DLL
		"""
		super()._stopMagnifier()
		try:
			# Reset fullscreen magnifier: 1.0 zoom, 0,0 position
			magnification.MagSetFullscreenTransform(1.0, 0, 0)
			# Reset color effect to normal (identity matrix)
			magnification.MagSetFullscreenColorEffect(FilterMatrix.NORMAL.value)
		except Exception as e:
			log.debug(f"Error resetting magnification: {e}")

		# Uninitialize Magnification API
		try:
			magnification.MagUninitialize()
			log.debug("Magnification API uninitialized")
		except Exception as e:
			log.debug(f"MagUninitialize result: {e}")

	def _applyFilter(self) -> None:
		"""
		Apply the current color filter to the full-screen magnifier
		"""
		try:
			match self.filterType:
				case Filter.NORMAL:
					matrix = FilterMatrix.NORMAL
				case Filter.GRAYSCALE:
					matrix = FilterMatrix.GRAYSCALE
				case Filter.INVERTED:
					matrix = FilterMatrix.INVERTED

			magnification.MagSetFullscreenColorEffect(matrix.value)

		except Exception as e:
			log.error(f"Failed to apply filter: {e}")

	def _fullscreenMagnifier(self, coordinates: Coordinates) -> None:
		"""
		Apply full-screen magnification at given Coordinates

		:coordinates: The (x, y) coordinates to center the magnifier on
		"""
		left, top, visibleWidth, visibleHeight = self._getMagnifierPosition(coordinates)
		try:
			result = magnification.MagSetFullscreenTransform(
				self.zoomLevel,
				left,
				top,
			)
			if not result:
				log.debug("Failed to set full-screen transform")
		except AttributeError:
			log.debug("Magnification API not available")

	def _getCoordinatesForMode(
		self,
		coordinates: Coordinates,
	) -> Coordinates:
		"""
		Get Coordinates adjusted for the current full-screen mode

		:param coordinates: Raw coordinates (x, y)
		:return: Adjusted coordinates according to full-screen mode
		"""

		match self._fullscreenMode:
			case FullScreenMode.RELATIVE:
				return self._relativePos(coordinates)
			case FullScreenMode.BORDER:
				return self._borderPos(coordinates)
			case FullScreenMode.CENTER:
				return coordinates

	def moveMouseToScreen(self) -> None:
		"""
		keep mouse in screen
		"""
		left, top, visibleWidth, visibleHeight = self._getMagnifierPosition(self._currentCoordinates)
		centerX = int(left + (visibleWidth / 2))
		centerY = int(top + (visibleHeight / 2))
		winUser.setCursorPos(centerX, centerY)

	def _borderPos(
		self,
		coordinates: Coordinates,
	) -> Coordinates:
		"""
		Check if focus is near magnifier border and adjust position accordingly
		Returns adjusted position to keep focus within margin limits

		:param coordinates: Raw coordinates (x, y)

		:return: The adjusted position (x, y) of the focus point
		"""
		focusX, focusY = coordinates
		lastLeft, lastTop, visibleWidth, visibleHeight = self._getMagnifierPosition(
			self._lastScreenPosition,
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
			return Coordinates(self._lastScreenPosition[0] + dx, self._lastScreenPosition[1] + dy)
		else:
			return self._lastScreenPosition

	def _relativePos(
		self,
		coordinates: Coordinates,
	) -> Coordinates:
		"""
		Calculate magnifier center maintaining mouse relative position
		Handles screen edges to prevent going off-screen

		:param coordinates: Raw coordinates (x, y)

		:return: The (x, y) coordinates of the magnifier center
		"""

		zoom = self.zoomLevel
		mouseX, mouseY = coordinates
		visibleWidth = self._displayOrientation.width / zoom
		visibleHeight = self._displayOrientation.height / zoom
		margin = int(zoom * 10)

		# Calculate left/top maintaining mouse relative position
		left = mouseX - (mouseX / self._displayOrientation.width) * (visibleWidth - margin)
		top = mouseY - (mouseY / self._displayOrientation.height) * (visibleHeight - margin)

		# Clamp to screen boundaries
		left = max(0, min(left, self._displayOrientation.width - visibleWidth))
		top = max(0, min(top, self._displayOrientation.height - visibleHeight))

		# Return center of zoom window
		centerX = int(left + visibleWidth / 2)
		centerY = int(top + visibleHeight / 2)
		self._lastScreenPosition = Coordinates(centerX, centerY)
		return self._lastScreenPosition

	def _startSpotlight(self) -> None:
		"""
		Launch Spotlight from Full-screen class
		"""
		log.debug(f"Launching spotlight mode from full-screen magnifier with mode {self._fullscreenMode}")
		self._stopTimer()
		self._spotlightManager._startSpotlight()

	def _stopSpotlight(self) -> None:
		"""
		Stop and destroy Spotlight from Full-screen class
		"""
		self._spotlightManager._spotlightIsActive = False
		self._startTimer(self._updateMagnifier)
