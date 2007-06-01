from ctypes import *
from ctypes.wintypes import *

EVENT_TYPED_CHARACTER=0x1000

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
registerKeyHook=hookDLL.NVWH_registerKeyHook
unregisterKeyHook=hookDLL.NVWH_unregisterKeyHook

userCharCallbackType=CFUNCTYPE(c_voidp,c_short)
setUserCharCallback=hookDLL.NVWH_setUserCharCallback
registerCharHook=hookDLL.NVWH_registerCharHook
unregisterCharHook=hookDLL.NVWH_unregisterCharHook
