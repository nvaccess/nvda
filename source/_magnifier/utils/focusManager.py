# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Focus Manager for the magnifier module.
Handles all focus tracking logic and coordinate calculations.
"""

import api
import winUser
import mouseHandler
from .types import Coordinates, FocusType
from ..config import followMouse, followReviewCursor, followSystemFocus, followNavigatorObject


class FocusManager:
	"""
	Manages focus tracking for the magnifier.
	Tracks mouse, system focus, and navigator object positions.
	"""

	def __init__(self):
		"""Initialize the focus manager."""
		self._lastFocusedObject: FocusType | None = None
		self._lastMousePosition = Coordinates(0, 0)
		self._lastSystemFocusPosition = Coordinates(0, 0)
		self._lastReviewPosition: Coordinates | None = None
		self._lastNavigatorObjectPosition = Coordinates(0, 0)
		self._lastValidSystemFocusPosition = Coordinates(0, 0)
		self._lastValidReviewPosition = Coordinates(0, 0)
		self._lastValidNavigatorObjectPosition = Coordinates(0, 0)

	def getCurrentFocusCoordinates(self) -> Coordinates:
		"""
		Get the current focus coordinates based on priority.
		Priority: Mouse (drag) > Mouse > System Focus > Review > Navigator Object

		Each source is only considered when its corresponding setting is enabled.

		:return: The (x, y) coordinates of the current focus
		"""
		mousePosition = self._getMousePosition()
		systemFocusPosition = self._getSystemFocusPosition()
		reviewPosition = self._getReviewPosition()
		navigatorPosition = self._getNavigatorObjectPosition()
		isClickPressed = mouseHandler.isLeftMouseButtonLocked()

		mouseChanged = self._lastMousePosition != mousePosition
		systemFocusChanged = self._lastSystemFocusPosition != systemFocusPosition
		reviewChanged = reviewPosition is not None and self._lastReviewPosition != reviewPosition
		navigatorChanged = self._lastNavigatorObjectPosition != navigatorPosition

		# Update tracked positions
		if mouseChanged:
			self._lastMousePosition = mousePosition
		if systemFocusChanged:
			self._lastSystemFocusPosition = systemFocusPosition
		if reviewChanged:
			self._lastReviewPosition = reviewPosition
		if navigatorChanged:
			self._lastNavigatorObjectPosition = navigatorPosition

		# Priority 1: Mouse during drag & drop
		if isClickPressed and followMouse():
			self._lastFocusedObject = FocusType.MOUSE
			return mousePosition

		# Priority 2: Mouse movement
		if mouseChanged and followMouse():
			self._lastFocusedObject = FocusType.MOUSE
			return mousePosition

		# Priority 3: System focus (focus object + browse mode cursor)
		if systemFocusChanged and followSystemFocus():
			self._lastFocusedObject = FocusType.SYSTEM_FOCUS
			return systemFocusPosition

		# Priority 4: Review cursor
		if reviewChanged and followReviewCursor() and reviewPosition is not None:
			self._lastFocusedObject = FocusType.REVIEW
			return reviewPosition

		# Priority 5: Navigator object (NumPad navigation)
		if navigatorChanged and followNavigatorObject():
			self._lastFocusedObject = FocusType.NAVIGATOR
			return navigatorPosition

		# No changes detected – return last focused position
		match self._lastFocusedObject:
			case FocusType.MOUSE:
				return mousePosition
			case FocusType.SYSTEM_FOCUS:
				return systemFocusPosition
			case FocusType.REVIEW:
				return reviewPosition if reviewPosition is not None else self._lastValidReviewPosition
			case FocusType.NAVIGATOR:
				return navigatorPosition
			case _:
				# Default to mouse if no previous focus
				return mousePosition

	def _getMousePosition(self) -> Coordinates:
		"""
		Get the current mouse position.

		:return: The (x, y) coordinates of the mouse
		"""
		mousePos = winUser.getCursorPos()
		return Coordinates(mousePos[0], mousePos[1])

	def _getSystemFocusPosition(self) -> Coordinates:
		"""
		Get the current system focus position (focus object + browse mode cursor).
		This includes both the system focus and the browse mode cursor if active.

		:return: The (x, y) coordinates of the system focus position
		"""
		try:
			# Get caret position (works for both browse mode and regular focus)
			caretPosition = api.getCaretPosition()
			point = caretPosition.pointAtStart
			coords = Coordinates(point.x, point.y)
			# Store as last valid position if not (0, 0)
			if coords != Coordinates(0, 0):
				self._lastValidSystemFocusPosition = coords
			return coords
		except (NotImplementedError, LookupError, AttributeError, RuntimeError):
			# Fallback: use focus object location
			try:
				focusObj = api.getFocusObject()
				if focusObj and focusObj.location:
					left, top, width, height = focusObj.location
					x = left + (width // 2)
					y = top + (height // 2)
					coords = Coordinates(x, y)
					if coords != Coordinates(0, 0):
						self._lastValidSystemFocusPosition = coords
					return coords
			except Exception:
				# Focus object location may fail (e.g., object without location)
				# Fall through to return last valid position
				pass
		return self._lastValidSystemFocusPosition

	def _getReviewPosition(self) -> Coordinates | None:
		"""
		Get the current review cursor position.

		:return: The (x, y) coordinates of the review cursor, or ``None`` if not available.
		"""
		reviewPosition = api.getReviewPosition()
		if reviewPosition:
			try:
				point = reviewPosition.pointAtStart
				coords = Coordinates(point.x, point.y)
				if coords != Coordinates(0, 0):
					self._lastValidReviewPosition = coords
				return coords
			except (NotImplementedError, LookupError, AttributeError):
				pass
		return None

	def _getNavigatorObjectLocation(self) -> Coordinates | None:
		"""
		Get the navigator object location from its bounding rectangle.

		:return: The (x, y) coordinates of the navigator object center, or None if not available
		"""
		navigatorObject = api.getNavigatorObject()
		if navigatorObject:
			try:
				left, top, width, height = navigatorObject.location
				x = left + (width // 2)
				y = top + (height // 2)
				return Coordinates(x, y)
			except Exception:
				# Navigator object may not have a valid location
				pass
		return None

	def _getNavigatorObjectPosition(self) -> Coordinates:
		"""
		Get the navigator object position (NumPad navigation).

		Updates :attr:`_lastValidNavigatorObjectPosition` when a valid position is obtained.

		:return: The (x, y) coordinates of the navigator object center,
			or the last valid position as fallback.
		"""
		position = self._getNavigatorObjectLocation()
		if position and position != Coordinates(0, 0):
			self._lastValidNavigatorObjectPosition = position
			return position
		return self._lastValidNavigatorObjectPosition

	def getLastFocusType(self) -> FocusType | None:
		"""
		Get the type of the last focused object.

		:return: The type of the last focused object
		"""
		return self._lastFocusedObject

	def updateFollowedFocus(self) -> None:
		"""
		Force an update of the magnifier focus based on current settings.
		Called after toggling follow settings to immediately apply changes.
		"""
		self._lastFocusedObject = None  # Reset to force re-evaluation of focus
		self.getCurrentFocusCoordinates()
