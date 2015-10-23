#IAccessibleHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import heapq
import itertools
import struct
import weakref
from ctypes import *
from ctypes.wintypes import HANDLE
from comtypes import IUnknown, IServiceProvider, COMError
import comtypes.client
import comtypes.client.lazybind
import oleacc
import UIAHandler
from comInterfaces.Accessibility import *
from comInterfaces.IAccessible2Lib import *
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

MAX_WINEVENTS=500
MAX_WINEVENTS_PER_THREAD=10

#Special Mozilla gecko MSAA constant additions
NAVRELATION_LABEL_FOR=0x1002
NAVRELATION_LABELLED_BY=0x1003
NAVRELATION_NODE_CHILD_OF=0x1005
NAVRELATION_EMBEDS=0x1009

# IAccessible2 relations (not included in the typelib)
IA2_RELATION_FLOWS_FROM = "flowsFrom"
IA2_RELATION_FLOWS_TO = "flowsTo"

MENU_EVENTIDS=(winUser.EVENT_SYSTEM_MENUSTART,winUser.EVENT_SYSTEM_MENUEND,winUser.EVENT_SYSTEM_MENUPOPUPSTART,winUser.EVENT_SYSTEM_MENUPOPUPEND)

class OrderedWinEventLimiter(object):
	"""Collects and limits winEvents based on whether they are focus changes, or just generic (all other ones).

	Only allow a max of L{maxFocusItems}, if more are added then the oldest focus event is removed to make room.
	Only allow one event for one specific object at a time, though push it further forward in time if a duplicate tries to get added. This is true for both generic and focus events.
 	"""

	def __init__(self,maxFocusItems=3):
		"""
		@param maxFocusItems: the amount of focus changed events allowed to be queued.
		@type maxFocusItems: integer
		"""
		self.maxFocusItems=maxFocusItems
		self._focusEventCache={}
		self._genericEventCache={}
		self._eventHeap=[]
		self._eventCounter=itertools.count()
		self._lastMenuEvent=None

	def addEvent(self,eventID,window,objectID,childID,threadID):
		"""Adds a winEvent to the limiter.
		@param eventID: the winEvent type
		@type eventID: integer
		@param window: the window handle of the winEvent
		@type window: integer
		@param objectID: the objectID of the winEvent
		@type objectID: integer
		@param childID: the childID of the winEvent
		@type childID: integer
		@param threadID: the threadID of the winEvent
		@type threadID: integer
		@return: C{True} if the event was added, C{False} if it was discarded.
		@rtype: bool
		"""
		if eventID==winUser.EVENT_OBJECT_FOCUS:
			if objectID in (winUser.OBJID_SYSMENU,winUser.OBJID_MENU) and childID==0:
				# This is a focus event on a menu bar itself, which is just silly. Ignore it.
				return False
			#We do not need a focus event on an object if we already got a foreground event for it
			if (winUser.EVENT_SYSTEM_FOREGROUND,window,objectID,childID,threadID) in self._focusEventCache:
				return False
			self._focusEventCache[(eventID,window,objectID,childID,threadID)]=next(self._eventCounter)
			return True
		elif eventID==winUser.EVENT_SYSTEM_FOREGROUND:
			self._focusEventCache.pop((winUser.EVENT_OBJECT_FOCUS,window,objectID,childID,threadID),None)
			self._focusEventCache[(eventID,window,objectID,childID,threadID)]=next(self._eventCounter)
		elif eventID==winUser.EVENT_OBJECT_SHOW:
			k=(winUser.EVENT_OBJECT_HIDE,window,objectID,childID,threadID)
			if k in self._genericEventCache:
				del self._genericEventCache[k]
				return True
		elif eventID==winUser.EVENT_OBJECT_HIDE:
			k=(winUser.EVENT_OBJECT_SHOW,window,objectID,childID,threadID)
			if k in self._genericEventCache:
				del self._genericEventCache[k]
				return True
		elif eventID in MENU_EVENTIDS:
			self._lastMenuEvent=(next(self._eventCounter),eventID,window,objectID,childID,threadID)
			return True
		self._genericEventCache[(eventID,window,objectID,childID,threadID)]=next(self._eventCounter)
		return True

	def flushEvents(self):
		"""Returns a list of winEvents (tuples of eventID,window,objectID,childID) that have been added, though due to limiting, it will not necessarily be all the winEvents that were originally added. They are definitely garenteed to be in the correct order though.
		"""
		if self._lastMenuEvent is not None:
			heapq.heappush(self._eventHeap,self._lastMenuEvent)
			self._lastMenuEvent=None
		g=self._genericEventCache
		self._genericEventCache={}
		threadCounters={}
		for k,v in sorted(g.iteritems(),key=lambda item: item[1],reverse=True):
			threadCount=threadCounters.get(k[-1],0)
			if threadCount>MAX_WINEVENTS_PER_THREAD:
				continue
			heapq.heappush(self._eventHeap,(v,)+k)
			threadCounters[k[-1]]=threadCount+1
		f=self._focusEventCache
		self._focusEventCache={}
		for k,v in sorted(f.iteritems(),key=lambda item: item[1])[0-self.maxFocusItems:]:
			heapq.heappush(self._eventHeap,(v,)+k)
		e=self._eventHeap
		self._eventHeap=[]
		r=[]
		for count in xrange(len(e)):
			event=heapq.heappop(e)[1:-1]
			r.append(event)
		return r

#The win event limiter for all winEvents
winEventLimiter=OrderedWinEventLimiter()

#A place to store live IAccessible NVDAObjects, that can be looked up by their window,objectID,childID event params.
liveNVDAObjectTable=weakref.WeakValueDictionary()

# #3831: Stuff related to deferring of events for foreground changes.
# See pumpAll for details.
MAX_FOREGROUND_DEFERS=2
_deferUntilForegroundWindow = None
_foregroundDefers = 0

