import ctypes
from . import VirtualBuffer, VirtualBufferTextInfo
from virtualBuffer_lib import *
import virtualBufferHandler
import controlTypes
import NVDAObjects.IAccessible
import winUser
import sayAllHandler
import speech
import eventHandler
import IAccessibleHandler
import globalVars
from logHandler import log
import api
import textHandler
import keyUtils

GECKO_SCROLL_TYPE_ANYWHERE=0x06

class Gecko_ia2_TextInfo(VirtualBufferTextInfo):

	def _normalizeControlField(self,attrs):
		accRole=attrs['iaccessible::role']
		accRole=int(accRole) if accRole.isdigit() else accRole
		role=IAccessibleHandler.IAccessibleRolesToNVDARoles.get(accRole,controlTypes.ROLE_UNKNOWN)
		if attrs.get('iaccessible2::attribute_tag',"").lower()=="blockquote":
			role=controlTypes.ROLE_BLOCKQUOTE
		states=set(IAccessibleHandler.IAccessibleStatesToNVDAStates[x] for x in [1<<y for y in xrange(32)] if int(attrs.get('iaccessible::state_%s'%x,0)) and x in IAccessibleHandler.IAccessibleStatesToNVDAStates)
		states|=set(IAccessibleHandler.IAccessible2StatesToNVDAStates[x] for x in [1<<y for y in xrange(32)] if int(attrs.get('iaccessible2::state_%s'%x,0)) and x in IAccessibleHandler.IAccessible2StatesToNVDAStates)
		defaultAction=attrs.get('defaultaction','')
		if defaultAction=="click":
			states.add(controlTypes.STATE_CLICKABLE)
		if role==controlTypes.ROLE_LINK and controlTypes.STATE_LINKED not in states:
			# This is a named link destination, not a link which can be activated. The user doesn't care about these.
			role=controlTypes.ROLE_TEXTFRAME
		level=attrs.get('iaccessible2::attribute_level',"")
		newAttrs=attrs.copy()
		newAttrs['role']=role
		newAttrs['states']=states
		if level is not "" and level is not None:
			newAttrs['level']=level
		return newAttrs

