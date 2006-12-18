import ctypes
import comtypesClient
import comtypes.automation
import MSAAHandler
import audio
import debug
from constants import *
from keyboardHandler import sendKey, key
import config
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

class appModule(_MSOffice.appModule):

	def __init__(self,*args):
		_MSOffice.appModule.__init__(self,*args)
		NVDAObjects.MSAA.registerNVDAObjectClass(self.processID,"_WwG",ROLE_SYSTEM_CLIENT,NVDAObject_wordDocument)

	def __del__(self):
		NVDAObjects.MSAA.unregisterNVDAObjectClass(self.processID,"_WwG",ROLE_SYSTEM_CLIENT)
		_MSOffice.appModule.__del__(self)

class NVDAObject_wordDocument(NVDAObjects.ITextDocument.NVDAObject_ITextDocument,NVDAObjects.MSAA.NVDAObject_MSAA):

	def __init__(self,*args,**vars):
		NVDAObjects.MSAA.NVDAObject_MSAA.__init__(self,*args,**vars)
		NVDAObjects.ITextDocument.NVDAObject_ITextDocument.__init__(self,*args)
		self.registerPresentationAttribute("style",self.msgStyle,lambda: config.conf["documentFormatting"]["reportStyle"])
		self.registerPresentationAttribute("page",self.msgPage,lambda: config.conf["documentFormatting"]["reportPage"])
		self.registerPresentationAttribute("table",self.msgTable,lambda: config.conf["documentFormatting"]["reportTables"])
		self.registerPresentationAttribute("tableRow",self.msgTableRow,lambda: config.conf["documentFormatting"]["reportTables"])
		self.registerPresentationAttribute("tableColumn",self.msgTableColumn,lambda: config.conf["documentFormatting"]["reportTables"])
		self.registerScriptKeys({
			key("control+ExtendedUp"):self.script_moveByParagraph,
			key("control+ExtendedDown"):self.script_moveByParagraph,
		})

	def getDocumentObjectModel(self):
		ptr=ctypes.POINTER(comtypes.automation.IDispatch)()
		if ctypes.windll.oleacc.AccessibleObjectFromWindow(self.windowHandle,OBJID_NATIVEOM,ctypes.byref(ptr._iid_),ctypes.byref(ptr))!=0:
			raise OSError("No native object model")
		return comtypesClient.wrap(ptr)

	def destroyObjectModel(self,om):
		pass

	def _duplicateDocumentRange(self,rangeObj):
		return rangeObj.Range

	def _get_role(self):
		return ROLE_SYSTEM_TEXT

	def _get_visibleRange(self):
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

	def getLineEnd(self,pos):
		saveSelection=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj=self.dom.Selection
		rangeObj.Start=rangeObj.End=pos
		rangeObj.Expand(wdLine)
		end=rangeObj.End
		rangeObj.Start=saveSelection.Start
		rangeObj.End=saveSelection.End
		return end

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

	def oldnextWord(self,pos):
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

	def oldpreviousWord(self,pos):
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

	def oldnextCharacter(self,pos):
		saveSelection=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj=self.dom.Selection
		rangeObj.Start=rangeObj.End=pos
		rangeObj.Move(wdCharacter,1)
		newPos=rangeObj.Start
		rangeObj.Start=saveSelection.Start
		rangeObj.End=saveSelection.End
		if newPos!=pos:
			return newPos
		else:
			return None

	def oldpreviousCharacter(self,pos):
		saveSelection=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj=self.dom.Selection
		rangeObj.Start=rangeObj.End=pos
		rangeObj.Move(wdCharacter,-1)
		newPos=rangeObj.Start
		rangeObj.Start=saveSelection.Start
		rangeObj.End=saveSelection.End
		if newPos!=pos:
			return newPos
		else:
			return None

	def event_caret(self):
		pass #We sometimes have to move the caret to compute other values

	def getStyle(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Style.NameLocal

	def msgStyle(self,pos):
		return _("style")+" %s"%self.getStyle(pos)


	def isTable(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Information(wdWithInTable)

	def msgTable(self,pos):
		if self.isTable(pos):
			return (MSAAHandler.getRoleName(ROLE_SYSTEM_TABLE)+" with %s "+_("columns")+" and %s "+_("rows"))%(self.getColumnCount(pos),self.getRowCount(pos))
		else:
			return "not in %s"%MSAAHandler.getRoleName(ROLE_SYSTEM_TABLE)

	def getRowNumber(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Information(wdStartOfRangeRowNumber)

	def msgTableRow(self,pos):
		rowNum=self.getRowNumber(pos)
		if rowNum>0:
			return MSAAHandler.getRoleName(ROLE_SYSTEM_ROW)+" %s"%rowNum

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
			return MSAAHandler.getRoleName(ROLE_SYSTEM_COLUMN)+" %s"%columnNum

	def getColumnCount(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Information(wdMaximumNumberOfColumns)

	def getPageNumber(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Information(wdActiveEndPageNumber)

	def msgPage(self,pos):
		pageNum=self.getPageNumber(pos)
		pageCount=self.pageCount
		if pageCount>0:
			return _("page")+" %s of %s"%(pageNum,pageCount)
		else:
			return _("page")+" %s"%pageNum

	def _get_pageCount(self):
		return self.dom.Selection.Information(wdNumberOfPagesInDocument)

	def getParagraphAlignment(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		align=rangeObj.ParagraphFormat.Alignment
		if align==wdAlignParagraphLeft:
			return _("left")
		elif align==wdAlignParagraphCenter:
			return _("centered")
		elif align==wdAlignParagraphRight:
			return _("right")
		elif align>=wdAlignParagraphJustify:
			return _("justified")

	def script_moveByParagraph(self,keyPress):
		sendKey(keyPress)
		audio.speakText(self.getCurrentParagraph())