IAccessibleRolesToNVDARoles={
	oleacc.ROLE_SYSTEM_WINDOW:controlTypes.ROLE_WINDOW,
	oleacc.ROLE_SYSTEM_CLIENT:controlTypes.ROLE_PANE,
	oleacc.ROLE_SYSTEM_TITLEBAR:controlTypes.ROLE_TITLEBAR,
	oleacc.ROLE_SYSTEM_DIALOG:controlTypes.ROLE_DIALOG,
	oleacc.ROLE_SYSTEM_PANE:controlTypes.ROLE_PANE,
	oleacc.ROLE_SYSTEM_CHECKBUTTON:controlTypes.ROLE_CHECKBOX,
	oleacc.ROLE_SYSTEM_RADIOBUTTON:controlTypes.ROLE_RADIOBUTTON,
	oleacc.ROLE_SYSTEM_STATICTEXT:controlTypes.ROLE_STATICTEXT,
	oleacc.ROLE_SYSTEM_TEXT:controlTypes.ROLE_EDITABLETEXT,
	oleacc.ROLE_SYSTEM_PUSHBUTTON:controlTypes.ROLE_BUTTON,
	oleacc.ROLE_SYSTEM_MENUBAR:controlTypes.ROLE_MENUBAR,
	oleacc.ROLE_SYSTEM_MENUITEM:controlTypes.ROLE_MENUITEM,
	oleacc.ROLE_SYSTEM_MENUPOPUP:controlTypes.ROLE_POPUPMENU,
	oleacc.ROLE_SYSTEM_COMBOBOX:controlTypes.ROLE_COMBOBOX,
	oleacc.ROLE_SYSTEM_LIST:controlTypes.ROLE_LIST,
	oleacc.ROLE_SYSTEM_LISTITEM:controlTypes.ROLE_LISTITEM,
	oleacc.ROLE_SYSTEM_GRAPHIC:controlTypes.ROLE_GRAPHIC,
	oleacc.ROLE_SYSTEM_HELPBALLOON:controlTypes.ROLE_HELPBALLOON,
	oleacc.ROLE_SYSTEM_TOOLTIP:controlTypes.ROLE_TOOLTIP,
	oleacc.ROLE_SYSTEM_LINK:controlTypes.ROLE_LINK,
	oleacc.ROLE_SYSTEM_OUTLINE:controlTypes.ROLE_TREEVIEW,
	oleacc.ROLE_SYSTEM_OUTLINEITEM:controlTypes.ROLE_TREEVIEWITEM,
	oleacc.ROLE_SYSTEM_OUTLINEBUTTON:controlTypes.ROLE_TREEVIEWITEM,
	oleacc.ROLE_SYSTEM_PAGETAB:controlTypes.ROLE_TAB,
	oleacc.ROLE_SYSTEM_PAGETABLIST:controlTypes.ROLE_TABCONTROL,
	oleacc.ROLE_SYSTEM_SLIDER:controlTypes.ROLE_SLIDER,
	oleacc.ROLE_SYSTEM_PROGRESSBAR:controlTypes.ROLE_PROGRESSBAR,
	oleacc.ROLE_SYSTEM_SCROLLBAR:controlTypes.ROLE_SCROLLBAR,
	oleacc.ROLE_SYSTEM_STATUSBAR:controlTypes.ROLE_STATUSBAR,
	oleacc.ROLE_SYSTEM_TABLE:controlTypes.ROLE_TABLE,
	oleacc.ROLE_SYSTEM_CELL:controlTypes.ROLE_TABLECELL,
	oleacc.ROLE_SYSTEM_COLUMN:controlTypes.ROLE_TABLECOLUMN,
	oleacc.ROLE_SYSTEM_ROW:controlTypes.ROLE_TABLEROW,
	oleacc.ROLE_SYSTEM_TOOLBAR:controlTypes.ROLE_TOOLBAR,
	oleacc.ROLE_SYSTEM_COLUMNHEADER:controlTypes.ROLE_TABLECOLUMNHEADER,
	oleacc.ROLE_SYSTEM_ROWHEADER:controlTypes.ROLE_TABLEROWHEADER,
	oleacc.ROLE_SYSTEM_SPLITBUTTON:controlTypes.ROLE_SPLITBUTTON,
	oleacc.ROLE_SYSTEM_BUTTONDROPDOWN:controlTypes.ROLE_DROPDOWNBUTTON,
	oleacc.ROLE_SYSTEM_SEPARATOR:controlTypes.ROLE_SEPARATOR,
	oleacc.ROLE_SYSTEM_DOCUMENT:controlTypes.ROLE_DOCUMENT,
	oleacc.ROLE_SYSTEM_ANIMATION:controlTypes.ROLE_ANIMATION,
	oleacc.ROLE_SYSTEM_APPLICATION:controlTypes.ROLE_APPLICATION,
	oleacc.ROLE_SYSTEM_GROUPING:controlTypes.ROLE_GROUPING,
	oleacc.ROLE_SYSTEM_PROPERTYPAGE:controlTypes.ROLE_PROPERTYPAGE,
	oleacc.ROLE_SYSTEM_ALERT:controlTypes.ROLE_ALERT,
	oleacc.ROLE_SYSTEM_BORDER:controlTypes.ROLE_BORDER,
	oleacc.ROLE_SYSTEM_BUTTONDROPDOWNGRID:controlTypes.ROLE_DROPDOWNBUTTONGRID,
	oleacc.ROLE_SYSTEM_CARET:controlTypes.ROLE_CARET,
	oleacc.ROLE_SYSTEM_CHARACTER:controlTypes.ROLE_CHARACTER,
	oleacc.ROLE_SYSTEM_CHART:controlTypes.ROLE_CHART,
	oleacc.ROLE_SYSTEM_CURSOR:controlTypes.ROLE_CURSOR,
	oleacc.ROLE_SYSTEM_DIAGRAM:controlTypes.ROLE_DIAGRAM,
	oleacc.ROLE_SYSTEM_DIAL:controlTypes.ROLE_DIAL,
	oleacc.ROLE_SYSTEM_DROPLIST:controlTypes.ROLE_DROPLIST,
	oleacc.ROLE_SYSTEM_BUTTONMENU:controlTypes.ROLE_MENUBUTTON,
	oleacc.ROLE_SYSTEM_EQUATION:controlTypes.ROLE_MATH,
	oleacc.ROLE_SYSTEM_GRIP:controlTypes.ROLE_GRIP,
	oleacc.ROLE_SYSTEM_HOTKEYFIELD:controlTypes.ROLE_HOTKEYFIELD,
	oleacc.ROLE_SYSTEM_INDICATOR:controlTypes.ROLE_INDICATOR,
	oleacc.ROLE_SYSTEM_SPINBUTTON:controlTypes.ROLE_SPINBUTTON,
	oleacc.ROLE_SYSTEM_SOUND:controlTypes.ROLE_SOUND,
	oleacc.ROLE_SYSTEM_WHITESPACE:controlTypes.ROLE_WHITESPACE,
	oleacc.ROLE_SYSTEM_IPADDRESS:controlTypes.ROLE_IPADDRESS,
	oleacc.ROLE_SYSTEM_OUTLINEBUTTON:controlTypes.ROLE_TREEVIEWBUTTON,
	oleacc.ROLE_SYSTEM_CLOCK:controlTypes.ROLE_CLOCK,
	#IAccessible2 roles
	IA2_ROLE_UNKNOWN:controlTypes.ROLE_UNKNOWN,
	IA2_ROLE_CANVAS:controlTypes.ROLE_CANVAS,
	IA2_ROLE_CAPTION:controlTypes.ROLE_CAPTION,
	IA2_ROLE_CHECK_MENU_ITEM:controlTypes.ROLE_CHECKMENUITEM,
	IA2_ROLE_COLOR_CHOOSER:controlTypes.ROLE_COLORCHOOSER,
	IA2_ROLE_DATE_EDITOR:controlTypes.ROLE_DATEEDITOR,
	IA2_ROLE_DESKTOP_ICON:controlTypes.ROLE_DESKTOPICON,
	IA2_ROLE_DESKTOP_PANE:controlTypes.ROLE_DESKTOPPANE,
	IA2_ROLE_DIRECTORY_PANE:controlTypes.ROLE_DIRECTORYPANE,
	IA2_ROLE_EDITBAR:controlTypes.ROLE_EDITBAR,
	IA2_ROLE_EMBEDDED_OBJECT:controlTypes.ROLE_EMBEDDEDOBJECT,
	IA2_ROLE_ENDNOTE:controlTypes.ROLE_ENDNOTE,
	IA2_ROLE_FILE_CHOOSER:controlTypes.ROLE_FILECHOOSER,
	IA2_ROLE_FONT_CHOOSER:controlTypes.ROLE_FONTCHOOSER,
	IA2_ROLE_FOOTER:controlTypes.ROLE_FOOTER,
	IA2_ROLE_FOOTNOTE:controlTypes.ROLE_FOOTNOTE,
	IA2_ROLE_FORM:controlTypes.ROLE_FORM,
	IA2_ROLE_FRAME:controlTypes.ROLE_FRAME,
	IA2_ROLE_GLASS_PANE:controlTypes.ROLE_GLASSPANE,
	IA2_ROLE_HEADER:controlTypes.ROLE_HEADER,
	IA2_ROLE_HEADING:controlTypes.ROLE_HEADING,
	IA2_ROLE_ICON:controlTypes.ROLE_ICON,
	IA2_ROLE_IMAGE_MAP:controlTypes.ROLE_IMAGEMAP,
	IA2_ROLE_INPUT_METHOD_WINDOW:controlTypes.ROLE_INPUTWINDOW,
	IA2_ROLE_INTERNAL_FRAME:controlTypes.ROLE_INTERNALFRAME,
	IA2_ROLE_LABEL:controlTypes.ROLE_LABEL,
	IA2_ROLE_LAYERED_PANE:controlTypes.ROLE_LAYEREDPANE,
	IA2_ROLE_NOTE:controlTypes.ROLE_NOTE,
	IA2_ROLE_OPTION_PANE:controlTypes.ROLE_OPTIONPANE,
	IA2_ROLE_PAGE:controlTypes.ROLE_PAGE,
	IA2_ROLE_PARAGRAPH:controlTypes.ROLE_PARAGRAPH,
	IA2_ROLE_RADIO_MENU_ITEM:controlTypes.ROLE_RADIOMENUITEM,
	IA2_ROLE_REDUNDANT_OBJECT:controlTypes.ROLE_REDUNDANTOBJECT,
	IA2_ROLE_ROOT_PANE:controlTypes.ROLE_ROOTPANE,
	IA2_ROLE_RULER:controlTypes.ROLE_RULER,
	IA2_ROLE_SCROLL_PANE:controlTypes.ROLE_SCROLLPANE,
	IA2_ROLE_SECTION:controlTypes.ROLE_SECTION,
	IA2_ROLE_SHAPE:controlTypes.ROLE_SHAPE,
	IA2_ROLE_SPLIT_PANE:controlTypes.ROLE_SPLITPANE,
	IA2_ROLE_TEAR_OFF_MENU:controlTypes.ROLE_TEAROFFMENU,
	IA2_ROLE_TERMINAL:controlTypes.ROLE_TERMINAL,
	IA2_ROLE_TEXT_FRAME:controlTypes.ROLE_TEXTFRAME,
	IA2_ROLE_TOGGLE_BUTTON:controlTypes.ROLE_TOGGLEBUTTON,
	IA2_ROLE_VIEW_PORT:controlTypes.ROLE_VIEWPORT,
	#some common string roles
	"frame":controlTypes.ROLE_FRAME,
	"iframe":controlTypes.ROLE_INTERNALFRAME,
	"page":controlTypes.ROLE_PAGE,
	"form":controlTypes.ROLE_FORM,
	"div":controlTypes.ROLE_SECTION,
	"li":controlTypes.ROLE_LISTITEM,
	"ul":controlTypes.ROLE_LIST,
	"tbody":controlTypes.ROLE_TABLEBODY,
	"browser":controlTypes.ROLE_WINDOW,
	"h1":controlTypes.ROLE_HEADING1,
	"h2":controlTypes.ROLE_HEADING2,
	"h3":controlTypes.ROLE_HEADING3,
	"h4":controlTypes.ROLE_HEADING4,
	"h5":controlTypes.ROLE_HEADING5,
	"h6":controlTypes.ROLE_HEADING6,
	"p":controlTypes.ROLE_PARAGRAPH,
	"hbox":controlTypes.ROLE_BOX,
	"embed":controlTypes.ROLE_EMBEDDEDOBJECT,
	"object":controlTypes.ROLE_EMBEDDEDOBJECT,
	"applet":controlTypes.ROLE_EMBEDDEDOBJECT,
}

