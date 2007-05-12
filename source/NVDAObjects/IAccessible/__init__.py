#NVDAObjects/IAccessible.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import weakref
import re
import os
import tones
import time
import difflib
import ctypes
import comtypes.automation
import comtypesClient
import debug
import appModuleHandler
from keyUtils import sendKey, key 
import IAccessibleHandler
import winUser
import winKernel
import globalVars
import speech
import api
import config
import controlTypes
from NVDAObjects.window import Window
from NVDAObjects import NVDAObject

re_gecko_level=re.compile('.*L([0-9]+)')
re_gecko_position=re.compile('.*([0-9]+) of ([0-9]+)')
re_gecko_contains=re.compile('.*with ([0-9]+)')

def getNVDAObjectFromEvent(hwnd,objectID,childID):
	accHandle=IAccessibleHandler.accessibleObjectFromEvent(hwnd,objectID,childID)
	if not accHandle:
		return None
	(pacc,child)=accHandle
	obj=IAccessible(pacc,child,hwnd,objectID=objectID,origChildID=childID)
	return obj

def getNVDAObjectFromPoint(x,y):
	accHandle=IAccessibleHandler.accessibleObjectFromPoint(x,y)
	if not accHandle:
		return None
	(pacc,child)=accHandle
	obj=IAccessible(pacc,child)
	return obj

def processGeckoDescription(obj):
	if obj.windowClassName not in ["MozillaWindowClass","MozillaContentWindowClass","MozillaUIWindowClass","MozillaDialogClass"]:
		return
	rawDescription=obj.description
	if not isinstance(rawDescription,basestring):
		return
	if rawDescription.startswith('Description: '):
		obj.description=rawDescription[13:]
		return
	m=re_gecko_level.match(rawDescription)
	groups=m.groups() if m else []
	if len(groups)>=1:
		obj.level=int(groups[0])
	m=re_gecko_position.match(rawDescription)
	groups=m.groups() if m else []
	if len(groups)==2:
		obj.positionString=_("%s of %s")%(groups[0],groups[1])
	m=re_gecko_contains.match(rawDescription)
	groups=m.groups() if m else []
	if len(groups)>=1:
		obj.contains=_("%s items")%groups[0]
	obj.description=""

IAccessibleStatesToNVDAStates={
	IAccessibleHandler.STATE_SYSTEM_UNAVAILABLE:controlTypes.STATE_UNAVAILABLE,
	IAccessibleHandler.STATE_SYSTEM_SELECTED:controlTypes.STATE_SELECTED,
	IAccessibleHandler.STATE_SYSTEM_BUSY:controlTypes.STATE_BUSY,
	IAccessibleHandler.STATE_SYSTEM_PRESSED:controlTypes.STATE_PRESSED,
	IAccessibleHandler.STATE_SYSTEM_CHECKED:controlTypes.STATE_CHECKED,
	IAccessibleHandler.STATE_SYSTEM_MIXED:controlTypes.STATE_HALFCHECKED,
	IAccessibleHandler.STATE_SYSTEM_EXPANDED:controlTypes.STATE_EXPANDED,
	IAccessibleHandler.STATE_SYSTEM_INVISIBLE:controlTypes.STATE_INVISIBLE,
	IAccessibleHandler.STATE_SYSTEM_TRAVERSED:controlTypes.STATE_VISITED,
	IAccessibleHandler.STATE_SYSTEM_LINKED:controlTypes.STATE_LINKED,
	IAccessibleHandler.STATE_SYSTEM_HASPOPUP:controlTypes.STATE_HASPOPUP,
	IAccessibleHandler.STATE_SYSTEM_HASSUBMENU:controlTypes.STATE_HASPOPUP,
	IAccessibleHandler.STATE_SYSTEM_PROTECTED:controlTypes.STATE_PROTECTED,
}

