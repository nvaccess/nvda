# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Full-screen magnifier module.
"""

from logHandler import log
from typing import Callable
import ui
import winUser
import wx
from winBindings import magnification
from .magnifier import Magnifier
from .utils.filterHandler import FilterMatrix
from .utils.types import Filter, ZoomHistory, Coordinates, FullScreenMode, FocusType
from .config import getDefaultFullscreenMode, shouldKeepMouseCentered


class FullScreenMagnifier(Magnifier):
	def __init__(self):
		super().__init__()
		self._fullscreenMode = getDefaultFullscreenMode()
		self._currentCoordinates = Coordinates(0, 0)
		self._spotlightManager = SpotlightManager(self)
		self._startMagnifier()

	@property
	def fullscreenMode(self) -> FullScreenMode:
		return self._fullscreenMode

	@fullscreenMode.setter
	def fullscreenMode(self, value: FullScreenMode) -> None:
		self._fullscreenMode = value

	@property
	def currentCoordinates(self) -> Coordinates:
		return self._currentCoordinates

	@currentCoordinates.setter
	def currentCoordinates(self, value: Coordinates) -> None:
		self._currentCoordinates = value

	@property
	def filterType(self) -> Filter:
		return super().filterType

	@filterType.setter
	def filterType(self, value: Filter) -> None:
		Magnifier.filterType.fset(self, value)
		if self.isActive:
			self._applyFilter()

	def event_gainFocus(
		self,
		obj,
		nextHandler,
	):
		log.info("Full-screen Magnifier gain focus event")
		nextHandler()

	def _startMagnifier(self) -> None:
		"""
		Start the Full-screen magnifier using windows DLL
		"""
		super()._startMagnifier()
		log.info(
			f"Starting magnifier with zoom level {self.zoomLevel} and filter {self.filterType} and full-screen mode {self.fullscreenMode}",
		)
		# Initialize Magnification API if not already initialized
		try:
			magnification.MagInitialize()
			log.debug("Magnification API initialized")
		except Exception as e:
			# Already initialized or failed - continue anyway
			log.debug(f"MagInitialize result: {e}")

		if self.isActive:
			self._applyFilter()
		self._startTimer(self._updateMagnifier)

	def _doUpdate(self):
		"""
		Perform the actual update of the magnifier
		"""
		# Calculate new position based on focus mode
		coordinates = self._getCoordinatesForMode(self.currentCoordinates)
		# Always save screen position for mode continuity
		self.lastScreenPosition = coordinates

		if self.lastFocusedObject == FocusType.NVDA:
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
			log.info(f"Error resetting magnification: {e}")

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
				log.info("Failed to set full-screen transform")
		except AttributeError:
			log.info("Magnification API not available")

	def _getCoordinatesForMode(
		self,
		coordinates: Coordinates,
	) -> Coordinates:
		"""
		Get Coordinates adjusted for the current full-screen mode

		:param coordinates: Raw coordinates (x, y)
		:returns Coordinates: Adjusted coordinates according to full-screen mode
		"""
		x, y = coordinates

		match self._fullscreenMode:
			case FullScreenMode.RELATIVE:
				return self._relativePos(x, y)
			case FullScreenMode.BORDER:
				return self._borderPos(x, y)
			case FullScreenMode.CENTER:
				return coordinates

	def moveMouseToScreen(self) -> None:
		"""
		keep mouse in screen
		"""
		x, y = self.currentCoordinates
		left, top, visibleWidth, visibleHeight = self._getMagnifierPosition(x, y)
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

		:returns Coordinates: The adjusted position (x, y) of the focus point
		"""
		focusX, focusY = coordinates
		lastLeft, lastTop, visibleWidth, visibleHeight = self._getMagnifierPosition(
			self.lastScreenPosition,
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
			return Coordinates(self.lastScreenPosition[0] + dx, self.lastScreenPosition[1] + dy)
		else:
			return self.lastScreenPosition

	def _relativePos(
		self,
		coordinates: Coordinates,
	) -> Coordinates:
		"""
		Calculate magnifier center maintaining mouse relative position
		Handles screen edges to prevent going off-screen

		:param coordinates: Raw coordinates (x, y)

		:returns Coordinates: The (x, y) coordinates of the magnifier center
		"""

		zoom = self.zoomLevel
		mouseX, mouseY = coordinates
		visibleWidth = self._screenWidth / zoom
		visibleHeight = self._screenHeight / zoom
		margin = int(zoom * 10)

		# Calculate left/top maintaining mouse relative position
		left = mouseX - (mouseX / self._screenWidth) * (visibleWidth - margin)
		top = mouseY - (mouseY / self._screenHeight) * (visibleHeight - margin)

		# Clamp to screen boundaries
		left = max(0, min(left, self._screenWidth - visibleWidth))
		top = max(0, min(top, self._screenHeight - visibleHeight))

		# Return center of zoom window
		centerX = int(left + visibleWidth / 2)
		centerY = int(top + visibleHeight / 2)
		self.lastScreenPosition = Coordinates(centerX, centerY)
		return self.lastScreenPosition

	def _startSpotlight(self) -> None:
		"""
		Launch Spotlight from Full-screen class
		"""
		log.info(f"Launching spotlight mode from full-screen magnifier with mode {self._fullscreenMode}")
		self._stopTimer()
		self._spotlightManager._startSpotlight()

	def _stopSpotlight(self) -> None:
		"""
		Stop and destroy Spotlight from Full-screen class
		"""
		self._spotlightManager._spotlightIsActive = False
		self._startTimer(self._updateMagnifier)


class SpotlightManager:
	def __init__(
		self,
		fullscreenMagnifier: FullScreenMagnifier,
	):
		self._fullscreenMagnifier: FullScreenMagnifier = fullscreenMagnifier
		self._spotlightIsActive: bool = False
		self._lastMousePosition = Coordinates(0, 0)
		self._timer: wx.CallLater | None = None
		self._animationSteps: int = 40
		self._currentCoordinates: Coordinates = fullscreenMagnifier._getFocusCoordinates()
		self._originalZoomLevel: float = fullscreenMagnifier.zoomLevel
		self._currentZoomLevel: float = fullscreenMagnifier.zoomLevel
		self._originalMode: FullScreenMode | None = None

	def _startSpotlight(self) -> None:
		"""
		Start the spotlight
		"""
		log.info("start spotlight")
		self._spotlightIsActive = True

		startCoords = self._fullscreenMagnifier._getFocusCoordinates()
		startCoords = self._fullscreenMagnifier._getCoordinatesForMode(startCoords)
		centerScreen = (
			self._fullscreenMagnifier._screenWidth // 2,
			self._fullscreenMagnifier._screenHeight // 2,
		)

		# Save the current mode for zoom back
		self._originalMode = self._fullscreenMagnifier._fullscreenMode
		self._currentCoordinates = startCoords
		self._animateZoom(1.0, centerScreen, self._startMouseMonitoring)

	def _stopSpotlight(self) -> None:
		"""
		Stop the spotlight
		"""
		log.info("stop spotlight")
		ui.message(
			pgettext(
				"magnifier",
				# Translators: Message announced when stopping the magnifier spotlight.
				"Magnifier spotlight stopped",
			),
		)
		if self._timer:
			self._timer.Stop()
			self._timer = None

		self._spotlightIsActive = False
		self._fullscreenMagnifier._stopSpotlight()

	def _animateZoom(
		self,
		targetZoom: float,
		targetCoordinates: Coordinates,
		callback: Callable[[], None],
	) -> None:
		"""
		Animate the zoom level change

		:param targetZoom: The target zoom level
		:param targetCoordinates: The target Coordinates (x, y)
		:param callback: The function to call after animation completes
		"""
		self._animationStepsList = self._computeAnimationSteps(
			self._currentZoomLevel,
			targetZoom,
			self._currentCoordinates,
			targetCoordinates,
		)

		self._executeStep(0, callback)

	def _executeStep(
		self,
		stepIndex: int,
		callback: Callable[[], None],
	) -> None:
		"""
		Execute one animation step

		:param stepIndex: The index of the current animation step
		:param callback: The function to call after animation completes
		"""

		if stepIndex < len(self._animationStepsList):
			zoomLevel, (x, y) = self._animationStepsList[stepIndex]
			self._fullscreenMagnifier.zoomLevel = zoomLevel
			self._fullscreenMagnifier._fullscreenMagnifier((x, y))
			self._currentZoomLevel = zoomLevel
			self._currentCoordinates = (x, y)
			wx.CallLater(12, lambda: self._executeStep(stepIndex + 1, callback))
		else:
			if callback:
				callback()

	def _startMouseMonitoring(self) -> None:
		"""
		Start monitoring the mouse position to detect idleness
		"""
		self._lastMousePosition = wx.GetMousePosition()
		self._timer = wx.CallLater(2000, self._checkMouseIdle)

	def _checkMouseIdle(self) -> None:
		"""
		Check if the mouse has been idle
		"""
		currentMousePosition = wx.GetMousePosition()
		if currentMousePosition == self._lastMousePosition:
			self.zoomBack()
		else:
			# Mouse moved, continue monitoring
			self._lastMousePosition = currentMousePosition
			self._currentCoordinates = currentMousePosition
			self._timer = wx.CallLater(1500, self._checkMouseIdle)

	def zoomBack(self) -> None:
		"""
		Zoom back to mouse position
		"""
		focusX, focusY = self._fullscreenMagnifier._getFocusCoordinates()

		if self._originalMode == FullScreenMode.RELATIVE:
			savedZoom = self._fullscreenMagnifier.zoomLevel
			self._fullscreenMagnifier.zoomLevel = self._originalZoomLevel
			endCoordinates = self._fullscreenMagnifier._relativePos(focusX, focusY)
			self._fullscreenMagnifier.zoomLevel = savedZoom
		else:
			endCoordinates = (focusX, focusY)
			self._fullscreenMagnifier.lastScreenPosition = endCoordinates

		self._animateZoom(self._originalZoomLevel, endCoordinates, self._stopSpotlight)

	def _computeAnimationSteps(
		self,
		zoomStart: float,
		zoomEnd: float,
		coordinateStart: Coordinates,
		coordinateEnd: Coordinates,
	) -> list[ZoomHistory]:
		"""
		Compute all intermediate animation steps with zoom levels and Coordinates

		:param zoomStart: Starting zoom level
		:param zoomEnd: Ending zoom level
		:param coordinateStart: Starting Coordinates (x, y)
		:param coordinateEnd: Ending Coordinates (x, y)

		:returns ZoomHistory list: List of animation steps as ZoomHistory for each animation step
		"""
		startX, startY = coordinateStart
		endX, endY = coordinateEnd
		animationSteps = []

		zoomDelta = (zoomEnd - zoomStart) / self._animationSteps
		coordDeltaX = (endX - startX) / self._animationSteps
		coordDeltaY = (endY - startY) / self._animationSteps

		for step in range(1, self._animationSteps + 1):
			currentZoom = zoomStart + zoomDelta * step

			currentX = startX + coordDeltaX * step
			currentY = startY + coordDeltaY * step

			animationSteps.append((round(currentZoom, 2), (int(round(currentX)), int(round(currentY)))))
		return animationSteps
