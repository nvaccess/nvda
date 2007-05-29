#NVDAObjects/IAccessible.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import weakref
import re
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
import queueHandler
import config
import baseType
import window

re_gecko_level=re.compile('.*L([0-9]+)')
re_gecko_position=re.compile('.*([0-9]+) of ([0-9]+)')
re_gecko_contains=re.compile('.*with ([0-9]+)')

def getNVDAObjectFromEvent(hwnd,objectID,childID):
	accHandle=IAccessibleHandler.accessibleObjectFromEvent(hwnd,objectID,childID)
	if not accHandle:
		return None
	(pacc,child)=accHandle
	obj=NVDAObject_IAccessible(pacc,child,hwnd,objectID=objectID,origChildID=childID)
	return obj

def getNVDAObjectFromPoint(x,y):
	accHandle=IAccessibleHandler.accessibleObjectFromPoint(x,y)
	if not accHandle:
		return None
	(pacc,child)=accHandle
	obj=NVDAObject_IAccessible(pacc,child)
	return obj

def registerNVDAObjectClass(appModule,windowClass,objectRole,cls):
	_dynamicMap[(id(appModule),windowClass,objectRole)]=cls

def unregisterNVDAObjectClass(appModule,windowClass,objectRole):
	del _dynamicMap[(id(appModule),windowClass,objectRole)]

def processGeckoDescription(obj):
	if obj.windowClassName not in ["MozillaWindowClass","MozillaContentWindowClass","MozillaUIWindowClass","MozillaDialogClass"]:
		return
	rawDescription=obj.description
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

