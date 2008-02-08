import weakref
import time
import winsound
import baseObject
import speech
import NVDAObjects
import winUser
import sayAllHandler
import controlTypes
import textHandler
from virtualBuffer_new_wrapper import *
import globalVars
import config
import api
import cursorManager

class VirtualBufferTextInfo(NVDAObjects.NVDAObjectTextInfo):

	hasXML=True

	def _getSelectionOffsets(self):
		start,end=VBufStorage_getBufferSelectionOffsets(self.obj.VBufHandle)
		return (start,end)

	def _setSelectionOffsets(self,start,end):
		VBufStorage_setBufferSelectionOffsets(self.obj.VBufHandle,start,end)

	def _getCaretOffset(self):
		return self._getSelectionOffsets()[0]

	def _setCaretOffset(self,offset):
		return self._setSelectionOffsets(offset,offset)

	def _getStoryLength(self):
		return VBufStorage_getBufferTextLength(self.obj.VBufHandle)

	def _getTextRange(self,start,end):
		text=VBufStorage_getBufferTextByOffsets(self.obj.VBufHandle,start,end)
		return text

	def _getLineOffsets(self,offset):
		return VBufStorage_getBufferLineOffsets(self.obj.VBufHandle,offset,config.conf["virtualBuffers"]["maxLineLength"],self.obj._useScreenLayout)

	def _get_XMLContext(self):
		return VBufStorage_getXMLContextAtBufferOffset(self.obj.VBufHandle,self._startOffset)

	def _get_XMLText(self):
		start=self._startOffset
		end=self._endOffset
		text=VBufStorage_getXMLBufferTextByOffsets(self.obj.VBufHandle,start,end)
		return text

	def getXMLFieldSpeech(self,attrs,fieldType,extraDetail=False,reason=None):
		childCount=int(attrs['_childcount'])
		indexInParent=int(attrs['_indexinparent'])
		parentChildCount=int(attrs['_parentchildcount'])
		role=attrs['role']
		states=attrs['states']
		keyboardShortcut=attrs['keyboardshortcut']
		roleText=speech.getSpeechTextForProperties(reason=reason,role=role)
		stateText=speech.getSpeechTextForProperties(reason=reason,states=states,_role=role)
		keyboardShortcutText=speech.getSpeechTextForProperties(reason=reason,keyboardShortcut=keyboardShortcut)
		if not extraDetail and ((reason==speech.REASON_FOCUS and fieldType in ("end_relative","end_inStack")) or (reason in (speech.REASON_CARET,speech.REASON_SAYALL) and fieldType in ("start_addedToStack","start_relative"))) and role in (controlTypes.ROLE_LINK,controlTypes.ROLE_HEADING,controlTypes.ROLE_BUTTON,controlTypes.ROLE_RADIOBUTTON,controlTypes.ROLE_CHECKBOX,controlTypes.ROLE_GRAPHIC):
			if role==controlTypes.ROLE_LINK:
				return " ".join([x for x in stateText,roleText,keyboardShortcutText])
			else:
				return " ".join([x for x in roleText,stateText,keyboardShortcutText if x])
		elif not extraDetail and fieldType in ("start_addedToStack","start_relative") and role==controlTypes.ROLE_EDITABLETEXT and not controlTypes.STATE_READONLY in states: 
			return " ".join([x for x in stateText,roleText,keyboardShortcutText if x])
		elif not extraDetail and fieldType=="start_addedToStack" and role==controlTypes.ROLE_LIST and controlTypes.STATE_READONLY in states:
			return roleText+_("with %s items")%childCount
		elif not extraDetail and fieldType=="end_removedFromStack" and role==controlTypes.ROLE_LIST and controlTypes.STATE_READONLY in states:
			return _("out of %s")%roleText
		elif not extraDetail and fieldType in ("start_addedToStack","start_relative") and role in (controlTypes.ROLE_LIST,controlTypes.ROLE_COMBOBOX):
			return " ".join([x for x in roleText,stateText,keyboardShortcutText if x])
		elif not extraDetail and fieldType in ("start_addedToStack","start_relative") and role==controlTypes.ROLE_LISTITEM:
			return _("bullet")
		elif not extraDetail and fieldType=="start_addedToStack" and role in (controlTypes.ROLE_FRAME,controlTypes.ROLE_INTERNALFRAME):
			return " ".join([x for x in roleText,stateText,keyboardShortcutText if x])
		elif not extraDetail and fieldType=="end_removedFromStack" and role in (controlTypes.ROLE_FRAME,controlTypes.ROLE_INTERNALFRAME):
			return _("out of %s")%roleText
		elif extraDetail and fieldType in ("start_addedToStack","start_relative"):
			return _("in %s")%roleText
		elif extraDetail and fieldType in ("end_removedFromStack","end_relative"):
			return _("out of %s")%roleText
		else:
			return ""

