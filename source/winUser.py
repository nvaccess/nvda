#winUser.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Functions that wrap Windows API functions from user32.dll"""

import ctypes
import ctypes.wintypes

#dll handles
user32=ctypes.windll.user32

#win types
POINT=ctypes.wintypes.POINT
MSG=ctypes.wintypes.MSG

#constants
#ListBox
LB_GETCARETINDEX=415
LB_GETCOUNT=395
LB_GETTEXT=393
LB_GETTEXTLEN=394

#getAncestor
GA_PARENT=1
GA_ROOT=2
GA_ROOTOWNER=3
#Window messages
WM_GETTEXT=13
WM_GETTEXTLENGTH=14
EM_GETSEL=176
EM_SETSEL=177
EM_GETLINE=196
EM_GETLINECOUNT=186
EM_LINEFROMCHAR=201
EM_LINEINDEX=187
EM_LINELENGTH=193
EM_POSFROMCHAR=214 
EM_CHARFROMPOS=215
#Virtual key codes
VK_LBUTTON=1
VK_RBUTTON=2
VK_CANCEL=3
VK_MBUTTON=4
VK_XBUTTON=15
VK_XBUTTON=26
VK_BACK=8
VK_TAB=9
VK_CLEAR=12
VK_RETURN=13
VK_SHIFT=16
VK_CONTROL=17
VK_MENU=18
VK_PAUSE=19
VK_CAPITAL=20
VK_FINAL=0x18
VK_ESCAPE=0x1B
VK_CONVERT=0x1C
VK_NONCONVERT=0x1D
VK_ACCEPT=0x1E
VK_MODECHANGE=0x1F
VK_SPACE=32
VK_PRIOR=33
VK_NEXT=34
VK_END=35
VK_HOME=36
VK_LEFT=37
VK_UP=38
VK_RIGHT=39
VK_DOWN=40
VK_SELECT=41
VK_PRINT=42
VK_EXECUTE=43
VK_SNAPSHOT=44
VK_INSERT=45
VK_DELETE=46
VK_HELP=47
VK_LWIN=0x5B
VK_RWIN=0x5C
VK_APPS=0x5D
VK_SLEEP=0x5F
VK_NUMPAD0=0x60
VK_NUMPAD1=0x61
VK_NUMPAD2=0x62
VK_NUMPAD3=0x63
VK_NUMPAD4=0x64
VK_NUMPAD5=0x65
VK_NUMPAD6=0x66
VK_NUMPAD7=0x67
VK_NUMPAD8=0x68
VK_NUMPAD9=0x69
VK_MULTIPLY=0x6A
VK_ADD=0x6B
VK_SEPARATOR=0x6C
VK_SUBTRACT=0x6D
VK_DECIMAL=0x6E
VK_DIVIDE=0x6F
VK_F1=0x70
VK_F2=0x71
VK_F3=0x72
VK_F4=0x73
VK_F5=0x74
VK_F6=0x75
VK_F7=0x76
VK_F8=0x77
VK_F9=0x78
VK_F10=0x79
VK_F11=0x7A
VK_F12=0x7B
VK_F13=0x7C
VK_F14=0x7D
VK_F15=0x7E
VK_F16=0x7F
VK_F17=0x80
VK_F18=0x81
VK_F19=0x82
VK_F20=0x83
VK_F21=0x84
VK_F22=0x85
VK_F23=0x86
VK_F24=0x87
VK_NUMLOCK=0x90
VK_SCROLL=0x91
VK_LSHIFT=0xA0
VK_RSHIFT=0xA1
VK_LCONTROL=0xA2
VK_RCONTROL=0xA3
VK_LMENU=0xA4
VK_RMENU=0xA5
#Windows hooks
WH_KEYBOARD=2
WH_MOUSE=7
#win events
EVENT_SYSTEM_SOUND=0x1
EVENT_SYSTEM_ALERT=0x2
EVENT_SYSTEM_FOREGROUND=0x3
EVENT_SYSTEM_MENUSTART=0x4
EVENT_SYSTEM_MENUEND=0x5
EVENT_SYSTEM_MENUPOPUPSTART=0x6
EVENT_SYSTEM_MENUPOPUPEND=0x7
EVENT_SYSTEM_CAPTURESTART=0x8
EVENT_SYSTEM_CAPTUREEND=0x9
EVENT_SYSTEM_MOVESIZESTART=0xa
EVENT_SYSTEM_MOVESIZEEND=0xb
EVENT_SYSTEM_CONTEXTHELPSTART=0xc
EVENT_SYSTEM_CONTEXTHELPEND=0xd
EVENT_SYSTEM_DRAGDROPSTART=0xe
EVENT_SYSTEM_DRAGDROPEND=0xf
EVENT_SYSTEM_DIALOGSTART=0x10
EVENT_SYSTEM_DIALOGEND=0x11
EVENT_SYSTEM_SCROLLINGSTART=0x12
EVENT_SYSTEM_SCROLLINGEND=0x13
EVENT_SYSTEM_SWITCHSTART=0x14
EVENT_SYSTEM_SWITCHEND=0x15
EVENT_SYSTEM_MINIMIZESTART=0x16
EVENT_SYSTEM_MINIMIZEEND=0x17
EVENT_OBJECT_CREATE=0x8000
EVENT_OBJECT_DESTROY=0x8001
EVENT_OBJECT_SHOW=0x8002
EVENT_OBJECT_HIDE=0x8003
EVENT_OBJECT_REORDER=0x8004
EVENT_OBJECT_FOCUS=0x8005
EVENT_OBJECT_SELECTION=0x8006
EVENT_OBJECT_SELECTIONADD=0x8007
EVENT_OBJECT_SELECTIONREMOVE=0x8008
EVENT_OBJECT_SELECTIONWITHIN=0x8009
EVENT_OBJECT_STATECHANGE=0x800a
EVENT_OBJECT_LOCATIONCHANGE=0x800b
EVENT_OBJECT_NAMECHANGE=0x800c
EVENT_OBJECT_DESCRIPTIONCHANGE=0x800d
EVENT_OBJECT_VALUECHANGE=0x800e
EVENT_OBJECT_PARENTCHANGE=0x800f
EVENT_OBJECT_HELPCHANGE=0x8010
EVENT_OBJECT_DEFACTIONCHANGE=0x8011
EVENT_OBJECT_ACCELERATORCHANGE=0x8012
EVENT_CONSOLE_CARET=0x4001
EVENT_CONSOLE_UPDATE_REGION=0x4002
EVENT_CONSOLE_UPDATE_SIMPLE=0x4003
EVENT_CONSOLE_UPDATE_SCROLL=0x4004
EVENT_CONSOLE_LAYOUT=0x4005
EVENT_CONSOLE_START_APPLICATION=0x4006
EVENT_CONSOLE_END_APPLICATION=0x4007

