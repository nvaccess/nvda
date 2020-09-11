# IAccessibleHandler.py
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import Tuple
import struct
import weakref
# Kept for backwards compatibility
from ctypes import *  # noqa: F401, F403
from ctypes import (
	wintypes,
	windll,
	byref,
	c_void_p,
	c_char,
	c_int,
	cast,
	POINTER,
	create_unicode_buffer,
)
from ctypes.wintypes import HANDLE
from comtypes import IUnknown, IServiceProvider, COMError
import comtypes.client
import oleacc
import UIAHandler

# Kept for backwards compatibility
from comInterfaces.Accessibility import *  # noqa: F401, F403
# Specific imports for items we know we use, hopefully in the future we can remove the import for this module.
from comInterfaces.Accessibility import (
	IAccessible,
	IAccIdentity,
	CAccPropServices,
)
# Kept for backwards compatibility
from comInterfaces.IAccessible2Lib import *  # noqa: F401, F403
# Specific imports for items we know we use, hopefully in the future we can remove the import for this module.
from comInterfaces.IAccessible2Lib import (
	IAccessibleText,
	IAccessibleHypertext,
	IAccessible2,
	IA2_STATE_REQUIRED,
	IA2_STATE_INVALID_ENTRY,
	IA2_STATE_MODAL,
	IA2_STATE_DEFUNCT,
	IA2_STATE_SUPPORTS_AUTOCOMPLETION,
	IA2_STATE_MULTI_LINE,
	IA2_STATE_ICONIFIED,
	IA2_STATE_EDITABLE,
	IA2_STATE_PINNED,
	IA2_STATE_CHECKABLE,
	IA2_ROLE_UNKNOWN,
	IA2_ROLE_CANVAS,
	IA2_ROLE_CAPTION,
	IA2_ROLE_CHECK_MENU_ITEM,
	IA2_ROLE_COLOR_CHOOSER,
	IA2_ROLE_DATE_EDITOR,
	IA2_ROLE_DIRECTORY_PANE,
	IA2_ROLE_DESKTOP_PANE,
	IA2_ROLE_EDITBAR,
	IA2_ROLE_EMBEDDED_OBJECT,
	IA2_ROLE_ENDNOTE,
	IA2_ROLE_FILE_CHOOSER,
	IA2_ROLE_FONT_CHOOSER,
	IA2_ROLE_FRAME,
	IA2_ROLE_FOOTNOTE,
	IA2_ROLE_FORM,
	IA2_ROLE_GLASS_PANE,
	IA2_ROLE_HEADER,
	IA2_ROLE_HEADING,
	IA2_ROLE_ICON,
	IA2_ROLE_IMAGE_MAP,
	IA2_ROLE_INPUT_METHOD_WINDOW,
	IA2_ROLE_INTERNAL_FRAME,
	IA2_ROLE_LABEL,
	IA2_ROLE_LAYERED_PANE,
	IA2_ROLE_NOTE,
	IA2_ROLE_OPTION_PANE,
	IA2_ROLE_PAGE,
	IA2_ROLE_PARAGRAPH,
	IA2_ROLE_RADIO_MENU_ITEM,
	IA2_ROLE_REDUNDANT_OBJECT,
	IA2_ROLE_ROOT_PANE,
	IA2_ROLE_RULER,
	IA2_ROLE_SCROLL_PANE,
	IA2_ROLE_SECTION,
	IA2_ROLE_SHAPE,
	IA2_ROLE_SPLIT_PANE,
	IA2_ROLE_TEAR_OFF_MENU,
	IA2_ROLE_TERMINAL,
	IA2_ROLE_TEXT_FRAME,
	IA2_ROLE_TOGGLE_BUTTON,
	IA2_ROLE_VIEW_PORT,
	IA2_ROLE_CONTENT_DELETION,
	IA2_ROLE_CONTENT_INSERTION,
	IA2_ROLE_BLOCK_QUOTE,
	IA2_ROLE_DESKTOP_ICON,
	IA2_ROLE_FOOTER,
	IA2_ROLE_MARK,
)
import config


_winEventNameCache = {}


def getWinEventName(eventID):
	""" Looks up the name of an EVENT_* winEvent constant. """
	global _winEventNameCache
	if not _winEventNameCache:
		_winEventNameCache = {y: x for x, y in vars(winUser).items() if x.startswith('EVENT_')}
		_winEventNameCache.update({y: x for x, y in vars(IA2).items() if x.startswith('IA2_EVENT_')})
	name = _winEventNameCache.get(eventID)
	if not name:
		name = "unknown event ({eventID})"
	return name


_objectIDNameCache = {}


def getObjectIDName(objectID):
	""" Looks up the name of an OBJID_* winEvent constant. """
	global _objectIDNameCache
	if not _objectIDNameCache:
		_objectIDNameCache = {y: x for x, y in vars(winUser).items() if x.startswith('OBJID_')}
	name = _objectIDNameCache.get(objectID)
	if not name:
		name = str(objectID)
	return name


def getWinEventLogInfo(window, objectID, childID, eventID=None, threadID=None):
	"""
	Formats the given winEvent parameters into a printable string.
	window, objectID and childID are mandatory,
	but eventID and threadID are optional.
	"""
	windowClassName = winUser.getClassName(window) or "unknown"
	objectIDName = getObjectIDName(objectID)
	processID = winUser.getWindowThreadProcessID(window)[0]
	if processID:
		processName = appModuleHandler.getAppModuleFromProcessID(processID).appName
	else:
		processName = "unknown application"
	messageList = []
	if eventID is not None:
		eventName = getWinEventName(eventID)
		messageList.append(f"{eventName}")
	messageList.append(
		f"window {window} ({windowClassName}), objectID {objectIDName}, childID {childID}, "
		f"process {processID} ({processName})"
	)
	if threadID is not None:
		messageList.append(f"thread {threadID}")
	return ", ".join(messageList)


def isMSAADebugLoggingEnabled():
	""" Whether the user has configured NVDA to log extra information about MSAA events. """
	return config.conf["debugLog"]["MSAA"]


IAccessibleObjectIdentifierType = Tuple[
	int,  # windowHandle
	int,  # objectID
	int,  # childID
]

from . import internalWinEventHandler
# Imported for backwards compat
from .internalWinEventHandler import (  # noqa: F401
	winEventHookIDs,
	winEventLimiter,
	winEventIDsToNVDAEventNames,
	_shouldGetEvents,
)

from comInterfaces import IAccessible2Lib as IA2
from logHandler import log
import JABHandler
import eventHandler
import winUser
import api
import NVDAObjects.IAccessible
import NVDAObjects.window
import appModuleHandler
import mouseHandler
import controlTypes
import keyboardHandler
import core
import re

from .orderedWinEventLimiter import MENU_EVENTIDS

# Special Mozilla gecko MSAA constant additions
NAVRELATION_LABEL_FOR = 0x1002
NAVRELATION_LABELLED_BY = 0x1003
NAVRELATION_NODE_CHILD_OF = 0x1005
NAVRELATION_EMBEDS = 0x1009

# IAccessible2 relations (not included in the typelib)
IA2_RELATION_FLOWS_FROM = "flowsFrom"
IA2_RELATION_FLOWS_TO = "flowsTo"

# A place to store live IAccessible NVDAObjects, that can be looked up by their window,objectID,
# childID event params.
liveNVDAObjectTable = weakref.WeakValueDictionary()

