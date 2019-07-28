from ctypes import *
from ctypes.wintypes import *
import textUtils

"""
Lower level utility functions and constants for NVDA's
legacy Windows console support, for situations where UIA isn't available.
"""

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

class CHAR_INFO(Structure):
	_fields_ = [
		('Char', c_wchar), #union of char and wchar_t isn't needed since we deal only with unicode
		('Attributes', WORD)
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
	# Use a string buffer, as from an unicode buffer, we can't get the raw data.
	buf=create_string_buffer(length * 2)
	numCharsRead=c_int()
	if windll.kernel32.ReadConsoleOutputCharacterW(handle,buf,length,COORD(x,y),byref(numCharsRead))==0:
		raise WinError()
	return textUtils.getTextFromRawBytes(buf.raw, numChars=numCharsRead.value, encoding=textUtils.WCHAR_ENCODING)

def ReadConsoleOutput(handle, length, rect):
	BufType=CHAR_INFO*length
	buf=BufType()
	#rect=SMALL_RECT(x, y, x+length-1, y)
	if windll.kernel32.ReadConsoleOutputW(handle, buf, COORD(rect.Right-rect.Left+1, rect.Bottom-rect.Top+1), COORD(0,0), byref(rect))==0:
		raise WinError()
	return buf

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
