import threading
from ctypes import *
from logHandler import log

class inprocWorkerHandle_t(c_void_p):
	pass

serverLib=cdll.LoadLibrary('lib/NVDAControlServer.dll')

inprocWorkers={}

#utility function to point an exported function pointer in a dll  to a ctypes wrapped python function
def _setDllFuncPointer(dll,name,cfunc):
	cast(getattr(dll,name),POINTER(c_void_p)).contents.value=cast(cfunc,c_void_p).value

#Implementation of methods

@CFUNCTYPE(c_voidp,POINTER(c_char_p))
def getNVDAVersionString(version):
	import versionInfo
	version.contents.value=versionInfo.version
_setDllFuncPointer(serverLib,"fp_getNVDAVersionString",getNVDAVersionString)

@CFUNCTYPE(inprocWorkerHandle_t,c_int,c_char_p)
def registerInprocWorker(processID,address):
	inprocWorkerHandle=processID
	inprocWorkers[inprocWorkerHandle]=address
	return inprocWorkerHandle
_setDllFuncPointer(serverLib,"fp_registerInprocWorker",registerInprocWorker)

@CFUNCTYPE(c_voidp,inprocWorkerHandle_t)
def unregisterInprocWorker(inprocWorkerHandle):
	del inprocWorkers[inprocWorkerHandle.value]
_setDllFuncPointer(serverLib,"fp_unregisterInprocWorker",unregisterInprocWorker)

def executeAppModuleEvent_helper(processID,event):
	import appModuleHandler
	appModule=appModuleHandler.getAppModuleFromProcessID(processID)
	print appModule
	print dir(appModule)
	event="appModule.event_external_%s"%event
	eval(event)

@CFUNCTYPE(c_int,c_int,c_char_p)
def executeAppModuleEvent(processID,event):
	import queueHandler
	queueHandler.queueFunction(queueHandler.eventQueue,executeAppModuleEvent_helper,processID,event)
	return True
_setDllFuncPointer(serverLib,"fp_executeAppModuleEvent",executeAppModuleEvent)

def initialize():
	global serverThread
	serverThread=threading.Thread(target=serverLib.runServer)
	serverThread.start()

def terminate():
	serverLib.stopServer()
