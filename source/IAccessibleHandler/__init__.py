# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2022 NV Access Limited, Łukasz Golonka, Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import typing

# F401 imported but unused. RelationType should be exposed from IAccessibleHandler, in future __all__
# should be used to export it.
from .types import RelationType  # noqa: F401

import re
import struct
from typing import (
	Optional,
	Tuple,
	Dict,
	Union,
	Set,
)
import weakref
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
import JABHandler
import UIAHandler
import textUtils

from comInterfaces import Accessibility as IA

from comInterfaces import IAccessible2Lib as IA2
import api
import appModuleHandler
import controlTypes
import core
import eventHandler
from logHandler import log
import mouseHandler
import NVDAObjects.IAccessible
import NVDAObjects.window
import winUser

from . import internalWinEventHandler
from .orderedWinEventLimiter import MENU_EVENTIDS
from .utils import getWinEventLogInfo, getWinEventName, isMSAADebugLoggingEnabled

if typing.TYPE_CHECKING:
	import textInfos

# Special Mozilla gecko MSAA constant additions
NAVRELATION_LABEL_FOR = 0x1002
NAVRELATION_LABELLED_BY = 0x1003
NAVRELATION_NODE_CHILD_OF = 0x1005
NAVRELATION_EMBEDS = 0x1009

# A place to store live IAccessible NVDAObjects, that can be looked up by their window,objectID,
# childID event params.
liveNVDAObjectTable = weakref.WeakValueDictionary()

