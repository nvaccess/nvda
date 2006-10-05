import win32com.client
import audio
import debug
from constants import *
from keyboardHandler import sendKey, key
from config import conf
import NVDAObjects
import _MSOffice

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
wdLine=5
wdStory=6
wdColumn=9
wdRow=10
wdWindow=11
wdCell=12
wdTable=15
#GoTo - direction
wdGoToAbsolute=1
wdGoToRelative=2
wdGoToNext=2
#GoTo - units
wdGoToPage=1
wdGoToLine=3

word_application=win32com.client.dynamic.Dispatch('word.Application')

class appModule(_MSOffice.appModule):

	def __init__(self):
		_MSOffice.appModule.__init__(self)
		NVDAObjects.registerNVDAObjectClass("_WwG",ROLE_SYSTEM_CLIENT,NVDAObject_wordDocument)

	def __del__(self):
		NVDAObjects.unregisterNVDAObjectClass("_WwG",ROLE_SYSTEM_CLIENT)
		_MSOffice.appModule.__del__(self)

class NVDAObject_wordDocument(NVDAObjects.NVDAObject_ITextDocument):

	def __init__(self,accObject):
		NVDAObjects.NVDAObject_ITextDocument.__init__(self,accObject)
		self.lastStyle=self.lastIsTable=self.lastRowNumber=self.lastColumnNumber=self.lastPageNumber=None
		self.keyMap.update({
key("control+ExtendedUp"):self.script_moveByParagraph,
key("control+ExtendedDown"):self.script_moveByParagraph,
})

	def getDocumentObjectModel(self):
		return word_application.ActiveWindow.ActivePane

	def _duplicateDocumentRange(self,rangeObj):
		return rangeObj.Range

	def getRole(self):
		return ROLE_SYSTEM_TEXT

	def getLineNumber(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Information(wdFirstCharacterLineNumber)-1

	def getLine(self,pos):
		saveSelection=self.dom.Selection
		rangeObj=self.dom.Selection
		rangeObj.Start=rangeObj.End=pos
		rangeObj.Expand(wdLine)
		text=rangeObj.Text
		self.dom.Selection.Start=saveSelection.Start
		self.dom.Selection.End=saveSelection.End
		return text

	def getCurrentLine(self):
		return self.getLine(self.getCaretPosition())

	def getStyle(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Style.NameLocal

	def getCurrentStyle(self):
		return self.getStyle(self.getCaretPosition())

	def isTable(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Information(wdWithInTable)

	def isCurrentTable(self):
		return self.isTable(self.getCaretPosition())

	def getRowNumber(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Information(wdStartOfRangeRowNumber)

	def getCurrentRowNumber(self):
		return self.getRowNumber(self.getCaretPosition())

	def getRowCount(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Information(wdMaximumNumberOfRows)

	def getCurrentRowCount(self):
		return self.getRowCount(self.getCaretPosition())

	def getColumnNumber(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Information(wdStartOfRangeColumnNumber)

	def getCurrentColumnNumber(self):
		return self.getColumnNumber(self.getCaretPosition())

	def getColumnCount(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Information(wdMaximumNumberOfColumns)

	def getCurrentColumnCount(self):
		return self.getColumnCount(self.getCaretPosition())

	def getPageNumber(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Information(wdActiveEndPageNumber)

	def getCurrentPageNumber(self):
		return self.getPageNumber(self.getCaretPosition())

	def getPageCount(self):
		return self.dom.Selection.Information(wdNumberOfPagesInDocument)

	def getParagraphAlignment(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		align=rangeObj.ParagraphFormat.Alignment
		if align==wdAlignParagraphLeft:
			return "left"
		elif align==wdAlignParagraphCenter:
			return "centered"
		elif align==wdAlignParagraphRight:
			return "right"
		elif align>=wdAlignParagraphJustify:
			return "justified"

	def reportChanges(self):
		if conf["documentFormatting"]["reportPageChanges"]:
			pageNumber=self.getCurrentPageNumber()
			if pageNumber!=self.lastPageNumber:
				audio.speakMessage("Page %d of %d"%(pageNumber,self.getPageCount()))
				self.lastPageNumber=pageNumber
		if conf["documentFormatting"]["reportTables"]:
			isTable=self.isCurrentTable()
			if isTable!=self.lastIsTable:
				if isTable:
					audio.speakMessage("Table with %d columns and %d rows"%(self.getCurrentColumnCount(),self.getCurrentRowCount()))
				elif self.lastIsTable: 
					audio.speakMessage("out of table")
					self.lastRowNumber=self.lastColumnNumber=None
				self.lastIsTable=isTable
			rowNumber=self.getCurrentRowNumber()
			columnNumber=self.getCurrentColumnNumber()
			if self.isCurrentTable() and ((rowNumber!=self.lastRowNumber) or (columnNumber!=self.lastColumnNumber)):
				audio.speakMessage("col %d row %d"%(columnNumber,rowNumber))
				self.lastRowNumber=rowNumber
				self.lastColumnNumber=columnNumber
		if conf["documentFormatting"]["reportStyleChanges"]:
			style=self.getCurrentStyle()
			if style!=self.lastStyle:
				audio.speakMessage("%s style"%style)
				self.lastStyle=style
		NVDAObjects.NVDAObject_ITextDocument.reportChanges(self)

	def script_moveByParagraph(self,keyPress):
		sendKey(keyPress)
		audio.speakText(self.getCurrentParagraph())

	def script_formatInfo(self,keyPress):
		audio.speakMessage("%s style"%self.getCurrentStyle())
		NVDAObjects.NVDAObject_ITextDocument.script_formatInfo(self,keyPress)
