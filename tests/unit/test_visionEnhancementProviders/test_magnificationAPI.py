# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited.

"""Unit tests for the magnification Windows API."""

import unittest

from visionEnhancementProviders.screenCurtain import Magnification, TRANSFORM_BLACK, MAGCOLOREFFECT


class _Test_MagnificationAPI(unittest.TestCase):
	def setUp(self):
		self.assertTrue(Magnification.MagInitialize())

	def tearDown(self):
		self.assertTrue(Magnification.MagUninitialize())


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
		resultEffect = Magnification.MagGetFullscreenColorEffect()
		if not self._isIdentityMatrix(resultEffect):
			# If the resultEffect is not the identity matrix, skip the test.
			# This is because a full screen colour effect is already set external to testing.
			self.skipTest(
				f"{resultEffect=}, should be identity matrix. "
				"Full screen colour effect set external to tests. ",
			)
		return

	def test_setAndConfirmBlackFullscreenColorEffect(self):
		result = Magnification.MagSetFullscreenColorEffect(TRANSFORM_BLACK)
		self.assertTrue(result)
		resultEffect = Magnification.MagGetFullscreenColorEffect()
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
		result = Magnification.MagShowSystemCursor(True)
		self.assertTrue(result)

	def test_MagHideSystemCursor(self):
		result = Magnification.MagShowSystemCursor(False)
		self.assertTrue(result)
