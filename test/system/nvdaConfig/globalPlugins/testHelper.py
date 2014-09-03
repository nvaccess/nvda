#test/system/nvdaConfig/globalPlugins/testHelper.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2014 NV Access Limited

"""Provides functionality enabling system tests to interface with NVDA.
This is done via the remote Python console.
"""

import logging
import globalPluginHandler
import remotePythonConsole
from logHandler import log

class RequestHandler(remotePythonConsole.BaseRequestHandler):

	# LogFilter
	def filter(self, record):
		if record.levelno == log.IO:
			if record.codepath in ("speech.speak", "braille.BrailleBuffer.update", "braille.BrailleHandler.update"):
				return True
		return False

	# Stream passed to the log handler
	def write(self, text):
		self.output(text)
	def flush(self):
		self.wfile.flush()

	def handle(self):
		logHandler = logging.StreamHandler(self)
		logHandler.setFormatter(logging.Formatter(
			"PRES %(message)r"))
		logHandler.addFilter(self)
		log.addHandler(logHandler)
		remotePythonConsole.BaseRequestHandler.handle(self)
		log.removeHandler(logHandler)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self):
		super(GlobalPlugin, self).__init__()
		remotePythonConsole.RequestHandler = RequestHandler
		remotePythonConsole.initialize(host="127.0.0.1", port=6838)

	def terminate(self):
		remotePythonConsole.terminate()
