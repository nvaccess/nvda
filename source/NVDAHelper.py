import struct
import locale
import ctypes
import keyboardHandler
import winUser
import speech
import queueHandler
import api
import globalVars
from logHandler import log

EVENT_TYPEDCHARACTER=0X1000
EVENT_INPUTLANGCHANGE=0X1001

helperLib=None

winEventHookID=None

def handleTypedCharacter(window,wParam,lParam):
	if wParam>=32:
		queueHandler.queueFunction(queueHandler.eventQueue,speech.speakTypedCharacters,unichr(wParam))

@ctypes.CFUNCTYPE(ctypes.c_voidp,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int)
def winEventCallback(handle,eventID,window,objectID,childID,threadID,timestamp):
	try:
		if eventID==EVENT_TYPEDCHARACTER:
			handleTypedCharacter(window,objectID,childID)
		elif eventID==EVENT_INPUTLANGCHANGE:
			keyboardHandler.speakKeyboardLayout(childID)
	except:
		log.error("helper.winEventCallback", exc_info=True)

def initialize():
	global helperLib, winEventHookID
	helperLib=ctypes.windll.LoadLibrary('lib/NVDAHelper.dll')
	helperLib.initialize()
	winEventHookID=winUser.setWinEventHook(EVENT_TYPEDCHARACTER,EVENT_INPUTLANGCHANGE,0,winEventCallback,0,0,0)

def terminate():
	global helperLib
	winUser.unhookWinEvent(winEventHookID)
	helperLib.terminate()
	del helperLib
