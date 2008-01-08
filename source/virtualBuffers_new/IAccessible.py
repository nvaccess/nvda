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

class IAccessibleTextInfo(VirtualBufferTextInfo):

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
			visitedText=controlTypes.speechStateLabels[controlTypes.STATE_VISITED] if states&IAccessibleHandler.STATE_SYSTEM_TRAVERSED else ""
			return "%s %s"%(visitedText,controlTypes.speechRoleLabels[controlTypes.ROLE_LINK])
		elif not extraDetail and fieldType in ("end_relative","end_inStack") and role in (IAccessibleHandler.IA2_ROLE_HEADING,"h1","h2","h3","h4","h5","h6"):
			return controlTypes.speechRoleLabels[controlTypes.ROLE_HEADING]
		elif not extraDetail and fieldType in ("end_relative","end_inStack") and role==IAccessibleHandler.ROLE_SYSTEM_PUSHBUTTON:
			return controlTypes.speechRoleLabels[controlTypes.ROLE_BUTTON]
		elif not extraDetail and fieldType in ("end_relative","end_inStack") and role==IAccessibleHandler.ROLE_SYSTEM_RADIOBUTTON:
			stateText=controlTypes.speechStateLabels[controlTypes.STATE_CHECKED] if states&IAccessibleHandler.STATE_SYSTEM_CHECKED else ""
			return "%s %s"%(controlTypes.speechRoleLabels[controlTypes.ROLE_RADIOBUTTON],stateText)
		elif not extraDetail and fieldType in ("end_relative","end_inStack") and role==IAccessibleHandler.ROLE_SYSTEM_CHECKBUTTON:
			stateText=controlTypes.speechStateLabels[controlTypes.STATE_CHECKED] if states&IAccessibleHandler.STATE_SYSTEM_CHECKED else ""
			return "%s %s"%(controlTypes.speechRoleLabels[controlTypes.ROLE_CHECKBOX],stateText)
		elif not extraDetail and fieldType in ("start_addedToStack","start_relative") and role==IAccessibleHandler.ROLE_SYSTEM_TEXT and not states&IAccessibleHandler.STATE_SYSTEM_READONLY:
			return controlTypes.speechRoleLabels[controlTypes.ROLE_EDITABLETEXT]
		elif not extraDetail and fieldType in ("start_addedToStack","start_relative") and role==IAccessibleHandler.ROLE_SYSTEM_COMBOBOX:
			return controlTypes.speechRoleLabels[controlTypes.ROLE_COMBOBOX]
		elif not extraDetail and fieldType in ("end_relative","end_inStack") and role==IAccessibleHandler.ROLE_SYSTEM_GRAPHIC: 
			return controlTypes.speechRoleLabels[controlTypes.ROLE_GRAPHIC]
		elif not extraDetail and fieldType in ("start_addedToStack","start_relative") and role==IAccessibleHandler.ROLE_SYSTEM_LISTITEM:
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

