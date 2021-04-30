# louisHelper.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018 NV Access Limited, Babbage B.V.

"""Helper module to ease communication to and from liblouis."""

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
