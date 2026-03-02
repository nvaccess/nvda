# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue
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
from .utils.types import (
	Filter,
	Coordinates,
	MagnifierType,
	FullScreenMode,
	FocusType,
	Size,
	MagnifierParameters,
)
from .config import getDefaultFullscreenMode, shouldKeepMouseCentered, isTrueCentered


class FullScreenMagnifier(Magnifier):
	def __init__(self):
		super().__init__()
		self._magnifierType = MagnifierType.FULLSCREEN
		self._fullscreenMode = getDefaultFullscreenMode()
		self._currentCoordinates = Coordinates(0, 0)
		self._spotlightManager = SpotlightManager(self)
		self._displaySize = Size(self._displayOrientation.width, self._displayOrientation.height)

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

		if self._focusManager.getLastFocusType() == FocusType.NAVIGATOR:
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
		if not self._isActive:
			return

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
		if not self._isActive:
			return

		params = self._getMagnifierParameters(coordinates)
		try:
			result = magnification.MagSetFullscreenTransform(
				self.zoomLevel,
				params.coordinates.x,
				params.coordinates.y,
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
		Move mouse to center of magnified view.
		Skip if a mouse button is currently pressed to avoid interfering with clicks.
		"""
		# Check if any mouse button is pressed (left, right, or middle)
		if (
			winUser.getKeyState(winUser.VK_LBUTTON) < 0
			or winUser.getKeyState(winUser.VK_RBUTTON) < 0
			or winUser.getKeyState(winUser.VK_MBUTTON) < 0
		):
			log.debug("Mouse button pressed, skipping cursor repositioning to avoid interfering with click")
			return

		left, top, visibleWidth, visibleHeight = self._getMagnifierPosition(
			self._currentCoordinates,
		)
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
		params = self._getMagnifierParameters(self._lastScreenPosition)
		magnifierWidth = params.magnifierSize.width
		magnifierHeight = params.magnifierSize.height
		lastLeft = params.coordinates.x
		lastTop = params.coordinates.y

		minX = lastLeft + self._MARGIN_BORDER
		maxX = lastLeft + magnifierWidth - self._MARGIN_BORDER
		minY = lastTop + self._MARGIN_BORDER
		maxY = lastTop + magnifierHeight - self._MARGIN_BORDER

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
			return Coordinates(
				self._lastScreenPosition[0] + dx,
				self._lastScreenPosition[1] + dy,
			)
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
		magnifierWidth = self._displayOrientation.width / zoom
		magnifierHeight = self._displayOrientation.height / zoom
		margin = int(zoom * 10)

		# Calculate left/top maintaining mouse relative position
		left = mouseX - (mouseX / self._displayOrientation.width) * (magnifierWidth - margin)
		top = mouseY - (mouseY / self._displayOrientation.height) * (magnifierHeight - margin)

		# Clamp to screen boundaries
		left = max(0, min(left, self._displayOrientation.width - magnifierWidth))
		top = max(0, min(top, self._displayOrientation.height - magnifierHeight))

		# Return center of zoom window
		centerX = int(left + magnifierWidth / 2)
		centerY = int(top + magnifierHeight / 2)
		self._lastScreenPosition = Coordinates(centerX, centerY)
		return self._lastScreenPosition

	def _startSpotlight(self) -> None:
		"""
		Launch Spotlight from Full-screen class
		"""
		log.debug(
			f"Launching spotlight mode from full-screen magnifier with mode {self._fullscreenMode}",
		)
		self._stopTimer()
		self._spotlightManager._startSpotlight()

	def _stopSpotlight(self) -> None:
		"""
		Stop and destroy Spotlight from Full-screen class
		"""
		self._spotlightManager._spotlightIsActive = False
		self._startTimer(self._updateMagnifier)

	def _getMagnifierParameters(self, coordinates: Coordinates) -> MagnifierParameters:
		"""
		Compute the top-left corner of the magnifier window centered on (x, y)

		:param coordinates: The (x, y) coordinates to center the magnifier on
		:param displaySize: The size of the display area (width, height) - used to calculate capture size

		:return: The size, position and filter of the magnifier window
		"""
		x, y = coordinates
		# Calculate the size of the capture area at the current zoom level
		magnifierWidth = self._displayOrientation.width / self.zoomLevel
		magnifierHeight = self._displayOrientation.height / self.zoomLevel

		# Compute the top-left corner so that (x, y) is at the center
		left = int(x - (magnifierWidth / 2))
		top = int(y - (magnifierHeight / 2))

		# Clamp to screen boundaries only if not in true center mode
		if not isTrueCentered():
			left = max(0, min(left, int(self._displayOrientation.width - magnifierWidth)))
			top = max(0, min(top, int(self._displayOrientation.height - magnifierHeight)))

		return MagnifierParameters(
			Size(int(magnifierWidth), int(magnifierHeight)),
			Coordinates(left, top),
			self._filterType,
		)
