import debug
import winUser
from keyboardHandler import key
import api
import audio
import NVDAObjects
import lang
from constants import *
import MSHTML

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
			if dynamicMap.has_key(className):
				virtualBufferClass=dynamicMap[className]
			elif staticMap.has_key(className):
				virtualBufferClass=staticMap[className]
			else:
				virtualBufferClass=None
			if virtualBufferClass:
				virtualBufferObject=virtualBufferClass(hwnd)
				runningTable[hwnd]=virtualBufferObject
			return 
		hwnd=winUser.getAncestor(hwnd,GA_PARENT)

def registerVirtualBufferClass(windowClass,cls):
	dynamicMap[windowClass]=cls

def unregisterVirtualBufferClass(windowClass):
	del dynamicMap[windowClass]

staticMap={
"Internet Explorer_Server":MSHTML.virtualBuffer_MSHTML,
}

dynamicMap={}

