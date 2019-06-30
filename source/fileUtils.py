#fileUtils.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2017-2019 NV Access Limited, Bram Duvigneau
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import ctypes
import ctypes.wintypes
import array
from contextlib import contextmanager
from tempfile import NamedTemporaryFile
from logHandler import log
from six import text_type
import winKernel

@contextmanager
def FaultTolerantFile(name):
	'''Used to write out files in a more fault tolerant way. A temporary file is used, and replaces the 
	file `name' when the context manager scope ends and the the context manager __exit__ is called. This
	means writing out the complete file can be performed with less concern of corrupting the original file
	if the process is interrupted by windows shutting down.
	`name` must be unicode.

	Usage:
		with FaultTolerantFile("myFile.txt") as f:
			f.write("This is a test")

	This creates a temporary file, and the writes actually happen on this temp file. At the end of the 
	`with` block, when `f` goes out of context the temporary file is closed and, this temporary file replaces "myFile.txt"
	'''
	if not isinstance(name, text_type):
		raise TypeError("name must be an unicode string")
	dirpath, filename = os.path.split(name)
	with NamedTemporaryFile(dir=dirpath, prefix=filename, suffix='.tmp', delete=False) as f:
		log.debug(f.name)
		yield f
		f.flush()
		os.fsync(f)
		f.close()
		winKernel.moveFileEx(f.name, name, winKernel.MOVEFILE_REPLACE_EXISTING)

def getFileVersionInfo(name, *attributes):
	"""Gets the specified file version info attributes from the provided file."""
	if not isinstance(name, text_type):
		raise TypeError("name must be an unicode string")
	if not os.path.exists(name):
		raise RuntimeError("The file %s does not exist" % name)
	fileVersionInfo = {}
	# Get size needed for buffer (0 if no info)
	size = ctypes.windll.version.GetFileVersionInfoSizeW(name, None)
	if not size:
		raise RuntimeError("No version information")
	# Create buffer
	res = ctypes.create_string_buffer(size)
	# Load file informations into buffer res
	ctypes.windll.version.GetFileVersionInfoW(name, None, size, res)
	r = ctypes.c_uint()
	l = ctypes.c_uint()
	# Look for codepages
	ctypes.windll.version.VerQueryValueW(res, u'\\VarFileInfo\\Translation',
		ctypes.byref(r), ctypes.byref(l))
	if not l.value:
		raise RuntimeError("No codepage")
	# Take the first codepage (what else ?)
	codepage = array.array('H', ctypes.string_at(r.value, 4))
	codepage = "%04x%04x" % tuple(codepage)
	for attr in attributes:
		if not ctypes.windll.version.VerQueryValueW(res,
			u'\\StringFileInfo\\%s\\%s' % (codepage, attr),
			ctypes.byref(r), ctypes.byref(l)
		):
			log.warning("Invalid or unavailable version info attribute for %r: %s" % (name, attr))
			fileVersionInfo[attr] = None
		else:
			fileVersionInfo[attr] = ctypes.wstring_at(r.value, l.value-1)
	return fileVersionInfo