class Gecko_ia2(VirtualBuffer):

	def __init__(self,rootNVDAObject):
		super(Gecko_ia2,self).__init__(rootNVDAObject,backendLibPath=ur"lib\VBufBackend_gecko_ia2.dll",TextInfo=Gecko_ia2_TextInfo)
		rootWindowHandle=getattr(self.rootNVDAObject,'event_windowHandle',0)
		if not rootWindowHandle:
			rootWindowHandle=self.rootNVDAObject.windowHandle
		self.rootWindowHandle=rootWindowHandle
		try:
			self.rootID=self.rootNVDAObject.IAccessibleObject.uniqueID
		except:
			self.rootID=0
		self._lastFocusIdentifier=(0,0)

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
			return True
		else:
			return True

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

	def event_focusEntered(self,obj,nextHandler):
		if self.passThrough:
			 nextHandler()

	def event_gainFocus(self,obj,nextHandler):
		try:
			docHandle=obj.IAccessibleObject.windowHandle
			ID=obj.IAccessibleObject.uniqueID
		except:
			return nextHandler()
		if not self.passThrough and self._lastFocusIdentifier==(docHandle,ID):
			# This was the last non-document node with focus, so don't handle this focus event.
			# Otherwise, if the user switches away and back to this document, the cursor will jump to this node.
			# This is not ideal if the user was positioned over a node which cannot receive focus.
			return
		api.setNavigatorObject(obj)
		if self.VBufHandle is None:
			return nextHandler()
		if obj==self.rootNVDAObject:
			if self.passThrough:
				return nextHandler()
			return 
		if obj.role==controlTypes.ROLE_DOCUMENT and not self.passThrough:
			return
		self._lastFocusIdentifier=(docHandle,ID)
		#We only want to update the caret and speak the field if we're not in the same one as before
		oldInfo=self.makeTextInfo(textHandler.POSITION_CARET)
		try:
			oldDocHandle,oldID=VBufClient_getFieldIdentifierFromBufferOffset(self.VBufHandle,oldInfo._startOffset)
		except:
			oldDocHandle=oldID=0
		if (docHandle!=oldDocHandle or ID!=oldID) and ID!=0:
			try:
				start,end=VBufClient_getBufferOffsetsFromFieldIdentifier(self.VBufHandle,docHandle,ID)
			except:
				#log.error("VBufClient_getBufferOffsetsFromFieldIdentifier",exc_info=True)
				return nextHandler()
			newInfo=self.makeTextInfo(textHandler.Offsets(start,end))
			startToStart=newInfo.compareEndPoints(oldInfo,"startToStart")
			startToEnd=newInfo.compareEndPoints(oldInfo,"startToEnd")
			endToStart=newInfo.compareEndPoints(oldInfo,"endToStart")
			endToEnd=newInfo.compareEndPoints(oldInfo,"endToEnd")
			if (startToStart<0 and endToEnd>0) or (startToStart>0 and endToEnd<0) or endToStart<=0 or startToEnd>0:
				if not self.passThrough:
					speech.cancelSpeech()
					speech.speakTextInfo(newInfo,reason=speech.REASON_FOCUS)
				else:
					nextHandler()
				self.passThrough=self.shouldEnablePassThrough(obj,reason=speech.REASON_FOCUS)
				virtualBufferHandler.reportPassThrough(self)
				newInfo.collapse()
				newInfo.updateCaret()
		else:
			# The virtual buffer caret was already at the focused node, so we don't speak it.
			# However, we still want to update the speech property cache so that property changes will be spoken properly.
			if not self.passThrough:
				speech.speakObject(obj,speech.REASON_ONLYCACHE)
			else:
				return nextHandler()
		if hasattr(obj,'IAccessibleTextObject'):
			# We aren't passing this event to the NVDAObject, so we need to do this ourselves.
			obj.initAutoSelectDetection()

	def _caretMovedToField(self,docHandle,ID,reason=speech.REASON_CARET):
		try:
			pacc,accChildID=IAccessibleHandler.accessibleObjectFromEvent(docHandle,IAccessibleHandler.OBJID_CLIENT,ID)
			if not (pacc==self.rootNVDAObject.IAccessibleObject and accChildID==self.rootNVDAObject.IAccessibleChildID):
				obj=NVDAObjects.IAccessible.IAccessible(IAccessibleObject=pacc,IAccessibleChildID=accChildID)
				api.setNavigatorObject(obj)
				obj.IAccessibleObject.scrollTo(GECKO_SCROLL_TYPE_ANYWHERE)
				if not eventHandler.isPendingEvents('gainFocus') and controlTypes.STATE_FOCUSABLE in obj.states and obj.role!=controlTypes.ROLE_EMBEDDEDOBJECT:
					obj.setFocus()
				if self.shouldEnablePassThrough(obj,reason=reason):
					self.passThrough=True
					virtualBufferHandler.reportPassThrough(self)
		except:
			pass

	def _activateField(self,docHandle,ID):
		try:
			obj=NVDAObjects.IAccessible.getNVDAObjectFromEvent(docHandle,IAccessibleHandler.OBJID_CLIENT,ID)
			if self.shouldEnablePassThrough(obj):
				obj.setFocus()
				self.passThrough=True
				virtualBufferHandler.reportPassThrough(self)
			else: #Just try performing the default action of the object, or of one of its ancestors
				try:
					action=obj.IAccessibleObject.accDefaultAction(obj.IAccessibleChildID)
					if not action:
						log.debugWarning("no default action for object")
						raise RuntimeError("need an action")
					try:
						obj.IAccessibleObject.accDoDefaultAction(obj.IAccessibleChildID)
					except:
						log.debugWarning("error in calling accDoDefaultAction",exc_info=True)
						raise RuntimeError("error in accDoDefaultAction")
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
		except:
			log.debugWarning("Error activating field",exc_info=True)
			pass

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

	def event_scrollingStart(self,obj,nextHandler):
		if self.VBufHandle is None:
			return nextHandler()
		#We only want to update the caret and speak the field if we're not in the same one as before
		oldInfo=self.makeTextInfo(textHandler.POSITION_CARET)
		try:
			oldDocHandle,oldID=VBufClient_getFieldIdentifierFromBufferOffset(self.VBufHandle,oldInfo._startOffset)
		except:
			oldDocHandle=oldID=0
		docHandle=obj.IAccessibleObject.windowHandle
		ID=obj.IAccessibleObject.uniqueID
		if (docHandle!=oldDocHandle or ID!=oldID) and ID!=0:
			try:
				start,end=VBufClient_getBufferOffsetsFromFieldIdentifier(self.VBufHandle,docHandle,ID)
			except:
				#log.error("VBufClient_getBufferOffsetsFromFieldIdentifier",exc_info=True)
				return nextHandler()
			newInfo=self.makeTextInfo(textHandler.Offsets(start,end))
			startToStart=newInfo.compareEndPoints(oldInfo,"startToStart")
			startToEnd=newInfo.compareEndPoints(oldInfo,"startToEnd")
			endToStart=newInfo.compareEndPoints(oldInfo,"endToStart")
			endToEnd=newInfo.compareEndPoints(oldInfo,"endToEnd")
			if (startToStart<0 and endToEnd>0) or (startToStart>0 and endToEnd<0) or endToStart<=0 or startToEnd>0:
				speech.speakTextInfo(newInfo,reason=speech.REASON_FOCUS)
				newInfo.collapse()
				newInfo.updateCaret()

	def _tabOverride(self, direction):
		"""Override the tab order if the virtual buffer caret is not within the currently focused node.
		This is done because many nodes are not focusable and it is thus possible for the virtual buffer caret to be unsynchronised with the focus.
		In this case, we want tab/shift+tab to move to the next/previous focusable node relative to the virtual buffer caret.
		If the virtual buffer caret is not within the focused node, the tab/shift+tab key should be passed through to allow normal tab order navigation.
		Note that this method does not pass the key through itself if it is not overridden. This should be done by the calling script if C{False} is returned.
		@param direction: The direction in which to move.
		@type direction: str
		@return: C{True} if the tab order was overridden, C{False} if not.
		@rtype: bool
		"""
		if self.VBufHandle is None:
			return False

		# We only want to override the tab order if the caret is not within the focused node.
		caretInfo=self.makeTextInfo(textHandler.POSITION_CARET)
		try:
			caretDocHandle,caretID=VBufClient_getFieldIdentifierFromBufferOffset(self.VBufHandle,caretInfo._startOffset)
		except:
			return False
		focus = api.getFocusObject()
		try:
			focusDocHandle=focus.IAccessibleObject.windowHandle
			focusID=focus.IAccessibleObject.uniqueID
		except:
			log.debugWarning("error getting focus windowHandle or uniqueID", exc_info=True)
			return False
		if (caretDocHandle == focusDocHandle and caretID == focusID) or focusID == 0:
			return False
		try:
			start,end=VBufClient_getBufferOffsetsFromFieldIdentifier(self.VBufHandle,focusDocHandle,focusID)
		except:
			return False
		focusInfo=self.makeTextInfo(textHandler.Offsets(start,end))
		startToStart=focusInfo.compareEndPoints(caretInfo,"startToStart")
		startToEnd=focusInfo.compareEndPoints(caretInfo,"startToEnd")
		endToStart=focusInfo.compareEndPoints(caretInfo,"endToStart")
		endToEnd=focusInfo.compareEndPoints(caretInfo,"endToEnd")
		if not ((startToStart<0 and endToEnd>0) or (startToStart>0 and endToEnd<0) or endToStart<=0 or startToEnd>0):
			return False

		# If we reach here, we do want to override tab/shift+tab if possible.
		# Find the next/previous focusable node.
		try:
			newDocHandle, newID, newStart, newEnd = self._iterNodesByType("focusable", direction, caretInfo._startOffset).next()
		except StopIteration:
			return False

		# Finally, speak, move to and set focus to this node.
		newInfo = self.makeTextInfo(textHandler.Offsets(newStart, newEnd))
		speech.speakTextInfo(newInfo,reason=speech.REASON_FOCUS)
		newInfo.collapse()
		newInfo.updateCaret()
		self._caretMovedToField(newDocHandle, newID, reason=speech.REASON_FOCUS)
		return True

	def script_tab(self, keyPress):
		if not self._tabOverride("next"):
			keyUtils.sendKey(keyPress)

	def script_shiftTab(self, keyPress):
		if not self._tabOverride("previous"):
			keyUtils.sendKey(keyPress)

[Gecko_ia2.bindKey(keyName,scriptName) for keyName,scriptName in (
	("tab", "tab"),
	("shift+tab", "shiftTab"),
)]