def LOBYTE(word):
	return word&0xFF
 
def HIBYTE(word):
	return word>>8

def MAKEWORD(lo,hi):
	return (hi<<8)+lo

def LOWORD(long):
	return long&0xFFFF
 
def HIWORD(long):
	return long>>16

def MAKELONG(lo,hi):
	return (hi<<16)+lo

def waitMessage():
	return user32.WaitMessage()

def getMessage(*args):
	return user32.GetMessageW(*args)

def translateMessage(*args):
	return user32.TranslateMessage(*args)

def dispatchMessage(*args):
	return user32.DispatchMessageW(*args)

def peekMessage(*args):
	try:
		res=user32.PeekMessageW(*args)
	except:
		res=0
	return res

def registerWindowMessage(name):
	return user32.RegisterWindowMessageW(name)

def getAsyncKeyState(v):
	return user32.GetAsyncKeyState(v)

def getKeyState(v):
	return user32.GetKeyState(v)

def isWindow(hwnd):
	return user32.IsWindow(hwnd)

def isDescendantWindow(parentHwnd,childHwnd):
	if (parentHwnd==childHwnd) or user32.IsChild(parentHwnd,childHwnd):
		return True
	else:
		return False

def getForegroundWindow():
	return user32.GetForegroundWindow()

def setForegroundWindow(hwnd):
	user32.SetForegroundWindow(hwnd)

def setFocus(hwnd):
	user32.SetFocus(hwnd)

def getDesktopWindow():
		return user32.GetDesktopWindow()

def getControlID(hwnd):
	return 0 
	#Need value of GWL_ID
	#return user32.GetWindowLong(hwnd,GWL_ID)

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

def getAncestor(hwnd,flags):
	return user32.GetAncestor(hwnd,flags)

def setCursorPos(x,y):
	user32.SetCursorPos(x,y)

def getCursorPos():
	point=ctypes.wintypes.POINT()
	user32.GetCursorPos(ctypes.byref(point))
	return [point.x,point.y]

def getCaretPos():
	point=ctypes.wintypes.POINT()
	user32.GetCaretPos(ctypes.byref(point))
	return [point.x,point.y]

def getWindowText(hwnd):
	buf=ctypes.create_unicode_buffer(1024)
	user32.InternalGetWindowText(hwnd,buf,1024)
	return buf.value
