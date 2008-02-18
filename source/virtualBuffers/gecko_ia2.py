import ctypes
from . import VirtualBuffer, VirtualBufferTextInfo
from virtualBuffer_lib import *
import virtualBufferHandler
import controlTypes
import NVDAObjects.IAccessible
import winUser
import sayAllHandler
import speech
import IAccessibleHandler
import globalVars
import api
import textHandler

class Gecko_ia2_TextInfo(VirtualBufferTextInfo):

	def getXMLFieldSpeech(self,attrs,fieldType,extraDetail=False,reason=None):
		accRole=attrs['iaccessible::role']
		accRole=int(accRole) if accRole.isdigit() else accRole
		role=IAccessibleHandler.IAccessibleRolesToNVDARoles.get(accRole,controlTypes.ROLE_UNKNOWN)
		IA2Attributes=attrs.get('iaccessible2::attributes',"")
		if IA2Attributes.lower().find('tag:blockquote')>=0:
			role=controlTypes.ROLE_BLOCKQUOTE
		states=set(IAccessibleHandler.IAccessibleStatesToNVDAStates[x] for x in [1<<y for y in xrange(32)] if int(attrs.get('iaccessible::state_%s'%x,0)) and x in IAccessibleHandler.IAccessibleStatesToNVDAStates)
		states|=set(IAccessibleHandler.IAccessible2StatesToNVDAStates[x] for x in [1<<y for y in xrange(32)] if int(attrs.get('iaccessible2::state_%s'%x,0)) and x in IAccessibleHandler.IAccessible2StatesToNVDAStates)
		newAttrs=attrs.copy()
		newAttrs['role']=role
		newAttrs['states']=states
		return super(Gecko_ia2_TextInfo,self).getXMLFieldSpeech(newAttrs,fieldType,extraDetail=extraDetail,reason=reason)

