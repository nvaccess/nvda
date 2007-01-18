import re
import tones
import time
import difflib
import ctypes
import comtypes.automation
import comtypesClient
import debug
from keyboardHandler import sendKey, key 
import IAccessibleHandler
import winUser
import winKernel
import globalVars
import audio
import api
import config
import baseType
import window
import winEdit
import winConsole
import ITextDocument
import MSHTML

def getNVDAObjectFromEvent(hwnd,objectID,childID):
	accHandle=IAccessibleHandler.accessibleObjectFromEvent(hwnd,objectID,childID)
	if not accHandle:
		return None
	(pacc,child)=accHandle
	obj=NVDAObject_IAccessible(pacc,child,hwnd=hwnd,objectID=objectID)
	return obj

def getNVDAObjectFromPoint(x,y):
	accHandle=IAccessibleHandler.accessibleObjectFromPoint(x,y)
	if not accHandle:
		return None
	(pacc,child)=accHandle
	obj=NVDAObject_IAccessible(pacc,child)
	return obj

def registerNVDAObjectClass(processID,windowClass,objectRole,cls):
	_dynamicMap[(processID,windowClass,objectRole)]=cls

def unregisterNVDAObjectClass(processID,windowClass,objectRole):
	del _dynamicMap[(processID,windowClass,objectRole)]

