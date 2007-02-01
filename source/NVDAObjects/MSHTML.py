#NVDAObjects/MSHTML.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import ctypes
import comtypesClient
import comtypes.automation
import debug
import winUser
import IAccessibleHandler
import virtualBuffers
from keyboardHandler import key, sendKey
import api
import audio
import IAccessible

class NVDAObject_MSHTML(IAccessible.NVDAObject_IAccessible):

	def getDocumentObjectModel(self):
		virtualBuffer=virtualBuffers.IAccessible.getVirtualBuffer(self)
		if virtualBuffer and hasattr(virtualBuffer,'dom'):
			return virtualBuffer.dom
		else:
			domPointer=ctypes.POINTER(comtypes.automation.IDispatch)()
			wm=winUser.registerWindowMessage(u'WM_HTML_GETOBJECT')
			lresult=winUser.sendMessage(self.windowHandle,wm,0,0)
			res=ctypes.windll.oleacc.ObjectFromLresult(lresult,ctypes.byref(domPointer._iid_),0,ctypes.byref(domPointer))
			return comtypesClient.wrap(domPointer)

	def __init__(self,*args,**vars):
		IAccessible.NVDAObject_IAccessible.__init__(self,*args,**vars)
		self.registerScriptKeys({
			key("ExtendedUp"):self.script_text_moveByLine,
			key("ExtendedDown"):self.script_text_moveByLine,
			key("ExtendedLeft"):self.script_text_moveByCharacter,
			key("ExtendedRight"):self.script_text_moveByCharacter,
			key("Control+ExtendedLeft"):self.script_text_moveByWord,
			key("Control+ExtendedRight"):self.script_text_moveByWord,
			key("Shift+ExtendedRight"):self.script_text_changeSelection,
			key("Shift+ExtendedLeft"):self.script_text_changeSelection,
			key("Shift+ExtendedHome"):self.script_text_changeSelection,
			key("Shift+ExtendedEnd"):self.script_text_changeSelection,
			key("Shift+ExtendedUp"):self.script_text_changeSelection,
			key("Shift+ExtendedDown"):self.script_text_changeSelection,
			key("Control+Shift+ExtendedLeft"):self.script_text_changeSelection,
			key("Control+Shift+ExtendedRight"):self.script_text_changeSelection,
			key("ExtendedHome"):self.script_text_moveByCharacter,
			key("ExtendedEnd"):self.script_text_moveByCharacter,
			key("control+extendedHome"):self.script_text_moveByLine,
			key("control+extendedEnd"):self.script_text_moveByLine,
			key("control+shift+extendedHome"):self.script_text_changeSelection,
			key("control+shift+extendedEnd"):self.script_text_changeSelection,
			key("ExtendedDelete"):self.script_text_delete,
			key("Back"):self.script_text_backspace,
		})

	def _get_typeString(self):
		if self.isContentEditable:
			return IAccessibleHandler.getRoleName(IAccessibleHandler.ROLE_SYSTEM_TEXT)

	def _get_value(self):
		if self.isContentEditable:
			r=self.text_getLineOffsets(self.text_caretOffset)
			if r:
				return self.text_getText(r[0],r[1])
		return ""

	def _get_isContentEditable(self):
		if hasattr(self,'dom') and self.dom.activeElement.isContentEditable:
			return True
		else:
			return False

	def getOffsetBias(self):
		r=self.dom.selection.createRange().duplicate()
		r.expand("textedit")
		return ord(r.getBookmark()[2])

	def getBookmarkOffset(self,bookmark):
		return ord(bookmark[2])-self.getOffsetBias()

	def getBookmarkOffsets(self,bookmark):
		if ord(bookmark[1])==3:
			return (ord(bookmark[2])-self.getOffsetBias(),ord(bookmark[40])-self.getOffsetBias())
		else:
			return (ord(bookmark[2])-self.getOffsetBias(),ord(bookmark[2])-self.getOffsetBias())

	def _get_text_characterCount(self):
		if not hasattr(self,'dom'):
			return 0
		r=self.dom.selection.createRange().duplicate()
		r.expand("textedit")
		bookmark=r.getBookmark()
		return self.getBookmarkOffsets(bookmark)[1]

	def text_getText(self,start=None,end=None):
		if not hasattr(self,'dom'):
			return "\0"
		start=start if isinstance(start,int) else 0
		end=end if isinstance(end,int) else self.text_characterCount
		#audio.speakMessage("get text: %s, %s"%(start,end))
		r=self.dom.selection.createRange().duplicate()
		r.expand("textedit")
		text=r.text
		if text:
			return text[start:end]
		else:
			return ""

	def _get_text_selectionCount(self):
		if not hasattr(self,'dom'):
			return 0
		bookmark=self.dom.selection.createRange().getBookmark()
		if ord(bookmark[1])==3:
			return 1
		else:
			return 0

	def text_getSelection(self,index):
		if not hasattr(self,'dom') or (index!=0) or (self.text_selectionCount!=1):
			return None
		bookmark=self.dom.selection.createRange().getBookmark()
		return self.getBookmarkOffsets(bookmark)

	def _get_text_caretOffset(self):
		if not hasattr(self,'dom'):
			return 0
		bookmark=self.dom.selection.createRange().getBookmark()
		return self.getBookmarkOffset(bookmark)

	def event_gainFocus(self):
		self.dom=self.getDocumentObjectModel()
		if self.dom.body.isContentEditable and not api.isVirtualBufferPassThrough():
			api.toggleVirtualBufferPassThrough()
		IAccessible.NVDAObject_IAccessible.event_gainFocus(self)

	def event_looseFocus(self):
		if hasattr(self,'dom'):
			del self.dom

	def script_text_moveByLine(self,keyPress):
		if not hasattr(self,'dom'):
			return
		sendKey(keyPress)
		bookmark=self.dom.selection.createRange().getBookmark()
		sendKey(key("ExtendedEnd"))
		endRange=self.dom.selection.createRange().Duplicate()
		sendKey(key("ExtendedHome"))
		startRange=self.dom.selection.createRange().Duplicate()
		startRange.setEndPoint("EndToStart",endRange)
		del endRange
		text=startRange.text
		self.dom.selection.createRange().moveToBookmark(bookmark)
		audio.speakText(text)

	def script_text_moveByWord(self,keyPress):
		if not hasattr(self,'dom'):
			return
		sendKey(keyPress)
		startRange=self.dom.selection.createRange().Duplicate()
		startRange.expand("word")
		text=startRange.text
		audio.speakText(text)

	def script_text_moveByCharacter(self,keyPress):
		if not hasattr(self,'dom'):
			return
		sendKey(keyPress)
		startRange=self.dom.selection.createRange().Duplicate()
		startRange.expand("character")
		text=startRange.text
		audio.speakSymbol(text)

	def script_text_delete(self,keyPress):
		if not hasattr(self,'dom'):
			return
		sendKey(keyPress)
		startRange=self.dom.selection.createRange().Duplicate()
		startRange.expand("character")
		text=startRange.text
		audio.speakSymbol(text)

