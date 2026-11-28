# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, nibarAhmed
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Tests for dropping stale IAccessible focus events when a same-process UIA element still holds focus."""

import unittest
from types import SimpleNamespace
from unittest.mock import patch

import eventHandler
import IAccessibleHandler
import NVDAObjects.IAccessible
import NVDAObjects.UIA
import UIAHandler
from comtypes import COMError


def _makeIAccessible(
	processID: int = 1234,
	windowClassName: str = "Chrome_RenderWidgetHostHWND",
	shouldAllowFocus: bool = True,
	onCheckShouldAllowFocus=None,
) -> NVDAObjects.IAccessible.IAccessible:
	"""Create a minimal IAccessible instance without invoking COM initialization."""
	if onCheckShouldAllowFocus is not None:

		class _DynamicIAccessible(NVDAObjects.IAccessible.IAccessible):
			@property
			def shouldAllowIAccessibleFocusEvent(self) -> bool:
				return onCheckShouldAllowFocus()

		obj = object.__new__(_DynamicIAccessible)
	else:
		obj = object.__new__(NVDAObjects.IAccessible.IAccessible)
		obj.shouldAllowIAccessibleFocusEvent = shouldAllowFocus
	obj.processID = processID
	obj.windowClassName = windowClassName
	return obj


def _makeUIAFocus(
	processID: int = 1234,
	hasKeyboardFocus: bool | Exception = True,
) -> NVDAObjects.UIA.UIA:
	"""Create a minimal UIA instance with configurable keyboard focus state."""
	obj = object.__new__(NVDAObjects.UIA.UIA)
	obj.processID = processID
	if isinstance(hasKeyboardFocus, Exception):

		class _FailingElement:
			@property
			def currentHasKeyboardFocus(self) -> bool:
				raise hasKeyboardFocus

		obj.UIAElement = _FailingElement()
	else:
		obj.UIAElement = SimpleNamespace(currentHasKeyboardFocus=hasKeyboardFocus)
	return obj


class TestProcessFocusNVDAEventWithUIAFocus(unittest.TestCase):
	def test_dropsIAccessibleFocusWhenSameProcessUIAStillHasKeyboardFocus(self) -> None:
		iaObj = _makeIAccessible(processID=1234)
		uiaFocus = _makeUIAFocus(processID=1234, hasKeyboardFocus=True)
		with (
			patch.object(UIAHandler, "handler", object()),
			patch.object(eventHandler, "lastQueuedFocusObject", uiaFocus),
			patch.object(eventHandler, "queueEvent") as queueEvent,
		):
			result = IAccessibleHandler.processFocusNVDAEvent(iaObj)
		self.assertFalse(result)
		queueEvent.assert_not_called()

	def test_dropsIAccessibleFocusWhenUIAFocusQueuedDuringShouldAllowCheck(self) -> None:
		uiaFocus = _makeUIAFocus(processID=1234, hasKeyboardFocus=True)

		def _simulateUIARace() -> bool:
			eventHandler.lastQueuedFocusObject = uiaFocus
			return True

		iaObj = _makeIAccessible(processID=1234, onCheckShouldAllowFocus=_simulateUIARace)
		with (
			patch.object(UIAHandler, "handler", object()),
			patch.object(eventHandler, "lastQueuedFocusObject", None),
			patch.object(eventHandler, "queueEvent") as queueEvent,
		):
			result = IAccessibleHandler.processFocusNVDAEvent(iaObj)
		self.assertFalse(result)
		queueEvent.assert_not_called()

	def test_allowsIAccessibleFocusWhenSameProcessUIALostKeyboardFocus(self) -> None:
		iaObj = _makeIAccessible(processID=1234)
		uiaFocus = _makeUIAFocus(processID=1234, hasKeyboardFocus=False)
		with (
			patch.object(UIAHandler, "handler", object()),
			patch.object(eventHandler, "lastQueuedFocusObject", uiaFocus),
			patch.object(eventHandler, "queueEvent") as queueEvent,
		):
			result = IAccessibleHandler.processFocusNVDAEvent(iaObj)
		self.assertTrue(result)
		queueEvent.assert_called_once_with("gainFocus", iaObj)

	def test_allowsIAccessibleFocusWhenUIAFocusElementRaisesCOMError(self) -> None:
		iaObj = _makeIAccessible(processID=1234)
		uiaFocus = _makeUIAFocus(
			processID=1234,
			hasKeyboardFocus=COMError(-2147220991, "Element not available", (None, None, None, 0, None)),
		)
		with (
			patch.object(UIAHandler, "handler", object()),
			patch.object(eventHandler, "lastQueuedFocusObject", uiaFocus),
			patch.object(eventHandler, "queueEvent") as queueEvent,
		):
			result = IAccessibleHandler.processFocusNVDAEvent(iaObj)
		self.assertTrue(result)
		queueEvent.assert_called_once_with("gainFocus", iaObj)

	def test_allowsIAccessibleFocusWhenUIAFocusIsInDifferentProcess(self) -> None:
		iaObj = _makeIAccessible(processID=1234)
		uiaFocus = _makeUIAFocus(processID=5678, hasKeyboardFocus=True)
		with (
			patch.object(UIAHandler, "handler", object()),
			patch.object(eventHandler, "lastQueuedFocusObject", uiaFocus),
			patch.object(eventHandler, "queueEvent") as queueEvent,
		):
			result = IAccessibleHandler.processFocusNVDAEvent(iaObj)
		self.assertTrue(result)
		queueEvent.assert_called_once_with("gainFocus", iaObj)

	def test_allowsNonChromiumIAccessibleFocusWhenSameProcessUIAHasKeyboardFocus(self) -> None:
		iaObj = _makeIAccessible(processID=1234, windowClassName="#32768")
		uiaFocus = _makeUIAFocus(processID=1234, hasKeyboardFocus=True)
		with (
			patch.object(UIAHandler, "handler", object()),
			patch.object(eventHandler, "lastQueuedFocusObject", uiaFocus),
			patch.object(eventHandler, "queueEvent") as queueEvent,
		):
			result = IAccessibleHandler.processFocusNVDAEvent(iaObj)
		self.assertTrue(result)
		queueEvent.assert_called_once_with("gainFocus", iaObj)

	def test_allowsForcedIAccessibleFocusEvenWhenUIAHasKeyboardFocus(self) -> None:
		iaObj = _makeIAccessible(processID=1234)
		uiaFocus = _makeUIAFocus(processID=1234, hasKeyboardFocus=True)
		with (
			patch.object(UIAHandler, "handler", object()),
			patch.object(eventHandler, "lastQueuedFocusObject", uiaFocus),
			patch.object(eventHandler, "queueEvent") as queueEvent,
		):
			result = IAccessibleHandler.processFocusNVDAEvent(iaObj, force=True)
		self.assertTrue(result)
		queueEvent.assert_called_once_with("gainFocus", iaObj)

	def test_allowsIAccessibleFocusWhenUIAHandlerIsNone(self) -> None:
		iaObj = _makeIAccessible(processID=1234)
		uiaFocus = _makeUIAFocus(processID=1234, hasKeyboardFocus=True)
		with (
			patch.object(UIAHandler, "handler", None),
			patch.object(eventHandler, "lastQueuedFocusObject", uiaFocus),
			patch.object(eventHandler, "queueEvent") as queueEvent,
		):
			result = IAccessibleHandler.processFocusNVDAEvent(iaObj)
		self.assertTrue(result)
		queueEvent.assert_called_once_with("gainFocus", iaObj)