IAccessibleRolesToNVDARoles = {
	oleacc.ROLE_SYSTEM_WINDOW: controlTypes.ROLE_WINDOW,
	oleacc.ROLE_SYSTEM_CLIENT: controlTypes.ROLE_PANE,
	oleacc.ROLE_SYSTEM_TITLEBAR: controlTypes.ROLE_TITLEBAR,
	oleacc.ROLE_SYSTEM_DIALOG: controlTypes.ROLE_DIALOG,
	oleacc.ROLE_SYSTEM_PANE: controlTypes.ROLE_PANE,
	oleacc.ROLE_SYSTEM_CHECKBUTTON: controlTypes.ROLE_CHECKBOX,
	oleacc.ROLE_SYSTEM_RADIOBUTTON: controlTypes.ROLE_RADIOBUTTON,
	oleacc.ROLE_SYSTEM_STATICTEXT: controlTypes.ROLE_STATICTEXT,
	oleacc.ROLE_SYSTEM_TEXT: controlTypes.ROLE_EDITABLETEXT,
	oleacc.ROLE_SYSTEM_PUSHBUTTON: controlTypes.ROLE_BUTTON,
	oleacc.ROLE_SYSTEM_MENUBAR: controlTypes.ROLE_MENUBAR,
	oleacc.ROLE_SYSTEM_MENUITEM: controlTypes.ROLE_MENUITEM,
	oleacc.ROLE_SYSTEM_MENUPOPUP: controlTypes.ROLE_POPUPMENU,
	oleacc.ROLE_SYSTEM_COMBOBOX: controlTypes.ROLE_COMBOBOX,
	oleacc.ROLE_SYSTEM_LIST: controlTypes.ROLE_LIST,
	oleacc.ROLE_SYSTEM_LISTITEM: controlTypes.ROLE_LISTITEM,
	oleacc.ROLE_SYSTEM_GRAPHIC: controlTypes.ROLE_GRAPHIC,
	oleacc.ROLE_SYSTEM_HELPBALLOON: controlTypes.ROLE_HELPBALLOON,
	oleacc.ROLE_SYSTEM_TOOLTIP: controlTypes.ROLE_TOOLTIP,
	oleacc.ROLE_SYSTEM_LINK: controlTypes.ROLE_LINK,
	oleacc.ROLE_SYSTEM_OUTLINE: controlTypes.ROLE_TREEVIEW,
	oleacc.ROLE_SYSTEM_OUTLINEITEM: controlTypes.ROLE_TREEVIEWITEM,
	oleacc.ROLE_SYSTEM_OUTLINEBUTTON: controlTypes.ROLE_TREEVIEWITEM,
	oleacc.ROLE_SYSTEM_PAGETAB: controlTypes.ROLE_TAB,
	oleacc.ROLE_SYSTEM_PAGETABLIST: controlTypes.ROLE_TABCONTROL,
	oleacc.ROLE_SYSTEM_SLIDER: controlTypes.ROLE_SLIDER,
	oleacc.ROLE_SYSTEM_PROGRESSBAR: controlTypes.ROLE_PROGRESSBAR,
	oleacc.ROLE_SYSTEM_SCROLLBAR: controlTypes.ROLE_SCROLLBAR,
	oleacc.ROLE_SYSTEM_STATUSBAR: controlTypes.ROLE_STATUSBAR,
	oleacc.ROLE_SYSTEM_TABLE: controlTypes.ROLE_TABLE,
	oleacc.ROLE_SYSTEM_CELL: controlTypes.ROLE_TABLECELL,
	oleacc.ROLE_SYSTEM_COLUMN: controlTypes.ROLE_TABLECOLUMN,
	oleacc.ROLE_SYSTEM_ROW: controlTypes.ROLE_TABLEROW,
	oleacc.ROLE_SYSTEM_TOOLBAR: controlTypes.ROLE_TOOLBAR,
	oleacc.ROLE_SYSTEM_COLUMNHEADER: controlTypes.ROLE_TABLECOLUMNHEADER,
	oleacc.ROLE_SYSTEM_ROWHEADER: controlTypes.ROLE_TABLEROWHEADER,
	oleacc.ROLE_SYSTEM_SPLITBUTTON: controlTypes.ROLE_SPLITBUTTON,
	oleacc.ROLE_SYSTEM_BUTTONDROPDOWN: controlTypes.ROLE_DROPDOWNBUTTON,
	oleacc.ROLE_SYSTEM_SEPARATOR: controlTypes.ROLE_SEPARATOR,
	oleacc.ROLE_SYSTEM_DOCUMENT: controlTypes.ROLE_DOCUMENT,
	oleacc.ROLE_SYSTEM_ANIMATION: controlTypes.ROLE_ANIMATION,
	oleacc.ROLE_SYSTEM_APPLICATION: controlTypes.ROLE_APPLICATION,
	oleacc.ROLE_SYSTEM_GROUPING: controlTypes.ROLE_GROUPING,
	oleacc.ROLE_SYSTEM_PROPERTYPAGE: controlTypes.ROLE_PROPERTYPAGE,
	oleacc.ROLE_SYSTEM_ALERT: controlTypes.ROLE_ALERT,
	oleacc.ROLE_SYSTEM_BORDER: controlTypes.ROLE_BORDER,
	oleacc.ROLE_SYSTEM_BUTTONDROPDOWNGRID: controlTypes.ROLE_DROPDOWNBUTTONGRID,
	oleacc.ROLE_SYSTEM_CARET: controlTypes.ROLE_CARET,
	oleacc.ROLE_SYSTEM_CHARACTER: controlTypes.ROLE_CHARACTER,
	oleacc.ROLE_SYSTEM_CHART: controlTypes.ROLE_CHART,
	oleacc.ROLE_SYSTEM_CURSOR: controlTypes.ROLE_CURSOR,
	oleacc.ROLE_SYSTEM_DIAGRAM: controlTypes.ROLE_DIAGRAM,
	oleacc.ROLE_SYSTEM_DIAL: controlTypes.ROLE_DIAL,
	oleacc.ROLE_SYSTEM_DROPLIST: controlTypes.ROLE_DROPLIST,
	oleacc.ROLE_SYSTEM_BUTTONMENU: controlTypes.ROLE_MENUBUTTON,
	oleacc.ROLE_SYSTEM_EQUATION: controlTypes.ROLE_MATH,
	oleacc.ROLE_SYSTEM_GRIP: controlTypes.ROLE_GRIP,
	oleacc.ROLE_SYSTEM_HOTKEYFIELD: controlTypes.ROLE_HOTKEYFIELD,
	oleacc.ROLE_SYSTEM_INDICATOR: controlTypes.ROLE_INDICATOR,
	oleacc.ROLE_SYSTEM_SPINBUTTON: controlTypes.ROLE_SPINBUTTON,
	oleacc.ROLE_SYSTEM_SOUND: controlTypes.ROLE_SOUND,
	oleacc.ROLE_SYSTEM_WHITESPACE: controlTypes.ROLE_WHITESPACE,
	oleacc.ROLE_SYSTEM_IPADDRESS: controlTypes.ROLE_IPADDRESS,
	oleacc.ROLE_SYSTEM_OUTLINEBUTTON: controlTypes.ROLE_TREEVIEWBUTTON,
	oleacc.ROLE_SYSTEM_CLOCK: controlTypes.ROLE_CLOCK,
	# IAccessible2 roles
	IA2_ROLE_UNKNOWN: controlTypes.ROLE_UNKNOWN,
	IA2_ROLE_CANVAS: controlTypes.ROLE_CANVAS,
	IA2_ROLE_CAPTION: controlTypes.ROLE_CAPTION,
	IA2_ROLE_CHECK_MENU_ITEM: controlTypes.ROLE_CHECKMENUITEM,
	IA2_ROLE_COLOR_CHOOSER: controlTypes.ROLE_COLORCHOOSER,
	IA2_ROLE_DATE_EDITOR: controlTypes.ROLE_DATEEDITOR,
	IA2_ROLE_DESKTOP_ICON: controlTypes.ROLE_DESKTOPICON,
	IA2_ROLE_DESKTOP_PANE: controlTypes.ROLE_DESKTOPPANE,
	IA2_ROLE_DIRECTORY_PANE: controlTypes.ROLE_DIRECTORYPANE,
	IA2_ROLE_EDITBAR: controlTypes.ROLE_EDITBAR,
	IA2_ROLE_EMBEDDED_OBJECT: controlTypes.ROLE_EMBEDDEDOBJECT,
	IA2_ROLE_ENDNOTE: controlTypes.ROLE_ENDNOTE,
	IA2_ROLE_FILE_CHOOSER: controlTypes.ROLE_FILECHOOSER,
	IA2_ROLE_FONT_CHOOSER: controlTypes.ROLE_FONTCHOOSER,
	IA2_ROLE_FOOTER: controlTypes.ROLE_FOOTER,
	IA2_ROLE_FOOTNOTE: controlTypes.ROLE_FOOTNOTE,
	IA2_ROLE_FORM: controlTypes.ROLE_FORM,
	IA2_ROLE_FRAME: controlTypes.ROLE_FRAME,
	IA2_ROLE_GLASS_PANE: controlTypes.ROLE_GLASSPANE,
	IA2_ROLE_HEADER: controlTypes.ROLE_HEADER,
	IA2_ROLE_HEADING: controlTypes.ROLE_HEADING,
	IA2_ROLE_ICON: controlTypes.ROLE_ICON,
	IA2_ROLE_IMAGE_MAP: controlTypes.ROLE_IMAGEMAP,
	IA2_ROLE_INPUT_METHOD_WINDOW: controlTypes.ROLE_INPUTWINDOW,
	IA2_ROLE_INTERNAL_FRAME: controlTypes.ROLE_INTERNALFRAME,
	IA2_ROLE_LABEL: controlTypes.ROLE_LABEL,
	IA2_ROLE_LAYERED_PANE: controlTypes.ROLE_LAYEREDPANE,
	IA2_ROLE_NOTE: controlTypes.ROLE_NOTE,
	IA2_ROLE_OPTION_PANE: controlTypes.ROLE_OPTIONPANE,
	IA2_ROLE_PAGE: controlTypes.ROLE_PAGE,
	IA2_ROLE_PARAGRAPH: controlTypes.ROLE_PARAGRAPH,
	IA2_ROLE_RADIO_MENU_ITEM: controlTypes.ROLE_RADIOMENUITEM,
	IA2_ROLE_REDUNDANT_OBJECT: controlTypes.ROLE_REDUNDANTOBJECT,
	IA2_ROLE_ROOT_PANE: controlTypes.ROLE_ROOTPANE,
	IA2_ROLE_RULER: controlTypes.ROLE_RULER,
	IA2_ROLE_SCROLL_PANE: controlTypes.ROLE_SCROLLPANE,
	IA2_ROLE_SECTION: controlTypes.ROLE_SECTION,
	IA2_ROLE_SHAPE: controlTypes.ROLE_SHAPE,
	IA2_ROLE_SPLIT_PANE: controlTypes.ROLE_SPLITPANE,
	IA2_ROLE_TEAR_OFF_MENU: controlTypes.ROLE_TEAROFFMENU,
	IA2_ROLE_TERMINAL: controlTypes.ROLE_TERMINAL,
	IA2_ROLE_TEXT_FRAME: controlTypes.ROLE_TEXTFRAME,
	IA2_ROLE_TOGGLE_BUTTON: controlTypes.ROLE_TOGGLEBUTTON,
	IA2_ROLE_VIEW_PORT: controlTypes.ROLE_VIEWPORT,
	IA2_ROLE_CONTENT_DELETION: controlTypes.ROLE_DELETED_CONTENT,
	IA2_ROLE_CONTENT_INSERTION: controlTypes.ROLE_INSERTED_CONTENT,
	IA2_ROLE_BLOCK_QUOTE: controlTypes.ROLE_BLOCKQUOTE,
	IA2.IA2_ROLE_LANDMARK: controlTypes.ROLE_LANDMARK,
	IA2_ROLE_MARK: controlTypes.ROLE_MARKED_CONTENT,
	# some common string roles
	"frame": controlTypes.ROLE_FRAME,
	"iframe": controlTypes.ROLE_INTERNALFRAME,
	"page": controlTypes.ROLE_PAGE,
	"form": controlTypes.ROLE_FORM,
	"div": controlTypes.ROLE_SECTION,
	"li": controlTypes.ROLE_LISTITEM,
	"ul": controlTypes.ROLE_LIST,
	"tbody": controlTypes.ROLE_TABLEBODY,
	"browser": controlTypes.ROLE_WINDOW,
	"h1": controlTypes.ROLE_HEADING1,
	"h2": controlTypes.ROLE_HEADING2,
	"h3": controlTypes.ROLE_HEADING3,
	"h4": controlTypes.ROLE_HEADING4,
	"h5": controlTypes.ROLE_HEADING5,
	"h6": controlTypes.ROLE_HEADING6,
	"p": controlTypes.ROLE_PARAGRAPH,
	"hbox": controlTypes.ROLE_BOX,
	"embed": controlTypes.ROLE_EMBEDDEDOBJECT,
	"object": controlTypes.ROLE_EMBEDDEDOBJECT,
	"applet": controlTypes.ROLE_EMBEDDEDOBJECT,
}