class NVDAObject_IAccessible(window.NVDAObject_window):
	"""
the NVDAObject for IAccessible
@ivar IAccessibleChildID: the IAccessible object's child ID
@type IAccessibleChildID: int
"""

	allowedPositiveStates=IAccessibleHandler.STATE_SYSTEM_UNAVAILABLE|IAccessibleHandler.STATE_SYSTEM_SELECTED|IAccessibleHandler.STATE_SYSTEM_PRESSED|IAccessibleHandler.STATE_SYSTEM_CHECKED|IAccessibleHandler.STATE_SYSTEM_MIXED|IAccessibleHandler.STATE_SYSTEM_EXPANDED|IAccessibleHandler.STATE_SYSTEM_COLLAPSED|IAccessibleHandler.STATE_SYSTEM_BUSY|IAccessibleHandler.STATE_SYSTEM_HASPOPUP

	def __new__(cls,pacc,child,hwnd=None,objectID=None):
		"""
Checks the window class and IAccessible role against a map of NVDAObject_IAccessible sub-types, and if a match is found, returns that rather than just NVDAObject_IAccessible.
"""  
		oldCls=cls
		if not hwnd:
			hwnd=IAccessibleHandler.windowFromAccessibleObject(pacc)
		windowClass=winUser.getClassName(hwnd)
		processID=winUser.getWindowThreadProcessID(hwnd)
		try:
			objectRole=pacc.accRole(child)
		except:
			objectRole=0
		if _dynamicMap.has_key((processID,windowClass,objectRole)):
			cls=_dynamicMap[(processID,windowClass,objectRole)]
		elif _dynamicMap.has_key((processID,windowClass,None)):
			cls=_dynamicMap[(processID,windowClass,None)]
		elif _dynamicMap.has_key((processID,None,objectRole)):
			cls=_dynamicMap[(processID,None,objectRole)]
		elif _staticMap.has_key((windowClass,objectRole)):
			cls=_staticMap[(windowClass,objectRole)]
		elif _staticMap.has_key((windowClass,None)):
			cls=_staticMap[(windowClass,None)]
		elif _staticMap.has_key((None,objectRole)):
			cls=_staticMap[(None,objectRole)]
		else:
			cls=NVDAObject_IAccessible
		obj=window.NVDAObject_window.__new__(cls,hwnd)
		obj._cachedRole=objectRole
		obj.__init__(pacc,child,hwnd=hwnd,objectID=objectID)
		return obj

	def __init__(self,pacc,child,hwnd=None,objectID=None):
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
		window.NVDAObject_window.__init__(self,hwnd)
		self._pacc=pacc
		self._accChild=child
		self._accObjectID=objectID
		self._lastPositiveStates=self.calculatePositiveStates()
		self._lastNegativeStates=self.calculateNegativeStates()
		self._doneInit=True


	def __hash__(self):
		l=self._hashLimit
		p=self._hashPrime
		h=baseType.NVDAObject.__hash__(self)
		h=(h+(hash(self._accObjectID)*p))%l
		h=(h+(hash(self.IAccessibleChildID)*p))%l
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
		return res if isinstance(res,basestring) else ""

	def _get_role(self):
		return self._cachedRole

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
			return nextObject

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
			return getNVDAObjectFromEvent(obj.windowHandle,IAccessibleHandler.OBJID_CLIENT,0)
		else:
			return obj

	def _get_children(self):
		childCount=self.childCount
		if childCount>0:
			children=[NVDAObject_IAccessible(x[0],x[1]) for x in IAccessibleHandler.accessibleChildren(self._pacc,0,childCount)]
			children=[(getNVDAObjectFromEvent(x.windowHandle,IAccessibleHandler.OBJID_CLIENT,0) if x and x.role==IAccessibleHandler.ROLE_SYSTEM_WINDOW else x) for x in children]
			children=[x for x in children if x]
			return children
		else:
			child=self.firstChild
			children=[]
			while child:
				children.append(child)
				child=child.next
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

	def updateMenuMode(self):
		if self.role not in [IAccessibleHandler.ROLE_SYSTEM_MENUBAR,IAccessibleHandler.ROLE_SYSTEM_MENUPOPUP,IAccessibleHandler.ROLE_SYSTEM_MENUITEM]:
			api.setMenuMode(False)
		if self.role==IAccessibleHandler.ROLE_SYSTEM_MENUITEM:
			audio.cancel()

	def event_mouseMove(self,x,y,oldX,oldY):
		location=self.location
		if not location or (len(location)!=4):
			return
		(left,top,width,height)=location
		right=left+width
		bottom=top+height
		if (oldX<left) or (oldX>right) or (oldY<top) or (oldY>bottom):
			audio.cancel()
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
		return self.states&IAccessibleHandler.STATE_SYSTEM_PROTECTED

	def event_gainFocus(self):
		self.updateMenuMode()
		if not (not api.getMenuMode() and (self.role==IAccessibleHandler.ROLE_SYSTEM_MENUITEM)):
			if config.conf["presentation"]["reportObjectGroupNames"] and api.getForegroundObject() and (api.getForegroundObject().role==IAccessibleHandler.ROLE_SYSTEM_DIALOG) and (self.IAccessibleChildID==0): 
				groupName=self.groupName
				if groupName:
					audio.speakMessage("%s %s"%(groupName,IAccessibleHandler.getRoleName(IAccessibleHandler.ROLE_SYSTEM_GROUPING)))
			window.NVDAObject_window.event_gainFocus(self)

	def event_menuStart(self):
		if self.role not in [IAccessibleHandler.ROLE_SYSTEM_MENUBAR,IAccessibleHandler.ROLE_SYSTEM_MENUPOPUP,IAccessibleHandler.ROLE_SYSTEM_MENUITEM]:
			return
		if not api.getMenuMode():
			audio.cancel()
			api.setMenuMode(True)
			self.speakObject()
			for child in self.children:
				if child.hasFocus:
					child.speakObject()
					break

	def event_valueChange(self):
		if self.hasFocus:
			audio.speakObjectProperties(value=self.value)

	def event_nameChange(self):
		if self.hasFocus:
			audio.speakObjectProperties(name=self.name)

	def event_stateChange(self):
		positiveStates=self.calculatePositiveStates()
		newPositiveStates=positiveStates-(positiveStates&self._lastPositiveStates)
		negativeStates=self.calculateNegativeStates()
		newNegativeStates=negativeStates-(negativeStates&self._lastNegativeStates)
		if self.hasFocus:
			if newPositiveStates:
				audio.speakObjectProperties(stateText=self.getStateNames(newPositiveStates))
			if newNegativeStates:
				audio.speakObjectProperties(stateText=self.getStateNames(newNegativeStates,opposite=True))
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

	def _get_value(self):
		return ""

	def event_foreground(self):
		super(NVDAObject_dialog,self).event_foreground()
		for child in self.children:
			states=child.states
			if (not states&IAccessibleHandler.STATE_SYSTEM_OFFSCREEN) and (not states&IAccessibleHandler.STATE_SYSTEM_INVISIBLE) and (not states&IAccessibleHandler.STATE_SYSTEM_UNAVAILABLE):
				child.speakObject()
				if child.states&IAccessibleHandler.STATE_SYSTEM_FOCUSED:
					audio.speakObjectProperties(stateText=child.getStateName(IAccessibleHandler.STATE_SYSTEM_FOCUSED))
				if child.states&IAccessibleHandler.STATE_SYSTEM_DEFAULT:
					audio.speakObjectProperties(stateText=child.getStateName(IAccessibleHandler.STATE_SYSTEM_DEFAULT))
			if child.role==IAccessibleHandler.ROLE_SYSTEM_PROPERTYPAGE:
				for grandChild in child.children:
					states=grandChild.states
					if (not states&IAccessibleHandler.STATE_SYSTEM_OFFSCREEN) and (not states&IAccessibleHandler.STATE_SYSTEM_INVISIBLE) and (not states&IAccessibleHandler.STATE_SYSTEM_UNAVAILABLE):
						grandChild.speakObject()
						if grandChild.states&IAccessibleHandler.STATE_SYSTEM_FOCUSED:
							audio.speakObjectProperties(stateText=grandChild.getStateName(IAccessibleHandler.STATE_SYSTEM_FOCUSED))
						if grandChild.states&IAccessibleHandler.STATE_SYSTEM_DEFAULT:
							audio.speakObjectProperties(stateText=grandChild.getStateName(IAccessibleHandler.STATE_SYSTEM_DEFAULT))