IAccessibleStatesToNVDAStates={
	oleacc.STATE_SYSTEM_TRAVERSED:controlTypes.STATE_VISITED,
	oleacc.STATE_SYSTEM_UNAVAILABLE:controlTypes.STATE_UNAVAILABLE,
	oleacc.STATE_SYSTEM_FOCUSED:controlTypes.STATE_FOCUSED,
	oleacc.STATE_SYSTEM_SELECTED:controlTypes.STATE_SELECTED,
	oleacc.STATE_SYSTEM_BUSY:controlTypes.STATE_BUSY,
	oleacc.STATE_SYSTEM_PRESSED:controlTypes.STATE_PRESSED,
	oleacc.STATE_SYSTEM_CHECKED:controlTypes.STATE_CHECKED,
	oleacc.STATE_SYSTEM_MIXED:controlTypes.STATE_HALFCHECKED,
	oleacc.STATE_SYSTEM_READONLY:controlTypes.STATE_READONLY,
	oleacc.STATE_SYSTEM_EXPANDED:controlTypes.STATE_EXPANDED,
	oleacc.STATE_SYSTEM_COLLAPSED:controlTypes.STATE_COLLAPSED,
	oleacc.STATE_SYSTEM_OFFSCREEN:controlTypes.STATE_OFFSCREEN,
	oleacc.STATE_SYSTEM_INVISIBLE:controlTypes.STATE_INVISIBLE,
	oleacc.STATE_SYSTEM_TRAVERSED:controlTypes.STATE_VISITED,
	oleacc.STATE_SYSTEM_LINKED:controlTypes.STATE_LINKED,
	oleacc.STATE_SYSTEM_HASPOPUP:controlTypes.STATE_HASPOPUP,
	oleacc.STATE_SYSTEM_PROTECTED:controlTypes.STATE_PROTECTED,
	oleacc.STATE_SYSTEM_SELECTABLE:controlTypes.STATE_SELECTABLE,
	oleacc.STATE_SYSTEM_FOCUSABLE:controlTypes.STATE_FOCUSABLE,
}

