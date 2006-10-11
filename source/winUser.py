import struct
import ctypes
import win32api

user32=ctypes.windll.user32

class hiLoWordType(ctypes.Structure):
	_fields_=[
	('lo',ctypes.c_short),
	('hi',ctypes.c_short),
	]

class pointType(ctypes.Structure):
	_fields_=[
	('x',ctypes.c_int),
	('y',ctypes.c_int),
	]

class msgType(ctypes.Structure):
	_fields_=[
	('hwnd',ctypes.c_int),
	('message',ctypes.c_int),
	('wParam',ctypes.c_int),
	('lParam',ctypes.c_int),
	('time',ctypes.c_int),
	('pt',pointType),
	]

def unpackWords(bytes):
	byteString=struct.pack('i',bytes)
	return struct.unpack('hh',byteString)

def old_LOWORD(bytes):
	(hi,lo)=unpackWords(bytes)
	return lo

def old_HIWORD(bytes):
	(hi,lo)=unpackWords(bytes)
	return hi

def LOWORD(bytes):
	return win32api.LOWORD(bytes)

def HIWORD(bytes):
	return win32api.HIWORD(bytes)

def waitMessage():
	return user32.WaitMessage()

def getMessage(*args):
	return user32.GetMessageW(*args)

def translateMessage(*args):
	return user32.TranslateMessage(*args)

def dispatchMessage(*args):
	return user32.DispatchMessageW(*args)

def peekMessage(*args):
	return user32.PeekMessageW(*args)

def isWindow(hwnd):
	return user32.IsWindow(hwnd)

def isDecendantWindow(parentHwnd,childHwnd):
	if (parentHwnd==childHwnd) or user32.IsChild(parentHwnd,childHwnd):
		return True
	else:
		return False

def getForegroundWindow():
	return user32.GetForegroundWindow()

def getControlID(hwnd):
	return user32.GetWindowLong(hwnd)

def getClientRect(hwnd):
	return user32.GetClientRect(hwnd)

def setWinEventHook(*args):
		return user32.SetWinEventHook(*args)

def unhookWinEvent(*args):
	return user32.UnhookWinEvent(*args)

def sendMessage(*args):
	return user32.SendMessageW(*args)

def getWindowThreadProcessID(hwnd):
	processID=ctypes.c_int()
	threadID=user32.GetWindowThreadProcessId(hwnd,ctypes.byref(processID))
	return (processID.value,threadID)

def getClassName(window):
	buf=ctypes.create_unicode_buffer(256)
	user32.GetClassNameW(window,buf,255)
	return buf.value

def keybd_event(*args):
	return user32.keybd_event(*args)

