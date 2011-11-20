#appModules/winword.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import ctypes
from comtypes import COMError, GUID, BSTR
import comtypes.client
import comtypes.automation
import NVDAHelper
import XMLFormatting
from logHandler import log
import winUser
import oleacc
import globalVars
import speech
import config
import textInfos
import textInfos.offsets
import controlTypes
from . import Window
from ..behaviors import EditableTextWithoutAutoSelectDetection
 
#Word constants

wdCollapseEnd=0
wdCollapseStart=1
#Indexing
wdActiveEndAdjustedPageNumber=1
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
wdGoToPrevious=3
#GoTo - units
wdGoToPage=1
wdGoToLine=3

wdCommentsStory=4
wdEndnotesStory=3
wdEvenPagesFooterStory=8
wdEvenPagesHeaderStory=6
wdFirstPageFooterStory=11
wdFirstPageHeaderStory=10
wdFootnotesStory=2
wdMainTextStory=1
wdPrimaryFooterStory=9
wdPrimaryHeaderStory=7
wdTextFrameStory=5

storyTypeLocalizedLabels={
	wdCommentsStory:_("Comments"),
	wdEndnotesStory:_("Endnotes"),
	wdEvenPagesFooterStory:_("Even pages footer"),
	wdEvenPagesHeaderStory:_("Even pages header"),
	wdFirstPageFooterStory:_("First page footer"),
	wdFirstPageHeaderStory:_("First page header"),
	wdFootnotesStory:_("Footnotes"),
	wdPrimaryFooterStory:_("Primary footer"),
	wdPrimaryHeaderStory:_("Primary header"),
	wdTextFrameStory:_("Text frame"),
}

winwordWindowIid=GUID('{00020962-0000-0000-C000-000000000046}')

wm_winword_expandToLine=ctypes.windll.user32.RegisterWindowMessageW(u"wm_winword_expandToLine")

NVDAUnitsToWordUnits={
	textInfos.UNIT_CHARACTER:wdCharacter,
	textInfos.UNIT_WORD:wdWord,
	textInfos.UNIT_LINE:wdLine,
	textInfos.UNIT_SENTENCE:wdSentence,
	textInfos.UNIT_PARAGRAPH:wdParagraph,
	textInfos.UNIT_TABLE:wdTable,
	textInfos.UNIT_CELL:wdCell,
	textInfos.UNIT_ROW:wdRow,
	textInfos.UNIT_COLUMN:wdColumn,
	textInfos.UNIT_STORY:wdStory,
	textInfos.UNIT_READINGCHUNK:wdSentence,
}

formatConfigFlagsMap={
	"reportFontName":1,
	"reportFontSize":2,
	"reportFontAttributes":4,
	"reportColor":8,
	"reportAlignment":16,
	"reportStyle":32,
	"reportSpellingErrors":64,
	"reportPage":128,
	"reportLineNumber":256,
	"reportTables":512,
	"reportLists":1024,
}

