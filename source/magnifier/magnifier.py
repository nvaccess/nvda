# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from typing import Callable
from logHandler import log
import wx
import api
import winUser
import mouseHandler
from winAPI._displayTracking import getPrimaryDisplayOrientation

from .utils.types import MagnifierPosition, Coordinates, MagnifierType, Direction, FocusType, Filter

from .config import getDefaultZoomLevel, getDefaultFilter, ZoomLevel


class Magnifier:
	_ZOOM_MIN: float = ZoomLevel.MIN_ZOOM
	_ZOOM_MAX: float = ZoomLevel.MAX_ZOOM
	_ZOOM_STEP: float = ZoomLevel.STEP_FACTOR
	_TIMER_INTERVAL_MS: int = 20
	_MARGIN_BORDER: int = 50
	display = getPrimaryDisplayOrientation()
	_SCREEN_WIDTH: int = display.width
	_SCREEN_HEIGHT: int = display.height

	def __init__(self):
		self._magnifierType: MagnifierType = MagnifierType.FULLSCREEN
		self._isActive: bool = False
		self._zoomLevel: float = getDefaultZoomLevel()
		self._timer: None | wx.Timer = None
		self._lastFocusedObject: FocusType | None = None
		self._lastNVDAPosition: Coordinates = (0, 0)
		self._lastMousePosition: Coordinates = (0, 0)
		self._lastScreenPosition: Coordinates = (0, 0)
		self._currentCoordinates: Coordinates = (0, 0)
		self._filterType: Filter = getDefaultFilter()

	@property
	def isActive(self) -> bool:
		return self._isActive

	@isActive.setter
	def isActive(self, value: bool) -> None:
		self._isActive = value

	@property
	def magnifierType(self) -> MagnifierType:
		return self._magnifierType

	@magnifierType.setter
	def magnifierType(self, value: MagnifierType) -> None:
		self._magnifierType = value

	@property
	def zoomLevel(self) -> float:
		return self._zoomLevel

	@zoomLevel.setter
	def zoomLevel(self, value: float) -> None:
		self._zoomLevel = value

	@property
	def lastFocusedObject(self) -> FocusType | None:
		return self._lastFocusedObject

	@lastFocusedObject.setter
	def lastFocusedObject(self, value: FocusType | None) -> None:
		self._lastFocusedObject = value

	@property
	def lastNVDAPosition(self) -> Coordinates:
		return self._lastNVDAPosition

	@lastNVDAPosition.setter
	def lastNVDAPosition(self, value: Coordinates) -> None:
		self._lastNVDAPosition = value

	@property
	def lastMousePosition(self) -> Coordinates:
		return self._lastMousePosition

	@lastMousePosition.setter
	def lastMousePosition(self, value: Coordinates) -> None:
		self._lastMousePosition = value

	@property
	def lastScreenPosition(self) -> Coordinates:
		return self._lastScreenPosition

	@lastScreenPosition.setter
	def lastScreenPosition(self, value: Coordinates) -> None:
		self._lastScreenPosition = value

	@property
	def currentCoordinates(self) -> Coordinates:
		return self._currentCoordinates

	@currentCoordinates.setter
	def currentCoordinates(self, value: Coordinates) -> None:
		self._currentCoordinates = value

	@property
	def timer(self) -> wx.Timer | None:
		return self._timer

	@timer.setter
	def timer(self, value: wx.Timer | None) -> None:
		self._timer = value

	@property
	def filterType(self) -> Filter:
		return self._filterType

	@filterType.setter
	def filterType(self, value: Filter) -> None:
		self._filterType = value

	# Functions

	def _startMagnifier(self) -> None:
		"""
		Start the magnifier
		"""
		if self.isActive:
			return
		self.isActive = True
		self.currentCoordinates = self._getFocusCoordinates()

	def _updateMagnifier(self) -> None:
		"""
		Update the magnifier position and content
		"""
		if not self.isActive:
			return
		self.currentCoordinates = self._getFocusCoordinates()
		self._doUpdate()
		self._startTimer(self._updateMagnifier)

	def _doUpdate(self) -> None:
		"""
		Perform the actual update of the magnifier
		"""
		raise NotImplementedError("Subclasses must implement this method.")

	def _stopMagnifier(self) -> None:
		"""
		Stop the magnifier
		"""
		if not self.isActive:
			return
		self._stopTimer()
		self.isActive = False

	def _zoom(self, direction: Direction) -> None:
		"""
		Adjust the zoom level of the magnifier

		:param direction: Direction.IN to zoom in, Direction.OUT to zoom out
		"""
		if direction == Direction.IN:
			newZoom = self.zoomLevel + self._ZOOM_STEP
			if newZoom <= self._ZOOM_MAX:
				self.zoomLevel = newZoom
		elif direction == Direction.OUT:
			newZoom = self.zoomLevel - self._ZOOM_STEP
			if newZoom >= self._ZOOM_MIN:
				self.zoomLevel = newZoom

	def _startTimer(self, callback: Callable[[], None] = None) -> None:
		"""
		Start the timer with a callback function

		:param callback: The function to call when the timer expires
		"""
		self._stopTimer()
		self.timer = wx.Timer()
		self.timer.Bind(wx.EVT_TIMER, lambda evt: callback())
		self.timer.Start(self._TIMER_INTERVAL_MS, oneShot=True)

	def _stopTimer(self) -> None:
		"""
		Stop timer execution
		"""
		if self.timer:
			if self.timer.IsRunning():
				self.timer.Stop()
			self.timer = None
		else:
			log.info("no timer to stop")

	def _getMagnifierPosition(self, x: int, y: int) -> MagnifierPosition:
		"""
		Compute the top-left corner of the magnifier window centered on (x, y)

		:param x: Focus x
		:param y: Focus y

		Returns:
			magnifierPosition: The position and size of the magnifier window
		"""

		# Calculate the size of the capture area at the current zoom level
		visibleWidth = self._SCREEN_WIDTH / self.zoomLevel
		visibleHeight = self._SCREEN_HEIGHT / self.zoomLevel

		# Compute the top-left corner so that (x, y) is at the center
		left = int(x - (visibleWidth / 2))
		top = int(y - (visibleHeight / 2))

		# Clamp to screen boundaries
		left = max(0, min(left, int(self._SCREEN_WIDTH - visibleWidth)))
		top = max(0, min(top, int(self._SCREEN_HEIGHT - visibleHeight)))

		return MagnifierPosition(left, top, int(visibleWidth), int(visibleHeight))

	def _getCursorPosition(self) -> Coordinates:
		"""
		Get the current review position as (x, y), falling back to navigator object if needed
		Tries to get the review position from NVDA's API, or the center of the navigator object
		This part is taken from NVDA+shift+m gesture

		Returns:
			coordinates: The (x, y) coordinates of the NVDA position
		"""
		# Try to get the current review position object from NVDA's API
		reviewPosition = api.getReviewPosition()
		if reviewPosition:
			try:
				# Try to get the point at the start of the review position
				point = reviewPosition.pointAtStart
				return point.x, point.y
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
			return x, y
		except Exception:
			# If no location is found, log this and return (0, 0)
			return 0, 0

	def _getFocusCoordinates(self) -> Coordinates:
		"""
		Return position (x,y) of current focus element

		Returns:
			coordinates: The (x, y) coordinates of the focus element
		"""
		nvdaPosition = self._getCursorPosition()
		mousePosition = winUser.getCursorPos()
		# Check if left mouse button is pressed
		isClickPressed = mouseHandler.isLeftMouseButtonLocked()

		# Always update positions in background (keep them synchronized)
		nvdaChanged = self.lastNVDAPosition != nvdaPosition
		mouseChanged = self.lastMousePosition != mousePosition

		if nvdaChanged:
			self.lastNVDAPosition = nvdaPosition
		if mouseChanged:
			self.lastMousePosition = mousePosition

		# During drag & drop, force focus on mouse
		if isClickPressed:
			self.lastFocusedObject = FocusType.MOUSE
			return mousePosition

		# Check mouse first (mouse has priority) - when not dragging
		if mouseChanged:
			self.lastFocusedObject = FocusType.MOUSE
			return mousePosition

		# Then check NVDA (only change focus if mouse didn't move)
		if nvdaChanged:
			self.lastFocusedObject = FocusType.NVDA
			return nvdaPosition

		# Return current position of the focused object (no changes detected)
		if self.lastFocusedObject == FocusType.NVDA:
			return nvdaPosition
		elif self.lastFocusedObject == FocusType.MOUSE:
			return mousePosition
		else:
			return mousePosition
