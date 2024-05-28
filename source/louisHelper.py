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
from typing import Generator

import brailleTables
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


def _resolveTableInner(tables: list[str], base: str | None = None) -> Generator[str, None, None]:
	"""Helper function to resolve braille table file names to file paths.
	This is used by the L{_resolveTable} function to abstract the inner workings
	from the ctypes related conversion of input and output.
	:param tables: List of table names.
	:param base: The base table (e.g. the table that contains include opcodes for the given tables).
	:returns: A generator that yields the paths for the requested tables.
	"""
	for table in tables:
		if _isDebug():
			log.debug(f"Resolving {table!r}")
		directoriesToSearch = [brailleTables.TABLES_DIR]
		path = None
		if base is None:
			try:
				registeredTable = brailleTables.getTable(table)
				path = brailleTables._tablesDirs.get(registeredTable.source)
			except LookupError:
				if _isDebug():
					log.debug(f"Table {table!r} not registered, falling back to built-in table lookup")
		else:
			path = os.path.dirname(base)
		if path and path not in directoriesToSearch:
			directoriesToSearch.insert(0, path)
		for directory in directoriesToSearch:
			path = os.path.join(directory, table)
			if os.path.isfile(path):
				if _isDebug():
					log.debug(f"Resolved {table!r} to {path!r} for base {base!r}")
				yield path
				break
		else:
			raise LookupError(f"Could not resolve table {table!r}, looked in paths: {directoriesToSearch!r}")


# Note: liblouis table resolvers return char**,
# but POINTER(c_char_p) is unsupported as a ctypes callback return type.
@WINFUNCTYPE(c_void_p, c_char_p, c_char_p)
def _resolveTable(tablesList: bytes, base: bytes | None) -> int | None:
	"""Resolve braille table file names to file paths.

	Unlike the default table resolver from liblouis, this implementation does
	not confer any special role to the directory of the first table of the list
	and completely ignores the liblouis data path and the
	C{LOUIS_TABLEPATH} environment variable.
	Instead, when base is None, it fetches the tables as registered in the brailleTables module,
	If they point to an existing file, the value of the absolutePath property is returned.
	When base is not None, the imported table is either looked up in the same directory as the base table,
	or in the directory with the built-in tables.
	"""
	if _isDebug():
		log.debug(f"liblouis called table resolver wit params: tablesList={tablesList}, base={base}")
	tables = tablesList.decode(louis.fileSystemEncoding).split(",")
	if not tables:
		return None
	baseTable: str | None = base.decode(louis.fileSystemEncoding) if base is not None else None
	try:
		paths = [p.encode(louis.fileSystemEncoding) for p in _resolveTableInner(tables, baseTable)]
	except LookupError:
		log.exception()
		return None
	if _isDebug():
		log.debug(f"Storing paths in an array of {len(paths)} null terminated strings")
	# Keeping a reference to the last returned value to ensure the returned
	# value is not GC'ed before it is copied on liblouis' side.
	_resolveTable._lastRes = arr = (c_char_p * len(paths))(*paths)
	# ctypes calls c_void_p on the returned value.
	# Return the address of the array.
	address = addressof(arr)
	if _isDebug():
		log.debug(f"Returning pointer to list of paths: {address}")
	return address


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


def initialize():
	# Register the liblouis logging callback.
	louis.registerLogCallback(louis_log)
	# Set the log level to debug.
	# The NVDA logging callback will filter messages appropriately,
	# i.e. error messages will be logged at the error level.
	louis.setLogLevel(louis.LOG_DEBUG)
	# Register the liblouis table resolver
	louis.liblouis.lou_registerTableResolver(_resolveTable)


def terminate():
	# Set the log level to off.
	louis.setLogLevel(louis.LOG_OFF)
	# Unregister the table resolver.
	louis.liblouis.lou_registerTableResolver(None)
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
	text = inbuf.replace("\0", "")
	braille, brailleToRawPos, rawToBraillePos, brailleCursorPos = louis.translate(
		tableList,
		text,
		# liblouis mutates typeform if it is a list.
		typeform=tuple(typeform) if isinstance(typeform, list) else typeform,
		cursorPos=cursorPos or 0,
		mode=mode,
	)
	# liblouis gives us back a character string of cells, so convert it to a list of ints.
	# For some reason, the highest bit is set, so only grab the lower 8 bits.
	braille = [ord(cell) & 255 for cell in braille]
	if cursorPos is None:
		brailleCursorPos = None
	return braille, brailleToRawPos, rawToBraillePos, brailleCursorPos
