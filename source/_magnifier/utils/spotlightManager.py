# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Spotlight manager module for full-screen magnifier.
Manages the spotlight effect, including zooming in on focus and zooming back.
"""

from typing import TYPE_CHECKING, Callable
import ui
from .types import Coordinates, AnimationFrame, FullScreenMode
from .animationManager import AnimationManager
from ..config import ZoomLevel
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
		self._animationStepDelay: int = 12
		self._animator: AnimationManager = AnimationManager(totalSteps=40)
		self._currentCoordinates: Coordinates = fullscreenMagnifier._focusManager.getCurrentFocusCoordinates()
		self._originalZoomLevel: int = 0
		self._currentZoomLevel: float = 0.0
		self._originalMode: FullScreenMode | None = None
		self._animationStep: int = 0

	def _startSpotlight(self) -> None:
		"""
		Start the spotlight
		"""
		self._originalZoomLevel = self._fullscreenMagnifier.zoomLevel
		self._currentZoomLevel = self._fullscreenMagnifier.zoomLevel

		startCoords = self._fullscreenMagnifier._focusManager.getCurrentFocusCoordinates()
		startCoords = self._fullscreenMagnifier._getCoordinatesForMode(startCoords)
		centerScreen = Coordinates(
			self._fullscreenMagnifier._displayOrientation.width // 2,
			self._fullscreenMagnifier._displayOrientation.height // 2,
		)

		# Save the current mode for zoom back
		self._originalMode = self._fullscreenMagnifier._fullscreenMode
		self._currentCoordinates = startCoords

		log.debug(
			f"[spotlight] start — zoom={self._originalZoomLevel}, "
			f"startCoords={startCoords}, centerScreen={centerScreen}, mode={self._originalMode}",
		)

		self._spotlightIsActive = True
		self._animator.start(AnimationFrame(self._currentZoomLevel, self._currentCoordinates))
		self._animateZoom(AnimationFrame(float(ZoomLevel.MIN_ZOOM), centerScreen), self._startMouseMonitoring)

	def _stopSpotlight(self) -> None:
		"""
		Stop the spotlight
		"""
		log.debug("[spotlight] _stopSpotlight called — stopping timer and notifying user")
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
		target: AnimationFrame,
		callback: Callable[[], None],
	) -> None:
		"""
		Animate the zoom level change towards target, then call callback.

		:param target: The target animation frame (zoom level and coordinates)
		:param callback: The function to call after animation completes
		"""
		self._animationStep = 0
		log.debug(
			f"[spotlight] _animateZoom — from zoom={self._currentZoomLevel:.2f} "
			f"to zoom={target.zoomLevel:.2f}, coords={target.coordinates}, callback={getattr(callback, '__name__', type(callback).__name__)}",
		)
		self._animator.setTarget(target, onComplete=callback)
		self._driveAnimation()

	def _driveAnimation(self) -> None:
		"""
		Advance the animator by one step, apply the resulting frame to the magnifier,
		and schedule the next step if the animation is not yet complete.
		"""
		if not self._fullscreenMagnifier._isActive:
			log.debug(
				f"[spotlight] _driveAnimation aborted at step {self._animationStep} — magnifier no longer active",
			)
			if self._timer:
				self._timer.Stop()
				self._timer = None
			self._spotlightIsActive = False
			return

		self._animationStep += 1
		frame = self._animator.tick()

		if self._animationStep == 1 or self._animationStep % 10 == 0:
			log.debug(
				f"[spotlight] step {self._animationStep} — zoom={frame.zoomLevel:.2f}, coords={frame.coordinates}",
			)

		try:
			self._fullscreenMagnifier._setZoomRawValue(frame.zoomLevel)
			self._fullscreenMagnifier._fullscreenMagnifier(frame.coordinates)
		except Exception:
			log.error(
				f"[spotlight] error at step {self._animationStep} — aborting spotlight",
				exc_info=True,
			)
			self._stopSpotlight()
			return

		self._currentZoomLevel = frame.zoomLevel
		self._currentCoordinates = frame.coordinates

		if self._animator.isComplete:
			self._timer = None
			log.debug(
				f"[spotlight] animation complete at step {self._animationStep} "
				f"— final zoom={frame.zoomLevel:.2f}, coords={frame.coordinates}",
			)
		else:
			self._timer = wx.CallLater(self._animationStepDelay, self._driveAnimation)

	def _startMouseMonitoring(self) -> None:
		"""
		Start monitoring the mouse position to detect idleness
		"""
		self._lastMousePosition = Coordinates(*wx.GetMousePosition())
		log.debug(f"[spotlight] _startMouseMonitoring — mouse at {self._lastMousePosition}, waiting 2000 ms")
		self._timer = wx.CallLater(2000, self._checkMouseIdle)

	def _checkMouseIdle(self) -> None:
		"""
		Check if the mouse has been idle
		"""
		currentMousePosition = Coordinates(*wx.GetMousePosition())
		log.debug(
			f"[spotlight] _checkMouseIdle — current={currentMousePosition}, last={self._lastMousePosition}, "
			f"idle={currentMousePosition == self._lastMousePosition}",
		)
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
		focus = self._fullscreenMagnifier._focusManager.getCurrentFocusCoordinates()

		if self._originalMode == FullScreenMode.RELATIVE:
			savedZoom = self._fullscreenMagnifier.zoomLevel
			self._fullscreenMagnifier.zoomLevel = self._originalZoomLevel
			endCoordinates = self._fullscreenMagnifier._relativePos(focus)
			self._fullscreenMagnifier.zoomLevel = savedZoom
		else:
			endCoordinates = focus
			self._fullscreenMagnifier._lastScreenPosition = endCoordinates

		log.debug(
			f"[spotlight] zoomBack — originalZoom={self._originalZoomLevel}, "
			f"currentZoom={self._currentZoomLevel:.2f}, focus={focus}, endCoords={endCoordinates}",
		)
		self._animateZoom(AnimationFrame(self._originalZoomLevel, endCoordinates), self._stopSpotlight)
