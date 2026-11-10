# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Akash Kakkar
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import ctypes
import importlib
import unittest
from ctypes import c_void_p
from ctypes.wintypes import BOOL, DWORD, HANDLE, LPWSTR
from unittest import mock

from winBindings import wtsapi32


@unittest.skipUnless(wtsapi32.WTSAPI32_AVAILABLE, "Windows Terminal Services API is unavailable")
class TestAvailableWtsApi32(unittest.TestCase):
	def test_bindingsAreCtypesFunctions(self):
		self.assertIsInstance(wtsapi32.WTSFreeMemory, ctypes._CFuncPtr)
		self.assertIsInstance(wtsapi32.WTSQuerySessionInformation, ctypes._CFuncPtr)


class TestUnavailableWtsApi32(unittest.TestCase):
	def test_importHandlesUnavailableDll(self):
		loadError = OSError("missing wtsapi32.dll")
		unavailableWindll = mock.MagicMock()
		type(unavailableWindll).wtsapi32 = mock.PropertyMock(side_effect=loadError)
		try:
			with mock.patch.object(ctypes, "windll", unavailableWindll):
				importlib.reload(wtsapi32)

			self.assertFalse(wtsapi32.WTSAPI32_AVAILABLE)
			self.assertIs(wtsapi32.WTSAPI32_LOAD_ERROR, loadError)
			self.assertIsNot(wtsapi32.WTSFreeMemory, wtsapi32.WTSQuerySessionInformation)
			self.assertEqual((c_void_p,), wtsapi32.WTSFreeMemory.argtypes)
			self.assertEqual(
				(HANDLE, DWORD, ctypes.c_int, ctypes.POINTER(LPWSTR), ctypes.POINTER(DWORD)),
				wtsapi32.WTSQuerySessionInformation.argtypes,
			)
			self.assertIs(BOOL, wtsapi32.WTSQuerySessionInformation.restype)
			with self.assertRaisesRegex(OSError, "Windows Terminal Services API is not available") as error:
				wtsapi32.WTSQuerySessionInformation()
			self.assertIs(error.exception.__cause__, loadError)
		finally:
			importlib.reload(wtsapi32)
