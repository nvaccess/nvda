#keyHook.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from ctypes import *
from ctypes.wintypes import *
from win32con import WH_KEYBOARD_LL, HC_ACTION, LLKHF_UP, LLKHF_EXTENDED, LLKHF_INJECTED

class KBDLLHOOKSTRUCT(Structure):
	_fields_=[
		('vkCode',DWORD),
		('scanCode',DWORD),
		('flags',DWORD),
		('time',DWORD),
		('dwExtraInfo',DWORD),
	]

hookID=0
keyDownCallback=None
keyUpCallback=None

@WINFUNCTYPE(c_long,c_int,WPARAM,LPARAM)
def keyboardHook(code,wParam,lParam):
	if code!=HC_ACTION:
		return windll.user32.CallNextHookEx(hookID,code,wParam,lParam)
	kbd=KBDLLHOOKSTRUCT.from_address(lParam)
	if kbd.flags&LLKHF_UP:
		res=keyUpCallback(kbd.vkCode,kbd.scanCode,bool(kbd.flags&LLKHF_EXTENDED),bool(kbd.flags&LLKHF_INJECTED))
	else:
		res=keyDownCallback(kbd.vkCode,kbd.scanCode,bool(kbd.flags&LLKHF_EXTENDED),bool(kbd.flags&LLKHF_INJECTED))
	if not res:
		return 1
	return windll.user32.CallNextHookEx(hookID,code,wParam,lParam)

def initialize(downCallback,upCallback):
	global hookID, keyDownCallback, keyUpCallback
	keyDownCallback=downCallback
	keyUpCallback=upCallback
	hookID=windll.user32.SetWindowsHookExW(WH_KEYBOARD_LL,keyboardHook,windll.kernel32.GetModuleHandleW(None),0)
	if hookID==0:
		raise OSError("Could not register hook")

def terminate():
	global hookID, keyDownCallbac, keyUpCallback
	if windll.user32.UnhookWindowsHookEx(hookID)==0:
		raise OSError("could not unregister hook %s"%hookID)
	hookID=0
	keyDownCallback=keyUpCallback=None