class NVDAObject_TrayClockWClass(NVDAObject_IAccessible):
	"""
	Based on NVDAObject but the role is changed to clock.
	"""

	def _get_role(self):
		return IAccessibleHandler.ROLE_SYSTEM_CLOCK

class NVDAObject_Shell_TrayWnd_client(NVDAObject_IAccessible):
	"""
	Based on NVDAObject but on foreground events nothing gets spoken.
	This is the window which holds the windows start button and taskbar.
	"""
 
	def __init__(self,*args,**vars):
		NVDAObject_IAccessible.__init__(self,*args,**vars)
		self.speakOnForeground=False
		self.speakOnGainFocus=False

class NVDAObject_Progman_client(NVDAObject_IAccessible):
	"""
	Based on NVDAObject but on foreground events nothing gets spoken.
	This is the window which holds the windows desktop.
	"""

	def __init__(self,*args,**vars):
		NVDAObject_IAccessible.__init__(self,*args,**vars)
		self.speakOnForeground=False
		self.speakOnGainFocus=False

class NVDAObject_staticText(NVDAObject_IAccessible):

	def text_getText(self,start=None,end=None):
		text=self.value
		start=start if isinstance(start,int) else 0
		end=end if isinstance(end,int) else len(self.value)
		return text[start:end]

	def _get_name(self):
		return ""

	def _get_value(self):
		return super(NVDAObject_staticText,self).name

class NVDAObject_edit(winEdit.NVDAObjectExt_edit,NVDAObject_IAccessible):

	def __init__(self,*args,**vars):
		NVDAObject_IAccessible.__init__(self,*args,**vars)
		winEdit.NVDAObjectExt_edit.__init__(self,*args,**vars)

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

class NVDAObject_outlineItem(NVDAObject_IAccessible):

	def _get_level(self):
		val=super(NVDAObject_outlineItem,self).value
		try:
			return int(val)
		except:
			return None

	def _get_value(self):
		val=super(NVDAObject_outlineItem,self).value
		try:
			int(val)
		except:
			return val

class NVDAObject_tooltip(NVDAObject_IAccessible):

	def _get_name(self):
		name=super(NVDAObject_tooltip,self).name
		value=super(NVDAObject_tooltip,self).value
		if name and not value:
			return ""
		else:
			return name

	def _get_value(self):
		name=super(NVDAObject_tooltip,self).name
		value=super(NVDAObject_tooltip,self).value
		if name and not value:
			return name
		else:
			return ""

	def event_toolTip(self):
		if (config.conf["presentation"]["reportTooltips"] and (self.role==IAccessibleHandler.ROLE_SYSTEM_TOOLTIP)) or (config.conf["presentation"]["reportHelpBalloons"] and (self.role==IAccessibleHandler.ROLE_SYSTEM_HELPBALLOON)):
			self.speakObject()

class NVDAObject_consoleWindowClass(NVDAObject_IAccessible):

	def event_nameChange(self):
		pass

