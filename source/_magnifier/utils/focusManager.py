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
from .types import Coordinates, MagnifierFollowFocusType
from ..config import getFollowState


class FocusManager:
	"""
	Manages focus tracking for the magnifier.
	Tracks mouse, system focus, and navigator object positions.
	"""

	_SYSTEM_FOCUS_STICKINESS_SECONDS: float = 0.12

	def __init__(self):
		"""Initialize the focus manager."""
		self._lastFocusedObject: MagnifierFollowFocusType | None = None
		self._lastMousePosition = Coordinates(0, 0)
		self._lastSystemFocusPosition = Coordinates(0, 0)
		self._lastReviewPosition: Coordinates | None = None
		self._lastNavigatorObjectPosition = Coordinates(0, 0)
		self._lastValidSystemFocusPosition = Coordinates(0, 0)
		self._lastValidReviewPosition = Coordinates(0, 0)
		self._lastValidNavigatorObjectPosition = Coordinates(0, 0)
		self._lastSystemFocusChangeTime: float = 0.0

	def getCurrentFocusCoordinates(self) -> Coordinates:
		"""
		Get the current focus coordinates based on priority.
		Priority: Mouse (drag) > Mouse > System Focus > Review > Navigator Object.
		Special case: when both the system focus and navigator object change simultaneously
		but the review cursor does not (e.g. table cell navigation via numpad), the navigator
		object takes priority over system focus.

		Each source is only considered when its corresponding setting is enabled.

		:return: The (x, y) coordinates of the current focus
		"""
		now = time.monotonic()

		mousePosition = self._getMousePosition()
		systemFocusPosition = self._getSystemFocusPosition()
		reviewPosition = self._getReviewPosition()
		navigatorPosition = self._getNavigatorObjectPosition()
		isClickPressed = mouseHandler.isLeftMouseButtonLocked()

		# Cache settings once — each call reads from config.conf
		isFollowMouse = getFollowState(MagnifierFollowFocusType.MOUSE)
		isFollowSystemFocus = getFollowState(MagnifierFollowFocusType.SYSTEM_FOCUS)
		isFollowReviewCursor = getFollowState(MagnifierFollowFocusType.REVIEW)
		isFollowNavigatorObject = getFollowState(MagnifierFollowFocusType.NAVIGATOR_OBJECT)

		mouseChanged = self._lastMousePosition != mousePosition
		systemFocusChanged = self._lastSystemFocusPosition != systemFocusPosition
		reviewChanged = reviewPosition is not None and self._lastReviewPosition != reviewPosition
		navigatorChanged = self._lastNavigatorObjectPosition != navigatorPosition

		# Update tracked positions
		if mouseChanged:
			self._lastMousePosition = mousePosition
		if systemFocusChanged:
			self._lastSystemFocusPosition = systemFocusPosition
			self._lastSystemFocusChangeTime = now
		if reviewChanged:
			self._lastReviewPosition = reviewPosition
		if navigatorChanged:
			self._lastNavigatorObjectPosition = navigatorPosition

		# Priority 1: Mouse — drag (fires even when stationary) or movement
		if (isClickPressed or mouseChanged) and isFollowMouse:
			self._lastFocusedObject = MagnifierFollowFocusType.MOUSE
			return mousePosition

		# Special case: table cell navigation (numpad).
		# When both the system focus and the navigator object change simultaneously but the
		# review cursor does not, the navigator object reflects the user's explicit navigation
		# intent and therefore takes priority over the system focus.
		if navigatorChanged and systemFocusChanged and not reviewChanged and isFollowNavigatorObject:
			self._lastFocusedObject = MagnifierFollowFocusType.NAVIGATOR_OBJECT
			return navigatorPosition

		# Priority 2: System focus (focus object + browse mode cursor)
		if systemFocusChanged and isFollowSystemFocus:
			self._lastFocusedObject = MagnifierFollowFocusType.SYSTEM_FOCUS
			return systemFocusPosition

		# Priority 3: Review cursor
		if reviewChanged and isFollowReviewCursor and reviewPosition is not None:
			self._lastFocusedObject = MagnifierFollowFocusType.REVIEW
			return reviewPosition

		# Priority 4: Navigator object (NumPad navigation)
		if navigatorChanged and isFollowNavigatorObject:
			self._lastFocusedObject = MagnifierFollowFocusType.NAVIGATOR_OBJECT
			return navigatorPosition

		# Resolve the effective review position once (fallback to last valid when None)
		reviewEffectivePosition = (
			reviewPosition if reviewPosition is not None else self._lastValidReviewPosition
		)

		# All sources in priority order
		_sources = (
			(MagnifierFollowFocusType.MOUSE, isFollowMouse, mousePosition),
			(MagnifierFollowFocusType.SYSTEM_FOCUS, isFollowSystemFocus, systemFocusPosition),
			(MagnifierFollowFocusType.REVIEW, isFollowReviewCursor, reviewEffectivePosition),
			(MagnifierFollowFocusType.NAVIGATOR_OBJECT, isFollowNavigatorObject, navigatorPosition),
		)

		# Keep current source if still enabled; otherwise mark it as NONE so we switch
		for focusType, isEnabled, position in _sources:
			if self._lastFocusedObject == focusType:
				if isEnabled:
					return position
				self._lastFocusedObject = None
				break

		# No active source – switch to the highest-priority enabled source
		for focusType, isEnabled, position in _sources:
			if isEnabled:
				self._lastFocusedObject = focusType
				return position

		# All sources disabled – return mouse position without changing focus state
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
		Get the current review cursor position.

		:return: The (x, y) coordinates of the review cursor, or ``None`` if not available.
		"""
		reviewPosition = api.getReviewPosition()
		if reviewPosition:
			try:
				point = self._getPointAtStart(reviewPosition)
				coords = Coordinates(point.x, point.y)
				if coords != Coordinates(0, 0):
					self._lastValidReviewPosition = coords
				return coords
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

		Updates :attr:`_lastValidNavigatorObjectPosition` when a valid position is obtained.

		:return: The (x, y) coordinates of the navigator object center,
			or the last valid position as fallback.
		"""
		position = self._getNavigatorObjectLocation()
		if position and position != Coordinates(0, 0):
			self._lastValidNavigatorObjectPosition = position
			return position
		return self._lastValidNavigatorObjectPosition

	def getLastFocusType(self) -> MagnifierFollowFocusType | None:
		"""
		Get the type of the last focused object.

		:return: The type of the last focused object, or None when no focus source is active.
		"""
		return self._lastFocusedObject

	def updateFollowedFocus(self) -> None:
		"""
		Force an update of the magnifier focus based on current settings.
		Called after toggling follow settings to immediately apply changes.
		"""
		self._lastFocusedObject = None  # Reset to force re-evaluation of focus
		self.getCurrentFocusCoordinates()
