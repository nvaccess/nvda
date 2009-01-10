#mouseHook.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from ctypes import *
from ctypes.wintypes import *
from win32con import WH_MOUSE_LL, HC_ACTION, LLMHF_INJECTED

class MSLLHOOKSTRUCT(Structure):
	_fields_=[
		('pt',POINT),
		('mouseData',DWORD),
		('flags',DWORD),
		('time',DWORD),
		('dwExtraInfo',DWORD),
	]


hookID=0
mouseCallback=None

@WINFUNCTYPE(c_long,c_int,WPARAM,LPARAM)
def mouseHook(code,wParam,lParam):
	if code!=HC_ACTION:
		return windll.user32.CallNextHookEx(hookID,code,wParam,lParam)
	msll=MSLLHOOKSTRUCT.from_address(lParam)
	res=mouseCallback(wParam,msll.pt.x,msll.pt.y,msll.flags&LLMHF_INJECTED);
	if not res:
		return 1
	return windll.user32.CallNextHookEx(hookID,code,wParam,lParam)

def initialize(callback):
	global hookID, mouseCallback
	mouseCallback=callback
	hookID=windll.user32.SetWindowsHookExW(WH_MOUSE_LL,mouseHook,windll.kernel32.GetModuleHandleW(None),0)
	if hookID==0:
		raise OSError("Could not register hook")

def terminate():
	global hookID, mouseCallback
	if windll.user32.UnhookWindowsHookEx(hookID)==0:
		raise OSError("could not unregister hook %s"%hookID)
	hookID=0
	mouseCallback=None
