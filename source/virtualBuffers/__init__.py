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

	def _getWordOffsets(self,offset):
		#Use VBufClient_getBufferLineOffsets with out screen layout to find out the range of the current field
		line_startOffset,line_endOffset=VBufClient_getBufferLineOffsets(self.obj.VBufHandle,offset,0,False)
		word_startOffset,word_endOffset=super(VirtualBufferTextInfo,self)._getWordOffsets(offset)
		return (max(line_startOffset,word_startOffset),min(line_endOffset,word_endOffset))

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
		if not extraDetail and ((reason==speech.REASON_FOCUS and fieldType in ("end_relative","end_inStack")) or (reason in (speech.REASON_CARET,speech.REASON_SAYALL) and fieldType in ("start_inStack","start_addedToStack","start_relative"))) and role in (controlTypes.ROLE_LINK,controlTypes.ROLE_HEADING,controlTypes.ROLE_BUTTON,controlTypes.ROLE_RADIOBUTTON,controlTypes.ROLE_CHECKBOX,controlTypes.ROLE_GRAPHIC,controlTypes.ROLE_SEPARATOR,controlTypes.ROLE_MENUITEM):
			if role==controlTypes.ROLE_LINK:
				return " ".join([x for x in stateText,roleText,keyboardShortcutText])
			else:
				return " ".join([x for x in nameText,roleText,stateText,levelText,keyboardShortcutText if x])
		elif not extraDetail and fieldType in ("start_addedToStack","start_relative","start_inStack") and ((role==controlTypes.ROLE_EDITABLETEXT and controlTypes.STATE_MULTILINE not in states and controlTypes.STATE_READONLY not in states) or role in (controlTypes.ROLE_UNKNOWN,controlTypes.ROLE_COMBOBOX,controlTypes.ROLE_SLIDER)): 
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
		elif not extraDetail and fieldType in ("start_addedToStack","start_relative") and ((role==controlTypes.ROLE_LIST and controlTypes.STATE_READONLY not in states) or  role in (controlTypes.ROLE_UNKNOWN,controlTypes.ROLE_COMBOBOX)):
			return " ".join([x for x in roleText,stateText,keyboardShortcutText if x])
		elif not extraDetail and fieldType=="start_addedToStack" and (role in (controlTypes.ROLE_FRAME,controlTypes.ROLE_INTERNALFRAME,controlTypes.ROLE_TOOLBAR,controlTypes.ROLE_MENUBAR,controlTypes.ROLE_POPUPMENU) or (role==controlTypes.ROLE_DOCUMENT and controlTypes.STATE_EDITABLE in states)):
			return " ".join([x for x in roleText,stateText,keyboardShortcutText if x])
		elif not extraDetail and fieldType=="end_removedFromStack" and (role in (controlTypes.ROLE_FRAME,controlTypes.ROLE_INTERNALFRAME,controlTypes.ROLE_TOOLBAR,controlTypes.ROLE_MENUBAR,controlTypes.ROLE_POPUPMENU) or (role==controlTypes.ROLE_DOCUMENT and controlTypes.STATE_EDITABLE in states)):
			return _("out of %s")%roleText
		elif not extraDetail and fieldType in ("start_addedToStack","start_relative")  and controlTypes.STATE_CLICKABLE in states: 
			return speech.getSpeechTextForProperties(states=set([controlTypes.STATE_CLICKABLE]))
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
		self.VBufHandle=VBufClient_createBuffer(self.rootWindowHandle,self.rootID,self.backendLibPath)

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

	def event_virtualBuffer_firstEnter(self):
		"""Triggered the first time this virtual buffer is entered.
		"""
		speech.cancelSpeech()
		virtualBufferHandler.reportPassThrough(self)
		speech.speakObjectProperties(self.rootNVDAObject,name=True)
		info=self.makeTextInfo(textHandler.POSITION_CARET)
		sayAllHandler.readText(info,sayAllHandler.CURSOR_CARET)

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

	def script_activatePosition(self,keyPress):
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

	def script_refreshBuffer(self,keyPress):
		if self.VBufHandle is None:
			return sendKey(keyPress)
		self.unloadBuffer()
		self.loadBuffer()
		speech.speakMessage(_("Refreshed"))

	def script_toggleScreenLayout(self,keyPress):
		config.conf["virtualBuffers"]["useScreenLayout"]=not config.conf["virtualBuffers"]["useScreenLayout"]
		onOff=_("on") if config.conf["virtualBuffers"]["useScreenLayout"] else _("off")
		speech.speakMessage(_("use screen layout %s")%onOff)

	def _searchableAttributesForNodeType(self,nodeType):
		pass

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
				continue

			startOffset,endOffset=VBufClient_getBufferOffsetsFromFieldIdentifier(self.VBufHandle,docHandle,ID)
			yield docHandle, ID, startOffset, endOffset

	def _quickNavScript(self,keyPress, nodeType, direction, errorMessage):
		if self.VBufHandle is None:
			return sendKey(keyPress)
		startOffset, endOffset=VBufClient_getBufferSelectionOffsets(self.VBufHandle)
		try:
			docHandle, ID, startOffset, endOffset = self._iterNodesByType(nodeType, direction, startOffset).next()
		except StopIteration:
			speech.speakMessage(errorMessage)
			return
		info = self.makeTextInfo(textHandler.Offsets(startOffset, endOffset))
		info.updateCaret()
		speech.speakFormattedTextWithXML(info.XMLContext, info.XMLText, info.obj, info.getXMLFieldSpeech, reason=speech.REASON_FOCUS)
		self._caretMovedToField(docHandle, ID)

	@classmethod
	def addQuickNav(cls, nodeType, key, nextDoc, nextError, prevDoc, prevError):
		scriptSuffix = nodeType[0].upper() + nodeType[1:]
		scriptName = "next%s" % scriptSuffix
		funcName = "script_%s" % scriptName
		script = lambda self,keyPress: self._quickNavScript(keyPress, nodeType, "next", nextError)
		script.__doc__ = nextDoc
		script.__name__ = funcName
		setattr(cls, funcName, script)
		cls.bindKey(key, scriptName)
		scriptName = "previous%s" % scriptSuffix
		funcName = "script_%s" % scriptName
		script = lambda self,keyPress: self._quickNavScript(keyPress, nodeType, "previous", prevError)
		script.__doc__ = prevDoc
		script.__name__ = funcName
		setattr(cls, funcName, script)
		cls.bindKey("shift+%s" % key, scriptName)

	def script_linksList(self,keyPress):
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
			text = self.makeTextInfo(textHandler.Offsets(startOffset,endOffset)).text
			nodes.append((text, docHandle, ID, startOffset, endOffset))

		def action(args):
			if args is None:
				return
			activate, index, text = args
			text, docHandle, ID, startOffset, endOffset = nodes[index]
			if activate:
				self._activateField(docHandle, ID)
			else:
				info=self.makeTextInfo(textHandler.Offsets(startOffset,endOffset))
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
	("NVDA+f7","linksList"),
]]

