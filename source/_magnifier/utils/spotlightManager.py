# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Spotlight manager module for full-screen magnifier.
Manages the spotlight effect, including zooming in on focus and zooming back.
"""

from typing import TYPE_CHECKING, Callable
import ui
from .types import Coordinates, ZoomHistory, FullScreenMode
import wx
from logHandler import log

if TYPE_CHECKING:
	from _magnifier.fullscreenMagnifier import FullScreenMagnifier


class SpotlightManager:
	def __init__(
		self,
		fullscreenMagnifier: "FullScreenMagnifier",
	):
		self._fullscreenMagnifier: "FullScreenMagnifier" = fullscreenMagnifier
		self._spotlightIsActive: bool = False
		self._lastMousePosition = Coordinates(0, 0)
		self._timer: wx.CallLater | None = None
		self._animationSteps: int = 40
		self._currentCoordinates: Coordinates = fullscreenMagnifier._getFocusCoordinates()
		self._originalZoomLevel: float = 0.0
		self._currentZoomLevel: float = 0.0
		self._originalMode: FullScreenMode | None = None

	def _startSpotlight(self) -> None:
		"""
		Start the spotlight
		"""
		self._originalZoomLevel = self._fullscreenMagnifier.zoomLevel
		self._currentZoomLevel = self._fullscreenMagnifier.zoomLevel

		log.debug("start spotlight")

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
		log.debug("stop spotlight")
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
		log.debug(
			f"animate zoom with original zoom level {self._originalZoomLevel} and current zoom level {self._currentZoomLevel}",
		)

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
		log.debug(
			f"execute step with original zoom level {self._originalZoomLevel} and current zoom level {self._currentZoomLevel}",
		)

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
		log.debug(
			f"zoom back with original zoom level {self._originalZoomLevel} and current zoom level {self._currentZoomLevel}",
		)

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
		log.debug(
			f"compute animation steps with original zoom level {self._originalZoomLevel} and current zoom level {self._currentZoomLevel}",
		)

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