class WordDocumentTextInfo(textInfos.TextInfo):

	def _moveInTable(self,c=0,r=0):
		try:
			cell=self._rangeObj.cells[1]
		except:
			return False
		try:
			columnIndex=cell.columnIndex
			rowIndex=cell.rowIndex
		except:
			return False
		if columnIndex==1 and c<0:
			return False
		if rowIndex==1 and r<0:
			return False
		try:
			self._rangeObj=self._rangeObj.tables[1].columns[columnIndex+c].cells[rowIndex+r].range
		except:
			return False
		return True

	def _expandToLineAtCaret(self):
		lineStart=ctypes.c_int()
		lineEnd=ctypes.c_int()
		res=NVDAHelper.localLib.nvdaInProcUtils_winword_expandToLine(self.obj.appModule.helperLocalBindingHandle,self.obj.windowHandle,self._rangeObj.start,ctypes.byref(lineStart),ctypes.byref(lineEnd))
		if res!=0:
			raise ctypes.WinError(res)
		self._rangeObj.setRange(lineStart.value,lineEnd.value)

	def _getFormatFieldAtRange(self,range,formatConfig):
		formatField=textInfos.FormatField()
		fontObj=None
		paraFormatObj=None
		listString=range.ListFormat.ListString
		if listString and range.Paragraphs[1].range.start==range.start:
			formatField['line-prefix']=listString
		if formatConfig["reportSpellingErrors"] and range.spellingErrors.count>0: 
			formatField["invalid-spelling"]=True
		if formatConfig["reportLineNumber"]:
			formatField["line-number"]=range.Information(wdFirstCharacterLineNumber)
		if formatConfig["reportPage"]:
			formatField["page-number"]=range.Information(wdActiveEndAdjustedPageNumber)
		if formatConfig["reportStyle"]:
			formatField["style"]=range.style.nameLocal
		if formatConfig["reportTables"] and range.Information(wdWithInTable):
			tableInfo={}
			tableInfo["column-count"]=range.Information(wdMaximumNumberOfColumns)
			tableInfo["row-count"]=range.Information(wdMaximumNumberOfRows)
			tableInfo["column-number"]=range.Information(wdStartOfRangeColumnNumber)
			tableInfo["row-number"]=range.Information(wdStartOfRangeRowNumber)
			formatField["table-info"]=tableInfo
		if formatConfig["reportAlignment"]:
			if not paraFormatObj: paraFormatObj=range.paragraphFormat
			alignment=paraFormatObj.alignment
			if alignment==wdAlignParagraphLeft:
				formatField["text-align"]="left"
			elif alignment==wdAlignParagraphCenter:
				formatField["text-align"]="center"
			elif alignment==wdAlignParagraphRight:
				formatField["text-align"]="right"
			elif alignment==wdAlignParagraphJustify:
				formatField["text-align"]="justify"
		if formatConfig["reportFontName"]:
			if not fontObj: fontObj=range.font
			formatField["font-name"]=fontObj.name
		if formatConfig["reportFontSize"]:
			if not fontObj: fontObj=range.font
			formatField["font-size"]="%spt"%fontObj.size
		if formatConfig["reportFontAttributes"]:
			if not fontObj: fontObj=range.font
			formatField["bold"]=bool(fontObj.bold)
			formatField["italic"]=bool(fontObj.italic)
			formatField["underline"]=bool(fontObj.underline)
			if fontObj.superscript:
				formatField["text-position"]="super"
			elif fontObj.subscript:
				formatField["text-position"]="sub"
		return formatField

	def _expandFormatRange(self,range):
		startLimit=self._rangeObj.start
		endLimit=self._rangeObj.end
		#Only Office 2007 onwards supports moving by format changes, -- and only moveEnd works.
		try:
			range.MoveEnd(13,1)
		except:
			range.Expand(wdWord)
		if range.start<startLimit:
			range.start=startLimit
		if range.end>endLimit:
			range.end=endLimit

	def __init__(self,obj,position,_rangeObj=None):
		super(WordDocumentTextInfo,self).__init__(obj,position)
		if _rangeObj:
			self._rangeObj=_rangeObj.Duplicate
			return
		if isinstance(position,textInfos.Point):
			self._rangeObj=self.obj.WinwordDocumentObject.activeWindow.RangeFromPoint(position.x,position.y)
		elif position==textInfos.POSITION_SELECTION:
			self._rangeObj=self.obj.WinwordSelectionObject.range
		elif position==textInfos.POSITION_CARET:
			self._rangeObj=self.obj.WinwordSelectionObject.range
			self._rangeObj.Collapse()
		elif position==textInfos.POSITION_ALL:
			self._rangeObj=self.obj.WinwordSelectionObject.range
			self._rangeObj.Expand(wdStory)
		elif position==textInfos.POSITION_FIRST:
			self._rangeObj=self.obj.WinwordSelectionObject.range
			self._rangeObj.SetRange(0,0)
		elif position==textInfos.POSITION_LAST:
			self._rangeObj=self.obj.WinwordSelectionObject.range
			self._rangeObj.moveEnd(wdStory,1)
			self._rangeObj.move(wdCharacter,-1)
		elif isinstance(position,textInfos.offsets.Offsets):
			self._rangeObj=self.obj.WinwordSelectionObject.range
			self._rangeObj.SetRange(position.startOffset,position.endOffset)
		else:
			raise NotImplementedError("position: %s"%position)

	def getTextWithFields(self,formatConfig=None):
		if not formatConfig:
			formatConfig=config.conf['documentFormatting']
		text=BSTR()
		formatConfigFlags=sum(y for x,y in formatConfigFlagsMap.iteritems() if formatConfig.get(x,False))
		res=NVDAHelper.localLib.nvdaInProcUtils_winword_getTextInRange(self.obj.appModule.helperLocalBindingHandle,self.obj.windowHandle,self._rangeObj.start,self._rangeObj.end,formatConfigFlags,ctypes.byref(text))
		commandList=XMLFormatting.XMLTextParser().parse(text.value)
		for index in xrange(len(commandList)):
			if isinstance(commandList[index],textInfos.FieldCommand):
				field=commandList[index].field
				if isinstance(field,textInfos.ControlField):
					commandList[index].field=self._normalizeControlField(field)
				elif isinstance(field,textInfos.FormatField):
					commandList[index].field=self._normalizeFormatField(field)
		return commandList

	def _normalizeControlField(self,field):
		storyType=int(field.pop('wdStoryType',0))
		if storyType:
			name=storyTypeLocalizedLabels.get(storyType,None)
			if name:
				field['name']=name
				field['alwaysReportName']=True
				field['role']=controlTypes.ROLE_FRAME
		return field

	def _normalizeFormatField(self,field):
		if field.pop('inTable',False):
			tableInfo={}
			for k in ('table-row-count','table-column-count','table-row-number','table-column-number'):
				val=field.pop(k,0)
				tableInfo[k[6:]]=val
			field['table-info']=tableInfo
		return field

	def expand(self,unit):
		if unit==textInfos.UNIT_LINE and self.basePosition not in (textInfos.POSITION_CARET,textInfos.POSITION_SELECTION):
			unit=textInfos.UNIT_SENTENCE
		if unit==textInfos.UNIT_LINE:
			self._expandToLineAtCaret()
		elif unit==textInfos.UNIT_CHARACTER:
			self._rangeObj.moveEnd(wdCharacter,1)
		elif unit in NVDAUnitsToWordUnits:
			self._rangeObj.Expand(NVDAUnitsToWordUnits[unit])
		else:
			raise NotImplementedError("unit: %s"%unit)

	def compareEndPoints(self,other,which):
		if which=="startToStart":
			diff=self._rangeObj.Start-other._rangeObj.Start
		elif which=="startToEnd":
			diff=self._rangeObj.Start-other._rangeObj.End
		elif which=="endToStart":
			diff=self._rangeObj.End-other._rangeObj.Start
		elif which=="endToEnd":
			diff=self._rangeObj.End-other._rangeObj.End
		else:
			raise ValueError("bad argument - which: %s"%which)
		if diff<0:
			diff=-1
		elif diff>0:
			diff=1
		return diff

	def setEndPoint(self,other,which):
		if which=="startToStart":
			self._rangeObj.Start=other._rangeObj.Start
		elif which=="startToEnd":
			self._rangeObj.Start=other._rangeObj.End
		elif which=="endToStart":
			self._rangeObj.End=other._rangeObj.Start
		elif which=="endToEnd":
			self._rangeObj.End=other._rangeObj.End
		else:
			raise ValueError("bad argument - which: %s"%which)

	def _get_isCollapsed(self):
		if self._rangeObj.Start==self._rangeObj.End:
			return True
		else:
			return False

	def collapse(self,end=False):
		if end:
			oldEndOffset=self._rangeObj.end
		self._rangeObj.collapse(wdCollapseEnd if end else wdCollapseStart)
		if end and self._rangeObj.end<oldEndOffset:
			raise RuntimeError

	def copy(self):
		return WordDocumentTextInfo(self.obj,None,_rangeObj=self._rangeObj)

	def _get_text(self):
		text=self._rangeObj.text
		if not text:
			text=""
		return text

	def move(self,unit,direction,endPoint=None):
		if unit==textInfos.UNIT_LINE:
			unit=textInfos.UNIT_SENTENCE
		if unit in NVDAUnitsToWordUnits:
			unit=NVDAUnitsToWordUnits[unit]
		else:
			raise NotImplementedError("unit: %s"%unit)
		if endPoint=="start":
			moveFunc=self._rangeObj.MoveStart
		elif endPoint=="end":
			moveFunc=self._rangeObj.MoveEnd
		else:
			moveFunc=self._rangeObj.Move
		res=moveFunc(unit,direction)
		#units higher than character and word expand to contain the last text plus the insertion point offset in the document
		#However move from a character before will incorrectly move to this offset which makes move/expand contridictory to each other
		#Make sure that move fails if it lands on the final offset but the unit is bigger than character/word
		if direction>0 and endPoint!="end" and unit not in (wdCharacter,wdWord)  and (self._rangeObj.start+1)==self.obj.WinwordDocumentObject.characters.count:
			return 0
		return res

	def _get_bookmark(self):
		return textInfos.offsets.Offsets(self._rangeObj.Start,self._rangeObj.End)

	def updateCaret(self):
		self.obj.WinwordWindowObject.ScrollIntoView(self._rangeObj)
		self.obj.WinwordSelectionObject.SetRange(self._rangeObj.Start,self._rangeObj.Start)

	def updateSelection(self):
		self.obj.WinwordWindowObject.ScrollIntoView(self._rangeObj)
		self.obj.WinwordSelectionObject.SetRange(self._rangeObj.Start,self._rangeObj.End)

