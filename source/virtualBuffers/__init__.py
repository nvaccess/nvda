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

def updateVirtualBuffers(hwnd):
	while hwnd:
		if not runningTable.has_key(hwnd):
			className=winUser.getClassName(hwnd)
			NVDAObject=NVDAObjects.getNVDAObjectByLocator(hwnd,OBJID_CLIENT,0)
			if not NVDAObject:
				return None
			role=NVDAObject.role
			if dynamicMap.has_key((className,role)):
				virtualBufferClass=dynamicMap[(className,role)]
			elif dynamicMap.has_key((className,None)):
				virtualBufferClass=dynamicMap[(className,None)]
			elif staticMap.has_key((className,role)):
				virtualBufferClass=staticMap[(className,role)]
			elif staticMap.has_key((className,None)):
				virtualBufferClass=staticMap[(className,None)]
			else:
				virtualBufferClass=None
			if virtualBufferClass:
				virtualBufferObject=virtualBufferClass(NVDAObject)
				runningTable[hwnd]=virtualBufferObject
			return 
		hwnd=winUser.getAncestor(hwnd,GA_PARENT)

def registerVirtualBufferClass(windowClass,role,cls):
	dynamicMap[(windowClass,role)]=cls

def unregisterVirtualBufferClass(windowClass,role):
	del dynamicMap[(windowClass,role)]

staticMap={
("Internet Explorer_Server",None):MSHTML.virtualBuffer_MSHTML,
("MozillaWindowClass",ROLE_SYSTEM_DOCUMENT):gecko.virtualBuffer_gecko,
("MozillaWindowClass",ROLE_SYSTEM_PANE):gecko.virtualBuffer_gecko,
("MozillaContentWindowClass",ROLE_SYSTEM_DOCUMENT):gecko.virtualBuffer_gecko,
("MozillaContentWindowClass",ROLE_SYSTEM_PANE):gecko.virtualBuffer_gecko,
}

dynamicMap={}

