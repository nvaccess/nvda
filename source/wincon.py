# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


from ctypes import (
	byref,
	WinError,
	create_string_buffer,
	c_int,
)
import winBindings.kernel32
from winBindings.kernel32 import (
	COORD as _COORD,
	CONSOLE_SCREEN_BUFFER_INFO as _CONSOLE_SCREEN_BUFFER_INFO,
	CONSOLE_SELECTION_INFO as _CONSOLE_SELECTION_INFO,
	CHAR_INFO as _CHAR_INFO,
)
import textUtils
from utils import _deprecate

"""
Lower level utility functions and constants for NVDA's
legacy Windows console support, for situations where UIA isn't available.
"""


__getattr__ = _deprecate.handleDeprecations(
	_deprecate.MovedSymbol(
		"COORD",
		"winBindings.kernel32",
	),
	_deprecate.MovedSymbol(
		"CONSOLE_SCREEN_BUFFER_INFO",
		"winBindings.kernel32",
	),
	_deprecate.MovedSymbol(
		"CONSOLE_SELECTION_INFO",
		"winBindings.kernel32",
	),
	_deprecate.MovedSymbol(
		"CHAR_INFO",
		"winBindings.kernel32",
	),
	_deprecate.MovedSymbol(
		"PHANDLER_ROUTINE",
		"winBindings.kernel32",
	),
)


CONSOLE_REAL_OUTPUT_HANDLE = -2


CTRL_C_EVENT = 0
CTRL_BREAK_EVENT = 1
CTRL_CLOSE_EVENT = 2

CONSOLE_NO_SELECTION = 0x0
CONSOLE_SELECTION_IN_PROGRESS = 0x1
CONSOLE_SELECTION_NOT_EMPTY = 0x2
CONSOLE_MOUSE_SELECTION = 0x4
CONSOLE_MOUSE_DOWN = 0x8


def GetConsoleSelectionInfo():
	info = _CONSOLE_SELECTION_INFO()
	if winBindings.kernel32.GetConsoleSelectionInfo(byref(info)) == 0:  # noqa: F405
		raise WinError()  # noqa: F405
	return info


def ReadConsoleOutputCharacter(handle, length, x, y):
	# Use a string buffer, as from an unicode buffer, we can't get the raw data.
	buf = create_string_buffer(length * 2)  # noqa: F405
	numCharsRead = c_int()  # noqa: F405
	if (
		winBindings.kernel32.ReadConsoleOutputCharacter(
			handle,
			buf,
			length,
			_COORD(x, y),
			byref(numCharsRead),
		)  # noqa: F405
		== 0
	):  # noqa: F405
		raise WinError()  # noqa: F405
	return textUtils.getTextFromRawBytes(
		buf.raw,
		numChars=numCharsRead.value,
		encoding=textUtils.WCHAR_ENCODING,
	)


def ReadConsoleOutput(handle, length, rect):
	BufType = _CHAR_INFO * length
	buf = BufType()
	# rect=SMALL_RECT(x, y, x+length-1, y)
	if (
		winBindings.kernel32.ReadConsoleOutput(  # noqa: F405
			handle,
			buf,
			_COORD(rect.Right - rect.Left + 1, rect.Bottom - rect.Top + 1),
			_COORD(0, 0),
			byref(rect),  # noqa: F405
		)
		== 0
	):  # noqa: F405
		raise WinError()  # noqa: F405
	return buf


def GetConsoleScreenBufferInfo(handle):
	info = _CONSOLE_SCREEN_BUFFER_INFO()
	if winBindings.kernel32.GetConsoleScreenBufferInfo(handle, byref(info)) == 0:  # noqa: F405
		raise WinError()  # noqa: F405
	return info


def FreeConsole():
	if winBindings.kernel32.FreeConsole() == 0:  # noqa: F405
		raise WinError()  # noqa: F405


def AttachConsole(processID):
	if winBindings.kernel32.AttachConsole(processID) == 0:  # noqa: F405
		raise WinError()  # noqa: F405


def GetConsoleWindow():
	return winBindings.kernel32.GetConsoleWindow()  # noqa: F405


def GetConsoleProcessList(maxProcessCount):
	processList = (c_int * maxProcessCount)()  # noqa: F405
	num = winBindings.kernel32.GetConsoleProcessList(processList, maxProcessCount)  # noqa: F405
	return processList[0:num]


def SetConsoleCtrlHandler(handler, add):
	if winBindings.kernel32.SetConsoleCtrlHandler(handler, add) == 0:  # noqa: F405
		raise WinError()  # noqa: F405