IAccessibleRolesToNVDARoles: Dict[Union[int, str], controlTypes.Role] = {
	oleacc.ROLE_SYSTEM_WINDOW: controlTypes.Role.WINDOW,
	oleacc.ROLE_SYSTEM_CLIENT: controlTypes.Role.PANE,
	oleacc.ROLE_SYSTEM_TITLEBAR: controlTypes.Role.TITLEBAR,
	oleacc.ROLE_SYSTEM_DIALOG: controlTypes.Role.DIALOG,
	oleacc.ROLE_SYSTEM_PANE: controlTypes.Role.PANE,
	oleacc.ROLE_SYSTEM_CHECKBUTTON: controlTypes.Role.CHECKBOX,
	oleacc.ROLE_SYSTEM_RADIOBUTTON: controlTypes.Role.RADIOBUTTON,
	oleacc.ROLE_SYSTEM_STATICTEXT: controlTypes.Role.STATICTEXT,
	oleacc.ROLE_SYSTEM_TEXT: controlTypes.Role.EDITABLETEXT,
	oleacc.ROLE_SYSTEM_PUSHBUTTON: controlTypes.Role.BUTTON,
	oleacc.ROLE_SYSTEM_MENUBAR: controlTypes.Role.MENUBAR,
	oleacc.ROLE_SYSTEM_MENUITEM: controlTypes.Role.MENUITEM,
	oleacc.ROLE_SYSTEM_MENUPOPUP: controlTypes.Role.POPUPMENU,
	oleacc.ROLE_SYSTEM_COMBOBOX: controlTypes.Role.COMBOBOX,
	oleacc.ROLE_SYSTEM_LIST: controlTypes.Role.LIST,
	oleacc.ROLE_SYSTEM_LISTITEM: controlTypes.Role.LISTITEM,
	oleacc.ROLE_SYSTEM_GRAPHIC: controlTypes.Role.GRAPHIC,
	oleacc.ROLE_SYSTEM_HELPBALLOON: controlTypes.Role.HELPBALLOON,
	oleacc.ROLE_SYSTEM_TOOLTIP: controlTypes.Role.TOOLTIP,
	oleacc.ROLE_SYSTEM_LINK: controlTypes.Role.LINK,
	oleacc.ROLE_SYSTEM_OUTLINE: controlTypes.Role.TREEVIEW,
	oleacc.ROLE_SYSTEM_OUTLINEITEM: controlTypes.Role.TREEVIEWITEM,
	oleacc.ROLE_SYSTEM_PAGETAB: controlTypes.Role.TAB,
	oleacc.ROLE_SYSTEM_PAGETABLIST: controlTypes.Role.TABCONTROL,
	oleacc.ROLE_SYSTEM_SLIDER: controlTypes.Role.SLIDER,
	oleacc.ROLE_SYSTEM_PROGRESSBAR: controlTypes.Role.PROGRESSBAR,
	oleacc.ROLE_SYSTEM_SCROLLBAR: controlTypes.Role.SCROLLBAR,
	oleacc.ROLE_SYSTEM_STATUSBAR: controlTypes.Role.STATUSBAR,
	oleacc.ROLE_SYSTEM_TABLE: controlTypes.Role.TABLE,
	oleacc.ROLE_SYSTEM_CELL: controlTypes.Role.TABLECELL,
	oleacc.ROLE_SYSTEM_COLUMN: controlTypes.Role.TABLECOLUMN,
	oleacc.ROLE_SYSTEM_ROW: controlTypes.Role.TABLEROW,
	oleacc.ROLE_SYSTEM_TOOLBAR: controlTypes.Role.TOOLBAR,
	oleacc.ROLE_SYSTEM_COLUMNHEADER: controlTypes.Role.TABLECOLUMNHEADER,
	oleacc.ROLE_SYSTEM_ROWHEADER: controlTypes.Role.TABLEROWHEADER,
	oleacc.ROLE_SYSTEM_SPLITBUTTON: controlTypes.Role.SPLITBUTTON,
	oleacc.ROLE_SYSTEM_BUTTONDROPDOWN: controlTypes.Role.DROPDOWNBUTTON,
	oleacc.ROLE_SYSTEM_SEPARATOR: controlTypes.Role.SEPARATOR,
	oleacc.ROLE_SYSTEM_DOCUMENT: controlTypes.Role.DOCUMENT,
	oleacc.ROLE_SYSTEM_ANIMATION: controlTypes.Role.ANIMATION,
	oleacc.ROLE_SYSTEM_APPLICATION: controlTypes.Role.APPLICATION,
	oleacc.ROLE_SYSTEM_GROUPING: controlTypes.Role.GROUPING,
	oleacc.ROLE_SYSTEM_PROPERTYPAGE: controlTypes.Role.PROPERTYPAGE,
	oleacc.ROLE_SYSTEM_ALERT: controlTypes.Role.ALERT,
	oleacc.ROLE_SYSTEM_BORDER: controlTypes.Role.BORDER,
	oleacc.ROLE_SYSTEM_BUTTONDROPDOWNGRID: controlTypes.Role.DROPDOWNBUTTONGRID,
	oleacc.ROLE_SYSTEM_CARET: controlTypes.Role.CARET,
	oleacc.ROLE_SYSTEM_CHARACTER: controlTypes.Role.CHARACTER,
	oleacc.ROLE_SYSTEM_CHART: controlTypes.Role.CHART,
	oleacc.ROLE_SYSTEM_CURSOR: controlTypes.Role.CURSOR,
	oleacc.ROLE_SYSTEM_DIAGRAM: controlTypes.Role.DIAGRAM,
	oleacc.ROLE_SYSTEM_DIAL: controlTypes.Role.DIAL,
	oleacc.ROLE_SYSTEM_DROPLIST: controlTypes.Role.DROPLIST,
	oleacc.ROLE_SYSTEM_BUTTONMENU: controlTypes.Role.MENUBUTTON,
	oleacc.ROLE_SYSTEM_EQUATION: controlTypes.Role.MATH,
	oleacc.ROLE_SYSTEM_GRIP: controlTypes.Role.GRIP,
	oleacc.ROLE_SYSTEM_HOTKEYFIELD: controlTypes.Role.HOTKEYFIELD,
	oleacc.ROLE_SYSTEM_INDICATOR: controlTypes.Role.INDICATOR,
	oleacc.ROLE_SYSTEM_SPINBUTTON: controlTypes.Role.SPINBUTTON,
	oleacc.ROLE_SYSTEM_SOUND: controlTypes.Role.SOUND,
	oleacc.ROLE_SYSTEM_WHITESPACE: controlTypes.Role.WHITESPACE,
	oleacc.ROLE_SYSTEM_IPADDRESS: controlTypes.Role.IPADDRESS,
	oleacc.ROLE_SYSTEM_OUTLINEBUTTON: controlTypes.Role.TREEVIEWBUTTON,
	oleacc.ROLE_SYSTEM_CLOCK: controlTypes.Role.CLOCK,
	# IAccessible2 roles
	IA2.IA2_ROLE_UNKNOWN: controlTypes.Role.UNKNOWN,
	IA2.IA2_ROLE_CANVAS: controlTypes.Role.CANVAS,
	IA2.IA2_ROLE_CAPTION: controlTypes.Role.CAPTION,
	IA2.IA2_ROLE_CHECK_MENU_ITEM: controlTypes.Role.CHECKMENUITEM,
	IA2.IA2_ROLE_COLOR_CHOOSER: controlTypes.Role.COLORCHOOSER,
	IA2.IA2_ROLE_DATE_EDITOR: controlTypes.Role.DATEEDITOR,
	IA2.IA2_ROLE_DESKTOP_ICON: controlTypes.Role.DESKTOPICON,
	IA2.IA2_ROLE_DESKTOP_PANE: controlTypes.Role.DESKTOPPANE,
	IA2.IA2_ROLE_DIRECTORY_PANE: controlTypes.Role.DIRECTORYPANE,
	IA2.IA2_ROLE_EDITBAR: controlTypes.Role.EDITBAR,
	IA2.IA2_ROLE_EMBEDDED_OBJECT: controlTypes.Role.EMBEDDEDOBJECT,
	IA2.IA2_ROLE_ENDNOTE: controlTypes.Role.ENDNOTE,
	IA2.IA2_ROLE_FILE_CHOOSER: controlTypes.Role.FILECHOOSER,
	IA2.IA2_ROLE_FONT_CHOOSER: controlTypes.Role.FONTCHOOSER,
	IA2.IA2_ROLE_FOOTER: controlTypes.Role.FOOTER,
	IA2.IA2_ROLE_FOOTNOTE: controlTypes.Role.FOOTNOTE,
	IA2.IA2_ROLE_FORM: controlTypes.Role.FORM,
	IA2.IA2_ROLE_FRAME: controlTypes.Role.FRAME,
	IA2.IA2_ROLE_GLASS_PANE: controlTypes.Role.GLASSPANE,
	IA2.IA2_ROLE_HEADER: controlTypes.Role.HEADER,
	IA2.IA2_ROLE_HEADING: controlTypes.Role.HEADING,
	IA2.IA2_ROLE_ICON: controlTypes.Role.ICON,
	IA2.IA2_ROLE_IMAGE_MAP: controlTypes.Role.IMAGEMAP,
	IA2.IA2_ROLE_INPUT_METHOD_WINDOW: controlTypes.Role.INPUTWINDOW,
	IA2.IA2_ROLE_INTERNAL_FRAME: controlTypes.Role.INTERNALFRAME,
	IA2.IA2_ROLE_LABEL: controlTypes.Role.LABEL,
	IA2.IA2_ROLE_LAYERED_PANE: controlTypes.Role.LAYEREDPANE,
	IA2.IA2_ROLE_NOTE: controlTypes.Role.NOTE,
	IA2.IA2_ROLE_OPTION_PANE: controlTypes.Role.OPTIONPANE,
	IA2.IA2_ROLE_PAGE: controlTypes.Role.PAGE,
	IA2.IA2_ROLE_PARAGRAPH: controlTypes.Role.PARAGRAPH,
	IA2.IA2_ROLE_RADIO_MENU_ITEM: controlTypes.Role.RADIOMENUITEM,
	IA2.IA2_ROLE_REDUNDANT_OBJECT: controlTypes.Role.REDUNDANTOBJECT,
	IA2.IA2_ROLE_ROOT_PANE: controlTypes.Role.ROOTPANE,
	IA2.IA2_ROLE_RULER: controlTypes.Role.RULER,
	IA2.IA2_ROLE_SCROLL_PANE: controlTypes.Role.SCROLLPANE,
	IA2.IA2_ROLE_SECTION: controlTypes.Role.SECTION,
	IA2.IA2_ROLE_SHAPE: controlTypes.Role.SHAPE,
	IA2.IA2_ROLE_SPLIT_PANE: controlTypes.Role.SPLITPANE,
	IA2.IA2_ROLE_TEAR_OFF_MENU: controlTypes.Role.TEAROFFMENU,
	IA2.IA2_ROLE_TERMINAL: controlTypes.Role.TERMINAL,
	IA2.IA2_ROLE_TEXT_FRAME: controlTypes.Role.TEXTFRAME,
	IA2.IA2_ROLE_TOGGLE_BUTTON: controlTypes.Role.TOGGLEBUTTON,
	IA2.IA2_ROLE_VIEW_PORT: controlTypes.Role.VIEWPORT,
	IA2.IA2_ROLE_CONTENT_DELETION: controlTypes.Role.DELETED_CONTENT,
	IA2.IA2_ROLE_CONTENT_INSERTION: controlTypes.Role.INSERTED_CONTENT,
	IA2.IA2_ROLE_BLOCK_QUOTE: controlTypes.Role.BLOCKQUOTE,
	IA2.IA2_ROLE_LANDMARK: controlTypes.Role.LANDMARK,
	IA2.IA2_ROLE_MARK: controlTypes.Role.MARKED_CONTENT,
	IA2.IA2_ROLE_COMMENT: controlTypes.Role.COMMENT,
	IA2.IA2_ROLE_SUGGESTION: controlTypes.Role.SUGGESTION,
	# some common string roles
	"frame": controlTypes.Role.FRAME,
	"iframe": controlTypes.Role.INTERNALFRAME,
	"page": controlTypes.Role.PAGE,
	"form": controlTypes.Role.FORM,
	"div": controlTypes.Role.SECTION,
	"li": controlTypes.Role.LISTITEM,
	"ul": controlTypes.Role.LIST,
	"tbody": controlTypes.Role.TABLEBODY,
	"browser": controlTypes.Role.WINDOW,
	"h1": controlTypes.Role.HEADING1,
	"h2": controlTypes.Role.HEADING2,
	"h3": controlTypes.Role.HEADING3,
	"h4": controlTypes.Role.HEADING4,
	"h5": controlTypes.Role.HEADING5,
	"h6": controlTypes.Role.HEADING6,
	"p": controlTypes.Role.PARAGRAPH,
	"hbox": controlTypes.Role.BOX,
	"embed": controlTypes.Role.EMBEDDEDOBJECT,
	"object": controlTypes.Role.EMBEDDEDOBJECT,
	"applet": controlTypes.Role.EMBEDDEDOBJECT,
}

