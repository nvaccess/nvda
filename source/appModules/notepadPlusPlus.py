# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited, Łukasz Golonka
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""AppModule for Notepad++.
Do not rename! The executable file for Notepad++ is named `notepad++` and `+` is not a valid character
in Python's import statements.
This module is mapped to the right binary separately
and the current name makes it possible to expose it from `nvdaBuiltin` for add-on developers.
"""

import ctypes

import appModuleHandler
import NVDAObjects.window.scintilla as ScintillaBase


class CharacterRangeStructLongLong(ctypes.Structure):
	"""By default character ranges in Scintilla are represented by longs.
	However long is not big enough for files over 2 GB,
	therefore in 64-bit builds of Notepad++ 8.3 and later
	these ranges are represented by longlong.
	"""
	_fields_ = [
		('cpMin', ctypes.c_longlong),
		('cpMax', ctypes.c_longlong),
	]


class ScintillaTextInfoNpp83(ScintillaBase.ScintillaTextInfo):
	"""Text info for 64-bit builds of Notepad++ 8.3 and later.
	"""

	class TextRangeStruct(ctypes.Structure):
		_fields_ = [
			('chrg', CharacterRangeStructLongLong),
			('lpstrText', ctypes.c_char_p),
		]


class NppEdit(ScintillaBase.Scintilla):

	name = None  # The name of the editor is not useful.

	def _get_TextInfo(self):
		if self.appModule.is64BitProcess:
			appVerMajor, appVerMinor, *__ = self.appModule.productVersion.split(".")
			# appVerMinor could be either one digit (e.g. in 8.3), two digits (e.g. in 8.21), or even three (8.1.9.2)
			appVerMinor = appVerMinor.ljust(3, '0')
			if int(appVerMajor) >= 8 and int(appVerMinor) >= 300:
				return ScintillaTextInfoNpp83
		return super().TextInfo


class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == "Scintilla" and obj.windowControlID == 0:
			clsList.insert(0, NppEdit)
