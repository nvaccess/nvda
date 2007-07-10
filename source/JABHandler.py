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

MAX_STRING_SIZE=1024
SHORT_STRING_SIZE=256

class NVDAJavaContext(Structure):
	_fields_=[
		('hwnd',c_int),
		('VM',c_int),
		('accessibleContext',c_int),
	]

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

def getAccessibleContextInfo(vmID,accContext):
	info=AccessibleContextInfo()
	bridgeDll.getAccessibleContextInfo(vmID,accContext,byref(info))
	return info

def getAccessibleTextInfo(vmID,accText,x,y):
	textInfo=AccessibleTextInfo()
	bridgeDll.getAccessibleTextInfo(vmID,accText,byref(textInfo),x,y)
	return textInfo

def getAccessibleTextItems(vmID,accText,index):
	textItemsInfo=AccessibleTextItemsInfo()
	bridgeDll.getAccessibleTextItems(vmID,accText,byref(textItemsInfo),index)
	return textItemsInfo

def getAccessibleTextSelectionInfo(vmID,accText):
	textSelectionInfo=AccessibleTextSelectionInfo()
	bridgeDll.getAccessibleTextSelectionInfo(vmID,accText,byref(textSelectionInfo))
	return textSelectionInfo

def getAccessibleTextRange(vmID,accText,start,end):
	len=(end-start)
	text=create_unicode_buffer(len+1)
	bridgeDll.getAccessibleTextRange(vmID,accText,start,end,text,len)
	return text.value

def getAccessibleTextLineBounds(vmID,accText,index):
	startIndex=c_int()
	endIndex=c_int()
	bridgeDll.getAccessibleTextLineBounds(vmID,accText,index,byref(startIndex),byref(endIndex))
	return [startIndex,endIndex]

@CFUNCTYPE(c_voidp,c_int,c_int,c_int)
def internal_event_focusGained(vmID, event,source):
	queueHandler.queueFunction(queueHandler.eventQueue,event_gainFocus,vmID,source)

def event_gainFocus(vmID,accContext):
	obj=NVDAObjects.JAB.JAB(vmID,accContext)
	api.setFocusObject(obj)
	eventHandler.manageEvent("gainFocus",obj)
	activeChild=obj.activeChild
	if activeChild:
		api.setFocusObject(activeChild)
		eventHandler.manageEvent("gainFocus",activeChild)

@CFUNCTYPE(c_voidp,c_int,c_int,c_int)
def internal_event_activeDescendantChange(vmID, event,source):
	queueHandler.queueFunction(queueHandler.eventQueue,event_activeDescendantChange,vmID,source)

def event_activeDescendantChange(vmID,accContext):
	obj=NVDAObjects.JAB.JAB(vmID,accContext)
	activeChild=obj.activeChild
	if activeChild:
		api.setFocusObject(activeChild)
		eventHandler.manageEvent("gainFocus",activeChild)

def initialize():
	global bridgeDll
	try:
		bridgeDll=cdll.WINDOWSACCESSBRIDGE
		res=bridgeDll.Windows_run()
		if not res:
			raise RuntimeError('Windows_run') 
		bridgeDll.setFocusGainedFP(internal_event_focusGained)
		bridgeDll.setPropertyActiveDescendentChangeFP(internal_event_activeDescendantChange)
		return True
	except:
		return False