# Add quick navigation scripts.
qn = VirtualBuffer.addQuickNav
qn("heading", key="h", nextDoc=_("moves to the next heading"), nextError=_("no next heading"),
	prevDoc=_("moves to the previous heading"), prevError=_("no previous heading"))
qn("table", key="t", nextDoc=_("moves to the next table"), nextError=_("no next table"),
	prevDoc=_("moves to the previous table"), prevError=_("no previous table"))
qn("link", key="k", nextDoc=_("moves to the next link"), nextError=_("no next link"),
	prevDoc=_("moves to the previous link"), prevError=_("no previous link"))
qn("visitedLink", key="v", nextDoc=_("moves to the next visited link"), nextError=_("no next visited link"),
	prevDoc=_("moves to the previous visited link"), prevError=_("no previous visited link"))
qn("unvisitedLink", key="u", nextDoc=_("moves to the next unvisited link"), nextError=_("no next unvisited link"),
	prevDoc=_("moves to the previous unvisited link"), prevError=_("no previous unvisited link"))
qn("formField", key="f", nextDoc=_("moves to the next form field"), nextError=_("no next form field"),
	prevDoc=_("moves to the previous form field"), prevError=_("no previous form field"))
qn("list", key="l", nextDoc=_("moves to the next list"), nextError=_("no next list"),
	prevDoc=_("moves to the previous list"), prevError=_("no previous list"))
qn("listItem", key="i", nextDoc=_("moves to the next list item"), nextError=_("no next list item"),
	prevDoc=_("moves to the previous list item"), prevError=_("no previous list item"))
qn("button", key="b", nextDoc=_("moves to the next button"), nextError=_("no next button"),
	prevDoc=_("moves to the previous button"), prevError=_("no previous button"))
qn("edit", key="e", nextDoc=_("moves to the next edit field"), nextError=_("no next edit field"),
	prevDoc=_("moves to the previous edit field"), prevError=_("no previous edit field"))
qn("frame", key="m", nextDoc=_("moves to the next frame"), nextError=_("no next frame"),
	prevDoc=_("moves to the previous frame"), prevError=_("no previous frame"))
qn("separator", key="s", nextDoc=_("moves to the next separator"), nextError=_("no next separator"),
	prevDoc=_("moves to the previous separator"), prevError=_("no previous separator"))
qn("radioButton", key="r", nextDoc=_("moves to the next radio button"), nextError=_("no next radio button"),
	prevDoc=_("moves to the previous radio button"), prevError=_("no previous radio button"))
qn("comboBox", key="c", nextDoc=_("moves to the next combo box"), nextError=_("no next combo box"),
	prevDoc=_("moves to the previous combo box"), prevError=_("no previous combo box"))
qn("checkBox", key="x", nextDoc=_("moves to the next check box"), nextError=_("no next check box"),
	prevDoc=_("moves to the previous check box"), prevError=_("no previous check box"))
qn("graphic", key="g", nextDoc=_("moves to the next graphic"), nextError=_("no next graphic"),
	prevDoc=_("moves to the previous graphic"), prevError=_("no previous graphic"))
del qn
