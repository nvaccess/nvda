# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2009-2021 NV Access Limited, Babbage B.V.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

r"""
This module wraps the SHGetFolderPath function in shell32.dll and defines the necessary contstants.
CSIDL (constant special item ID list) values provide a unique system-independent way to
identify special folders used frequently by applications, but which may not have the same name
or location on any given system. For example, the system folder may be "C:\Windows" on one system
and "C:\Winnt" on another. The CSIDL system is used to be compatible with Windows XP.
"""

from ctypes import byref, create_unicode_buffer, windll, WinError
import enum
import typing

shell32 = windll.shell32

MAX_PATH = 260


class CSIDL(enum.IntEnum):
	#: The file system directory that serves as a common repository for application-specific data.
	#: A typical path is C:\Documents and Settings\username\Application Data.
	APPDATA = 0x001a
	#: The file system directory that serves as a data repository for local (nonroaming) applications.
	#: A typical path is C:\Documents and Settings\username\Local Settings\Application Data.
	LOCAL_APPDATA = 0x001c
	#: The file system directory that contains application data for all users.
	#: A typical path is C:\Documents and Settings\All Users\Application Data.
	#: This folder is used for application data that is not user specific.
	COMMON_APPDATA = 0x0023
	#  The Windows System folder.
	# A typical path is C:\Windows\System32.
	SYSTEM = 0x25
	SYSTEMX86 = 0x29


def SHGetFolderPath(owner: typing.Union[None, int], folder: CSIDL, token: int = 0, flags: int = 0) -> str:
	path = create_unicode_buffer(MAX_PATH)
	# Note  As of Windows Vista, this function is merely a wrapper for SHGetKnownFolderPath
	if shell32.SHGetFolderPathW(owner, folder, token, flags, byref(path)) != 0:
		raise WinError()
	return path.value