IAccessible2StatesToNVDAStates={
	IA2_STATE_REQUIRED:controlTypes.STATE_REQUIRED,
	IA2_STATE_DEFUNCT:controlTypes.STATE_DEFUNCT,
	#IA2_STATE_STALE:controlTypes.STATE_DEFUNCT,
	IA2_STATE_INVALID_ENTRY:controlTypes.STATE_INVALID_ENTRY,
	IA2_STATE_MODAL:controlTypes.STATE_MODAL,
	IA2_STATE_SUPPORTS_AUTOCOMPLETION:controlTypes.STATE_AUTOCOMPLETE,
	IA2_STATE_MULTI_LINE:controlTypes.STATE_MULTILINE,
	IA2_STATE_ICONIFIED:controlTypes.STATE_ICONIFIED,
	IA2_STATE_EDITABLE:controlTypes.STATE_EDITABLE,
	IA2_STATE_PINNED:controlTypes.STATE_PINNED,
}

#A list to store handles received from setWinEventHook, for use with unHookWinEvent  
winEventHookIDs=[]

def normalizeIAccessible(pacc,childID=0):
	if not isinstance(pacc,IAccessible):
		try:
			pacc=pacc.QueryInterface(IAccessible)
		except COMError:
			raise RuntimeError("%s Not an IAccessible"%pacc)
	# #2558: IAccessible2 doesn't support simple children.
	# Therefore, it doesn't make sense to use IA2 if the child ID is non-0.
	if childID==0 and not isinstance(pacc,IAccessible2):
		try:
			s=pacc.QueryInterface(IServiceProvider)
			pacc2=s.QueryService(IAccessible._iid_,IAccessible2)
			if not pacc2:
				# QueryService should fail if IA2 is not supported, but some applications such as AIM 7 misbehave and return a null COM pointer.
				# Treat this as if QueryService failed.
				raise ValueError
			pacc=pacc2
		except:
			pass
	return pacc

def accessibleObjectFromEvent(window,objectID,childID):
	try:
		pacc,childID=oleacc.AccessibleObjectFromEvent(window,objectID,childID)
	except Exception as e:
		log.debugWarning("oleacc.AccessibleObjectFromEvent with window %s, objectID %s and childID %s: %s"%(window,objectID,childID,e))
		return None
	return (normalizeIAccessible(pacc,childID),childID)

def accessibleObjectFromPoint(x,y):
	try:
		pacc, child = oleacc.AccessibleObjectFromPoint(x, y)
	except:
		return None
	return (normalizeIAccessible(pacc,child),child)

def windowFromAccessibleObject(ia):
	try:
		return oleacc.WindowFromAccessibleObject(ia)
	except:
		return 0

def accessibleChildren(ia,startIndex,numChildren):
	# #4091: AccessibleChildren can throw WindowsError (blocked by callee) e.g. Outlook 2010 Email setup and new profiles dialogs
	try:
		rawChildren=oleacc.AccessibleChildren(ia,startIndex,numChildren)
	except (WindowsError,COMError):
		log.debugWarning("AccessibleChildren failed",exc_info=True)
		return []
	children=[]
	for child in rawChildren:
		if child is None:
			# This is a bug in the server.
			# Filtering these out here makes life easier for the caller.
			continue
		elif isinstance(child,comtypes.client.lazybind.Dispatch) or isinstance(child,comtypes.client.dynamic._Dispatch) or isinstance(child,IUnknown):
			child=(normalizeIAccessible(child),0)
		elif isinstance(child,int):
			child=(ia,child)
		children.append(child)
	return children

def accFocus(ia):
	try:
		res=ia.accFocus
		if isinstance(res,comtypes.client.lazybind.Dispatch) or isinstance(res,comtypes.client.dynamic._Dispatch) or isinstance(res,IUnknown):
			new_ia=normalizeIAccessible(res)
			new_child=0
		elif res==0:
			# #3005: Don't call accChild for CHILDID_SELF.
			new_ia=ia
			new_child=res
		elif isinstance(res,int):
			# accFocus can return a child ID even when there is actually an IAccessible for that child; e.g. Lotus Symphony.
			try:
				new_ia=ia.accChild(res)
			except:
				new_ia=None
			if new_ia:
				new_ia=normalizeIAccessible(new_ia)
				new_child=0
			else:
				new_ia=ia
				new_child=res
		else:
			return None
		return (new_ia,new_child)
	except:
		return None

def accHitTest(ia,x,y):
	try:
		res=ia.accHitTest(x,y)
	except COMError:
		return None
	if isinstance(res,comtypes.client.lazybind.Dispatch) or isinstance(res,comtypes.client.dynamic._Dispatch) or isinstance(res,IUnknown):
		return accHitTest(normalizeIAccessible(res),x,y),0
	elif isinstance(res,int):
		return ia,res
	return None

def accChild(ia,child):
	try:
		res=ia.accChild(child)
		if not res:
			return (ia,child)
		elif isinstance(res,comtypes.client.lazybind.Dispatch) or isinstance(res,comtypes.client.dynamic._Dispatch) or isinstance(res,IUnknown):
			return normalizeIAccessible(res),0
	except:
		pass
	return None

def accParent(ia,child):
	try:
		if not child:
			res=ia.accParent
			if isinstance(res,comtypes.client.lazybind.Dispatch) or isinstance(res,comtypes.client.dynamic._Dispatch) or isinstance(res,IUnknown):
				new_ia=normalizeIAccessible(res)
				new_child=0
			else:
				raise ValueError("no IAccessible interface")
		else:
			new_ia=ia
			new_child=0
		return (new_ia,new_child)
	except:
		return None

