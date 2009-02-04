#javaAccessBridgeHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import Queue
from ctypes import *
from ctypes.wintypes import *
import queueHandler
import speech
import globalVars
from logHandler import log
import winUser
import api
import eventHandler
import controlTypes
import NVDAObjects.JAB

bridgeDll=None
isRunning=False
vmIDsToWindowHandles={}
internalFunctionQueue=Queue.Queue(1000)
internalFunctionQueue.__name__="JABHandler.internalFunctionQueue"
lastFocusNVDAObject=None

def internalQueueFunction(func,*args,**kwargs):
	internalFunctionQueue.put_nowait((func,args,kwargs))

MAX_STRING_SIZE=1024
SHORT_STRING_SIZE=256

class JABContext(object):

	def __init__(self,hwnd=None,vmID=None,accContext=None):
		if hwnd and not vmID:
 			vmID=c_int()
			accContext=c_int()
			bridgeDll.getAccessibleContextFromHWND(hwnd,byref(vmID),byref(accContext))
			vmID=vmID.value
			accContext=accContext.value
			#Record  this vm ID and window handle for later use with other objects
			vmIDsToWindowHandles[vmID]=hwnd
		elif vmID and not hwnd:
			hwnd=vmIDsToWindowHandles.get(vmID,0)
		self.hwnd=hwnd
		self.vmID=vmID
		self.accContext=accContext

	def __del__(self):
		if isRunning:
			try:
				bridgeDll.releaseJavaObject(self.vmID,self.accContext)
			except:
				log.debugWarning("Error releasing java object",exc_info=True)


	def __eq__(self,jabContext):
		if self.vmID==jabContext.vmID and bridgeDll.isSameObject(self.vmID,self.accContext,jabContext.accContext):
			return True
		else:
			return False

	def __ne__(self,jabContext):
		if self.vmID!=jabContext.vmID or not bridgeDll.isSameObject(self.vmID,self.accContext,jabContext.accContext):
			return True
		else:
			return False

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
		index=max(index,0)
		log.debug("lineBounds: index %s"%index)
		#Java returns end as the last character, not end as past the last character
		startIndex=c_int()
		endIndex=c_int()
		bridgeDll.getAccessibleTextLineBounds(self.vmID,self.accContext,index,byref(startIndex),byref(endIndex))
		start=startIndex.value
		end=endIndex.value
		log.debug("line bounds: start %s, end %s"%(start,end))
		if end<start:
			# Invalid or empty line.
			return (0,-1)
		ok=False
		# OpenOffice sometimes returns offsets encompassing more than one line, so try to narrow them down.
		# Try to retract the end offset.
		while not ok:
			bridgeDll.getAccessibleTextLineBounds(self.vmID,self.accContext,end,byref(startIndex),byref(endIndex))
			tempStart=max(startIndex.value,0)
			tempEnd=max(endIndex.value,0)
			log.debug("line bounds: tempStart %s, tempEnd %s"%(tempStart,tempEnd))
			if tempStart>(index+1):
				# This line starts after the requested index, so set end to point at the line before.
				end=tempStart-1
			else:
				ok=True
		ok=False
		# Try to retract the start.
		while not ok:
			bridgeDll.getAccessibleTextLineBounds(self.vmID,self.accContext,start,byref(startIndex),byref(endIndex))
			tempStart=max(startIndex.value,0)
			tempEnd=max(endIndex.value,0)
			log.debug("line bounds: tempStart %s, tempEnd %s"%(tempStart,tempEnd))
			if tempEnd<(index-1):
				# This line ends before the requested index, so set start to point at the line after.
				start=tempEnd+1
			else:
				ok=True
		log.debug("line bounds: returning %s, %s"%(start,end))
		return (start,end)


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

	def getAccessibleContextAt(self,x,y):
		newAccContext=c_int()
		res=bridgeDll.getAccessibleContextAt(self.vmID,self.accContext,x,y,byref(newAccContext))
		newAccContext=newAccContext.value
		if not res or not newAccContext:
			return None
		if not bridgeDll.isSameObject(self.vmID,newAccContext,self.accContext):
			return self.__class__(self.hwnd,self.vmID,newAccContext)
		elif newAccContext!=self.accContext:
			bridgeDll.releaseJavaObject(self.vmID,newAccContext)
		return None

	def getCurrentAccessibleValueFromContext(self):
		buf=create_unicode_buffer(SHORT_STRING_SIZE+1)
		bridgeDll.getCurrentAccessibleValueFromContext(self.vmID,self.accContext,buf,SHORT_STRING_SIZE)
		return buf.value

	def selectTextRange(self,start,end):
		bridgeDll.selectTextRange(start,end)

	def setCaretPosition(self,offset):
		bridgeDll.setCaretPosition(self.vmID,self.accContext,offset)

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
		('accessibleValue',BOOL),
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
	internalQueueFunction(event_gainFocus,vmID,source)
	bridgeDll.releaseJavaObject(vmID,event)

