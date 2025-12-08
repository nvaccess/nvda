# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import ctypes
from ctypes import wintypes

from logHandler import log
from typing import Callable
import ui
import winUser
import wx

from .magnifier import Magnifier
from .utils.filterHandler import FilterMatrix
from .utils.types import Filter, ZoomHistory, Coordinates, FullScreenMode, FocusType
from .config import (
	getDefaultFullscreenMode,
)


class FullScreenMagnifier(Magnifier):
	def __init__(self):
		super().__init__()
		self._fullscreenMode = getDefaultFullscreenMode()
		self._currentCoordinates: Coordinates = (0, 0)
		self._spotlightManager = SpotlightManager(self)
		self._startMagnifier()
		self._applyFilter()

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

	def event_gainFocus(self, obj, nextHandler):
		log.info("FullscreenMagnifier gain focus event")
		nextHandler()

	def _startMagnifier(self) -> None:
		"""
		Start the Fullscreen magnifier using windows DLL
		"""
		super()._startMagnifier()
		log.info(
			f"Starting magnifier with zoom level {self.zoomLevel} and filter {self.filterType} and fullscreen mode {self.fullscreenMode}"
		)
		self._loadMagnifierApi()
		self._startTimer(self._updateMagnifier)

	def _doUpdate(self):
		"""
		Perform the actual update of the magnifier
		"""
		# Calculate new position based on focus mode
		x, y = self._getCoordinatesForMode(self.currentCoordinates)
		# Always save screen position for mode continuity
		self.lastScreenPosition = (x, y)

		if self.lastFocusedObject == FocusType.NVDA:
			try:
				from .config import shouldKeepMouseCentered
			except ImportError:
				log.error("Failed to import shouldKeepMouseCentered from magnifier.config")
			else:
				if shouldKeepMouseCentered():
					self.moveMouseToScreen()
		# Apply transformation
		self._fullscreenMagnifier(x, y)

	def _stopMagnifier(self) -> None:
		"""
		Stop the Fullscreen magnifier using windows DLL
		"""
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
		"""
		Apply the current color filter to the fullscreen magnifier
		"""
		if self.filterType == Filter.NORMAL:
			ctypes.windll.magnification.MagSetFullscreenColorEffect(FilterMatrix.NORMAL.value)
		elif self.filterType == Filter.GREYSCALE:
			ctypes.windll.magnification.MagSetFullscreenColorEffect(FilterMatrix.GREYSCALE.value)
		elif self.filterType == Filter.INVERTED:
			ctypes.windll.magnification.MagSetFullscreenColorEffect(FilterMatrix.INVERTED.value)
		else:
			log.info(f"Unknown color filter: {self.filterType}")

	def _loadMagnifierApi(self) -> None:
		"""
		Initialize the Magnification API
		"""
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
		"""
		Stop the Magnification API
		"""
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
		"""
		Get Windows Magnification API function
		"""
		MagSetFullscreenTransform = ctypes.windll.magnification.MagSetFullscreenTransform
		MagSetFullscreenTransform.restype = wintypes.BOOL
		MagSetFullscreenTransform.argtypes = [ctypes.c_float, ctypes.c_int, ctypes.c_int]
		return MagSetFullscreenTransform

	def _fullscreenMagnifier(self, x: int, y: int) -> None:
		"""
		Apply fullscreen magnification at given Coordinates

		:param x: The x-coordinate for the magnifier
		:param y: The y-coordinate for the magnifier
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

	def _getCoordinatesForMode(self, coordinates: Coordinates) -> Coordinates:
		"""
		Get Coordinates adjusted for the current fullscreen mode

		:param coordinates: Raw Coordinates (x, y)

		Returns:
			Adjusted Coordinates according to fullscreen mode
		"""
		x, y = coordinates

		if self._fullscreenMode == FullScreenMode.RELATIVE:
			return self._relativePos(x, y)
		elif self._fullscreenMode == FullScreenMode.BORDER:
			return self._borderPos(x, y)
		else:  # CENTER mode
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

	def _borderPos(self, focusX: int, focusY: int) -> Coordinates:
		"""
		Check if focus is near magnifier border and adjust position accordingly
		Returns adjusted position to keep focus within margin limits

		:param focusX: The x-coordinate of the focus point
		:param focusY: The y-coordinate of the focus point

		Returns:
			lastScreenPosition (Coordinates): The adjusted position (x, y) of the focus point
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

	def _relativePos(self, mouseX: int, mouseY: int) -> Coordinates:
		"""
		Calculate magnifier center maintaining mouse relative position
		Handles screen edges to prevent going off-screen

		:param mouseX: The x-coordinate of the mouse pointer
		:param mouseY: The y-coordinate of the mouse pointer

		Returns:
			Coordinates: The (x, y) Coordinates of the magnifier center
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

	def _startSpotlight(self) -> None:
		"""
		Launch Spotlight from Fullscreen class
		"""
		log.info(f"Launching spotlight mode from fullscreen magnifier with mode {self._fullscreenMode}")
		self._stopTimer()
		self._spotlightManager._startSpotlight()

	def _stopSpotlight(self) -> None:
		"""
		Stop and destroy Spotlight from Fullscreen class
		"""
		self._spotlightManager._spotlightIsActive = False
		self._startTimer(self._updateMagnifier)


class SpotlightManager:
	def __init__(self, fullscreenMagnifier: FullScreenMagnifier):
		self._fullscreenMagnifier: FullScreenMagnifier = fullscreenMagnifier
		self._spotlightIsActive: bool = False
		self._lastMousePosition: Coordinates = (0, 0)
		self._timer: wx.CallLater | None = None
		self._animationSteps: int = 40
		self._currentCoordinates: Coordinates = fullscreenMagnifier._getFocusCoordinates()
		self._originalZoomLevel: float = fullscreenMagnifier.zoomLevel
		self._currentZoomLevel: float = fullscreenMagnifier.zoomLevel

	def _startSpotlight(self) -> None:
		"""
		Start the spotlight
		"""
		log.info("start spotlight")
		self._spotlightIsActive = True

		startCoords = self._fullscreenMagnifier._getFocusCoordinates()
		startCoords = self._fullscreenMagnifier._getCoordinatesForMode(startCoords)
		centerScreen = (
			self._fullscreenMagnifier._SCREEN_WIDTH // 2,
			self._fullscreenMagnifier._SCREEN_HEIGHT // 2,
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
			_(
				# Translators: Message announced when stopping the magnifier spotlight
				"Magnifier spotlight stopped"
			)
		)
		if self._timer:
			self._timer.Stop()
			self._timer = None

		self._spotlightIsActive = False
		self._fullscreenMagnifier._stopSpotlight()

	def _animateZoom(
		self, targetZoom: float, targetCoordinates: Coordinates, callback: Callable[[], None]
	) -> None:
		"""
		Animate the zoom level change

		:param targetZoom: The target zoom level
		:param targetCoordinates: The target Coordinates (x, y)
		:param callback: The function to call after animation completes
		"""
		self._animationStepsList = self._computeAnimationSteps(
			self._currentZoomLevel, targetZoom, self._currentCoordinates, targetCoordinates
		)

		self._executeStep(0, callback)

	def _executeStep(self, stepIndex: int, callback: Callable[[], None]) -> None:
		"""
		Execute one animation step

		:param stepIndex: The index of the current animation step
		:param callback: The function to call after animation completes
		"""

		if stepIndex < len(self._animationStepsList):
			zoomLevel, (x, y) = self._animationStepsList[stepIndex]
			self._fullscreenMagnifier.zoomLevel = zoomLevel
			self._fullscreenMagnifier._fullscreenMagnifier(x, y)
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
		:param CoordinateStart: Starting Coordinates (x, y)
		:param coordinateEnd: Ending Coordinates (x, y)

		Returns:
			List of animation steps as ZoomHistory for each animation step
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
