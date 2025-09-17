# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from ctypes import *  # noqa: F403
from ctypes.wintypes import *  # noqa: F403
from typing import Optional
import winBindings.shell32
from utils import _deprecate


__getattr__ = _deprecate.handleDeprecations(
	_deprecate.MovedSymbol("SHELLEXECUTEINFO", "winBindings.shell32"),
	_deprecate.MovedSymbol("SHELLEXECUTEINFOW", "winBindings.shell32"),
	_deprecate.MovedSymbol("shell32", "winBindings.shell32", "dll"),
)

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
	if winBindings.shell32.ShellExecute(hwnd, operation, file, parameters, directory, showCmd) <= 32:
		raise WinError()  # noqa: F405


def ShellExecuteEx(execInfo):
	if not winBindings.shell32.ShellExecuteEx(byref(execInfo)):  # noqa: F405
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


def SHChangeNotify(wEventId, uFlags, dwItem1, dwItem2):
	winBindings.shell32.SHChangeNotify(wEventId, uFlags, dwItem1, dwItem2)
