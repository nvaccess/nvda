# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Magnifier module.
Implements the magnifier global class and its basic functionalities.
"""

from typing import Callable
from logHandler import log
import wx
import api
import ui
import speech
import screenCurtain
import winUser
import mouseHandler
from winAPI import _displayTracking
from winAPI._displayTracking import OrientationState, getPrimaryDisplayOrientation
from .utils.types import (
	MagnifierPosition,
	Coordinates,
	MagnifierType,
	Direction,
	FocusType,
	Filter,
)

from .config import getDefaultZoomLevel, getDefaultFilter, ZoomLevel


class Magnifier:
	_TIMER_INTERVAL_MS: int = 12
	_MARGIN_BORDER: int = 50

	def __init__(self):
		self._displayOrientation = getPrimaryDisplayOrientation()
		self._magnifierType: MagnifierType
		self._isActive: bool = False
		self._zoomLevel: float = getDefaultZoomLevel()
		self._timer: None | wx.Timer = None
		self._lastFocusedObject: FocusType | None = None
		self._lastNVDAPosition = Coordinates(0, 0)
		self._lastMousePosition = Coordinates(0, 0)
		self._lastScreenPosition = Coordinates(0, 0)
		self._currentCoordinates = Coordinates(0, 0)
		self._filterType: Filter = getDefaultFilter()
		# Register for display changes
		_displayTracking.displayChanged.register(self._onDisplayChanged)
		self._screenCurtainIsActive: bool = False

	@property
	def zoomLevel(self) -> float:
		return self._zoomLevel

	@zoomLevel.setter
	def zoomLevel(self, value: float) -> None:
		"""
		Set zoom level, ensuring it's a valid value in the zoom range.

		:param value: The zoom level to set
		:raises ValueError: If the value is not in the valid zoom range
		"""
		validZoomValues = ZoomLevel.zoom_range()
		if value not in validZoomValues:
			# Find the closest valid zoom value
			closestZoom = min(validZoomValues, key=lambda x: abs(x - value))
			log.warning(f"Invalid zoom level {value}, using closest valid value {closestZoom}")
			value = closestZoom
		self._zoomLevel = value

	def _setZoomRawValue(self, value: float) -> None:
		"""
		Set zoom level directly without validation.
		Used internally for smooth animations (e.g., spotlight).

		:param value: The zoom level to set (can be any intermediate value)
		"""
		self._zoomLevel = value

	# Functions
	def _onDisplayChanged(self, orientationState: OrientationState) -> None:
		"""
		Called when display configuration changes
		"""
		log.debug("Display configuration changed, updating screen dimensions")
		self.orientationState = orientationState

	def _startMagnifier(self) -> None:
		"""
		Start the magnifier
		"""
		if self._isActive:
			return
		# Check if screen curtain is active - if so, block magnifier from starting
		if screenCurtain.screenCurtain and screenCurtain.screenCurtain.enabled:
			log.debug("Screen curtain is active, cannot start magnifier")

			message = pgettext(
				"magnifier",
				# Translators: Message when trying to enable magnifier while screen curtain is active
				"Cannot enable magnifier: screen curtain is active. Please disable screen curtain first.",
			)
			ui.message(message, speechPriority=speech.priorities.Spri.NOW)
			return

		self._isActive = True
		self._currentCoordinates = self._getFocusCoordinates()

	def _updateMagnifier(self) -> None:
		"""
		Update the magnifier position and content
		"""
		if not self._isActive:
			return
		self._currentCoordinates = self._getFocusCoordinates()
		self._doUpdate()
		self._startTimer(self._updateMagnifier)

	def _doUpdate(self) -> None:
		"""
		Perform the actual update of the magnifier
		"""
		raise NotImplementedError("Subclasses must implement this method")

	def _stopMagnifier(self) -> None:
		"""
		Stop the magnifier
		"""
		if not self._isActive:
			return
		self._stopTimer()
		self._isActive = False
		# Unregister from display changes
		_displayTracking.displayChanged.unregister(self._onDisplayChanged)

	def onScreenCurtainEnabled(self) -> None:
		"""
		Called when screen curtain is being enabled.
		Handles disabling magnifier if it's active.
		"""
		if self._isActive:
			ui.message(
				pgettext(
					"magnifier",
					# Translators: Spoken message when magnifier is disabled due to screen curtain being enabled.
					"Magnifier is active, disabling it before enabling screen curtain",
				),
			)
			self._stopMagnifier()
			self._screenCurtainIsActive = True
		else:
			self._screenCurtainIsActive = False

	def onScreenCurtainDisabled(self) -> None:
		"""
		Called when screen curtain is being disabled.
		Handles re-enabling magnifier if it was active before screen curtain.
		"""
		if self._screenCurtainIsActive:
			ui.message(
				pgettext(
					"magnifier",
					# Translators: Spoken message when magnifier is re-enabled after screen curtain is disabled.
					"Magnifier was active before screen curtain, re-enabling it",
				),
			)
			self._startMagnifier()
			self._updateMagnifier()
			self._screenCurtainIsActive = False

	def _zoom(self, direction: Direction) -> None:
		"""
		Adjust the zoom level of the magnifier

		:param direction: Direction.IN to zoom in, Direction.OUT to zoom out
		"""
		if direction == Direction.IN:
			newZoom = self.zoomLevel + ZoomLevel.STEP_FACTOR
			if newZoom <= ZoomLevel.MAX_ZOOM:
				self.zoomLevel = newZoom
		elif direction == Direction.OUT:
			newZoom = self.zoomLevel - ZoomLevel.STEP_FACTOR
			if newZoom >= ZoomLevel.MIN_ZOOM:
				self.zoomLevel = newZoom

	def _startTimer(self, callback: Callable[[], None] = None) -> None:
		"""
		Start the timer with a callback function

		:param callback: The function to call when the timer expires
		"""
		self._stopTimer()
		self._timer = wx.Timer()
		self._timer.Bind(wx.EVT_TIMER, lambda evt: callback())
		self._timer.Start(self._TIMER_INTERVAL_MS, oneShot=True)

	def _stopTimer(self) -> None:
		"""
		Stop timer execution
		"""
		if self._timer:
			if self._timer.IsRunning():
				self._timer.Stop()
			self._timer = None
		else:
			log.debug("no timer to stop")

	def _getMagnifierPosition(self, coordinates: Coordinates) -> MagnifierPosition:
		"""
		Compute the top-left corner of the magnifier window centered on (x, y)

		:param coordinates: The (x, y) coordinates to center the magnifier on

		:return: The position and size of the magnifier window
		"""
		x, y = coordinates
		# Calculate the size of the capture area at the current zoom level
		visibleWidth = self._displayOrientation.width / self.zoomLevel
		visibleHeight = self._displayOrientation.height / self.zoomLevel

		# Compute the top-left corner so that (x, y) is at the center
		left = int(x - (visibleWidth / 2))
		top = int(y - (visibleHeight / 2))

		# Clamp to screen boundaries
		left = max(0, min(left, int(self._displayOrientation.width - visibleWidth)))
		top = max(0, min(top, int(self._displayOrientation.height - visibleHeight)))

		return MagnifierPosition(left, top, int(visibleWidth), int(visibleHeight))

	def _getCursorPosition(self) -> Coordinates:
		"""
		Get the current review position as (x, y), falling back to navigator object if needed
		Tries to get the review position from NVDA's API, or the center of the navigator object
		This part is taken from NVDA+shift+m gesture

		:return: The (x, y) coordinates of the NVDA position
		"""
		# Try to get the current review position object from NVDA's API
		reviewPosition = api.getReviewPosition()
		if reviewPosition:
			try:
				# Try to get the point at the start of the review position
				point = reviewPosition.pointAtStart
				return Coordinates(point.x, point.y)
			except (NotImplementedError, LookupError, AttributeError):
				# If that fails, fall through to try navigator object
				pass

		# Fallback: try to use the navigator object location
		navigatorObject = api.getNavigatorObject()
		try:
			# Try to get the bounding rectangle of the navigator object
			left, top, width, height = navigatorObject.location
			# Calculate the center point of the rectangle
			x = left + (width // 2)
			y = top + (height // 2)
			return Coordinates(x, y)
		except Exception:
			# If no location is found, log this and return (0, 0)
			return Coordinates(0, 0)

	def _getFocusCoordinates(self) -> Coordinates:
		"""
		Return position (x,y) of current focus element

		:return: The (x, y) coordinates of the focus element
		"""
		nvdaPosition = self._getCursorPosition()
		mousePosition = winUser.getCursorPos()
		# convert to Coordinates named tuple
		mousePosition = Coordinates(mousePosition[0], mousePosition[1])
		# Check if left mouse button is pressed
		isClickPressed = mouseHandler.isLeftMouseButtonLocked()

		# Always update positions in background (keep them synchronized)
		nvdaChanged = self._lastNVDAPosition != nvdaPosition
		mouseChanged = self._lastMousePosition != mousePosition

		if nvdaChanged:
			self._lastNVDAPosition = nvdaPosition
		if mouseChanged:
			self._lastMousePosition = mousePosition

		# During drag & drop, force focus on mouse
		if isClickPressed:
			self._lastFocusedObject = FocusType.MOUSE
			return mousePosition

		# Check mouse first (mouse has priority) - when not dragging
		if mouseChanged:
			self._lastFocusedObject = FocusType.MOUSE
			return mousePosition

		# Then check NVDA (only change focus if mouse didn't move)
		if nvdaChanged:
			self._lastFocusedObject = FocusType.NVDA
			return nvdaPosition

		# Return current position of the focused object (no changes detected)
		if self._lastFocusedObject == FocusType.NVDA:
			return nvdaPosition
		elif self._lastFocusedObject == FocusType.MOUSE:
			return mousePosition
		else:
			return mousePosition