class NVDAObject_IAccessible(window.NVDAObject_window):
	"""
the NVDAObject for IAccessible
@ivar IAccessibleChildID: the IAccessible object's child ID
@type IAccessibleChildID: int
"""

	allowedPositiveStates=IAccessibleHandler.STATE_SYSTEM_UNAVAILABLE|IAccessibleHandler.STATE_SYSTEM_SELECTED|IAccessibleHandler.STATE_SYSTEM_PRESSED|IAccessibleHandler.STATE_SYSTEM_CHECKED|IAccessibleHandler.STATE_SYSTEM_MIXED|IAccessibleHandler.STATE_SYSTEM_EXPANDED|IAccessibleHandler.STATE_SYSTEM_COLLAPSED|IAccessibleHandler.STATE_SYSTEM_BUSY|IAccessibleHandler.STATE_SYSTEM_HASPOPUP

	def __new__(cls,pacc,childID,windowHandle=None,origChildID=None,objectID=None):
		"""
Checks the window class and IAccessible role against a map of NVDAObject_IAccessible sub-types, and if a match is found, returns that rather than just NVDAObject_IAccessible.
"""  
		if not windowHandle:
			windowHandle=IAccessibleHandler.windowFromAccessibleObject(pacc)
		windowClass=winUser.getClassName(windowHandle)
		try:
			objectRole=pacc.accRole(childID)
		except:
			objectRole=0
		newCls=None
		appModule=appModuleHandler.getAppModuleFromWindow(windowHandle)
		if appModule:
			appModuleRef=id(appModule)
			if _dynamicMap.has_key((appModuleRef,windowClass,objectRole)):
				newCls=_dynamicMap[(appModuleRef,windowClass,objectRole)]
			elif _dynamicMap.has_key((appModuleRef,windowClass,None)):
				newCls=_dynamicMap[(appModuleRef,windowClass,None)]
			elif _dynamicMap.has_key((appModuleRef,None,objectRole)):
				newCls=_dynamicMap[(appModuleRef,None,objectRole)]
		if newCls is None:
			if _staticMap.has_key((windowClass,objectRole)):
				newCls=_staticMap[(windowClass,objectRole)]
			elif _staticMap.has_key((windowClass,None)):
				newCls=_staticMap[(windowClass,None)]
			elif _staticMap.has_key((None,objectRole)):
				newCls=_staticMap[(None,objectRole)]
		if newCls is None:
			newCls=NVDAObject_IAccessible
		obj=window.NVDAObject_window.__new__(newCls,windowHandle)
		if appModule is not None:
			obj.appModule=weakref.ref(appModule)
		else:
			obj.appModule=lambda: None
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
		self._pacc=pacc
		self._accChild=childID
		self._accObjectID=objectID
		self._accOrigChildID=origChildID
		self._lastPositiveStates=self.calculatePositiveStates()
		self._lastNegativeStates=self.calculateNegativeStates()
		window.NVDAObject_window.__init__(self,windowHandle)
		#Mozilla Gecko objects use the description property to report other info
		processGeckoDescription(self)
		self._doneInit=True

	def __hash__(self):
		l=self._hashLimit
		p=self._hashPrime
		h=baseType.NVDAObject.__hash__(self)
		h=(h+(hash(self.windowHandle)*p))%l
		h=(h+(hash(self._accObjectID)*p))%l
		h=(h+(hash(self.IAccessibleChildID)*p))%l
		location=self.location
		if location is not None:
			for d in location:
				h=(h+(d*p))%l
		return h

		return h

	def _get_name(self):
		try:
			res=self._pacc.accName(self._accChild)
		except:
			return ""
		return res if isinstance(res,basestring) else ""

	def _get_value(self):
		try:
			res=self._pacc.accValue(self._accChild)
		except:
			return ""
		return res if (isinstance(res,basestring) or isinstance(res,int) or isinstance(res,float)) else ""

	def _get_role(self):
		try:
			res=self._pacc.accRole(self._accChild)
		except:
			return 0
		return res if (isinstance(res,basestring) or isinstance(res,int) or isinstance(res,float)) else ""

	def _get_typeString(self):
		role=self.role
		if role==IAccessibleHandler.ROLE_SYSTEM_CLIENT:
			role=IAccessibleHandler.ROLE_SYSTEM_WINDOW
		if config.conf["presentation"]["reportClassOfClientObjects"] and (role==IAccessibleHandler.ROLE_SYSTEM_WINDOW):
			typeString=self.windowClassName
		else:
			typeString=""
		return "%s %s"%(typeString,IAccessibleHandler.getRoleName(role))

	def _get_states(self):
		try:
			res=self._pacc.accState(self._accChild)
		except:
			return 0
		return res if isinstance(res,int) else 0

	def getStateName(self,state,opposite=False):
		if isinstance(state,int):
			newState=IAccessibleHandler.getStateText(state)
		else:
			newState=state
		if opposite:
			newState=_("not %s")%newState
		return newState

	def _get_description(self):
		try:
			res=self._pacc.accDescription(self._accChild)
		except:
			return ""
		return res if isinstance(res,basestring) else ""

	def _get_keyboardShortcut(self):
		try:
			res=self._pacc.accKeyboardShortcut(self._accChild)
		except:
			return ""
		return res if isinstance(res,basestring) else ""

	def _get_IAccessibleChildID(self):
		return self._accChild

	def _get_childCount(self):
		count=IAccessibleHandler.accChildCount(self._pacc)
		return count

	def _get_location(self):
		location=IAccessibleHandler.accLocation(self._pacc,self._accChild)
		return location

	def _get_labeledBy(self):
		try:
			(pacc,accChild)=IAccessibleHandler.accNavigate(self._pacc,self._accChild,IAccessibleHandler.NAVRELATION_LABELLED_BY)
			obj=NVDAObject_IAccessible(pacc,accChild)
			return obj
		except:
			return None

	def _get_parent(self):
		res=IAccessibleHandler.accParent(self._pacc,self._accChild)
		if res:
			(ia,child)=res
		else:
			return None
		obj=NVDAObject_IAccessible(ia,child)
		if obj and (obj.role==IAccessibleHandler.ROLE_SYSTEM_WINDOW):
			return obj.parent
		else:
			return obj

	def _get_next(self):
		res=IAccessibleHandler.accParent(self._pacc,self._accChild)
		if res:
			parentObject=NVDAObject_IAccessible(res[0],res[1])
			parentRole=parentObject.role
		else:
			parentObject=None
			parentRole=None
		if parentObject and (parentRole==IAccessibleHandler.ROLE_SYSTEM_WINDOW):
			obj=parentObject
		else:
			obj=self
		res=IAccessibleHandler.accNavigate(obj._pacc,obj._accChild,IAccessibleHandler.NAVDIR_NEXT)
		if res:
			nextObject=NVDAObject_IAccessible(res[0],res[1])
			if nextObject and (nextObject.role==IAccessibleHandler.ROLE_SYSTEM_WINDOW):
				nextObject=getNVDAObjectFromEvent(nextObject.windowHandle,-4,0)
			return nextObject if nextObject and nextObject.role!=0 else None

	def _get_previous(self):
		res=IAccessibleHandler.accParent(self._pacc,self._accChild)
		if res:
			parentObject=NVDAObject_IAccessible(res[0],res[1])
			parentRole=parentObject.role
		else:
			parentObject=None
			parentRole=None
		if parentObject and (parentRole==IAccessibleHandler.ROLE_SYSTEM_WINDOW):
			obj=parentObject
		else:
			obj=self
		res=IAccessibleHandler.accNavigate(obj._pacc,obj._accChild,IAccessibleHandler.NAVDIR_PREVIOUS)
		if res:
			previousObject=NVDAObject_IAccessible(res[0],res[1])
			if previousObject and (previousObject.role==IAccessibleHandler.ROLE_SYSTEM_WINDOW):
				previousObject=getNVDAObjectFromEvent(previousObject.windowHandle,-4,0)
			return previousObject

	def _get_firstChild(self):
		res=IAccessibleHandler.accNavigate(self._pacc,self._accChild,IAccessibleHandler.NAVDIR_FIRSTCHILD)
		if res:
			obj=NVDAObject_IAccessible(res[0],res[1])
		else:
			return None
		if obj and (obj.role==IAccessibleHandler.ROLE_SYSTEM_WINDOW):
			obj=getNVDAObjectFromEvent(obj.windowHandle,IAccessibleHandler.OBJID_CLIENT,0)
		if winUser.isDescendantWindow(self.windowHandle,obj.windowHandle) or self.windowHandle==winUser.getDesktopWindow():
			return obj
		else:
			return None

	def _get_children(self):
		childCount= self.childCount
		if childCount>0:
			children=[NVDAObject_IAccessible(x[0],x[1]) for x in IAccessibleHandler.accessibleChildren(self._pacc,0,childCount) if x]
			children=[(getNVDAObjectFromEvent(x.windowHandle,IAccessibleHandler.OBJID_CLIENT,0) if x and x.role==IAccessibleHandler.ROLE_SYSTEM_WINDOW else x) for x in children]
		else:
			child=self.firstChild
			children=[]
			while child:
				children.append(child)
				child=child.next
		children=[x for x in children if x and winUser.isDescendantWindow(self.windowHandle,x.windowHandle)]
		return children


	def doDefaultAction(self):
		IAccessibleHandler.accDoDefaultAction(self._pacc,self._accChild)

	def _get_activeChild(self):
		res=IAccessibleHandler.accFocus(self._pacc)
		if res:
			return NVDAObject_IAccessible(res[0],res[1])

	def _get_hasFocus(self):
		states=0
		states=self.states
		if (states&IAccessibleHandler.STATE_SYSTEM_FOCUSED):
			return True
		else:
			return False

	def setFocus(self):
		try:
			self._pacc.accSelect(1,self._accChild)
		except:
			pass


	def _get_statusBar(self):
		statusWindow=ctypes.windll.user32.FindWindowExW(self.windowHandle,0,u'msctls_statusbar32',0)
		statusObject=getNVDAObjectFromEvent(statusWindow,IAccessibleHandler.OBJID_CLIENT,0)
		if not isinstance(statusObject,baseType.NVDAObject):
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
		if self.role==IAccessibleHandler.ROLE_SYSTEM_MENUPOPUP:
			self.event_menuStart()

	def event_mouseMove(self,isEntering,x,y,oldX,oldY):
		if isEntering:
			speech.cancelSpeech()
			self.speakObject()

	def _get_groupName(self):
		try:
			curLocation=self.location
			groupObj=self
			while groupObj and (groupObj.role!=IAccessibleHandler.ROLE_SYSTEM_GROUPING):
				groupObj=groupObj.previous
			if groupObj and groupObj.role==IAccessibleHandler.ROLE_SYSTEM_GROUPING:
				groupLocation=groupObj.location
				if curLocation and groupLocation and (curLocation[0]>=groupLocation[0]) and (curLocation[1]>=groupLocation[1]) and ((curLocation[0]+curLocation[2])<=(groupLocation[0]+groupLocation[2])) and ((curLocation[1]+curLocation[3])<=(groupLocation[1]+groupLocation[3])):
					return groupObj.name
			return ""
		except:
			return ""

	def _get_isProtected(self):
		return bool(self.states&IAccessibleHandler.STATE_SYSTEM_PROTECTED)

	def speakDescendantObjects(self,hashList=None):
		if hashList is None:
			hashList=[]
		child=self.firstChild
		while child and winUser.isDescendantWindow(self.windowHandle,child.windowHandle):
			h=hash(child)
			if h not in hashList:
				hashList.append(h)
				child.speakObject()
				child.speakDescendantObjects(hashList=hashList)
			child=child.next

	def event_gainFocus(self):
		if self.role in [IAccessibleHandler.ROLE_SYSTEM_MENUITEM,IAccessibleHandler.ROLE_SYSTEM_MENUPOPUP,IAccessibleHandler.ROLE_SYSTEM_MENUBAR]:
			api.setMenuMode(True)
			speech.cancelSpeech()
		else:
			api.setMenuMode(False)
		if config.conf["presentation"]["reportObjectGroupNames"] and api.getForegroundObject() and (api.getForegroundObject().role==IAccessibleHandler.ROLE_SYSTEM_DIALOG) and (self.IAccessibleChildID==0): 
			groupName=self.groupName
			if groupName:
				speech.speakMessage("%s %s"%(groupName,IAccessibleHandler.getRoleName(IAccessibleHandler.ROLE_SYSTEM_GROUPING)))
		window.NVDAObject_window.event_gainFocus(self)

	def event_menuStart(self):
		api.setMenuMode(True)
		focusObject=api.getFocusObject()
		parentObject=focusObject.parent if focusObject else None
		if self!=focusObject and self!=parentObject  and self.role in [IAccessibleHandler.ROLE_SYSTEM_MENUITEM,IAccessibleHandler.ROLE_SYSTEM_MENUPOPUP]:
			api.setFocusObject(self)
			speech.cancelSpeech()
			if self.role==IAccessibleHandler.ROLE_SYSTEM_MENUPOPUP and focusObject.role==IAccessibleHandler.ROLE_SYSTEM_MENUITEM:
				speech.speakObjectProperties(name=focusObject.name,typeString=self.typeString)
			else:
				self.speakObject()

	def event_menuEnd(self):
		if self.role not in [IAccessibleHandler.ROLE_SYSTEM_MENUITEM,IAccessibleHandler.ROLE_SYSTEM_MENUPOPUP] or self==api.getFocusObject():
			obj=api.findObjectWithFocus()
			if isinstance(obj,baseType.NVDAObject) and obj!=api.getFocusObject():
				api.setFocusObject(obj)
				speech.cancelSpeech()
				obj.event_gainFocus()

	def event_stateChange(self):
		positiveStates=self.calculatePositiveStates()
		newPositiveStates=positiveStates-(positiveStates&self._lastPositiveStates)
		negativeStates=self.calculateNegativeStates()
		newNegativeStates=negativeStates-(negativeStates&self._lastNegativeStates)
		if self.hasFocus:
			if newPositiveStates:
				speech.speakObjectProperties(stateText=self.getStateNames(newPositiveStates))
			if newNegativeStates:
				speech.speakObjectProperties(stateText=self.getStateNames(newNegativeStates,opposite=True))
		self._lastPositiveStates=positiveStates
		self._lastNegativeStates=negativeStates

	def event_selection(self):
		return self.event_stateChange()

	def event_selectionAdd(self):
		return self.event_stateChange()

	def event_selectionRemove(self):
		return self.event_stateChange()

	def event_selectionWithIn(self):
		return self.event_stateChange()

