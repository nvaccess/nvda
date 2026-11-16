# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for magnifier native error handling."""

import unittest
from unittest.mock import MagicMock, patch

from _magnifier.utils.errorHandling import trackNativeMagnifierErrors

from tests.unit.test_magnifier.test_magnifier import _TestMagnifier


class TestTrackNativeMagnifierErrors(unittest.TestCase):
	def testReturnsValue(self):
		@trackNativeMagnifierErrors
		def succeed() -> str:
			return "ok"

		self.assertEqual(succeed(), "ok")

	def testReturnsNoneAndLogsOnOSError(self):
		@trackNativeMagnifierErrors
		def fail() -> str:
			raise OSError("injected")

		with (
			patch("_magnifier.utils.errorHandling._isDebug", return_value=True),
			patch("_magnifier.utils.errorHandling.log") as mockLog,
		):
			self.assertIsNone(fail())
		mockLog.debug.assert_called_once()

	def testReraisesOtherExceptions(self):
		@trackNativeMagnifierErrors
		def fail() -> None:
			raise ValueError("bug")

		with self.assertRaises(ValueError):
			fail()

	def testPreservesIdentity(self):
		def original() -> None:
			pass

		wrapped = trackNativeMagnifierErrors(original)
		self.assertEqual(wrapped.__name__, original.__name__)
		self.assertEqual(wrapped.__qualname__, original.__qualname__)


class TestMousePathErrors(_TestMagnifier):
	def setUp(self):
		super().setUp()
		self.magnifier._isActive = True
		self.magnifier._doUpdate = MagicMock(side_effect=OSError("injected"))

	def testOSErrorIsCounted(self):
		with patch("_magnifier.magnifier._isDebug", return_value=False):
			self.magnifier._applyPendingMousePosition()
		self.assertEqual(self.magnifier._consecutiveErrors, 1)

	def testLoggedOnlyWithDebugLogging(self):
		for isDebug, expectedCalls in ((True, 1), (False, 0)):
			with (
				self.subTest(isDebug=isDebug),
				patch("_magnifier.magnifier._isDebug", return_value=isDebug),
				patch("_magnifier.magnifier.log") as mockLog,
			):
				self.magnifier._applyPendingMousePosition()
				self.assertEqual(mockLog.debugWarning.call_count, expectedCalls)

	def testOtherExceptionsPropagate(self):
		self.magnifier._doUpdate = MagicMock(side_effect=ValueError("bug"))
		with self.assertRaises(ValueError):
			self.magnifier._applyPendingMousePosition()
