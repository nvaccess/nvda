#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2013-2017 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Fixes some broken features in Python such as gettempdir"""

# #2729: Python's tempfile.get_default_tempdir() has a bug when handling multibyte paths. os.path.normcase is used incorrectly.
# Override this to use the temp path as returned by Windows.
import ctypes
import tempfile
tempPath = ctypes.create_string_buffer(260)
if ctypes.windll.kernel32.GetTempPathA(260, tempPath) > 0:
	# Strip trailing backslash which is always included.
	tempfile.tempdir = tempPath.value[:-1]

# #6705: ctypes._dlopen (imported from _ctypes.LoadLibrary) doesn't support unicode paths.
# In Python < 2.7.13, it silently converted them to str, treating them as ASCII.
# In Python 2.7.13 (Python issue 27330), passing unicode now throws an exception.
# Some add-ons depend on the previous behaviour, so monkey patch this to support unicode.
old_dlopen = ctypes._dlopen
def _dlopen(name, mode=ctypes.DEFAULT_MODE):
	if isinstance(name, unicode):
		name = name.encode("mbcs")
	return old_dlopen(name, mode)
ctypes._dlopen = _dlopen
