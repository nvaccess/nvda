from . import VirtualBuffer, VirtualBufferTextInfo
import virtualBufferHandler
import controlTypes
import NVDAObjects.IAccessible
import winUser
import IAccessibleHandler
from logHandler import log
import textInfos

class Gecko_ia2_TextInfo(VirtualBufferTextInfo):

	def _normalizeControlField(self,attrs):
		accRole=attrs['IAccessible::role']
		accRole=int(accRole) if accRole.isdigit() else accRole
		role=IAccessibleHandler.IAccessibleRolesToNVDARoles.get(accRole,controlTypes.ROLE_UNKNOWN)
		if attrs.get('IAccessible2::attribute_tag',"").lower()=="blockquote":
			role=controlTypes.ROLE_BLOCKQUOTE
		states=set(IAccessibleHandler.IAccessibleStatesToNVDAStates[x] for x in [1<<y for y in xrange(32)] if int(attrs.get('IAccessible::state_%s'%x,0)) and x in IAccessibleHandler.IAccessibleStatesToNVDAStates)
		states|=set(IAccessibleHandler.IAccessible2StatesToNVDAStates[x] for x in [1<<y for y in xrange(32)] if int(attrs.get('IAccessible2::state_%s'%x,0)) and x in IAccessibleHandler.IAccessible2StatesToNVDAStates)
		defaultAction=attrs.get('defaultAction','')
		if defaultAction=="click":
			states.add(controlTypes.STATE_CLICKABLE)
		if role==controlTypes.ROLE_LINK and controlTypes.STATE_LINKED not in states:
			# This is a named link destination, not a link which can be activated. The user doesn't care about these.
			role=controlTypes.ROLE_TEXTFRAME
		level=attrs.get('IAccessible2::attribute_level',"")
		newAttrs=textInfos.ControlField()
		newAttrs.update(attrs)
		newAttrs['role']=role
		newAttrs['states']=states
		if level is not "" and level is not None:
			newAttrs['level']=level
		return newAttrs

