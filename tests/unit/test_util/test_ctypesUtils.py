# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021 NV Access Limited.

"""Unit tests for the displayString submodule."""

import unittest
from ctypes import POINTER
from ctypes.wintypes import BOOL, HWND, RECT
from typing import Annotated
from utils.ctypesUtils import FuncSpec, getFuncSPec, OutParam, ParamDirectionFlag


class Test_FuncSPec(unittest.TestCase):
	"""Tests for the getFuncSPec function in ctypesUtils module.
	It verifies that the function correctly extracts the function signature
	from a given function definition with type hints."""

	def testBasicTypes(self):
		"""Tests that getFuncSPec can extract a function signature with basic ctypes type hints."""

		def GetClientRect(hWnd: HWND, lpRect: POINTER(RECT)) -> BOOL: ...

		actualFuncSPec = getFuncSPec(GetClientRect)
		expectedFuncSpec = FuncSpec(
			BOOL,
			(HWND, POINTER(RECT)),
			((ParamDirectionFlag.IN, "hWnd"), (ParamDirectionFlag.IN, "lpRect")),
		)
		self.assertEqual(actualFuncSPec, expectedFuncSpec)

	def testAnnotatedTypesInOnly(self):
		"""Tests that getFuncSPec can extract a function signature with annotated ctypes type hints."""

		def GetClientRect(hWnd: Annotated[int, HWND], lpRect: POINTER(RECT)) -> Annotated[int, BOOL]: ...

		actualFuncSPec = getFuncSPec(GetClientRect)
		expectedFuncSpec = FuncSpec(
			BOOL,
			(HWND, POINTER(RECT)),
			((ParamDirectionFlag.IN, "hWnd"), (ParamDirectionFlag.IN, "lpRect")),
		)
		self.assertEqual(actualFuncSPec, expectedFuncSpec)

	def testAnnotatedTypesInOut(self):
		"""Tests that getFuncSPec can extract a function signature with
		annotated ctypes type hints, including output parameters.
		"""

		def GetClientRect(
			hWnd: Annotated[int, HWND],
		) -> Annotated[RECT, OutParam(POINTER(RECT), "lpRect", 2)]: ...

		actualFuncSPec = getFuncSPec(GetClientRect, restype=BOOL)
		expectedFuncSpec = FuncSpec(
			BOOL,
			(HWND, POINTER(RECT)),
			((ParamDirectionFlag.IN, "hWnd"), (ParamDirectionFlag.OUT, "lpRect")),
		)
		self.assertEqual(actualFuncSPec, expectedFuncSpec)


class Test_FuncSPecRaises(unittest.TestCase):
	def testMissingArgType(self):
		def GetClientRect(hWnd) -> BOOL: ...

		self.assertRaises(TypeError, getFuncSPec, GetClientRect)

	def testMissingReturnType(self):
		def GetClientRect(hWnd: HWND): ...

		self.assertRaises(TypeError, getFuncSPec, GetClientRect)

	def testUnsupportedTypes(self):
		def GetClientRect(hWnd: int) -> bool: ...

		self.assertRaises(TypeError, getFuncSPec, GetClientRect)

	def testUnsupportedReturnTypeAnnotation(self):
		def GetClientRect(hWnd: HWND) -> Annotated[int, int]: ...

		self.assertRaises(TypeError, getFuncSPec, GetClientRect)

	def testUnsupportedArgTypeAnnotation(self):
		def GetClientRect(hWnd: Annotated[int, int]) -> BOOL: ...

		self.assertRaises(TypeError, getFuncSPec, GetClientRect)

	def testOutParamWithoutResType(self):
		def GetClientRect(hWnd: HWND) -> Annotated[int, OutParam(POINTER(RECT), "lpRect", 2)]: ...

		self.assertRaises(TypeError, getFuncSPec, GetClientRect)

	def testOutParamWithUnsupportedType(self):
		def GetClientRect(
			hWnd: HWND,
		) -> Annotated[int, OutParam(int, "lpRect", 2)]: ...

		self.assertRaises(TypeError, getFuncSPec, GetClientRect)

	def testOutParamInArgTypes(self):
		def GetClientRect(
			hWnd: HWND,
			lpRect: Annotated[int, OutParam(POINTER(RECT), "lpRect", 2)],
		) -> BOOL: ...

		self.assertRaises(TypeError, getFuncSPec, GetClientRect)
