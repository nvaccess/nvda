#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from ctypes import *
from ctypes.wintypes import *
from typing import Optional


shell32 = windll.shell32

class SHELLEXECUTEINFOW(Structure):
	_fields_ = (
		("cbSize", DWORD),
		("fMask", ULONG),
		("hwnd", HWND),
		("lpVerb", LPCWSTR),
		("lpFile", LPCWSTR),
		("lpParameters", LPCWSTR),
		("lpDirectory", LPCWSTR),
		("nShow", c_int),
		("hInstApp", HINSTANCE),
		("lpIDList", LPVOID),
		("lpClass", LPCWSTR),
		("hkeyClass", HKEY),
		("dwHotKey", DWORD),
		("hIconOrMonitor", HANDLE),
		("hProcess", HANDLE),
	)
	def __init__(self, **kwargs):
		super(SHELLEXECUTEINFOW, self).__init__(cbSize=sizeof(self), **kwargs)
SHELLEXECUTEINFO = SHELLEXECUTEINFOW

SEE_MASK_NOCLOSEPROCESS = 0x00000040


def ShellExecute(
		hwnd: Optional[int],
		operation: Optional[str],
		file: str,
		parameters: Optional[str],
		directory: Optional[str],
		showCmd: int
) -> None:
	if not file:
		raise RuntimeError("file cannot be None")
	if shell32.ShellExecuteW(hwnd, operation, file, parameters, directory, showCmd) <= 32:
		raise WinError()


def ShellExecuteEx(execInfo):
	if not shell32.ShellExecuteExW(byref(execInfo)):
		raise WinError()

FILEOP_FLAGS=WORD

FO_MOVE=1
FO_COPY=2
FO_DELETE=3
FO_RENAME=4

FOF_NOCONFIRMMKDIR=0x200

class SHFILEOPSTRUCT(Structure):
	_fields_=[
		('hwnd',HWND),
		('wFunc',c_uint),
		('pFrom',c_wchar_p),
		('pTo',c_wchar_p),
		('fFlags',FILEOP_FLAGS),
		('fAnyOperationsAborted',BOOL),
		('hNameMapping',c_void_p),
		('lpszProgressTitle',c_wchar_p),
	]

	
SHCNE_ASSOCCHANGED=0x08000000
SHCNF_IDLIST=0x0
shell32.SHChangeNotify.argtypes = [c_long, c_uint, c_void_p, c_void_p]
shell32.SHChangeNotify.restype = None
def SHChangeNotify(wEventId, uFlags, dwItem1, dwItem2):
	shell32.SHChangeNotify(wEventId, uFlags, dwItem1, dwItem2)