IAccessibleStatesToNVDAStates = {
	oleacc.STATE_SYSTEM_TRAVERSED: controlTypes.STATE_VISITED,
	oleacc.STATE_SYSTEM_UNAVAILABLE: controlTypes.STATE_UNAVAILABLE,
	oleacc.STATE_SYSTEM_FOCUSED: controlTypes.STATE_FOCUSED,
	oleacc.STATE_SYSTEM_SELECTED: controlTypes.STATE_SELECTED,
	oleacc.STATE_SYSTEM_BUSY: controlTypes.STATE_BUSY,
	oleacc.STATE_SYSTEM_PRESSED: controlTypes.STATE_PRESSED,
	oleacc.STATE_SYSTEM_CHECKED: controlTypes.STATE_CHECKED,
	oleacc.STATE_SYSTEM_MIXED: controlTypes.STATE_HALFCHECKED,
	oleacc.STATE_SYSTEM_READONLY: controlTypes.STATE_READONLY,
	oleacc.STATE_SYSTEM_EXPANDED: controlTypes.STATE_EXPANDED,
	oleacc.STATE_SYSTEM_COLLAPSED: controlTypes.STATE_COLLAPSED,
	oleacc.STATE_SYSTEM_OFFSCREEN: controlTypes.STATE_OFFSCREEN,
	oleacc.STATE_SYSTEM_INVISIBLE: controlTypes.STATE_INVISIBLE,
	oleacc.STATE_SYSTEM_TRAVERSED: controlTypes.STATE_VISITED,
	oleacc.STATE_SYSTEM_LINKED: controlTypes.STATE_LINKED,
	oleacc.STATE_SYSTEM_HASPOPUP: controlTypes.STATE_HASPOPUP,
	oleacc.STATE_SYSTEM_PROTECTED: controlTypes.STATE_PROTECTED,
	oleacc.STATE_SYSTEM_SELECTABLE: controlTypes.STATE_SELECTABLE,
	oleacc.STATE_SYSTEM_FOCUSABLE: controlTypes.STATE_FOCUSABLE,
}

