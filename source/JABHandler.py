#javaAccessBridgeHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from ctypes import *
from ctypes.wintypes import *
import queueHandler
import audio
import debug
import api
import eventHandler
import NVDAObjects

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

@CFUNCTYPE(c_voidp,c_int,c_int,c_int)
def event_gainFocus(vmID, event,accContext):
	try:
		obj=NVDAObjects.JAB.NVDAObject_JAB(vmID,accContext)
		api.setFocusObject(obj)
		eventHandler.manageEvent("gainFocus",obj)
	except:
		debug.writeException("event_focus")

def initialize():
	global bridgeDll
	try:
		bridgeDll=cdll.WINDOWSACCESSBRIDGE
		res=bridgeDll.Windows_run()
		if not res:
			raise RuntimeError('Windows_run') 
		bridgeDll.setFocusGainedFP(event_gainFocus)
		return True
	except:
		return False