class Gecko_ia2(VirtualBuffer):

	TextInfo=Gecko_ia2_TextInfo

	def __init__(self,rootNVDAObject):
		super(Gecko_ia2,self).__init__(rootNVDAObject,backendLibPath=r"lib\VBufBackend_gecko_ia2.dll")

	def isNVDAObjectInVirtualBuffer(self,obj):
		#Special code to handle Mozilla combobox lists
		if obj.windowClassName.startswith('Mozilla') and winUser.getWindowStyle(obj.windowHandle)&winUser.WS_POPUP:
			parent=obj.parent
			while parent and parent.windowHandle==obj.windowHandle:
				parent=parent.parent
			if parent:
				obj=parent.parent
		if not (isinstance(obj,NVDAObjects.IAccessible.IAccessible) and isinstance(obj.IAccessibleObject,IAccessibleHandler.IAccessible2)) or not obj.windowClassName.startswith('Mozilla') or not winUser.isDescendantWindow(self.rootNVDAObject.windowHandle,obj.windowHandle):
			return False
		if self.rootNVDAObject.windowHandle==obj.windowHandle:
			ID=obj.IAccessibleObject.uniqueID
			try:
				self.rootNVDAObject.IAccessibleObject.accChild(ID)
			except:
				return False

		return self._isNVDAObjectInApplication(obj)

	def isAlive(self):
		root=self.rootNVDAObject
		if not root:
			return False
		states=root.states
		if not winUser.isWindow(root.windowHandle) or controlTypes.STATE_DEFUNCT in states or controlTypes.STATE_READONLY not in states:
			return False
		try:
			if not NVDAObjects.IAccessible.getNVDAObjectFromEvent(root.windowHandle,IAccessibleHandler.OBJID_CLIENT,root.IAccessibleObject.uniqueID):
				return False
		except:
			return False
		return True

	def getNVDAObjectFromIdentifier(self, docHandle, ID):
		return NVDAObjects.IAccessible.getNVDAObjectFromEvent(docHandle, IAccessibleHandler.OBJID_CLIENT, ID)

	def getIdentifierFromNVDAObject(self,obj):
		docHandle=obj.windowHandle
		ID=obj.IAccessibleObject.uniqueID
		return docHandle,ID

	def _shouldIgnoreFocus(self, obj):
		if obj.role == controlTypes.ROLE_DOCUMENT:
			return True
		return super(Gecko_ia2, self)._shouldIgnoreFocus(obj)

	def _postGainFocus(self, obj):
		if hasattr(obj,'IAccessibleTextObject'):
			# We aren't passing this event to the NVDAObject, so we need to do this ourselves.
			obj.initAutoSelectDetection()
		super(Gecko_ia2, self)._postGainFocus(obj)

	def _shouldSetFocusToObj(self, obj):
		return super(Gecko_ia2,self)._shouldSetFocusToObj(obj) and obj.role!=controlTypes.ROLE_EMBEDDEDOBJECT

	def _activateNVDAObject(self, obj):
		try:
			obj.doAction()
		except:
			log.debugWarning("could not programmatically activate field, trying mouse")
			l=obj.location
			if l:
				x=(l[0]+l[2]/2)
				y=l[1]+(l[3]/2) 
				oldX,oldY=winUser.getCursorPos()
				winUser.setCursorPos(x,y)
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
				winUser.setCursorPos(oldX,oldY)
			else:
				log.debugWarning("no location for field")

	def _searchableAttribsForNodeType(self,nodeType):
		if nodeType.startswith('heading') and nodeType[7:].isdigit():
			attrs={"IAccessible::role":[IAccessibleHandler.IA2_ROLE_HEADING],"IAccessible2::attribute_level":[nodeType[7:]]}
		elif nodeType=="heading":
			attrs={"IAccessible::role":[IAccessibleHandler.IA2_ROLE_HEADING]}
		elif nodeType=="table":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_TABLE]}
		elif nodeType=="link":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_LINK],"IAccessible::state_%d"%IAccessibleHandler.STATE_SYSTEM_LINKED:[1]}
		elif nodeType=="visitedLink":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_LINK],"IAccessible::state_%d"%IAccessibleHandler.STATE_SYSTEM_TRAVERSED:[1]}
		elif nodeType=="unvisitedLink":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_LINK],"IAccessible::state_%d"%IAccessibleHandler.STATE_SYSTEM_LINKED:[1],"IAccessible::state_%d"%IAccessibleHandler.STATE_SYSTEM_TRAVERSED:[None]}
		elif nodeType=="formField":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_PUSHBUTTON,IAccessibleHandler.ROLE_SYSTEM_RADIOBUTTON,IAccessibleHandler.ROLE_SYSTEM_CHECKBUTTON,IAccessibleHandler.ROLE_SYSTEM_COMBOBOX,IAccessibleHandler.ROLE_SYSTEM_LIST,IAccessibleHandler.ROLE_SYSTEM_OUTLINE,IAccessibleHandler.ROLE_SYSTEM_TEXT],"IAccessible::state_%s"%IAccessibleHandler.STATE_SYSTEM_READONLY:[None]}
		elif nodeType=="list":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_LIST]}
		elif nodeType=="listItem":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_LISTITEM]}
		elif nodeType=="button":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_PUSHBUTTON]}
		elif nodeType=="edit":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_TEXT],"IAccessible::state_%s"%IAccessibleHandler.STATE_SYSTEM_READONLY:[None]}
		elif nodeType=="frame":
			attrs={"IAccessible::role":[IAccessibleHandler.IA2_ROLE_INTERNAL_FRAME]}
		elif nodeType=="separator":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_SEPARATOR]}
		elif nodeType=="radioButton":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_RADIOBUTTON]}
		elif nodeType=="comboBox":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_COMBOBOX]}
		elif nodeType=="checkBox":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_CHECKBUTTON]}
		elif nodeType=="graphic":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_GRAPHIC]}
		elif nodeType=="blockQuote":
			attrs={"IAccessible2::attribute_tag":["BLOCKQUOTE"]}
		elif nodeType=="focusable":
			attrs={"IAccessible::state_%s"%IAccessibleHandler.STATE_SYSTEM_FOCUSABLE:[1]}
		else:
			return None
		return attrs

	def event_stateChange(self,obj,nextHandler):
		if not self.isAlive():
			return virtualBufferHandler.killVirtualBuffer(self)
		return nextHandler()

	def event_scrollingStart(self, obj, nextHandler):
		if not self._handleScrollTo(obj):
			return nextHandler()