class IAccessible(VirtualBuffer):

	def __init__(self,rootNVDAObject):
		super(IAccessible,self).__init__(rootNVDAObject,TextInfo=IAccessibleTextInfo)

	def _fillVBufHelper(self,pacc=None,accChildID=0,parentNode=None,previousNode=None):
		if not pacc:
			pacc=self.rootNVDAObject.IAccessibleObject
		if not parentNode:
			parentNode=self.VBufHandle
		attrs={}
		isBlockElement=True
		if isinstance(pacc,IAccessibleHandler.IAccessible2):
			ID=pacc.uniqueID
			globalVars.log.debug("ID %s"%ID)
			role=pacc.role()
			globalVars.log.debug("IA2 attribs %s"%pacc.attributes)
			objAttributes=pacc.attributes
			if role!=IAccessibleHandler.ROLE_SYSTEM_CELL and objAttributes.find("formatting:block")<0:
				isBlockElement=False
		else:
			ID=-hash(pacc)
			role=pacc.accRole(accChildID)
		states=pacc.accState(accChildID)
		attrs['role']=str(role)
		attrs['states']=str(states)
		children=[] #will be strings  or pacc,childID tuples
		paccChildCount=0
		if not accChildID and isinstance(pacc,IAccessibleHandler.IAccessible2) and role!=IAccessibleHandler.ROLE_SYSTEM_COMBOBOX:
			try:
				paccText=pacc.QueryInterface(IAccessibleHandler.IAccessibleText)
			except:
				globalVars.log.debug("no IAccessibleText",exc_info=True)
				paccText=None
		else:
			paccText=None
		if paccText:
			try:
				text=paccText.text(0,-1)
			except:
				globalVars.log.debug("error in IAccessibleText::text, role %s"%pacc.role(),exc_info=True)
				text=""
		else:
			text=""
		if paccText and text:
			try:
				paccHypertext=pacc.QueryInterface(IAccessibleHandler.IAccessibleHypertext)
			except:
				globalVars.log.debug("no IAccessibleHypertext",exc_info=True)
				paccHypertext=None
			offset=0
			plainText=u""
			for ch in text:
				if not paccHypertext or ord(ch)!=0xfffc:
					plainText+=ch
				else:
					if plainText:
						children.append(plainText)
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
			if plainText:
				children.append(plainText)
		elif role!=IAccessibleHandler.ROLE_SYSTEM_COMBOBOX and accChildID==0 and pacc.accChildCount>0:
			children=IAccessibleHandler.accessibleChildren(pacc,0,pacc.accChildCount)
			paccChildCount=len(children)
		else:
			name=pacc.accName(accChildID)
			value=pacc.accValue(accChildID)
			description=pacc.accDescription(accChildID)
			if name:
				text=name
			else:
				text=value
			if text:
				children.append(text)
		attrs['childCount']=str(paccChildCount)
		del pacc
		parentNode=VBufStorage_addTagNodeToBuffer(parentNode,previousNode,ID,attrs,isBlockElement)
		previousNode=None
		for child in children:
			if isinstance(child,basestring):
				previousNode=VBufStorage_addTextNodeToBuffer(parentNode,previousNode,0,child)
			else:
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
			nextHandler()
			if not IAccessibleHandler.STATE_SYSTEM_BUSY in states and obj!=self.rootNVDAObject:
				self.rootNVDAObject=obj
				self.fillVBuf()
			return
		#We only want to update the caret and speak the field if we're not in the same one as before
		oldInfo=self.makeTextInfo(textHandler.POSITION_CARET)
		oldID=VBufStorage_getFieldIDFromBufferOffset(self.VBufHandle,oldInfo._startOffset)
		ID=obj.IAccessibleObject.uniqueID if isinstance(obj.IAccessibleObject,IAccessibleHandler.IAccessible2) else -hash(obj.IAccessibleObject)
		if ID!=oldID and ID!=0:
			try:
				start,end=VBufStorage_getBufferOffsetsFromFieldID(self.VBufHandle,ID)
			except:
				return nextHandler()
			newInfo=self.makeTextInfo(textHandler.Bookmark(self.TextInfo,(start,end)))
			startToStart=newInfo.compareEndPoints(oldInfo,"startToStart")
			startToEnd=newInfo.compareEndPoints(oldInfo,"startToEnd")
			endToStart=newInfo.compareEndPoints(oldInfo,"endToStart")
			endToEnd=newInfo.compareEndPoints(oldInfo,"endToEnd")
			if (startToStart<0 and endToEnd>0) or (startToStart>0 and endToEnd<0) or endToStart<0 or startToEnd>0:  
				speech.speakFormattedTextWithXML(newInfo.XMLContext,newInfo.XMLText,self,newInfo.getXMLFieldSpeech)
				newInfo.collapse()
				newInfo.updateCaret()


	def activatePosition(self,ID):
		pacc,accChildID=IAccessibleHandler.accChild(self.rootNVDAObject.IAccessibleObject,ID)
		speech.speakMessage("pacc: %s"%pacc)
		speech.speakMessage("accChildID: %s"%accChildID)
		speech.speakMessage("name: %s"%pacc.accName(accChildID))
		pacc.accDoDefaultAction(accChildID)

	def _caretMovedToID(self,ID):
		try:
			pacc,accChildID=IAccessibleHandler.accChild(self.rootNVDAObject.IAccessibleObject,ID)
			pacc.accSelect(1,accChildID)
		except:
			pass

	def _activateID(self,ID):
		try:
			pacc,accChildID=IAccessibleHandler.accChild(self.rootNVDAObject.IAccessibleObject,ID)
			role=pacc.accRole(accChildID)
			if role in (IAccessibleHandler.ROLE_SYSTEM_COMBOBOX,IAccessibleHandler.ROLE_SYSTEM_TEXT,IAccessibleHandler.ROLE_SYSTEM_LIST):
				api.toggleVirtualBufferPassThrough()
			else:
				pacc.accDoDefaultAction(accChildID)
		except:
			pass

	def _searchableAttribsForNodeType(self,nodeType):
		if nodeType==_("heading"):
			return {"role":["heading","h1","h2","h3","h4","h5","h6",str(IAccessibleHandler.IA2_ROLE_HEADING)]}
		elif nodeType==_("link"):
			return {"role":["link",str(IAccessibleHandler.ROLE_SYSTEM_LINK)]}
		else:
			return None

