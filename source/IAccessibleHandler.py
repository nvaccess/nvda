#IAccessiblehandler.py
	#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from __future__ import with_statement

MAX_WINEVENTS=500

#Constants
#OLE constants
REGCLS_SINGLEUSE = 0       # class object only generates one instance
REGCLS_MULTIPLEUSE = 1     # same class object genereates multiple inst.
REGCLS_MULTI_SEPARATE = 2  # multiple use, but separate control over each
REGCLS_SUSPENDED      = 4  # register it as suspended, will be activated
REGCLS_SURROGATE      = 8  # must be used when a surrogate process

CLSCTX_INPROC_SERVER=1
CLSCTX_LOCAL_SERVER=4
#IAccessible Object IDs
OBJID_WINDOW=0
OBJID_SYSMENU=-1
OBJID_TITLEBAR=-2
OBJID_MENU=-3
OBJID_CLIENT=-4
OBJID_VSCROLL=-5
OBJID_HSCROLL=-6
OBJID_SIZEGRIP=-7
OBJID_CARET=-8
OBJID_CURSOR=-9
OBJID_ALERT=-10
OBJID_SOUND=-11
OBJID_NATIVEOM=-16
#IAccessible navigation
NAVDIR_DOWN=2
NAVDIR_FIRSTCHILD=7
NAVDIR_LASTCHILD=8
NAVDIR_LEFT=3
NAVDIR_NEXT=5
NAVDIR_PREVIOUS=6
NAVDIR_RIGHT=4
NAVDIR_UP=1
#IAccessible roles
ROLE_SYSTEM_TITLEBAR=1
ROLE_SYSTEM_MENUBAR=2
ROLE_SYSTEM_SCROLLBAR=3
ROLE_SYSTEM_GRIP=4
ROLE_SYSTEM_SOUND=5
ROLE_SYSTEM_CURSOR=6
ROLE_SYSTEM_CARET=7
ROLE_SYSTEM_ALERT=8
ROLE_SYSTEM_WINDOW=9
ROLE_SYSTEM_CLIENT=10
ROLE_SYSTEM_MENUPOPUP=11
ROLE_SYSTEM_MENUITEM=12
ROLE_SYSTEM_TOOLTIP=13
ROLE_SYSTEM_APPLICATION=14
ROLE_SYSTEM_DOCUMENT=15
ROLE_SYSTEM_PANE=16
ROLE_SYSTEM_CHART=17
ROLE_SYSTEM_DIALOG=18
ROLE_SYSTEM_BORDER=19
ROLE_SYSTEM_GROUPING=20
ROLE_SYSTEM_SEPARATOR=21
ROLE_SYSTEM_TOOLBAR=22
ROLE_SYSTEM_STATUSBAR=23
ROLE_SYSTEM_TABLE=24
ROLE_SYSTEM_COLUMNHEADER=25
ROLE_SYSTEM_ROWHEADER=26
ROLE_SYSTEM_COLUMN=27
ROLE_SYSTEM_ROW=28
ROLE_SYSTEM_CELL=29
ROLE_SYSTEM_LINK=30
ROLE_SYSTEM_HELPBALLOON=31
ROLE_SYSTEM_CHARACTER=32
ROLE_SYSTEM_LIST=33
ROLE_SYSTEM_LISTITEM=34
ROLE_SYSTEM_OUTLINE=35
ROLE_SYSTEM_OUTLINEITEM=36
ROLE_SYSTEM_PAGETAB=37
ROLE_SYSTEM_PROPERTYPAGE=38
ROLE_SYSTEM_INDICATOR=39
ROLE_SYSTEM_GRAPHIC=40
ROLE_SYSTEM_STATICTEXT=41
ROLE_SYSTEM_TEXT=42
ROLE_SYSTEM_PUSHBUTTON=43
ROLE_SYSTEM_CHECKBUTTON=44
ROLE_SYSTEM_RADIOBUTTON=45
ROLE_SYSTEM_COMBOBOX=46
ROLE_SYSTEM_DROPLIST=47
ROLE_SYSTEM_PROGRESSBAR=48
ROLE_SYSTEM_DIAL=49
ROLE_SYSTEM_HOTKEYFIELD=50
ROLE_SYSTEM_SLIDER=51
ROLE_SYSTEM_SPINBUTTON=52
ROLE_SYSTEM_DIAGRAM=53
ROLE_SYSTEM_ANIMATION=54
ROLE_SYSTEM_EQUATION=55
ROLE_SYSTEM_BUTTONDROPDOWN=56
ROLE_SYSTEM_BUTTONMENU=57
ROLE_SYSTEM_BUTTONDROPDOWNGRID=58
ROLE_SYSTEM_WHITESPACE=59
ROLE_SYSTEM_PAGETABLIST=60
ROLE_SYSTEM_CLOCK=61
ROLE_SYSTEM_SPLITBUTTON=62
ROLE_SYSTEM_IPADDRESS=63
ROLE_SYSTEM_OUTLINEBUTTON=64
#IAccessible states
STATE_SYSTEM_UNAVAILABLE=0x1
STATE_SYSTEM_SELECTED=0x2
STATE_SYSTEM_FOCUSED=0x4
STATE_SYSTEM_PRESSED=0x8
STATE_SYSTEM_CHECKED=0x10
STATE_SYSTEM_MIXED=0x20
STATE_SYSTEM_READONLY=0x40
STATE_SYSTEM_HOTTRACKED=0x80
STATE_SYSTEM_DEFAULT=0x100
STATE_SYSTEM_EXPANDED=0x200
STATE_SYSTEM_COLLAPSED=0x400
STATE_SYSTEM_BUSY=0x800
STATE_SYSTEM_FLOATING=0x1000
STATE_SYSTEM_MARQUEED=0x2000
STATE_SYSTEM_ANIMATED=0x4000
STATE_SYSTEM_INVISIBLE=0x8000
STATE_SYSTEM_OFFSCREEN=0x10000
STATE_SYSTEM_SIZEABLE=0x20000
STATE_SYSTEM_MOVEABLE=0x40000
STATE_SYSTEM_SELFVOICING=0x80000
STATE_SYSTEM_FOCUSABLE=0x100000
STATE_SYSTEM_SELECTABLE=0x200000
STATE_SYSTEM_LINKED=0x400000
STATE_SYSTEM_TRAVERSED=0x800000
STATE_SYSTEM_MULTISELECTABLE=0x1000000
STATE_SYSTEM_EXTSELECTABLE=0x2000000
STATE_SYSTEM_ALERT_LOW=0x4000000
STATE_SYSTEM_ALERT_MEDIUM=0x8000000
STATE_SYSTEM_ALERT_HIGH=0x10000000
STATE_SYSTEM_PROTECTED=0x20000000
STATE_SYSTEM_HASPOPUP=0x40000000
STATE_SYSTEM_VALID=0x1fffffff

