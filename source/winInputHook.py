#winInputHook.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import threading
import comtypes.client
import time
from ctypes import *
from ctypes.wintypes import *
from win32con import WM_QUIT, HC_ACTION, WH_KEYBOARD_LL, LLKHF_UP, LLKHF_EXTENDED, LLKHF_INJECTED, WH_MOUSE_LL, LLMHF_INJECTED

class KBDLLHOOKSTRUCT(Structure):
	_fields_=[
		('vkCode',DWORD),
		('scanCode',DWORD),
		('flags',DWORD),
		('time',DWORD),
		('dwExtraInfo',DWORD),
	]

class MSLLHOOKSTRUCT(Structure):
	_fields_=[
		('pt',POINT),
		('mouseData',DWORD),
		('flags',DWORD),
		('time',DWORD),
		('dwExtraInfo',DWORD),
	]

keyDownCallback=None
keyUpCallback=None
mouseCallback=None

@WINFUNCTYPE(c_long,c_int,WPARAM,LPARAM)
def keyboardHook(code,wParam,lParam):
	if code!=HC_ACTION:
		return windll.user32.CallNextHookEx(0,code,wParam,lParam)
	kbd=KBDLLHOOKSTRUCT.from_address(lParam)
	if keyUpCallback and kbd.flags&LLKHF_UP:
		if not keyUpCallback(kbd.vkCode,kbd.scanCode,bool(kbd.flags&LLKHF_EXTENDED),bool(kbd.flags&LLKHF_INJECTED)):
			return 1
	elif keyDownCallback:
		if not keyDownCallback(kbd.vkCode,kbd.scanCode,bool(kbd.flags&LLKHF_EXTENDED),bool(kbd.flags&LLKHF_INJECTED)):
			return 1
	return windll.user32.CallNextHookEx(0,code,wParam,lParam)

@WINFUNCTYPE(c_long,c_int,WPARAM,LPARAM)
def mouseHook(code,wParam,lParam):
	if code!=HC_ACTION:
		return windll.user32.CallNextHookEx(0,code,wParam,lParam)
	msll=MSLLHOOKSTRUCT.from_address(lParam)
	if mouseCallback:
		if not mouseCallback(wParam,msll.pt.x,msll.pt.y,msll.flags&LLMHF_INJECTED):
			return 1
	return windll.user32.CallNextHookEx(0,code,wParam,lParam)

hookThread=None
hookThreadRefCount=0

def hookThreadFunc():
	keyHookID=windll.user32.SetWindowsHookExW(WH_KEYBOARD_LL,keyboardHook,windll.kernel32.GetModuleHandleW(None),0)
	if keyHookID==0:
		raise OSError("Could not register keyboard hook")
	mouseHookID=windll.user32.SetWindowsHookExW(WH_MOUSE_LL,mouseHook,windll.kernel32.GetModuleHandleW(None),0)
	if mouseHookID==0:
		raise OSError("Could not register mouse hook")
	msg=MSG()
	while windll.user32.GetMessageW(byref(msg),None,0,0):
		pass
	if windll.user32.UnhookWindowsHookEx(keyHookID)==0:
		raise OSError("could not unregister key hook %s"%keyHookID)
	if windll.user32.UnhookWindowsHookEx(mouseHookID)==0:
		raise OSError("could not unregister mouse hook %s"%mouseHookID)

def initialize():
	global hookThread, hookThreadRefCount
	hookThreadRefCount+=1
	if hookThreadRefCount==1:
		hookThread=threading.Thread(target=hookThreadFunc)
		hookThread.start()

def setCallbacks(keyUp=None,keyDown=None,mouse=None):
	global keyUpCallback, keyDownCallback, mouseCallback
	if keyUp:
		keyUpCallback=keyUp
	if keyDown:
		keyDownCallback=keyDown
	if mouse:
		mouseCallback=mouse

def terminate():
	global hookThread, hookThreadRefCount
	if not hookThread:
		raise RuntimeError("winInputHook not running")
	hookThreadRefCount-=1
	if hookThreadRefCount==0:
		windll.user32.PostThreadMessageW(hookThread.ident,WM_QUIT,0,0)
		hookThread.join()
		hookThread=None
