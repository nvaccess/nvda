import ctypes
import comtypesClient
import comtypes.automation
import audio
import debug
from constants import *
from keyboardHandler import sendKey, key
from config import conf
import NVDAObjects
import lang
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

class appModule(_MSOffice.appModule):

	def __init__(self):
		_MSOffice.appModule.__init__(self)
		NVDAObjects.registerNVDAObjectClass("_WwG",ROLE_SYSTEM_CLIENT,NVDAObject_wordDocument)

	def __del__(self):
		NVDAObjects.unregisterNVDAObjectClass("_WwG",ROLE_SYSTEM_CLIENT)
		_MSOffice.appModule.__del__(self)

class NVDAObject_wordDocument(NVDAObjects.NVDAObject_ITextDocument):

	def __init__(self,*args):
		NVDAObjects.NVDAObject_ITextDocument.__init__(self,*args)
		self.presentationTable.insert(0,[self.msgStyle,["documentFormatting","reportStyle"],None,None])
		self.presentationTable.insert(1,[self.msgPage,["documentFormatting","reportPage"],None,None])
		self.presentationTable.insert(2,[self.msgTable,["documentFormatting","reportTables"],None,None])
		self.presentationTable.insert(3,[self.msgTableRow,["documentFormatting","reportTables"],None,None])
		self.presentationTable.insert(4,[self.msgTableColumn,["documentFormatting","reportTables"],None,None])
		self.keyMap.update({
			key("control+ExtendedUp"):self.script_moveByParagraph,
			key("control+ExtendedDown"):self.script_moveByParagraph,
		})

	def getDocumentObjectModel(self):
		ptr=ctypes.POINTER(comtypes.automation.IDispatch)()
		if ctypes.windll.oleacc.AccessibleObjectFromWindow(self.getWindowHandle(),OBJID_NATIVEOM,ctypes.byref(ptr._iid_),ctypes.byref(ptr))!=0:
			raise OSError("No native object model")
		return comtypesClient.wrap(ptr)


	def destroyObjectModel(self,om):
		pass

	def _duplicateDocumentRange(self,rangeObj):
		return rangeObj.Range

	def getRole(self):
		return ROLE_SYSTEM_TEXT

	def event_caret(self):
		pass #These scripts must move the selection to get lines etc


	def getVisibleRange(self):
		(left,top,right,bottom)=self.getLocation()
		topRange=self.dom.Application.ActiveWindow.RangeFromPoint(left,top)
		bottomRange=self.dom.Application.ActiveWindow.RangeFromPoint(right,bottom)
		return (topRange.Start,bottomRange.Start)

	def getLineNumber(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Information(wdFirstCharacterLineNumber)-1

	def getLineStart(self,pos):
		saveSelection=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj=self.dom.Selection
		rangeObj.Start=rangeObj.End=pos
		rangeObj.Expand(wdLine)
		lineStart=rangeObj.Start
		rangeObj.Start=saveSelection.Start
		rangeObj.End=saveSelection.End
		return lineStart

	def getLineLength(self,pos):
		saveSelection=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj=self.dom.Selection
		rangeObj.Start=rangeObj.End=pos
		rangeObj.Expand(wdLine)
		lineStart=rangeObj.Start
		lineEnd=rangeObj.End
		rangeObj.Start=saveSelection.Start
		rangeObj.End=saveSelection.End
		return lineEnd-lineStart

	def getLine(self,pos):
		saveSelection=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj=self.dom.Selection
		rangeObj.Start=rangeObj.End=pos
		rangeObj.Expand(wdLine)
		text=rangeObj.Text
		rangeObj.Start=saveSelection.Start
		rangeObj.End=saveSelection.End
		if text=="\r\n":
			text=None
		return text

	def nextWord(self,pos):
		saveSelection=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj=self.dom.Selection
		rangeObj.Start=rangeObj.End=pos
		rangeObj.Move(wdWord,1)
		newPos=rangeObj.Start
		rangeObj.Start=saveSelection.Start
		rangeObj.End=saveSelection.End
		if newPos!=pos:
			return newPos
		else:
			return None

	def previousWord(self,pos):
		saveSelection=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj=self.dom.Selection
		rangeObj.Start=rangeObj.End=pos
		rangeObj.Move(wdWord,-1)
		newPos=rangeObj.Start
		rangeObj.Start=saveSelection.Start
		rangeObj.End=saveSelection.End
		if newPos!=pos:
			return newPos
		else:
			return None

	def nextLine(self,pos):
		saveSelection=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj=self.dom.Selection
		rangeObj.Start=rangeObj.End=pos
		rangeObj.Move(wdLine,1)
		newPos=rangeObj.Start
		rangeObj.Start=saveSelection.Start
		rangeObj.End=saveSelection.End
		if newPos!=pos:
			return newPos
		else:
			return None

	def previousLine(self,pos):
		saveSelection=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj=self.dom.Selection
		rangeObj.Start=rangeObj.End=pos
		rangeObj.Move(wdLine,-1)
		newPos=rangeObj.Start
		rangeObj.Start=saveSelection.Start
		rangeObj.End=saveSelection.End
		if newPos!=pos:
			return newPos
		else:
			return None

	def getStyle(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Style.NameLocal

	def msgStyle(self,pos):
		return lang.messages["style"]+" %s"%self.getStyle(pos)


	def isTable(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Information(wdWithInTable)

	def msgTable(self,pos):
		if self.isTable(pos):
			return (NVDAObjects.getRoleName(ROLE_SYSTEM_TABLE)+" with %s "+lang.messages["columns"]+" and %s "+lang.messages["rows"])%(self.getColumnCount(pos),self.getRowCount(pos))
		else:
			return "not in %s"%NVDAObjects.getRoleName(ROLE_SYSTEM_TABLE)

	def getRowNumber(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Information(wdStartOfRangeRowNumber)

	def msgTableRow(self,pos):
		rowNum=self.getRowNumber(pos)
		if rowNum>0:
			return NVDAObjects.getRoleName(ROLE_SYSTEM_ROW)+" %s"%rowNum

	def getRowCount(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Information(wdMaximumNumberOfRows)

	def getColumnNumber(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Information(wdStartOfRangeColumnNumber)

	def msgTableColumn(self,pos):
		columnNum=self.getColumnNumber(pos)
		if columnNum>0:
			return NVDAObjects.getRoleName(ROLE_SYSTEM_COLUM)+" %s"%columnNum

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

	def msgPage(self,pos):
		pageNum=self.getPageNumber(pos)
		pageCount=self.getPageCount()
		if pageCount>0:
			return lang.messages["page"]+" %s of %s"%(pageNum,pageCount)
		else:
			return lang.messages["page"]+" %s"%pageNum

	def getPageCount(self):
		return self.dom.Selection.Information(wdNumberOfPagesInDocument)

	def getParagraphAlignment(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		align=rangeObj.ParagraphFormat.Alignment
		if align==wdAlignParagraphLeft:
			return lang.messages["left"]
		elif align==wdAlignParagraphCenter:
			return lang.messages["centered"]
		elif align==wdAlignParagraphRight:
			return lang.messages["right"]
		elif align>=wdAlignParagraphJustify:
			return lang.messages["justified"]

	def script_moveByParagraph(self,keyPress):
		sendKey(keyPress)
		audio.speakText(self.getCurrentParagraph())

