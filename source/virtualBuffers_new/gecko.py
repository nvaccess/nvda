from . import VirtualBuffer
from virtualBuffer_new_wrapper import *
import controlTypes
import NVDAObjects.IAccessible
import winUser
import speech
import IAccessibleHandler
import globalVars

class Gecko(VirtualBuffer):

	def _fillVBufHelper(self,pacc=None,accChildID=0,parentNode=None,previousNode=None):
		if not pacc:
			pacc=self.rootNVDAObject.IAccessibleObject
		if not parentNode:
			parentNode=self.VBufHandle
		parentParentNode=parentNode
		attrs={}
		if isinstance(pacc,IAccessibleHandler.IAccessible2):
			ID=pacc.uniqueID
			attrs['IAccessible2::role']=str(pacc.role())
		else:
			ID=id(pacc)
			attrs['IAccessible2::role']=str(0)
		attrs['IAccessible::accRole']=str(pacc.accRole(accChildID))
		attrs['IAccessible::accState']=str(pacc.accState(accChildID))
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

	def getFieldSpeech(self,attrs,fieldType,extraDetail=False):
		if not extraDetail and fieldType in ("end_relative","end_inStack") and attrs['IAccessible::accRole']==str(IAccessibleHandler.ROLE_SYSTEM_LINK): 
			return "link"
		elif not extraDetail and fieldType in ("end_relative","end_inStack") and attrs['IAccessible2::role']==str(IAccessibleHandler.IA2_ROLE_HEADING):
			return "heading"
		elif not extraDetail and fieldType in ("end_relative","end_inStack") and attrs['IAccessible::accRole']==str(IAccessibleHandler.ROLE_SYSTEM_PUSHBUTTON):
			return "button"
		elif not extraDetail and fieldType in ("end_relative","end_inStack") and attrs['IAccessible::accRole']==str(IAccessibleHandler.ROLE_SYSTEM_GRAPHIC): 
			return "graphic"
		elif extraDetail and fieldType in ("start_addedToStack","start_relative"):
			return "in %s"%attrs['IAccessible2::role']
		elif extraDetail and fieldType in ("end_removedFromStack","end_relative"):
			return "out of %s"%attrs['IAccessible2::role']
		else:
			return ""

