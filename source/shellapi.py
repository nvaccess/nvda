#shellapi.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from ctypes import *
from ctypes.wintypes import *

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

def ShellExecute(hwnd, operation, file, parameters, directory, showCmd):
	if shell32.ShellExecuteW(hwnd, operation, file, parameters, directory, showCmd) <= 32:
		raise WinError()

def ShellExecuteEx(execInfo):
	if not shell32.ShellExecuteExW(byref(execInfo)):
		raise WinError()
