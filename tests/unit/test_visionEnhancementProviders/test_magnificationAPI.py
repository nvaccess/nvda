# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited.

"""Unit tests for the magnification Windows API."""

import unittest

from visionEnhancementProviders.screenCurtain import Magnification, TRANSFORM_BLACK


class _Test_MagnificationAPI(unittest.TestCase):
	def setUp(self):
		self.assertTrue(Magnification.MagInitialize())

	def tearDown(self):
		self.assertTrue(Magnification.MagUninitialize())


class Test_ScreenCurtain(_Test_MagnificationAPI):
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
						msg=f"i={i}, j={j}, resultEffect={resultEffect}"
					)

	def test_getDefaultIdentityFullscreenColorEffect(self):
		resultEffect = Magnification.MagGetFullscreenColorEffect()
		for i in range(5):
			for j in range(5):
				with self.subTest(i=i, j=j):
					# The transform matrix should be the identity matrix
					self.assertEqual(
						int(i == j),
						resultEffect.transform[i][j],
						msg=f"i={i}, j={j}, resultEffect={resultEffect}"
					)


class Test_Mouse(_Test_MagnificationAPI):
	def test_MagShowSystemCursor(self):
		result = Magnification.MagShowSystemCursor(True)
		self.assertTrue(result)

	def test_MagHideSystemCursor(self):
		result = Magnification.MagShowSystemCursor(False)
		self.assertTrue(result)
