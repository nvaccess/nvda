#javaAccessBridgeHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from ctypes import *
from ctypes.wintypes import *
import queueHandler
import speech
import debug
import api
import eventHandler
import NVDAObjects.JAB

bridgeDll=None
isRunning=False
vmIDsToWindowHandles={}

MAX_STRING_SIZE=1024
SHORT_STRING_SIZE=256

class JABObjectWrapper(object):

	def __init__(self,hwnd=None,vmID=None,accContext=None):
		if hwnd and (not vmID or not accContext):
 			vmID=c_int()
			accContext=c_int()
			bridgeDll.getAccessibleContextFromHWND(hwnd,byref(vmID),byref(accContext))
			vmID=vmID.value
			accContext=accContext.value
			#Record  this vm ID and window handle for later use with other objects
			vmIDsToWindowHandles[vmID]=hwnd
		elif vmID and accContext and not hwnd:
			hwnd=vmIDsToWindowHandles.get(vmID,0)
		self.hwnd=hwnd
		self.vmID=vmID
		self.accContext=accContext

	def __del__(self):
		bridgeDll.releaseJavaObject(self.vmID,self.accContext)

	def getVersionInfo(self):
		info=AccessBridgeVersionInfo()
		bridgeDll.getVersionInfo(self.vmID,byref(info))
		return info

	def getAccessibleContextInfo(self):
		info=AccessibleContextInfo()
		bridgeDll.getAccessibleContextInfo(self.vmID,self.accContext,byref(info))
		return info

	def getAccessibleTextInfo(self,x,y):
		textInfo=AccessibleTextInfo()
		bridgeDll.getAccessibleTextInfo(self.vmID,self.accContext,byref(textInfo),x,y)
		return textInfo

	def getAccessibleTextItems(self,index):
		textItemsInfo=AccessibleTextItemsInfo()
		bridgeDll.getAccessibleTextItems(self.vmID,self.accContext,byref(textItemsInfo),index)
		return textItemsInfo

	def getAccessibleTextSelectionInfo(self):
		textSelectionInfo=AccessibleTextSelectionInfo()
		bridgeDll.getAccessibleTextSelectionInfo(self.vmID,self.accContext,byref(textSelectionInfo))
		return textSelectionInfo

	def getAccessibleTextRange(self,start,end):
		length=((end+1)-start)
		if length<=0:
			return "\n"
		text=create_unicode_buffer(length+1)
		bridgeDll.getAccessibleTextRange(self.vmID,self.accContext,start,end,text,length)
		return text.value

	def getAccessibleTextLineBounds(self,index):
		#Java returns end as the last character, not end as past the last character
		startIndex=c_int()
		endIndex=c_int()
		bridgeDll.getAccessibleTextLineBounds(self.vmID,self.accContext,index,byref(startIndex),byref(endIndex))
		startIndex=startIndex.value
		endIndex=endIndex.value
		if startIndex<0:
			startIndex=0
		if endIndex<0:
			endIndex=0
		return [startIndex,endIndex]

	def getAccessibleParentFromContext(self):
		accContext=bridgeDll.getAccessibleParentFromContext(self.vmID,self.accContext)
		if accContext:
			return self.__class__(self.hwnd,self.vmID,accContext)
		else:
			return None

	def getAccessibleChildFromContext(self,index):
		accContext=bridgeDll.getAccessibleChildFromContext(self.vmID,self.accContext,index)
		if accContext:
			return self.__class__(self.hwnd,self.vmID,accContext)
		else:
			return None

	def getActiveDescendent(self):
		accContext=bridgeDll.getActiveDescendent(self.vmID,self.accContext)
		if accContext:
			return self.__class__(self.hwnd,self.vmID,accContext)
		else:
			return None

class AccessBridgeVersionInfo(Structure):
	_fields_=[
		('VMVersion',WCHAR*SHORT_STRING_SIZE),
		('bridgeJavaClassVersion',WCHAR*SHORT_STRING_SIZE),
		('bridgeJavaDLLVersion',WCHAR*SHORT_STRING_SIZE),
		('bridgeWinDLLVersion',WCHAR*SHORT_STRING_SIZE),
	]

