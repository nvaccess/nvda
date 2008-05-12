#IAccessiblehandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from __future__ import with_statement

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
STATE_SYSTEM_HASSUBMENU=0x4000000
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
import comtypes.client
import Queue
from comInterfaces.Accessibility import *
from comInterfaces.IAccessible2Lib import *
from comInterfaces.servprov import *
import tones
import globalVars
import JABHandler
import eventHandler
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

_IA2Dll=None
_IA2ClassFactory=None
_IA2RegCooky=None

class OrderedWinEventLimiter(object):
	"""Collects and limits winEvents based on whether they are property changes, focus changes, or just generic (all other ones).
	Only allow a max of L{maxFocusItems}, if more are added then the oldest focus event is removed to make room.
	Only allow one property change for one specific object at a time, though push it further forward in time if a duplicate tries to get added.
 	"""

	def __init__(self,maxFocusItems=3):
		"""
		@param maxFocusItems: the amount of focus changed events allowed to be queued.
		@type maxFocusItems: integer
		"""
		self._maxFocusItems=maxFocusItems
		self._focusEventCache={}
		self._genericEventCache={}
		self._eventHeap=[]
		self._eventCounter=itertools.count()

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
			self._focusEventCache[(eventID,window,objectID,childID)]=self._eventCounter.next()
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
		elif eventID==winUser.EVENT_OBJECT_CREATE:
			k=(winUser.EVENT_OBJECT_DESTROY,window,objectID,childID)
			if k in self._genericEventCache:
				del self._genericEventCache[k]
				return
		elif eventID==winUser.EVENT_OBJECT_DESTROY:
			k=(winUser.EVENT_OBJECT_CREATE,window,objectID,childID)
			if k in self._genericEventCache:
				del self._genericEventCache[k]
				return
		else:
			self._genericEventCache[(eventID,window,objectID,childID)]=self._eventCounter.next()

	def flushEvents(self):
		"""Returns a list of winEvents (tuples of eventID,window,objectID,childID) that have been added, though due to limiting, it will not necessarily be all the winEvents that were originally added. They are definitely garenteed to be in the correct order though.
		"""
		g=self._genericEventCache
		self._genericEventCache={}
		for k,v in g.iteritems():
			heapq.heappush(self._eventHeap,(v,)+k)
		f=self._focusEventCache
		self._focusEventCache={}
		for k,v in sorted(f.iteritems())[-4:]:
			heapq.heappush(self._eventHeap,(v,)+k)
		e=self._eventHeap
		self._eventHeap=[]
		r=[]
		for count in xrange(len(e)):
			r.append(heapq.heappop(e)[1:])
		return r

#The win event limiter for all winEvents
winEventLimiter=OrderedWinEventLimiter()

#A place to store live IAccessible NVDAObjects, that can be looked up by their window,objectID,childID event params, or special usage strings, like 'focus' or 'foreground' etc.
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
	STATE_SYSTEM_INVISIBLE:controlTypes.STATE_INVISIBLE,
	STATE_SYSTEM_TRAVERSED:controlTypes.STATE_VISITED,
	STATE_SYSTEM_LINKED:controlTypes.STATE_LINKED,
	STATE_SYSTEM_HASPOPUP:controlTypes.STATE_HASPOPUP,
	STATE_SYSTEM_HASSUBMENU:controlTypes.STATE_HASPOPUP,
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
}

#A list to store handles received from setWinEventHook, for use with unHookWinEvent  
winEventHookIDs=[]

eventCounter=itertools.count()
eventHeap=[]

def normalizeIAccessible(pacc):
	if isinstance(pacc,comtypes.client.dynamic._Dispatch) or isinstance(pacc,IUnknown):
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
		if isinstance(children[childNum],comtypes.client.dynamic._Dispatch) or isinstance(children[childNum],IUnknown):
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
		if isinstance(res,comtypes.client.dynamic._Dispatch) or isinstance(res,IUnknown):
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
		if isinstance(res,comtypes.client.dynamic._Dispatch) or isinstance(res,IUnknown):
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
		if isinstance(res,comtypes.client.dynamic._Dispatch) or isinstance(res,IUnknown):
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
			if isinstance(res,comtypes.client.dynamic._Dispatch) or isinstance(res,IUnknown):
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
		elif isinstance(res,comtypes.client.dynamic._Dispatch) or isinstance(res,IUnknown):
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
winUser.EVENT_SYSTEM_FOREGROUND:"foreground",
winUser.EVENT_SYSTEM_ALERT:"alert",
winUser.EVENT_SYSTEM_MENUSTART:"menuStart",
winUser.EVENT_SYSTEM_MENUEND:"menuEnd",
winUser.EVENT_SYSTEM_MENUPOPUPSTART:"menuStart",
winUser.EVENT_SYSTEM_MENUPOPUPEND:"menuEnd",
winUser.EVENT_SYSTEM_SCROLLINGSTART:"scrollingStart",
winUser.EVENT_SYSTEM_SWITCHSTART:"switchStart",
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

