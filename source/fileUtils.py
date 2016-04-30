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