IAccessible2StatesToNVDAStates = {
	IA2_STATE_REQUIRED: controlTypes.STATE_REQUIRED,
	IA2_STATE_DEFUNCT: controlTypes.STATE_DEFUNCT,
	# IA2_STATE_STALE:controlTypes.STATE_DEFUNCT,
	IA2_STATE_INVALID_ENTRY: controlTypes.STATE_INVALID_ENTRY,
	IA2_STATE_MODAL: controlTypes.STATE_MODAL,
	IA2_STATE_SUPPORTS_AUTOCOMPLETION: controlTypes.STATE_AUTOCOMPLETE,
	IA2_STATE_MULTI_LINE: controlTypes.STATE_MULTILINE,
	IA2_STATE_ICONIFIED: controlTypes.STATE_ICONIFIED,
	IA2_STATE_EDITABLE: controlTypes.STATE_EDITABLE,
	IA2_STATE_PINNED: controlTypes.STATE_PINNED,
	IA2_STATE_CHECKABLE: controlTypes.STATE_CHECKABLE,
}


def normalizeIAccessible(pacc, childID=0):
	if not isinstance(pacc, IAccessible):
		try:
			pacc = pacc.QueryInterface(IAccessible)
		except COMError:
			raise RuntimeError("%s Not an IAccessible" % pacc)
	# #2558: IAccessible2 doesn't support simple children.
	# Therefore, it doesn't make sense to use IA2 if the child ID is non-0.
	if childID == 0 and not isinstance(pacc, IAccessible2):
		try:
			s = pacc.QueryInterface(IServiceProvider)
			pacc2 = s.QueryService(IAccessible._iid_, IAccessible2)
			if not pacc2:
				# QueryService should fail if IA2 is not supported, but some applications such as AIM 7 misbehave
				# and return a null COM pointer. Treat this as if QueryService failed.
				raise ValueError
			pacc = pacc2
		except:  # noqa: E722 Bare except
			pass
	return pacc


def accessibleObjectFromEvent(window, objectID, childID):
	try:
		pacc, childID = oleacc.AccessibleObjectFromEvent(window, objectID, childID)
	except Exception as e:
		if isMSAADebugLoggingEnabled():
			log.debugWarning(
				f"oleacc.AccessibleObjectFromEvent failed with {e}."
				f" WinEvent: {getWinEventLogInfo(window, objectID, childID)}"
			)
		return None
	return normalizeIAccessible(pacc, childID), childID


def accessibleObjectFromPoint(x, y):
	try:
		pacc, child = oleacc.AccessibleObjectFromPoint(x, y)
	except:  # noqa: E722 Bare except
		return None
	return normalizeIAccessible(pacc, child), child


def windowFromAccessibleObject(ia):
	try:
		return oleacc.WindowFromAccessibleObject(ia)
	except:  # noqa: E722 Bare except
		return 0


def accessibleChildren(ia, startIndex, numChildren):
	# #4091: AccessibleChildren can throw WindowsError (blocked by callee) e.g. Outlook 2010 Email setup and
	# new profiles dialogs
	try:
		rawChildren = oleacc.AccessibleChildren(ia, startIndex, numChildren)
	except (WindowsError, COMError):
		log.debugWarning("AccessibleChildren failed", exc_info=True)
		return []
	children = []
	for child in rawChildren:
		if child is None:
			# This is a bug in the server.
			# Filtering these out here makes life easier for the caller.
			continue
		elif (
			isinstance(child, comtypes.client.lazybind.Dispatch)
			or isinstance(child, comtypes.client.dynamic._Dispatch)
			or isinstance(child, IUnknown)
		):
			child = (normalizeIAccessible(child), 0)
		elif isinstance(child, int):
			child = (ia, child)
		children.append(child)
	return children


def accFocus(ia):
	try:
		res = ia.accFocus
		if (
			isinstance(res, comtypes.client.lazybind.Dispatch)
			or isinstance(res, comtypes.client.dynamic._Dispatch)
			or isinstance(res, IUnknown)
		):
			new_ia = normalizeIAccessible(res)
			new_child = 0
		elif res == 0:
			# #3005: Don't call accChild for CHILDID_SELF.
			new_ia = ia
			new_child = res
		elif isinstance(res, int):
			# accFocus can return a child ID even when there is actually an IAccessible for that child; e.g. Lotus
			# Symphony.
			try:
				new_ia = ia.accChild(res)
			except:  # noqa: E722 Bare except
				new_ia = None
			if new_ia:
				new_ia = normalizeIAccessible(new_ia)
				new_child = 0
			else:
				new_ia = ia
				new_child = res
		else:
			return None
		return new_ia, new_child
	except:  # noqa: E722 Bare except
		return None


def accHitTest(ia, x, y):
	try:
		res = ia.accHitTest(x, y)
	except COMError:
		return None
	if (
		isinstance(res, comtypes.client.lazybind.Dispatch)
		or isinstance(res, comtypes.client.dynamic._Dispatch)
		or isinstance(res, IUnknown)
	):
		return accHitTest(normalizeIAccessible(res), x, y), 0
	elif isinstance(res, int):
		return ia, res
	return None


def accChild(ia, child):
	try:
		res = ia.accChild(child)
		if not res:
			return (ia, child)
		elif (
			isinstance(res, comtypes.client.lazybind.Dispatch)
			or isinstance(res, comtypes.client.dynamic._Dispatch)
			or isinstance(res, IUnknown)
		):
			return normalizeIAccessible(res), 0
	except:  # noqa: E722 Bare except
		pass
	return None


def accParent(ia, child):
	try:
		if not child:
			res = ia.accParent
			if (
				isinstance(res, comtypes.client.lazybind.Dispatch)
				or isinstance(res, comtypes.client.dynamic._Dispatch)
				or isinstance(res, IUnknown)
			):
				new_ia = normalizeIAccessible(res)
				new_child = 0
			else:
				raise ValueError("no IAccessible interface")
		else:
			new_ia = ia
			new_child = 0
		return new_ia, new_child
	except:  # noqa: E722 Bare except
		return None


def accNavigate(pacc, childID, direction):
	try:
		res = pacc.accNavigate(direction, childID)
	except COMError:
		res = None
	if not res:
		return None
	elif isinstance(res, int):
		if childID == 0 and oleacc.NAVDIR_UP <= direction <= oleacc.NAVDIR_PREVIOUS:
			parentRes = accParent(pacc, 0)
			if not parentRes:
				return None
			pacc = parentRes[0]
		return pacc, res
	elif (
		isinstance(res, comtypes.client.lazybind.Dispatch)
		or isinstance(res, comtypes.client.dynamic._Dispatch)
		or isinstance(res, IUnknown)
	):
		return normalizeIAccessible(res, 0), 0
	else:
		log.debugWarning("Unknown IAccessible type: %s" % res, stack_info=True)
		return None


