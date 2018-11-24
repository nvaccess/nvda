#louisHelper.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018 NV Access Limited, Babbage B.V.

"""Helper module to ease communication to and from liblouis."""

import louis
from logHandler import log

LOUIS_TO_NVDA_LOG_LEVELS = {
	louis.LOG_ALL: log.DEBUG,
	louis.LOG_DEBUG: log.DEBUG,
	louis.LOG_INFO: log.INFO,
	louis.LOG_WARN: log.WARNING,
	louis.LOG_ERROR: log.ERROR,
	louis.LOG_FATAL: log.ERROR,
}

@louis.logcallback
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
	# The NVDA logging callback will filter messages appropriately.
	louis.setLogLevel(louis.LOG_DEBUG)

def terminate():
	# Set the log level to off.
	louis.setLogLevel(louis.LOG_OFF)
	# Unregister the liblouis logging callback.
	louis.registerLogCallback(None)
