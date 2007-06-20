#appModules/winword.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import ctypes
import comtypes.automation
import win32com.client
import pythoncom
import IAccessibleHandler
import speech
import debug
from keyUtils import sendKey, key
import config
import text
import controlTypes
from . import IAccessible

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

class WordDocumentTextRangePosition(text.Position):

	def __init__(self,textRange):
		self.textRange=textRange

	def compareStart(self,p):
		return self.textRange.Start-p.textRange.Start

	def compareEnd(self,p):
		return self.textRange.End-p.textRange.End

NVDAUnitsToWordUnits={
	text.UNIT_CHARACTER:wdCharacter,
	text.UNIT_WORD:wdWord,
	text.UNIT_LINE:wdLine,
	text.UNIT_PARAGRAPH:wdParagraph,
	text.UNIT_TABLE:wdTable,
	text.UNIT_ROW:wdRow,
	text.UNIT_COLUMN:wdColumn,
	text.UNIT_SCREEN:wdStory,
	text.UNIT_STORY:wdStory,
}

class WordDocumentTextInfo(text.TextInfo):


	def _expandToLine(self,textRange):
		sel=self.obj.dom.selection
		oldSel=sel.range
		sel.SetRange(textRange.Start,textRange.End)
		sel.Expand(wdLine)
		textRange.SetRange(sel.Start,sel.End)
		sel.SetRange(oldSel.Start,oldSel.End)

	def _moveByLine(self,textRange,movement):
		sel=self.obj.dom.selection
		oldSel=sel.range
		sel.SetRange(textRange.Start,textRange.End)
		sel.Collapse()
		res=sel.Move(wdLine,movement)
		textRange.SetRange(sel.Start,sel.End)
		sel.SetRange(oldSel.Start,oldSel.End)
		return res

	def __init__(self,obj,position,expandToUnit=None,limitToUnit=None,_limitRange=None):
		super(WordDocumentTextInfo,self).__init__(obj,position,expandToUnit,limitToUnit)
		if isinstance(position,WordDocumentTextRangePosition):
			self._range=position.textRange.duplicate
		elif isinstance(position,text.OffsetsPosition):
			self._range=self.obj.dom.selection.range
			self._range.SetRange(position.start,position.end)
		elif position==text.POSITION_CARET:
			self._range=self.obj.dom.selection.range
			self._range.end=self._range.start
		elif position==text.POSITION_SELECTION:
			self._range=self.obj.dom.selection.range
		else:
			raise NotImplementedError("Position: %s"%position)
		if expandToUnit and NVDAUnitsToWordUnits.has_key(expandToUnit):
			wordUnit=NVDAUnitsToWordUnits[expandToUnit]
			self._range.Collapse()
			if expandToUnit==text.UNIT_LINE:
				self._expandToLine(self._range)
			else:
				self._range.Expand(wordUnit)
		elif expandToUnit is not None:
			raise NotImplementedError("Unit: %s"%expandToUnit)
		if _limitRange is not None:
			self._limitRange=_limitRange
		else:
			if limitToUnit is None:
				limitToUnit=text.UNIT_STORY
			if NVDAUnitsToWordUnits.has_key(limitToUnit):
				wordUnit=NVDAUnitsToWordUnits[limitToUnit]
				self._limitRange=self._range.duplicate
				if limitToUnit==text.UNIT_LINE:
					self._expandToLine(self._limitRange)
				else:
					self._limitRange.Expand(wordUnit)
			else:
				raise NotImplementedError("Unit: %s"%limitToUnit)

	def _get_text(self):
		return self._range.text

	def _get_position(self):
		return WordDocumentTextRangePosition(self._range.duplicate)

	def getRelatedUnit(self,relation):
		if self.unit is None:
			raise RuntimeError("No unit")
		newRange=self._range.duplicate
		newRange.Collapse()
		res=0
		if relation==text.UNITRELATION_NEXT:
			if self.unit==text.UNIT_LINE:
				res=self._moveByLine(newRange,1)
			else:
				res=newRange.Move(NVDAUnitsToWordUnits[self.unit],1)
		elif relation==text.UNITRELATION_PREVIOUS:
			if self.unit==text.UNIT_LINE:
				res=self._moveByLine(newRange,-1)
			else:
				res=newRange.Move(NVDAUnitsToWordUnits[self.unit],-1)
		elif relation==text.UNITRELATION_FIRST:
			newRange.SetRange(self._limitRange.start,self._limitRange.start)
			res=1
		elif relation==text.UNITRELATION_LAST:
			newRange.SetRange(self._limitRange.end-1,self._limitRange.end-1)
			res=1
		if res and newRange.InRange(self._limitRange):
			return self.__class__(self.obj,WordDocumentTextRangePosition(newRange.duplicate),expandToUnit=self.unit,limitToUnit=self.limitUnit,_limitRange=self._limitRange)
		else:
			raise text.E_noRelatedUnit




class WordDocument(IAccessible):

	def __init__(self,*args,**kwargs):
		super(WordDocument,self).__init__(*args,**kwargs)
		self.dom=self.getDocumentObjectModel()

	def __del__(self):
		self.destroyObjectModel(self.dom)

	def _get_role(self):
		return controlTypes.ROLE_EDITABLETEXT

	def getDocumentObjectModel(self):
		ptr=ctypes.c_void_p()
		if ctypes.windll.oleacc.AccessibleObjectFromWindow(self.windowHandle,IAccessibleHandler.OBJID_NATIVEOM,ctypes.byref(comtypes.automation.IDispatch._iid_),ctypes.byref(ptr))!=0:
			raise OSError("No native object model")
		#We use pywin32 for large IDispatch interfaces since it handles them much better than comtypes
		o=pythoncom._univgw.interface(ptr.value,pythoncom.IID_IDispatch)
		t=o.GetTypeInfo()
		a=t.GetTypeAttr()
		oleRepr=win32com.client.build.DispatchItem(attr=a)
		return win32com.client.CDispatch(o,oleRepr)
 
	def destroyObjectModel(self,om):
		pass

[WordDocument.bindKey(keyName,scriptName) for keyName,scriptName in [
	("ExtendedUp","moveByLine"),
	("ExtendedDown","moveByLine"),
	("ExtendedLeft","moveByCharacter"),
	("ExtendedRight","moveByCharacter"),
	("Control+ExtendedLeft","moveByWord"),
	("Control+ExtendedRight","moveByWord"),
	("Shift+ExtendedRight","changeSelection"),
	("control+extendedDown","moveByParagraph"),
	("control+extendedUp","moveByParagraph"),
	("Shift+ExtendedLeft","changeSelection"),
	("Shift+ExtendedHome","changeSelection"),
	("Shift+ExtendedEnd","changeSelection"),
	("Shift+ExtendedUp","changeSelection"),
	("Shift+ExtendedDown","changeSelection"),
	("Control+Shift+ExtendedLeft","changeSelection"),
	("Control+Shift+ExtendedRight","changeSelection"),
	("ExtendedHome","moveByCharacter"),
	("ExtendedEnd","moveByCharacter"),
	("control+extendedHome","moveByLine"),
	("control+extendedEnd","moveByLine"),
	("control+shift+extendedHome","changeSelection"),
	("control+shift+extendedEnd","changeSelection"),
	("ExtendedDelete","delete"),
	("Back","backspace"),
]]

WordDocument.TextInfo=WordDocumentTextInfo