def winEventToNVDAEvent(eventID, window, objectID, childID, useCache=True):
	"""Tries to convert a win event ID to an NVDA event name, and instanciate or fetch an NVDAObject for
	 the win event parameters.
	@param eventID: the win event ID (type)
	@type eventID: integer
	@param window: the win event's window handle
	@type window: integer
	@param objectID: the win event's object ID
	@type objectID: integer
	@param childID: the win event's childID
	@type childID: the win event's childID
	@param useCache: C{True} to use the L{liveNVDAObjectTable} cache when
	 retrieving an NVDAObject, C{False} if the cache should not be used.
	@type useCache: boolean
	@returns: the NVDA event name and the NVDAObject the event is for
	@rtype: tuple of string and L{NVDAObjects.IAccessible.IAccessible}
	"""
	if isMSAADebugLoggingEnabled():
		log.debug(
			f"Creating NVDA event from winEvent: {getWinEventLogInfo(window, objectID, childID, eventID)}, "
			f"use cache {useCache}"
		)
	NVDAEventName = winEventIDsToNVDAEventNames.get(eventID, None)
	if not NVDAEventName:
		log.debugWarning(f"No NVDA event name for {getWinEventName(eventID)}")
		return None
	if isMSAADebugLoggingEnabled():
		log.debug(f"winEvent mapped to NVDA event: {NVDAEventName}")
	# Ignore any events with invalid window handles
	if not window or not winUser.isWindow(window):
		if isMSAADebugLoggingEnabled():
			log.debug(
				f"Invalid window. Dropping winEvent {getWinEventLogInfo(window, objectID, childID, eventID)}"
			)
		return None
	# Make sure this window does not have a ghost window if possible
	if NVDAObjects.window.GhostWindowFromHungWindow and NVDAObjects.window.GhostWindowFromHungWindow(window):
		if isMSAADebugLoggingEnabled():
			log.debug(
				f"Ghosted hung window. Dropping winEvent {getWinEventLogInfo(window, objectID, childID, eventID)}"
			)
		return None
	# We do not support MSAA object proxied from native UIA
	if UIAHandler.handler and UIAHandler.handler.isUIAWindow(window):
		if isMSAADebugLoggingEnabled():
			log.debug(
				f"Native UIA window. Dropping winEvent {getWinEventLogInfo(window, objectID, childID, eventID)}"
			)
		return None
	obj = None
	if useCache:
		# See if we already know an object by this win event info
		obj = liveNVDAObjectTable.get((window, objectID, childID), None)
		if isMSAADebugLoggingEnabled() and obj:
			log.debug(
				f"Fetched existing NVDAObject {obj} from liveNVDAObjectTable"
				f" for winEvent {getWinEventLogInfo(window, objectID, childID)}"
			)
	# If we don't yet have the object, then actually instanciate it.
	if not obj:
		obj = NVDAObjects.IAccessible.getNVDAObjectFromEvent(window, objectID, childID)
	# At this point if we don't have an object then we can't do any more
	if not obj:
		if isMSAADebugLoggingEnabled():
			log.debug(
				"Could not instantiate an NVDAObject for winEvent: "
				f"{getWinEventLogInfo(window, objectID, childID, eventID)}"
			)
		return None
	# SDM MSAA objects sometimes don't contain enough information to be useful Sometimes there is a real
	# window that does, so try to get the SDMChild property on the NVDAObject, and if successull use that as
	# obj instead.
	if 'bosa_sdm' in obj.windowClassName:
		SDMChild = getattr(obj, 'SDMChild', None)
		if SDMChild:
			obj = SDMChild
	if isMSAADebugLoggingEnabled():
		log.debug(
			f"Successfully created NVDA event {NVDAEventName} for {obj} "
			f"from winEvent {getWinEventLogInfo(window, objectID, childID, eventID)}"
		)
	return (NVDAEventName, obj)


def processGenericWinEvent(eventID, window, objectID, childID):
	"""Converts the win event to an NVDA event,
	Checks to see if this NVDAObject  equals the current focus.
	If all goes well, then the event is queued and we return True
	@param eventID: a win event ID (type)
	@type eventID: integer
	@param window: a win event's window handle
	@type window: integer
	@param objectID: a win event's object ID
	@type objectID: integer
	@param childID: a win event's child ID
	@type childID: integer
	@returns: True if the event was processed, False otherwise.
	@rtype: boolean
	"""
	if isMSAADebugLoggingEnabled():
		log.debug(
			f"Processing generic winEvent: {getWinEventLogInfo(window, objectID, childID, eventID)}"
		)
	# Notify appModuleHandler of this new window
	appModuleHandler.update(winUser.getWindowThreadProcessID(window)[0])
	# Handle particular events for the special MSAA caret object just as if they were for the focus object
	focus = eventHandler.lastQueuedFocusObject
	if focus and objectID == winUser.OBJID_CARET and eventID in (
		winUser.EVENT_OBJECT_LOCATIONCHANGE,
		winUser.EVENT_OBJECT_SHOW
	):
		if isMSAADebugLoggingEnabled():
			log.debug("handling winEvent as caret event on focus")
		NVDAEvent = ("caret", focus)
	else:
		NVDAEvent = winEventToNVDAEvent(eventID, window, objectID, childID)
		if not NVDAEvent:
			return False
	if NVDAEvent[0] == "nameChange" and objectID == winUser.OBJID_CURSOR:
		if isMSAADebugLoggingEnabled():
			log.debug("Handling winEvent as mouse shape change")
		mouseHandler.updateMouseShape(NVDAEvent[1].name)
		return
	if NVDAEvent[1] == focus:
		if isMSAADebugLoggingEnabled():
			log.debug(
				f"Directing winEvent to focus object {focus}. WinEvent {getWinEventLogInfo(window, objectID, childID)}"
			)
		NVDAEvent = (NVDAEvent[0], focus)
	eventHandler.queueEvent(*NVDAEvent)
	return True


def processFocusWinEvent(window, objectID, childID, force=False):
	"""checks to see if the focus win event is not the same as the existing focus,
	then converts the win event to an NVDA event (instantiating an NVDA Object) then calls
	processFocusNVDAEvent. If all is ok it returns True.
	@type window: integer
	@param objectID: a win event's object ID
	@type objectID: integer
	@param childID: a win event's child ID
	@type childID: integer
	@param force: If True, the shouldAllowIAccessibleFocusEvent property of the object is ignored.
	@type force: boolean
	@returns: True if the focus is valid and was handled, False otherwise.
	@rtype: boolean
	"""
	if isMSAADebugLoggingEnabled():
		log.debug(
			f"Processing focus winEvent: {getWinEventLogInfo(window, objectID, childID)}, "
			f"force {force}"
		)
	windowClassName = winUser.getClassName(window)
	# Generally, we must ignore focus on child windows of SDM windows as we only want the SDM MSAA events.
	# However, we don't want to ignore focus if the child ID isn't 0,
	# as this is a child control and the SDM MSAA events don't handle child controls.
	if (
		childID == 0
		and not windowClassName.startswith('bosa_sdm')
		and winUser.getClassName(winUser.getAncestor(window, winUser.GA_PARENT)).startswith('bosa_sdm')
	):
		if isMSAADebugLoggingEnabled():
			log.debug(
				f"Focus event for child window of MS Office SDM window. "
				f"Dropping winEvent {getWinEventLogInfo(window, objectID, childID)}, "
			)
		return False
	# Notify appModuleHandler of this new foreground window
	appModuleHandler.update(winUser.getWindowThreadProcessID(window)[0])
	# If Java access bridge is running, and this is a java window, then pass it to java and forget about it
	if (
		childID == 0
		and objectID == winUser.OBJID_CLIENT
		and JABHandler.isRunning
		and JABHandler.isJavaWindow(window)
	):
		if isMSAADebugLoggingEnabled():
			log.debug(
				f"Redirecting focus to Java window. WinEvent {getWinEventLogInfo(window, objectID, childID)}"
			)
		JABHandler.event_enterJavaWindow(window)
		return True
	# Convert the win event to an NVDA event
	NVDAEvent = winEventToNVDAEvent(winUser.EVENT_OBJECT_FOCUS, window, objectID, childID, useCache=False)
	if not NVDAEvent:
		return False
	eventName, obj = NVDAEvent
	if (
		(childID == 0 and obj.IAccessibleRole == oleacc.ROLE_SYSTEM_LIST)
		or (objectID == winUser.OBJID_CLIENT and "SysListView32" in obj.windowClassName)
	):
		# Some controls incorrectly fire focus on child ID 0, even when there is a child with focus.
		try:
			realChildID = obj.IAccessibleObject.accFocus
		except:  # noqa: E722 Bare except
			realChildID = None
		if isinstance(realChildID, int) and realChildID > 0 and realChildID != childID:
			realObj = NVDAObjects.IAccessible.IAccessible(
				IAccessibleObject=obj.IAccessibleObject,
				IAccessibleChildID=realChildID,
				event_windowHandle=window,
				event_objectID=objectID,
				event_childID=realChildID
			)
			if realObj:
				obj = realObj
	return processFocusNVDAEvent(obj, force=force)