def accNavigate(ia,child,direction):
	res=None
	try:
		res=ia.accNavigate(direction,child)
		if isinstance(res,int):
			new_ia=ia
			new_child=res
		elif isinstance(res,comtypes.client.lazybind.Dispatch) or isinstance(res,comtypes.client.dynamic._Dispatch) or isinstance(res,IUnknown):
			new_ia=normalizeIAccessible(res)
			new_child=0
		else:
			raise RuntimeError
		return (new_ia,new_child)
	except:
		pass


winEventIDsToNVDAEventNames={
winUser.EVENT_SYSTEM_DESKTOPSWITCH:"desktopSwitch",
winUser.EVENT_SYSTEM_FOREGROUND:"gainFocus",
winUser.EVENT_SYSTEM_ALERT:"alert",
winUser.EVENT_SYSTEM_MENUSTART:"menuStart",
winUser.EVENT_SYSTEM_MENUEND:"menuEnd",
winUser.EVENT_SYSTEM_MENUPOPUPSTART:"menuStart",
winUser.EVENT_SYSTEM_MENUPOPUPEND:"menuEnd",
winUser.EVENT_SYSTEM_SCROLLINGSTART:"scrollingStart",
# We don't need switchStart.
winUser.EVENT_SYSTEM_SWITCHEND:"switchEnd",
winUser.EVENT_OBJECT_FOCUS:"gainFocus",
winUser.EVENT_OBJECT_SHOW:"show",
winUser.EVENT_OBJECT_HIDE:"hide",
winUser.EVENT_OBJECT_DESTROY:"destroy",
winUser.EVENT_OBJECT_DESCRIPTIONCHANGE:"descriptionChange",
winUser.EVENT_OBJECT_LOCATIONCHANGE:"locationChange",
winUser.EVENT_OBJECT_NAMECHANGE:"nameChange",
winUser.EVENT_OBJECT_REORDER:"reorder",
winUser.EVENT_OBJECT_SELECTION:"selection",
winUser.EVENT_OBJECT_SELECTIONADD:"selectionAdd",
winUser.EVENT_OBJECT_SELECTIONREMOVE:"selectionRemove",
winUser.EVENT_OBJECT_SELECTIONWITHIN:"selectionWithIn",
winUser.EVENT_OBJECT_STATECHANGE:"stateChange",
winUser.EVENT_OBJECT_VALUECHANGE:"valueChange",
IA2_EVENT_TEXT_CARET_MOVED:"caret",
IA2_EVENT_DOCUMENT_LOAD_COMPLETE:"documentLoadComplete",
IA2_EVENT_OBJECT_ATTRIBUTE_CHANGED:"IA2AttributeChange",
}

def winEventToNVDAEvent(eventID,window,objectID,childID,useCache=True):
	"""Tries to convert a win event ID to an NVDA event name, and instanciate or fetch an NVDAObject for the win event parameters.
	@param eventID: the win event ID (type)
	@type eventID: integer
	@param window: the win event's window handle
	@type window: integer
	@param objectID: the win event's object ID
	@type objectID: integer
	@param childID: the win event's childID
	@type childID: the win event's childID
	@param useCache: C{True} to use the L{liveNVDAObjectTable} cache when retrieving an NVDAObject, C{False} if the cache should not be used.
	@type useCache: boolean
	@returns: the NVDA event name and the NVDAObject the event is for
	@rtype: tuple of string and L{NVDAObjects.IAccessible.IAccessible}
	"""
	NVDAEventName=winEventIDsToNVDAEventNames.get(eventID,None)
	if not NVDAEventName:
		return None
	#Ignore any events with invalid window handles
	if not window or not winUser.isWindow(window):
		return None
	#Make sure this window does not have a ghost window if possible
	if NVDAObjects.window.GhostWindowFromHungWindow and NVDAObjects.window.GhostWindowFromHungWindow(window):
		return None
	#We do not support MSAA object proxied from native UIA
	if UIAHandler.handler and UIAHandler.handler.isUIAWindow(window):
		return None
	obj=None
	if useCache:
		#See if we already know an object by this win event info
		obj=liveNVDAObjectTable.get((window,objectID,childID),None)
	#If we don't yet have the object, then actually instanciate it.
	if not obj: 
		obj=NVDAObjects.IAccessible.getNVDAObjectFromEvent(window,objectID,childID)
	#At this point if we don't have an object then we can't do any more
	if not obj:
		return None
	#SDM MSAA objects sometimes don't contain enough information to be useful
	#Sometimes there is a real window that does, so try to get the SDMChild property on the NVDAObject, and if successull use that as obj instead.
	if 'bosa_sdm' in obj.windowClassName:
		SDMChild=getattr(obj,'SDMChild',None)
		if SDMChild: obj=SDMChild
	return (NVDAEventName,obj)

