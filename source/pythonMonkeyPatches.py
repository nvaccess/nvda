#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2013 NVDA Contributors <http://www.nvda-project.org/>
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