def processFocusNVDAEvent(obj, force=False):
	"""Processes a focus NVDA event.
	If the focus event is valid, it is queued.
	@param obj: the NVDAObject the focus event is for
	@type obj: L{NVDAObjects.NVDAObject}
	@param force: If True, the shouldAllowIAccessibleFocusEvent property of the object is ignored.
	@type force: boolean
	@return: C{True} if the focus event is valid and was queued, C{False} otherwise.
	@rtype: boolean
	"""
	if not force and isinstance(obj, NVDAObjects.IAccessible.IAccessible):
		focus = eventHandler.lastQueuedFocusObject
		if isinstance(focus, NVDAObjects.IAccessible.IAccessible) and focus.isDuplicateIAccessibleEvent(obj):
			if isMSAADebugLoggingEnabled():
				log.debug(f"Dropping duplicate IAccessible focus event for {obj}")
			return True
		if not obj.shouldAllowIAccessibleFocusEvent:
			if isMSAADebugLoggingEnabled():
				log.debug(f"IAccessible focus event not allowed by {obj}")
			return False
	eventHandler.queueEvent('gainFocus', obj)
	return True


class SecureDesktopNVDAObject(NVDAObjects.window.Desktop):

	def findOverlayClasses(self, clsList):
		clsList.append(SecureDesktopNVDAObject)
		return clsList

	def _get_name(self):
		# Translators: Message to indicate User Account Control (UAC) or other secure desktop screen is active.
		return _("Secure Desktop")

	def _get_role(self):
		return controlTypes.ROLE_PANE

	def event_gainFocus(self):
		super(SecureDesktopNVDAObject, self).event_gainFocus()
		# After handling the focus, NVDA should sleep while the secure desktop is active.
		self.sleepMode = self.SLEEP_FULL


def processDesktopSwitchWinEvent(window, objectID, childID):
	if isMSAADebugLoggingEnabled():
		log.debug(
			f"Processing desktopSwitch winEvent: {getWinEventLogInfo(window, objectID, childID)}"
		)
	hDesk = windll.user32.OpenInputDesktop(0, False, 0)
	if hDesk != 0:
		windll.user32.CloseDesktop(hDesk)
		core.callLater(200, _correctFocus)
	else:
		# Switching to a secure desktop.
		# We don't receive key up events for any keys down before switching to a secure desktop,
		# so clear our recorded modifiers.
		keyboardHandler.currentModifiers.clear()
		obj = SecureDesktopNVDAObject(windowHandle=window)
		eventHandler.executeEvent("gainFocus", obj)


def _correctFocus():
	eventHandler.queueEvent("gainFocus", api.getDesktopObject().objectWithFocus())


def processForegroundWinEvent(window, objectID, childID):
	"""checks to see if the foreground win event is not the same as the existing focus or any of its parents,
	then converts the win event to an NVDA event (instantiating an NVDA Object) and then checks the NVDAObject
	against the existing focus object.
	If all is ok it queues the foreground event to NVDA and returns True.
	@param window: a win event's window handle
	@type window: integer
	@param objectID: a win event's object ID
	@type objectID: integer
	@param childID: a win event's child ID
	@type childID: integer
	@returns: True if the foreground was processed, False otherwise.
	@rtype: boolean
	"""
	if isMSAADebugLoggingEnabled():
		log.debug(
			f"Processing foreground winEvent: {getWinEventLogInfo(window, objectID, childID)}"
		)
	# Ignore foreground events on windows that aren't the current foreground window
	if window != winUser.getForegroundWindow():
		if isMSAADebugLoggingEnabled():
			log.debug(
				f"Dropping foreground winEvent as it does not match GetForegroundWindow. "
				f"WinEvent {getWinEventLogInfo(window, objectID, childID)}"
			)
		return False
	# If there is a pending gainFocus, it will handle the foreground object.
	oldFocus = eventHandler.lastQueuedFocusObject
	# If this foreground win event's window is an ancestor of the existing focus's window, then ignore it
	if (
		isinstance(oldFocus, NVDAObjects.window.Window)
		and winUser.isDescendantWindow(window, oldFocus.windowHandle)
	):
		if isMSAADebugLoggingEnabled():
			log.debug(
				f"Dropping foreground winEvent as focus is already on a descendant. "
				f"WinEvent {getWinEventLogInfo(window, objectID, childID)}"
			)
		return False
	# If the existing focus has the same win event params as these, then ignore this event
	if (
		isinstance(oldFocus, NVDAObjects.IAccessible.IAccessible)
		and window == oldFocus.event_windowHandle
		and objectID == oldFocus.event_objectID
		and childID == oldFocus.event_childID
	):
		if isMSAADebugLoggingEnabled():
			log.debug(
				f"Dropping foreground winEvent as it is duplicate to existing focus. "
				f"WinEvent {getWinEventLogInfo(window, objectID, childID)}"
			)
		return False
	# Notify appModuleHandler of this new foreground window
	appModuleHandler.update(winUser.getWindowThreadProcessID(window)[0])
	# If Java access bridge is running, and this is a java window, then pass it to java and forget about it
	if JABHandler.isRunning and JABHandler.isJavaWindow(window):
		JABHandler.event_enterJavaWindow(window)
		if isMSAADebugLoggingEnabled():
			log.debug(
				f"Redirecting foreground winEvent to Java window. "
				f"WinEvent {getWinEventLogInfo(window, objectID, childID)}"
			)
		return True
	# Convert the win event to an NVDA event
	NVDAEvent = winEventToNVDAEvent(winUser.EVENT_SYSTEM_FOREGROUND, window, objectID, childID, useCache=False)
	if not NVDAEvent:
		if isMSAADebugLoggingEnabled():
			log.debug(
				f"Could not convert foreground winEvent to an NVDA event. "
				f"WinEvent {getWinEventLogInfo(window, objectID, childID)}"
			)
		return False
	eventHandler.queueEvent(*NVDAEvent)
	return True


def processShowWinEvent(window, objectID, childID):
	if isMSAADebugLoggingEnabled():
		log.debug(
			f"Processing show winEvent: {getWinEventLogInfo(window, objectID, childID)}"
		)
	# eventHandler.shouldAcceptEvent only accepts show events for a few specific cases.
	# Narrow this further to only accept events for clients or custom objects.
	if objectID == winUser.OBJID_CLIENT or objectID > 0:
		NVDAEvent = winEventToNVDAEvent(winUser.EVENT_OBJECT_SHOW, window, objectID, childID)
		if NVDAEvent:
			eventHandler.queueEvent(*NVDAEvent)


