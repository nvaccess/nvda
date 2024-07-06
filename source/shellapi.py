# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from ctypes import *  # noqa: F403
from ctypes.wintypes import *  # noqa: F403
from typing import Optional


shell32 = windll.shell32  # noqa: F405


class SHELLEXECUTEINFOW(Structure):  # noqa: F405
	_fields_ = (
		("cbSize", DWORD),  # noqa: F405
		("fMask", ULONG),  # noqa: F405
		("hwnd", HWND),  # noqa: F405
		("lpVerb", LPCWSTR),  # noqa: F405
		("lpFile", LPCWSTR),  # noqa: F405
		("lpParameters", LPCWSTR),  # noqa: F405
		("lpDirectory", LPCWSTR),  # noqa: F405
		("nShow", c_int),  # noqa: F405
		("hInstApp", HINSTANCE),  # noqa: F405
		("lpIDList", LPVOID),  # noqa: F405
		("lpClass", LPCWSTR),  # noqa: F405
		("hkeyClass", HKEY),  # noqa: F405
		("dwHotKey", DWORD),  # noqa: F405
		("hIconOrMonitor", HANDLE),  # noqa: F405
		("hProcess", HANDLE),  # noqa: F405
	)

	def __init__(self, **kwargs):
		super(SHELLEXECUTEINFOW, self).__init__(cbSize=sizeof(self), **kwargs)  # noqa: F405


SHELLEXECUTEINFO = SHELLEXECUTEINFOW

SEE_MASK_NOCLOSEPROCESS = 0x00000040


def ShellExecute(
	hwnd: Optional[int],
	operation: Optional[str],
	file: str,
	parameters: Optional[str],
	directory: Optional[str],
	showCmd: int,
) -> None:
	if not file:
		raise RuntimeError("file cannot be None")
	if shell32.ShellExecuteW(hwnd, operation, file, parameters, directory, showCmd) <= 32:
		raise WinError()  # noqa: F405


def ShellExecuteEx(execInfo):
	if not shell32.ShellExecuteExW(byref(execInfo)):  # noqa: F405
		raise WinError()  # noqa: F405


FILEOP_FLAGS = WORD  # noqa: F405

FO_MOVE = 1
FO_COPY = 2
FO_DELETE = 3
FO_RENAME = 4

FOF_NOCONFIRMMKDIR = 0x200


class SHFILEOPSTRUCT(Structure):  # noqa: F405
	_fields_ = [
		("hwnd", HWND),  # noqa: F405
		("wFunc", c_uint),  # noqa: F405
		("pFrom", c_wchar_p),  # noqa: F405
		("pTo", c_wchar_p),  # noqa: F405
		("fFlags", FILEOP_FLAGS),
		("fAnyOperationsAborted", BOOL),  # noqa: F405
		("hNameMapping", c_void_p),  # noqa: F405
		("lpszProgressTitle", c_wchar_p),  # noqa: F405
	]


SHCNE_ASSOCCHANGED = 0x08000000
SHCNF_IDLIST = 0x0
shell32.SHChangeNotify.argtypes = [c_long, c_uint, c_void_p, c_void_p]  # noqa: F405
shell32.SHChangeNotify.restype = None


def SHChangeNotify(wEventId, uFlags, dwItem1, dwItem2):
	shell32.SHChangeNotify(wEventId, uFlags, dwItem1, dwItem2)
