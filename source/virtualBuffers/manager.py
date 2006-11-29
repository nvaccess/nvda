import debug
import winUser
from keyboardHandler import key
import api
import audio
import NVDAObjects
from constants import *
import MSHTML
import gecko

runningTable={}

def getVirtualBuffer(hwnd):
	while hwnd:
		if runningTable.has_key(hwnd):
			return runningTable[hwnd]
		hwnd=winUser.getAncestor(hwnd,GA_PARENT)
	return None

def removeVirtualBuffer(hwnd):
	if runningTable.has_key(hwnd):
		del runningTable[hwnd]

def insertVirtualBuffer(hwnd,virtualBufferObject):
	runningTable[hwnd]=virtualBufferObject

def updateVirtualBuffers(hwnd):
	while hwnd:
		if not runningTable.has_key(hwnd):
			className=winUser.getClassName(hwnd)
			NVDAObject=NVDAObjects.getNVDAObjectByLocator(hwnd,OBJID_CLIENT,0)
			if not NVDAObject:
				return None
			role=NVDAObject.role
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
				virtualBufferObject=virtualBufferClass(NVDAObject)
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