def processDestroyWinEvent(window, objectID, childID):
	"""Process a destroy win event.
	This removes the object associated with the event parameters from L{liveNVDAObjectTable} if
	such an object exists.
	"""
	if isMSAADebugLoggingEnabled():
		log.debug(
			f"Processing destroy winEvent: {getWinEventLogInfo(window, objectID, childID)}"
		)
	try:
		del liveNVDAObjectTable[(window, objectID, childID)]
	except KeyError:
		pass
	# Specific support for input method MSAA candidate lists.
	# When their window is destroyed we must correct focus to its parent - which could be a composition string
	# so can't use generic focus correction. (#2695)
	focus = api.getFocusObject()
	from NVDAObjects.IAccessible.mscandui import BaseCandidateItem
	if (
		objectID == 0
		and childID == 0
		and isinstance(focus, BaseCandidateItem)
		and window == focus.windowHandle
		and not eventHandler.isPendingEvents("gainFocus")
	):
		obj = focus.container
		if obj:
			eventHandler.queueEvent("gainFocus", obj)


def processMenuStartWinEvent(eventID, window, objectID, childID, validFocus):
	"""Process a menuStart win event.
	@postcondition: Focus will be directed to the menu if appropriate.
	"""
	if isMSAADebugLoggingEnabled():
		log.debug(
			f"Processing menuStart winEvent: {getWinEventLogInfo(window, objectID, childID)}, "
			f"validFocus {validFocus}"
		)
	if validFocus:
		lastFocus = eventHandler.lastQueuedFocusObject
		if (
			isinstance(lastFocus, NVDAObjects.IAccessible.IAccessible)
			and lastFocus.IAccessibleRole in (oleacc.ROLE_SYSTEM_MENUPOPUP, oleacc.ROLE_SYSTEM_MENUITEM)
		):
			# Focus has already been set to a menu or menu item, so we don't need to handle the menuStart.
			return
	NVDAEvent = winEventToNVDAEvent(eventID, window, objectID, childID)
	if not NVDAEvent:
		return
	eventName, obj = NVDAEvent
	if obj.IAccessibleRole != oleacc.ROLE_SYSTEM_MENUPOPUP:
		# menuStart on anything other than a menu is silly.
		return
	processFocusNVDAEvent(obj, force=True)


def processFakeFocusWinEvent(eventID, window, objectID, childID):
	"""Process a fake focus win event.
	@postcondition: The focus will be found and an event generated for it if appropriate.
	"""
	# A suitable event for faking the focus has been received with no focus event, so we probably need to
	# find the focus and fake it.
	# However, it is possible that the focus event has simply been delayed, so wait a bit and only do it if
	# the focus hasn't changed yet.
	if isMSAADebugLoggingEnabled():
		log.debug(
			f"Processing fake focus winEvent {getWinEventLogInfo(window, objectID, childID)}"
		)
	core.callLater(50, _fakeFocus, api.getFocusObject())


def _fakeFocus(oldFocus):
	if oldFocus is not api.getFocusObject():
		# The focus has changed - no need to fake it.
		return
	focus = api.getDesktopObject().objectWithFocus()
	if not focus:
		return
	if isMSAADebugLoggingEnabled():
		log.debug(
			f"Faking focus on {focus}"
		)
	processFocusNVDAEvent(focus)


#: Only valid after initialisation.
accPropServices = None


def initialize():
	global accPropServices
	try:
		accPropServices = comtypes.client.CreateObject(CAccPropServices)
	except (WindowsError, COMError) as e:
		log.debugWarning("AccPropServices is not available: %s" % e)
	internalWinEventHandler.initialize(processDestroyWinEvent)


# C901 'pumpAll' is too complex
def pumpAll():  # noqa: C901
	if not _shouldGetEvents():
		return
	focusWinEvents = []
	validFocus = False
	fakeFocusEvent = None
	focus = eventHandler.lastQueuedFocusObject

	alwaysAllowedObjects = []
	# winEvents for the currently focused object are special,
	# and should be never filtered out.
	if isinstance(focus, NVDAObjects.IAccessible.IAccessible) and focus.event_objectID is not None:
		alwaysAllowedObjects.append((focus.event_windowHandle, focus.event_objectID, focus.event_childID))

	# Receive all the winEvents from the limiter for this cycle
	winEvents = winEventLimiter.flushEvents(alwaysAllowedObjects)

	for winEvent in winEvents:
		isEventOnCaret = winEvent[2] == winUser.OBJID_CARET
		showHideCaretEvent = focus and isEventOnCaret and winEvent[0] in [
			winUser.EVENT_OBJECT_SHOW,
			winUser.EVENT_OBJECT_HIDE
		]
		# #4001: Ideally, we'd call shouldAcceptEvent in winEventCallback, but this causes focus issues when
		# starting applications. #7332: If this is a show event, which would normally be dropped by
		# `shouldAcceptEvent` and this event is for the caret, later it will be mapped to a caret event,
		# so skip `shouldAcceptEvent`
		if showHideCaretEvent:
			if not focus.shouldAcceptShowHideCaretEvent:
				continue
		elif not eventHandler.shouldAcceptEvent(
			winEventIDsToNVDAEventNames[winEvent[0]],
			windowHandle=winEvent[1]
		):
			continue
		# We want to only pass on one focus event to NVDA, but we always want to use the most recent possible one
		if winEvent[0] in (
			winUser.EVENT_OBJECT_FOCUS,
			winUser.EVENT_SYSTEM_FOREGROUND
		):
			focusWinEvents.append(winEvent)
			continue
		else:
			for focusWinEvent in reversed(focusWinEvents):
				isForeground = focusWinEvent[0] == winUser.EVENT_SYSTEM_FOREGROUND
				procFunc = processForegroundWinEvent if isForeground else processFocusWinEvent
				if procFunc(*(focusWinEvent[1:])):
					validFocus = True
					break
			focusWinEvents = []
			if winEvent[0] == winUser.EVENT_SYSTEM_DESKTOPSWITCH:
				processDesktopSwitchWinEvent(*winEvent[1:])
			# we dont want show caret events to be processed by `processShowWinEvent`, instead they should be
			# handled by `processGenericWinEvent`
			elif winEvent[0] == winUser.EVENT_OBJECT_SHOW and not isEventOnCaret:
				processShowWinEvent(*winEvent[1:])
			elif winEvent[0] in MENU_EVENTIDS + (winUser.EVENT_SYSTEM_SWITCHEND,):
				# If there is no valid focus event, we may need to use this to fake the focus later.
				fakeFocusEvent = winEvent
			else:
				processGenericWinEvent(*winEvent)
	for focusWinEvent in reversed(focusWinEvents):
		isForeground = focusWinEvent[0] == winUser.EVENT_SYSTEM_FOREGROUND
		procFunc = processForegroundWinEvent if isForeground else processFocusWinEvent
		if procFunc(*(focusWinEvent[1:])):
			validFocus = True
			break
	if fakeFocusEvent:
		# Try this as a last resort.
		if fakeFocusEvent[0] in (
			winUser.EVENT_SYSTEM_MENUSTART,
			winUser.EVENT_SYSTEM_MENUPOPUPSTART
		):
			# menuStart needs to be handled specially and might act even if there was a valid focus event.
			processMenuStartWinEvent(*fakeFocusEvent, validFocus=validFocus)
		elif not validFocus:
			# Other fake focus events only need to be handled if there was no valid focus event.
			processFakeFocusWinEvent(*fakeFocusEvent)


def terminate():
	internalWinEventHandler.terminate()