class Gecko_ia2(VirtualBuffer):

	def __init__(self,rootNVDAObject):
		super(Gecko_ia2,self).__init__(rootNVDAObject,backendLibPath="VBufBackend_gecko_ia2.dll",TextInfo=Gecko_ia2_TextInfo)
		self.busyFlag=True if controlTypes.STATE_BUSY in self.rootNVDAObject.states else False


	def isNVDAObjectInVirtualBuffer(self,obj):
		if not isinstance(obj,NVDAObjects.IAccessible.IA2.IA2):
			return False
		if not winUser.isDescendantWindow(self.rootNVDAObject.windowHandle,obj.windowHandle):
			return False
		return True

		while w:
			if w==root.windowHandle:
				return True
			w=winUser.getAncestor(w,winUser.GA_PARENT)
		return False

	def isAlive(self):
		root=self.rootNVDAObject
		if root and winUser.isWindow(root.windowHandle) and controlTypes.STATE_DEFUNCT not in root.states and root.role!=controlTypes.ROLE_UNKNOWN: 
			return True
		else:
			return False

	def event_focusEntered(self,obj,nextHandler):
		pass

	def event_gainFocus(self,obj,nextHandler):
		if self._inFind:
			return
		if not self.isAlive():
			return virtualBufferHandler.killVirtualBuffer(self)
		api.setNavigatorObject(obj)
		role=obj.role
		states=obj.states
		if controlTypes.STATE_BUSY in self.rootNVDAObject.states:
			try:
				newRoot=NVDAObjects.IAccessible.getNVDAObjectFromEvent(self.rootNVDAObject.windowHandle,-4,self.rootNVDAObject.IAccessibleObject.uniqueID)
			except:
				return virtualBufferHandler.killVirtualBuffer(self)
			if newRoot and controlTypes.STATE_BUSY not in newRoot.states:
				self.rootNVDAObject=newRoot
				self.unloadBuffer()
				self.loadBuffer()
				self.busyFlag=False
				return self.event_gainFocus(obj,nextHandler)
			else:
				speech.speakMessage(controlTypes.speechStateLabels[controlTypes.STATE_BUSY])
				self.busyFlag=True
				return
		else:
			self.busyFlag=False
		if obj==self.rootNVDAObject:
			return speech.speakObjectProperties(obj,name=True)
		if sayAllHandler.isRunning():
			speech.cancelSpeech()
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
			if (startToStart<0 and endToEnd>0) or (startToStart>0 and endToEnd<0) or endToStart<0 or startToEnd>0:  
				speech.speakFormattedTextWithXML(newInfo.XMLContext,newInfo.XMLText,self,newInfo.getXMLFieldSpeech,reason=speech.REASON_FOCUS)
				newInfo.collapse()
				newInfo.updateCaret()

	def _caretMovedToField(self,docHandle,ID):
		try:
			pacc,accChildID=IAccessibleHandler.accessibleObjectFromEvent(docHandle,IAccessibleHandler.OBJID_CLIENT,ID)
			if not (pacc==self.rootNVDAObject.IAccessibleObject and accChildID==self.rootNVDAObject.IAccessibleChildID):
				pacc.accSelect(1,accChildID)
		except:
			pass

	def _activateField(self,docHandle,ID):
		try:
			pacc,accChildID=IAccessibleHandler.accessibleObjectFromEvent(docHandle,IAccessibleHandler.OBJID_CLIENT,ID)
			role=pacc.accRole(accChildID)
			if role in (IAccessibleHandler.ROLE_SYSTEM_COMBOBOX,IAccessibleHandler.ROLE_SYSTEM_TEXT,IAccessibleHandler.ROLE_SYSTEM_LIST):
				api.toggleVirtualBufferPassThrough()
			else:
				pacc.accDoDefaultAction(accChildID)
		except:
			pass

	def _searchableAttribsForNodeType(self,nodeType):
		if nodeType=="heading":
			return {"IAccessible::role":[IAccessibleHandler.IA2_ROLE_HEADING]}
		elif nodeType=="link":
			return {"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_LINK]}
		elif nodeType=="visitedLink":
			return {"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_LINK],"IAccessible::state_%d"%IAccessibleHandler.STATE_SYSTEM_TRAVERSED:[1]}
		elif nodeType=="unvisitedLink":
			return {"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_LINK],"IAccessible::state_%d"%IAccessibleHandler.STATE_SYSTEM_TRAVERSED:[None]}
		elif nodeType=="formField":
			return {"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_PUSHBUTTON,IAccessibleHandler.ROLE_SYSTEM_RADIOBUTTON,IAccessibleHandler.ROLE_SYSTEM_CHECKBUTTON,IAccessibleHandler.ROLE_SYSTEM_COMBOBOX,IAccessibleHandler.ROLE_SYSTEM_LIST,IAccessibleHandler.ROLE_SYSTEM_OUTLINE,IAccessibleHandler.ROLE_SYSTEM_TEXT],"IAccessible::state_%s"%IAccessibleHandler.STATE_SYSTEM_READONLY:[None]}
		else:
			return None

	def event_stateChange(self,obj,nextHandler):
		if controlTypes.STATE_BUSY in self.rootNVDAObject.states:
			try:
				newRoot=NVDAObjects.IAccessible.getNVDAObjectFromEvent(self.rootNVDAObject.windowHandle,-4,ID)
			except:
				return virtualBufferHandler.killVirtualBuffer(self)
			if newRoot and controlTypes.STATE_BUSY not in newRoot.states:
				self.rootNVDAObject=newRoot
				self.unloadBuffer()
				self.loadBuffer()
				self.busyFlag=False
				return self.event_stateChange(obj,nextHandler)
			else:
				speech.speakMessage(controlTypes.speechStateLabels[controlTypes.STATE_BUSY])
				self.busyFlag=True
		if not self.isAlive():
			return virtualBufferHandler.killVirtualBuffer(self)
		if self.rootNVDAObject and self.busyFlag and not controlTypes.STATE_BUSY in self.rootNVDAObject.states:
			self.unloadBuffer()
			self.loadBuffer()
			self.busyFlag=False
