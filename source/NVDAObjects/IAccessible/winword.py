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
import textHandler
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

NVDAUnitsToWordUnits={
	textHandler.UNIT_CHARACTER:wdCharacter,
	textHandler.UNIT_WORD:wdWord,
	textHandler.UNIT_LINE:wdLine,
	textHandler.UNIT_SENTENCE:wdSentence,
	textHandler.UNIT_PARAGRAPH:wdParagraph,
	textHandler.UNIT_TABLE:wdTable,
	textHandler.UNIT_CELL:wdCell,
	textHandler.UNIT_ROW:wdRow,
	textHandler.UNIT_COLUMN:wdColumn,
	textHandler.UNIT_STORY:wdStory,
	textHandler.UNIT_READINGCHUNK:wdSentence,
}

class WordDocumentTextInfo(textHandler.TextInfo):

	def _expandToLine(self,rangeObj):
		sel=self.obj.dom.Selection
		oldSel=sel.range
		sel.Start=rangeObj.Start
		sel.End=rangeObj.End
		sel.Expand(wdLine)
		rangeObj.SetRange(sel.Start,sel.End)
		sel.SetRange(oldSel.Start,oldSel.End)

	def __init__(self,obj,position,_rangeObj=None):
		super(WordDocumentTextInfo,self).__init__(obj,position)
		if _rangeObj:
			self._rangeObj=_rangeObj.Duplicate
			return
		self._rangeObj=self.obj.dom.Selection.range
		if position==textHandler.POSITION_SELECTION:
			pass
		elif position==textHandler.POSITION_CARET:
			self._rangeObj.Collapse()
		elif position==textHandler.POSITION_FIRST:
			self._rangeObj.SetRange(0,0)
		elif position==textHandler.POSITION_LAST:
			self._rangeObj.moveEnd(wdStory,1)
			self._rangeObj.move(wdCharacter,-1)
		elif isinstance(position,textHandler.Bookmark):
			if position.infoClass==self.__class__:
				self._rangeObj.SetRange(position.data[0],position.data[1])
			else:
				raise TypeError("Bookmark was for %s type, not for %s type"%(position.infoClass.__name__,self.__class__.__name__))
		else:
			raise NotImplementedError("position: %s"%position)

	def expand(self,unit):
		if unit==textHandler.UNIT_LINE and self.basePosition not in (textHandler.POSITION_CARET,textHandler.POSITION_SELECTION):
			unit=textHandler.UNIT_SENTENCE
		if unit==textHandler.UNIT_LINE:
			self._expandToLine(self._rangeObj)
		elif unit in NVDAUnitsToWordUnits:
			self._rangeObj.Expand(NVDAUnitsToWordUnits[unit])
		else:
			raise NotImplementedError("unit: %s"%unit)

	def compareStart(self,info,useEnd=False):
		if useEnd:
			return self._rangeObj.Start-info._rangeObj.End
		else:
			return self._rangeObj.Start-info._rangeObj.Start

	def compareEnd(self,info,useStart=False):
		if useStart:
			return self._rangeObj.End-info._rangeObj.Start
		else:
			return self._rangeObj.End-info._rangeObj.End

	def _get_isCollapsed(self):
		if self._rangeObj.Start==self._rangeObj.End:
			return True
		else:
			return False

	def collapse(self,end=False):
		a=self._rangeObj.Start
		b=self._rangeObj.end
		startOffset=min(a,b)
		endOffset=max(a,b)
		if not end:
			offset=startOffset
		else:
			offset=endOffset
		self._rangeObj.SetRange(offset,offset)

	def copy(self):
		return WordDocumentTextInfo(self.obj,None,_rangeObj=self._rangeObj)

	def _get_text(self):
		return self._rangeObj.text

	def getFormattedText(self,searchRange=False,includes=set(),excludes=set()):
		fieldList=[]
		curRangeObj=self._rangeObj.Duplicate
		curRangeObj.Collapse()
		startLimit=self._rangeObj.Start
		endLimit=self._rangeObj.End
		lastStyle=lastFontName=lastFontSize=lastBold=lastItalic=lastUnderline=lastTable=lastRow=lastColumn=None
		while curRangeObj.Start>=startLimit and curRangeObj.Start<endLimit:
			if textHandler.isFormatEnabled(controlTypes.ROLE_TABLE,includes=includes,excludes=excludes):
				table=curRangeObj.Information(wdWithInTable)
				if table and not lastTable:
					value=_("with %s columns and %s rows")%(curRangeObj.Information(wdMaximumNumberOfColumns),curRangeObj.Information(wdMaximumNumberOfRows))
					fieldList.append(textHandler.FormatCommand(textHandler.FORMAT_CMD_INFIELD,textHandler.Format(role=controlTypes.ROLE_TABLE,value=value)))
				elif not table and lastTable:
	 				fieldList.append(textHandler.FormatCommand(textHandler.FORMAT_CMD_OUTOFFIELD,textHandler.Format(role=controlTypes.ROLE_TABLE)))
				lastTable=table
				if table:
					row=str(curRangeObj.Information(wdStartOfRangeRowNumber))
					if row!=lastRow:
						fieldList.append(textHandler.FormatCommand(textHandler.FORMAT_CMD_CHANGE,textHandler.Format(role=controlTypes.ROLE_TABLEROW,value=row)))
					lastRow=row
					column=str(curRangeObj.Information(wdStartOfRangeColumnNumber))
					if column!=lastColumn:
						fieldList.append(textHandler.FormatCommand(textHandler.FORMAT_CMD_CHANGE,textHandler.Format(role=controlTypes.ROLE_TABLECOLUMN,value=column)))
					lastColumn=column
			curFont=curRangeObj.font
			curStyle=curRangeObj.style
			if textHandler.isFormatEnabled(controlTypes.ROLE_STYLE,includes=includes,excludes=excludes):
				style=curStyle.nameLocal
				if style!=lastStyle:
					fieldList.append(textHandler.FormatCommand(textHandler.FORMAT_CMD_CHANGE,textHandler.Format(role=controlTypes.ROLE_STYLE,value=style)))
					lastStyle=style
			if textHandler.isFormatEnabled(controlTypes.ROLE_FONTNAME,includes=includes,excludes=excludes):
				fontName=curFont.name
				if fontName!=lastFontName:
					fieldList.append(textHandler.FormatCommand(textHandler.FORMAT_CMD_CHANGE,textHandler.Format(role=controlTypes.ROLE_FONTNAME,value=fontName)))
					lastFontName=fontName
			if textHandler.isFormatEnabled(controlTypes.ROLE_FONTSIZE,includes=includes,excludes=excludes):
				fontSize=str(curFont.size)
				if fontSize!=lastFontSize:
					fieldList.append(textHandler.FormatCommand(textHandler.FORMAT_CMD_CHANGE,textHandler.Format(role=controlTypes.ROLE_FONTSIZE,value=fontSize)))
					lastFontSize=fontSize
			if textHandler.isFormatEnabled(controlTypes.ROLE_BOLD,includes=includes,excludes=excludes):
				bold=curFont.bold
				if bold!=lastBold and bold:
					fieldList.append(textHandler.FormatCommand(textHandler.FORMAT_CMD_SWITCHON,textHandler.Format(role=controlTypes.ROLE_BOLD)))
				elif lastBold is not None and bold!=lastBold and not bold:
					fieldList.append(textHandler.FormatCommand(textHandler.FORMAT_CMD_SWITCHOFF,textHandler.Format(role=controlTypes.ROLE_BOLD)))
				lastBold=bold
			if textHandler.isFormatEnabled(controlTypes.ROLE_ITALIC,includes=includes,excludes=excludes):
				italic=curFont.italic
				if italic!=lastItalic and italic:
					fieldList.append(textHandler.FormatCommand(textHandler.FORMAT_CMD_SWITCHON,textHandler.Format(role=controlTypes.ROLE_ITALIC)))
				elif lastItalic is not None and italic!=lastItalic and not italic:
					fieldList.append(textHandler.FormatCommand(textHandler.FORMAT_CMD_SWITCHOFF,textHandler.Format(role=controlTypes.ROLE_ITALIC)))
				lastItalic=italic
			if textHandler.isFormatEnabled(controlTypes.ROLE_UNDERLINE,includes=includes,excludes=excludes):
				underline=curFont.UNDERLINE
				if underline!=lastUnderline and underline:
					fieldList.append(textHandler.FormatCommand(textHandler.FORMAT_CMD_SWITCHON,textHandler.Format(role=controlTypes.ROLE_UNDERLINE)))
				elif lastUnderline is not None and underline!=lastUnderline and not underline:
					fieldList.append(textHandler.FormatCommand(textHandler.FORMAT_CMD_SWITCHOFF,textHandler.Format(role=controlTypes.ROLE_UNDERLINE)))
				lastUnderline=underline
			if not searchRange:
				break
			tempStart=curRangeObj.Start
			tempEnd=curRangeObj.End
			curRangeObj.Expand(wdWord)
			curRangeObj.Start=max(startLimit,curRangeObj.Start)
			curRangeObj.End=min(endLimit,curRangeObj.End)
			fieldList.append(curRangeObj.text)
			curRangeObj.Start=tempStart
			curRangeObj.End=tempEnd
			if curRangeObj.Move(wdWord,1)<1:
				break
		if curRangeObj.End<endLimit:
			curRangeObj.Start=curRangeObj.End
			curRangeObj.End=endLimit
			fieldList.append(curRangeObj.text)
		return fieldList

	def moveByUnit(self,unit,num,start=True,end=True):
		if unit==textHandler.UNIT_LINE:
			unit=textHandler.UNIT_SENTENCE
		if unit in NVDAUnitsToWordUnits:
			unit=NVDAUnitsToWordUnits[unit]
		else:
			raise NotImplementedError("unit: %s"%unit)
		if start and not end:
			moveFunc=self._rangeObj.MoveStart
		elif end and not start:
			moveFunc=self._rangeObj.MoveEnd
		else:
			moveFunc=self._rangeObj.Move
		res=moveFunc(unit,num)
		return res

	def _get_bookmark(self):
		return textHandler.Bookmark(self.__class__,(self._rangeObj.Start,self._rangeObj.End))

	def updateCaret(self):
		self.obj.dom.Selection.SetRange(self._rangeObj.Start,self._rangeObj.End)

