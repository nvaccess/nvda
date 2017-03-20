import winVersion
from comtypes import COMError
import config
from logHandler import log

handler=None
isUIAAvailable=False

if config.conf and config.conf["UIA"]["enabled"]:
	winver=winVersion.winVersion.major+(winVersion.winVersion.minor/10.0)
	if winver>=config.conf["UIA"]["minWindowsVersion"]:
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
