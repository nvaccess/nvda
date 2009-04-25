from ctypes import *
from ctypes.wintypes import *

CONSOLE_REAL_OUTPUT_HANDLE=-2

class COORD(Structure):
	_fields_=[
		('x',c_short),
		('y',c_short),
	]

class CONSOLE_SCREEN_BUFFER_INFO(Structure):
	_fields_=[
		('dwSize',COORD),
		('dwCursorPosition',COORD),
		('wAttributes',WORD),
		('srWindow',SMALL_RECT),
		('dwMaximumWindowSize',COORD),
	]

class CONSOLE_SELECTION_INFO(Structure):
	_fields_=[
		('dwFlags',DWORD),
		('dwSelectionAnchor',COORD),
		('srSelection',SMALL_RECT),
	]

PHANDLER_ROUTINE=WINFUNCTYPE(BOOL,DWORD)

CTRL_C_EVENT=0
CTRL_BREAK_EVENT=1
CTRL_CLOSE_EVENT=2

CONSOLE_NO_SELECTION=0X0
CONSOLE_SELECTION_IN_PROGRESS=0X1
CONSOLE_SELECTION_NOT_EMPTY=0x2
CONSOLE_MOUSE_SELECTION=0X4
CONSOLE_MOUSE_DOWN=0x8

def GetConsoleSelectionInfo():
	info=CONSOLE_SELECTION_INFO()
	if windll.kernel32.GetConsoleSelectionInfo(byref(info))==0:
		raise WinError()
	return info

def ReadConsoleOutputCharacter(handle,length,x,y):
	buf=create_unicode_buffer(length)
	numCharsRead=c_int()
	if windll.kernel32.ReadConsoleOutputCharacterW(handle,buf,length,COORD(x,y),byref(numCharsRead))==0:
		raise WinError()
	return buf.value

def GetConsoleScreenBufferInfo(handle):
	info=CONSOLE_SCREEN_BUFFER_INFO()
	if windll.kernel32.GetConsoleScreenBufferInfo(handle,byref(info))==0:
		raise WinError()
	return info

def FreeConsole():
	if windll.kernel32.FreeConsole()==0:
		raise WinError()

def AttachConsole(processID):
	if windll.kernel32.AttachConsole(processID)==0:
		raise WinError()

def GetConsoleWindow():
	return windll.kernel32.GetConsoleWindow()

def GetConsoleProcessList(maxProcessCount):
	processList=(c_int*maxProcessCount)()
	num=windll.kernel32.GetConsoleProcessList(processList,maxProcessCount)
	return processList[0:num]

def SetConsoleCtrlHandler(handler,add):
	if windll.kernel32.SetConsoleCtrlHandler(handler,add)==0:
		raise WinError()
