# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024-2026 NV Access Limited, Akash Kakkar
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the magnification Windows API."""

import unittest
from unittest import mock

import screenCurtain
from screenCurtain._screenCurtain import TRANSFORM_BLACK
from winBindings import magnification
from winBindings.magnification import MAGCOLOREFFECT


class _Test_MagnificationAPI(unittest.TestCase):
	def setUp(self):
		self.assertTrue(magnification.MagInitialize())

	def tearDown(self):
		self.assertTrue(magnification.MagUninitialize())


class TestScreenCurtainAvailability(unittest.TestCase):
	def test_unavailableMagnificationPreventsInitialization(self):
		loadError = OSError("missing Magnification.dll")
		with (
			mock.patch.object(screenCurtain, "MAGNIFICATION_AVAILABLE", False),
			mock.patch.object(screenCurtain, "MAGNIFICATION_LOAD_ERROR", loadError),
			mock.patch.object(screenCurtain, "screenCurtain", None),
			mock.patch.object(screenCurtain, "ScreenCurtain") as screenCurtainClass,
			mock.patch.object(screenCurtain.log, "warning") as logWarning,
		):
			screenCurtain.initialize()

			screenCurtainClass.assert_not_called()
			self.assertIsNone(screenCurtain.screenCurtain)
			logWarning.assert_called_once_with(
				"Screen Curtain unavailable because the Windows Magnification API is unavailable.",
				exc_info=loadError,
			)


class Test_ScreenCurtain(_Test_MagnificationAPI):
	def _isIdentityMatrix(self, magTransformMatrix: MAGCOLOREFFECT) -> bool:
		for i in range(5):
			for j in range(5):
				if i == j:
					if magTransformMatrix.transform[i][j] != 1:
						return False
				else:
					if magTransformMatrix.transform[i][j] != 0:
						return False
		return True

	def setUp(self):
		super().setUp()
		resultEffect = magnification.MagGetFullscreenColorEffect()
		if not self._isIdentityMatrix(resultEffect):
			# If the resultEffect is not the identity matrix, skip the test.
			# This is because a full screen colour effect is already set external to testing.
			self.skipTest(
				f"{resultEffect=}, should be identity matrix. "
				"Full screen colour effect set external to tests. ",
			)

	def test_setAndConfirmBlackFullscreenColorEffect(self):
		result = magnification.MagSetFullscreenColorEffect(TRANSFORM_BLACK)
		self.assertTrue(result)
		resultEffect = magnification.MagGetFullscreenColorEffect()
		for i in range(5):
			for j in range(5):
				with self.subTest(i=i, j=j):
					self.assertEqual(
						TRANSFORM_BLACK.transform[i][j],
						resultEffect.transform[i][j],
						msg=f"i={i}, j={j}, resultEffect={resultEffect}",
					)


class Test_Mouse(_Test_MagnificationAPI):
	def test_MagShowSystemCursor(self):
		result = magnification.MagShowSystemCursor(True)
		self.assertTrue(result)

	def test_MagHideSystemCursor(self):
		result = magnification.MagShowSystemCursor(False)
		self.assertTrue(result)