#Special Mozilla gecko MSAA constant additions
NAVRELATION_LABELLED_BY=0x1002
NAVRELATION_LABELLED_BY=0x1003
NAVRELATION_NODE_CHILD_OF=0x1005

import heapq
import itertools
import time
import struct
import weakref
from ctypes import *
from ctypes.wintypes import *
from comtypes.automation import *
from comtypes.server import *
from comtypes import GUID
import comtypes.client
import comtypes.client.lazybind
import Queue
from comInterfaces.Accessibility import *
from comInterfaces.IAccessible2Lib import *
from comInterfaces.servprov import *
import tones
import globalVars
from logHandler import log
import JABHandler
import eventHandler
import winKernel
import winUser
import speech
import sayAllHandler
import textHandler
import api
import queueHandler
import NVDAObjects.IAccessible
import appModuleHandler
import config
import mouseHandler
import controlTypes

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

	def addEvent(self,eventID,window,objectID,childID):
		"""Adds a winEvent to the limiter.
		@param eventID: the winEvent type
		@type eventID: integer
		@param window: the window handle of the winEvent
		@type window: integer
		@param objectID: the objectID of the winEvent
		@type objectID: integer
		@param childID: the childID of the winEvent
		@type childID: integer
		"""
		if eventID==winUser.EVENT_OBJECT_FOCUS:
			if objectID in (OBJID_SYSMENU,OBJID_MENU) and childID==0:
				# This is a focus event on a menu bar itself, which is just silly. Ignore it.
				return
			self._focusEventCache[(eventID,window,objectID,childID)]=next(self._eventCounter)
			return
		elif eventID==winUser.EVENT_OBJECT_SHOW:
			k=(winUser.EVENT_OBJECT_HIDE,window,objectID,childID)
			if k in self._genericEventCache:
				del self._genericEventCache[k]
				return
		elif eventID==winUser.EVENT_OBJECT_HIDE:
			k=(winUser.EVENT_OBJECT_SHOW,window,objectID,childID)
			if k in self._genericEventCache:
				del self._genericEventCache[k]
				return
		elif eventID==winUser.EVENT_OBJECT_DESTROY:
			k=(winUser.EVENT_OBJECT_CREATE,window,objectID,childID)
			if k in self._genericEventCache:
				del self._genericEventCache[k]
				return
		elif eventID in MENU_EVENTIDS:
			if self._lastMenuEvent:
				# We only care about the most recent menu event.
				del self._genericEventCache[self._lastMenuEvent]
			self._lastMenuEvent=(eventID,window,objectID,childID)
		self._genericEventCache[(eventID,window,objectID,childID)]=next(self._eventCounter)

	def flushEvents(self):
		"""Returns a list of winEvents (tuples of eventID,window,objectID,childID) that have been added, though due to limiting, it will not necessarily be all the winEvents that were originally added. They are definitely garenteed to be in the correct order though.
		"""
		g=self._genericEventCache
		self._genericEventCache={}
		self._lastMenuEvent=None
		for k,v in g.iteritems():
			heapq.heappush(self._eventHeap,(v,)+k)
		f=self._focusEventCache
		self._focusEventCache={}
		for k,v in sorted(f.iteritems(),key=lambda item: item[1])[0-self.maxFocusItems:]:
			heapq.heappush(self._eventHeap,(v,)+k)
		e=self._eventHeap
		self._eventHeap=[]
		r=[]
		for count in xrange(len(e)):
			r.append(heapq.heappop(e)[1:])
		return r