def winEventCallback(handle,eventID,window,objectID,childID,threadID,timestamp):
	try:
		#Ignore all object IDs from alert onwards (sound, nativeom etc) as we don't support them
		if objectID<=winUser.OBJID_ALERT: 
			return
		#Ignore all locationChange events except ones for the caret
		if eventID==winUser.EVENT_OBJECT_LOCATIONCHANGE and objectID!=winUser.OBJID_CARET:
			return
		if eventID==winUser.EVENT_OBJECT_DESTROY:
			processDestroyWinEvent(window,objectID,childID)
			return
		#Change window objIDs to client objIDs for better reporting of objects
		if (objectID==0) and (childID==0):
			objectID=winUser.OBJID_CLIENT
		#Ignore events with invalid window handles
		isWindow = winUser.isWindow(window) if window else 0
		if window==0 or (not isWindow and eventID in (winUser.EVENT_SYSTEM_SWITCHSTART,winUser.EVENT_SYSTEM_SWITCHEND,winUser.EVENT_SYSTEM_MENUEND,winUser.EVENT_SYSTEM_MENUPOPUPEND)):
			window=winUser.getDesktopWindow()
		elif not isWindow:
			return

		if childID<0:
			tempWindow=window
			while tempWindow and not winUser.getWindowStyle(tempWindow)&winUser.WS_POPUP and winUser.getClassName(tempWindow)=="MozillaWindowClass":
				tempWindow=winUser.getAncestor(tempWindow,winUser.GA_PARENT)
			if tempWindow and winUser.getClassName(tempWindow).startswith('Mozilla'):
				window=tempWindow

		windowClassName=winUser.getClassName(window)
		#At the moment we can't handle show, hide or reorder events on Mozilla Firefox Location bar,as there are just too many of them
		#Ignore show, hide and reorder on MozillaDropShadowWindowClass windows.
		if windowClassName.startswith('Mozilla') and eventID in (winUser.EVENT_OBJECT_SHOW,winUser.EVENT_OBJECT_HIDE,winUser.EVENT_OBJECT_REORDER) and childID<0:
			#Mozilla Gecko can sometimes fire win events on a catch-all window which isn't really the real window
			#Move up the ancestry to find the real mozilla Window and use that
			if winUser.getClassName(window)=='MozillaDropShadowWindowClass':
				return
		if eventID==winUser.EVENT_SYSTEM_FOREGROUND:
			#We never want to see foreground events for the Program Manager or Shell (task bar) 
			if windowClassName in ("Progman","Shell_TrayWnd"):
				return
			# #3831: Event handling can be deferred if Windows takes a while to change the foreground window.
			# See pumpAll for details.
			global _deferUntilForegroundWindow,_foregroundDefers
			_deferUntilForegroundWindow=window
			_foregroundDefers=0
		if windowClassName=="MSNHiddenWindowClass":
			# HACK: Events get fired by this window in Windows Live Messenger 2009 when it starts.
			# If we send a WM_NULL to this window at this point (which happens in accessibleObjectFromEvent), Messenger will silently exit (#677).
			# Therefore, completely ignore these events, which is useless to us anyway.
			return
		if winEventLimiter.addEvent(eventID,window,objectID,childID,threadID):
			core.requestPump()
	except:
		log.error("winEventCallback", exc_info=True)

def processGenericWinEvent(eventID,window,objectID,childID):
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
	#Notify appModuleHandler of this new window
	appModuleHandler.update(winUser.getWindowThreadProcessID(window)[0])
	#Handle particular events for the special MSAA caret object just as if they were for the focus object
	focus=eventHandler.lastQueuedFocusObject
	if focus and objectID==winUser.OBJID_CARET and eventID in (winUser.EVENT_OBJECT_LOCATIONCHANGE,winUser.EVENT_OBJECT_SHOW):
		NVDAEvent=("caret",focus)
	else:
		NVDAEvent=winEventToNVDAEvent(eventID,window,objectID,childID)
		if not NVDAEvent:
			return False
	if NVDAEvent[0]=="nameChange" and objectID==winUser.OBJID_CURSOR:
		mouseHandler.updateMouseShape(NVDAEvent[1].name)
		return
	if NVDAEvent[1]==focus:
		NVDAEvent=(NVDAEvent[0],focus)
	eventHandler.queueEvent(*NVDAEvent)
	return True

def processFocusWinEvent(window,objectID,childID,force=False):
	"""checks to see if the focus win event is not the same as the existing focus, 
	then converts the win event to an NVDA event (instanciating an NVDA Object) then calls processFocusNVDAEvent. If all is ok it returns True.
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
	windowClassName=winUser.getClassName(window)
	# Generally, we must ignore focus on child windows of SDM windows as we only want the SDM MSAA events.
	# However, we don't want to ignore focus if the child ID isn't 0,
	# as this is a child control and the SDM MSAA events don't handle child controls.
	if childID==0 and not windowClassName.startswith('bosa_sdm') and winUser.getClassName(winUser.getAncestor(window,winUser.GA_PARENT)).startswith('bosa_sdm'):
		return False
	#Notify appModuleHandler of this new foreground window
	appModuleHandler.update(winUser.getWindowThreadProcessID(window)[0])
	#If Java access bridge is running, and this is a java window, then pass it to java and forget about it
	if childID==0 and objectID==winUser.OBJID_CLIENT and JABHandler.isRunning and JABHandler.isJavaWindow(window):
		JABHandler.event_enterJavaWindow(window)
		return True
	#Convert the win event to an NVDA event
	NVDAEvent=winEventToNVDAEvent(winUser.EVENT_OBJECT_FOCUS,window,objectID,childID,useCache=False)
	if not NVDAEvent:
		return False
	eventName,obj=NVDAEvent
	if (childID==0 and obj.IAccessibleRole==oleacc.ROLE_SYSTEM_LIST) or (objectID==winUser.OBJID_CLIENT and "SysListView32" in obj.windowClassName):
		# Some controls incorrectly fire focus on child ID 0, even when there is a child with focus.
		try:
			realChildID=obj.IAccessibleObject.accFocus
		except:
			realChildID=None
		if isinstance(realChildID,int) and realChildID>0 and realChildID!=childID:
			realObj=NVDAObjects.IAccessible.IAccessible(IAccessibleObject=obj.IAccessibleObject,IAccessibleChildID=realChildID,event_windowHandle=window,event_objectID=objectID,event_childID=realChildID)
			if realObj:
				obj=realObj
	return processFocusNVDAEvent(obj,force=force)

def processFocusNVDAEvent(obj,force=False):
	"""Processes a focus NVDA event.
	If the focus event is valid, it is queued.
	@param obj: the NVDAObject the focus event is for
	@type obj: L{NVDAObjects.NVDAObject}
	@param force: If True, the shouldAllowIAccessibleFocusEvent property of the object is ignored.
	@type force: boolean
	@return: C{True} if the focus event is valid and was queued, C{False} otherwise.
	@rtype: boolean
	"""
	if not force and isinstance(obj,NVDAObjects.IAccessible.IAccessible):
		focus=eventHandler.lastQueuedFocusObject
		if isinstance(focus,NVDAObjects.IAccessible.IAccessible) and focus.isDuplicateIAccessibleEvent(obj):
			return True
		if not obj.shouldAllowIAccessibleFocusEvent:
			return False
	eventHandler.queueEvent('gainFocus',obj)
	return True

class SecureDesktopNVDAObject(NVDAObjects.window.Desktop):

	def findOverlayClasses(self,clsList):
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

def processDesktopSwitchWinEvent(window,objectID,childID):
	hDesk=windll.user32.OpenInputDesktop(0, False, 0)
	if hDesk!=0:
		windll.user32.CloseDesktop(hDesk)
		core.callLater(200, _correctFocus)
	else:
		# Switching to a secure desktop.
		# We don't receive key up events for any keys down before switching to a secure desktop,
		# so clear our recorded modifiers.
		keyboardHandler.currentModifiers.clear()
		obj=SecureDesktopNVDAObject(windowHandle=window)
		eventHandler.executeEvent("gainFocus",obj)

def _correctFocus():
	eventHandler.queueEvent("gainFocus",api.getDesktopObject().objectWithFocus())

def processForegroundWinEvent(window,objectID,childID):
	"""checks to see if the foreground win event is not the same as the existing focus or any of its parents, 
	then converts the win event to an NVDA event (instanciating an NVDA Object) and then checks the NVDAObject against the existing focus object. 
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
	#Ignore foreground events on windows that aren't the current foreground window
	if window!=winUser.getForegroundWindow():
		return False
	# If there is a pending gainFocus, it will handle the foreground object.
	oldFocus=eventHandler.lastQueuedFocusObject
	#If this foreground win event's window is an ancestor of the existing focus's window, then ignore it
	if isinstance(oldFocus,NVDAObjects.window.Window) and winUser.isDescendantWindow(window,oldFocus.windowHandle):
		return False
	#If the existing focus has the same win event params as these, then ignore this event
	if isinstance(oldFocus,NVDAObjects.IAccessible.IAccessible) and window==oldFocus.event_windowHandle and objectID==oldFocus.event_objectID and childID==oldFocus.event_childID:
		return False
	#Notify appModuleHandler of this new foreground window
	appModuleHandler.update(winUser.getWindowThreadProcessID(window)[0])
	#If Java access bridge is running, and this is a java window, then pass it to java and forget about it
	if JABHandler.isRunning and JABHandler.isJavaWindow(window):
		JABHandler.event_enterJavaWindow(window)
		return True
	#Convert the win event to an NVDA event
	NVDAEvent=winEventToNVDAEvent(winUser.EVENT_SYSTEM_FOREGROUND,window,objectID,childID,useCache=False)
	if not NVDAEvent:
		return False
	eventHandler.queueEvent(*NVDAEvent)
	return True

