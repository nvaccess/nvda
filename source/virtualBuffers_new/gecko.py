from . import VirtualBuffer, VirtualBufferTextInfo
from virtualBuffer_new_wrapper import *
import controlTypes
import NVDAObjects.IAccessible
import winUser
import speech
import IAccessibleHandler
import globalVars
import api
import textHandler

class GeckoTextInfo(VirtualBufferTextInfo):

	def getXMLFieldSpeech(self,attrs,fieldType,extraDetail=False):
		role=attrs['role']
		if role.isdigit():
			role=int(role)
		if not extraDetail and fieldType in ("end_relative","end_inStack") and role==IAccessibleHandler.ROLE_SYSTEM_LINK: 
			return controlTypes.speechRoleLabels[controlTypes.ROLE_LINK]
		elif not extraDetail and fieldType in ("end_relative","end_inStack") and role==IAccessibleHandler.IA2_ROLE_HEADING:
			return controlTypes.speechRoleLabels[controlTypes.ROLE_HEADING]
		elif not extraDetail and fieldType in ("end_relative","end_inStack") and role==IAccessibleHandler.ROLE_SYSTEM_PUSHBUTTON:
			return controlTypes.speechRoleLabels[controlTypes.ROLE_BUTTON]
		elif not extraDetail and fieldType in ("end_relative","end_inStack") and role==IAccessibleHandler.ROLE_SYSTEM_GRAPHIC: 
			return controlTypes.speechRoleLabels[controlTypes.ROLE_GRAPHIC]
		elif extraDetail and fieldType in ("start_addedToStack","start_relative"):
			return _("in %s")%controlTypes.speechRoleLabels[IAccessibleHandler.IAccessibleRolesToNVDARoles.get(role,0)]
		elif extraDetail and fieldType in ("end_removedFromStack","end_relative"):
			return _("out of %s")%controlTypes.speechRoleLabels[IAccessibleHandler.IAccessibleRolesToNVDARoles.get(role,0)]
		else:
			return ""

class Gecko(VirtualBuffer):

	def __init__(self,rootNVDAObject):
		super(Gecko,self).__init__(rootNVDAObject,TextInfo=GeckoTextInfo)

	def _fillVBufHelper(self,pacc=None,accChildID=0,parentNode=None,previousNode=None):
		if not pacc:
			pacc=self.rootNVDAObject.IAccessibleObject
		if not parentNode:
			parentNode=self.VBufHandle
		parentParentNode=parentNode
		attrs={}
		if isinstance(pacc,IAccessibleHandler.IAccessible2):
			ID=pacc.uniqueID
			attrs['role']=str(pacc.role())
		else:
			ID=hash(pacc)
			attrs['role']=str(pacc.accRole(accChildID))
		attrs['states']=str(pacc.accState(accChildID))
		parentNode=VBufStorage_addTagNodeToBuffer(parentNode,previousNode,ID,attrs)
		previousNode=None
		if not accChildID and isinstance(pacc,IAccessibleHandler.IAccessible2):
			try:
				paccText=pacc.QueryInterface(IAccessibleHandler.IAccessibleText)
			except:
				globalVars.log.warning("no IAccessibleText",exc_info=True)
				paccText=None
		else:
			paccText=None
		if paccText:
			try:
				text=paccText.text(0,-1)
				text=text.replace('\n',"").replace('\r',"")
			except:
				globalVars.log.warning("error in IAccessibleText::text",exc_info=True)
				text=""
		if paccText and text:
			try:
				paccHypertext=pacc.QueryInterface(IAccessibleHandler.IAccessibleHypertext)
			except:
				globalVars.log.warning("no IAccessibleHypertext",exc_info=True)
				paccHypertext=None
			count=0
			plainText=u""
			for ch in text:
				if ord(ch)!=0xfffc:
					plainText+=ch
				elif paccHypertext:
					if plainText:
						previousNode=VBufStorage_addTextNodeToBuffer(parentNode,previousNode,0,unicode(u"%s\n"%plainText))
					plainText=u""
					try:
						paccHyperlink=paccHypertext.hyperlink(paccHypertext.hyperlinkIndex(count))
					except:
						paccHyperlink=None
					if paccHyperlink:
						newPacc=IAccessibleHandler.normalizeIAccessible(paccHyperlink)
						previousNode=self._fillVBufHelper(newPacc,0,parentNode,previousNode)
				count+=1
			if plainText:
				previousNode=VBufStorage_addTextNodeToBuffer(parentNode,previousNode,0,unicode(u"%s\n"%plainText))
		elif accChildID==0 and pacc.accChildCount>0:
			children=IAccessibleHandler.accessibleChildren(pacc,0,pacc.accChildCount)
			for newPacc,newAccChildID in children:
				previousNode=self._fillVBufHelper(newPacc,newAccChildID,parentNode,previousNode)
		else:
			text=pacc.accName(accChildID)
			if not text:
				text=pacc.accValue(accChildID)
			if not text:
				text=pacc.accDescription(accChildID)
			if text:
				previousNode=VBufStorage_addTextNodeToBuffer(parentNode,previousNode,0,u"%s\n"%text)
		return parentNode

	def isNVDAObjectInVirtualBuffer(self,obj):
		root=self.rootNVDAObject
		if root and obj and isinstance(obj,NVDAObjects.IAccessible.IAccessible) and winUser.isDescendantWindow(root.windowHandle,obj.windowHandle): 
			return True

	def isAlive(self):
		root=self.rootNVDAObject
		if root and winUser.isWindow(root.windowHandle):
			return True

	def event_focusEntered(self,obj,nextHandler):
		pass

	def event_gainFocus(self,obj,nextHandler):
		api.setNavigatorObject(obj)
		role=obj.role
		states=obj.states
		if role==controlTypes.ROLE_DOCUMENT:
			if controlTypes.STATE_BUSY in states:
				speech.speakMessage(controlTypes.speechRoleLabels[controlTypes.STATE_BUSY])
			elif obj!=self.rootNVDAObject:
				self.rootNVDAObject=obj
				self.fillVBuf()
		ID=obj.IAccessibleObject.uniqueID if isinstance(obj.IAccessibleObject,IAccessibleHandler.IAccessible2) else hash(obj.IAccessibleObject)
		try:
			start,end=VBufStorage_getBufferOffsetsFromFieldID(self.VBufHandle,ID)
		except:
			return nextHandler()
		info=self.makeTextInfo(textHandler.Bookmark(self.TextInfo,(start,end)))
		speech.speakFormattedTextWithXML(info.XMLContext,info.XMLText,self,info.getXMLFieldSpeech)
		VBufStorage_setBufferSelectionOffsets(self.VBufHandle,start,end)
