from textwrap import TextWrapper
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
import config

def wrapText(text):
	maxLineLength=config.conf["virtualBuffers"]["maxLineLength"]
	if len(text)>maxLineLength:
		wrapper = TextWrapper(width=maxLineLength, expand_tabs=False, replace_whitespace=False, break_long_words=False)
		text=wrapper.fill(text)
	return text

class GeckoTextInfo(VirtualBufferTextInfo):

	def getXMLFieldSpeech(self,attrs,fieldType,extraDetail=False):
		role=attrs['role']
		if role.isdigit():
			role=int(role)
		states=int(attrs['states'])
		try:
			childCount=int(attrs['childCount'])
		except:
			childCount=0
		if not extraDetail and fieldType in ("end_relative","end_inStack") and role==IAccessibleHandler.ROLE_SYSTEM_LINK: 
			return controlTypes.speechRoleLabels[controlTypes.ROLE_LINK]
		elif not extraDetail and fieldType in ("end_relative","end_inStack") and role==IAccessibleHandler.IA2_ROLE_HEADING:
			return controlTypes.speechRoleLabels[controlTypes.ROLE_HEADING]
		elif not extraDetail and fieldType in ("end_relative","end_inStack") and role==IAccessibleHandler.ROLE_SYSTEM_PUSHBUTTON:
			return controlTypes.speechRoleLabels[controlTypes.ROLE_BUTTON]
		elif not extraDetail and fieldType in ("start_addedToStack","start_relative") and role==IAccessibleHandler.ROLE_SYSTEM_TEXT and not states&IAccessibleHandler.STATE_SYSTEM_READONLY:
			return controlTypes.speechRoleLabels[controlTypes.ROLE_EDITABLETEXT]
		elif not extraDetail and fieldType in ("end_relative","end_inStack") and role==IAccessibleHandler.ROLE_SYSTEM_GRAPHIC: 
			return controlTypes.speechRoleLabels[controlTypes.ROLE_GRAPHIC]
		elif not extraDetail and fieldType=="start_addedToStack" and role==IAccessibleHandler.ROLE_SYSTEM_LISTITEM:
			return _("bullet")
		elif not extraDetail and fieldType=="start_addedToStack" and role==IAccessibleHandler.ROLE_SYSTEM_LIST:
			return _("%s with %s items")%(controlTypes.speechRoleLabels[controlTypes.ROLE_LIST],childCount)
		elif not extraDetail and fieldType=="end_removedFromStack" and role==IAccessibleHandler.ROLE_SYSTEM_LIST:
			return _("out of %s")%controlTypes.speechRoleLabels[controlTypes.ROLE_LIST]
		elif not extraDetail and fieldType=="start_addedToStack" and role in ("frame",IAccessibleHandler.IA2_ROLE_FRAME):
			return controlTypes.speechRoleLabels[controlTypes.ROLE_FRAME]
		elif not extraDetail and fieldType=="end_removedFromStack" and role in ("frame",IAccessibleHandler.IA2_ROLE_FRAME):
			return _("out of %s")%controlTypes.speechRoleLabels[controlTypes.ROLE_FRAME]
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
		attrs={}
		if isinstance(pacc,IAccessibleHandler.IAccessible2):
			ID=pacc.uniqueID
			attrs['role']=str(pacc.role())
		else:
			attrs['level']='0'
			ID=hash(pacc)
			attrs['role']=str(pacc.accRole(accChildID))
		attrs['states']=str(pacc.accState(accChildID))
		children=[] #will be strings  or pacc,childID tuples
		paccChildCount=0
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
				globalVars.log.warning("error in IAccessibleText::text, role %s"%pacc.role(),exc_info=True)
				text=""
		if paccText and text:
			try:
				paccHypertext=pacc.QueryInterface(IAccessibleHandler.IAccessibleHypertext)
			except:
				globalVars.log.warning("no IAccessibleHypertext",exc_info=True)
				paccHypertext=None
			offset=0
			plainText=u""
			for ch in text:
				if ord(ch)!=0xfffc:
					plainText+=ch
				elif paccHypertext:
					if plainText and not plainText.isspace():
						children.append(unicode(u"%s\n"%wrapText(plainText)))
					plainText=u""
					try:
						index=paccHypertext.hyperlinkIndex(offset)
						paccHyperlink=paccHypertext.hyperlink(index)
					except:
						paccHyperlink=None
					if paccHyperlink:
						newPacc=IAccessibleHandler.normalizeIAccessible(paccHyperlink)
						children.append((newPacc,0))
						paccChildCount+=1
				offset+=1
			if plainText and (paccChildCount==0 and not plainText.isspace()):
				children.append(unicode(u"%s\n"%wrapText(plainText)))
		elif accChildID==0 and pacc.accChildCount>0:
			children=IAccessibleHandler.accessibleChildren(pacc,0,pacc.accChildCount)
			paccChildCount=len(children)
		else:
			text=pacc.accValue(accChildID)
			if not text:
				text=pacc.accName(accChildID)
			if text:
				children.append(u"%s\n"%wrapText(text))
		attrs['childCount']=str(paccChildCount)
		del pacc
		parentNode=VBufStorage_addTagNodeToBuffer(parentNode,previousNode,ID,attrs)
		previousNode=None
		for child in children:
			if isinstance(child,basestring):
				previousNode=VBufStorage_addTextNodeToBuffer(parentNode,previousNode,0,child)
			elif isinstance(child,tuple) and len(child)==2:
				previousNode=self._fillVBufHelper(child[0],child[1],parentNode,previousNode)
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
