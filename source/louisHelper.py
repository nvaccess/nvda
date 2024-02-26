# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2024 NV Access Limited, Babbage B.V., Julien Cochuyt, Leonard de Ruijter

"""Helper module to ease communication to and from liblouis."""

import os
from ctypes import (
	WINFUNCTYPE,
	addressof,
	c_char_p,
	c_void_p,
)

import config
import globalVars
from logHandler import log

with os.add_dll_directory(globalVars.appDir):
	import louis


LOUIS_TO_NVDA_LOG_LEVELS = {
	louis.LOG_ALL: log.DEBUG,
	louis.LOG_DEBUG: log.DEBUG,
	louis.LOG_INFO: log.INFO,
	louis.LOG_WARN: log.WARNING,
	louis.LOG_ERROR: log.ERROR,
	louis.LOG_FATAL: log.ERROR,
}

_tablesDirs = []


# Note: liblouis table resolvers return char**,
# but POINTER(c_char_p) is unsupported as a ctypes callback return type.
@WINFUNCTYPE(c_void_p, c_char_p, c_char_p)
def _resolveTable(tablesList: str, base: str) -> int | None:
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
	tables = tablesList.decode(louis.fileSystemEncoding).split(",")
	paths = []
	for table in tables:
		for dir_ in _tablesDirs:
			# L{os.path.join} returns a path relative to the first absolute path.
			# That is, if L{table} is absolute, it is returned unchanged.
			path = os.path.join(dir_, table)
			if os.path.isfile(path):
				paths.append(path.encode(louis.fileSystemEncoding))
				if _isDebug():
					log.debug(f"Resolved \"{table}\" to \"{path}\"")
				break
		else:
			if _isDebug():
				log.error(f"Could not resolve table \"{table}\". Search paths: {_tablesDirs}")
			return None
	if not paths:
		return None
	arr = (c_char_p * len(paths))(*paths)
	# ctypes calls c_void_p on the returned value.
	# Return the address of the array.
	return addressof(arr)


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


def initialize(tablesDirs: list[str]):
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
