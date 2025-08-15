# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2025 NV Access Limited, Leonard de Ruijter

"""Unit tests for the ctypesUtils submodule."""

import unittest
from ctypes import c_long, windll
from ctypes.wintypes import BOOL, HWND, RECT
from typing import Annotated, Union
from utils.ctypesUtils import FuncSpec, Pointer, dllFunc, OutParam, ParamDirectionFlag


class Test_FuncSpec(unittest.TestCase):
	"""Tests for the :class:`FuncSpec` and its :classmethod:`FuncSpec.getCallable` factory in ctypesUtils module.
	It verifies that the function correctly extracts the function signature
	from a given function definition with type hints."""

	def testBasicTypes(self):
		"""Tests that FuncSpec.fromCallable can extract a function signature with basic ctypes type hints."""

		def GetClientRect(hWnd: HWND, lpRect: Pointer[RECT]) -> BOOL: ...

		actualFuncSpec = FuncSpec.fromCallable(GetClientRect)
		expectedFuncSpec = FuncSpec(
			BOOL,
			(HWND, Pointer[RECT]),
			((ParamDirectionFlag.IN, "hWnd"), (ParamDirectionFlag.IN, "lpRect")),
		)
		self.assertEqual(actualFuncSpec, expectedFuncSpec)

	def testUnionTypesInOnly(self):
		"""Tests that FuncSpec.fromCallable can extract a function signature with union ctypes type hints."""

		def GetClientRect(hWnd: int | HWND, lpRect: Pointer[RECT]) -> Annotated[int, BOOL]: ...

		actualFuncSpec = FuncSpec.fromCallable(GetClientRect)
		expectedFuncSpec = FuncSpec(
			BOOL,
			(HWND, Pointer[RECT]),
			((ParamDirectionFlag.IN, "hWnd"), (ParamDirectionFlag.IN, "lpRect")),
		)
		self.assertEqual(actualFuncSpec, expectedFuncSpec)

	def testLegacyUnionTypesInOnly(self):
		"""Tests that FuncSpec.fromCallable can extract a function signature with legacy Union ctypes type hints."""

		def GetClientRect(hWnd: Union[int, HWND], lpRect: Pointer[RECT]) -> Annotated[int, BOOL]: ...

		actualFuncSpec = FuncSpec.fromCallable(GetClientRect)
		expectedFuncSpec = FuncSpec(
			BOOL,
			(HWND, Pointer[RECT]),
			((ParamDirectionFlag.IN, "hWnd"), (ParamDirectionFlag.IN, "lpRect")),
		)
		self.assertEqual(actualFuncSpec, expectedFuncSpec)

	def testAnnotatedTypesInOut(self):
		"""Tests that FuncSpec.fromCallable can extract a function signature with
		union type hints, including output parameters.
		"""

		def GetClientRect(hWnd: int | HWND) -> Annotated[RECT, OutParam("lpRect", 1)]: ...

		actualFuncSpec = FuncSpec.fromCallable(GetClientRect, restype=BOOL)
		expectedFuncSpec = FuncSpec(
			BOOL,
			(HWND, Pointer[RECT]),
			((ParamDirectionFlag.IN, "hWnd"), (ParamDirectionFlag.OUT, "lpRect")),
		)
		self.assertEqual(actualFuncSpec, expectedFuncSpec)


