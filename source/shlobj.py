# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2009-2021 NV Access Limited, Babbage B.V., Łukasz Golonka
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

r"""
This module wraps the `SHGetKnownFolderPath` function in shell32.dll and defines the necessary contstants.
Known folder ids provide a unique system-independent way to
identify special folders used frequently by applications, but which may not have the same name
or location on any given system. For example, the system folder may be "C:\Windows" on one system
and "C:\Winnt" on another.
"""

import comtypes
import ctypes
from enum import Enum
import functools
from typing import Optional, Union


class FolderId(str, Enum):
	"""Contains guids of known folders from Knownfolders.h. Full list is availabe at:
	https://docs.microsoft.com/en-us/windows/win32/shell/knownfolderid"""
	#: The file system directory that serves as a common repository for application-specific data.
	#: A typical path is C:\Documents and Settings\username\Application Data.
	ROAMING_APP_DATA = "{3EB685DB-65F9-4CF6-A03A-E3EF65729F3D}"
	#: The file system directory that serves as a data repository for local (nonroaming) applications.
	#: A typical path is C:\Documents and Settings\username\Local Settings\Application Data.
	LOCAL_APP_DATA = "{F1B32785-6FBA-4FCF-9D55-7B8E7F157091}"
	#: The file system directory that contains application data for all users.
	#: A typical path is C:\Documents and Settings\All Users\Application Data.
	#: This folder is used for application data that is not user specific.
	PROGRAM_DATA = "{62AB5D82-FDC1-4DC3-A9DD-070D1D495D97}"
	#  The Windows System folder.
	# A typical path is C:\Windows\System32.
	SYSTEM = "{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}"
	SYSTEM_X86 = "{D65231B0-B2F1-4857-A4CE-A8E7C6EA7D27}"


@functools.lru_cache(maxsize=128)
def SHGetKnownFolderPath(
		folderGuid: Union[FolderId, str],
		dwFlags: int = 0,
		hToken: Optional[int] = None
) -> str:
	"""Wrapper for `SHGetKnownFolderPath` which caches the results
	to avoid calling the win32 function unnecessarily."""
	if isinstance(folderGuid, FolderId):
		folderGuid = folderGuid.value
	guid = comtypes.GUID(folderGuid)

	pathPointer = ctypes.c_wchar_p()
	res = ctypes.windll.shell32.SHGetKnownFolderPath(
		comtypes.byref(guid),
		dwFlags,
		hToken,
		ctypes.byref(pathPointer)
	)
	if res != 0:
		raise RuntimeError(f"SHGetKnownFolderPath failed with error code {res}")
	path = pathPointer.value
	ctypes.windll.ole32.CoTaskMemFree(pathPointer)
	return path
