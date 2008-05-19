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
import api
import textHandler

class Gecko_ia2_TextInfo(VirtualBufferTextInfo):

	def getXMLFieldSpeech(self,attrs,fieldType,extraDetail=False,reason=None):
		accRole=attrs['iaccessible::role']
		accRole=int(accRole) if accRole.isdigit() else accRole
		role=IAccessibleHandler.IAccessibleRolesToNVDARoles.get(accRole,controlTypes.ROLE_UNKNOWN)
		_IA2Attributes=attrs.get('iaccessible2::attributes',"")
		IA2Attributes={}
		for attrib in _IA2Attributes.split(';'):
			nameValue=attrib.split(':')
			name=nameValue[0].lower()
			if len(nameValue)>1:
				value=nameValue[1]
			else:
				value=""
			if value is not "":
				IA2Attributes[name]=value
		if IA2Attributes.get('tag',"").lower()=="blockquote":
			role=controlTypes.ROLE_BLOCKQUOTE
		states=set(IAccessibleHandler.IAccessibleStatesToNVDAStates[x] for x in [1<<y for y in xrange(32)] if int(attrs.get('iaccessible::state_%s'%x,0)) and x in IAccessibleHandler.IAccessibleStatesToNVDAStates)
		states|=set(IAccessibleHandler.IAccessible2StatesToNVDAStates[x] for x in [1<<y for y in xrange(32)] if int(attrs.get('iaccessible2::state_%s'%x,0)) and x in IAccessibleHandler.IAccessible2StatesToNVDAStates)
		defaultAction=attrs.get('defaultaction','')
		if defaultAction=="click":
			states.add(controlTypes.STATE_CLICKABLE)
		if role==controlTypes.ROLE_LINK and controlTypes.STATE_LINKED not in states:
			# This is a named link destination, not a link which can be activated. The user doesn't care about these.
			role=controlTypes.ROLE_TEXTFRAME
		level=IA2Attributes.get('level',"")
		newAttrs=attrs.copy()
		newAttrs['role']=role
		newAttrs['states']=states
		if level is not "" and level is not None:
			newAttrs['level']=level
		return super(Gecko_ia2_TextInfo,self).getXMLFieldSpeech(newAttrs,fieldType,extraDetail=extraDetail,reason=reason)