class NVDAObject_consoleWindowClassClient(winConsole.NVDAObjectExt_console,NVDAObject_IAccessible):

	def __init__(self,*args,**vars):
		NVDAObject_IAccessible.__init__(self,*args,**vars)
		self.registerScriptKeys({
			key("control+c"):self.script_protectConsoleKillKey,
			key("ExtendedUp"):self.script_text_moveByLine,
			key("ExtendedDown"):self.script_text_moveByLine,
			key("ExtendedLeft"):self.script_text_moveByCharacter,
			key("ExtendedRight"):self.script_text_moveByCharacter,
			key("Control+ExtendedLeft"):self.script_text_moveByWord,
			key("Control+ExtendedRight"):self.script_text_moveByWord,
			key("ExtendedHome"):self.script_text_moveByCharacter,
			key("ExtendedEnd"):self.script_text_moveByCharacter,
			key("control+extendedHome"):self.script_text_moveByLine,
			key("control+extendedEnd"):self.script_text_moveByLine,
			key("ExtendedDelete"):self.script_text_delete,
			key("Back"):self.script_text_backspace,
		})

class NVDAObject_richEdit(ITextDocument.NVDAObjectExt_ITextDocument,NVDAObject_IAccessible):

	def __init__(self,*args,**vars):
		NVDAObject_IAccessible.__init__(self,*args,**vars)
		ITextDocument.NVDAObjectExt_ITextDocument.__init__(self,*args,**vars)

	def _get_typeString(self):
		return "rich "+super(NVDAObject_richEdit,self).typeString

	def _get_value(self):
		r=self.text_getLineOffsets(self.text_caretOffset)
		return self.text_getText(r[0],r[1])

	def getDocumentObjectModel(self):
		domPointer=ctypes.POINTER(comtypes.automation.IDispatch)()
		res=ctypes.windll.oleacc.AccessibleObjectFromWindow(self.windowHandle,IAccessibleHandler.OBJID_NATIVEOM,ctypes.byref(domPointer._iid_),ctypes.byref(domPointer))
		if res==0:
			return comtypesClient.wrap(domPointer)
		else:
			raise OSError("No ITextDocument interface")

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

	def __init__(self,*args,**vars):
		NVDAObject_IAccessible.__init__(self,*args,**vars)
		self.speakOnGainFocus=False

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
		name=super(NVDAObject_mozillaListItem,self).name
		if self.states&IAccessibleHandler.STATE_SYSTEM_READONLY:
			children=super(NVDAObject_mozillaListItem,self).children
			if len(children)>0 and (children[0].role in ["bullet",IAccessibleHandler.ROLE_SYSTEM_STATICTEXT]):
				name=children[0].name
		return name

	def _get_children(self):
		children=super(NVDAObject_mozillaListItem,self).children
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

	def _get_value(self):
		return ""

	def _get_typeString(self):
		states=self.states
		typeString=""
		if states&IAccessibleHandler.STATE_SYSTEM_TRAVERSED:
			typeString+="visited "
		if states&IAccessibleHandler.STATE_SYSTEM_SELECTABLE:
			typeString+="same page "
		typeString+=super(NVDAObject_link,self).typeString
		return typeString

class NVDAObject_mozillaText(NVDAObject_IAccessible):
	"""
	Based on NVDAObject_mozillaContentWindowClass but:
	*If the object has a name but no value, the name is used as the value and no name is provided.
	*the role is changed to static text if it has the read only state set.
	"""

	def _get_name(self):
		name=super(NVDAObject_mozillaText,self).name
		value=super(NVDAObject_mozillaText,self).value
		if (self.role==IAccessibleHandler.ROLE_SYSTEM_STATICTEXT):
			return ""
		else:
			return name

	def _get_role(self):
		if super(NVDAObject_mozillaText,self).states&IAccessibleHandler.STATE_SYSTEM_READONLY:
			return IAccessibleHandler.ROLE_SYSTEM_STATICTEXT
		else:
			return super(NVDAObject_mozillaText,self).role
 
	def _get_value(self):
		name=super(NVDAObject_mozillaText,self).name
		value=super(NVDAObject_mozillaText,self).value
		if (self.role==IAccessibleHandler.ROLE_SYSTEM_STATICTEXT):
			return name
		else:
			return value


	def text_getText(self,start=None,end=None):
		return self.value

class NVDAObject_mozillaOutlineItem(NVDAObject_IAccessible):

	_re_level=re.compile('.*L([0-9]+)')
	_re_position=re.compile('.*([0-9]+) of ([0-9]+)')
	_re_children=re.compile('.*with ([0-9]+)')

	def _get_description(self):
		desc=super(NVDAObject_mozillaOutlineItem,self).description
		if desc.startswith('Description: '):
			return desc[13:]
		else:
			return ""

	def _get_level(self):
		desc=super(NVDAObject_mozillaOutlineItem,self).description
		m=self._re_level.match(desc)
		try:
			return int(m.groups()[0])
		except:
			return None

	def _get_contains(self):
		desc=super(NVDAObject_mozillaOutlineItem,self).description
		m=self._re_children.match(desc)
		if len(m.groups()[0])>0 and (m.groups()[0]!='0'):
			return _("%s items")%m.groups()[0]
		else:
			return ""

	def _get_positionString(self):
		desc=super(NVDAObject_mozillaOutlineItem,self).description
		m=self._re_position.match(desc)
		if len(m.groups())==2:
			return _("%s of %s")%(m.groups()[0],m.groups()[1])
		else:
			return ""



