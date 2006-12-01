import debug
from constants import *
import winUser
from keyboardHandler import key
import api
import audio
import NVDAObjects
from constants import *
import MSHTML
import gecko

runningTable={}

def getVirtualBuffer(obj):
	if len(runningTable)==0:
		return None
	hwnd=obj.windowHandle
	for existingHwnd in runningTable:
		if winUser.isDescendantWindow(existingHwnd,hwnd):
			return runningTable[existingHwnd]
	return None

def removeVirtualBuffer(obj):
	hwnd=obj.windowHandle
	if runningTable.has_key(hwnd):
		del runningTable[hwnd]

def updateVirtualBuffers(obj):
	if not isinstance(obj,NVDAObjects.MSAA.NVDAObject_MSAA):
		return
	if getVirtualBuffer(obj):
		return
	hwnd=obj.windowHandle
	while hwnd:
		obj=NVDAObjects.MSAA.getNVDAObjectFromEvent(hwnd,OBJID_CLIENT,0)
		if obj:
			className=obj.windowClassName
			role=obj.role
			if _dynamicMap.has_key((className,role)):
				virtualBufferClass=_dynamicMap[(className,role)]
			elif _dynamicMap.has_key((className,None)):
				virtualBufferClass=_dynamicMap[(className,None)]
			elif _staticMap.has_key((className,role)):
				virtualBufferClass=_staticMap[(className,role)]
			elif _staticMap.has_key((className,None)):
				virtualBufferClass=_staticMap[(className,None)]
			else:
				virtualBufferClass=None
			if virtualBufferClass:
				virtualBufferObject=virtualBufferClass(obj)
				runningTable[hwnd]=virtualBufferObject
				return 
		hwnd=winUser.getAncestor(hwnd,GA_PARENT)

def registerVirtualBufferClass(windowClass,role,cls):
	_dynamicMap[(windowClass,role)]=cls

def unregisterVirtualBufferClass(windowClass,role):
	del _dynamicMap[(windowClass,role)]

_staticMap={
("Internet Explorer_Server",None):MSHTML.virtualBuffer_MSHTML,
("MozillaWindowClass",ROLE_SYSTEM_DOCUMENT):gecko.virtualBuffer_gecko,
#("MozillaWindowClass",ROLE_SYSTEM_PANE):gecko.virtualBuffer_gecko,
#("MozillaContentWindowClass",ROLE_SYSTEM_DOCUMENT):gecko.virtualBuffer_gecko,
#("MozillaContentWindowClass",ROLE_SYSTEM_PANE):gecko.virtualBuffer_gecko,
}

_dynamicMap={}

