import weakref
import time
import os
import winsound
import baseObject
from keyUtils import sendKey
from scriptHandler import isScriptWaiting
import speech
import NVDAObjects
import winUser
import api
import sayAllHandler
import controlTypes
import textHandler
from virtualBuffer_lib import *
import globalVars
import config
import api
import cursorManager
from gui import scriptUI
import virtualBufferHandler

class VirtualBufferTextInfo(NVDAObjects.NVDAObjectTextInfo):

	hasXML=True

	def _getSelectionOffsets(self):
		start,end=VBufClient_getBufferSelectionOffsets(self.obj.VBufHandle)
		return (start,end)

	def _setSelectionOffsets(self,start,end):
		VBufClient_setBufferSelectionOffsets(self.obj.VBufHandle,start,end)

	def _getCaretOffset(self):
		return self._getSelectionOffsets()[0]

	def _setCaretOffset(self,offset):
		return self._setSelectionOffsets(offset,offset)

	def _getStoryLength(self):
		return VBufClient_getBufferTextLength(self.obj.VBufHandle)

	def _getTextRange(self,start,end):
		text=VBufClient_getBufferTextByOffsets(self.obj.VBufHandle,start,end)
		return text

	def _getLineOffsets(self,offset):
		return VBufClient_getBufferLineOffsets(self.obj.VBufHandle,offset,config.conf["virtualBuffers"]["maxLineLength"],config.conf["virtualBuffers"]["useScreenLayout"])

	def _getParagraphOffsets(self,offset):
		return VBufClient_getBufferLineOffsets(self.obj.VBufHandle,offset,0,True)

	def _get_XMLContext(self):
		return VBufClient_getXMLContextAtBufferOffset(self.obj.VBufHandle,self._startOffset)

	def _get_XMLText(self):
		start=self._startOffset
		end=self._endOffset
		text=VBufClient_getXMLBufferTextByOffsets(self.obj.VBufHandle,start,end)
		return text

	def getXMLFieldSpeech(self,attrs,fieldType,extraDetail=False,reason=None):
		childCount=int(attrs['_childcount'])
		indexInParent=int(attrs['_indexinparent'])
		parentChildCount=int(attrs['_parentchildcount'])
		if reason==speech.REASON_FOCUS:
			name=attrs.get('name',"")
		else:
			name=""
		role=attrs['role']
		states=attrs['states']
		keyboardShortcut=attrs['keyboardshortcut']
		level=attrs.get('level',None)
		roleText=speech.getSpeechTextForProperties(reason=reason,role=role)
		stateText=speech.getSpeechTextForProperties(reason=reason,states=states,_role=role)
		keyboardShortcutText=speech.getSpeechTextForProperties(reason=reason,keyboardShortcut=keyboardShortcut)
		nameText=speech.getSpeechTextForProperties(reason=reason,name=name)
		levelText=speech.getSpeechTextForProperties(reason=reason,level=level)
		if not extraDetail and ((reason==speech.REASON_FOCUS and fieldType in ("end_relative","end_inStack")) or (reason in (speech.REASON_CARET,speech.REASON_SAYALL) and fieldType in ("start_inStack","start_addedToStack","start_relative"))) and role in (controlTypes.ROLE_LINK,controlTypes.ROLE_HEADING,controlTypes.ROLE_BUTTON,controlTypes.ROLE_RADIOBUTTON,controlTypes.ROLE_CHECKBOX,controlTypes.ROLE_GRAPHIC,controlTypes.ROLE_SEPARATOR,controlTypes.ROLE_SLIDER):
			if role==controlTypes.ROLE_LINK:
				return " ".join([x for x in stateText,roleText,keyboardShortcutText])
			else:
				return " ".join([x for x in nameText,roleText,stateText,levelText,keyboardShortcutText if x])
		elif not extraDetail and fieldType in ("start_addedToStack","start_relative","start_inStack") and role==controlTypes.ROLE_EDITABLETEXT and not controlTypes.STATE_READONLY in states and not controlTypes.STATE_MULTILINE in states: 
			return " ".join([x for x in nameText,roleText,stateText,keyboardShortcutText if x])
		elif not extraDetail and fieldType in ("start_addedToStack","start_relative") and role==controlTypes.ROLE_EDITABLETEXT and not controlTypes.STATE_READONLY in states and controlTypes.STATE_MULTILINE in states: 
			return " ".join([x for x in nameText,roleText,stateText,keyboardShortcutText if x])
		elif not extraDetail and fieldType in ("end_removedFromStack") and role==controlTypes.ROLE_EDITABLETEXT and not controlTypes.STATE_READONLY in states and controlTypes.STATE_MULTILINE in states: 
			return _("out of %s")%roleText
		elif not extraDetail and fieldType=="start_addedToStack" and reason in (speech.REASON_CARET,speech.REASON_SAYALL) and role==controlTypes.ROLE_LIST and controlTypes.STATE_READONLY in states:
			return roleText+_("with %s items")%childCount
		elif not extraDetail and fieldType=="end_removedFromStack" and reason in (speech.REASON_CARET,speech.REASON_SAYALL) and role==controlTypes.ROLE_LIST and controlTypes.STATE_READONLY in states:
			return _("out of %s")%roleText
		elif not extraDetail and fieldType=="start_addedToStack" and role==controlTypes.ROLE_BLOCKQUOTE:
			return roleText
		elif not extraDetail and fieldType=="end_removedFromStack" and role==controlTypes.ROLE_BLOCKQUOTE:
			return _("out of %s")%roleText
		elif not extraDetail and fieldType in ("start_addedToStack","start_relative") and ((role==controlTypes.ROLE_LIST and controlTypes.STATE_READONLY not in states) or  role==controlTypes.ROLE_COMBOBOX):
			return " ".join([x for x in roleText,stateText,keyboardShortcutText if x])
		elif not extraDetail and fieldType=="start_addedToStack" and role in (controlTypes.ROLE_FRAME,controlTypes.ROLE_INTERNALFRAME):
			return " ".join([x for x in roleText,stateText,keyboardShortcutText if x])
		elif not extraDetail and fieldType=="end_removedFromStack" and role in (controlTypes.ROLE_FRAME,controlTypes.ROLE_INTERNALFRAME):
			return _("out of %s")%roleText
		elif extraDetail and fieldType in ("start_addedToStack","start_relative") and roleText:
			return _("in %s")%roleText
		elif extraDetail and fieldType in ("end_removedFromStack","end_relative") and roleText:
			return _("out of %s")%roleText
		else:
			return ""

