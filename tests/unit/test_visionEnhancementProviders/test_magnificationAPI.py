# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited.

"""Unit tests for the magnification Windows API."""

import unittest

from visionEnhancementProviders.screenCurtain import Magnification, TRANSFORM_BLACK


class Test_ScreenCurtain(unittest.TestCase):
	def setUp(self):
		self.assertTrue(Magnification.MagInitialize())

	def tearDown(self):
		self.assertTrue(Magnification.MagUninitialize())

	def test_setAndConfirmBlackFullscreenColorEffect(self):
		result = Magnification.MagSetFullscreenColorEffect(TRANSFORM_BLACK)
		self.assertTrue(result)
		resultEffect = Magnification.MagGetFullscreenColorEffect()
		for i in range(5):
			for j in range(5):
				self.assertEqual(TRANSFORM_BLACK.transform[i][j], resultEffect.transform[i][j])

	def test_getDefaultIdentityFullscreenColorEffect(self):
		resultEffect = Magnification.MagGetFullscreenColorEffect()
		for i in range(5):
			for j in range(5):
				# The transform matrix should be the identity matrix
				self.assertEqual(int(i == j), resultEffect.transform[i][j], f"i={i}, j={j}")


class Test_Mouse(unittest.TestCase):
	def setUp(self):
		self.assertTrue(Magnification.MagInitialize())

	def tearDown(self):
		self.assertTrue(Magnification.MagUninitialize())

	def test_MagShowSystemCursor(self):
		result = Magnification.MagShowSystemCursor(True)
		self.assertTrue(result)

	def test_MagHideSystemCursor(self):
		result = Magnification.MagShowSystemCursor(False)
		self.assertTrue(result)