class WordDocument(EditableTextWithoutAutoSelectDetection, Window):

	TextInfo=WordDocumentTextInfo

	def __init__(self,*args,**kwargs):
		super(WordDocument,self).__init__(*args,**kwargs)

	def _get_role(self):
		return controlTypes.ROLE_EDITABLETEXT

	def _get_WinwordVersion(self):
		if not hasattr(self,'_WinwordVersion'):
			self._WinwordVersion=float(self.WinwordWindowObject.application.version)
		return self._WinwordVersion

	def _get_WinwordWindowObject(self):
		if not getattr(self,'_WinwordWindowObject',None): 
			try:
				pDispatch=oleacc.AccessibleObjectFromWindow(self.windowHandle,winUser.OBJID_NATIVEOM,interface=comtypes.automation.IDispatch)
			except (COMError, WindowsError):
				log.debugWarning("Could not get MS Word object model",exc_info=True)
				return None
			self._WinwordWindowObject=comtypes.client.dynamic.Dispatch(pDispatch)
 		return self._WinwordWindowObject

	def _get_WinwordDocumentObject(self):
		if not getattr(self,'_WinwordDocumentObject',None): 
			windowObject=self.WinwordWindowObject
			if not windowObject: return None
			self._WinwordDocumentObject=windowObject.document
 		return self._WinwordDocumentObject

	def _get_WinwordApplicationObject(self):
		if not getattr(self,'_WinwordApplicationObject',None): 
			self._WinwordApplicationObject=self.WinwordWindowObject.application
 		return self._WinwordApplicationObject

	def _get_WinwordSelectionObject(self):
		if not getattr(self,'_WinwordSelectionObject',None):
			windowObject=self.WinwordWindowObject
			if not windowObject: return None
			self._WinwordSelectionObject=windowObject.selection
		return self._WinwordSelectionObject

	def script_tab(self,gesture):
		gesture.send()
		info=self.makeTextInfo(textInfos.POSITION_CARET)
		if info._rangeObj.tables.count>0:
			info.expand(textInfos.UNIT_LINE)
			speech.speakTextInfo(info,reason=speech.REASON_CARET)

	def script_nextRow(self,gesture):
		info=self.makeTextInfo("caret")
		if not info._rangeObj.Information(wdWithInTable):
 			speech.speakMessage(_("not in table"))
			return
		if info._moveInTable(0,1):
			info.updateCaret()
			info.expand(textInfos.UNIT_CELL)
			speech.speakTextInfo(info,reason=speech.REASON_CARET)
		else:
			speech.speakMessage(_("edge of table"))

	def script_previousRow(self,gesture):
		info=self.makeTextInfo("caret")
		if not info._rangeObj.Information(wdWithInTable):
 			speech.speakMessage(_("not in table"))
			return
		if info._moveInTable(0,-1):
			info.updateCaret()
			info.expand(textInfos.UNIT_CELL)
			speech.speakTextInfo(info,reason=speech.REASON_CARET)
		else:
			speech.speakMessage(_("edge of table"))

	def script_nextColumn(self,gesture):
		info=self.makeTextInfo("caret")
		if not info._rangeObj.Information(wdWithInTable):
 			speech.speakMessage(_("not in table"))
			return
		if info._moveInTable(1,0):
			info.updateCaret()
			info.expand(textInfos.UNIT_CELL)
			speech.speakTextInfo(info,reason=speech.REASON_CARET)
		else:
			speech.speakMessage(_("edge of table"))

	def script_previousColumn(self,gesture):
		info=self.makeTextInfo("caret")
		if not info._rangeObj.Information(wdWithInTable):
 			speech.speakMessage(_("not in table"))
			return
		if info._moveInTable(-1,0):
			info.updateCaret()
			info.expand(textInfos.UNIT_CELL)
			speech.speakTextInfo(info,reason=speech.REASON_CARET)
		else:
			speech.speakMessage(_("edge of table"))

	__gestures = {
		"kb:tab": "tab",
		"kb:shift+tab": "tab",
		"kb:control+alt+upArrow": "previousRow",
		"kb:control+alt+downArrow": "nextRow",
		"kb:control+alt+leftArrow": "previousColumn",
		"kb:control+alt+rightArrow": "nextColumn",
		"kb:control+pageUp": "caret_moveByLine",
		"kb:control+pageDown": "caret_moveByLine",
	}