def processShowWinEvent(window,objectID,childID):
	# eventHandler.shouldAcceptEvent only accepts show events for a few specific cases.
	# Narrow this further to only accept events for clients or custom objects.
	if objectID==winUser.OBJID_CLIENT or objectID>0:
		NVDAEvent=winEventToNVDAEvent(winUser.EVENT_OBJECT_SHOW,window,objectID,childID)
		if NVDAEvent:
			eventHandler.queueEvent(*NVDAEvent)

def processDestroyWinEvent(window,objectID,childID):
	"""Process a destroy win event.
	This removes the object associated with the event parameters from L{liveNVDAObjectTable} if such an object exists.
	"""
	try:
		del liveNVDAObjectTable[(window,objectID,childID)]
	except KeyError:
		pass
	#Specific support for input method MSAA candidate lists.
	#When their window is destroyed we must correct focus to its parent - which could be a composition string
	# so can't use generic focus correction. (#2695)
	focus=api.getFocusObject()
	from NVDAObjects.IAccessible.mscandui import BaseCandidateItem
	if objectID==0 and childID==0 and isinstance(focus,BaseCandidateItem) and window==focus.windowHandle and not eventHandler.isPendingEvents("gainFocus"):
		obj=focus.parent
		if obj:
			eventHandler.queueEvent("gainFocus",obj)

def processMenuStartWinEvent(eventID, window, objectID, childID, validFocus):
	"""Process a menuStart win event.
	@postcondition: Focus will be directed to the menu if appropriate.
	"""
	if validFocus:
		lastFocus=eventHandler.lastQueuedFocusObject
		if isinstance(lastFocus,NVDAObjects.IAccessible.IAccessible) and lastFocus.IAccessibleRole in (oleacc.ROLE_SYSTEM_MENUPOPUP, oleacc.ROLE_SYSTEM_MENUITEM):
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
	# A suitable event for faking the focus has been received with no focus event, so we probably need to find the focus and fake it.
	# However, it is possible that the focus event has simply been delayed, so wait a bit and only do it if the focus hasn't changed yet.
	core.callLater(50, _fakeFocus, api.getFocusObject())

def _fakeFocus(oldFocus):
	if oldFocus is not api.getFocusObject():
		# The focus has changed - no need to fake it.
		return
	focus = api.getDesktopObject().objectWithFocus()
	if not focus:
		return
	processFocusNVDAEvent(focus)

#Register internal object event with IAccessible
cWinEventCallback=WINFUNCTYPE(None,c_int,c_int,c_int,c_int,c_int,c_int,c_int)(winEventCallback)

accPropServices=None

def initialize():
	global accPropServices
	try:
		accPropServices=comtypes.client.CreateObject(CAccPropServices)
	except (WindowsError,COMError) as e:
		log.debugWarning("AccPropServices is not available: %s"%e)
	for eventType in winEventIDsToNVDAEventNames.keys():
		hookID=winUser.setWinEventHook(eventType,eventType,0,cWinEventCallback,0,0,0)
		if hookID:
			winEventHookIDs.append(hookID)
		else:
			log.error("initialize: could not register callback for event %s (%s)"%(eventType,winEventIDsToNVDAEventNames[eventType]))

