# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited.

"""Unit tests for the magnification Windows API."""

import unittest

from winAPI import _displayTracking
from visionEnhancementProviders.magnifier import HostWindow
from visionEnhancementProviders.screenCurtain import MAGTRANSFORM, Magnification, TRANSFORM_BLACK


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
						msg=f"i={i}, j={j}, resultEffect={resultEffect}",
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
						msg=f"i={i}, j={j}, resultEffect={resultEffect}",
					)


class Test_Mouse(_Test_MagnificationAPI):
	def test_MagShowSystemCursor(self):
		result = Magnification.MagShowSystemCursor(True)
		self.assertTrue(result)

	def test_MagHideSystemCursor(self):
		result = Magnification.MagShowSystemCursor(False)
		self.assertTrue(result)


class Test_Magnification(unittest.TestCase):
	def setUp(self):
		self.hostWindow: HostWindow | None = None
		self._prevOrientationState = _displayTracking._orientationState
		self.assertIsNone(self._prevOrientationState)
		_displayTracking.initialize()
		self.assertTrue(Magnification.MagInitialize())

	def tearDown(self):
		self.assertTrue(Magnification.MagUninitialize())
		_displayTracking._orientationState = self._prevOrientationState
		if self.hostWindow:
			self.hostWindow.destroy()

	def _initializeMagWindow(self, magnificationFactor: int = 1):
		self.hostWindow = HostWindow(magnificationFactor)
		self.assertTrue(self.hostWindow.handle)
		self.assertTrue(self.hostWindow.magnifierWindow.handle)

	def test_setAndConfirmMagLevel(self):
		expectedTransform = MAGTRANSFORM(2)
		self._initializeMagWindow(2)
		resultTransform = Magnification.MagGetWindowTransform(self.hostWindow.magnifierWindow.handle)
		for i in range(3):
			for j in range(3):
				with self.subTest(i=i, j=j):
					self.assertEqual(
						expectedTransform.v[i][j],
						resultTransform.v[i][j],
						msg=f"i={i}, j={j}, resultTransform={resultTransform}",
					)

	def test_getDefaultIdentityMagLevel(self):
		self._initializeMagWindow()
		resultTransform = Magnification.MagGetWindowTransform(self.hostWindow.magnifierWindow.handle)
		for i in range(3):
			for j in range(3):
				with self.subTest(i=i, j=j):
					self.assertEqual(
						# The transform matrix should be the identity matrix
						int(i == j),
						resultTransform.v[i][j],
						msg=f"i={i}, j={j}, resultTransform={resultTransform}",
					)