IAccessibleRolesToNVDARoles={
	IAccessibleHandler.ROLE_SYSTEM_WINDOW:controlTypes.ROLE_WINDOW,
	IAccessibleHandler.ROLE_SYSTEM_CLIENT:controlTypes.ROLE_WINDOW,
	IAccessibleHandler.ROLE_SYSTEM_TITLEBAR:controlTypes.ROLE_TITLEBAR,
	IAccessibleHandler.ROLE_SYSTEM_DIALOG:controlTypes.ROLE_DIALOG,
	IAccessibleHandler.ROLE_SYSTEM_PANE:controlTypes.ROLE_PANEL,
	IAccessibleHandler.ROLE_SYSTEM_CHECKBUTTON:controlTypes.ROLE_CHECKBOX,
	IAccessibleHandler.ROLE_SYSTEM_RADIOBUTTON:controlTypes.ROLE_RADIOBUTTON,
	IAccessibleHandler.ROLE_SYSTEM_STATICTEXT:controlTypes.ROLE_STATICTEXT,
	IAccessibleHandler.ROLE_SYSTEM_TEXT:controlTypes.ROLE_EDITABLETEXT,
	IAccessibleHandler.ROLE_SYSTEM_PUSHBUTTON:controlTypes.ROLE_BUTTON,
	IAccessibleHandler.ROLE_SYSTEM_MENUBAR:controlTypes.ROLE_MENUBAR,
	IAccessibleHandler.ROLE_SYSTEM_MENUITEM:controlTypes.ROLE_MENUITEM,
	IAccessibleHandler.ROLE_SYSTEM_MENUPOPUP:controlTypes.ROLE_POPUPMENU,
	IAccessibleHandler.ROLE_SYSTEM_COMBOBOX:controlTypes.ROLE_COMBOBOX,
	IAccessibleHandler.ROLE_SYSTEM_LIST:controlTypes.ROLE_LIST,
	IAccessibleHandler.ROLE_SYSTEM_LISTITEM:controlTypes.ROLE_LISTITEM,
	IAccessibleHandler.ROLE_SYSTEM_GRAPHIC:controlTypes.ROLE_GRAPHIC,
	IAccessibleHandler.ROLE_SYSTEM_HELPBALLOON:controlTypes.ROLE_HELPBALLOON,
	IAccessibleHandler.ROLE_SYSTEM_TOOLTIP:controlTypes.ROLE_TOOLTIP,
	IAccessibleHandler.ROLE_SYSTEM_LINK:controlTypes.ROLE_LINK,
	IAccessibleHandler.ROLE_SYSTEM_OUTLINE:controlTypes.ROLE_TREEVIEW,
	IAccessibleHandler.ROLE_SYSTEM_OUTLINEITEM:controlTypes.ROLE_TREEVIEWITEM,
	IAccessibleHandler.ROLE_SYSTEM_OUTLINEBUTTON:controlTypes.ROLE_TREEVIEWITEM,
	IAccessibleHandler.ROLE_SYSTEM_PAGETAB:controlTypes.ROLE_TAB,
	IAccessibleHandler.ROLE_SYSTEM_PAGETABLIST:controlTypes.ROLE_TABCONTROL,
	IAccessibleHandler.ROLE_SYSTEM_SLIDER:controlTypes.ROLE_SLIDER,
	IAccessibleHandler.ROLE_SYSTEM_PROGRESSBAR:controlTypes.ROLE_PROGRESSBAR,
	IAccessibleHandler.ROLE_SYSTEM_SCROLLBAR:controlTypes.ROLE_SCROLLBAR,
	IAccessibleHandler.ROLE_SYSTEM_STATUSBAR:controlTypes.ROLE_STATUSBAR,
	IAccessibleHandler.ROLE_SYSTEM_TABLE:controlTypes.ROLE_TABLE,
	IAccessibleHandler.ROLE_SYSTEM_CELL:controlTypes.ROLE_TABLECELL,
	IAccessibleHandler.ROLE_SYSTEM_COLUMN:controlTypes.ROLE_TABLECOLUMN,
	IAccessibleHandler.ROLE_SYSTEM_ROW:controlTypes.ROLE_TABLEROW,
	IAccessibleHandler.ROLE_SYSTEM_TOOLBAR:controlTypes.ROLE_TOOLBAR,
	IAccessibleHandler.ROLE_SYSTEM_COLUMNHEADER:controlTypes.ROLE_TABLECOLUMNHEADER,
	IAccessibleHandler.ROLE_SYSTEM_ROWHEADER:controlTypes.ROLE_TABLEROWHEADER,
	IAccessibleHandler.ROLE_SYSTEM_BUTTONDROPDOWN:controlTypes.ROLE_DROPDOWNBUTTON,
	IAccessibleHandler.ROLE_SYSTEM_SEPARATOR:controlTypes.ROLE_SEPARATOR,
	IAccessibleHandler.ROLE_SYSTEM_DOCUMENT:controlTypes.ROLE_DOCUMENT,
	IAccessibleHandler.ROLE_SYSTEM_ANIMATION:controlTypes.ROLE_ANIMATION,
	IAccessibleHandler.ROLE_SYSTEM_APPLICATION:controlTypes.ROLE_APPLICATION,
}