def event_gainFocus(vmID,accContext):
	global lastFocusNVDAObject
	jabContext=JABContext(vmID=vmID,accContext=accContext)
	if not winUser.isDescendantWindow(winUser.getForegroundWindow(),jabContext.hwnd):
		return
	focus=api.getFocusObject()
	if (isinstance(focus,NVDAObjects.JAB.JAB) and focus.jabContext==jabContext) or (lastFocusNVDAObject and lastFocusNVDAObject.jabContext==jabContext):
		return 
	obj=NVDAObjects.JAB.JAB(jabContext=jabContext)
	if obj.role==controlTypes.ROLE_UNKNOWN:
		return
	eventHandler.queueEvent("gainFocus",obj)
	lastFocusNVDAObject=obj
	activeChild=obj.activeChild
	if activeChild and activeChild.role!=controlTypes.ROLE_UNKNOWN and activeChild.jabContext!=jabContext:
		eventHandler.queueEvent("gainFocus",activeChild)
		lastFocusNVDAObject=activeChild

@CFUNCTYPE(c_voidp,c_int,c_int,c_int,c_int,c_int)
def internal_event_activeDescendantChange(vmID, event,source,oldDescendant,newDescendant):
	internalQueueFunction(event_gainFocus,vmID,newDescendant)
	for accContext in [event,oldDescendant]:
		bridgeDll.releaseJavaObject(vmID,accContext)

@CFUNCTYPE(c_voidp,c_int,c_int,c_int,c_wchar_p,c_wchar_p)
def internal_event_stateChange(vmID,event,source,oldState,newState):
	internalQueueFunction(event_stateChange,vmID,source,oldState,newState)
	bridgeDll.releaseJavaObject(vmID,event)

def event_stateChange(vmID,accContext,oldState,newState):
	jabContext=JABContext(vmID=vmID,accContext=accContext)
	focus=api.getFocusObject()
	#For broken tabs and menus, we need to watch for things being selected and pretend its a focus change
	stateList=newState.split(',')
	if "focused" in stateList or "selected" in stateList:
		obj=NVDAObjects.JAB.JAB(jabContext=jabContext)
		if focus!=obj and obj.role in [controlTypes.ROLE_MENUITEM,controlTypes.ROLE_TAB,controlTypes.ROLE_MENU]:
			eventHandler.queueEvent("gainFocus",obj)
			return
	if isinstance(focus,NVDAObjects.JAB.JAB) and focus.jabContext==jabContext:
		obj=focus
	else:
		obj=NVDAObjects.JAB.JAB(jabContext=jabContext)
	eventHandler.queueEvent("stateChange",obj)

@CFUNCTYPE(c_voidp,c_int,c_int,c_int,c_int,c_int)
def internal_event_caretChange(vmID, event,source,oldPos,newPos):
	if oldPos<0 and newPos>=0:
		internalQueueFunction(event_gainFocus,vmID,source)
	bridgeDll.releaseJavaObject(vmID,event)

def event_enterJavaWindow(hwnd):
	try:
		jabContext=JABContext(hwnd=hwnd)
	except:
		return
	obj=NVDAObjects.JAB.JAB(jabContext=jabContext)
	if obj==api.getForegroundObject():
		return
	eventHandler.queueEvent("gainFocus",obj)
	vmID=c_int()
	accContext=c_int()
	bridgeDll.getAccessibleContextWithFocus(hwnd,byref(vmID),byref(accContext))
	jabContext=JABContext(hwnd=hwnd,vmID=vmID.value,accContext=accContext.value)
	focusObject=NVDAObjects.JAB.JAB(jabContext=jabContext)
	activeChild=focusObject.activeChild
	if activeChild and activeChild.role!=controlTypes.ROLE_UNKNOWN:
		focusObject=activeChild
	eventHandler.queueEvent("gainFocus",focusObject)
	lastFocusNVDAObject=focusObject



def isJavaWindow(hwnd):
	if not isRunning:
		return False
	return bridgeDll.isJavaWindow(hwnd)

def _errcheck(res, func, args):
	if not res:
		raise RuntimeError("Result %d" % res)

def initialize():
	global bridgeDll, isRunning
	try:
		bridgeDll=cdll.WINDOWSACCESSBRIDGE
		for func in (
			bridgeDll.Windows_run, bridgeDll.getAccessibleContextFromHWND, bridgeDll.getVersionInfo, 
			bridgeDll.getAccessibleContextInfo, bridgeDll.getAccessibleTextInfo, bridgeDll.getAccessibleTextItems,
			bridgeDll.getAccessibleTextSelectionInfo, bridgeDll.getAccessibleTextRange, bridgeDll.getAccessibleTextLineBounds,
			bridgeDll.getCurrentAccessibleValueFromContext, bridgeDll.selectTextRange, bridgeDll.setCaretPosition,
			bridgeDll.getAccessibleContextWithFocus, 
		):
			func.errcheck = _errcheck
		bridgeDll.Windows_run()
		bridgeDll.setFocusGainedFP(internal_event_focusGained)
		bridgeDll.setPropertyActiveDescendentChangeFP(internal_event_activeDescendantChange)
		bridgeDll.setPropertyStateChangeFP(internal_event_stateChange)
		bridgeDll.setPropertyCaretChangeFP(internal_event_caretChange)
		isRunning=True
		return True
	except:
		return False

def pumpAll():
	if isRunning: 
		queueHandler.flushQueue(internalFunctionQueue)

def terminate():
	global isRunning, bridgeDll
	if not isRunning:
		return
	bridgeDll.setFocusGainedFP(None)
	bridgeDll.setPropertyActiveDescendentChangeFP(None)
	bridgeDll.setPropertyStateChangeFP(None)
	bridgeDll.setPropertyCaretChangeFP(None)
	windll.kernel32.FreeLibrary(bridgeDll._handle)
	cdll.WINDOWSACCESSBRIDGE=bridgeDll=None
	isRunning=False
