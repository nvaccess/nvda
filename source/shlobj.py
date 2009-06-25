#shlobj.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from ctypes import *
from ctypes.wintypes import *

shell32 = windll.shell32

MAX_PATH = 260

CSIDL_APPDATA = 0x001a
CSIDL_COMMON_APPDATA = 0x0023

def SHGetFolderPath(owner, folder, token=0, flags=0):
	path = create_unicode_buffer(MAX_PATH)
	if shell32.SHGetFolderPathW(owner, folder, token, flags, byref(path)) != 0:
		raise WinError()
	return path.value