#The win event limiter for all winEvents
winEventLimiter=OrderedWinEventLimiter()

#A place to store live IAccessible NVDAObjects, that can be looked up by their window,objectID,childID event params.
liveNVDAObjectTable=weakref.WeakValueDictionary()

IAccessibleRolesToNVDARoles={
	ROLE_SYSTEM_WINDOW:controlTypes.ROLE_WINDOW,
	ROLE_SYSTEM_CLIENT:controlTypes.ROLE_PANE,
	ROLE_SYSTEM_TITLEBAR:controlTypes.ROLE_TITLEBAR,
	ROLE_SYSTEM_DIALOG:controlTypes.ROLE_DIALOG,
	ROLE_SYSTEM_PANE:controlTypes.ROLE_PANE,
	ROLE_SYSTEM_CHECKBUTTON:controlTypes.ROLE_CHECKBOX,
	ROLE_SYSTEM_RADIOBUTTON:controlTypes.ROLE_RADIOBUTTON,
	ROLE_SYSTEM_STATICTEXT:controlTypes.ROLE_STATICTEXT,
	ROLE_SYSTEM_TEXT:controlTypes.ROLE_EDITABLETEXT,
	ROLE_SYSTEM_PUSHBUTTON:controlTypes.ROLE_BUTTON,
	ROLE_SYSTEM_MENUBAR:controlTypes.ROLE_MENUBAR,
	ROLE_SYSTEM_MENUITEM:controlTypes.ROLE_MENUITEM,
	ROLE_SYSTEM_MENUPOPUP:controlTypes.ROLE_POPUPMENU,
	ROLE_SYSTEM_COMBOBOX:controlTypes.ROLE_COMBOBOX,
	ROLE_SYSTEM_LIST:controlTypes.ROLE_LIST,
	ROLE_SYSTEM_LISTITEM:controlTypes.ROLE_LISTITEM,
	ROLE_SYSTEM_GRAPHIC:controlTypes.ROLE_GRAPHIC,
	ROLE_SYSTEM_HELPBALLOON:controlTypes.ROLE_HELPBALLOON,
	ROLE_SYSTEM_TOOLTIP:controlTypes.ROLE_TOOLTIP,
	ROLE_SYSTEM_LINK:controlTypes.ROLE_LINK,
	ROLE_SYSTEM_OUTLINE:controlTypes.ROLE_TREEVIEW,
	ROLE_SYSTEM_OUTLINEITEM:controlTypes.ROLE_TREEVIEWITEM,
	ROLE_SYSTEM_OUTLINEBUTTON:controlTypes.ROLE_TREEVIEWITEM,
	ROLE_SYSTEM_PAGETAB:controlTypes.ROLE_TAB,
	ROLE_SYSTEM_PAGETABLIST:controlTypes.ROLE_TABCONTROL,
	ROLE_SYSTEM_SLIDER:controlTypes.ROLE_SLIDER,
	ROLE_SYSTEM_PROGRESSBAR:controlTypes.ROLE_PROGRESSBAR,
	ROLE_SYSTEM_SCROLLBAR:controlTypes.ROLE_SCROLLBAR,
	ROLE_SYSTEM_STATUSBAR:controlTypes.ROLE_STATUSBAR,
	ROLE_SYSTEM_TABLE:controlTypes.ROLE_TABLE,
	ROLE_SYSTEM_CELL:controlTypes.ROLE_TABLECELL,
	ROLE_SYSTEM_COLUMN:controlTypes.ROLE_TABLECOLUMN,
	ROLE_SYSTEM_ROW:controlTypes.ROLE_TABLEROW,
	ROLE_SYSTEM_TOOLBAR:controlTypes.ROLE_TOOLBAR,
	ROLE_SYSTEM_COLUMNHEADER:controlTypes.ROLE_TABLECOLUMNHEADER,
	ROLE_SYSTEM_ROWHEADER:controlTypes.ROLE_TABLEROWHEADER,
	ROLE_SYSTEM_SPLITBUTTON:controlTypes.ROLE_SPLITBUTTON,
	ROLE_SYSTEM_BUTTONDROPDOWN:controlTypes.ROLE_DROPDOWNBUTTON,
	ROLE_SYSTEM_SEPARATOR:controlTypes.ROLE_SEPARATOR,
	ROLE_SYSTEM_DOCUMENT:controlTypes.ROLE_DOCUMENT,
	ROLE_SYSTEM_ANIMATION:controlTypes.ROLE_ANIMATION,
	ROLE_SYSTEM_APPLICATION:controlTypes.ROLE_APPLICATION,
	ROLE_SYSTEM_GROUPING:controlTypes.ROLE_GROUPING,
	ROLE_SYSTEM_PROPERTYPAGE:controlTypes.ROLE_PROPERTYPAGE,
	ROLE_SYSTEM_ALERT:controlTypes.ROLE_ALERT,
	ROLE_SYSTEM_BORDER:controlTypes.ROLE_BORDER,
	ROLE_SYSTEM_BUTTONDROPDOWNGRID:controlTypes.ROLE_DROPDOWNBUTTONGRID,
	ROLE_SYSTEM_CARET:controlTypes.ROLE_CARET,
	ROLE_SYSTEM_CHARACTER:controlTypes.ROLE_CHARACTER,
	ROLE_SYSTEM_CHART:controlTypes.ROLE_CHART,
	ROLE_SYSTEM_CURSOR:controlTypes.ROLE_CURSOR,
	ROLE_SYSTEM_DIAGRAM:controlTypes.ROLE_DIAGRAM,
	ROLE_SYSTEM_DIAL:controlTypes.ROLE_DIAL,
	ROLE_SYSTEM_DROPLIST:controlTypes.ROLE_DROPLIST,
	ROLE_SYSTEM_BUTTONMENU:controlTypes.ROLE_MENUBUTTON,
	ROLE_SYSTEM_EQUATION:controlTypes.ROLE_EQUATION,
	ROLE_SYSTEM_GRIP:controlTypes.ROLE_GRIP,
	ROLE_SYSTEM_HOTKEYFIELD:controlTypes.ROLE_HOTKEYFIELD,
	ROLE_SYSTEM_INDICATOR:controlTypes.ROLE_INDICATOR,
	ROLE_SYSTEM_SPINBUTTON:controlTypes.ROLE_SPINBUTTON,
	ROLE_SYSTEM_SOUND:controlTypes.ROLE_SOUND,
	ROLE_SYSTEM_WHITESPACE:controlTypes.ROLE_WHITESPACE,
	ROLE_SYSTEM_IPADDRESS:controlTypes.ROLE_IPADDRESS,
	ROLE_SYSTEM_OUTLINEBUTTON:controlTypes.ROLE_TREEVIEWBUTTON,
	ROLE_SYSTEM_CLOCK:controlTypes.ROLE_CLOCK,
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
}

