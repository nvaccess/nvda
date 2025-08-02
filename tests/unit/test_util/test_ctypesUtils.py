# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2025 NV Access Limited, Leonard de Ruijter

"""Unit tests for the ctypesUtils submodule."""

import unittest
from ctypes import c_long, windll
from ctypes.wintypes import BOOL, HWND, RECT
from typing import Annotated
from utils.ctypesUtils import FuncSpec, Pointer, dllFunc, getFuncSpec, OutParam, ParamDirectionFlag


class Test_FuncSpec(unittest.TestCase):
	"""Tests for the getFuncSpec function in ctypesUtils module.
	It verifies that the function correctly extracts the function signature
	from a given function definition with type hints."""

	def testBasicTypes(self):
		"""Tests that getFuncSpec can extract a function signature with basic ctypes type hints."""

		def GetClientRect(hWnd: HWND, lpRect: Pointer[RECT]) -> BOOL: ...

		actualFuncSpec = getFuncSpec(GetClientRect)
		expectedFuncSpec = FuncSpec(
			BOOL,
			(HWND, Pointer[RECT]),
			((ParamDirectionFlag.IN, "hWnd"), (ParamDirectionFlag.IN, "lpRect")),
		)
		self.assertEqual(actualFuncSpec, expectedFuncSpec)

	def testAnnotatedTypesInOnly(self):
		"""Tests that getFuncSpec can extract a function signature with annotated ctypes type hints."""

		def GetClientRect(hWnd: Annotated[int, HWND], lpRect: Pointer[RECT]) -> Annotated[int, BOOL]: ...

		actualFuncSpec = getFuncSpec(GetClientRect)
		expectedFuncSpec = FuncSpec(
			BOOL,
			(HWND, Pointer[RECT]),
			((ParamDirectionFlag.IN, "hWnd"), (ParamDirectionFlag.IN, "lpRect")),
		)
		self.assertEqual(actualFuncSpec, expectedFuncSpec)

	def testUnionTypesInOnly(self):
		"""Tests that getFuncSpec can extract a function signature with union ctypes type hints."""

		def GetClientRect(hWnd: int | HWND, lpRect: Pointer[RECT]) -> Annotated[int, BOOL]: ...

		actualFuncSpec = getFuncSpec(GetClientRect)
		expectedFuncSpec = FuncSpec(
			BOOL,
			(HWND, Pointer[RECT]),
			((ParamDirectionFlag.IN, "hWnd"), (ParamDirectionFlag.IN, "lpRect")),
		)
		self.assertEqual(actualFuncSpec, expectedFuncSpec)

	def testAnnotatedTypesInOut(self):
		"""Tests that getFuncSpec can extract a function signature with
		annotated ctypes type hints, including output parameters.
		"""

		def GetClientRect(hWnd: int | HWND) -> Annotated[RECT, OutParam("lpRect", 1)]: ...

		actualFuncSpec = getFuncSpec(GetClientRect, restype=BOOL)
		expectedFuncSpec = FuncSpec(
			BOOL,
			(HWND, Pointer[RECT]),
			((ParamDirectionFlag.IN, "hWnd"), (ParamDirectionFlag.OUT, "lpRect")),
		)
		self.assertEqual(actualFuncSpec, expectedFuncSpec)


class Test_FuncSpecRaises(unittest.TestCase):
	"""Tests for scenarios where getFuncSpec should raise exceptions."""

	def testMissingArgType(self):
		"""Tests that getFuncSpec raises TypeError when a function is missing an argument type annotation."""

		def GetClientRect(hWnd) -> BOOL: ...

		self.assertRaises(TypeError, getFuncSpec, GetClientRect)

	def testMissingReturnType(self):
		"""Tests that getFuncSpec raises TypeError when a function is missing a return type annotation."""

		def GetClientRect(hWnd: HWND): ...

		self.assertRaises(TypeError, getFuncSpec, GetClientRect)

	def testUnsupportedTypes(self):
		"""Tests that getFuncSpec raises TypeError when a function has unsupported types."""

		def GetClientRect(hWnd: int) -> bool: ...

		self.assertRaises(TypeError, getFuncSpec, GetClientRect)

	def testUnsupportedReturnTypeAnnotation(self):
		"""Tests that getFuncSpec raises TypeError when a function has an unsupported return type annotation."""

		def GetClientRect(hWnd: HWND) -> Annotated[int, int]: ...

		self.assertRaises(TypeError, getFuncSpec, GetClientRect)

	def testUnsupportedArgTypeAnnotation(self):
		"""Tests that getFuncSpec raises TypeError when a function has an unsupported argument type annotation."""

		def GetClientRect(hWnd: Annotated[int, int]) -> BOOL: ...

		self.assertRaises(TypeError, getFuncSpec, GetClientRect)

	def testOutParamWithWrongResType(self):
		"""Tests that getFuncSpec raises TypeError when an OutParam is used with a wrong return type."""

		def GetClientRect(hWnd: HWND) -> Annotated[int, OutParam("lpRect", 2)]: ...

		self.assertRaises(TypeError, getFuncSpec, GetClientRect)

	def testOutParamWithUnsupportedType(self):
		"""Tests that getFuncSpec raises TypeError when an OutParam is used with an unsupported type."""

		def GetClientRect(hWnd: HWND) -> Annotated[int, OutParam("lpRect", 2, int)]: ...

		self.assertRaises(TypeError, getFuncSpec, GetClientRect)

	def testOutParamInArgTypes(self):
		"""Tests that getFuncSpec raises TypeError when an OutParam is used in argument types."""

		def GetClientRect(hWnd: HWND, lpRect: Annotated[int, OutParam("lpRect", 2)]) -> BOOL: ...

		self.assertRaises(TypeError, getFuncSpec, GetClientRect)


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

	def testAnnotatedTypesInOnly(self):
		"""Tests that dllFunc can set restype and argtypes for a function with annotated ctypes type hints on parameters."""

		@dllFunc(windll.user32, annotateOriginalCFunc=True)
		def GetClientRect(hWnd: Annotated[int, HWND], lpRect: Pointer[RECT]) -> Annotated[int, BOOL]: ...

		self.assertEqual(windll.user32.GetClientRect.restype, BOOL)
		self.assertEqual(windll.user32.GetClientRect.argtypes, (HWND, Pointer[RECT]))

	def testAnnotatedTypesInOut(self):
		"""Tests that dllFunc can set restype and argtypes for a function with annotated ctypes type hints,
		including output parameters.
		"""

		@dllFunc(windll.user32, restype=BOOL, annotateOriginalCFunc=True)
		def GetClientRect(hWnd: Annotated[int, HWND]) -> Annotated[RECT, OutParam("lpRect", 1)]: ...

		self.assertEqual(windll.user32.GetClientRect.restype, BOOL)
		self.assertEqual(windll.user32.GetClientRect.argtypes, (HWND, Pointer[RECT]))

	def testDontOverrideOnOriginalPointer(self):
		windll.user32.GetClientRect.restype = c_long
		windll.user32.GetClientRect.argtypes = None

		@dllFunc(windll.user32, restype=BOOL, annotateOriginalCFunc=False)
		def GetClientRect(hWnd: int | HWND) -> Annotated[RECT, OutParam("lpRect", 1)]: ...

		self.assertEqual(windll.user32.GetClientRect.restype, c_long)  # Default
		self.assertIsNone(windll.user32.GetClientRect.argtypes)
