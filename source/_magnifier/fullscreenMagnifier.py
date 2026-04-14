# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Full-screen magnifier module.
"""

from logHandler import log
import screenCurtain
import ui
import winUser
from winBindings import magnification
from .magnifier import Magnifier
from .utils.filterHandler import FilterMatrix
from .utils.spotlightManager import SpotlightManager
from .utils.types import Filter, Coordinates, FullScreenMode
from .config import getDefaultFullscreenMode
from .utils.errorHandling import trackNativeMagnifierErrors


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
		self._initializeNativeMagnification()

		if self._isActive:
			self._applyFilter()
		self._startTimer(self._updateMagnifier)

	@trackNativeMagnifierErrors
	def _initializeNativeMagnification(self) -> None:
		"""
		Initialize the Magnification API.
		If already initialized or on failure, continues anyway.
		"""
		magnification.MagInitialize()
		log.debug("Magnification API initialized")

	def _doUpdate(self):
		"""
		Perform the actual update of the magnifier
		"""
		# Calculate new position based on focus mode
		coordinates = self._getCoordinatesForMode(self._currentCoordinates)
		# Always save screen position for mode continuity
		self._lastScreenPosition = coordinates

		self._fullscreenMagnifier(coordinates)

	def _stopMagnifier(self) -> None:
		"""
		Stop the Full-screen magnifier using windows DLL
		"""
		super()._stopMagnifier()
		self._resetMagnification()
		self._uninitializeNativeMagnification()

	@trackNativeMagnifierErrors
	def _resetMagnification(self) -> None:
		"""
		Reset fullscreen magnifier to neutral state:
		- Zoom: 1.0 (no magnification)
		- Position: 0,0
		- Color effect: normal (identity matrix)
		"""
		magnification.MagSetFullscreenTransform(1.0, 0, 0)
		magnification.MagSetFullscreenColorEffect(FilterMatrix.NORMAL.value)
		log.debug("Magnification reset to neutral state")

	@trackNativeMagnifierErrors
	def _uninitializeNativeMagnification(self) -> None:
		"""
		Uninitialize the Magnification API.
		If already uninitialized or on failure, continues anyway.
		"""
		magnification.MagUninitialize()
		log.debug("Magnification API uninitialized")

	def _attemptRecovery(self) -> None:
		"""
		Attempt to recover from repeated Magnification API errors by
		reinitializing the API. If recovery fails, the magnifier is stopped.

		Each step (uninitialize, initialize, apply filter, restart timer) is
		controlled independently. If any critical step fails, recovery is aborted.
		"""
		log.info("Attempting full-screen magnifier recovery via API reinitialization")

		# Step 1: Uninitialize (best effort, may already be uninitialized)
		self._uninitializeNativeMagnification()

		# Step 2: Initialize (critical - raises on failure)
		try:
			magnification.MagInitialize()
			log.debug("Magnification API initialized during recovery")
		except OSError:
			log.error("MagInitialize during recovery failed, aborting recovery", exc_info=True)
			self._conductRecoveryFailure()
			return

		# Step 3: Apply filter (critical - raises on failure)
		try:
			magnification.MagSetFullscreenColorEffect(self._getFilterMatrix().value)
			log.debug("Filter applied during recovery")
		except OSError:
			log.error("Failed to apply filter during recovery, aborting recovery", exc_info=True)
			self._conductRecoveryFailure()
			return

		# All steps succeeded
		self._consecutiveErrors = 0
		log.info("Full-screen magnifier recovery succeeded")
		self._startTimer(self._updateMagnifier)

	def _conductRecoveryFailure(self) -> None:
		"""
		Handle unrecoverable magnifier error: stop magnifier and notify user.
		"""
		self._consecutiveErrors = 0
		self._stopMagnifier()
		ui.message(
			pgettext(
				"magnifier",
				# Translators: Message announced when the magnifier stops due to an unrecoverable error.
				"Magnifier stopped due to an error. Please restart it.",
			),
		)

	def _getFilterMatrix(self) -> FilterMatrix:
		"""Return the FilterMatrix corresponding to the current filter type."""
		match self.filterType:
			case Filter.NORMAL:
				return FilterMatrix.NORMAL
			case Filter.GRAYSCALE:
				return FilterMatrix.GRAYSCALE
			case Filter.INVERTED:
				return FilterMatrix.INVERTED

	@trackNativeMagnifierErrors
	def _applyFilter(self) -> None:
		"""
		Apply the current color filter to the full-screen magnifier.

		If an OSError occurs (native API failure), it is logged and execution continues.
		"""
		magnification.MagSetFullscreenColorEffect(self._getFilterMatrix().value)

	def _fullscreenMagnifier(self, coordinates: Coordinates) -> None:
		"""
		Apply full-screen magnification at given Coordinates.

		Exceptions from MagSetFullscreenTransform are intentionally left to
		propagate so that _updateMagnifier can count them and trigger recovery when needed.

		:coordinates: The (x, y) coordinates to center the magnifier on
		"""
		left, top, visibleWidth, visibleHeight = self._getMagnifierPosition(coordinates)
		magnification.MagSetFullscreenTransform(
			self.zoomLevel,
			left,
			top,
		)

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

	def _keepMouseCentered(self) -> None:
		"""
		Move the mouse to the center of the magnified view.
		Skips if a mouse button is currently pressed to avoid interfering with clicks.
		"""
		if (
			winUser.getKeyState(winUser.VK_LBUTTON) < 0
			or winUser.getKeyState(winUser.VK_RBUTTON) < 0
			or winUser.getKeyState(winUser.VK_MBUTTON) < 0
		):
			log.debug("Mouse button pressed, skipping cursor repositioning to avoid interfering with click")
			return
		coords = self._getCoordinatesForMode(self._currentCoordinates)
		left, top, visibleWidth, visibleHeight = self._getMagnifierPosition(coords)
		centerX = left + visibleWidth // 2
		centerY = top + visibleHeight // 2
		self._setCursorToCenter(centerX, centerY)

	@trackNativeMagnifierErrors
	def _setCursorToCenter(self, x: int, y: int) -> None:
		"""
		Set cursor to the specified position.
		If this fails, it is logged but execution continues.
		"""
		winUser.setCursorPos(x, y)
		log.debug(f"Cursor repositioned to center ({x}, {y})")

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