class Test_FuncSpecRaises(unittest.TestCase):
	"""Tests for scenarios where FuncSpec.fromCallable should raise exceptions."""

	def testMissingArgType(self):
		"""Tests that FuncSpec.fromCallable raises TypeError when a function is missing an argument type annotation."""

		def GetClientRect(hWnd) -> BOOL: ...

		self.assertRaises(TypeError, FuncSpec, GetClientRect)

	def testMissingReturnType(self):
		"""Tests that FuncSpec.fromCallable raises TypeError when a function is missing a return type annotation."""

		def GetClientRect(hWnd: HWND): ...

		self.assertRaises(TypeError, FuncSpec.fromCallable, GetClientRect)

	def testUnsupportedTypes(self):
		"""Tests that FuncSpec.fromCallable raises TypeError when a function has unsupported types."""

		def GetClientRect(hWnd: int) -> bool: ...

		self.assertRaises(TypeError, FuncSpec.fromCallable, GetClientRect)

	def testUnsupportedReturnTypeAnnotation(self):
		"""Tests that FuncSpec.fromCallable raises TypeError when a function has an unsupported return type annotation."""

		def GetClientRect(hWnd: HWND) -> Annotated[int, int]: ...

		self.assertRaises(TypeError, FuncSpec.fromCallable, GetClientRect)

	def testUnsupportedAnnotatedArgument(self):
		"""Tests that FuncSpec.fromCallable raises TypeError when a function has an unsupported argument type."""

		def GetClientRect(hWnd: Annotated[int, HWND]) -> BOOL: ...

		self.assertRaises(TypeError, FuncSpec.fromCallable, GetClientRect)

	def testOutParamWithWrongResType(self):
		"""Tests that FuncSpec.fromCallable raises TypeError when an OutParam is used with a wrong return type."""

		def GetClientRect(hWnd: HWND) -> Annotated[int, OutParam("lpRect", 2)]: ...

		self.assertRaises(TypeError, FuncSpec.fromCallable, GetClientRect)

	def testOutParamWithUnsupportedType(self):
		"""Tests that FuncSpec.fromCallable raises TypeError when an OutParam is used with an unsupported type."""

		def GetClientRect(hWnd: HWND) -> Annotated[int, OutParam("lpRect", 2, int)]: ...

		self.assertRaises(TypeError, FuncSpec.fromCallable, GetClientRect)

	def testOutParamInArgTypes(self):
		"""Tests that FuncSpec.fromCallable raises TypeError when an OutParam is used in argument types."""

		def GetClientRect(hWnd: HWND, lpRect: Annotated[int, OutParam("lpRect", 2)]) -> BOOL: ...

		self.assertRaises(TypeError, FuncSpec.fromCallable, GetClientRect)


class Test_dllFunc(unittest.TestCase):
	"""Tests for the dllFunc decorator in ctypesUtils module.
	It verifies that the decorator correctly sets the function's restype and argtypes.
	"""

	def testBasicTypes(self):
		"""Tests that dllFunc can set restype and argtypes for a function with basic ctypes type hints."""

		@dllFunc(windll.user32, annotateOriginalCFunc=True)
		def GetClientRect(hWnd: HWND, lpRect: Pointer[RECT]) -> BOOL: ...

		self.assertEqual(windll.user32.GetClientRect.restype, BOOL)
		self.assertEqual(windll.user32.GetClientRect.argtypes, (HWND, Pointer[RECT]))

	def testTypesInOut(self):
		"""Tests that dllFunc can set restype and argtypes for a function with union ctypes type hints,
		including Annotated output parameters.
		"""

		@dllFunc(windll.user32, restype=BOOL, annotateOriginalCFunc=True)
		def GetClientRect(hWnd: int | HWND) -> Annotated[RECT, OutParam("lpRect", 1)]: ...

		self.assertEqual(windll.user32.GetClientRect.restype, BOOL)
		self.assertEqual(windll.user32.GetClientRect.argtypes, (HWND, Pointer[RECT]))

	def testDontOverrideOnOriginalPointer(self):
		"""Tests that dllFunc does not override the restype and argtypes
		when instructed not to."""
		windll.user32.GetClientRect.restype = c_long
		windll.user32.GetClientRect.argtypes = None

		@dllFunc(windll.user32, restype=BOOL, annotateOriginalCFunc=False)
		def GetClientRect(hWnd: int | HWND) -> Annotated[RECT, OutParam("lpRect", 1)]: ...

		self.assertEqual(windll.user32.GetClientRect.restype, c_long)  # Default
		self.assertIsNone(windll.user32.GetClientRect.argtypes)