class IAccessible(Window):
	"""
the NVDAObject for IAccessible
@ivar IAccessibleChildID: the IAccessible object's child ID
@type IAccessibleChildID: int
"""

	def __new__(cls,pacc,childID,windowHandle=None,origChildID=None,objectID=None):
		"""
Checks the window class and IAccessible role against a map of IAccessible sub-types, and if a match is found, returns that rather than just IAccessible.
"""  
		if not windowHandle:
			windowHandle=IAccessibleHandler.windowFromAccessibleObject(pacc)
		windowClass=winUser.getClassName(windowHandle)
		try:
			objectRole=pacc.accRole(childID)
		except:
			objectRole=0
		classString=None
		if _staticMap.has_key((windowClass,objectRole)):
			classString=_staticMap[(windowClass,objectRole)]
		elif _staticMap.has_key((windowClass,None)):
			classString=_staticMap[(windowClass,None)]
		elif _staticMap.has_key((None,objectRole)):
			classString=_staticMap[(None,objectRole)]
		if classString is None:
			classString="IAccessible"
		if classString.find('.')>0:
			modString,classString=os.path.splitext(classString)
			classString=classString[1:]
			mod=__import__(modString,globals(),locals(),[])
			newClass=getattr(mod,classString)
		else:
			newClass=globals()[classString]
		obj=Window.__new__(newClass,windowHandle)
		obj.__init__(pacc,childID,windowHandle=windowHandle,origChildID=origChildID,objectID=objectID)
		return obj

	def __init__(self,pacc,childID,windowHandle=None,origChildID=None,objectID=None):
		"""
@param pacc: a pointer to an IAccessible object
@type pacc: ctypes.POINTER(IAccessible)
@param child: A child ID that will be used on all methods of the IAccessible pointer
@type child: int
@param hwnd: the window handle, if known
@type hwnd: int
@param objectID: the objectID for the IAccessible Object, if known
@type objectID: int
"""
		if hasattr(self,"_doneInit"):
			return
		self.IAccessibleObject=pacc
		self.IAccessibleChildID=childID
		self.IAccessibleObjectID=objectID
		self._accOrigChildID=origChildID
		Window.__init__(self,windowHandle)
		#Mozilla Gecko objects use the description property to report other info
		processGeckoDescription(self)
		self._doneInit=True

	def __hash__(self):
		l=self._hashLimit
		p=self._hashPrime
		h=NVDAObject.__hash__(self)
		h=(h+(hash(self.windowHandle)*p))%l
		h=(h+(hash(self.IAccessibleObjectID)*p))%l
		h=(h+(hash(self.IAccessibleChildID)*p))%l
		location=self.location
		if location is not None:
			for d in location:
				h=(h+(d*p))%l
		return h

		return h

	def _get_name(self):
		try:
			res=self.IAccessibleObject.accName(self.IAccessibleChildID)
		except:
			res=None
		return res if isinstance(res,basestring) and not res.isspace() else None

	def _get_value(self):
		try:
			res=self.IAccessibleObject.accValue(self.IAccessibleChildID)
		except:
			res=None
		return res if isinstance(res,basestring) and not res.isspace() else None

	def _get_IAccessibleRole(self):
		try:
			res=self.IAccessibleObject.accRole(self.IAccessibleChildID)
		except:
			return 0
		return res if (isinstance(res,basestring) or isinstance(res,int) or isinstance(res,float)) else ""

	def _get_role(self):
		return IAccessibleRolesToNVDARoles.get(self.IAccessibleRole,controlTypes.ROLE_UNKNOWN)

	def _get_IAccessibleStates(self):
		try:
			res=self.IAccessibleObject.accState(self.IAccessibleChildID)
		except:
			return 0
		return res if isinstance(res,int) else 0

	def _get_states(self):
		newStates=[]
		for state in api.createStateList(self.IAccessibleStates):
			if IAccessibleStatesToNVDAStates.has_key(state):
				newStates.append(IAccessibleStatesToNVDAStates[state])
		return frozenset(newStates)

	def _get_description(self):
		try:
			res=self.IAccessibleObject.accDescription(self.IAccessibleChildID)
		except:
			res=None
		return res if isinstance(res,basestring) and not res.isspace() else None

	def _get_keyboardShortcut(self):
		try:
			res=self.IAccessibleObject.accKeyboardShortcut(self.IAccessibleChildID)
		except:
			res=None
		return res if isinstance(res,basestring) and not res.isspace() else None

	def _get_childCount(self):
		count=IAccessibleHandler.accChildCount(self.IAccessibleObject)
		return count

	def _get_location(self):
		location=IAccessibleHandler.accLocation(self.IAccessibleObject,self.IAccessibleChildID)
		return location

	def _get_labeledBy(self):
		try:
			(pacc,accChild)=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVRELATION_LABELLED_BY)
			obj=IAccessible(pacc,accChild)
			return obj
		except:
			return None

	def _get_parent(self):
		res=IAccessibleHandler.accParent(self.IAccessibleObject,self.IAccessibleChildID)
		if res:
			(ia,child)=res
		else:
			return None
		obj=IAccessible(ia,child)
		if obj and (obj.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_WINDOW):
			return obj.parent
		else:
			return obj

	def _get_next(self):
		res=IAccessibleHandler.accParent(self.IAccessibleObject,self.IAccessibleChildID)
		if res:
			parentObject=IAccessible(res[0],res[1])
			parentRole=parentObject.IAccessibleRole
		else:
			parentObject=None
			parentRole=None
		if parentObject and (parentRole==IAccessibleHandler.ROLE_SYSTEM_WINDOW):
			obj=parentObject
		else:
			obj=self
		res=IAccessibleHandler.accNavigate(obj.IAccessibleObject,obj.IAccessibleChildID,IAccessibleHandler.NAVDIR_NEXT)
		if res:
			nextObject=IAccessible(res[0],res[1])
			if nextObject and (nextObject.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_WINDOW):
				nextObject=getNVDAObjectFromEvent(nextObject.windowHandle,-4,0)
			return nextObject if nextObject and nextObject.IAccessibleRole!=0 else None

	def _get_previous(self):
		res=IAccessibleHandler.accParent(self.IAccessibleObject,self.IAccessibleChildID)
		if res:
			parentObject=IAccessible(res[0],res[1])
			parentRole=parentObject.IAccessibleRole
		else:
			parentObject=None
			parentRole=None
		if parentObject and (parentRole==IAccessibleHandler.ROLE_SYSTEM_WINDOW):
			obj=parentObject
		else:
			obj=self
		res=IAccessibleHandler.accNavigate(obj.IAccessibleObject,obj.IAccessibleChildID,IAccessibleHandler.NAVDIR_PREVIOUS)
		if res:
			previousObject=IAccessible(res[0],res[1])
			if previousObject and (previousObject.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_WINDOW):
				previousObject=getNVDAObjectFromEvent(previousObject.windowHandle,-4,0)
			return previousObject

	def _get_firstChild(self):
		res=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVDIR_FIRSTCHILD)
		if res:
			obj=IAccessible(res[0],res[1])
		else:
			return None
		if obj and (obj.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_WINDOW):
			obj=getNVDAObjectFromEvent(obj.windowHandle,IAccessibleHandler.OBJID_CLIENT,0)
		if winUser.isDescendantWindow(self.windowHandle,obj.windowHandle) or self.windowHandle==winUser.getDesktopWindow():
			return obj
		else:
			return None

	def _get_children(self):
		childCount= self.childCount
		if childCount>0:
			children=[IAccessible(x[0],x[1]) for x in IAccessibleHandler.accessibleChildren(self.IAccessibleObject,0,childCount) if x]
			children=[(getNVDAObjectFromEvent(x.windowHandle,IAccessibleHandler.OBJID_CLIENT,0) if x and x.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_WINDOW else x) for x in children]
		else:
			child=self.firstChild
			children=[]
			while child:
				children.append(child)
				child=child.next
		children=[x for x in children if x and winUser.isDescendantWindow(self.windowHandle,x.windowHandle)]
		return children

	def doDefaultAction(self):
		IAccessibleHandler.accDoDefaultAction(self.IAccessibleObject,self.IAccessibleChildID)

	def _get_activeChild(self):
		res=IAccessibleHandler.accFocus(self.IAccessibleObject)
		if res:
			return IAccessible(res[0],res[1])

	def _get_hasFocus(self):
		if (self.IAccessibleStates&IAccessibleHandler.STATE_SYSTEM_FOCUSED):
			return True
		else:
			return False

	def setFocus(self):
		try:
			self.IAccessibleObject.accSelect(1,self.IAccessibleChildID)
		except:
			pass

	def _get_statusBar(self):
		statusWindow=ctypes.windll.user32.FindWindowExW(self.windowHandle,0,u'msctls_statusbar32',0)
		statusObject=getNVDAObjectFromEvent(statusWindow,IAccessibleHandler.OBJID_CLIENT,0)
		if not isinstance(statusObject,NVDAObject):
			return None 
		return statusObject

	def _get_positionString(self):
		position=""
		childID=self.IAccessibleChildID
		if childID>0:
			parent=self.parent
			if parent:
				parentChildCount=parent.childCount
				if parentChildCount>=childID:
					position=_("%s of %s")%(childID,parentChildCount)
		return position

	def event_show(self):
		if self.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_MENUPOPUP:
			self.event_menuStart()

	def event_mouseMove(self,isEntering,x,y,oldX,oldY):
		if isEntering:
			speech.cancelSpeech()
			speech.speakObject(self)

	def _get_groupName(self):
		if not api.getForegroundObject() or self == api.getForegroundObject() or api.getForegroundObject().IAccessibleRole != IAccessibleHandler.ROLE_SYSTEM_DIALOG or self.IAccessibleChildID != 0:
			return None
		try:
			curLocation=self.location
			groupObj=self
			while groupObj and (groupObj.IAccessibleRole!=IAccessibleHandler.ROLE_SYSTEM_GROUPING):
				groupObj=groupObj.previous
			if groupObj and groupObj.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_GROUPING:
				groupLocation=groupObj.location
				if curLocation and groupLocation and (curLocation[0]>=groupLocation[0]) and (curLocation[1]>=groupLocation[1]) and ((curLocation[0]+curLocation[2])<=(groupLocation[0]+groupLocation[2])) and ((curLocation[1]+curLocation[3])<=(groupLocation[1]+groupLocation[3])):
					return groupObj.name
			return None
		except:
			return None

	def speakDescendantObjects(self,hashList=None):
		if hashList is None:
			hashList=[]
		child=self.firstChild
		while child and winUser.isDescendantWindow(self.windowHandle,child.windowHandle):
			h=hash(child)
			if h not in hashList:
				hashList.append(h)
				speech.speakObject(child)
				child.speakDescendantObjects(hashList=hashList)
			child=child.next

	def event_gainFocus(self):
		if self.IAccessibleRole in [IAccessibleHandler.ROLE_SYSTEM_MENUITEM,IAccessibleHandler.ROLE_SYSTEM_MENUPOPUP,IAccessibleHandler.ROLE_SYSTEM_MENUBAR]:
			api.setMenuMode(True)
			speech.cancelSpeech()
		else:
			api.setMenuMode(False)
		Window.event_gainFocus(self)

	def event_menuStart(self):
		api.setMenuMode(True)
		focusObject=api.getFocusObject()
		parentObject=focusObject.parent if focusObject else None
		if self!=focusObject and self!=parentObject  and self.IAccessibleRole in [IAccessibleHandler.ROLE_SYSTEM_MENUITEM,IAccessibleHandler.ROLE_SYSTEM_MENUPOPUP]:
			api.setFocusObject(self)
			speech.cancelSpeech()
			if self.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_MENUPOPUP and focusObject.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_MENUITEM:
				speech.speakObject(self)
			else:
				speech.speakObject(self)

	def event_menuEnd(self):
		if self.IAccessibleRole not in [IAccessibleHandler.ROLE_SYSTEM_MENUITEM,IAccessibleHandler.ROLE_SYSTEM_MENUPOPUP] or self==api.getFocusObject():
			obj=api.findObjectWithFocus()
			if isinstance(obj,NVDAObject) and obj!=api.getFocusObject():
				api.setFocusObject(obj)
				speech.cancelSpeech()
				obj.event_gainFocus()

	def event_selection(self):
		return self.event_stateChange()

	def event_selectionAdd(self):
		return self.event_stateChange()

	def event_selectionRemove(self):
		return self.event_stateChange()

	def event_selectionWithIn(self):
		return self.event_stateChange()