class NVDAObject_listItem(NVDAObject_IAccessible):

	allowedNegativeStates=NVDAObject_IAccessible.allowedNegativeStates|IAccessibleHandler.STATE_SYSTEM_SELECTED

	def __init__(self,*args,**vars):
		NVDAObject_IAccessible.__init__(self,*args,**vars)
		self._lastNegativeStates=self.calculateNegativeStates()

class NVDAObject_SHELLDLL_DefView_client(NVDAObject_IAccessible):

	def __init__(self,*args,**vars):
		NVDAObject_IAccessible.__init__(self,*args,**vars)
		self.speakOnGainFocus=False

class NVDAObject_list(NVDAObject_IAccessible):

	def _get_name(self):
		name=super(NVDAObject_list,self).name
		if not name:
			name=super(NVDAObject_IAccessible,self).name
		return name

	def event_gainFocus(self):
		NVDAObject_IAccessible.event_gainFocus(self)
		child=self.activeChild
		if child and (child.role==IAccessibleHandler.ROLE_SYSTEM_LISTITEM):
			child._accObjectID=self._accObjectID
			api.setFocusObject(child)
			child.event_gainFocus()
		elif not self.firstChild:
			audio.speakMessage(_("%d items")%0)

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
		return "HTML "+super(NVDAObject_internetExplorerClient,self).typeString

	def _get_description(self):
		return ""

class NVDAObject_internetExplorerEdit(MSHTML.NVDAObjectExt_MSHTMLEdit,NVDAObject_IAccessible):

	def __init__(self,*args,**vars):
		NVDAObject_IAccessible.__init__(self,*args,**vars)
		MSHTML.NVDAObjectExt_MSHTMLEdit.__init__(self,*args,**vars)

	def getDocumentObjectModel(self):
		domPointer=ctypes.POINTER(comtypes.automation.IDispatch)()
		wm=winUser.registerWindowMessage(u'WM_HTML_GETOBJECT')
		lresult=winUser.sendMessage(self.windowHandle,wm,0,0)
		res=ctypes.windll.oleacc.ObjectFromLresult(lresult,ctypes.byref(domPointer._iid_),0,ctypes.byref(domPointer))
		return comtypesClient.wrap(domPointer)

	def _get_typeString(self):
		if self.isContentEditable:
			return IAccessibleHandler.getRoleName(IAccessibleHandler.ROLE_SYSTEM_TEXT)
		else:
			return IAccessibleHandler.getRoleName(self.role)

	def _get_value(self):
		if self.isContentEditable:
			r=self.text_getLineOffsets(self.text_caretOffset)
			if r:
				return self.text_getText(r[0],r[1])
		return ""
 
	def event_gainFocus(self):
		MSHTML.NVDAObjectExt_MSHTMLEdit.event_gainFocus(self)
		self.text_reviewOffset=self.text_caretOffset
		NVDAObject_IAccessible.event_gainFocus(self)

	def event_looseFocus(self):
		MSHTML.NVDAObjectExt_MSHTMLEdit.event_looseFocus(self)

class NVDAObject_statusBar(NVDAObject_IAccessible):

	def _get_value(self):
		value=""
		for child in self.children:
			if child.name is not None:
				value+="  "+child.name
		return value

###class mappings

_dynamicMap={}

