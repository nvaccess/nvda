from ctypes import *
from ctypes.wintypes import *

hookDLL=cdll.NVWH

class keyInfoType(Structure):
	_fields_=[
		('vkCode',DWORD),
		('scanCode',DWORD),
		('extended',BOOL),
		('injected',BOOL),
	]

userKeyCallbackType=CFUNCTYPE(BOOL,keyInfoType)

setUserKeyUpCallback=hookDLL.NVWH_setUserKeyUpCallback
setUserKeyDownCallback=hookDLL.NVWH_setUserKeyDownCallback

def registerKeyHook():
	hookDLL.NVWH_registerKeyHook(hookDLL._handle)

unregisterKeyHook=hookDLL.NVWH_unregisterKeyHook

userCharCallbackType=CFUNCTYPE(c_voidp,c_short)

setUserCharCallback=hookDLL.NVWH_setUserCharCallback

def registerCharHook():
	hookDLL.NVWH_registerCharHook(hookDLL._handle)

pumpCharQueue=hookDLL.NVWH_pumpCharQueue

unregisterCharHook=hookDLL.NVWH_unregisterCharHook