class Dialog(IAccessible):
	"""
	Based on NVDAObject but on foreground events, the dialog contents gets read.
	"""

	def _get_role(self):
		return controlTypes.ROLE_DIALOG

	def _get_value(self):
		return None

	def event_foreground(self):
		super(Dialog,self).event_foreground()
		self.speakDescendantObjects()

class TrayClockWClass(IAccessible):
	"""
	Based on NVDAObject but the role is changed to clock.
	"""

	def _get_role(self):
		return controlTypes.ROLE_CLOCK

class Shell_TrayWnd_client(IAccessible):
	speakOnForeground=False
	speakOnGainFocus=False

class Progman_client(IAccessible):
	speakOnForeground=False
	speakOnGainFocus=False

class StaticText(IAccessible):

	def _get_role(self):
		return controlTypes.ROLE_STATICTEXT

	def _get_text_characterCount(self):
		return len(self.name)

	def text_getText(self,start=None,end=None):
		text=self.name
		start=start if isinstance(start,int) else 0
		end=end if isinstance(end,int) else len(self.name)
		return text[start:end]

[StaticText.bindKey(keyName,scriptName) for keyName,scriptName in [
	("extendedDown","text_review_nextLine"),
	("extendedUp","text_review_prevLine"),
	("extendedLeft","text_review_prevCharacter"),
	("extendedRight","text_review_nextCharacter"),
	("extendedHome","text_review_startOfLine"),
	("extendedEnd","text_review_endOfLine"),
	("control+extendedLeft","text_review_prevWord"),
	("control+extendedRight","text_review_nextWord"),
	("control+extendedHome","text_review_top"),
	("control+extendedEnd","text_review_bottom"),
]]

