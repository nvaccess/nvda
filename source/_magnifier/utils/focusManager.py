# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Focus Manager for the magnifier module.
Handles all focus tracking logic and coordinate calculations.
"""

from logHandler import log
import api
import winUser
import mouseHandler
import time
import locationHelper
import textInfos
from textInfos.offsets import OffsetsTextInfo
from .types import Coordinates, FocusType


class FocusManager:
	"""
	Manages focus tracking for the magnifier.
	Tracks mouse, system focus, and navigator object positions.
	"""

	_SYSTEM_FOCUS_STICKINESS_SECONDS: float = 0.12

	def __init__(self):
		"""Initialize the focus manager."""
		self._lastFocusedObject: FocusType | None = None
		self._lastMousePosition = Coordinates(0, 0)
		self._lastSystemFocusPosition = Coordinates(0, 0)
		self._lastNavigatorObjectPosition = Coordinates(0, 0)
		self._lastValidSystemFocusPosition = Coordinates(0, 0)
		self._lastValidNavigatorObjectPosition = Coordinates(0, 0)
		self._lastSystemFocusChangeTime: float = 0.0

	def getCurrentFocusCoordinates(self) -> Coordinates:
		"""
		Get the current focus coordinates based on priority.
		Priority: Mouse > Navigator Object > System Focus

		:return: The (x, y) coordinates of the current focus
		"""
		now = time.monotonic()

		# Get all three positions
		systemFocusPosition = self._getSystemFocusPosition()
		navigatorObjectPosition = self._getNavigatorObjectPosition()
		mousePosition = self._getMousePosition()

		# Check if left mouse button is pressed
		isClickPressed = mouseHandler.isLeftMouseButtonLocked()

		# Track which positions have changed
		systemFocusChanged = self._lastSystemFocusPosition != systemFocusPosition
		navigatorObjectChanged = self._lastNavigatorObjectPosition != navigatorObjectPosition
		mouseChanged = self._lastMousePosition != mousePosition

		# Update last positions
		if systemFocusChanged:
			self._lastSystemFocusPosition = systemFocusPosition
			self._lastSystemFocusChangeTime = now
		if navigatorObjectChanged:
			self._lastNavigatorObjectPosition = navigatorObjectPosition
		if mouseChanged:
			self._lastMousePosition = mousePosition

		# Priority 1: Mouse during drag & drop
		if isClickPressed:
			self._lastFocusedObject = FocusType.MOUSE
			return mousePosition

		# Priority 2: Mouse movement (when not dragging)
		if mouseChanged:
			self._lastFocusedObject = FocusType.MOUSE
			return mousePosition

		# Priority 3: Navigator object – but only when it represents a genuinely independent movement.
		if navigatorObjectChanged:
			# If system focus just changed and we were already tracking it, keep system focus
			# briefly to avoid visible oscillation while editing text.
			if (
				self._lastFocusedObject == FocusType.SYSTEM_FOCUS
				and now - self._lastSystemFocusChangeTime <= self._SYSTEM_FOCUS_STICKINESS_SECONDS
			):
				return systemFocusPosition

			# If both navigator and system focus changed but ended up at the same
			# coordinates, treat this as ordinary system-focus navigation.
			# This avoids marking normal focus/caret movement as NAVIGATOR when
			# the review cursor is merely following focus/caret.
			if systemFocusChanged and navigatorObjectPosition == systemFocusPosition:
				# Navigator followed focus/caret – behave as a system-focus event.
				self._lastFocusedObject = FocusType.SYSTEM_FOCUS
				return systemFocusPosition
			self._lastFocusedObject = FocusType.NAVIGATOR
			return navigatorObjectPosition

		# Priority 4: System focus (Tab, plain focus changes, browse-mode caret).
		# Reached when only the system-focus position changed without a corresponding
		# navigator change
		if systemFocusChanged:
			self._lastFocusedObject = FocusType.SYSTEM_FOCUS
			return systemFocusPosition

		# No changes detected - return last focused position
		match self._lastFocusedObject:
			case FocusType.MOUSE:
				return mousePosition
			case FocusType.SYSTEM_FOCUS:
				return systemFocusPosition
			case FocusType.NAVIGATOR:
				return navigatorObjectPosition
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
			point = self._getPointAtStart(caretPosition)
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
		Get the current review position (review cursor).

		:return: The (x, y) coordinates of the review position, or None if not available
		"""
		reviewPosition = api.getReviewPosition()
		if reviewPosition:
			try:
				point = self._getPointAtStart(reviewPosition)
				return Coordinates(point.x, point.y)
			except (NotImplementedError, LookupError, AttributeError):
				# Review position may not support pointAtStart
				pass
		return None

	def _getPointAtStart(self, textInfo: textInfos.TextInfo) -> locationHelper.Point:
		"""
		Get a point for the start of a text range with a local end-of-text fallback.

		When a collapsed TextInfo is positioned at an exclusive end offset, use the
		right edge of the previous character if available. This keeps the workaround
		local to the magnifier instead of changing TextInfo behavior globally.
		"""
		try:
			return textInfo.pointAtStart
		except (NotImplementedError, LookupError, AttributeError) as e:
			log.debug(f"pointAtStart failed for {textInfo!r}: {e}", exc_info=True)
			originalExc = e

		# Only apply the fallback for TextInfos exposing the offset-based internals
		# we need. Otherwise, preserve the original failure.
		if not (isinstance(textInfo, OffsetsTextInfo) and textInfo.isCollapsed and textInfo._startOffset > 0):
			raise originalExc

		prevOffset = textInfo._startOffset - 1
		try:
			return textInfo._getBoundingRectFromOffset(prevOffset).topRight
		except (NotImplementedError, LookupError, AttributeError) as e:
			log.debug(f"_getBoundingRectFromOffset failed: {e}", exc_info=True)
			try:
				return textInfo._getPointFromOffset(prevOffset)
			except (NotImplementedError, LookupError, AttributeError) as e:
				log.debug(f"_getPointFromOffset failed: {e}", exc_info=True)
		raise originalExc

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
		Tries review position first, then navigator object location.

		:return: The (x, y) coordinates of the navigator object
		"""
		# Try review position first
		position = self._getReviewPosition()
		if position and position != Coordinates(0, 0):
			self._lastValidNavigatorObjectPosition = position
			return position

		# Fallback: use navigator object location
		position = self._getNavigatorObjectLocation()
		if position and position != Coordinates(0, 0):
			self._lastValidNavigatorObjectPosition = position
			return position

		# Return last valid navigator object position instead of (0, 0)
		return self._lastValidNavigatorObjectPosition

	def getLastFocusType(self) -> FocusType | None:
		"""
		Get the type of the last focused object.

		:return: The type of the last focused object
		"""
		return self._lastFocusedObject