IAccessibleStatesToNVDAStates = {
	oleacc.STATE_SYSTEM_TRAVERSED: controlTypes.State.VISITED,
	oleacc.STATE_SYSTEM_UNAVAILABLE: controlTypes.State.UNAVAILABLE,
	oleacc.STATE_SYSTEM_FOCUSED: controlTypes.State.FOCUSED,
	oleacc.STATE_SYSTEM_SELECTED: controlTypes.State.SELECTED,
	oleacc.STATE_SYSTEM_BUSY: controlTypes.State.BUSY,
	oleacc.STATE_SYSTEM_PRESSED: controlTypes.State.PRESSED,
	oleacc.STATE_SYSTEM_CHECKED: controlTypes.State.CHECKED,
	oleacc.STATE_SYSTEM_MIXED: controlTypes.State.HALFCHECKED,
	oleacc.STATE_SYSTEM_READONLY: controlTypes.State.READONLY,
	oleacc.STATE_SYSTEM_EXPANDED: controlTypes.State.EXPANDED,
	oleacc.STATE_SYSTEM_COLLAPSED: controlTypes.State.COLLAPSED,
	oleacc.STATE_SYSTEM_OFFSCREEN: controlTypes.State.OFFSCREEN,
	oleacc.STATE_SYSTEM_INVISIBLE: controlTypes.State.INVISIBLE,
	oleacc.STATE_SYSTEM_LINKED: controlTypes.State.LINKED,
	oleacc.STATE_SYSTEM_HASPOPUP: controlTypes.State.HASPOPUP,
	oleacc.STATE_SYSTEM_PROTECTED: controlTypes.State.PROTECTED,
	oleacc.STATE_SYSTEM_SELECTABLE: controlTypes.State.SELECTABLE,
	oleacc.STATE_SYSTEM_FOCUSABLE: controlTypes.State.FOCUSABLE,
}