class OutlineItem(IAccessible):

	def _get_level(self):
		val=super(OutlineItem,self)._get_value()
		try:
			return int(val)
		except:
			return 0

	def _get_value(self):
		val=super(OutlineItem,self)._get_value()
		try:
			int(val)
		except:
			return val

class Tooltip(IAccessible):

	def event_show(self):
		if (config.conf["presentation"]["reportTooltips"] and (self.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_TOOLTIP)) or (config.conf["presentation"]["reportHelpBalloons"] and (self.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_HELPBALLOON)):
			speech.speakObject(self)

class ConsoleWindowClass(IAccessible):

	def event_nameChange(self):
		pass

class MozillaProgressBar(IAccessible):

	def event_valueChange(self):
		if config.conf["presentation"]["beepOnProgressBarUpdates"] and winUser.isDescendantWindow(winUser.getForegroundWindow(),self.windowHandle):
			val=self.value
			if val=="" or val is None:
				return
			if val!=globalVars.lastProgressValue:
				baseFreq=110
				tones.beep(int(baseFreq*(1+(float(val[:-1])/6.25))),40)
				globalVars.lastProgressValue=val
		else:
			super(MozillaProgressBar,self).event_valueChange()

class MozillaUIWindowClass(IAccessible):
	"""
	Based on NVDAObject, but on focus events, actions are performed whether or not the object really has focus.
	mozillaUIWindowClass objects sometimes do not set their focusable state properly.
	"""

	def __init__(self,*args,**vars):
		IAccessible.__init__(self,*args,**vars)
		self.needsFocusState=False