class VirtualBuffer(cursorManager.CursorManager):

	def __init__(self,rootNVDAObject,TextInfo=VirtualBufferTextInfo):
		self.TextInfo=TextInfo
		self.rootNVDAObject=rootNVDAObject
		self.VBufHandle=VBufStorage_createBuffer()
		self.fillVBuf()
		super(VirtualBuffer,self).__init__()
		self._useScreenLayout=True

	def __del__(self):
		VBufStorage_destroyBuffer(self.VBufHandle)

	def makeTextInfo(self,position):
		return self.TextInfo(self,position)

	def isNVDAObjectInVirtualBuffer(self,obj):
		pass

	def isAlive(self):
		pass

	def _calculateLineBreaks(self,text):
		maxLineLength=config.conf["virtualBuffers"]["maxLineLength"]
		lastBreak=0
		lineBreakOffsets=[]
		for offset in range(len(text)):
			if offset-lastBreak>maxLineLength and offset>0 and text[offset-1].isspace() and not text[offset].isspace():
				lineBreakOffsets.append(offset)
				lastBreak=offset
		return lineBreakOffsets

	def _fillVBufHelper(self):
		pass

	def fillVBuf(self):
		if api.isVirtualBufferPassThrough():
			api.toggleVirtualBufferPassThrough()
		VBufStorage_clearBuffer(self.VBufHandle)
		if hasattr(self,'_speech_XMLCache'):
			del self._speech_XMLCache
		startTime=time.time()
		speech.cancelSpeech()
		speech.speakMessage(_("Loading document..."))
		self._fillVBufHelper()
		endTime=time.time()
		globalVars.log.debug("load took %s seconds"%(endTime-startTime))
		speech.cancelSpeech()
		speech.speakMessage(_("Done"))
		api.processPendingEvents()
		info=self.makeTextInfo(textHandler.POSITION_FIRST)
		sayAllHandler.readText(info,sayAllHandler.CURSOR_CARET)

	def _activateField(self,docHandle,ID):
		pass

	def _activateContextMenuForField(self,docHandle,ID):
		pass

	def _caretMovedToField(self,dochandle,ID):
		pass

	def script_activatePosition(self,keyPress,nextScript):
		start,end=VBufStorage_getBufferSelectionOffsets(self.VBufHandle)
		docHandle,ID=VBufStorage_getFieldIdentifierFromBufferOffset(self.VBufHandle,start)
		self._activateField(docHandle,ID)
	script_activatePosition.__doc__ = _("activates the current object in the virtual buffer")

	def _caretMovementScriptHelper(self, *args, **kwargs):
		oldDocHandle,oldID=VBufStorage_getFieldIdentifierFromBufferOffset(self.VBufHandle,self.caret._startOffset)
		super(VirtualBuffer, self)._caretMovementScriptHelper(*args, **kwargs)
		docHandle,ID=VBufStorage_getFieldIdentifierFromBufferOffset(self.VBufHandle,self.caret._startOffset)
		if ID!=0 and (docHandle!=oldDocHandle or ID!=oldID):
			self._caretMovedToField(docHandle,ID)

	def script_refreshBuffer(self,keyPress,nextScript):
		self.fillVBuf()

	def script_toggleScreenLayout(self,keyPress,nextScript):
		self._useScreenLayout=not self._useScreenLayout
		onOff=_("on") if self._useScreenLayout else _("off")
		speech.speakMessage(_("use screen layout %s")%onOff)

	def _searchableAttributesForNodeType(self,nodeType):
		pass

	def _jumpToNodeType(self,nodeType,direction):
		attribs=self._searchableAttribsForNodeType(nodeType)
		if attribs:
			startOffset,endOffset=VBufStorage_getBufferSelectionOffsets(self.VBufHandle)
			try:
				newDocHandle,newID=VBufStorage_findBufferFieldIdentifierByProperties(self.VBufHandle,direction,startOffset,attribs)
			except:
				return False
		if not newID or not attribs:
			return False
		startOffset,endOffset=VBufStorage_getBufferOffsetsFromFieldIdentifier(self.VBufHandle,newDocHandle,newID)
		info=self.makeTextInfo(textHandler.Bookmark(self.TextInfo,(startOffset,endOffset)))
		info.updateCaret()
		speech.speakFormattedTextWithXML(info.XMLContext,info.XMLText,info.obj,info.getXMLFieldSpeech,reason=speech.REASON_FOCUS)
		self._caretMovedToField(newDocHandle,newID)
		return True

	def script_nextHeading(self,keyPress,nextScript):
		if not self._jumpToNodeType("heading","next"):
			speech.speakMessage(_("no next heading"))
	script_nextHeading.__doc__ = _("moves to the next heading")

	def script_previousHeading(self,keyPress,nextScript):
		if not self._jumpToNodeType("heading","previous"):
			speech.speakMessage(_("no previous heading"))
	script_previousHeading.__doc__ = _("moves to the previous heading")

	def script_nextLink(self,keyPress,nextScript):
		if not self._jumpToNodeType("link","next"):
			speech.speakMessage(_("no next link"))
	script_nextLink.__doc__ = _("moves to the next link")

	def script_previousLink(self,keyPress,nextScript):
		if not self._jumpToNodeType("link","previous"):
			speech.speakMessage(_("no previous link"))
	script_previousLink.__doc__ = _("moves to the previous link")

	def script_nextVisitedLink(self,keyPress,nextScript):
		if not self._jumpToNodeType("visitedLink","next"):
			speech.speakMessage(_("no next visited link"))
	script_nextLink.__doc__ = _("moves to the next visited link")

	def script_previousVisitedLink(self,keyPress,nextScript):
		if not self._jumpToNodeType("visitedLink","previous"):
			speech.speakMessage(_("no previous visited link"))
	script_previousLink.__doc__ = _("moves to the previous visited link")

	def script_nextUnvisitedLink(self,keyPress,nextScript):
		if not self._jumpToNodeType("unvisitedLink","next"):
			speech.speakMessage(_("no next unvisited link"))
	script_nextUnvisitedLink.__doc__ = _("moves to the next unvisited link")

	def script_previousUnvisitedLink(self,keyPress,nextScript):
		if not self._jumpToNodeType("unvisitedLink","previous"):
			speech.speakMessage(_("no previous unvisited link"))
	script_previousUnvisitedLink.__doc__ = _("moves to the previous unvisited link")

	def script_nextFormField(self,keyPress,nextScript):
		if not self._jumpToNodeType("formField","next"):
			speech.speakMessage(_("no next form field"))
	script_nextFormField.__doc__ = _("moves to the next form field")

	def script_previousFormField(self,keyPress,nextScript):
		if not self._jumpToNodeType("formField","previous"):
			speech.speakMessage(_("no previous form field"))
	script_previousFormField.__doc__ = _("moves to the next form field")

[VirtualBuffer.bindKey(keyName,scriptName) for keyName,scriptName in [
	("Return","activatePosition"),
	("Space","activatePosition"),
	("NVDA+f5","refreshBuffer"),
	("NVDA+v","toggleScreenLayout"),
	("h","nextHeading"),
	("shift+h","previousHeading"),
	("k","nextLink"),
	("shift+k","previousLink"),
	("v","nextVisitedLink"),
	("shift+v","previousVisitedLink"),
	("u","nextUnvisitedLink"),
	("shift+u","previousUnvisitedLink"),
	("f","nextFormField"),
	("shift+f","previousFormField"),
]]
