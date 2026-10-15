# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 Christos Bouronikos
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for vision.util."""

import unittest
from unittest.mock import Mock, patch

from comtypes import COMError
from exceptions import CallCancelled, LocationUnavailableError
from vision import util
from vision.constants import Context


class TestGetContextRect(unittest.TestCase):
	def test_unavailableReviewPositionPropagates(self):
		error = LocationUnavailableError()
		with (
			patch.object(util.api, "getReviewPosition", side_effect=error),
			self.assertRaises(LocationUnavailableError) as caught,
		):
			util.getContextRect(Context.REVIEW)
		self.assertIs(caught.exception, error)

	def test_retrievalErrorsRaiseLocationUnavailable(self):
		"""#20860: Retrieval errors are raised as a single error type, keeping the original as the cause."""
		for error in (
			COMError(-2147467259, "Unspecified error", None),
			LookupError(),
			RuntimeError(),
			OSError(),
		):
			with (
				self.subTest(error=error),
				patch.object(util, "getReviewRect", side_effect=error),
				self.assertRaises(LocationUnavailableError) as caught,
			):
				util.getContextRect(Context.REVIEW)
			self.assertIs(caught.exception.__cause__, error)

	def test_browseModeCaretError(self):
		error = COMError(-2147467259, "Unspecified error", None)
		with (
			patch.object(util.api, "isCursorManager", return_value=True),
			patch.object(util, "getCaretRect", side_effect=error),
			self.assertRaises(LocationUnavailableError) as caught,
		):
			util.getContextRect(Context.BROWSEMODE, obj=Mock())
		self.assertIs(caught.exception.__cause__, error)

	def test_unexpectedErrorsPropagate(self):
		for error in (AttributeError(), TypeError(), CallCancelled()):
			with (
				self.subTest(error=error),
				patch.object(util, "getReviewRect", side_effect=error),
				self.assertRaises(type(error)),
			):
				util.getContextRect(Context.REVIEW)
