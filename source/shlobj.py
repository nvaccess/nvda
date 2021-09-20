# -*- coding: UTF-8 -*-
#shlobj.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2017 NV Access Limited, Babbage B.V.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""
This module wraps the SHGetFolderPath function in shell32.dll and defines the necessary contstants.
CSIDL (constant special item ID list) values provide a unique system-independent way to
identify special folders used frequently by applications, but which may not have the same name
or location on any given system. For example, the system folder may be "C:\Windows" on one system
and "C:\Winnt" on another. The CSIDL system is used to be compatible with Windows XP.
"""

from ctypes import *
from ctypes.wintypes import *

shell32 = windll.shell32

MAX_PATH = 260

#: The file system directory that serves as a common repository for application-specific data.
#: A typical path is C:\Documents and Settings\username\Application Data.
CSIDL_APPDATA = 0x001a
#: The file system directory that serves as a data repository for local (nonroaming) applications.
#: A typical path is C:\Documents and Settings\username\Local Settings\Application Data.
CSIDL_LOCAL_APPDATA = 0x001c
#: The file system directory that contains application data for all users.
#: A typical path is C:\Documents and Settings\All Users\Application Data.
#: This folder is used for application data that is not user specific.
CSIDL_COMMON_APPDATA = 0x0023

def SHGetFolderPath(owner, folder, token=0, flags=0):
	path = create_unicode_buffer(MAX_PATH)
	# Note  As of Windows Vista, this function is merely a wrapper for SHGetKnownFolderPath
	if shell32.SHGetFolderPathW(owner, folder, token, flags, byref(path)) != 0:
		raise WinError()
	return path.value
