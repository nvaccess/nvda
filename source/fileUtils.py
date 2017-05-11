#fileUtils.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2017 NV Access Limited, Bram Duvigneau
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
import os
import ctypes
from contextlib import contextmanager
from tempfile import NamedTemporaryFile
from logHandler import log

#: Constant; flag for MoveFileEx(). If a file with the destination filename already exists, it is overwritten.
MOVEFILE_REPLACE_EXISTING = 1

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
	if not isinstance(name, unicode):
		raise TypeError("name must be unicode")
	dirpath, filename = os.path.split(name)
	with NamedTemporaryFile(dir=dirpath, prefix=filename, suffix='.tmp', delete=False) as f:
		log.debug(f.name)
		yield f
		f.flush()
		os.fsync(f)
		f.close()
		moveFileResult = ctypes.windll.kernel32.MoveFileExW(f.name, name, MOVEFILE_REPLACE_EXISTING)
		if moveFileResult == 0:
			raise ctypes.WinError()
