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

charHookLib=None

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
		log.error("charHook.winEventCallback", exc_info=True)

def initialize():
	global charHookLib, winEventHookID
	charHookLib=ctypes.windll.LoadLibrary('lib/charHook.dll')
	charHookLib.initialize()
	winEventHookID=winUser.setWinEventHook(EVENT_TYPEDCHARACTER,EVENT_INPUTLANGCHANGE,0,winEventCallback,0,0,0)

def terminate():
	global charHookLib
	winUser.unhookWinEvent(winEventHookID)
	charHookLib.terminate()
	del charHookLib
