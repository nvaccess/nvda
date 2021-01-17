#UIAHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2008-2018 NV Access Limited, Joseph Lee
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from comtypes import COMError
import config
from logHandler import log
# Maintain backwards compatibility: F403 (unable to detect undefined names) flake8 warning.
from _UIAHandler import *  # noqa: F403

# Make the _UIAHandler._isDebug function available to this module,
# ignoring the fact that it is not used here directly.
from _UIAHandler import _isDebug   # noqa: F401

handler=None

def initialize():
	global handler
	if not config.conf["UIA"]["enabled"]:
		raise RuntimeError("UIA forcefully disabled in configuration")
	try:
		handler=UIAHandler()
	except COMError:
		handler=None
		raise

def terminate():
	global handler
	if handler:
		handler.terminate()
		handler=None