IAccessible2StatesToNVDAStates = {
	IA2.IA2_STATE_REQUIRED: controlTypes.State.REQUIRED,
	IA2.IA2_STATE_DEFUNCT: controlTypes.State.DEFUNCT,
	# IA2.IA2_STATE_STALE:controlTypes.State.DEFUNCT,
	IA2.IA2_STATE_INVALID_ENTRY: controlTypes.State.INVALID_ENTRY,
	IA2.IA2_STATE_MODAL: controlTypes.State.MODAL,
	IA2.IA2_STATE_SUPPORTS_AUTOCOMPLETION: controlTypes.State.AUTOCOMPLETE,
	IA2.IA2_STATE_MULTI_LINE: controlTypes.State.MULTILINE,
	IA2.IA2_STATE_ICONIFIED: controlTypes.State.ICONIFIED,
	IA2.IA2_STATE_EDITABLE: controlTypes.State.EDITABLE,
	IA2.IA2_STATE_PINNED: controlTypes.State.PINNED,
	IA2.IA2_STATE_CHECKABLE: controlTypes.State.CHECKABLE,
}

Role = controlTypes.Role
State = controlTypes.State


def _getStatesSetFromIAccessibleStates(
	IAccessibleStates: int,
) -> Set[controlTypes.State]:
	return set(
		IAccessibleStatesToNVDAStates[IAState]
		for IAState in IAccessibleStatesToNVDAStates.keys()
		if IAState & IAccessibleStates
	)


def getStatesSetFromIAccessible2States(IAccessible2States: int) -> Set[State]:
	return set(
		IAccessible2StatesToNVDAStates[IA2State]
		for IA2State in IAccessible2StatesToNVDAStates.keys()
		if IA2State & IAccessible2States
	)


def getStatesSetFromIAccessibleAttrs(attrs: "textInfos.ControlField") -> Set[State]:
	# States are serialized (in XML) with an attribute per state.
	# The value for the state is used in the attribute name.
	# The attribute value is always 1.
	# EG IAccessible::state_40="1"
	IAccessibleStateAttrName = "IAccessible::state_{}"
	return set(
		IAccessibleStatesToNVDAStates[IAState]
		for IAState in IAccessibleStatesToNVDAStates.keys()
		if int(attrs.get(IAccessibleStateAttrName.format(IAState), 0))
	)


def getStatesSetFromIAccessible2Attrs(attrs: "textInfos.ControlField") -> Set[State]:
	# States are serialized (in XML) with an attribute per state.
	# The value for the state is used in the attribute name.
	# The attribute value is always 1.
	# EG IAccessible2::state_40="1"
	IAccessible2StateAttrName = "IAccessible2::state_{}"
	return set(
		IAccessible2StatesToNVDAStates[IA2State]
		for IA2State in IAccessible2StatesToNVDAStates.keys()
		if int(attrs.get(IAccessible2StateAttrName.format(IA2State), 0))
	)