class AccessibleContextInfo(Structure):
	_fields_=[
		('name',WCHAR*MAX_STRING_SIZE),
		('description',WCHAR*MAX_STRING_SIZE),
		('role',WCHAR*SHORT_STRING_SIZE),
		('role_en_US',WCHAR*SHORT_STRING_SIZE),
		('states',WCHAR*SHORT_STRING_SIZE),
		('states_en_US',WCHAR*SHORT_STRING_SIZE),
		('indexInParent',c_int),
		('childrenCount',c_int),
		('x',c_int),
		('y',c_int),
		('width',c_int),
		('height',c_int),
		('accessibleComponent',BOOL),
		('accessibleAction',BOOL),
		('accessibleSelection',BOOL),
		('accessibleText',BOOL),
		('accessibleInterfaces',BOOL),
	]

class AccessibleTextInfo(Structure):
	_fields_=[
		('charCount',c_int),
		('caretIndex',c_int),
		('indexAtPoint',c_int),
	]

class AccessibleTextItemsInfo(Structure):
	_fields_=[
		('letter',WCHAR),
		('word',WCHAR*SHORT_STRING_SIZE),
		('sentence',WCHAR*MAX_STRING_SIZE),
	]

class AccessibleTextSelectionInfo(Structure):
	_fields_=[
		('selectionStartIndex',c_int),
		('selectionEndIndex',c_int),
		('selectedText',WCHAR*MAX_STRING_SIZE),
	]

class AccessibleTextRectInfo(Structure):
	_fields_=[
		('x',c_int),
		('y',c_int),
		('width',c_int),
		('height',c_int),
	]

class AccessibleTextAttributesInfo(Structure):
	_fields_=[
		('bold',BOOL),
		('italic',BOOL),
		('underline',BOOL),
		('strikethrough',BOOL),
		('superscript',BOOL),
		('subscript',BOOL),
		('backgroundColor',WCHAR*SHORT_STRING_SIZE),
		('foregroundColor',WCHAR*SHORT_STRING_SIZE),
		('fontFamily',WCHAR*SHORT_STRING_SIZE),
		('fontSize',c_int),
		('alignment',c_int),
		('bidiLevel',c_int),
		('firstLineIndent',c_float),
		('LeftIndent',c_float),
		('rightIndent',c_float),
		('lineSpacing',c_float),
		('spaceAbove',c_float),
		('spaceBelow',c_float),
		('fullAttributesString',WCHAR*MAX_STRING_SIZE),
	]


@CFUNCTYPE(c_voidp,c_int,c_int,c_int)
def internal_event_focusGained(vmID, event,source):
	queueHandler.queueFunction(queueHandler.eventQueue,event_gainFocus,vmID,source)
	bridgeDll.releaseJavaObject(vmID,event)

def event_gainFocus(vmID,accContext):
	JABObject=JABObjectWrapper(vmID=vmID,accContext=accContext)
	obj=NVDAObjects.JAB.JAB(JABObject)
	api.setFocusObject(obj)
	eventHandler.manageEvent("gainFocus",obj)
	activeChild=obj.activeChild
	if activeChild:
		api.setFocusObject(activeChild)
		eventHandler.manageEvent("gainFocus",activeChild)

@CFUNCTYPE(c_voidp,c_int,c_int,c_int,c_int,c_int)
def internal_event_activeDescendantChange(vmID, event,source,oldDescendant,newDescendant):
	queueHandler.queueFunction(queueHandler.eventQueue,event_gainFocus,vmID,newDescendant)
	for accContext in [event,oldDescendant]:
		bridgeDll.releaseJavaObject(vmID,accContext)

def event_activeDescendantChange(vmID,accContext):
	JABObject=JABObjectWrapper(vmID=vmID,accContext=accContext)
	obj=NVDAObjects.JAB.JAB(JABObject)
	activeChild=obj.activeChild
	if activeChild:
		api.setFocusObject(activeChild)
		eventHandler.manageEvent("gainFocus",activeChild)

def event_enterJavaWindow(hwnd):
	JABObject=JABObjectWrapper(hwnd=hwnd)
	obj=NVDAObjects.JAB.JAB(JABObject)
	api.setForegroundObject(obj)
	eventHandler.manageEvent("foreground",obj)

def isJavaWindow(hwnd):
	return bridgeDll.isJavaWindow(hwnd)

def initialize():
	global bridgeDll, isRunning
	try:
		bridgeDll=cdll.WINDOWSACCESSBRIDGE
		res=bridgeDll.Windows_run()
		if not res:
			raise RuntimeError('Windows_run') 
		bridgeDll.setFocusGainedFP(internal_event_focusGained)
		bridgeDll.setPropertyActiveDescendentChangeFP(internal_event_activeDescendantChange)
		isRunning=True
		return True
	except:
		return False
