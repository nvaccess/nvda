from ctypes import *  # noqa: F403
from ctypes.wintypes import *  # noqa: F403
import textUtils

"""
Lower level utility functions and constants for NVDA's
legacy Windows console support, for situations where UIA isn't available.
"""

CONSOLE_REAL_OUTPUT_HANDLE = -2


class COORD(Structure):  # noqa: F405
	_fields_ = [
		("x", c_short),  # noqa: F405
		("y", c_short),  # noqa: F405
	]


class CONSOLE_SCREEN_BUFFER_INFO(Structure):  # noqa: F405
	_fields_ = [
		("dwSize", COORD),
		("dwCursorPosition", COORD),
		("wAttributes", WORD),  # noqa: F405
		("srWindow", SMALL_RECT),  # noqa: F405
		("dwMaximumWindowSize", COORD),
	]


class CONSOLE_SELECTION_INFO(Structure):  # noqa: F405
	_fields_ = [
		("dwFlags", DWORD),  # noqa: F405
		("dwSelectionAnchor", COORD),
		("srSelection", SMALL_RECT),  # noqa: F405
	]


class CHAR_INFO(Structure):  # noqa: F405
	_fields_ = [
		(
			"Char",
			c_wchar,  # noqa: F405
		),  # union of char and wchar_t isn't needed since we deal only with unicode  # noqa: F405
		("Attributes", WORD),  # noqa: F405
	]


PHANDLER_ROUTINE = WINFUNCTYPE(BOOL, DWORD)  # noqa: F405

CTRL_C_EVENT = 0
CTRL_BREAK_EVENT = 1
CTRL_CLOSE_EVENT = 2

CONSOLE_NO_SELECTION = 0x0
CONSOLE_SELECTION_IN_PROGRESS = 0x1
CONSOLE_SELECTION_NOT_EMPTY = 0x2
CONSOLE_MOUSE_SELECTION = 0x4
CONSOLE_MOUSE_DOWN = 0x8


def GetConsoleSelectionInfo():
	info = CONSOLE_SELECTION_INFO()
	if windll.kernel32.GetConsoleSelectionInfo(byref(info)) == 0:  # noqa: F405
		raise WinError()  # noqa: F405
	return info


def ReadConsoleOutputCharacter(handle, length, x, y):
	# Use a string buffer, as from an unicode buffer, we can't get the raw data.
	buf = create_string_buffer(length * 2)  # noqa: F405
	numCharsRead = c_int()  # noqa: F405
	if (
		windll.kernel32.ReadConsoleOutputCharacterW(handle, buf, length, COORD(x, y), byref(numCharsRead))  # noqa: F405
		== 0
	):  # noqa: F405
		raise WinError()  # noqa: F405
	return textUtils.getTextFromRawBytes(
		buf.raw,
		numChars=numCharsRead.value,
		encoding=textUtils.WCHAR_ENCODING,
	)


def ReadConsoleOutput(handle, length, rect):
	BufType = CHAR_INFO * length
	buf = BufType()
	# rect=SMALL_RECT(x, y, x+length-1, y)
	if (
		windll.kernel32.ReadConsoleOutputW(  # noqa: F405
			handle,
			buf,
			COORD(rect.Right - rect.Left + 1, rect.Bottom - rect.Top + 1),
			COORD(0, 0),
			byref(rect),  # noqa: F405
		)
		== 0
	):  # noqa: F405
		raise WinError()  # noqa: F405
	return buf


def GetConsoleScreenBufferInfo(handle):
	info = CONSOLE_SCREEN_BUFFER_INFO()
	if windll.kernel32.GetConsoleScreenBufferInfo(handle, byref(info)) == 0:  # noqa: F405
		raise WinError()  # noqa: F405
	return info


def FreeConsole():
	if windll.kernel32.FreeConsole() == 0:  # noqa: F405
		raise WinError()  # noqa: F405


def AttachConsole(processID):
	if windll.kernel32.AttachConsole(processID) == 0:  # noqa: F405
		raise WinError()  # noqa: F405


def GetConsoleWindow():
	return windll.kernel32.GetConsoleWindow()  # noqa: F405


def GetConsoleProcessList(maxProcessCount):
	processList = (c_int * maxProcessCount)()  # noqa: F405
	num = windll.kernel32.GetConsoleProcessList(processList, maxProcessCount)  # noqa: F405
	return processList[0:num]


def SetConsoleCtrlHandler(handler, add):
	if windll.kernel32.SetConsoleCtrlHandler(handler, add) == 0:  # noqa: F405
		raise WinError()  # noqa: F405
