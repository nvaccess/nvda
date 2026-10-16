# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter, Tobias Heath
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file:
# https://github.com/nvaccess/nvda/blob/master/copying.txt


"""Unit tests for the UIAHandler hung-window guard.

These cover the mechanism that drops UIA events from a not-responding
application so it cannot freeze NVDA or flood the log.
"""

from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import MagicMock, patch

import exceptions
import textInfos
import UIAHandler
import winUser
from comtypes import COMError
from UIAHandler import NVDAUnitsToUIAUnits, getUIAUnitFromNVDAUnit, utils


def _makeCOMError() -> COMError:
	# Mirrors the error seen when an unresponsive application's element is accessed:
	# (-2147220991, 'An event was unable to invoke any of the subscribers', ...)
	return COMError(
		-2147220991,
		"An event was unable to invoke any of the subscribers",
		(None, None, None, 0, None),
	)


class _FakeElement:
	"""Stand-in for an IUIAutomationElement event sender."""

	def __init__(self, cachedHandle: int = 0, raiseOnCached: bool = False) -> None:
		self._cachedHandle = cachedHandle
		self._raiseOnCached = raiseOnCached

	@property
	def cachedNativeWindowHandle(self) -> int:
		if self._raiseOnCached:
			raise _makeCOMError()
		return self._cachedHandle

	@property
	def currentNativeWindowHandle(self):
		raise AssertionError(
			"The hung-window guard must never read a live (current) property, "
			"as that is exactly the call that hangs on an unresponsive application.",
		)


class Test_getUIAUnitFromNVDAUnit(TestCase):
	def test_mappedUnitReturnsUIAUnit(self):
		self.assertEqual(
			getUIAUnitFromNVDAUnit(textInfos.UNIT_WORD),
			NVDAUnitsToUIAUnits[textInfos.UNIT_WORD],
		)

	def test_unmappedUnitRaisesNotImplementedError(self):
		with self.assertRaises(NotImplementedError):
			getUIAUnitFromNVDAUnit(textInfos.UNIT_SENTENCE)


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
	def test_noWindowHandleIsNotSkipped(self):
		with patch.object(winUser, "isHungAppWindow", side_effect=AssertionError("must not be called")):
			self.assertFalse(utils._shouldSkipEventForHungWindow(_FakeElement(cachedHandle=0)))

	def test_hungWindowIsSkipped(self):
		with patch.object(winUser, "isHungAppWindow", return_value=True):
			self.assertTrue(utils._shouldSkipEventForHungWindow(_FakeElement(cachedHandle=1)))

	def test_respondingWindowIsNotSkipped(self):
		with patch.object(winUser, "isHungAppWindow", return_value=False):
			self.assertFalse(utils._shouldSkipEventForHungWindow(_FakeElement(cachedHandle=1)))

	def test_guardNeverRaises(self):
		with patch.object(winUser, "isHungAppWindow", side_effect=RuntimeError("boom")):
			# A failure inside the guard itself must never escape into the COM handler.
			self.assertFalse(utils._shouldSkipEventForHungWindow(_FakeElement(cachedHandle=1)))


class Test_isUIAWindow(TestCase):
	"""#20442: a hung application must not make NVDA stop treating its window as UIA."""

	_HWND: int = 1

	def setUp(self) -> None:
		# Stand-in for the UIAHandler instance, so no UIA client is needed.
		self._handler = SimpleNamespace(
			UIAWindowHandleCache={},
			_isUIAWindowHelper=MagicMock(return_value=True),
		)

	def _setExpiredCachedAnswer(self, isUIA: bool) -> None:
		self._handler.UIAWindowHandleCache[self._HWND] = (isUIA, 0)

	def _isUIAWindow(self) -> bool:
		return UIAHandler.UIAHandler.isUIAWindow(self._handler, self._HWND)

	def test_respondingWindowIsChecked(self) -> None:
		self._setExpiredCachedAnswer(False)
		with patch.object(winUser, "isHungAppWindow", return_value=False):
			self.assertTrue(self._isUIAWindow())
		self._handler._isUIAWindowHelper.assert_called_once()

	def test_hungWindowKeepsLastKnownAnswer(self) -> None:
		self._setExpiredCachedAnswer(True)
		self._handler._isUIAWindowHelper.return_value = False
		with patch.object(winUser, "isHungAppWindow", return_value=True):
			self.assertTrue(self._isUIAWindow())
		self._handler._isUIAWindowHelper.assert_not_called()

	def test_cancelledCheckKeepsLastKnownAnswer(self) -> None:
		self._setExpiredCachedAnswer(True)
		self._handler._isUIAWindowHelper.side_effect = exceptions.CallCancelled
		with patch.object(winUser, "isHungAppWindow", return_value=False):
			self.assertTrue(self._isUIAWindow())

	def test_cancelledCheckWithoutLastKnownAnswerIsNotUIA(self) -> None:
		self._handler._isUIAWindowHelper.side_effect = exceptions.CallCancelled
		self.assertFalse(self._isUIAWindow())
