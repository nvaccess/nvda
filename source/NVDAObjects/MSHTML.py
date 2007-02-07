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
		lineNum=(ord(bookmark[8])/2)-2
		return ord(bookmark[2])-self.offsetBias-lineNum

	def getBookmarkOffsets(self,bookmark):
		start=self.getBookmarkOffset(bookmark)
		if ord(bookmark[1])==3:
			lineNum=self.text_getLineNumber(ord(bookmark[40])-self.offsetBias)-1
			end=ord(bookmark[40])-self.offsetBias-lineNum
		else:
			end=start
		return (start,end)

	def getDomRange(self,start,end):
		r=self.dom.selection.createRange().duplicate()
		r.move("textedit",-1)
		r.move("character",start)
		if end!=start:
			r.moveEnd("character",end-start)
		return r

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
		r=self.getDomRange(start,end)
		return r.text

	def _get_text_selectionCount(self):
		if not hasattr(self,'dom'):
			return 0
		bookmark=self.dom.selection.createRange().getBookmark()
		if ord(bookmark[1])==3:
			return 1
		else:
			return 0

	def text_getSelectionOffsets(self,index):
		if not hasattr(self,'dom') or (index!=0) or (self.text_selectionCount!=1):
			return None
		bookmark=self.dom.selection.createRange().getBookmark()
		return self.getBookmarkOffsets(bookmark)

	def _get_text_caretOffset(self):
		if not hasattr(self,'dom'):
			return 0
		bookmark=self.dom.selection.createRange().getBookmark()
		return self.getBookmarkOffset(bookmark)

	def _set_text_caretOffset(self,offset):
		if not hasattr(self,'dom'):
			return
		r=self.getDomRange(offset,offset)
		bookmark=r.getBookmark()
		self.dom.selection.createRange().moveToBookmark(bookmark)

	def text_getLineNumber(self,offset):
		r=self.getDomRange(offset,offset)
		return (ord(r.getBookmark()[8])/2)-1

	def text_getLineOffsets(self,offset):
		if not hasattr(self,'dom'):
			return
		oldBookmark=self.dom.selection.createRange().getBookmark()
		r=self.getDomRange(offset,offset)
		self.dom.selection.createRange().moveToBookmark(r.getBookmark())
		sendKey(key("ExtendedEnd"))
		end=self.getBookmarkOffset(self.dom.selection.createRange().getBookmark())
		sendKey(key("ExtendedHome"))
		start=self.getBookmarkOffset(self.dom.selection.createRange().getBookmark())
		self.dom.selection.createRange().moveToBookmark(oldBookmark)
		return (start,end)

	def text_getNextLineOffsets(self,offset):
		if not hasattr(self,'dom'):
			return
		oldBookmark=self.dom.selection.createRange().getBookmark()
		r=self.getDomRange(offset,offset)
		self.dom.selection.createRange().moveToBookmark(r.getBookmark())
		sendKey(key("extendedDown"))
		sendKey(key("ExtendedEnd"))
		end=self.getBookmarkOffset(self.dom.selection.createRange().getBookmark())
		sendKey(key("ExtendedHome"))
		start=self.getBookmarkOffset(self.dom.selection.createRange().getBookmark())
		self.dom.selection.createRange().moveToBookmark(oldBookmark)
		if start>offset:
			return (start,end)
		else:
			return None

	def text_getPrevLineOffsets(self,offset):
		if not hasattr(self,'dom'):
			return
		oldBookmark=self.dom.selection.createRange().getBookmark()
		r=self.getDomRange(offset,offset)
		self.dom.selection.createRange().moveToBookmark(r.getBookmark())
		sendKey(key("extendedUp"))
		sendKey(key("ExtendedEnd"))
		end=self.getBookmarkOffset(self.dom.selection.createRange().getBookmark())
		sendKey(key("ExtendedHome"))
		start=self.getBookmarkOffset(self.dom.selection.createRange().getBookmark())
		self.dom.selection.createRange().moveToBookmark(oldBookmark)
		if end<=offset and start<offset:
			return (start,end)
		else:
			return None

	def text_getWordOffsets(self,offset):
		r=self.getDomRange(offset,offset+1)
		r.expand("word")
		return self.getBookmarkOffsets(r.getBookmark())

	def text_getNextWordOffsets(self,offset):
		r=self.getDomRange(offset,offset)
		r.move("word",1)
		r.expand("word")
		(start,end)=self.getBookmarkOffsets(r.getBookmark())
		if start>offset:
			return (start,end)
		else:
			return None

	def text_getPrevWordOffsets(self,offset):
		r=self.getDomRange(offset,offset)
		r.move("word",-1)
		r.expand("word")
		(start,end)=self.getBookmarkOffsets(r.getBookmark())
		if end<=offset and start<offset:
			return (start,end)
		else:
			return None

	def text_getSentenceOffsets(self,offset):
		r=self.getDomRange(offset,offset)
		r.expand("sentence")
		return self.getBookmarkOffsets(r.getBookmark())

	def text_getNextSentenceOffsets(self,offset):
		r=self.getDomRange(offset,offset)
		r.move("sentence",1)
		r.expand("sentence")
		(start,end)=self.getBookmarkOffsets(r.getBookmark())
		if start>offset:
			return (start,end)
		else:
			return None

	def text_getPrevSentenceOffsets(self,offset):
		r=self.getDomRange(offset,offset)
		r.move("sentence",-1)
		r.expand("sentence")
		(start,end)=self.getBookmarkOffsets(r.getBookmark())
		if end<=offset and start<offset:
			return (start,end)
		else:
			return None

	def text_getFieldOffsets(self,offset):
		r=self.text_getSentenceOffsets(offset)
		if r is None:
			r=self.text_getLineOffsets(offset)
		return r

	def text_getNextFieldOffsets(self,offset):
		r=self.text_getNextSentenceOffsets(offset)
		if r is None:
			r=self.text_getNextLineOffsets(offset)
		return r

	def text_getPrevFieldOffsets(self,offset):
		r=self.text_getPrevSentenceOffsets(offset)
		if r is None:
			r=self.text_getPrevLineOffsets(offset)
		return r

	def event_gainFocus(self):
		self.dom=self.getDocumentObjectModel()
		self.offsetBias=self.getOffsetBias()
		if self.dom.body.isContentEditable and not api.isVirtualBufferPassThrough():
			api.toggleVirtualBufferPassThrough()
		IAccessible.NVDAObject_IAccessible.event_gainFocus(self)

	def event_looseFocus(self):
		if hasattr(self,'dom'):
			del self.dom