IAccessibleStatesToNVDAStates={
	STATE_SYSTEM_TRAVERSED:controlTypes.STATE_VISITED,
	STATE_SYSTEM_UNAVAILABLE:controlTypes.STATE_UNAVAILABLE,
	STATE_SYSTEM_FOCUSED:controlTypes.STATE_FOCUSED,
	STATE_SYSTEM_SELECTED:controlTypes.STATE_SELECTED,
	STATE_SYSTEM_BUSY:controlTypes.STATE_BUSY,
	STATE_SYSTEM_PRESSED:controlTypes.STATE_PRESSED,
	STATE_SYSTEM_CHECKED:controlTypes.STATE_CHECKED,
	STATE_SYSTEM_MIXED:controlTypes.STATE_HALFCHECKED,
	STATE_SYSTEM_READONLY:controlTypes.STATE_READONLY,
	STATE_SYSTEM_EXPANDED:controlTypes.STATE_EXPANDED,
	STATE_SYSTEM_COLLAPSED:controlTypes.STATE_COLLAPSED,
	STATE_SYSTEM_OFFSCREEN:controlTypes.STATE_OFFSCREEN,
	STATE_SYSTEM_INVISIBLE:controlTypes.STATE_INVISIBLE,
	STATE_SYSTEM_TRAVERSED:controlTypes.STATE_VISITED,
	STATE_SYSTEM_LINKED:controlTypes.STATE_LINKED,
	STATE_SYSTEM_HASPOPUP:controlTypes.STATE_HASPOPUP,
	STATE_SYSTEM_PROTECTED:controlTypes.STATE_PROTECTED,
	STATE_SYSTEM_SELECTABLE:controlTypes.STATE_SELECTABLE,
	STATE_SYSTEM_FOCUSABLE:controlTypes.STATE_FOCUSABLE,
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
}

#A list to store handles received from setWinEventHook, for use with unHookWinEvent  
winEventHookIDs=[]

eventCounter=itertools.count()
eventHeap=[]

def normalizeIAccessible(pacc):
	if isinstance(pacc,comtypes.client.lazybind.Dispatch) or isinstance(pacc,comtypes.client.dynamic._Dispatch) or isinstance(pacc,IUnknown):
		pacc=pacc.QueryInterface(IAccessible)
	elif not isinstance(pacc,IAccessible):
		raise ValueError("pacc %s is not, or can not be converted to, an IAccessible"%str(pacc))
	if not isinstance(pacc,IAccessible2):
		try:
			s=pacc.QueryInterface(IServiceProvider)
			i=s.QueryService(byref(IAccessible._iid_),byref(IAccessible2._iid_))
			pacc=POINTER(IAccessible2)(i)
		except:
			pass
	return pacc