class MozillaUIWindowClass_application(MozillaUIWindowClass):
	"""
	Based on MozillaUIWindowClass, but:
	*Value is always empty because otherwise it is a long url to a .shul file that generated the mozilla application.
	*firstChild is the first child that is not a tooltip or a menu popup since these don't seem to allow getNext etc.
	*On focus events, the object is not spoken automatically since focus is given to this object when moving from one object to another.
	"""

	speakOnGainFocus=False

	def _get_value(self):
		return None

	def _get_firstChild(self):
		try:
			children=self.children
		except:
			return None
		for child in children:
			try:
				role=child.IAccessibleRole
				if role not in [IAccessibleHandler.ROLE_SYSTEM_TOOLTIP,IAccessibleHandler.ROLE_SYSTEM_MENUPOPUP]:
					return child
			except:
				pass

class MozillaDocument(IAccessible):

	def __init__(self,*args,**vars):
		IAccessible.__init__(self,*args,**vars)
		self.needsFocusState=False


	def _get_value(self):
		return 

class MozillaListItem(IAccessible):

	def _get_name(self):
		name=super(MozillaListItem,self)._get_name()
		if self.IAccessibleStates&IAccessibleHandler.STATE_SYSTEM_READONLY:
			children=super(MozillaListItem,self)._get_children()
			if len(children)>0 and (children[0].IAccessibleRole in ["bullet",IAccessibleHandler.ROLE_SYSTEM_STATICTEXT]):
				name=children[0].value
		return name

	def _get_children(self):
		children=super(MozillaListItem,self)._get_children()
		if self.IAccessibleStates&IAccessibleHandler.STATE_SYSTEM_READONLY and len(children)>0 and (children[0].IAccessibleRole in ["bullet",IAccesssibleHandler.ROLE_SYSTEM_STATICTEXT]):
			del children[0]
		return children

