import struct
import locale
from ctypes import *
import keyboardHandler
import winUser
import speech
import eventHandler
import queueHandler
import api
import globalVars
from logHandler import log

EVENT_TYPEDCHARACTER=0X1000
EVENT_INPUTLANGCHANGE=0X1001

remoteLib=None
localLib=None

winEventHookID=None

def handleTypedCharacter(window,wParam,lParam):
	focus=api.getFocusObject()
	if focus.windowClassName!="ConsoleWindowClass":
		eventHandler.queueEvent("typedCharacter",focus,ch=unichr(wParam))

@winUser.WINEVENTPROC
def winEventCallback(handle,eventID,window,objectID,childID,threadID,timestamp):
	try:
		if eventID==EVENT_TYPEDCHARACTER:
			handleTypedCharacter(window,objectID,childID)
		elif eventID==EVENT_INPUTLANGCHANGE:
			keyboardHandler.speakKeyboardLayout(childID)
	except:
		log.error("helper.winEventCallback", exc_info=True)

def initialize():
	global remoteLib, localLib, winEventHookID
	localLib=cdll.LoadLibrary('lib/nvdaHelperLocal.dll')
	remoteLib=cdll.LoadLibrary('lib/NVDAHelperRemote.dll')
	if remoteLib.nvdaHelper_initialize() < 0:
		raise RuntimeError("Error initializing NVDAHelper")
	winEventHookID=winUser.setWinEventHook(EVENT_TYPEDCHARACTER,EVENT_INPUTLANGCHANGE,0,winEventCallback,0,0,0)

def terminate():
	global remoteLib, localLib
	winUser.unhookWinEvent(winEventHookID)
	if remoteLib.nvdaHelper_terminate() < 0:
		raise RuntimeError("Error terminating NVDAHelper")
	remoteLib=None
	localLib=None