def winEventToNVDAEvent(eventID,window,objectID,childID):
	"""Tries to convert a win event ID to an NVDA event name, and instanciate or fetch an NVDAObject for the win event parameters.
	@param eventID: the win event ID (type)
	@type eventID: integer
	@param window: the win event's window handle
	@type window: integer
	@param objectID: the win event's object ID
	@type objectID: integer
	@param childID: the win event's childID
	@type childID: the win event's childID
	@returns: the NVDA event name and the NVDAObject the event is for
	@rtype: boolean of string and L{NVDAObject.IAccessible.IAccessible}
	"""
	neededCreation=True #used to track if we were able to use a previously instanciated object instead
	#We can't handle MSAA create and destroy events.
	if eventID in (winUser.EVENT_OBJECT_CREATE,winUser.EVENT_OBJECT_DESTROY):
		return None
	#Handle the special MSAA caret object's locationChange and show events as 'caret' events for the focus object
	NVDAEventName=winEventIDsToNVDAEventNames.get(eventID,None)
	if not NVDAEventName:
		return None
	#Ignore any events with invalid window handles
	if not window or not winUser.isWindow(window):
		return None
	obj=None
	#See if we already know an object by this win event info
	obj=liveNVDAObjectTable.get((window,objectID,childID),None)
	if obj:
		neededCreation=False
	#If we don't yet have the object, then actually instanciate it.
	if not obj: 
		obj=NVDAObjects.IAccessible.getNVDAObjectFromEvent(window,objectID,childID)
	#At this point if we don't have an object then we can't do any more
	if not obj:
		return None
	return (NVDAEventName,obj)

