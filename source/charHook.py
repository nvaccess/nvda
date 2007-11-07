import ctypes
import debug
import keyboardHandler
import winUser
import speech
import queueHandler
import api

EVENT_TYPEDCHARACTER=0X1000
EVENT_INPUTLANGCHANGE=0X1001

charHookLib=None

@ctypes.CFUNCTYPE(ctypes.c_voidp,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int)
def winEventCallback(handle,eventID,window,objectID,childID,threadID,timestamp):
	try:
		foregroundWindow=api.getForegroundObject().windowHandle
		if eventID==EVENT_TYPEDCHARACTER and (window==foregroundWindow or winUser.isDescendantWindow(foregroundWindow,window)):
			ch=unichr(objectID)
			if ord(ch)>=32:
				queueHandler.queueFunction(queueHandler.eventQueue,speech.speakTypedCharacters,ch)
		elif eventID==EVENT_INPUTLANGCHANGE and (window==foregroundWindow or winUser.isDescendantWindow(foregroundWindow,window)):
			keyboardHandler.speakKeyboardLayout(childID)
	except:
		debug.writeException("charHook.winEventCallback")

def initialize():
	global charHookLib
	charHookLib=ctypes.windll.charHook
	charHookLib.initialize()
	winEventHookID=winUser.setWinEventHook(EVENT_TYPEDCHARACTER,EVENT_INPUTLANGCHANGE,0,winEventCallback,0,0,0)

def terminate():
	global charHookLib
	charHookLib.terminate()
	del charHookLib