def getIAccIdentity(pacc, childID):
	IAccIdentityObject = pacc.QueryInterface(IAccIdentity)
	stringPtr, stringSize = IAccIdentityObject.getIdentityString(childID)
	try:
		if accPropServices:
			try:
				hwnd, objectID, childID = accPropServices.DecomposeHwndIdentityString(stringPtr, stringSize)
				return dict(windowHandle=hwnd, objectID=c_int(objectID).value, childID=childID)
			except COMError:
				hmenu, childID = accPropServices.DecomposeHmenuIdentityString(stringPtr, stringSize)
				# hmenu is a wireHMENU, but it seems we can just treat this as a number.
				# comtypes transparently does this for wireHWND.
				return dict(menuHandle=cast(hmenu, wintypes.HMENU).value, childID=childID)
		stringPtr = cast(stringPtr, POINTER(c_char * stringSize))
		fields = struct.unpack('IIiI', stringPtr.contents.raw)
		d = {}
		d['childID'] = fields[3]
		if fields[0] & 2:
			d['menuHandle'] = fields[2]
		else:
			d['objectID'] = fields[2]
			d['windowHandle'] = fields[1]
		return d
	finally:
		windll.ole32.CoTaskMemFree(stringPtr)


def findGroupboxObject(obj):
	prevWindow = winUser.getPreviousWindow(obj.windowHandle)
	while prevWindow:
		if (
			winUser.getClassName(prevWindow) == "Button"
			and winUser.getWindowStyle(prevWindow) & winUser.BS_GROUPBOX
			and winUser.isWindowVisible(prevWindow)
		):
			groupObj = NVDAObjects.IAccessible.getNVDAObjectFromEvent(prevWindow, winUser.OBJID_CLIENT, 0)
			try:
				(left, top, width, height) = obj.location
				(groupLeft, groupTop, groupWidth, groupHeight) = groupObj.location
			except:  # noqa: E722 Bare except
				return
			if (
				groupObj.IAccessibleRole == oleacc.ROLE_SYSTEM_GROUPING
				and left >= groupLeft
				and (left + width) <= (groupLeft + groupWidth)
				and top >= groupTop
				and (top + height) <= (groupTop + groupHeight)
			):
				return groupObj
		tempWindow = winUser.getPreviousWindow(prevWindow)
		if tempWindow == prevWindow:
			# In rare cases (e.g. HWND 65554 "Message"), getPreviousWindow can return
			# the window passed to it, causing an infinite loop.
			break
		prevWindow = tempWindow


# C901 'getRecursiveTextFromIAccessibleTextObject'
def getRecursiveTextFromIAccessibleTextObject(obj, startOffset=0, endOffset=-1):  # noqa: C901
	if not isinstance(obj, IAccessibleText):
		try:
			textObject = obj.QueryInterface(IAccessibleText)
		except:  # noqa: E722 Bare except
			textObject = None
	else:
		textObject = obj
	if not isinstance(obj, IAccessible):
		try:
			accObject = obj.QueryInterface(IAccessible)
		except:  # noqa: E722 Bare except
			return ""
	else:
		accObject = obj
	try:
		text = textObject.text(startOffset, endOffset)
	except:  # noqa: E722 Bare except
		text = None
	if not text or text.isspace():
		try:
			name = accObject.accName(0)
		except:  # noqa: E722 Bare except
			name = None
		try:
			value = accObject.accValue(0)
		except:  # noqa: E722 Bare except
			value = None
		try:
			description = accObject.accDescription(0)
		except:  # noqa: E722 Bare except
			description = None
		return " ".join([x for x in [name, value, description] if x and not x.isspace()])
	try:
		hypertextObject = accObject.QueryInterface(IAccessibleHypertext)
	except:  # noqa: E722 Bare except
		return text
	textList = []
	for i, t in enumerate(text):
		if ord(t) == 0xFFFC:
			try:
				index = hypertextObject.hyperlinkIndex(i + startOffset)
				childTextObject = hypertextObject.hyperlink(index).QueryInterface(IAccessible)
				t = " %s " % getRecursiveTextFromIAccessibleTextObject(childTextObject)
			except:  # noqa: E722 Bare except
				pass
		textList.append(t)
	return "".join(textList).replace('  ', ' ')


ATTRIBS_STRING_BASE64_PATTERN = re.compile(
	r"(([^\\](\\\\)*);src:data\\:[^\\;]+\\;base64\\,)[A-Za-z0-9+/=]+"
)
ATTRIBS_STRING_BASE64_REPL = r"\1<truncated>"
ATTRIBS_STRING_BASE64_THRESHOLD = 4096


# C901: splitIA2Attribs is too complex
def splitIA2Attribs(attribsString):  # noqa: C901
	"""Split an IAccessible2 attributes string into a dict of attribute keys and values.
	An invalid attributes string does not cause an error, but strange results may be returned.
	Subattributes are handled. Subattribute keys and values are placed into a dict which becomes the value
	of the attribute.
	@param attribsString: The IAccessible2 attributes string to convert.
	@type attribsString: str
	@return: A dict of the attribute keys and values, where values are strings or dicts.
	@rtype: {str: str or {str: str}}
	"""
	# Do not treat huge base64 data as it might freeze NVDA in Google Chrome (#10227)
	if len(attribsString) >= ATTRIBS_STRING_BASE64_THRESHOLD:
		attribsString = ATTRIBS_STRING_BASE64_PATTERN.sub(ATTRIBS_STRING_BASE64_REPL, attribsString)
		if len(attribsString) >= ATTRIBS_STRING_BASE64_THRESHOLD:
			log.debugWarning(f"IA2 attributes string exceeds threshold: {attribsString}")
	attribsDict = {}
	tmp = ""
	key = ""
	subkey = ""
	subattr = {}
	inEscape = False
	for char in attribsString:
		if inEscape:
			tmp += char
			inEscape = False
		elif char == "\\":
			inEscape = True
		elif char == ":":
			# We're about to move on to the value, so save the key and clear tmp.
			key = tmp
			tmp = ""
		elif char == "=":
			# This is a subattribute.
			# Save the subattribute key and clear tmp, ready for the value.
			subkey = tmp
			tmp = ""
		elif char == ",":
			# We're about to move on to a new subattribute.
			# Add this subattribute key/value pair to the dict.
			if subkey:
				subattr[subkey] = tmp
				subkey = ""
				tmp = ""
		elif char == ";":
			# We're about to move on to a new attribute.
			if subkey:
				# Add the last subattribute key/value pair to the dict.
				subattr[subkey] = tmp
				subkey = ""
			if subattr:
				# This attribute had subattributes.
				# Add the key/subattribute pair to the dict.
				attribsDict[key] = subattr
				subattr = {}
			elif key:
				# Add this key/value pair to the dict.
				attribsDict[key] = tmp
			key = ""
			tmp = ""
		else:
			tmp += char
	# If there was no trailing semi-colon, we need to handle the last attribute.
	if subkey:
		# Add the last subattribute key/value pair to the dict.
		subattr[subkey] = tmp
	if subattr:
		# This attribute had subattributes.
		# Add the key/subattribute pair to the dict.
		attribsDict[key] = subattr
	elif key:
		# Add this key/value pair to the dict.
		attribsDict[key] = tmp
	return attribsDict


def isMarshalledIAccessible(IAccessibleObject):
	"""Looks at the location of the first function in the IAccessible object's vtable (IUnknown::AddRef) to
	see if it was implemented in oleacc.dll (its local) or ole32.dll (its marshalled).
	"""
	if not isinstance(IAccessibleObject, IAccessible):
		raise TypeError("object should be of type IAccessible, not %s" % IAccessibleObject)
	buf = create_unicode_buffer(1024)
	addr = POINTER(c_void_p).from_address(
		super(comtypes._compointer_base, IAccessibleObject).value).contents.value
	handle = HANDLE()
	windll.kernel32.GetModuleHandleExW(6, addr, byref(handle))
	windll.kernel32.GetModuleFileNameW(handle, buf, 1024)
	return not buf.value.lower().endswith('oleacc.dll')