_staticMap={
("Shell_TrayWnd",IAccessibleHandler.ROLE_SYSTEM_CLIENT):NVDAObject_Shell_TrayWnd_client,
("tooltips_class32",IAccessibleHandler.ROLE_SYSTEM_TOOLTIP):NVDAObject_tooltip,
("tooltips_class32",IAccessibleHandler.ROLE_SYSTEM_HELPBALLOON):NVDAObject_tooltip,
("Progman",IAccessibleHandler.ROLE_SYSTEM_CLIENT):NVDAObject_Progman_client,
(None,IAccessibleHandler.ROLE_SYSTEM_DIALOG):NVDAObject_dialog,
("TrayClockWClass",IAccessibleHandler.ROLE_SYSTEM_CLIENT):NVDAObject_TrayClockWClass,
("Edit",IAccessibleHandler.ROLE_SYSTEM_TEXT):NVDAObject_edit,
("Static",IAccessibleHandler.ROLE_SYSTEM_STATICTEXT):NVDAObject_staticText,
("RichEdit20W",IAccessibleHandler.ROLE_SYSTEM_TEXT):NVDAObject_richEdit,
("RICHEDIT50W",IAccessibleHandler.ROLE_SYSTEM_TEXT):NVDAObject_richEdit,
(None,IAccessibleHandler.ROLE_SYSTEM_CHECKBUTTON):NVDAObject_checkBox,
(None,IAccessibleHandler.ROLE_SYSTEM_OUTLINEITEM):NVDAObject_outlineItem,
(None,IAccessibleHandler.ROLE_SYSTEM_LINK):NVDAObject_link,
("MozillaUIWindowClass",None):NVDAObject_mozillaUIWindowClass,
("MozillaUIWindowClass",IAccessibleHandler.ROLE_SYSTEM_APPLICATION):NVDAObject_mozillaUIWindowClass_application,
("MozillaDialogClass",IAccessibleHandler.ROLE_SYSTEM_ALERT):NVDAObject_dialog,
("MozillaDialogClass",IAccessibleHandler.ROLE_SYSTEM_DIALOG):NVDAObject_dialog,
("MozillaUIWindowClass",IAccessibleHandler.ROLE_SYSTEM_ALERT):NVDAObject_dialog,
("MozillaUIWindowClass",IAccessibleHandler.ROLE_SYSTEM_DIALOG):NVDAObject_dialog,
("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_ALERT):NVDAObject_dialog,
("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_DIALOG):NVDAObject_dialog,
("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_TEXT):NVDAObject_mozillaText,
("MozillaDialogClass",IAccessibleHandler.ROLE_SYSTEM_STATICTEXT):NVDAObject_staticText,
("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_STATICTEXT):NVDAObject_staticText,
("MozillaContentWindowClass",IAccessibleHandler.ROLE_SYSTEM_TEXT):NVDAObject_mozillaText,
("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_LISTITEM):NVDAObject_mozillaListItem,
("MozillaContentWindowClass",IAccessibleHandler.ROLE_SYSTEM_LISTITEM):NVDAObject_mozillaListItem,
("MozillaContentWindowClass",IAccessibleHandler.ROLE_SYSTEM_DOCUMENT):NVDAObject_mozillaDocument,
("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_DOCUMENT):NVDAObject_mozillaDocument,
("MozillaUIWindowClass",IAccessibleHandler.ROLE_SYSTEM_OUTLINEITEM):NVDAObject_mozillaOutlineItem,
("MozillaContentWindowClass",IAccessibleHandler.ROLE_SYSTEM_OUTLINEITEM):NVDAObject_mozillaOutlineItem,
("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_OUTLINEITEM):NVDAObject_mozillaDocument,
("ConsoleWindowClass",IAccessibleHandler.ROLE_SYSTEM_WINDOW):NVDAObject_consoleWindowClass,
("ConsoleWindowClass",IAccessibleHandler.ROLE_SYSTEM_CLIENT):NVDAObject_consoleWindowClassClient,
(None,IAccessibleHandler.ROLE_SYSTEM_LISTITEM):NVDAObject_listItem,
("SHELLDLL_DefView",IAccessibleHandler.ROLE_SYSTEM_CLIENT):NVDAObject_SHELLDLL_DefView_client,
(None,IAccessibleHandler.ROLE_SYSTEM_LIST):NVDAObject_list,
("msctls_progress32",IAccessibleHandler.ROLE_SYSTEM_PROGRESSBAR):NVDAObject_progressBar,
("Internet Explorer_Server",IAccessibleHandler.ROLE_SYSTEM_TEXT):NVDAObject_internetExplorerEdit,
("Internet Explorer_Server",IAccessibleHandler.ROLE_SYSTEM_PANE):NVDAObject_internetExplorerEdit,
("Internet Explorer_Server",IAccessibleHandler.ROLE_SYSTEM_CLIENT):NVDAObject_internetExplorerClient,
("msctls_statusbar32",IAccessibleHandler.ROLE_SYSTEM_STATUSBAR):NVDAObject_statusBar,
}
