# louisHelper.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2021 NV Access Limited, Babbage B.V., Julien Cochuyt

"""Helper module to ease communication to and from liblouis."""

from ctypes import (
	WINFUNCTYPE,
	c_char_p,
	c_void_p,
	cast,
)
import os
from typing import List
import louis
from logHandler import log
import config


LOUIS_TO_NVDA_LOG_LEVELS = {
	louis.LOG_ALL: log.DEBUG,
	louis.LOG_DEBUG: log.DEBUG,
	louis.LOG_INFO: log.INFO,
	louis.LOG_WARN: log.WARNING,
	louis.LOG_ERROR: log.ERROR,
	louis.LOG_FATAL: log.ERROR,
}

_tablesDirs = []


@WINFUNCTYPE(c_void_p, c_char_p, c_char_p)
def _resolveTable(tablesList, base):
	"""Resolve braille table file names to file paths.
	
	Unlike the default table resolver from liblouis, this implementation does
	not confer any special role to the directory of the first table of the list
	and completely ignores the C{base} parameter, the liblouis data path and the
	C{LOUIS_TABLEPATH} environment variable.
	Instead, it only considers a list of directories (passed from
	L{brailleTables} by L{braille.BrailleHandler}) and search in those a match
	with the relative paths found in C{tableList}.
	If they point to an existing file, absolute paths in L{tablesList} are
	returned as-is.
	"""
	# We only receive ASCII for now, but it will most likely be MBCS once liblouis issue #698 is fixed.
	tables = tablesList.decode("mbcs").split(",")
	paths = []
	for table in tables:
		for dir_ in _tablesDirs:
			# L{os.path.join} returns a path relative to the first absolute path.
			# That is, if L{table} is absolute, it is returned unchanged.
			path = os.path.join(dir_, table)
			if os.path.isfile(path):
				# This already works without liblouis issue #698 being fixed.
				# That is, table file names cannot (yet) contain non-ASCII characters,
				# but the name of the directory in which they are located can.
				paths.append(path.encode("mbcs"))
				if _isDebug():
					log.debug(f"Resolved \"{table}\" to \"{path}\"")
				break
		else:
			if _isDebug():
				log.error(f"Could not resolve table \"{table}\". Search paths: {_tablesDirs}")
			return None
	# Keeping a reference to the last returned value to ensure the returned
	# value is not GC'ed before it is copied on liblouis' side.
	# See https://github.com/liblouis/liblouis/issues/315
	_resolveTable.lastRes = arr = (c_char_p * len(paths))(*paths)
	# ctypes calls c_void_p on the returned value.
	# See https://bugs.python.org/issue1574593#msg30207
	return cast(arr, c_void_p).value


@louis.LogCallback
def louis_log(level, message):
	if not _isDebug():
		return
	NVDALevel = LOUIS_TO_NVDA_LOG_LEVELS.get(level, log.DEBUG)
	if not log.isEnabledFor(NVDALevel):
		return
	message = message.decode("ASCII")
	codepath = "liblouis at internal log level %d" % level
	log._log(NVDALevel, message, [], codepath=codepath)

def _isDebug():
	return config.conf["debugLog"]["louis"]


def initialize(tablesDirs: List[str]):
	if _isDebug():
		log.debug(f"Tables directories: {tablesDirs}")
	# Register the liblouis logging callback.
	louis.registerLogCallback(louis_log)
	# Set the log level to debug.
	# The NVDA logging callback will filter messages appropriately,
	# i.e. error messages will be logged at the error level.
	louis.setLogLevel(louis.LOG_DEBUG)
	# Register the liblouis table resolver
	global _tablesDirs
	_tablesDirs = tablesDirs
	louis.liblouis.lou_registerTableResolver(_resolveTable)

def terminate():
	# Set the log level to off.
	louis.setLogLevel(louis.LOG_OFF)
	# Unregister the liblouis logging callback.
	louis.registerLogCallback(None)
	# Free liblouis resources
	louis.liblouis.lou_free()

def translate(tableList, inbuf, typeform=None, cursorPos=None, mode=0):
	"""
	Convenience wrapper for louis.translate that:
	* returns a list of integers instead of a string with cells, and
	* distinguishes between cursor position 0 (cursor at first character) and None (no cursor at all)
	"""
	text = inbuf.replace('\0','')
	braille, brailleToRawPos, rawToBraillePos, brailleCursorPos = louis.translate(
		tableList,
		text,
		# liblouis mutates typeform if it is a list.
		typeform=tuple(typeform) if isinstance(typeform, list) else typeform,
		cursorPos=cursorPos or 0,
		mode=mode
	)
	# liblouis gives us back a character string of cells, so convert it to a list of ints.
	# For some reason, the highest bit is set, so only grab the lower 8 bits.
	braille = [ord(cell) & 255 for cell in braille]
	if cursorPos is None:
		brailleCursorPos = None
	return braille, brailleToRawPos, rawToBraillePos, brailleCursorPos