def calculateNvdaRole(IARole: int, IAStates: int) -> Role:
	"""Convert IARole value into an NVDA role, and apply any required transformations."""
	role = IAccessibleRolesToNVDARoles.get(IARole, Role.UNKNOWN)
	states = _getStatesSetFromIAccessibleStates(IAStates)
	role, states = controlTypes.transformRoleStates(role, states)
	return role


def calculateNvdaStates(IARole: int, IAStates: int) -> Set[State]:
	"""Convert IAStates bit set into a Set of NVDA States and apply any required transformations."""
	role = IAccessibleRolesToNVDARoles.get(IARole, Role.UNKNOWN)
	states = _getStatesSetFromIAccessibleStates(IAStates)
	role, states = controlTypes.transformRoleStates(role, states)
	return states


def NVDARoleFromAttr(accRole: Optional[str]) -> Role:
	if not accRole:  # empty string or None
		return controlTypes.Role.UNKNOWN
	assert isinstance(accRole, str)
	if accRole.isdigit():
		accRole = int(accRole)
	else:
		accRole = accRole.lower()
	return IAccessibleRolesToNVDARoles.get(accRole, controlTypes.Role.UNKNOWN)


def normalizeIAccessible(
	pacc: Union[IUnknown, IA.IAccessible, IA2.IAccessible2],
	childID: int = 0,
) -> Union[IA.IAccessible, IA2.IAccessible2]:
	if not isinstance(pacc, IA.IAccessible):
		try:
			pacc = pacc.QueryInterface(IA.IAccessible)
		except COMError:
			raise RuntimeError("%s Not an IAccessible" % pacc)
	# #2558: IAccessible2 doesn't support simple children.
	# Therefore, it doesn't make sense to use IA2 if the child ID is non-0.
	if childID == 0 and not isinstance(pacc, IA2.IAccessible2):
		try:
			s = pacc.QueryInterface(IServiceProvider)
			pacc2 = s.QueryService(IA.IAccessible._iid_, IA2.IAccessible2)
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
				f" WinEvent: {getWinEventLogInfo(window, objectID, childID)}",
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


