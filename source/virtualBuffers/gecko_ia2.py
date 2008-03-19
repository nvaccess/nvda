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
		self.busyFlag=True if controlTypes.STATE_BUSY in self.rootNVDAObject.states else False


	def isNVDAObjectInVirtualBuffer(self,obj):
		if not isinstance(obj,NVDAObjects.IAccessible.IA2.IA2) or not obj.windowClassName.startswith('Mozilla') or not winUser.isDescendantWindow(self.rootNVDAObject.windowHandle,obj.windowHandle):
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
			speech.speakMessage(controlTypes.speechStateLabels[controlTypes.STATE_BUSY])
			self.busyFlag=True
			return nextHandler()
		else:
			self.busyFlag=False
		if obj==self.rootNVDAObject:
			return speech.speakObjectProperties(obj,name=True)
		if role==controlTypes.ROLE_DOCUMENT:
			return
		if self.VBufHandle is None:
			return nextHandler()
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
				obj=NVDAObjects.IAccessible.IAccessible(IAccessibleObject=pacc,IAccessibleChildID=accChildID)
				obj.setFocus()
				api.setNavigatorObject(obj)
		except:
			pass

	def _activateField(self,docHandle,ID):
		try:
			pacc,accChildID=IAccessibleHandler.accessibleObjectFromEvent(docHandle,IAccessibleHandler.OBJID_CLIENT,ID)
			role=pacc.accRole(accChildID)
			if role in (IAccessibleHandler.ROLE_SYSTEM_COMBOBOX,IAccessibleHandler.ROLE_SYSTEM_TEXT,IAccessibleHandler.ROLE_SYSTEM_LIST,IAccessibleHandler.ROLE_SYSTEM_SLIDER):
				api.toggleVirtualBufferPassThrough()
			else:
				pacc.accDoDefaultAction(accChildID)
		except:
			pass

	def _searchableAttribsForNodeType(self,nodeType):
		if nodeType=="heading":
			attrs={"IAccessible::role":[IAccessibleHandler.IA2_ROLE_HEADING]}
		elif nodeType=="table":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_TABLE]}
		elif nodeType=="link":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_LINK]}
		elif nodeType=="visitedLink":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_LINK],"IAccessible::state_%d"%IAccessibleHandler.STATE_SYSTEM_TRAVERSED:[1]}
		elif nodeType=="unvisitedLink":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_LINK],"IAccessible::state_%d"%IAccessibleHandler.STATE_SYSTEM_TRAVERSED:[None]}
		elif nodeType=="formField":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_PUSHBUTTON,IAccessibleHandler.ROLE_SYSTEM_RADIOBUTTON,IAccessibleHandler.ROLE_SYSTEM_CHECKBUTTON,IAccessibleHandler.ROLE_SYSTEM_COMBOBOX,IAccessibleHandler.ROLE_SYSTEM_LIST,IAccessibleHandler.ROLE_SYSTEM_OUTLINE,IAccessibleHandler.ROLE_SYSTEM_TEXT],"IAccessible::state_%s"%IAccessibleHandler.STATE_SYSTEM_READONLY:[None]}
		else:
			return None
		# We should never consider invisible nodes.
		attrs["IAccessible::state_%s"%IAccessibleHandler.STATE_SYSTEM_INVISIBLE]=[None]
		return attrs

	def event_stateChange(self,obj,nextHandler):
		if obj==self.rootNVDAObject:
			self.rootNVDAObject=obj
		if controlTypes.STATE_BUSY in self.rootNVDAObject.states:
			speech.speakMessage(controlTypes.speechStateLabels[controlTypes.STATE_BUSY])
			self.busyFlag=True
			return
		if not self.isAlive():
			return virtualBufferHandler.killVirtualBuffer(self)
		if self.rootNVDAObject and self.busyFlag and not controlTypes.STATE_BUSY in self.rootNVDAObject.states:
			self.unloadBuffer()
			self.loadBuffer()
			self.busyFlag=False
		if obj!=self.rootNVDAObject:
			return nextHandler()

	def loadBuffer(self):
		if controlTypes.STATE_BUSY in self.rootNVDAObject.states:
			return
		super(Gecko_ia2,self).loadBuffer()

	def event_scrollingStart(self,obj,nextHandler):
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
