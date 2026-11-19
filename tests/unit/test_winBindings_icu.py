# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for loading the Windows built-in ICU library in winBindings.icu."""

import ctypes
import importlib.util
import unittest
from collections.abc import Container
from types import ModuleType
from unittest.mock import patch

import winBindings.icu


def _loadIcuBindings(loadableDlls: Container[str]) -> ModuleType:
	"""Execute a fresh copy of winBindings.icu where windll can only load the given DLL names.

	The copy is not registered in sys.modules, so the real winBindings.icu is left untouched.
	"""

	def dllType(name: str) -> ctypes.WinDLL:
		if name not in loadableDlls:
			raise FileNotFoundError(f"Could not find module {name!r}")
		return ctypes.WinDLL(name)

	spec = importlib.util.spec_from_file_location("_winBindingsIcuUnderTest", winBindings.icu.__file__)
	module = importlib.util.module_from_spec(spec)
	with patch.object(ctypes, "windll", ctypes.LibraryLoader(dllType)):
		spec.loader.exec_module(module)
	return module


class Test_icuLoading(unittest.TestCase):
	def test_noIcuLibrary(self):
		"""Without icu.dll and icuuc.dll, ICU is reported unavailable instead of failing to import."""
		module = _loadIcuBindings(loadableDlls=())
		self.assertFalse(module.ICU_AVAILABLE)
		self.assertIsNone(module.dll)
		self.assertFalse(hasattr(module, "ubrk_open"))

	def test_fallsBackToIcuuc(self):
		"""Without icu.dll, the break iterator functions are bound from icuuc.dll."""
		try:
			ctypes.WinDLL("icuuc")
		except OSError:
			self.skipTest("icuuc.dll not available on this system")
		module = _loadIcuBindings(loadableDlls=("icuuc",))
		self.assertTrue(module.ICU_AVAILABLE)
		self.assertEqual(module.dll._name, "icuuc")
		for funcName in ("ubrk_open", "ubrk_close", "ubrk_preceding", "ubrk_following"):
			with self.subTest(funcName=funcName):
				self.assertTrue(callable(getattr(module, funcName)))
