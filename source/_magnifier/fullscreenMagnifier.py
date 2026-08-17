# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Full-screen magnifier module.
"""

from ctypes import byref
from ctypes.wintypes import RECT
from typing import override

from logHandler import log
import ui
import systemUtils
from winBindings import magnification
from .magnifier import Magnifier
from .utils.filterHandler import FilterMatrix
from .utils.spotlightManager import SpotlightManager
from .utils.types import (
	Filter,
	MagnifiedView,
	FullScreenMode,
	Size,
	MagnifierParameters,
	Coordinates,
)
from .config import getFullscreenMode, isTrueCentered, _isDebug
from .utils.errorHandling import trackNativeMagnifierErrors, MagnifierStartError


class FullScreenMagnifier(Magnifier):
	"""Magnifier that uses the Windows Magnification API to magnify the entire screen."""

	_MAX_RECOVERY_ATTEMPTS: int = 3
	_MAGNIFIED_VIEW = MagnifiedView.FULLSCREEN

	def __init__(self):
		super().__init__()
		self._fullscreenMode = getFullscreenMode()
		self.currentCoordinates = Coordinates(0, 0)
		self._spotlightManager = SpotlightManager(self)
		self._displaySize = Size(self._displayOrientation.width, self._displayOrientation.height)
		self._inputTransformSupported = systemUtils.hasUiAccess()

	@staticmethod
	def _isAccessDeniedError(error: OSError) -> bool:
		"""Return True when OSError represents Windows access denied (WinError 5)."""
		return getattr(error, "winerror", None) == 5

	@Magnifier.filterType.setter
	def filterType(self, value: Filter) -> None:
		self._filterType = value
		if self._isActive:
			self._applyFilter()

	def event_gainFocus(
		self,
		obj,
		nextHandler,
	):
		if _isDebug():
			log.debug("Full-screen Magnifier gain focus event")
		nextHandler()

	@override
	def _startMagnifier(self) -> None:
		"""
		Start the Full-screen magnifier using windows DLL
		"""
		super()._startMagnifier()
		if not self._isActive:
			return
		if _isDebug():
			log.debug(
				f"Starting magnifier with zoom level {self.zoomLevel} and filter {self.filterType} and full-screen tracking mode {self._fullscreenMode}",
			)
		try:
			self._initializeNativeMagnification()
		except OSError:
			log.exception("Failed to initialize magnification API")
			# _isActive is True from super(), so _stopMagnifier properly unregisters
			self._stopMagnifier()
			raise MagnifierStartError(
				pgettext(
					"magnifier",
					# Translators: Message when NVDA's Magnifier cannot start because another magnifier is already running.
					"Cannot start magnifier. Another magnifier application may already be running.",
				),
			)

		if self._isActive:
			self._applyFilter()
		self._startTimer(self._updateMagnifier)

	def _clearStaleApiState(self) -> None:
		"""
		Dummy MagInitialize/MagUninitialize cycle to clear stale Windows API state.

		After a MagSetFullscreenTransform or MagSetFullscreenColorEffect call,
		MagUninitialize leaves internal state that causes the next MagSetFullscreenTransform
		to fail. Resetting the color effect to neutral here also clears stale state
		left by a screen curtain session. All OSError exceptions are suppressed.
		"""
		try:
			magnification.MagInitialize()
		except OSError:
			return
		try:
			magnification.MagSetFullscreenColorEffect(FilterMatrix.NORMAL.value)
		except OSError:
			pass
		try:
			magnification.MagUninitialize()
		except OSError:
			pass

	def _initializeNativeMagnification(self) -> None:
		"""
		Initialize the Magnification API and apply the initial fullscreen transform.

		Raises OSError if MagInitialize or MagSetFullscreenTransform fails.
		"""
		self._uninitializeNativeMagnification()
		self._clearStaleApiState()
		magnification.MagInitialize()
		if _isDebug():
			log.debug("Magnification API initialized")
		# Applying the first real update verifies the API is usable without
		# briefly jumping the magnified view to the top-left corner.
		try:
			coordinates = self._getCoordinatesForMode(self.currentCoordinates)
			# Save screen position for mode continuity, matching _doUpdate.
			self._lastScreenPosition = coordinates
			self._fullscreenMagnifier(coordinates)
		except OSError:
			self._uninitializeNativeMagnification()
			raise

	@override
	def _doUpdate(self):
		"""
		Perform the actual update of the magnifier
		"""
		# Calculate new position based on focus mode
		coordinates = self._getCoordinatesForMode(self.currentCoordinates)
		# Always save screen position for mode continuity
		self._lastScreenPosition = coordinates

		self._fullscreenMagnifier(coordinates)

	@override
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
		if self._inputTransformSupported:
			destRect = RECT(0, 0, self._displayOrientation.width, self._displayOrientation.height)
			try:
				magnification.MagSetInputTransform(False, byref(destRect), byref(destRect))
			except OSError as e:
				if self._isAccessDeniedError(e):
					self._inputTransformSupported = False
				else:
					raise
		magnification.MagSetFullscreenTransform(1.0, 0, 0)
		magnification.MagSetFullscreenColorEffect(FilterMatrix.NORMAL.value)
		if _isDebug():
			log.debug("Magnification reset to neutral state")

	@trackNativeMagnifierErrors
	def _uninitializeNativeMagnification(self) -> None:
		"""
		Uninitialize the Magnification API.
		If already uninitialized or on failure, continues anyway.
		"""
		magnification.MagUninitialize()
		if _isDebug():
			log.debug("Magnification API uninitialized")

	@override
	def _attemptRecovery(self) -> None:
		"""
		Attempt to recover from repeated Magnification API errors by
		reinitializing the API. If recovery fails, the magnifier is stopped.

		Capped at _MAX_RECOVERY_ATTEMPTS to prevent an infinite restart loop
		when the API is permanently unavailable (e.g. Windows Magnifier running).
		"""
		self._recoveryAttempts += 1
		if self._recoveryAttempts > self._MAX_RECOVERY_ATTEMPTS:
			log.error(
				f"Max recovery attempts ({self._MAX_RECOVERY_ATTEMPTS}) reached, stopping magnifier",
			)
			self._conductRecoveryFailure()
			return

		log.debug(
			f"Attempting full-screen magnifier recovery "
			f"(attempt {self._recoveryAttempts}/{self._MAX_RECOVERY_ATTEMPTS})",
		)

		try:
			# _initializeNativeMagnification also probes MagSetFullscreenTransform,
			# which is the call that fails when Windows Magnifier is running.
			self._initializeNativeMagnification()
			magnification.MagSetFullscreenColorEffect(self._getFilterMatrix().value)
		except OSError:
			log.error("Recovery failed", exc_info=True)
			self._conductRecoveryFailure()
			return

		self._consecutiveErrors = 0
		log.debug("Full-screen magnifier recovery succeeded")
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
		params = self._getMagnifierParameters(coordinates)
		magnification.MagSetFullscreenTransform(
			self.zoomLevelRatio,
			params.coordinates.x,
			params.coordinates.y,
		)
		if self._inputTransformSupported:
			sourceRect = RECT(
				params.coordinates.x,
				params.coordinates.y,
				params.coordinates.x + params.magnifierSize.width,
				params.coordinates.y + params.magnifierSize.height,
			)
			destRect = RECT(0, 0, self._displayOrientation.width, self._displayOrientation.height)
			try:
				magnification.MagSetInputTransform(True, byref(sourceRect), byref(destRect))
			except OSError as e:
				if self._isAccessDeniedError(e):
					self._inputTransformSupported = False
					log.debugWarning(
						"MagSetInputTransform unavailable (UIAccess required). Continuing without input transform.",
						exc_info=e,
					)
				else:
					raise

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
			case FullScreenMode.CENTER:
				return coordinates

	def _computeMagnifiedViewCenter(self) -> Coordinates:
		"""
		Compute the coordinates of the center of the currently magnified view.

		:return: The (x, y) coordinates of the center of the magnified view
		"""

		coordinates = self._getCoordinatesForMode(self.currentCoordinates)
		params = self._getMagnifierParameters(coordinates)
		centerX = params.coordinates.x + params.magnifierSize.width // 2
		centerY = params.coordinates.y + params.magnifierSize.height // 2
		return Coordinates(centerX, centerY)

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

		zoom = self.zoomLevelRatio
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
		if _isDebug():
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

	@override
	def _getMagnifierParameters(self, coordinates: Coordinates) -> MagnifierParameters:
		"""
		Compute the top-left corner of the magnifier window centered on (x, y)

		:param coordinates: The (x, y) coordinates to center the magnifier on

		:return: The size, position and filter of the magnifier window
		"""
		x, y = coordinates
		# Calculate the size of the capture area at the current zoom level
		magnifierWidth = self._displayOrientation.width / self.zoomLevelRatio
		magnifierHeight = self._displayOrientation.height / self.zoomLevelRatio

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