class NVDAObject_dialog(NVDAObject_IAccessible):
	"""
	Based on NVDAObject but on foreground events, the dialog contents gets read.
	"""

	def _get_typeString(self):
		return IAccessibleHandler.getRoleName(IAccessibleHandler.ROLE_SYSTEM_DIALOG)

	def _get_value(self):
		return ""

	def event_foreground(self):
		super(NVDAObject_dialog,self).event_foreground()
		self.speakDescendantObjects()

class NVDAObject_TrayClockWClass(NVDAObject_IAccessible):
	"""
	Based on NVDAObject but the role is changed to clock.
	"""

	def _get_role(self):
		return IAccessibleHandler.ROLE_SYSTEM_CLOCK

class NVDAObject_Shell_TrayWnd_client(NVDAObject_IAccessible):
	speakOnForeground=False
	speakOnGainFocus=False

class NVDAObject_Progman_client(NVDAObject_IAccessible):
	speakOnForeground=False
	speakOnGainFocus=False

class NVDAObject_staticText(NVDAObject_IAccessible):

	def _get_typeString(self):
		return IAccessibleHandler.getRoleName(IAccessibleHandler.ROLE_SYSTEM_STATICTEXT)

	def _get_text_characterCount(self):
		return len(self.name)

	def text_getText(self,start=None,end=None):
		text=self.name
		start=start if isinstance(start,int) else 0
		end=end if isinstance(end,int) else len(self.name)
		return text[start:end]