class Gecko_ia2(VirtualBuffer):

	def __init__(self,rootNVDAObject):
		super(Gecko_ia2,self).__init__(rootNVDAObject,backendLibPath=u"VBufBackend_gecko_ia2.dll",TextInfo=Gecko_ia2_TextInfo)
		rootWindowHandle=getattr(self.rootNVDAObject,'event_windowHandle',0)
		if not rootWindowHandle:
			rootWindowHandle=self.rootNVDAObject.windowHandle
		self.rootWindowHandle=rootWindowHandle
		try:
			self.rootID=self.rootNVDAObject.IAccessibleObject.uniqueID
		except:
			self.rootID=0
		self._lastFocusID=0

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
		if not winUser.isWindow(root.windowHandle) or controlTypes.STATE_DEFUNCT in states or controlTypes.STATE_READONLY not in states or controlTypes.STATE_BUSY in states: 
			return False
		try:
			if not NVDAObjects.IAccessible.getNVDAObjectFromEvent(root.windowHandle,IAccessibleHandler.OBJID_CLIENT,root.IAccessibleObject.uniqueID):
				return False
		except:
			return False
		return True

	def event_focusEntered(self,obj,nextHandler):
		pass

	def event_gainFocus(self,obj,nextHandler):
		ID=obj.IAccessibleObject.uniqueID
		if self._lastFocusID==ID:
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
		self._lastFocusID=ID
		#We only want to update the caret and speak the field if we're not in the same one as before
		oldInfo=self.makeTextInfo(textHandler.POSITION_CARET)
		try:
			oldDocHandle,oldID=VBufClient_getFieldIdentifierFromBufferOffset(self.VBufHandle,oldInfo._startOffset)
		except:
			oldDocHandle=oldID=0
		try:
			docHandle=obj.IAccessibleObject.windowHandle
		except:
			return nextHandler()
		if (docHandle!=oldDocHandle or ID!=oldID) and ID!=0:
			try:
				start,end=VBufClient_getBufferOffsetsFromFieldIdentifier(self.VBufHandle,docHandle,ID)
			except:
				#globalVars.log.error("VBufClient_getBufferOffsetsFromFieldIdentifier",exc_info=True)
				return nextHandler()
			newInfo=self.makeTextInfo(textHandler.Bookmark(self.TextInfo,(start,end)))
			startToStart=newInfo.compareEndPoints(oldInfo,"startToStart")
			startToEnd=newInfo.compareEndPoints(oldInfo,"startToEnd")
			endToStart=newInfo.compareEndPoints(oldInfo,"endToStart")
			endToEnd=newInfo.compareEndPoints(oldInfo,"endToEnd")
			if (startToStart<0 and endToEnd>0) or (startToStart>0 and endToEnd<0) or endToStart<=0 or startToEnd>0:
				if not self.passThrough:
					speech.cancelSpeech()
					speech.speakFormattedTextWithXML(newInfo.XMLContext,newInfo.XMLText,self,newInfo.getXMLFieldSpeech,reason=speech.REASON_FOCUS)
				else:
					nextHandler()
				newInfo.collapse()
				newInfo.updateCaret()
		else:
			# The virtual buffer caret was already at the focused node, so we don't speak it.
			# However, we still want to update the speech property cache so that property changes will be spoken properly.
			if not self.passThrough:
				speech.speakObject(obj,speech.REASON_ONLYCACHE)
			else:
				return nextHandler()

	def _caretMovedToField(self,docHandle,ID):
		try:
			pacc,accChildID=IAccessibleHandler.accessibleObjectFromEvent(docHandle,IAccessibleHandler.OBJID_CLIENT,ID)
			if not (pacc==self.rootNVDAObject.IAccessibleObject and accChildID==self.rootNVDAObject.IAccessibleChildID):
				obj=NVDAObjects.IAccessible.IAccessible(IAccessibleObject=pacc,IAccessibleChildID=accChildID)
				api.setNavigatorObject(obj)
				if not eventHandler.isPendingEvents('gainFocus') and controlTypes.STATE_FOCUSABLE in obj.states:
					obj.setFocus()
		except:
			pass

	def _activateField(self,docHandle,ID):
		try:
			pacc,accChildID=IAccessibleHandler.accessibleObjectFromEvent(docHandle,IAccessibleHandler.OBJID_CLIENT,ID)
			role=pacc.accRole(accChildID)
			if role in (IAccessibleHandler.ROLE_SYSTEM_COMBOBOX,IAccessibleHandler.ROLE_SYSTEM_TEXT,IAccessibleHandler.ROLE_SYSTEM_LIST,IAccessibleHandler.ROLE_SYSTEM_SLIDER):
				self.passThrough=True
				virtualBufferHandler.reportPassThrough(self)
			else: #Just try performing the default action of the object, or of one of its ancestors
				obj=NVDAObjects.IAccessible.IAccessible(IAccessibleObject=pacc,IAccessibleChildID=accChildID)
				while obj and obj!=self.rootNVDAObject:
					try:
						action=obj.IAccessibleObject.accDefaultAction(obj.IAccessibleChildID)
						if action:
							try:
								obj.IAccessibleObject.accDoDefaultAction(obj.IAccessibleChildID)
							except:
								l=obj.location
								if l:
									x=(l[0]+l[2]/2)
									y=l[1]+(l[3]/2) 
									oldX,oldY=winUser.getCursorPos()
									winUser.setCursorPos(x,y)
									winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
									winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
									winuser.setCursorPos(oldX,oldY)
							break
					except:
						pass
					obj=obj.parent
		except:
			pass

	def _searchableAttribsForNodeType(self,nodeType):
		if nodeType=="heading":
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
		else:
			return None
		# We should never consider invisible nodes.
		attrs["IAccessible::state_%s"%IAccessibleHandler.STATE_SYSTEM_INVISIBLE]=[None]
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
				#globalVars.log.error("VBufClient_getBufferOffsetsFromFieldIdentifier",exc_info=True)
				return nextHandler()
			newInfo=self.makeTextInfo(textHandler.Bookmark(self.TextInfo,(start,end)))
			startToStart=newInfo.compareEndPoints(oldInfo,"startToStart")
			startToEnd=newInfo.compareEndPoints(oldInfo,"startToEnd")
			endToStart=newInfo.compareEndPoints(oldInfo,"endToStart")
			endToEnd=newInfo.compareEndPoints(oldInfo,"endToEnd")
			if (startToStart<0 and endToEnd>0) or (startToStart>0 and endToEnd<0) or endToStart<=0 or startToEnd>0:
				speech.speakFormattedTextWithXML(newInfo.XMLContext,newInfo.XMLText,self,newInfo.getXMLFieldSpeech,reason=speech.REASON_FOCUS)
				newInfo.collapse()
				newInfo.updateCaret()