def pumpAll():
	global _deferUntilForegroundWindow,_foregroundDefers
	if _deferUntilForegroundWindow:
		# #3831: Sometimes, a foreground event is fired,
		# but GetForegroundWindow() takes a short while to return this new foreground.
		if _foregroundDefers<MAX_FOREGROUND_DEFERS and winUser.getForegroundWindow()!=_deferUntilForegroundWindow:
			# Wait a core cycle before handling events to give the foreground window time to update.
			core.requestPump()
			_foregroundDefers+=1
			return
		else:
			# Either the foreground window is now correct
			# or we've already had the maximum number of defers.
			# (Sometimes, foreground events are fired even when the foreground hasn't actually changed.)
			_deferUntilForegroundWindow=None

	#Receive all the winEvents from the limiter for this cycle
	winEvents=winEventLimiter.flushEvents()
	focusWinEvents=[]
	validFocus=False
	fakeFocusEvent=None
	for winEvent in winEvents[0-MAX_WINEVENTS:]:
		# #4001: Ideally, we'd call shouldAcceptEvent in winEventCallback,
		# but this causes focus issues when starting applications.
		if not eventHandler.shouldAcceptEvent(winEventIDsToNVDAEventNames[winEvent[0]], windowHandle=winEvent[1]):
			continue
		#We want to only pass on one focus event to NVDA, but we always want to use the most recent possible one 
		if winEvent[0] in (winUser.EVENT_OBJECT_FOCUS,winUser.EVENT_SYSTEM_FOREGROUND):
			focusWinEvents.append(winEvent)
			continue
		else:
			for focusWinEvent in reversed(focusWinEvents):
				procFunc=processForegroundWinEvent if focusWinEvent[0]==winUser.EVENT_SYSTEM_FOREGROUND else processFocusWinEvent
				if procFunc(*(focusWinEvent[1:])):
					validFocus=True
					break
			focusWinEvents=[]
			if winEvent[0]==winUser.EVENT_SYSTEM_DESKTOPSWITCH:
				processDesktopSwitchWinEvent(*winEvent[1:])
			elif winEvent[0]==winUser.EVENT_OBJECT_SHOW:
				processShowWinEvent(*winEvent[1:])
			elif winEvent[0] in MENU_EVENTIDS+(winUser.EVENT_SYSTEM_SWITCHEND,):
				# If there is no valid focus event, we may need to use this to fake the focus later.
				fakeFocusEvent=winEvent
			else:
				processGenericWinEvent(*winEvent)
	for focusWinEvent in reversed(focusWinEvents):
		procFunc=processForegroundWinEvent if focusWinEvent[0]==winUser.EVENT_SYSTEM_FOREGROUND else processFocusWinEvent
		if procFunc(*(focusWinEvent[1:])):
			validFocus=True
			break
	if fakeFocusEvent:
		# Try this as a last resort.
		if fakeFocusEvent[0] in (winUser.EVENT_SYSTEM_MENUSTART, winUser.EVENT_SYSTEM_MENUPOPUPSTART):
			# menuStart needs to be handled specially and might act even if there was a valid focus event.
			processMenuStartWinEvent(*fakeFocusEvent, validFocus=validFocus)
		elif not validFocus:
			# Other fake focus events only need to be handled if there was no valid focus event.
			processFakeFocusWinEvent(*fakeFocusEvent)

def terminate():
	for handle in winEventHookIDs:
		winUser.unhookWinEvent(handle)

def getIAccIdentity(pacc,childID):
	IAccIdentityObject=pacc.QueryInterface(IAccIdentity)
	stringPtr,stringSize=IAccIdentityObject.getIdentityString(childID)
	try:
		if accPropServices:
			try:
				hwnd,objectID,childID=accPropServices.DecomposeHwndIdentityString(stringPtr,stringSize)
				return dict(windowHandle=hwnd,objectID=c_int(objectID).value,childID=childID)
			except COMError:
				hmenu,childID=accPropServices.DecomposeHmenuIdentityString(stringPtr,stringSize)
				# hmenu is a wireHMENU, but it seems we can just treat this as a number.
				# comtypes transparently does this for wireHWND.
				return dict(menuHandle=cast(hmenu,wintypes.HMENU).value,childID=childID)
		stringPtr=cast(stringPtr,POINTER(c_char*stringSize))
		fields=struct.unpack('IIiI',stringPtr.contents.raw)
		d={}
		d['childID']=fields[3]
		if fields[0]&2:
			d['menuHandle']=fields[2]
		else:
			d['objectID']=fields[2]
			d['windowHandle']=fields[1]
		return d
	finally:
		windll.ole32.CoTaskMemFree(stringPtr)

def findGroupboxObject(obj):
	prevWindow=winUser.getPreviousWindow(obj.windowHandle)
	while prevWindow:
		if winUser.getClassName(prevWindow)=="Button" and winUser.getWindowStyle(prevWindow)&winUser.BS_GROUPBOX and winUser.isWindowVisible(prevWindow):
			groupObj=NVDAObjects.IAccessible.getNVDAObjectFromEvent(prevWindow,winUser.OBJID_CLIENT,0)
			try:
				(left,top,width,height)=obj.location
				(groupLeft,groupTop,groupWidth,groupHeight)=groupObj.location
			except:
				return
			if groupObj.IAccessibleRole==oleacc.ROLE_SYSTEM_GROUPING and left>=groupLeft and (left+width)<=(groupLeft+groupWidth) and top>=groupTop and (top+height)<=(groupTop+groupHeight):
				return groupObj
		prevWindow=winUser.getPreviousWindow(prevWindow)

def getRecursiveTextFromIAccessibleTextObject(obj,startOffset=0,endOffset=-1):
	if not isinstance(obj,IAccessibleText):
		try:
			textObject=obj.QueryInterface(IAccessibleText)
		except:
			textObject=None
	else:
		textObject=obj
	if not isinstance(obj,IAccessible):
		try:
			accObject=obj.QueryInterface(IAccessible)
		except:
			return ""
	else:
		accObject=obj
	try:
		text=textObject.text(startOffset,endOffset)
	except:
		text=None
	if not text or text.isspace(): 
		try:
			name=accObject.accName(0)
		except:
			name=None
		try:
			value=accObject.accValue(0)
		except:
			value=None
		try:
			description=accObject.accDescription(0)
		except:
			description=None
		return " ".join([x for x in [name,value,description] if x and not x.isspace()])
	try:
		hypertextObject=accObject.QueryInterface(IAccessibleHypertext)
	except:
		return text
	textList=[]
	for i in xrange(len(text)):
		t=text[i]
		if ord(t)==0xFFFC:
			try:
				childTextObject=hypertextObject.hyperlink(hypertextObject.hyperlinkIndex(i+startOffset)).QueryInterface(IAccessible)
				t=" %s "%getRecursiveTextFromIAccessibleTextObject(childTextObject)
			except:
				pass
		textList.append(t)
	return "".join(textList).replace('  ',' ')

def splitIA2Attribs(attribsString):
	"""Split an IAccessible2 attributes string into a dict of attribute keys and values.
	An invalid attributes string does not cause an error, but strange results may be returned.
	Subattributes are handled. Subattribute keys and values are placed into a dict which becomes the value of the attribute.
	@param attribsString: The IAccessible2 attributes string to convert.
	@type attribsString: str
	@return: A dict of the attribute keys and values, where values are strings or dicts.
	@rtype: {str: str or {str: str}}
	"""
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
	"""Looks at the location of the first function in the IAccessible object's vtable (IUnknown::AddRef) to see if it was implemented in oleacc.dll (its local) or ole32.dll (its marshalled)."""
	if not isinstance(IAccessibleObject,IAccessible):
		raise TypeError("object should be of type IAccessible, not %s"%IAccessibleObject)
	buf=create_unicode_buffer(1024)
	addr=POINTER(c_void_p).from_address(super(comtypes._compointer_base,IAccessibleObject).value).contents.value
	handle=HANDLE()
	windll.kernel32.GetModuleHandleExW(6,addr,byref(handle))
	windll.kernel32.GetModuleFileNameW(handle,buf,1024)
	return not buf.value.lower().endswith('oleacc.dll')