def accessibleObjectFromWindow(window,objectID):
	if not winUser.isWindow(window):
		return None
	ptr=POINTER(IAccessible)()
	res=windll.oleacc.AccessibleObjectFromWindow(window,objectID,byref(IAccessible._iid_),byref(ptr))
	if res==0:
		return normalizeIAccessible(ptr)
	else:
		return None

def accessibleObjectFromEvent(window,objectID,childID):
	if not winUser.isWindow(window):
		return None
	pacc=POINTER(IAccessible)()
	varChild=VARIANT()
	res=windll.oleacc.AccessibleObjectFromEvent(window,objectID,childID,byref(pacc),byref(varChild))
	if res==0:
		child=varChild.value
		return (normalizeIAccessible(pacc),child)
	else:
		return None

def accessibleObjectFromPoint(x,y):
	point=POINT(x,y)
	pacc=POINTER(IAccessible)()
	varChild=VARIANT()
	res=windll.oleacc.AccessibleObjectFromPoint(point,byref(pacc),byref(varChild))
	if res==0:
		if not isinstance(varChild.value,int):
			child=0
		else:
			child=varChild.value
		return (normalizeIAccessible(pacc),child)

def windowFromAccessibleObject(ia):
	hwnd=c_int()
	try:
		res=windll.oleacc.WindowFromAccessibleObject(ia,byref(hwnd))
	except:
		res=0
	if res==0:
		return hwnd.value
	else:
		return 0

def accessibleChildren(ia,startIndex,numChildren):
	children=(VARIANT*numChildren)()
	realCount=c_int()
	windll.oleacc.AccessibleChildren(ia,startIndex,numChildren,children,byref(realCount))
	children=[x.value for x in children[0:realCount.value]]
	for childNum in xrange(len(children)):
		if isinstance(children[childNum],comtypes.client.lazybind.Dispatch) or isinstance(children[childNum],comtypes.client.dynamic._Dispatch) or isinstance(children[childNum],IUnknown):
			children[childNum]=(normalizeIAccessible(children[childNum]),0)
		elif isinstance(children[childNum],int):
			children[childNum]=(ia,children[childNum])
	return children

def getRoleText(role):
	textLen=windll.oleacc.GetRoleTextW(role,0,0)
	if textLen:
		buf=create_unicode_buffer(textLen+2)
		windll.oleacc.GetRoleTextW(role,buf,textLen+1)
		return buf.value
	else:
		return None

def getStateText(state):
	textLen=windll.oleacc.GetStateTextW(state,0,0)
	if textLen:
		buf=create_unicode_buffer(textLen+2)
		windll.oleacc.GetStateTextW(state,buf,textLen+1)
		return buf.value
	else:
		return None

def accName(ia,child):
	try:
		return ia.accName(child)
	except:
		return ""

def accValue(ia,child):
	try:
		return ia.accValue(child)
	except:
		return ""

def accRole(ia,child):
	try:
		return ia.accRole(child)
	except:
		return 0

def accState(ia,child):
	try:
		return ia.accState(child)
	except:
		return 0

def accDescription(ia,child):
	try:
		return ia.accDescription(child)
	except:
		return ""

def accHelp(ia,child):
	try:
		return ia.accHelp(child)
	except:
		return ""

def accKeyboardShortcut(ia,child):
	try:
		return ia.accKeyboardShortcut(child)
	except:
		return ""

def accDoDefaultAction(ia,child):
	try:
		ia.accDoDefaultAction(child)
	except:
		pass

def accSelect(ia,child,flags):
		ia.accSelect(flags,child)

def accFocus(ia):
	try:
		res=ia.accFocus
		if isinstance(res,comtypes.client.lazybind.Dispatch) or isinstance(res,comtypes.client.dynamic._Dispatch) or isinstance(res,IUnknown):
			new_ia=normalizeIAccessible(res)
			new_child=0
		elif isinstance(res,int):
			new_ia=ia
			new_child=res
		else:
			return None
		return (new_ia,new_child)
	except:
		return None

def accHitTest(ia,child,x,y):
	try:
		res=ia.accHitTest(x,y)
		if isinstance(res,comtypes.client.lazybind.Dispatch) or isinstance(res,comtypes.client.dynamic._Dispatch) or isinstance(res,IUnknown):
			new_ia=normalizeIAccessible(res)
			new_child=0
		elif isinstance(res,int) and res!=child:
			new_ia=ia
			new_child=res
		else:
			return None
		return (new_ia,new_child)
	except:
		return None

def accChild(ia,child):
	try:
		res=ia.accChild(child)
		if isinstance(res,comtypes.client.lazybind.Dispatch) or isinstance(res,comtypes.client.dynamic._Dispatch) or isinstance(res,IUnknown):
			new_ia=normalizeIAccessible(res)
			new_child=0
		elif isinstance(res,int):
			new_ia=ia
			new_child=res
		return (new_ia,new_child)
	except:
		return None

def accChildCount(ia):
	try:
		count=ia.accChildCount
	except:
		count=0
	return count

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


def accLocation(ia,child):
	try:
		return ia.accLocation(child)
	except:
		return None