[NVDAObject_staticText.bindKey(keyName,scriptName) for keyName,scriptName in [
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

class NVDAObject_checkBox(NVDAObject_IAccessible):
	"""
	Based on NVDAObject, but filterStates removes the pressed state for checkboxes.
	"""

	allowedPositiveStates=NVDAObject_IAccessible.allowedPositiveStates-(NVDAObject_IAccessible.allowedPositiveStates&IAccessibleHandler.STATE_SYSTEM_PRESSED)
	allowedNegativeStates=NVDAObject_IAccessible.allowedNegativeStates|IAccessibleHandler.STATE_SYSTEM_CHECKED

	def __init__(self,*args,**vars):
		NVDAObject_IAccessible.__init__(self,*args,**vars)
		self._lastPositiveStates=self.calculatePositiveStates()
		self._lastNegativeStates=self.calculateNegativeStates()

class NVDAObject_menuItem(NVDAObject_IAccessible):

	def reportFocus(self):
		positiveStates=self.calculatePositiveStates()
		positiveStates=positiveStates-(positiveStates&IAccessibleHandler.STATE_SYSTEM_SELECTED)
		negativeStates=self.calculateNegativeStates()
		stateText=" ".join([self.getStateNames(positiveStates),self.getStateNames(negativeStates,opposite=True)])
		speech.speakObjectProperties(name=self.name,stateText=stateText,value=self.value,description=self.description,keyboardShortcut=self.keyboardShortcut,position=self.positionString)

class NVDAObject_outlineItem(NVDAObject_IAccessible):

	def _get_level(self):
		val=super(NVDAObject_outlineItem,self)._get_value()
		try:
			return int(val)
		except:
			return 0

	def _get_value(self):
		val=super(NVDAObject_outlineItem,self)._get_value()
		try:
			int(val)
		except:
			return val

	def reportFocus(self):
		positiveStates=self.calculatePositiveStates()
		positiveStates=positiveStates-(positiveStates&IAccessibleHandler.STATE_SYSTEM_SELECTED)
		negativeStates=self.calculateNegativeStates()
		stateText=" ".join([self.getStateNames(positiveStates),self.getStateNames(negativeStates,opposite=True)])
		speech.speakObjectProperties(name=self.name,stateText=stateText,value=self.value,description=self.description,keyboardShortcut=self.keyboardShortcut,level=_("level %d")%self.level)

class NVDAObject_tab(NVDAObject_IAccessible):

	def reportFocus(self):
		positiveStates=self.calculatePositiveStates()
		positiveStates=positiveStates-(positiveStates&IAccessibleHandler.STATE_SYSTEM_SELECTED)
		negativeStates=self.calculateNegativeStates()
		stateText=" ".join([self.getStateNames(positiveStates),self.getStateNames(negativeStates,opposite=True)])
		speech.speakObjectProperties(name=self.name,stateText=stateText,value=self.value,description=self.description,keyboardShortcut=self.keyboardShortcut,position=self.positionString)

class NVDAObject_tooltip(NVDAObject_IAccessible):

	def event_show(self):
		if (config.conf["presentation"]["reportTooltips"] and (self.role==IAccessibleHandler.ROLE_SYSTEM_TOOLTIP)) or (config.conf["presentation"]["reportHelpBalloons"] and (self.role==IAccessibleHandler.ROLE_SYSTEM_HELPBALLOON)):
			self.speakObject()

class NVDAObject_consoleWindowClass(NVDAObject_IAccessible):

	def event_nameChange(self):
		pass

class NVDAObject_mozillaProgressBar(NVDAObject_IAccessible):

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
			super(NVDAObject_mozillaProgressBar,self).event_valueChange()

class NVDAObject_mozillaUIWindowClass(NVDAObject_IAccessible):
	"""
	Based on NVDAObject, but on focus events, actions are performed whether or not the object really has focus.
	mozillaUIWindowClass objects sometimes do not set their focusable state properly.
	"""

	def __init__(self,*args,**vars):
		NVDAObject_IAccessible.__init__(self,*args,**vars)
		self.needsFocusState=False

class NVDAObject_mozillaUIWindowClass_application(NVDAObject_mozillaUIWindowClass):
	"""
	Based on NVDAObject_mozillaUIWindowClass, but:
	*Value is always empty because otherwise it is a long url to a .shul file that generated the mozilla application.
	*firstChild is the first child that is not a tooltip or a menu popup since these don't seem to allow getNext etc.
	*On focus events, the object is not spoken automatically since focus is given to this object when moving from one object to another.
	"""

	speakOnGainFocus=False

	def _get_value(self):
		return ""

	def _get_firstChild(self):
		try:
			children=self.children
		except:
			return None
		for child in children:
			try:
				role=child.role
				if role not in [IAccessibleHandler.ROLE_SYSTEM_TOOLTIP,IAccessibleHandler.ROLE_SYSTEM_MENUPOPUP]:
					return child
			except:
				pass

class NVDAObject_mozillaDocument(NVDAObject_IAccessible):

	def __init__(self,*args,**vars):
		NVDAObject_IAccessible.__init__(self,*args,**vars)
		self.needsFocusState=False


	def _get_value(self):
		return ""

	def _get_typeString(self):
		if self.states&IAccessibleHandler.STATE_SYSTEM_READONLY:
			return "Mozilla "+IAccessibleHandler.getRoleName(IAccessibleHandler.ROLE_SYSTEM_DOCUMENT)
		else:
			return _("not supported")
 
class NVDAObject_mozillaListItem(NVDAObject_IAccessible):

	def _get_name(self):
		name=super(NVDAObject_mozillaListItem,self)._get_name()
		if self.states&IAccessibleHandler.STATE_SYSTEM_READONLY:
			children=super(NVDAObject_mozillaListItem,self)._get_children()
			if len(children)>0 and (children[0].role in ["bullet",IAccessibleHandler.ROLE_SYSTEM_STATICTEXT]):
				name=children[0].value
		return name

	def _get_children(self):
		children=super(NVDAObject_mozillaListItem,self)._get_children()
		if self.states&IAccessibleHandler.STATE_SYSTEM_READONLY and len(children)>0 and (children[0].role in ["bullet",IAccesssibleHandler.ROLE_SYSTEM_STATICTEXT]):
			del children[0]
		return children

class NVDAObject_link(NVDAObject_IAccessible):
	"""
	Based on NVDAObject_IAccessible, but:
	*Value is always empty otherwise it would be the full url.
	*typeString is link, visited link, or same page link depending on certain states.
	*getChildren does not include any text objects, since text objects are where the name of the link comes from.
	"""

	def _get_typeString(self):
		states=self.states
		typeString=""
		if states&IAccessibleHandler.STATE_SYSTEM_TRAVERSED:
			typeString+="visited "
		typeString+=super(NVDAObject_link,self)._get_typeString()
		return typeString

class NVDAObject_mozillaText(NVDAObject_IAccessible):

	def _get_typeString(self):
		if self.states&IAccessibleHandler.STATE_SYSTEM_READONLY:
			return IAccessibleHandler.getRoleText(IAccessibleHandler.ROLE_SYSTEM_STATICTEXT)
		else:
			return super(NVDAObject_mozillaText,self)._get_typeString()

	def text_getText(self,start=None,end=None):
		return self.name

class NVDAObject_listItem(NVDAObject_IAccessible):

	allowedNegativeStates=NVDAObject_IAccessible.allowedNegativeStates|IAccessibleHandler.STATE_SYSTEM_SELECTED

	def reportFocus(self):
		positiveStates=self.calculatePositiveStates()
		positiveStates=positiveStates-(positiveStates&IAccessibleHandler.STATE_SYSTEM_SELECTED)
		negativeStates=self.calculateNegativeStates()
		stateText=" ".join([self.getStateNames(positiveStates),self.getStateNames(negativeStates,opposite=True)])
		speech.speakObjectProperties(name=self.name,stateText=stateText,value=self.value,description=self.description,keyboardShortcut=self.keyboardShortcut,position=self.positionString)

class NVDAObject_SHELLDLL_DefView_client(NVDAObject_IAccessible):

	speakOnGainFocus=False

class NVDAObject_list(NVDAObject_IAccessible):

	def _get_name(self):
		name=super(NVDAObject_list,self)._get_name()
		if not name:
			name=super(NVDAObject_IAccessible,self)._get_name()
		return name

	def _get_typeString(self):
		return IAccessibleHandler.getRoleName(IAccessibleHandler.ROLE_SYSTEM_LIST)

	def speakDescendantObjects(self,hashList=None):
		child=self.activeChild
		if child:
			child.speakObject()

	def event_gainFocus(self):
		NVDAObject_IAccessible.event_gainFocus(self)
		child=self.activeChild
		if child and (child.role==IAccessibleHandler.ROLE_SYSTEM_LISTITEM):
			IAccessibleHandler.objectEventCallback(-1,winUser.EVENT_OBJECT_FOCUS,self.windowHandle,self._accObjectID,child.IAccessibleChildID,0,0)
		elif not self.firstChild:
			speech.speakMessage(_("%d items")%0)

class NVDAObject_comboBox(NVDAObject_IAccessible):

	def speakDescendantObjects(self,hashList=None):
		child=self.activeChild
		if child:
			child.speakObject()

class NVDAObject_outline(NVDAObject_IAccessible):

	def speakDescendantObjects(self,hashList=None):
		child=self.activeChild
		if child:
			child.speakObject()

class NVDAObject_progressBar(NVDAObject_IAccessible):

	def event_valueChange(self):
		if config.conf["presentation"]["beepOnProgressBarUpdates"]:
			val=self.value
			if val!=globalVars.lastProgressValue:
				baseFreq=110
				tones.beep(int(baseFreq*(1+(float(val[:-1])/6.25))),40)
				globalVars.lastProgressValue=val
		else:
			super(NVDAObject_progressBar,self).event_valueChange()

class NVDAObject_internetExplorerClient(NVDAObject_IAccessible):

	def _get_name(self):
		return ""

	def _get_typeString(self):
		return "HTML "+super(NVDAObject_internetExplorerClient,self)._get_typeString()

	def _get_description(self):
		return ""

class NVDAObject_statusBar(NVDAObject_IAccessible):

	def _get_value(self):
		value=""
		for child in self.children:
			if child.name is not None:
				value+="  "+child.name
		return value

class NVDAObject_sysLink(NVDAObject_IAccessible):

	speakOnGainFocus=False

class NVDAObject_directUIHwndText(NVDAObject_IAccessible):

	def _get_text_characterCount(self):
		return len(self.value)

	def text_getText(self,start=None,end=None):
		start=start if start is not None else 0
		end=end if end is not None else self.text_characterCount
		text=self.value
		return text[start:end]

###class mappings

import winEdit
import richEdit
import winConsole
import MSHTML
import sysListView32
import winword

_dynamicMap={}

_staticMap={
("Shell_TrayWnd",IAccessibleHandler.ROLE_SYSTEM_CLIENT):NVDAObject_Shell_TrayWnd_client,
("tooltips_class32",IAccessibleHandler.ROLE_SYSTEM_TOOLTIP):NVDAObject_tooltip,
("tooltips_class32",IAccessibleHandler.ROLE_SYSTEM_HELPBALLOON):NVDAObject_tooltip,
("Progman",IAccessibleHandler.ROLE_SYSTEM_CLIENT):NVDAObject_Progman_client,
(None,IAccessibleHandler.ROLE_SYSTEM_DIALOG):NVDAObject_dialog,
("TrayClockWClass",IAccessibleHandler.ROLE_SYSTEM_CLIENT):NVDAObject_TrayClockWClass,
("Edit",IAccessibleHandler.ROLE_SYSTEM_TEXT):winEdit.NVDAObject_winEdit,
("Static",IAccessibleHandler.ROLE_SYSTEM_STATICTEXT):NVDAObject_staticText,
("RichEdit20",IAccessibleHandler.ROLE_SYSTEM_TEXT):richEdit.NVDAObject_richEdit,
("RichEdit20A",IAccessibleHandler.ROLE_SYSTEM_TEXT):richEdit.NVDAObject_richEdit,
("RichEdit20W",IAccessibleHandler.ROLE_SYSTEM_TEXT):richEdit.NVDAObject_richEdit,
("RICHEDIT50W",IAccessibleHandler.ROLE_SYSTEM_TEXT):richEdit.NVDAObject_richEdit,
(None,IAccessibleHandler.ROLE_SYSTEM_CHECKBUTTON):NVDAObject_checkBox,
(None,IAccessibleHandler.ROLE_SYSTEM_MENUITEM):NVDAObject_menuItem,
(None,IAccessibleHandler.ROLE_SYSTEM_OUTLINEITEM):NVDAObject_outlineItem,
(None,IAccessibleHandler.ROLE_SYSTEM_PAGETAB):NVDAObject_tab,
(None,IAccessibleHandler.ROLE_SYSTEM_LINK):NVDAObject_link,
("MozillaUIWindowClass",None):NVDAObject_mozillaUIWindowClass,
("MozillaUIWindowClass",IAccessibleHandler.ROLE_SYSTEM_APPLICATION):NVDAObject_mozillaUIWindowClass_application,
("MozillaDialogClass",IAccessibleHandler.ROLE_SYSTEM_ALERT):NVDAObject_dialog,
("MozillaDialogClass",IAccessibleHandler.ROLE_SYSTEM_DIALOG):NVDAObject_dialog,
("MozillaUIWindowClass",IAccessibleHandler.ROLE_SYSTEM_ALERT):NVDAObject_dialog,
("MozillaUIWindowClass",IAccessibleHandler.ROLE_SYSTEM_DIALOG):NVDAObject_dialog,
("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_ALERT):NVDAObject_dialog,
("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_DIALOG):NVDAObject_dialog,
("MozillaDialogClass",IAccessibleHandler.ROLE_SYSTEM_STATICTEXT):NVDAObject_staticText,
("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_STATICTEXT):NVDAObject_staticText,
("MozillaContentWindowClass",IAccessibleHandler.ROLE_SYSTEM_STATICTEXT):NVDAObject_staticText,
("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_TEXT):NVDAObject_mozillaText,
("MozillaContentWindowClass",IAccessibleHandler.ROLE_SYSTEM_TEXT):NVDAObject_mozillaText,
("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_LISTITEM):NVDAObject_mozillaListItem,
("MozillaContentWindowClass",IAccessibleHandler.ROLE_SYSTEM_LISTITEM):NVDAObject_mozillaListItem,
("MozillaContentWindowClass",IAccessibleHandler.ROLE_SYSTEM_DOCUMENT):NVDAObject_mozillaDocument,
("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_DOCUMENT):NVDAObject_mozillaDocument,
("MozillaContentWindowClass",IAccessibleHandler.ROLE_SYSTEM_PROGRESSBAR):NVDAObject_mozillaProgressBar,
("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_PROGRESSBAR):NVDAObject_mozillaProgressBar,
("ConsoleWindowClass",IAccessibleHandler.ROLE_SYSTEM_WINDOW):NVDAObject_consoleWindowClass,
("ConsoleWindowClass",IAccessibleHandler.ROLE_SYSTEM_CLIENT):winConsole.NVDAObject_winConsole,
(None,IAccessibleHandler.ROLE_SYSTEM_LISTITEM):NVDAObject_listItem,
("SHELLDLL_DefView",IAccessibleHandler.ROLE_SYSTEM_CLIENT):NVDAObject_SHELLDLL_DefView_client,
(None,IAccessibleHandler.ROLE_SYSTEM_LIST):NVDAObject_list,
(None,IAccessibleHandler.ROLE_SYSTEM_COMBOBOX):NVDAObject_comboBox,
(None,IAccessibleHandler.ROLE_SYSTEM_OUTLINE):NVDAObject_outline,
("msctls_progress32",IAccessibleHandler.ROLE_SYSTEM_PROGRESSBAR):NVDAObject_progressBar,
("Internet Explorer_Server",IAccessibleHandler.ROLE_SYSTEM_TEXT):MSHTML.NVDAObject_MSHTML,
("Internet Explorer_Server",IAccessibleHandler.ROLE_SYSTEM_PANE):MSHTML.NVDAObject_MSHTML,
("Internet Explorer_Server",IAccessibleHandler.ROLE_SYSTEM_CLIENT):NVDAObject_internetExplorerClient,
("msctls_statusbar32",IAccessibleHandler.ROLE_SYSTEM_STATUSBAR):NVDAObject_statusBar,
("TTntEdit.UnicodeClass",IAccessibleHandler.ROLE_SYSTEM_TEXT):winEdit.NVDAObject_winEdit,
("TTntMemo.UnicodeClass",IAccessibleHandler.ROLE_SYSTEM_TEXT):winEdit.NVDAObject_winEdit,
("TRichViewEdit",IAccessibleHandler.ROLE_SYSTEM_CLIENT):winEdit.NVDAObject_winEdit,
("TRichView",IAccessibleHandler.ROLE_SYSTEM_CLIENT):NVDAObject_staticText,
("TRichEdit",IAccessibleHandler.ROLE_SYSTEM_CLIENT):richEdit.NVDAObject_richEdit,
("TTntDrawGrid.UnicodeClass",IAccessibleHandler.ROLE_SYSTEM_CLIENT):NVDAObject_list,
("SysListView32",IAccessibleHandler.ROLE_SYSTEM_LISTITEM):sysListView32.NVDAObject_listItem,
("ATL:SysListView32",IAccessibleHandler.ROLE_SYSTEM_LISTITEM):sysListView32.NVDAObject_listItem,
("TWizardForm",IAccessibleHandler.ROLE_SYSTEM_CLIENT):NVDAObject_dialog,
("SysLink",IAccessibleHandler.ROLE_SYSTEM_CLIENT):NVDAObject_sysLink,
("VsTextEditPane",IAccessibleHandler.ROLE_SYSTEM_TEXT):winEdit.NVDAObject_winEdit,
("DirectUIHWND",IAccessibleHandler.ROLE_SYSTEM_TEXT):NVDAObject_directUIHwndText,
("_WwG",IAccessibleHandler.ROLE_SYSTEM_CLIENT):winword.NVDAObject_wordDocument,
}
