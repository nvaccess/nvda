#UIAHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2008-2018 NV Access Limited, Joseph Lee
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from comtypes import COMError
import config
from logHandler import log

handler=None
isUIAAvailable=False

if config.conf and config.conf["UIA"]["enabled"]:
	# Because Windows 7 SP1 (NT 6.1) or later is supported, just assume UIA can be used unless told otherwise.
	try:
		from _UIAHandler import *
		isUIAAvailable=True
	except ImportError:
		log.debugWarning("Unable to import _UIAHandler",exc_info=True)
		pass

def initialize():
	global handler
	if not isUIAAvailable:
		raise NotImplementedError
	try:
		handler=UIAHandler()
	except COMError:
		handler=None
		raise RuntimeError("UIA not available")

def terminate():
	global handler
	if handler:
		handler.terminate()
		handler=None
