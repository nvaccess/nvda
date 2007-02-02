#appModules/winword.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import ctypes
import comtypesClient
import comtypes.automation
from autoPropertyType import autoPropertyType
import IAccessibleHandler
import audio
import debug
from keyboardHandler import sendKey, key
import config
import NVDAObjects
import _default

#Word constants

#Indexing
wdActiveEndPageNumber=3
wdNumberOfPagesInDocument=4
wdFirstCharacterLineNumber=10
wdWithInTable=12
wdStartOfRangeRowNumber=13
wdMaximumNumberOfRows=15
wdStartOfRangeColumnNumber=16
wdMaximumNumberOfColumns=18
#Horizontal alignment
wdAlignParagraphLeft=0
wdAlignParagraphCenter=1
wdAlignParagraphRight=2
wdAlignParagraphJustify=3
#Units
wdCharacter=1
wdWord=2
wdSentence=3
wdParagraph=4
wdLine=5
wdStory=6
wdColumn=9
wdRow=10
wdWindow=11
wdCell=12
wdCharFormat=13
wdParaFormat=14
wdTable=15
#GoTo - direction
wdGoToAbsolute=1
wdGoToRelative=2
wdGoToNext=2
#GoTo - units
wdGoToPage=1
wdGoToLine=3

class appModule(_default.appModule):

	def __init__(self,*args):
		_default.appModule.__init__(self,*args)
		NVDAObjects.IAccessible.registerNVDAObjectClass(self.processID,"_WwG",IAccessibleHandler.ROLE_SYSTEM_CLIENT,NVDAObject_wordDocument)

	def __del__(self):
		NVDAObjects.IAccessible.unregisterNVDAObjectClass(self.processID,"_WwG",IAccessibleHandler.ROLE_SYSTEM_CLIENT)
		_default.appModule.__del__(self)

