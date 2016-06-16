#fileUtils.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2016 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
import os
import osreplace
from contextlib import contextmanager
from tempfile import NamedTemporaryFile
from logHandler import log

@contextmanager
def FaultTolerantFile(name):
	dirpath, filename = os.path.split(name)
	with NamedTemporaryFile(dir=dirpath, prefix=filename, suffix='.tmp', delete=False) as f:
		log.debug(f.name)
		yield f
		f.flush()
		os.fsync(f)
		f.close()
		osreplace.replace(f.name, name)