# C901 'winEventToNVDAEvent' is too complex
# Note: when working on winEventToNVDAEvent, look for opportunities to simplify
# and move logic out into smaller helper functions.
def winEventToNVDAEvent(  # noqa: C901
	eventID: int,
	window: int,
	objectID: int,
	childID: int,
	useCache: bool = True,
) -> Optional[Tuple[str, NVDAObjects.IAccessible.IAccessible]]:
	"""Tries to convert a win event ID to an NVDA event name, and instantiate or fetch an NVDAObject for
	 the win event parameters.
	@param eventID: the win event ID (type)
	@param window: the win event's window handle
	@param objectID: the win event's object ID
	@param childID: the win event's childID
	@param useCache: C{True} to use the L{liveNVDAObjectTable} cache when
	 retrieving an NVDAObject, C{False} if the cache should not be used.
	@returns: the NVDA event name and the NVDAObject the event is for
	"""
	if isMSAADebugLoggingEnabled():
		log.debug(
			f"Creating NVDA event from winEvent: {getWinEventLogInfo(window, objectID, childID, eventID)}, "
			f"use cache {useCache}",
		)
	NVDAEventName = internalWinEventHandler.winEventIDsToNVDAEventNames.get(eventID, None)
	if not NVDAEventName:
		log.debugWarning(f"No NVDA event name for {getWinEventName(eventID)}")
		return None
	if isMSAADebugLoggingEnabled():
		log.debug(f"winEvent mapped to NVDA event: {NVDAEventName}")
	# Ignore any events with invalid window handles
	if not window or not winUser.isWindow(window):
		if isMSAADebugLoggingEnabled():
			log.debug(
				f"Invalid window. Dropping winEvent {getWinEventLogInfo(window, objectID, childID, eventID)}",
			)
		return None
	# Make sure this window does not have a ghost window if possible
	if NVDAObjects.window.GhostWindowFromHungWindow and NVDAObjects.window.GhostWindowFromHungWindow(window):
		if isMSAADebugLoggingEnabled():
			log.debug(
				f"Ghosted hung window. Dropping winEvent {getWinEventLogInfo(window, objectID, childID, eventID)}",
			)
		return None
	# We do not support MSAA object proxied from native UIA
	if UIAHandler.handler and UIAHandler.handler.isUIAWindow(window, isDebug=isMSAADebugLoggingEnabled()):
		if isMSAADebugLoggingEnabled():
			log.debug(
				f"Native UIA window. Dropping winEvent {getWinEventLogInfo(window, objectID, childID, eventID)}",
			)
		return None
	obj = None
	if useCache:
		# See if we already know an object by this win event info
		obj = liveNVDAObjectTable.get((window, objectID, childID), None)
		if isMSAADebugLoggingEnabled() and obj:
			log.debug(
				f"Fetched existing NVDAObject {obj} from liveNVDAObjectTable"
				f" for winEvent {getWinEventLogInfo(window, objectID, childID)}",
			)
	# If we don't yet have the object, then actually instanciate it.
	if not obj:
		obj = NVDAObjects.IAccessible.getNVDAObjectFromEvent(window, objectID, childID)
	# At this point if we don't have an object then we can't do any more
	if not obj:
		if isMSAADebugLoggingEnabled():
			log.debug(
				"Could not instantiate an NVDAObject for winEvent: "
				f"{getWinEventLogInfo(window, objectID, childID, eventID)}",
			)
		return None
	# SDM MSAA objects sometimes don't contain enough information to be useful Sometimes there is a real
	# window that does, so try to get the SDMChild property on the NVDAObject, and if successull use that as
	# obj instead.
	if "bosa_sdm" in obj.windowClassName:
		SDMChild = getattr(obj, "SDMChild", None)
		if SDMChild:
			obj = SDMChild
	if isMSAADebugLoggingEnabled():
		log.debug(
			f"Successfully created NVDA event {NVDAEventName} for {obj} "
			f"from winEvent {getWinEventLogInfo(window, objectID, childID, eventID)}",
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
			f"Processing generic winEvent: {getWinEventLogInfo(window, objectID, childID, eventID)}",
		)
	# Notify appModuleHandler of this new window
	appModuleHandler.update(winUser.getWindowThreadProcessID(window)[0])
	# Handle particular events for the special MSAA caret object just as if they were for the focus object
	focus = eventHandler.lastQueuedFocusObject
	if objectID == winUser.OBJID_CARET and eventID in (
		winUser.EVENT_OBJECT_LOCATIONCHANGE,
		winUser.EVENT_OBJECT_SHOW,
	):
		if not isinstance(focus, NVDAObjects.IAccessible.IAccessible):
			# #12855: Ignore MSAA caret event on non-MSAA focus.
			# as Chinese input method fires MSAA caret events over and over on UIA Word documents.
			# #13098: However, limit this specifically to UIA Word documents,
			# As other UIA documents (E.g. Visual Studio)
			# Seem to rely on MSAA caret events,
			# as they do not fire their own UIA caret events.
			from NVDAObjects.UIA.wordDocument import WordDocument

			if isinstance(focus, WordDocument):
				if isMSAADebugLoggingEnabled():
					log.debug(
						f"Ignoring MSAA caret event on focused UIA Word document"
						f"winEvent {getWinEventLogInfo(window, objectID, childID)}",
					)
				return False
		elif isinstance(focus.IAccessibleObject, IA2.IAccessible2):
			if isMSAADebugLoggingEnabled():
				log.debug(
					"Ignoring MSAA caret event on focused IAccessible2 object"
					f"winEvent {getWinEventLogInfo(window, objectID, childID)}",
				)
			return False
		if isMSAADebugLoggingEnabled():
			log.debug(
				"handling winEvent as caret event on focus. "
				f"winEvent {getWinEventLogInfo(window, objectID, childID)}",
			)
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
	# if the winEvent is for the object with focus,
	# Ensure that that the event is send to the existing focus instance,
	# rather than a new instance of the object with focus.
	if NVDAEvent[1] is not focus and NVDAEvent[1] == focus:
		if isMSAADebugLoggingEnabled():
			log.debug(
				f"Directing winEvent to existing focus object {focus}. "
				f"WinEvent {getWinEventLogInfo(window, objectID, childID)}",
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
			f"Processing focus winEvent: {getWinEventLogInfo(window, objectID, childID)}, force {force}",
		)
	windowClassName = winUser.getClassName(window)
	# Generally, we must ignore focus on child windows of SDM windows as we only want the SDM MSAA events.
	# However, we don't want to ignore focus if the child ID isn't 0,
	# as this is a child control and the SDM MSAA events don't handle child controls.
	if (
		childID == 0
		and not windowClassName.startswith("bosa_sdm")
		and winUser.getClassName(winUser.getAncestor(window, winUser.GA_PARENT)).startswith("bosa_sdm")
	):
		if isMSAADebugLoggingEnabled():
			log.debug(
				f"Focus event for child window of MS Office SDM window. "
				f"Dropping winEvent {getWinEventLogInfo(window, objectID, childID)}, ",
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
				f"Redirecting focus to Java window. WinEvent {getWinEventLogInfo(window, objectID, childID)}",
			)
		JABHandler.event_enterJavaWindow(window)
		return True
	# Convert the win event to an NVDA event
	NVDAEvent = winEventToNVDAEvent(winUser.EVENT_OBJECT_FOCUS, window, objectID, childID, useCache=False)
	if not NVDAEvent:
		return False
	eventName, obj = NVDAEvent
	if (childID == 0 and obj.IAccessibleRole == oleacc.ROLE_SYSTEM_LIST) or (
		objectID == winUser.OBJID_CLIENT and "SysListView32" in obj.windowClassName
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
				event_childID=realChildID,
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
	eventHandler.queueEvent("gainFocus", obj)
	return True


def processDesktopSwitchWinEvent(window, objectID, childID):
	from winAPI.secureDesktop import _handleSecureDesktopChange

	if isMSAADebugLoggingEnabled():
		log.debug(
			f"Processing desktopSwitch winEvent: {getWinEventLogInfo(window, objectID, childID)}",
		)
	hDesk = windll.user32.OpenInputDesktop(0, False, 0)
	if hDesk != 0:
		windll.user32.CloseDesktop(hDesk)
		core.callLater(200, _handleUserDesktop)
	else:
		# When hDesk == 0, the active desktop has changed.
		# This is usually means the secure desktop has been launched,
		# but the new desktop can also be a secondary desktop created through the Windows API.
		# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-createdesktopa
		# This secondary desktop has some bugs, and as such is not properly supported (#14395).
		# It is not immediately clear how to differentiate changing to a secondary desktop and the secure desktop.
		# When looking to support the secondary desktop,
		# the UX should be updated to announce "desktop change" rather than "Secure Desktop".
		_handleSecureDesktopChange()


def _handleUserDesktop():
	from winAPI.secureDesktop import post_secureDesktopStateChange

	eventHandler.queueEvent("gainFocus", api.getDesktopObject().objectWithFocus())
	post_secureDesktopStateChange.notify(isSecureDesktop=False)


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
			f"Processing foreground winEvent: {getWinEventLogInfo(window, objectID, childID)}",
		)
	# Ignore foreground events on windows that aren't the current foreground window
	if window != winUser.getForegroundWindow():
		if isMSAADebugLoggingEnabled():
			log.debug(
				f"Dropping foreground winEvent as it does not match GetForegroundWindow. "
				f"WinEvent {getWinEventLogInfo(window, objectID, childID)}",
			)
		return False
	# If there is a pending gainFocus, it will handle the foreground object.
	oldFocus = eventHandler.lastQueuedFocusObject
	# If this foreground win event's window is an ancestor of the existing focus's window, then ignore it
	if isinstance(oldFocus, NVDAObjects.window.Window) and winUser.isDescendantWindow(
		window,
		oldFocus.windowHandle,
	):
		if isMSAADebugLoggingEnabled():
			log.debug(
				f"Dropping foreground winEvent as focus is already on a descendant. "
				f"WinEvent {getWinEventLogInfo(window, objectID, childID)}",
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
				f"WinEvent {getWinEventLogInfo(window, objectID, childID)}",
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
				f"WinEvent {getWinEventLogInfo(window, objectID, childID)}",
			)
		return True
	# Convert the win event to an NVDA event
	NVDAEvent = winEventToNVDAEvent(
		winUser.EVENT_SYSTEM_FOREGROUND,
		window,
		objectID,
		childID,
		useCache=False,
	)
	if not NVDAEvent:
		if isMSAADebugLoggingEnabled():
			log.debug(
				f"Could not convert foreground winEvent to an NVDA event. "
				f"WinEvent {getWinEventLogInfo(window, objectID, childID)}",
			)
		return False
	eventHandler.queueEvent(*NVDAEvent)
	return True