class NVDAObject_wordDocument(NVDAObjects.IAccessible.NVDAObject_IAccessible):

	__metaclass__=autoPropertyType

	def __init__(self,*args,**vars):
		NVDAObjects.IAccessible.NVDAObject_IAccessible.__init__(self,*args,**vars)
		self.dom=self.getDocumentObjectModel()
		self.registerScriptKeys({
			key("ExtendedUp"):self.script_text_moveByLine,
			key("ExtendedDown"):self.script_text_moveByLine,
			key("ExtendedLeft"):self.script_text_moveByCharacter,
			key("ExtendedRight"):self.script_text_moveByCharacter,
			key("Control+ExtendedUp"):self.script_text_prevParagraph,
			key("Control+ExtendedDown"):self.script_text_nextParagraph,
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
			key("control+ExtendedUp"):self.script_text_moveByParagraph,
			key("control+ExtendedDown"):self.script_text_moveByParagraph,
		})
		self.text_reviewOffset=self.text_caretOffset

	def event_caret(self):
		pass

	def __del__(self):
		self.destroyObjectModel(self.dom)

	def _get_role(self):
		return IAccessibleHandler.ROLE_SYSTEM_TEXT

	def getDocumentObjectModel(self):
		ptr=ctypes.POINTER(comtypes.automation.IDispatch)()
		if ctypes.windll.oleacc.AccessibleObjectFromWindow(self.windowHandle,IAccessibleHandler.OBJID_NATIVEOM,ctypes.byref(ptr._iid_),ctypes.byref(ptr))!=0:
			raise OSError("No native object model")
		return comtypesClient.wrap(ptr)

	def destroyObjectModel(self,om):
		pass

	def _get_text_characterCount(self):
		r=self.dom.selection.Document.range(0,0)
		r.Expand(wdStory)
		return r.End

	def text_getText(self,start=None,end=None):
		start=start if isinstance(start,int) else 0
		end=end if isinstance(end,int) else self.text_characterCount
		r=self.dom.selection.Document.range(start,end)
		return r.text

	def _get_text_selectionCount(self):
		if self.dom.Selection.Start!=self.dom.Selection.End:
			return 1
		else:
			return 0

	def text_getSelectionOffsets(self,index):
		if index!=0:
			return None
		start=self.dom.Selection.Start
		end=self.dom.Selection.End
		if start!=end:
			return (start,end)
		else:
			return None

	def _get_text_caretOffset(self):
		return self.dom.Selection.Start

	def _set_text_caretOffset(self,offset):
		self.dom.Selection.Start=offset
		self.dom.Selection.End=offset

	def text_getLineNumber(self,offset):
		return self.dom.selection.Document.range(offset,offset).Information(wdFirstCharacterLineNumber)

	def text_getPageNumber(self,offset):
		pageNum=self.dom.selection.Document.range(offset,offset).Information(wdActiveEndPageNumber)
		if pageNum>0:
			return pageNum
		else:
			return None

	def text_getLineOffsets(self,offset):
		oldSel=self.dom.selection.range
		oldReview=self.text_reviewOffset
		sel=self.dom.selection
		sel.Start=offset
		sel.End=offset
		sel.Expand(wdLine)
		lineOffsets=(sel.Start,sel.End)
		sel.Start=oldSel.Start
		sel.End=oldSel.End
		self.text_reviewOffset=oldReview
		return lineOffsets

	def text_getNextLineOffsets(self,offset):
		(start,end)=self.text_getLineOffsets(offset)
		oldSel=self.dom.selection.range
		oldReview=self.text_reviewOffset
		sel=self.dom.selection
		sel.Start=sel.End=start
		res=sel.Move(wdLine,1)
		if res!=0:
			lineOffsets=self.text_getLineOffsets(sel.Start)
		else:
			lineOffsets=None
		sel.Start=oldSel.Start
		sel.End=oldSel.End
		self.text_reviewOffset=oldReview
		return lineOffsets

	def text_getPrevLineOffsets(self,offset):
		(start,end)=self.text_getLineOffsets(offset)
		oldSel=self.dom.selection.range
		oldReview=self.text_reviewOffset
		sel=self.dom.selection
		sel.Start=sel.End=start
		res=sel.Move(wdLine,-1)
		if res!=0:
			lineOffsets=self.text_getLineOffsets(sel.Start)
		else:
			lineOffsets=None
		sel.Start=oldSel.Start
		sel.End=oldSel.End
		self.text_reviewOffset=oldReview
		return lineOffsets

	def text_getWordOffsets(self,offset):
		r=self.dom.selection.Document.range(offset,offset)
		r.Expand(wdWord)
		return (r.Start,r.End)

	def text_getNextWordOffsets(self,offset):
		(start,end)=self.text_getWordOffsets(offset)
		r=self.dom.selection.Document.range(start,start)
		res=r.Move(wdWord,1)
		if res:
			return self.text_getWordOffsets(r.Start)
		else:
			return None

	def text_getPrevWordOffsets(self,offset):
		(start,end)=self.text_getWordOffsets(offset)
		r=self.dom.selection.Document.range(start,start)
		res=r.Move(wdWord,-1)
		if res:
			return self.text_getWordOffsets(r.Start)
		else:
			return None

	def text_getSentenceOffsets(self,offset):
		r=self.dom.selection.Document.range(offset,offset)
		r.Expand(wdSentence)
		return (r.Start,r.End)

	def text_getNextSentenceOffsets(self,offset):
		(start,end)=self.text_getSentenceOffsets(offset)
		r=self.dom.selection.Document.range(start,start)
		res=r.Move(wdSentence,1)
		if res:
			return self.text_getSentenceOffsets(r.Start)
		else:
			return None

	def text_getPrevSentenceOffsets(self,offset):
		(start,end)=self.text_getSentenceOffsets(offset)
		r=self.dom.selection.Document.range(start,start)
		res=r.Move(wdSentence,-1)
		if res:
			return self.text_getSentenceOffsets(r.Start)
		else:
			return None

	def text_getParagraphOffsets(self,offset):
		r=self.dom.selection.Document.range(offset,offset)
		r.Expand(wdParagraph)
		return (r.Start,r.End)

	def text_getNextParagraphOffsets(self,offset):
		(start,end)=self.text_getParagraphOffsets(offset)
		r=self.dom.selection.Document.range(start,start)
		res=r.Move(wdParagraph,1)
		if res:
			return self.text_getParagraphOffsets(r.Start)
		else:
			return None

	def text_getPrevParagraphOffsets(self,offset):
		(start,end)=self.text_getParagraphOffsets(offset)
		r=self.dom.selection.Document.range(start,start)
		res=r.Move(wdParagraph,-1)
		if res:
			return self.text_getParagraphOffsets(r.Start)
		else:
			return None

	def text_getFieldOffsets(self,offset):
		r=self.dom.selection.Document.range(offset,offset)
		r.Expand(wdCharFormat)
		return (r.Start,r.End)

	def text_getNextFieldOffsets(self,offset):
		(start,end)=self.text_getFieldOffsets(offset)
		r=self.dom.selection.Document.range(start,start)
		res=r.Move(wdCharFormat,1)
		if res:
			return self.text_getFieldOffsets(r.Start)
		else:
			return None

	def text_getPrevFieldOffsets(self,offset):
		(start,end)=self.text_getFieldOffsets(offset)
		r=self.dom.selection.Document.range(start,start)
		res=r.Move(wdCharFormat,-1)
		if res:
			return self.text_getFieldOffsets(r.Start)
		else:
			return None

	def text_getStyle(self,offset):
		return self.dom.selection.Document.range(offset,offset).Style.NameLocal

	def text_getFontName(self,offset):
		return self.dom.selection.Document.range(offset,offset).Font.Name

	def text_getFontSize(self,offset):
		return int(self.dom.selection.Document.range(offset,offset).Font.Size)

	def text_getAlignment(self,offset):
		alignment=self.dom.selection.Document.range(offset,offset).ParagraphFormat.Alignment
		if alignment==wdAlignParagraphLeft:
			return _("left")
		elif alignment==wdAlignParagraphCenter:
			return _("centered")
		elif alignment==wdAlignParagraphRight:
			return _("right")
		elif alignment==wdAlignParagraphJustify:
			return _("justified")

	def text_isBold(self,offset):
		return bool(self.dom.selection.Document.range(offset,offset).Font.Bold)

	def text_isItalic(self,offset):
		return bool(self.dom.selection.Document.range(offset,offset).Font.Italic)

	def text_isUnderline(self,offset):
		return bool(self.dom.selection.Document.range(offset,offset).Font.Underline)

	def text_isSuperscript(self,offset):
		return bool(self.dom.selection.Document.range(offset,offset).Font.Superscript)

	def text_isSubscript(self,offset):
		return bool(self.dom.selection.Document.range(offset,offset).Font.Subscript)

	def text_inTable(self,offset):
		return self.dom.selection.Document.range(offset,offset).Information(wdWithInTable)

	def text_getTableRowNumber(self,offset):
		rowNum=self.dom.selection.Document.range(offset,offset).Information(wdStartOfRangeRowNumber)
		if rowNum>0:
			return rowNum
		else:
			return None

	def text_getTableColumnNumber(self,offset):
		columnNum=self.dom.selection.Document.range(offset,offset).Information(wdStartOfRangeColumnNumber)
		if columnNum>0:
			return columnNum
		else:
			return None

	def text_getTableRowCount(self,offset):
		rowCount=self.dom.selection.Document.range(offset,offset).Information(wdMaximumNumberOfRows)
		if rowCount>0:
			return rowCount
		else:
			return None

	def text_getTableColumnCount(self,offset):
		columnCount=self.dom.selection.Document.range(offset,offset).Information(wdMaximumNumberOfColumns)
		if columnCount>0:
			return columnCount
		else:
			return None

