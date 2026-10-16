# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 Christos Bouronikos
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for review position handling in the api module."""

import unittest
from unittest.mock import Mock, patch

import api
import exceptions
import globalVars
import review
import treeInterceptorHandler
from comtypes import COMError
from NVDAObjects import NVDAObject


class TestGetReviewPosition(unittest.TestCase):
	def setUp(self) -> None:
		self.obj = Mock()
		for name, value in (
			("navigatorObject", self.obj),
			("reviewPosition", None),
			("reviewPositionObj", None),
		):
			patcher = patch.object(globalVars, name, value)
			patcher.start()
			self.addCleanup(patcher.stop)

	def test_cachedPositionIsReturned(self) -> None:
		position = globalVars.reviewPosition = Mock()
		with patch.object(review, "getPositionForCurrentMode") as getPosition:
			self.assertIs(api.getReviewPosition(), position)
		getPosition.assert_not_called()

	def test_failureIsNotCachedAndKeepsCause(self) -> None:
		"""#20860: A failure raises LocationUnavailableError, and a later call can succeed."""
		position = Mock()
		for error in (
			COMError(-2147024809, "Invalid argument", None),
			RuntimeError(),
			NotImplementedError(),
			LookupError(),
			OSError(),
		):
			with self.subTest(error=error):
				globalVars.reviewPosition = globalVars.reviewPositionObj = None
				with patch.object(
					review,
					"getPositionForCurrentMode",
					side_effect=[error, (position, self.obj)],
				):
					with self.assertRaises(exceptions.LocationUnavailableError) as caught:
						api.getReviewPosition()
					self.assertIs(caught.exception.__cause__, error)
					self.assertIsNone(globalVars.reviewPosition)
					self.assertIs(api.getReviewPosition(), position)
				self.assertIs(globalVars.reviewPositionObj, self.obj)

	def test_noNavigatorObject(self) -> None:
		globalVars.navigatorObject = None
		with self.assertRaises(exceptions.LocationUnavailableError):
			api.getReviewPosition()

	def test_unexpectedErrorsPropagate(self) -> None:
		for error in (AttributeError(), TypeError(), exceptions.CallCancelled()):
			with (
				self.subTest(error=error),
				patch.object(review, "getPositionForCurrentMode", side_effect=error),
				self.assertRaises(type(error)),
			):
				api.getReviewPosition()


class TestSetNavigatorObject(unittest.TestCase):
	def test_caretFailureDoesNotAbortFocusHandling(self) -> None:
		"""#20860: Failing to get the caret for the review position must not stop focus handling."""
		treeInterceptor = Mock(spec=treeInterceptorHandler.DocumentTreeInterceptor)
		treeInterceptor.isReady = True
		treeInterceptor.passThrough = False
		treeInterceptor.makeTextInfo.side_effect = COMError(-2147467259, "Unspecified error", None)
		obj = Mock(spec=NVDAObject)
		obj.treeInterceptor = treeInterceptor
		with (
			patch.object(api, "objectBelowLockScreenAndWindowsIsLocked", return_value=False),
			patch.object(globalVars, "navigatorObject"),
			patch.object(globalVars, "reviewPosition"),
			patch.object(globalVars, "reviewPositionObj"),
			patch.object(review, "_currentMode", 0),
			patch.object(api.eventHandler, "executeEvent") as executeEvent,
		):
			self.assertTrue(api.setNavigatorObject(obj, isFocus=True))
			self.assertIsNone(globalVars.reviewPosition)
			self.assertIsNone(globalVars.reviewPositionObj)
		executeEvent.assert_called_once_with("becomeNavigatorObject", obj, isFocus=True)