def processShowWinEvent(window, objectID, childID):
	if isMSAADebugLoggingEnabled():
		log.debug(
			f"Processing show winEvent: {getWinEventLogInfo(window, objectID, childID)}",
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
			f"Processing destroy winEvent: {getWinEventLogInfo(window, objectID, childID)}",
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
			f"validFocus {validFocus}",
		)
	if validFocus:
		lastFocus = eventHandler.lastQueuedFocusObject
		if isinstance(lastFocus, NVDAObjects.IAccessible.IAccessible) and lastFocus.IAccessibleRole in (
			oleacc.ROLE_SYSTEM_MENUPOPUP,
			oleacc.ROLE_SYSTEM_MENUITEM,
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
	elif not obj.shouldAllowIAccessibleMenuStartEvent:
		if isMSAADebugLoggingEnabled():
			log.debug(
				f"Ignoring menuStart winEvent: {getWinEventLogInfo(window, objectID, childID)}, "
				f"shouldAllowIAccessibleMenuStartEvent {obj.shouldAllowIAccessibleMenuStartEvent}",
			)
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
			f"Processing fake focus winEvent {getWinEventLogInfo(window, objectID, childID)}",
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
			f"Faking focus on {focus}",
		)
	processFocusNVDAEvent(focus)


#: Only valid after initialisation.
accPropServices = None


def initialize():
	global accPropServices
	try:
		accPropServices = comtypes.client.CreateObject(IA.CAccPropServices)
	except (WindowsError, COMError) as e:
		log.debugWarning("AccPropServices is not available: %s" % e)
	internalWinEventHandler.initialize(processDestroyWinEvent)