winEventIDsToNVDAEventNames={
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
winUser.EVENT_OBJECT_DESTROY:"destroy",
winUser.EVENT_OBJECT_HIDE:"hide",
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
	#We can't handle MSAA create events. (Destroys are handled elsewhere.)
	if eventID == winUser.EVENT_OBJECT_CREATE:
		return None
	#Handle the special MSAA caret object's locationChange and show events as 'caret' events for the focus object
	NVDAEventName=winEventIDsToNVDAEventNames.get(eventID,None)
	if not NVDAEventName:
		return None
	#Ignore any events with invalid window handles
	if not window or not winUser.isWindow(window):
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
	return (NVDAEventName,obj)

def winEventCallback(handle,eventID,window,objectID,childID,threadID,timestamp):
	try:
		#ignore  particular objectIDs as we do not support them in winEvents
		if objectID in (OBJID_SOUND,OBJID_ALERT,OBJID_NATIVEOM):
			return


		#Change window objIDs to client objIDs for better reporting of objects
		if (objectID==0) and (childID==0):
			objectID=OBJID_CLIENT
		#Ignore events with invalid window handles
		isWindow = winUser.isWindow(window) if window else 0
		if window==0 or (not isWindow and eventID in (winUser.EVENT_SYSTEM_SWITCHSTART,winUser.EVENT_SYSTEM_SWITCHEND,winUser.EVENT_SYSTEM_MENUEND,winUser.EVENT_SYSTEM_MENUPOPUPEND)):
			window=winUser.getDesktopWindow()
		elif not isWindow:
			return
		windowClassName=winUser.getClassName(window)
		#At the moment we can't handle show, hide or reorder events on Mozilla Firefox Location bar,as there are just too many of them
		#Ignore show, hide and reorder on MozillaDropShadowWindowClass windows.
		if windowClassName.startswith('Mozilla') and eventID in (winUser.EVENT_OBJECT_SHOW,winUser.EVENT_OBJECT_HIDE,winUser.EVENT_OBJECT_REORDER) and childID<0:
			#Mozilla Gecko can sometimes fire win events on a catch-all window which isn't really the real window
			#Move up the ancestry to find the real mozilla Window and use that
			realWindow=window
			while realWindow and winUser.getClassName(realWindow)=="MozillaWindowClass":
				realWindow=winUser.getAncestor(realWindow,winUser.GA_PARENT)
			if winUser.getClassName(realWindow)=='MozillaDropShadowWindowClass':
				return
		winEventLimiter.addEvent(eventID,window,objectID,childID)
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
	if focus and objectID==OBJID_CARET and eventID in (winUser.EVENT_OBJECT_LOCATIONCHANGE,winUser.EVENT_OBJECT_SHOW):
		NVDAEvent=("caret",focus)
	else:
		NVDAEvent=winEventToNVDAEvent(eventID,window,objectID,childID)
		if not NVDAEvent:
			return False
	if NVDAEvent[0]=="nameChange" and objectID==OBJID_CURSOR:
		mouseHandler.updateMouseShape(NVDAEvent[1].name)
		return
	if NVDAEvent[1]==focus:
		NVDAEvent=(NVDAEvent[0],focus)
	eventHandler.queueEvent(*NVDAEvent)
	return True

def processFocusWinEvent(window,objectID,childID,needsFocusedState=True):
	"""checks to see if the focus win event is not the same as the existing focus, 
	then converts the win event to an NVDA event (instanciating an NVDA Object) then calls processFocusNVDAEvent. If all is ok it returns True.
	@type window: integer
	@param objectID: a win event's object ID
	@type objectID: integer
	@param childID: a win event's child ID
	@type childID: integer
	@param needsFocusedState: If true then the object or one of its ancestors, for this focus event *must* have state_focused.
	@type needsFocusedState: boolean
	@returns: True if the focus is valid and was handled, False otherwise.
	@rtype: boolean
	"""
	#Ignore focus events on invisible windows
	if not winUser.isWindowVisible(window):
		return False
	#Ignore focus  events on the parent of the desktop and taskbar
	windowClassName=winUser.getClassName(window)
	if windowClassName in ("Progman","Shell_TrayWnd"):
		return False
	rootWindow=winUser.getAncestor(window,winUser.GA_ROOT)
	# If this window's root window is not the foreground window and this window or its root window is not a popup window:
	if rootWindow!=winUser.getForegroundWindow() and not (winUser.getWindowStyle(window) & winUser.WS_POPUP or winUser.getWindowStyle(rootWindow)&winUser.WS_POPUP):
		# This is a focus event from a background window, so ignore it.
		return False
	oldFocus=eventHandler.lastQueuedFocusObject
	#If the existing focus has the same win event params as these, then ignore this event
	#However don't ignore if its SysListView32 and the childID is 0 as this could be a groupItem
	if isinstance(oldFocus,NVDAObjects.IAccessible.IAccessible)  and window==oldFocus.event_windowHandle and objectID==oldFocus.event_objectID and childID==oldFocus.event_childID and ("SysListView32" not in windowClassName or childID!=0 or objectID!=OBJID_CLIENT) :
		# Don't actually process the event, as it is the same as the current focus.
		# However, it is still a valid event, so return True.
		return True
	#Notify appModuleHandler of this new foreground window
	appModuleHandler.update(winUser.getWindowThreadProcessID(window)[0])
	#If Java access bridge is running, and this is a java window, then pass it to java and forget about it
	if JABHandler.isRunning and JABHandler.isJavaWindow(window):
		JABHandler.event_enterJavaWindow(window)
		return True
	#Convert the win event to an NVDA event
	NVDAEvent=winEventToNVDAEvent(winUser.EVENT_OBJECT_FOCUS,window,objectID,childID,useCache=False)
	if not NVDAEvent:
		return False
	eventName,obj=NVDAEvent
	if (childID==0 and obj.IAccessibleRole==ROLE_SYSTEM_LIST) or (objectID==OBJID_CLIENT and "SysListView32" in obj.windowClassName):
		# Some controls incorrectly fire focus on child ID 0, even when there is a child with focus.
		try:
			realChildID=obj.IAccessibleObject.accFocus
		except:
			realChildID=None
		if isinstance(realChildID,int) and realChildID>0 and realChildID!=childID:
			realObj=NVDAObjects.IAccessible.IAccessible(IAccessibleObject=obj.IAccessibleObject,IAccessibleChildID=realChildID,event_windowHandle=window,event_objectID=objectID,event_childID=realChildID)
			if realObj:
				obj=realObj
	return processFocusNVDAEvent(obj,needsFocusedState=needsFocusedState)

def processFocusNVDAEvent(obj,needsFocusedState=True):
	"""Processes a focus NVDA event.
	If the focus event is valid, it is queued.
	@param obj: the NVDAObject the focus event is for
	@type obj: L{NVDAObjects.NVDAObject}
	@param needsFocusedState: If true then the object or one of its ancestors, for this focus event *must* have state_focused.
	@type needsFocusedState: boolean
	@return: C{True} if the focus event is valid and was queued, C{False} otherwise.
	@rtype: boolean
	"""
	#this object, or one of its ancestors *must* have state_focused. Also cache the parents as we do this check
	if needsFocusedState and obj.windowClassName=="AVL_AVView" and obj.virtualBuffer:
		#Adobe acrobat document nodes don't have the focused state
		needsFocusedState=False
	elif needsFocusedState and obj.windowClassName.startswith("Mozilla") and obj.IAccessibleRole in (ROLE_SYSTEM_COMBOBOX, ROLE_SYSTEM_DOCUMENT, ROLE_SYSTEM_LIST):
		# The focused state is not set on certain Mozilla controls.
		needsFocusedState=False
	if needsFocusedState:
		testObj=obj
		while testObj:
			if controlTypes.STATE_FOCUSED in testObj.states:
				break
			parent=testObj.parent
			testObj.parent=parent
			testObj=parent
		if not testObj:
			return False
	eventHandler.queueEvent('gainFocus',obj)
	return True

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
	#Ignore foreground events on the parent of the desktop and taskbar
	if winUser.getClassName(window) in ("Progman","Shell_TrayWnd"):
		return False
	oldFocus=eventHandler.lastQueuedFocusObject
	#If this foreground win event's window is an ancestor of the existing focus's window, then ignore it
	if isinstance(oldFocus,NVDAObjects.IAccessible.IAccessible) and winUser.isDescendantWindow(window,oldFocus.windowHandle):
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

def processDestroyWinEvent(window,objectID,childID):
	"""Process a destroy win event.
	This removes the object associated with the event parameters from L{liveNVDAObjectTable} if such an object exists.
	"""
	try:
		del liveNVDAObjectTable[(window,objectID,childID)]
	except KeyError:
		pass

def processMenuStartWinEvent(eventID, window, objectID, childID, validFocus):
	"""Process a menuStart win event.
	@postcondition: Focus will be directed to the menu if appropriate.
	"""
	if validFocus:
		lastFocus=eventHandler.lastQueuedFocusObject
		if isinstance(lastFocus,NVDAObjects.IAccessible.IAccessible) and lastFocus.IAccessibleRole in (ROLE_SYSTEM_MENUPOPUP, ROLE_SYSTEM_MENUITEM):
			# Focus has already been set to a menu or menu item, so we don't need to handle the menuStart.
			return
	NVDAEvent = winEventToNVDAEvent(eventID, window, objectID, childID)
	if not NVDAEvent:
		return
	eventName, obj = NVDAEvent
	if obj.IAccessibleRole != ROLE_SYSTEM_MENUPOPUP:
		# menuStart on anything other than a menu is silly.
		return
	processFocusNVDAEvent(obj, needsFocusedState=False)

def processFakeFocusWinEvent(eventID, window, objectID, childID):
	"""Process a fake focus win event.
	@postcondition: The focus will be found and an event generated for it if appropriate.
	"""
	# A suitable event for faking the focus has been received with no focus event, so we probably need to find the focus and fake it.
	# However, it is possible that the focus event has simply been delayed, so wait a bit and only do it if the focus hasn't changed yet.
	import wx
	wx.CallLater(50, _fakeFocus, api.getFocusObject())

def _fakeFocus(oldFocus):
	if oldFocus is not api.getFocusObject():
		# The focus has changed - no need to fake it.
		return
	processFocusNVDAEvent(api.getDesktopObject().objectWithFocus())

#Register internal object event with IAccessible
cWinEventCallback=WINFUNCTYPE(c_voidp,c_int,c_int,c_int,c_int,c_int,c_int,c_int)(winEventCallback)

def initialize():
	focusObject=api.getDesktopObject().objectWithFocus()
	for eventType in winEventIDsToNVDAEventNames.keys():
		hookID=winUser.setWinEventHook(eventType,eventType,0,cWinEventCallback,0,0,0)
		if hookID:
			winEventHookIDs.append(hookID)
		else:
			log.error("initialize: could not register callback for event %s (%s)"%(eventType,winEventIDsToNVDAEventNames[eventType]))

def pumpAll():
	#Receive all the winEvents from the limiter for this cycle
	winEvents=winEventLimiter.flushEvents()
	focusWinEvents=[]
	validFocus=False
	fakeFocusEvent=None
	for winEvent in winEvents[0-MAX_WINEVENTS:]:
		#We want to only pass on one focus event to NVDA, but we always want to use the most recent possible one 
		if winEvent[0]==winUser.EVENT_OBJECT_FOCUS:
			focusWinEvents.append(winEvent)
			continue
		else:
			for focusWinEvent in reversed(focusWinEvents):
				if processFocusWinEvent(*(focusWinEvent[1:])):
					validFocus=True
					break
			focusWinEvents=[]
			if winEvent[0]==winUser.EVENT_SYSTEM_FOREGROUND:
				processForegroundWinEvent(*(winEvent[1:]))
			elif winEvent[0]==winUser.EVENT_OBJECT_DESTROY:
				processDestroyWinEvent(*winEvent[1:])
			elif winEvent[0] in MENU_EVENTIDS+(winUser.EVENT_SYSTEM_SWITCHEND,):
				# If there is no valid focus event, we may need to use this to fake the focus later.
				fakeFocusEvent=winEvent
			else:
				processGenericWinEvent(*winEvent)
	for focusWinEvent in reversed(focusWinEvents):
		if processFocusWinEvent(*(focusWinEvent[1:])):
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
	stringPtr=cast(stringPtr,POINTER(c_char*stringSize))
	identityString=stringPtr.contents.raw
	fields=struct.unpack('IIiI',identityString)
	d={}
	d['childID']=fields[3]
	if fields[0]&2:
		d['menuHandle']=fields[2]
	else:
		d['objectID']=fields[2]
		d['windowHandle']=fields[1]
	return d

def findGroupboxObject(obj):
	prevWindow=winUser.getPreviousWindow(obj.windowHandle)
	while prevWindow:
		if winUser.getClassName(prevWindow)=="Button" and winUser.getWindowStyle(prevWindow)&winUser.BS_GROUPBOX:
			groupObj=NVDAObjects.IAccessible.getNVDAObjectFromEvent(prevWindow,OBJID_CLIENT,0)
			try:
				(left,top,width,height)=obj.location
				(groupLeft,groupTop,groupWidth,groupHeight)=groupObj.location
			except:
				return
			if groupObj.IAccessibleRole==ROLE_SYSTEM_GROUPING and left>=groupLeft and (left+width)<=(groupLeft+groupWidth) and top>=groupTop and (top+height)<=(groupTop+groupHeight):
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
	for i in range(len(text)):
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
				# This attribute had subattributes.
				# Add the last subattribute key/value pair to the dict.
				subattr[subkey] = tmp
				# Add the key/subattribute pair to the dict.
				attribsDict[key] = subattr
				subkey = ""
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
		# This attribute had subattributes.
		# Add the last subattribute key/value pair to the dict.
		subattr[subkey] = tmp
		# Add the key/subattribute pair to the dict.
		attribsDict[key] = subattr
	elif key:
		# Add this key/value pair to the dict.
		attribsDict[key] = tmp
	return attribsDict

def getProcessHandleFromHwnd(windowHandle):
	"""Retreaves a process handle of the process who owns the window.
	If Windows Vista, uses GetProcessHandleFromHwnd found in oleacc.dll which allows a client with UIAccess to open a process who is elevated.
	if older than Windows Vista, just uses OpenProcess from user32.dll instead.
	@param windowHandle: a window of a process you wish to retreave a process handle for
	@type windowHandle: integer
	@returns: a process handle with read, write and operation access
	@rtype: integer
	"""
	try:
		return oledll.oleacc.GetProcessHandleFromHwnd(windowHandle)
	except:
		return winKernel.openProcess(winKernel.PROCESS_VM_READ|winKernel.PROCESS_VM_WRITE|winKernel.PROCESS_VM_OPERATION,False,winUser.getWindowThreadProcessID(windowHandle)[0])