def winEventCallback(handle,eventID,window,objectID,childID,threadID,timestamp):
	try:
		#Change window objIDs to client objIDs for better reporting of objects
		if (objectID==0) and (childID==0):
			objectID=OBJID_CLIENT
		#Ignore events with invalid window handles
		isWindow = winUser.isWindow(window) if window else 0
		if not isWindow and eventID in (winUser.EVENT_SYSTEM_SWITCHSTART,winUser.EVENT_SYSTEM_SWITCHEND,winUser.EVENT_SYSTEM_MENUEND,winUser.EVENT_SYSTEM_MENUPOPUPEND):
			window=winUser.getDesktopWindow()
		elif not isWindow:
			return
		windowClassName=winUser.getClassName(window)
		#At the moment we can't handle Gecko show, hide or reorder events as there are just too many of them
		if windowClassName.startswith('Mozilla') and eventID in (winUser.EVENT_OBJECT_SHOW,winUser.EVENT_OBJECT_HIDE,winUser.EVENT_OBJECT_REORDER) and childID<0:
			return
		winEventLimiter.addEvent(eventID,window,objectID,childID)
	except:
		globalVars.log.error("winEventCallback", exc_info=True)

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
	#Notify appModuleHandler of this new foreground window
	appModuleHandler.update(window)
	#Handle particular events for the special MSAA caret object just as if they were for the focus object
	focus=liveNVDAObjectTable.get('focus',None)
	if focus and objectID==OBJID_CARET and eventID in (winUser.EVENT_OBJECT_LOCATIONCHANGE,winUser.EVENT_OBJECT_SHOW):
		NVDAEvent=("caret",focus)
	else:
		NVDAEvent=winEventToNVDAEvent(eventID,window,objectID,childID)
		if not NVDAEvent:
			return False
	if NVDAEvent[1]==focus:
		NVDAEvent=(NVDAEvent[0],focus)
	queueHandler.queueFunction(queueHandler.eventQueue,eventHandler.manageEvent,*NVDAEvent)
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
	@returns: True if the focus was processed, False otherwise.
	@rtype: boolean
	"""
	#Ignore focus events on invisible windows
	if not winUser.isWindowVisible(window):
		return False
	#Ignore focus  events on the parent of the desktop and taskbar
	if winUser.getClassName(window) in ("Progman","Shell_TrayWnd"):
		return False
	oldFocus=liveNVDAObjectTable.get('focus',None)
	#If the existing focus has the same win event params as these, then ignore this event
	if oldFocus and window==oldFocus.event_windowHandle and objectID==oldFocus.event_objectID and childID==oldFocus.event_childID:
		return False
	#Notify appModuleHandler of this new foreground window
	appModuleHandler.update(window)
	#If Java access bridge is running, and this is a java window, then pass it to java and forget about it
	if JABHandler.isRunning and JABHandler.isJavaWindow(window):
		JABHandler.event_enterJavaWindow(window)
		return True
	#Convert the win event to an NVDA event
	NVDAEvent=winEventToNVDAEvent(winUser.EVENT_OBJECT_FOCUS,window,objectID,childID)
	if not NVDAEvent:
		return False
	return processFocusNVDAEvent(NVDAEvent[1],needsFocusedState=needsFocusedState)

def processFocusNVDAEvent(obj,needsFocusedState=True):
	"""Checks the given NVDAObject against the existing focus to make sure they are not equal.
	Queues the focus event.
	If the focus event is bad then it returns False, else it returns True.
	@param obj: the NVDAObject the focus event is for
	@type obj: L{NVDAObjects.NVDAObject}
	@param needsFocusedState: If true then the object or one of its ancestors, for this focus event *must* have state_focused.
	@type needsFocusedState: boolean
	"""
	oldFocus=liveNVDAObjectTable.get('focus',None)
	if oldFocus and obj==oldFocus:
		return False
	#this object, or one of its ancestors *must* have state_focused. Also cache the parents as we do this check
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
	liveNVDAObjectTable['focus']=obj
	queueHandler.queueFunction(queueHandler.eventQueue,api.setFocusObject,obj) #Eventually eventHandler will do that
	queueHandler.queueFunction(queueHandler.eventQueue,eventHandler.manageEvent,'gainFocus',obj)
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
	#Ignore foreground events on invisible windows
	#Ignore foreground events on the parent of the desktop and taskbar
	if winUser.getClassName(window) in ("Progman","Shell_TrayWnd"):
		return False
	oldFocus=liveNVDAObjectTable.get('focus',None)
	#If this foreground win event's window is an ancestor of the existing focus's window, then ignore it
	if oldFocus and winUser.isDescendantWindow(window,oldFocus.windowHandle):
		return False
	#If the existing focus has the same win event params as these, then ignore this event
	if oldFocus and window==oldFocus.event_windowHandle and objectID==oldFocus.event_objectID and childID==oldFocus.event_childID:
		return False
	#Notify appModuleHandler of this new foreground window
	appModuleHandler.update(window)
	#If Java access bridge is running, and this is a java window, then pass it to java and forget about it
	if JABHandler.isRunning and JABHandler.isJavaWindow(window):
		JABHandler.event_enterJavaWindow(window)
		return True
	#Convert the win event to an NVDA event
	NVDAEvent=winEventToNVDAEvent(winUser.EVENT_SYSTEM_FOREGROUND,window,objectID,childID)
	if not NVDAEvent:
		return False
	liveNVDAObjectTable['focus']=NVDAEvent[1]
	queueHandler.queueFunction(queueHandler.eventQueue,api.setFocusObject,NVDAEvent[1]) #Eventually eventHandler will do that
	queueHandler.queueFunction(queueHandler.eventQueue,api.setForegroundObject,NVDAEvent[1]) #Eventually eventHandler will do that
	queueHandler.queueFunction(queueHandler.eventQueue,speech.cancelSpeech)
	queueHandler.queueFunction(queueHandler.eventQueue,eventHandler.manageEvent,*NVDAEvent)
	return True

#Register internal object event with IAccessible
cWinEventCallback=CFUNCTYPE(c_voidp,c_int,c_int,c_int,c_int,c_int,c_int,c_int)(winEventCallback)

def initialize():
	global _IA2Dll, _IA2ClassFactory, _IA2RegCooky
	#Load the IA2 proxy dll
	_IA2Dll=oledll.LoadLibrary('lib/ia2.dll')
	#Instanciate a class object for the IA2 proxy dll
	punk=POINTER(IUnknown)()
	_IA2Dll.DllGetClassObject(byref(IAccessible2._iid_),byref(IUnknown._iid_),byref(punk))
	#Register this class object in this process
	regCooky=c_long()
	oledll.ole32.CoRegisterClassObject(byref(IAccessible2._iid_),punk,CLSCTX_LOCAL_SERVER,REGCLS_MULTIPLEUSE,byref(regCooky))
	_IA2RegCooky=regCooky.value
	#Register all the IAccessible2 interfaces we want to use in this process
	oledll.ole32.CoRegisterPSClsid(byref(IAccessible2._iid_),byref(IAccessible2._iid_))
	oledll.ole32.CoRegisterPSClsid(byref(IAccessibleAction._iid_),byref(IAccessible2._iid_))
	oledll.ole32.CoRegisterPSClsid(byref(IAccessibleApplication._iid_),byref(IAccessible2._iid_))
	oledll.ole32.CoRegisterPSClsid(byref(IAccessibleComponent._iid_),byref(IAccessible2._iid_))
	oledll.ole32.CoRegisterPSClsid(byref(IAccessibleEditableText._iid_),byref(IAccessible2._iid_))
	oledll.ole32.CoRegisterPSClsid(byref(IAccessibleHypertext._iid_),byref(IAccessible2._iid_))
	oledll.ole32.CoRegisterPSClsid(byref(IAccessibleImage._iid_),byref(IAccessible2._iid_))
	oledll.ole32.CoRegisterPSClsid(byref(IAccessibleRelation._iid_),byref(IAccessible2._iid_))
	oledll.ole32.CoRegisterPSClsid(byref(IAccessibleTable._iid_),byref(IAccessible2._iid_))
	oledll.ole32.CoRegisterPSClsid(byref(IAccessibleText._iid_),byref(IAccessible2._iid_))
	oledll.ole32.CoRegisterPSClsid(byref(IAccessibleValue._iid_),byref(IAccessible2._iid_))
	desktopObject=NVDAObjects.IAccessible.getNVDAObjectFromEvent(winUser.getDesktopWindow(),OBJID_CLIENT,0)
	if not isinstance(desktopObject,NVDAObjects.IAccessible.IAccessible):
		raise OSError("can not get desktop object")
	api.setDesktopObject(desktopObject)
	api.setForegroundObject(desktopObject)
	api.setFocusObject(desktopObject)
	api.setNavigatorObject(desktopObject)
	api.setMouseObject(desktopObject)
	foregroundObject=NVDAObjects.IAccessible.getNVDAObjectFromEvent(winUser.getForegroundWindow(),OBJID_CLIENT,0)
	if foregroundObject:
		api.setForegroundObject(foregroundObject)
		queueHandler.queueFunction(queueHandler.eventQueue,eventHandler.manageEvent,"gainFocus",foregroundObject)
	focusObject=api.findObjectWithFocus()
	if isinstance(focusObject,NVDAObjects.IAccessible.IAccessible):
		queueHandler.queueFunction(queueHandler.eventQueue,eventHandler.manageEvent,"gainFocus",focusObject)
	for eventType in winEventIDsToNVDAEventNames.keys():
		hookID=winUser.setWinEventHook(eventType,eventType,0,cWinEventCallback,0,0,0)
		if hookID:
			winEventHookIDs.append(hookID)
		else:
			globalVars.log.error("initialize: could not register callback for event %s (%s)"%(eventType,winEventIDsToNVDAEventNames[eventType]))

def pumpAll():
	#Receive all the winEvents from the limiter for this cycle
	winEvents=winEventLimiter.flushEvents()
	focusWinEvents=[]
	for winEvent in winEvents:
		#We want to only pass on one focus event to NVDA, but we always want to use the most recent possible one 
		if winEvent[0]==winUser.EVENT_OBJECT_FOCUS:
			focusWinEvents.append(winEvent)
			continue
		else:
			for focusWinEvent in reversed(focusWinEvents):
				if processFocusWinEvent(*(focusWinEvent[1:])):
					break
			focusWinEvents=[]
			if winEvent[0]==winUser.EVENT_SYSTEM_FOREGROUND:
				processForegroundWinEvent(*(winEvent[1:]))
			else:
				processGenericWinEvent(*winEvent)
	for focusWinEvent in reversed(focusWinEvents):
		if processFocusWinEvent(*(focusWinEvent[1:])):
			break

def terminate():
	for handle in winEventHookIDs:
		winUser.unhookWinEvent(handle)
	oledll.ole32.CoRevokeClassObject(_IA2RegCooky)


def getIAccIdentity(pacc,childID):
	stringPtr,stringSize=pacc.QueryInterface(IAccIdentity).getIdentityString(childID)
	stringPtr=cast(stringPtr,POINTER(c_char*stringSize))
	s=p.contents.raw
	fields=struct.unpack('IIII',s)
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

