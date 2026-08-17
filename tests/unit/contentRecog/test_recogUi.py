# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Cary-rowen
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Unit tests for the contentRecog.recogUi module."""

from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

import contentRecog
from contentRecog import recogUi
import exceptions


class _FakeRefreshableRecogResult:
	def __init__(self, allowAutoRefresh: bool):
		self.recognizer = SimpleNamespace(allowAutoRefresh=allowAutoRefresh)


class TestCaptureImage(unittest.TestCase):
	def setUp(self):
		self.imageInfo = contentRecog.RecogImageInfo(0, 0, 100, 100, 1)
		self.gdiPixels = object()

	def test_usesGdiByDefault(self):
		with (
			patch.object(recogUi, "_isScreenCurtainActive", return_value=False),
			patch.object(recogUi, "_isMagnifierActive", return_value=False),
			patch.object(recogUi, "_captureWithWgc") as captureWithWgc,
			patch.object(recogUi, "_captureWithGdi", return_value=self.gdiPixels) as captureWithGdi,
		):
			pixels = recogUi._captureImage(self.imageInfo)

		self.assertIs(pixels, self.gdiPixels)
		captureWithWgc.assert_not_called()
		captureWithGdi.assert_called_once_with(self.imageInfo)

	def test_screenCurtainWgcFailureDoesNotFallBackToGdi(self):
		captureError = RuntimeError("capture failed")
		with (
			patch.object(recogUi, "_isScreenCurtainActive", return_value=True),
			patch.object(recogUi, "_captureWithWgc", side_effect=captureError) as captureWithWgc,
			patch.object(recogUi, "_captureWithGdi") as captureWithGdi,
		):
			with self.assertRaises(RuntimeError) as cm:
				recogUi._captureImage(self.imageInfo)

		self.assertIs(cm.exception, captureError)
		captureWithWgc.assert_called_once_with(self.imageInfo)
		captureWithGdi.assert_not_called()

	def test_magnifierWgcFailureFallsBackToGdi(self):
		with (
			patch.object(recogUi, "_isScreenCurtainActive", return_value=False),
			patch.object(recogUi, "_isMagnifierActive", return_value=True),
			patch.object(recogUi, "_isWgcCaptureSupported", return_value=True),
			patch.object(
				recogUi,
				"_captureWithWgc",
				side_effect=RuntimeError("capture failed"),
			) as captureWithWgc,
			patch.object(recogUi, "_captureWithGdi", return_value=self.gdiPixels) as captureWithGdi,
		):
			pixels = recogUi._captureImage(self.imageInfo)

		self.assertIs(pixels, self.gdiPixels)
		captureWithWgc.assert_called_once_with(self.imageInfo)
		captureWithGdi.assert_called_once_with(self.imageInfo)


class TestRecognize(unittest.TestCase):
	def test_callCancelledIsReported(self):
		cancellation = exceptions.CallCancelled()
		recognizer = Mock()
		result = SimpleNamespace(
			result=None,
			imageInfo=object(),
			recognizer=recognizer,
		)
		results = []

		with patch.object(recogUi, "_captureImage", side_effect=cancellation):
			recogUi.RefreshableRecogResultNVDAObject._recognize(result, results.append)

		self.assertEqual(results, [cancellation])
		recognizer.recognize.assert_not_called()


class TestScreenCurtainEnableBlock(unittest.TestCase):
	def test_autoRefreshRecognitionBlocksScreenCurtainOnlyWhenWgcUnsupported(self):
		focusObj = _FakeRefreshableRecogResult(allowAutoRefresh=True)

		with (
			patch.object(recogUi, "RefreshableRecogResultNVDAObject", _FakeRefreshableRecogResult),
			patch.object(recogUi, "_isWgcCaptureSupported", side_effect=(False, True)),
		):
			self.assertTrue(recogUi._shouldBlockScreenCurtainEnable(focusObj))
			self.assertFalse(recogUi._shouldBlockScreenCurtainEnable(focusObj))

	def test_nonAutoRefreshRecognitionDoesNotBlockScreenCurtain(self):
		focusObj = _FakeRefreshableRecogResult(allowAutoRefresh=False)

		with patch.object(recogUi, "RefreshableRecogResultNVDAObject", _FakeRefreshableRecogResult):
			self.assertFalse(recogUi._shouldBlockScreenCurtainEnable(focusObj))
