from ctypes import *

class inprocWorkerHandle_t(c_void_p):
	pass

clientLib=cdll.NVDAControlClient

version=c_char_p()
if not clientLib.getNVDAVersionString(byref(version)):
	raise RuntimeError("could not get version")
print version.value

if not clientLib.executeAppModuleEvent("speakMessage('testing with event_external_speakMessage')"):
	raise RuntimeError("could not execute appModule event")

raw_input()