class MozillaText(IAccessible):

	def text_getText(self,start=None,end=None):
		return self.name

class SHELLDLL_DefView_client(IAccessible):

	speakOnGainFocus=False

class List(IAccessible):

	def _get_name(self):
		name=super(List,self)._get_name()
		if not name:
			name=super(IAccessible,self)._get_name()
		return name

	def _get_role(self):
		return controlTypes.ROLE_LIST

	def speakDescendantObjects(self,hashList=None):
		child=self.activeChild
		if child:
			speech.speakObject(child)

	def event_gainFocus(self):
		IAccessible.event_gainFocus(self)
		child=self.activeChild
		if child and (child.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_LISTITEM):
			IAccessibleHandler.objectEventCallback(-1,winUser.EVENT_OBJECT_FOCUS,self.windowHandle,self.IAccessibleObjectID,child.IAccessibleChildID,0,0)
		elif not self.firstChild:
			speech.speakMessage(_("%d items")%0)

class ComboBox(IAccessible):

	def speakDescendantObjects(self,hashList=None):
		child=self.activeChild
		if child:
			speech.speakObject(child)

class Outline(IAccessible):

	def speakDescendantObjects(self,hashList=None):
		child=self.activeChild
		if child:
			speech.speakObject(child)

class ProgressBar(IAccessible):

	def event_valueChange(self):
		if config.conf["presentation"]["beepOnProgressBarUpdates"]:
			val=self.value
			if val!=globalVars.lastProgressValue:
				baseFreq=110
				tones.beep(int(baseFreq*(1+(float(val[:-1])/6.25))),40)
				globalVars.lastProgressValue=val
		else:
			super(ProgressBar,self).event_valueChange()

class InternetExplorerClient(IAccessible):

	def _get_name(self):
		return None

	def _get_description(self):
		return None

class StatusBar(IAccessible):

	def _get_value(self):
		value=""
		for child in self.children:
			if child.name is not None:
				value+="  "+child.name
		return value

class SysLink(IAccessible):

	speakOnGainFocus=False

###class mappings