class WordDocument(IAccessible):

	def __init__(self,*args,**kwargs):
		if not hasattr(self,'TextInfo'):
			self.TextInfo=WordDocumentTextInfo
			replacedTextInfo=True
		else:
			replacedTextInfo=False
		super(WordDocument,self).__init__(*args,**kwargs)
		self.dom=self.getDocumentObjectModel()
		if replacedTextInfo:
			self.reviewPosition=self.makeTextInfo(textHandler.POSITION_CARET)

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

	def script_nextRow(self,keyPress,nextScript):
		info=self.makeTextInfo(textHandler.POSITION_CARET)
		if not info._rangeObj.Information(wdWithInTable):
 			speech.speakMessage(_("not in table"))
		lastRowIndex=info._rangeObj.Information(wdMaximumNumberOfRows)-1
		rowIndex=info._rangeObj.Information(wdStartOfRangeRowNumber)-1
		columnIndex=info._rangeObj.Information(wdStartOfRangeColumnNumber)-1
		if rowIndex<lastRowIndex:
			info._rangeObj=info._rangeObj.tables[0].columns[columnIndex].cells[rowIndex+1].range
			info.collapse()
			info.updateCaret()
		else:
			speech.speakMessage(_("bottom of column"))
		info.expand(textHandler.UNIT_CELL)
		speech.speakFormattedText(info)

	def script_previousRow(self,keyPress,nextScript):
		info=self.makeTextInfo(textHandler.POSITION_CARET)
		if not info._rangeObj.Information(wdWithInTable):
 			speech.speakMessage(_("not in table"))
		lastRowIndex=info._rangeObj.Information(wdMaximumNumberOfRows)-1
		rowIndex=info._rangeObj.Information(wdStartOfRangeRowNumber)-1
		columnIndex=info._rangeObj.Information(wdStartOfRangeColumnNumber)-1
		if rowIndex>0:
			info._rangeObj=info._rangeObj.tables[0].columns[columnIndex].cells[rowIndex-1].range
			info.collapse()
			info.updateCaret()
		else:
			speech.speakMessage(_("top of column"))
		info.expand(textHandler.UNIT_CELL)
		speech.speakFormattedText(info)

	def script_nextColumn(self,keyPress,nextScript):
		info=self.makeTextInfo(textHandler.POSITION_CARET)
		if not info._rangeObj.Information(wdWithInTable):
 			speech.speakMessage(_("not in table"))
		lastColumnIndex=info._rangeObj.Information(wdMaximumNumberOfColumns)-1
		rowIndex=info._rangeObj.Information(wdStartOfRangeRowNumber)-1
		columnIndex=info._rangeObj.Information(wdStartOfRangeColumnNumber)-1
		if columnIndex<lastColumnIndex:
			info._rangeObj=info._rangeObj.tables[0].columns[columnIndex+1].cells[rowIndex].range
			info.collapse()
			info.updateCaret()
		else:
			speech.speakMessage(_("end of row"))
		info.expand(textHandler.UNIT_CELL)
		speech.speakFormattedText(info)

	def script_previousColumn(self,keyPress,nextScript):
		info=self.makeTextInfo(textHandler.POSITION_CARET)
		if not info._rangeObj.Information(wdWithInTable):
 			speech.speakMessage(_("not in table"))
		lastColumnIndex=info._rangeObj.Information(wdMaximumNumberOfColumns)-1
		rowIndex=info._rangeObj.Information(wdStartOfRangeRowNumber)-1
		columnIndex=info._rangeObj.Information(wdStartOfRangeColumnNumber)-1
		if columnIndex>0:
			info._rangeObj=info._rangeObj.tables[0].columns[columnIndex-1].cells[rowIndex].range
			info.collapse()
			info.updateCaret()
		else:
			speech.speakMessage(_("beginning of row"))
		info.expand(textHandler.UNIT_CELL)
		speech.speakFormattedText(info)

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
	("control+alt+extendedUp","previousRow"),
	("control+alt+extendedDown","nextRow"),
	("control+alt+extendedLeft","previousColumn"),
	("control+alt+extendedRight","nextColumn"),
]]

