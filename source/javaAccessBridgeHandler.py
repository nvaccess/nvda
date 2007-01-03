import ctypes
import ctypes.wintypes

bridgeDll=None

MAX_STRING_SIZE=1024
SHORT_STRING_SIZE=256

class AccessBridgeVersionInfo(ctypes.Structure):
	_fields_=[
		('VMVersion',ctypes.wintypes.WCHAR*SHORT_STRING_SIZE),
		(bridgeJavaClassVersion,ctypes.wintypes.WCHAR*SHORT_STRING_SIZE),
		(bridgeJavaDLLVersion,ctypes.wintypes.WCHAR*SHORT_STRING_SIZE),
		(bridgeWinDLLVersion,ctypes.wintypes.WCHAR*SHORT_STRING_SIZE),
	]

class AccessibleContextInfo(ctypes.Structure):
	_fields_=[
		('name',ctypes.wintypes.WCHAR*MAX_STRING_SIZE),
		('description',ctypes.wintypes.WCHAR*MAX_STRING_SIZE),
		('role',ctypes.wintypes.WCHAR*SHORT_STRING_SIZE),
		('states',ctypes.wintypes.WCHAR*SHORT_STRING_SIZE),
		('indexInParent',ctypes.c_int),
		('childrenCount',ctypes.c_int),
		('x',ctypes.c_int),
		('y',ctypes.c_int),
		('width',ctypes.c_int),
		('height',ctypes.c_int),
		('accessibleComponent',ctypes.wintypes.BOOL),
		('accessibleAction',ctypes.wintypes.BOOL),
		('accessibleSelection',ctypes.wintypes.BOOL),
		('accessibleText',ctypes.wintypes.BOOL),
		('accessibleValue',ctypes.wintypes.BOOL),
	]

class AccessibleTextInfo(ctypes.Structure):
	_fields_=[
		('charCount',ctypes.c_int),
		('caretIndex',ctypes.c_int),
		('indexAtPoint',ctypes.c_int),
	]

class AccessibleTextItemsInfo(ctypes.Structure):
	_fields_=[
		('letter',ctypes.wintypes.WCHAR),
		('word',ctypes.wintypes.WCHAR*SHORT_STRING_SIZE),
		('sentence',ctypes.wintypes.WCHAR*MAX_STRING_SIZE),
	]

class AccessibleTextSelectionInfo(ctypes.Structure):
	_fields_=[
		('selectionStartIndex',ctypes.c_int),
		('selectionEndIndex',ctypes.c_int),
		('selectedText',ctypes.wintypes.WCHAR*MAX_STRING_SIZE),
	]

class AccessibleTextRectInfo(ctypes.Structure):
	_fields_=[
		('x',ctypes.c_int),
		('y',ctypes.c_int),
		('width',ctypes.c_int),
		('height',ctypes.c_int),
	]

class AccessibleTextAttributesInfo(ctypes.Structure):
	_fields_=[
		('bold',ctypes.wintypes.BOOL),
		('italic',ctypes.wintypes.BOOL),
		('underline',ctypes.wintypes.BOOL),
		('strikethrough',ctypes.wintypes.BOOL),
		('superscript',ctypes.wintypes.BOOL),
		('subscript',ctypes.wintypes.BOOL),
		('backgroundColor',ctypes.wintypes.WCHAR*SHORT_STRING_SIZE),
		('foregroundColor',ctypes.wintypes.WCHAR*SHORT_STRING_SIZE),
		('fontFamily',ctypes.wintypes.WCHAR*SHORT_STRING_SIZE),
		('fontSize',ctypes.c_int),
		('alignment',ctypes.c_int),
		('bidiLevel',ctypes.c_int),
		('firstLineIndent',ctypes.c_float),
		('LeftIndent',ctypes.c_float),
		('rightIndent',ctypes.c_float),
		('lineSpacing',ctypes.c_float),
		('spaceAbove',ctypes.c_float),
		('spaceBelow',ctypes.c_float),
		('fullAttributesString',ctypes.wintypes.WCHAR*MAX_STRING_SIZE),
	]

def initialize():
	global bridgeDll
	try:
		bridgeDll=ctypes.cdll.WINDOWSACCESSBRIDGE
		bridgeDll.Windows_run()
	except:
		pass