_staticMap={
	("Shell_TrayWnd",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"Shell_TrayWnd_client",
	("tooltips_class32",IAccessibleHandler.ROLE_SYSTEM_TOOLTIP):"Tooltip",
	("tooltips_class32",IAccessibleHandler.ROLE_SYSTEM_HELPBALLOON):"Tooltip",
	("Progman",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"Progman_client",
	(None,IAccessibleHandler.ROLE_SYSTEM_DIALOG):"Dialog",
	("TrayClockWClass",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"TrayClockWClass",
	("Edit",IAccessibleHandler.ROLE_SYSTEM_TEXT):"winEdit.WinEdit",
	("Static",IAccessibleHandler.ROLE_SYSTEM_STATICTEXT):"StaticText",
	("RichEdit20",IAccessibleHandler.ROLE_SYSTEM_TEXT):"richEdit.RichEdit",
	("RichEdit20A",IAccessibleHandler.ROLE_SYSTEM_TEXT):"richEdit.RichEdit",
	("RichEdit20W",IAccessibleHandler.ROLE_SYSTEM_TEXT):"richEdit.RichEdit",
	("RICHEDIT50W",IAccessibleHandler.ROLE_SYSTEM_TEXT):"richEdit.RichEdit",
	(None,IAccessibleHandler.ROLE_SYSTEM_OUTLINEITEM):"OutlineItem",
	("MozillaUIWindowClass",None):"MozillaUIWindowClass",
	("MozillaUIWindowClass",IAccessibleHandler.ROLE_SYSTEM_APPLICATION):"MozillaUIWindowClass_application",
	("MozillaDialogClass",IAccessibleHandler.ROLE_SYSTEM_ALERT):"Dialog",
	("MozillaDialogClass",IAccessibleHandler.ROLE_SYSTEM_DIALOG):"Dialog",
	("MozillaUIWindowClass",IAccessibleHandler.ROLE_SYSTEM_ALERT):"Dialog",
	("MozillaUIWindowClass",IAccessibleHandler.ROLE_SYSTEM_DIALOG):"Dialog",
	("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_ALERT):"Dialog",
	("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_DIALOG):"Dialog",
	("MozillaDialogClass",IAccessibleHandler.ROLE_SYSTEM_STATICTEXT):"StaticText",
	("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_STATICTEXT):"StaticText",
	("MozillaContentWindowClass",IAccessibleHandler.ROLE_SYSTEM_STATICTEXT):"StaticText",
	("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_TEXT):"MozillaText",
	("MozillaContentWindowClass",IAccessibleHandler.ROLE_SYSTEM_TEXT):"MozillaText",
	("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_LISTITEM):"MozillaListItem",
	("MozillaContentWindowClass",IAccessibleHandler.ROLE_SYSTEM_LISTITEM):"MozillaListItem",
	("MozillaContentWindowClass",IAccessibleHandler.ROLE_SYSTEM_DOCUMENT):"MozillaDocument",
	("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_DOCUMENT):"MozillaDocument",
	("MozillaContentWindowClass",IAccessibleHandler.ROLE_SYSTEM_PROGRESSBAR):"MozillaProgressBar",
	("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_PROGRESSBAR):"MozillaProgressBar",
	("ConsoleWindowClass",IAccessibleHandler.ROLE_SYSTEM_WINDOW):"ConsoleWindowClass",
	("ConsoleWindowClass",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"winConsole.WinConsole",
	("SHELLDLL_DefView",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"SHELLDLL_DefView_client",
	(None,IAccessibleHandler.ROLE_SYSTEM_LIST):"List",
	(None,IAccessibleHandler.ROLE_SYSTEM_COMBOBOX):"ComboBox",
	(None,IAccessibleHandler.ROLE_SYSTEM_OUTLINE):"Outline",
	("msctls_progress32",IAccessibleHandler.ROLE_SYSTEM_PROGRESSBAR):"ProgressBar",
	("Internet Explorer_Server",IAccessibleHandler.ROLE_SYSTEM_TEXT):"MSHTML.MSHTML",
	("Internet Explorer_Server",IAccessibleHandler.ROLE_SYSTEM_PANE):"MSHTML.MSHTML",
	("Internet Explorer_Server",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"InternetExplorerClient",
	("msctls_statusbar32",IAccessibleHandler.ROLE_SYSTEM_STATUSBAR):"StatusBar",
	("TTntEdit.UnicodeClass",IAccessibleHandler.ROLE_SYSTEM_TEXT):"winEdit.WinEdit",
	("TTntMemo.UnicodeClass",IAccessibleHandler.ROLE_SYSTEM_TEXT):"winEdit.WinEdit",
	("TRichViewEdit",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"winEdit.WinEdit",
	("TRichView",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"StaticText",
	("TRichEdit",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"richEdit.RichEdit",
	("TTntDrawGrid.UnicodeClass",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"List",
	("SysListView32",IAccessibleHandler.ROLE_SYSTEM_LISTITEM):"sysListView32.ListItem",
	("ATL:SysListView32",IAccessibleHandler.ROLE_SYSTEM_LISTITEM):"sysListView32.ListItem",
	("TWizardForm",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"Dialog",
	("SysLink",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"SysLink",
	("_WwG",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"winword.WordDocument",
	("EXCEL7",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"excel.ExcelGrid",
}