# C901 'pumpAll' is too complex
def pumpAll():  # noqa: C901
	if not internalWinEventHandler._shouldGetEvents():
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
	winEvents = internalWinEventHandler.winEventLimiter.flushEvents(alwaysAllowedObjects)

	for winEvent in winEvents:
		isEventOnCaret = winEvent[2] == winUser.OBJID_CARET
		showHideCaretEvent = (
			focus
			and isEventOnCaret
			and winEvent[0]
			in [
				winUser.EVENT_OBJECT_SHOW,
				winUser.EVENT_OBJECT_HIDE,
			]
		)
		# #4001: Ideally, we'd call shouldAcceptEvent in winEventCallback, but this causes focus issues when
		# starting applications. #7332: If this is a show event, which would normally be dropped by
		# `shouldAcceptEvent` and this event is for the caret, later it will be mapped to a caret event,
		# so skip `shouldAcceptEvent`
		if showHideCaretEvent:
			if not focus.shouldAcceptShowHideCaretEvent:
				continue
		elif not eventHandler.shouldAcceptEvent(
			internalWinEventHandler.winEventIDsToNVDAEventNames[winEvent[0]],
			windowHandle=winEvent[1],
		):
			continue
		# We want to only pass on one focus event to NVDA, but we always want to use the most recent possible one
		if winEvent[0] in (
			winUser.EVENT_OBJECT_FOCUS,
			winUser.EVENT_SYSTEM_FOREGROUND,
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
			winUser.EVENT_SYSTEM_MENUPOPUPSTART,
		):
			# menuStart needs to be handled specially and might act even if there was a valid focus event.
			processMenuStartWinEvent(*fakeFocusEvent, validFocus=validFocus)
		elif not validFocus:
			# Other fake focus events only need to be handled if there was no valid focus event.
			processFakeFocusWinEvent(*fakeFocusEvent)


def terminate():
	internalWinEventHandler.terminate()


def getIAccIdentity(pacc, childID):
	IAccIdentityObject = pacc.QueryInterface(IA.IAccIdentity)
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
		fields = struct.unpack("IIiI", stringPtr.contents.raw)
		d = {}
		d["childID"] = fields[3]
		if fields[0] & 2:
			d["menuHandle"] = fields[2]
		else:
			d["objectID"] = fields[2]
			d["windowHandle"] = fields[1]
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
	if not isinstance(obj, IA2.IAccessibleText):
		try:
			textObject = obj.QueryInterface(IA2.IAccessibleText)
		except:  # noqa: E722 Bare except
			textObject = None
	else:
		textObject = obj
	if not isinstance(obj, IA.IAccessible):
		try:
			accObject = obj.QueryInterface(IA.IAccessible)
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
		hypertextObject = accObject.QueryInterface(IA2.IAccessibleHypertext)
	except:  # noqa: E722 Bare except
		return text
	textList = []
	for i, t in enumerate(text):
		if ord(t) == ord(textUtils.OBJ_REPLACEMENT_CHAR):
			try:
				index = hypertextObject.hyperlinkIndex(i + startOffset)
				childTextObject = hypertextObject.hyperlink(index).QueryInterface(IA.IAccessible)
				t = " %s " % getRecursiveTextFromIAccessibleTextObject(childTextObject)
			except:  # noqa: E722 Bare except
				pass
		textList.append(t)
	return "".join(textList).replace("  ", " ")


ATTRIBS_STRING_BASE64_PATTERN = re.compile(
	r"(([^\\](\\\\)*);src:data\\:[^\\;]+\\;base64\\,)[A-Za-z0-9+/=]+",
)
ATTRIBS_STRING_BASE64_REPL = r"\1<truncated>"
ATTRIBS_STRING_BASE64_THRESHOLD = 4096


# C901: splitIA2Attribs is too complex
def splitIA2Attribs(  # noqa: C901
	attribsString: str,
) -> Dict[str, Union[str, Dict]]:
	"""Split an IAccessible2 attributes string into a dict of attribute keys and values.
	An invalid attributes string does not cause an error, but strange results may be returned.
	Subattributes are handled. Subattribute keys and values are placed into a dict which becomes the value
	of the attribute.
	@param attribsString: The IAccessible2 attributes string to convert.
	@return: A dict of the attribute keys and values, where values are strings or dicts.
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
	if not isinstance(IAccessibleObject, IA.IAccessible):
		raise TypeError("object should be of type IAccessible, not %s" % IAccessibleObject)
	buf = create_unicode_buffer(1024)
	addr = (
		POINTER(c_void_p)
		.from_address(
			super(comtypes._compointer_base, IAccessibleObject).value,
		)
		.contents.value
	)
	handle = HANDLE()
	windll.kernel32.GetModuleHandleExW(6, addr, byref(handle))
	windll.kernel32.GetModuleFileNameW(handle, buf, 1024)
	return not buf.value.lower().endswith("oleacc.dll")
