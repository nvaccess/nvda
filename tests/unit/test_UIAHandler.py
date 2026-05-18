# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited

"""Unit tests for the UIAHandler hung-window guards.

These cover the mechanism that stops an unresponsive application from making NVDA
itself unresponsive or flooding the log with COMError tracebacks out of the UIA
event handlers.
"""

from unittest import TestCase
from unittest.mock import patch

from comtypes import COMError

import config
import winUser
from UIAHandler import _catchUIAEventHandlerCOMError
from UIAHandler import utils


def _makeCOMError() -> COMError:
	# Mirrors the error seen when an unresponsive application's element is accessed:
	# (-2147220991, 'An event was unable to invoke any of the subscribers', ...)
	return COMError(
		-2147220991, "An event was unable to invoke any of the subscribers", (None, None, None, 0, None)
	)


class _FakeElement:
	"""Stand-in for an IUIAutomationElement event sender."""

	def __init__(self, cachedHandle=0, raiseOnCached=False):
		self._cachedHandle = cachedHandle
		self._raiseOnCached = raiseOnCached

	@property
	def cachedNativeWindowHandle(self):
		if self._raiseOnCached:
			raise _makeCOMError()
		return self._cachedHandle

	@property
	def currentNativeWindowHandle(self):
		raise AssertionError(
			"The hung-window guard must never read a live (current) property, "
			"as that is exactly the call that hangs on an unresponsive application.",
		)


class Test_getCachedWindowHandleFromEvent(TestCase):
	def test_returnsHandle(self):
		self.assertEqual(
			utils._getCachedWindowHandleFromEvent(_FakeElement(cachedHandle=1234)),
			1234,
		)

	def test_noHandleReturnsNone(self):
		self.assertIsNone(utils._getCachedWindowHandleFromEvent(_FakeElement(cachedHandle=0)))

	def test_comErrorReturnsNone(self):
		# Must swallow the COMError rather than propagate, and must not fall back
		# to the live property (which _FakeElement asserts against).
		self.assertIsNone(utils._getCachedWindowHandleFromEvent(_FakeElement(raiseOnCached=True)))


class Test_shouldSkipEventForHungWindow(TestCase):
	def setUp(self):
		self._origSetting = config.conf["UIA"]["ignoreHungWindowEvents"]

	def tearDown(self):
		config.conf["UIA"]["ignoreHungWindowEvents"] = self._origSetting

	def test_disabledByConfig(self):
		config.conf["UIA"]["ignoreHungWindowEvents"] = False
		with patch.object(winUser, "isHungAppWindow", side_effect=AssertionError("must not be called")):
			self.assertFalse(utils._shouldSkipEventForHungWindow(_FakeElement(cachedHandle=1)))

	def test_noWindowHandleIsNotSkipped(self):
		config.conf["UIA"]["ignoreHungWindowEvents"] = True
		with patch.object(winUser, "isHungAppWindow", side_effect=AssertionError("must not be called")):
			self.assertFalse(utils._shouldSkipEventForHungWindow(_FakeElement(cachedHandle=0)))

	def test_hungWindowIsSkipped(self):
		config.conf["UIA"]["ignoreHungWindowEvents"] = True
		with patch.object(winUser, "isHungAppWindow", return_value=True):
			self.assertTrue(utils._shouldSkipEventForHungWindow(_FakeElement(cachedHandle=1)))

	def test_respondingWindowIsNotSkipped(self):
		config.conf["UIA"]["ignoreHungWindowEvents"] = True
		with patch.object(winUser, "isHungAppWindow", return_value=False):
			self.assertFalse(utils._shouldSkipEventForHungWindow(_FakeElement(cachedHandle=1)))

	def test_guardNeverRaises(self):
		config.conf["UIA"]["ignoreHungWindowEvents"] = True
		with patch.object(winUser, "isHungAppWindow", side_effect=RuntimeError("boom")):
			# A failure inside the guard itself must never escape into the COM handler.
			self.assertFalse(utils._shouldSkipEventForHungWindow(_FakeElement(cachedHandle=1)))


class Test_catchUIAEventHandlerCOMError(TestCase):
	def test_comErrorIsSwallowed(self):
		class Handler:
			@_catchUIAEventHandlerCOMError
			def IUIAutomationEventHandler_HandleAutomationEvent(self, sender, eventID):
				raise _makeCOMError()

		# Must not raise: this is what stops the flood out through comtypes.
		self.assertIsNone(Handler().IUIAutomationEventHandler_HandleAutomationEvent(object(), 0))

	def test_returnValueIsPreserved(self):
		class Handler:
			@_catchUIAEventHandlerCOMError
			def IUIAutomationEventHandler_HandleAutomationEvent(self, sender, eventID):
				return "ok"

		self.assertEqual(
			Handler().IUIAutomationEventHandler_HandleAutomationEvent(object(), 0),
			"ok",
		)

	def test_nonCOMErrorStillRaises(self):
		class Handler:
			@_catchUIAEventHandlerCOMError
			def IUIAutomationEventHandler_HandleAutomationEvent(self, sender, eventID):
				raise ValueError("real bug")

		# Only COMError is a safety-net concern; genuine bugs must not be hidden.
		with self.assertRaises(ValueError):
			Handler().IUIAutomationEventHandler_HandleAutomationEvent(object(), 0)