class VirtualBuffer(cursorManager.CursorManager):

	def __init__(self,rootNVDAObject,backendLibPath=None,TextInfo=VirtualBufferTextInfo):
		self.backendLibPath=os.path.abspath(backendLibPath)
		self.TextInfo=TextInfo
		self.rootNVDAObject=rootNVDAObject
		super(VirtualBuffer,self).__init__()
		self.VBufHandle=None
		self.passThrough=False
		self.rootWindowHandle=self.rootNVDAObject.windowHandle
		self.rootID=0

	def loadBuffer(self):
		try:
			self.VBufHandle=VBufClient_createBuffer(self.rootWindowHandle,self.rootID,self.backendLibPath)
		except:
			return virtualBufferHandler.killVirtualBuffer(self)
		focusObject=api.getFocusObject()
		if self.isNVDAObjectInVirtualBuffer(focusObject):
			speech.cancelSpeech()
			if self.passThrough:
				self.passThrough=False
				virtualBufferHandler.reportPassThrough(self)
			info=self.makeTextInfo(textHandler.POSITION_FIRST)
			sayAllHandler.readText(info,sayAllHandler.CURSOR_CARET)

	def unloadBuffer(self):
		if self.VBufHandle is not None:
			VBufClient_destroyBuffer(self.VBufHandle)
			self.VBufHandle=None

	def makeTextInfo(self,position):
		return self.TextInfo(self,position)

	def isNVDAObjectInVirtualBuffer(self,obj):
		pass

	def isAlive(self):
		pass

	def _get_windowHandle(self):
		return self.rootNVDAObject.windowHandle

	def _calculateLineBreaks(self,text):
		maxLineLength=config.conf["virtualBuffers"]["maxLineLength"]
		lastBreak=0
		lineBreakOffsets=[]
		for offset in range(len(text)):
			if offset-lastBreak>maxLineLength and offset>0 and text[offset-1].isspace() and not text[offset].isspace():
				lineBreakOffsets.append(offset)
				lastBreak=offset
		return lineBreakOffsets

	def _activateField(self,docHandle,ID):
		pass

	def _activateContextMenuForField(self,docHandle,ID):
		pass

	def _caretMovedToField(self,dochandle,ID):
		pass

	def script_activatePosition(self,keyPress,nextScript):
		if self.VBufHandle is None:
			return sendKey(keyPress)
		start,end=VBufClient_getBufferSelectionOffsets(self.VBufHandle)
		docHandle,ID=VBufClient_getFieldIdentifierFromBufferOffset(self.VBufHandle,start)
		self._activateField(docHandle,ID)
	script_activatePosition.__doc__ = _("activates the current object in the virtual buffer")

	def _caretMovementScriptHelper(self, *args, **kwargs):
		if self.VBufHandle is None:
			return 
		noKeyWaiting=not isScriptWaiting()
		if noKeyWaiting:
			oldDocHandle,oldID=VBufClient_getFieldIdentifierFromBufferOffset(self.VBufHandle,self.selection._startOffset)
		super(VirtualBuffer, self)._caretMovementScriptHelper(*args, **kwargs)
		if noKeyWaiting:
			docHandle,ID=VBufClient_getFieldIdentifierFromBufferOffset(self.VBufHandle,self.selection._startOffset)
			if ID!=0 and (docHandle!=oldDocHandle or ID!=oldID):
				self._caretMovedToField(docHandle,ID)

	def script_refreshBuffer(self,keyPress,nextScript):
		if self.VBufHandle is None:
			return sendKey(keyPress)
		self.unloadBuffer()
		self.loadBuffer()
		speech.speakMessage(_("Refreshed"))

	def script_toggleScreenLayout(self,keyPress,nextScript):
		config.conf["virtualBuffers"]["useScreenLayout"]=not config.conf["virtualBuffers"]["useScreenLayout"]
		onOff=_("on") if config.conf["virtualBuffers"]["useScreenLayout"] else _("off")
		speech.speakMessage(_("use screen layout %s")%onOff)

	def _searchableAttributesForNodeType(self,nodeType):
		pass

	def _jumpToNodeType(self,nodeType,direction):
		attribs=self._searchableAttribsForNodeType(nodeType)
		if attribs:
			startOffset,endOffset=VBufClient_getBufferSelectionOffsets(self.VBufHandle)
			try:
				newDocHandle,newID=VBufClient_findBufferFieldIdentifierByProperties(self.VBufHandle,direction,startOffset,attribs)
			except:
				return False
		if not newID or not attribs:
			return False
		startOffset,endOffset=VBufClient_getBufferOffsetsFromFieldIdentifier(self.VBufHandle,newDocHandle,newID)
		info=self.makeTextInfo(textHandler.Bookmark(self.TextInfo,(startOffset,endOffset)))
		info.updateCaret()
		speech.speakFormattedTextWithXML(info.XMLContext,info.XMLText,info.obj,info.getXMLFieldSpeech,reason=speech.REASON_FOCUS)
		self._caretMovedToField(newDocHandle,newID)
		return True

	def _iterNodesByType(self,nodeType,direction="next",startOffset=-1):
		attribs=self._searchableAttribsForNodeType(nodeType)
		if not attribs:
			return

		while True:
			try:
				docHandle,ID=VBufClient_findBufferFieldIdentifierByProperties(self.VBufHandle,direction,startOffset,attribs)
			except:
				return
			if not ID:
				return

			startOffset,endOffset=VBufClient_getBufferOffsetsFromFieldIdentifier(self.VBufHandle,docHandle,ID)
			yield docHandle, ID, startOffset, endOffset

	def script_nextHeading(self,keyPress,nextScript):
		if self.VBufHandle is None:
			return sendKey(keyPress)
		if not self._jumpToNodeType("heading","next"):
			speech.speakMessage(_("no next heading"))
	script_nextHeading.__doc__ = _("moves to the next heading")

	def script_previousHeading(self,keyPress,nextScript):
		if self.VBufHandle is None:
			return sendKey(keyPress)
		if not self._jumpToNodeType("heading","previous"):
			speech.speakMessage(_("no previous heading"))
	script_previousHeading.__doc__ = _("moves to the previous heading")

	def script_nextTable(self,keyPress,nextScript):
		if self.VBufHandle is None:
			return sendKey(keyPress)
		if not self._jumpToNodeType("table","next"):
			speech.speakMessage(_("no next table"))
	script_nextTable.__doc__ = _("moves to the next table")

	def script_previousTable(self,keyPress,nextScript):
		if self.VBufHandle is None:
			return sendKey(keyPress)
		if not self._jumpToNodeType("table","previous"):
			speech.speakMessage(_("no previous table"))
	script_previousTable.__doc__ = _("moves to the previous table")

	def script_nextLink(self,keyPress,nextScript):
		if self.VBufHandle is None:
			return sendKey(keyPress)
		if not self._jumpToNodeType("link","next"):
			speech.speakMessage(_("no next link"))
	script_nextLink.__doc__ = _("moves to the next link")

	def script_previousLink(self,keyPress,nextScript):
		if self.VBufHandle is None:
			return sendKey(keyPress)
		if not self._jumpToNodeType("link","previous"):
			speech.speakMessage(_("no previous link"))
	script_previousLink.__doc__ = _("moves to the previous link")

	def script_nextVisitedLink(self,keyPress,nextScript):
		if self.VBufHandle is None:
			return sendKey(keyPress)
		if not self._jumpToNodeType("visitedLink","next"):
			speech.speakMessage(_("no next visited link"))
	script_nextLink.__doc__ = _("moves to the next visited link")

	def script_previousVisitedLink(self,keyPress,nextScript):
		if self.VBufHandle is None:
			return sendKey(keyPress)
		if not self._jumpToNodeType("visitedLink","previous"):
			speech.speakMessage(_("no previous visited link"))
	script_previousLink.__doc__ = _("moves to the previous visited link")

	def script_nextUnvisitedLink(self,keyPress,nextScript):
		if self.VBufHandle is None:
			return sendKey(keyPress)
		if not self._jumpToNodeType("unvisitedLink","next"):
			speech.speakMessage(_("no next unvisited link"))
	script_nextUnvisitedLink.__doc__ = _("moves to the next unvisited link")

	def script_previousUnvisitedLink(self,keyPress,nextScript):
		if self.VBufHandle is None:
			return sendKey(keyPress)
		if not self._jumpToNodeType("unvisitedLink","previous"):
			speech.speakMessage(_("no previous unvisited link"))
	script_previousUnvisitedLink.__doc__ = _("moves to the previous unvisited link")

	def script_nextFormField(self,keyPress,nextScript):
		if self.VBufHandle is None:
			return sendKey(keyPress)
		if not self._jumpToNodeType("formField","next"):
			speech.speakMessage(_("no next form field"))
	script_nextFormField.__doc__ = _("moves to the next form field")

	def script_previousFormField(self,keyPress,nextScript):
		if self.VBufHandle is None:
			return sendKey(keyPress)
		if not self._jumpToNodeType("formField","previous"):
			speech.speakMessage(_("no previous form field"))
	script_previousFormField.__doc__ = _("moves to the next form field")

	def script_linksList(self, keyPress, nextScript):
		if self.VBufHandle is None:
			return

		nodes = []
		caretOffset, _ignored = VBufClient_getBufferSelectionOffsets(self.VBufHandle)
		defaultIndex = None
		for docHandle, ID, startOffset, endOffset in self._iterNodesByType("link"):
			if defaultIndex is None:
				if startOffset <= caretOffset and caretOffset < endOffset:
					# The caret is inside this link, so make it the default selection.
					defaultIndex = len(nodes)
				elif startOffset > caretOffset:
					# The caret wasn't inside a link, so set the default selection to be the next link.
					defaultIndex = len(nodes)
			text = self.makeTextInfo(textHandler.Bookmark(self.TextInfo,(startOffset,endOffset))).text
			nodes.append((text, docHandle, ID, startOffset, endOffset))

		def action(args):
			if args is None:
				return
			activate, index, text = args
			text, docHandle, ID, startOffset, endOffset = nodes[index]
			if activate:
				self._activateField(docHandle, ID)
			else:
				info=self.makeTextInfo(textHandler.Bookmark(self.TextInfo,(startOffset,endOffset)))
				info.updateCaret()
				speech.cancelSpeech()
				speech.speakFormattedTextWithXML(info.XMLContext,info.XMLText,info.obj,info.getXMLFieldSpeech,reason=speech.REASON_FOCUS)
				self._caretMovedToField(docHandle,ID)

		scriptUI.LinksListDialog(choices=[node[0] for node in nodes], default=defaultIndex if defaultIndex is not None else 0, callback=action).run()
	script_linksList.__doc__ = _("displays a list of links")

[VirtualBuffer.bindKey(keyName,scriptName) for keyName,scriptName in [
	("Return","activatePosition"),
	("Space","activatePosition"),
	("NVDA+f5","refreshBuffer"),
	("NVDA+v","toggleScreenLayout"),
	("h","nextHeading"),
	("shift+h","previousHeading"),
	("t","nextTable"),
	("shift+t","previousTable"),
	("k","nextLink"),
	("shift+k","previousLink"),
	("v","nextVisitedLink"),
	("shift+v","previousVisitedLink"),
	("u","nextUnvisitedLink"),
	("shift+u","previousUnvisitedLink"),
	("f","nextFormField"),
	("shift+f","previousFormField"),
	("NVDA+f7","linksList"),
]]
