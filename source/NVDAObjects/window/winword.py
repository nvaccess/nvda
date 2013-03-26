#appModules/winword.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2012 NVDA Contributors
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import ctypes
from comtypes import COMError, GUID, BSTR
import comtypes.client
import comtypes.automation
import locale
import languageHandler
import ui
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
import colors
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
	"reportLinks":2048,
	"reportComments":4096,
	"reportHeadings":8192,
	"autoLanguageSwitching":16384,	
}

class WordDocumentTextInfo(textInfos.TextInfo):

	def _expandToLineAtCaret(self):
		lineStart=ctypes.c_int()
		lineEnd=ctypes.c_int()
		res=NVDAHelper.localLib.nvdaInProcUtils_winword_expandToLine(self.obj.appModule.helperLocalBindingHandle,self.obj.windowHandle,self._rangeObj.start,ctypes.byref(lineStart),ctypes.byref(lineEnd))
		if res!=0 or (lineStart.value==lineEnd.value==-1): 
			log.debugWarning("winword_expandToLine failed")
			self._rangeObj.expand(wdParagraph)
			return
		self._rangeObj.setRange(lineStart.value,lineEnd.value)

	def __init__(self,obj,position,_rangeObj=None):
		super(WordDocumentTextInfo,self).__init__(obj,position)
		if _rangeObj:
			self._rangeObj=_rangeObj.Duplicate
			return
		if isinstance(position,textInfos.Point):
			try:
				self._rangeObj=self.obj.WinwordDocumentObject.activeWindow.RangeFromPoint(position.x,position.y)
			except COMError:
				raise NotImplementedError
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
		formatConfig['autoLanguageSwitching']=config.conf['speech'].get('autoLanguageSwitching',False)
		startOffset=self._rangeObj.start
		endOffset=self._rangeObj.end
		if startOffset==endOffset:
			return []
		text=BSTR()
		formatConfigFlags=sum(y for x,y in formatConfigFlagsMap.iteritems() if formatConfig.get(x,False))
		res=NVDAHelper.localLib.nvdaInProcUtils_winword_getTextInRange(self.obj.appModule.helperLocalBindingHandle,self.obj.windowHandle,startOffset,endOffset,formatConfigFlags,ctypes.byref(text))
		if res or not text:
			log.debugWarning("winword_getTextInRange failed with %d"%res)
			return [self.text]
		commandList=XMLFormatting.XMLTextParser().parse(text.value)
		for index,item in enumerate(commandList):
			if isinstance(item,textInfos.FieldCommand):
				field=item.field
				if isinstance(field,textInfos.ControlField):
					item.field=self._normalizeControlField(field)
				elif isinstance(field,textInfos.FormatField):
					item.field=self._normalizeFormatField(field)
			elif index>0 and isinstance(item,basestring) and item.isspace():
				 #2047: don't expose language for whitespace as its incorrect for east-asian languages 
				lastItem=commandList[index-1]
				if isinstance(lastItem,textInfos.FieldCommand) and isinstance(lastItem.field,textInfos.FormatField):
					try:
						del lastItem.field['language']
					except KeyError:
						pass
		return commandList

	def _normalizeControlField(self,field):
		role=field.pop('role',None)
		if role=="heading":
			role=controlTypes.ROLE_HEADING
		elif role=="table":
			role=controlTypes.ROLE_TABLE
			field['table-rowcount']=int(field.get('table-rowcount',0))
			field['table-columncount']=int(field.get('table-columncount',0))
		elif role=="tableCell":
			role=controlTypes.ROLE_TABLECELL
			field['table-rownumber']=int(field.get('table-rownumber',0))
			field['table-columnnumber']=int(field.get('table-columnnumber',0))
		elif role=="footnote":
			role=controlTypes.ROLE_FOOTNOTE
		elif role=="endnote":
			role=controlTypes.ROLE_ENDNOTE
		elif role=="graphic":
			role=controlTypes.ROLE_GRAPHIC
		elif role=="object":
			role=controlTypes.ROLE_EMBEDDEDOBJECT
		else:
			role=controlTypes.ROLE_UNKNOWN
		field['role']=role
		storyType=int(field.pop('wdStoryType',0))
		if storyType:
			name=storyTypeLocalizedLabels.get(storyType,None)
			if name:
				field['name']=name
				field['alwaysReportName']=True
				field['role']=controlTypes.ROLE_FRAME
		return field

	def _normalizeFormatField(self,field):
		color=field.pop('color',None)
		if color is not None:
			field['color']=colors.RGB.fromCOLORREF(int(color))		
		try:
			languageId = int(field.pop('wdLanguageId',0))
			if languageId:
				field['language']=self._getLanguageFromLcid(languageId)
		except:
			log.debugWarning("language error",exc_info=True)
			pass
		return field

	def _getLanguageFromLcid(self, lcid):
		"""
		gets a normalized locale from a lcid
		"""
		lang = locale.windows_locale[lcid]
		if lang:
			return languageHandler.normalizeLanguage(lang)
		
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

	def event_caret(self):
		curSelectionPos=self.makeTextInfo(textInfos.POSITION_SELECTION)
		lastSelectionPos=getattr(self,'_lastSelectionPos',None)
		self._lastSelectionPos=curSelectionPos
		if lastSelectionPos:
			if curSelectionPos._rangeObj.isEqual(lastSelectionPos._rangeObj):
				return
		super(WordDocument,self).event_caret()

	def _get_role(self):
		return controlTypes.ROLE_EDITABLETEXT

	def _get_states(self):
		states=super(WordDocument,self).states
		states.add(controlTypes.STATE_MULTILINE)
		return states

	def _get_WinwordVersion(self):
		if not hasattr(self,'_WinwordVersion'):
			self._WinwordVersion=float(self.WinwordApplicationObject.version)
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
			speech.speakTextInfo(info,reason=controlTypes.REASON_CARET)

	def _moveInTable(self,row=True,forward=True):
		info=self.makeTextInfo(textInfos.POSITION_CARET)
		info.expand(textInfos.UNIT_CHARACTER)
		formatConfig=config.conf['documentFormatting'].copy()
		formatConfig['reportTables']=True
		commandList=info.getTextWithFields(formatConfig)
		if len(commandList)<3 or commandList[1].field.get('role',None)!=controlTypes.ROLE_TABLE or commandList[2].field.get('role',None)!=controlTypes.ROLE_TABLECELL:
			# Translators: The message reported when a user attempts to use a table movement command
			# when the cursor is not withnin a table.
			ui.message(_("Not in table"))
			return False
		rowCount=commandList[1].field.get('table-rowcount',1)
		columnCount=commandList[1].field.get('table-columncount',1)
		rowNumber=commandList[2].field.get('table-rownumber',1)
		columnNumber=commandList[2].field.get('table-columnnumber',1)
		if row:
			rowNumber+=1 if forward else -1
		else:
			columnNumber+=1 if forward else -1
		if rowNumber<1 or rowNumber>rowCount or columnNumber<1 or columnNumber>columnCount:
			# Translators: The message reported when a user attempts to use a table movement command
			# but the cursor can't be moved in that direction because it is at the edge of the table.
			ui.message(_("Edge of table"))
			return False
		try:
			table=info._rangeObj.tables[1]
		except COMError:
			log.debugWarning("Could not get MS Word table object indicated in XML")
			ui.message(_("Not in table"))
			return False
		while (columnNumber if row else rowNumber)>0:
			try:
				cell=table.cell(rowNumber,columnNumber)
				break
			except COMError:
				cell=None
				if row:
					columnNumber-=1
				else:
					rowNumber-=1
		if not cell:
			ui.message(_("Edge of table"))
			return False
		newInfo=WordDocumentTextInfo(self,textInfos.POSITION_CARET,_rangeObj=cell.range)
		speech.speakTextInfo(newInfo,reason=controlTypes.REASON_CARET)
		newInfo.collapse()
		newInfo.updateCaret()
		return True

	def script_nextRow(self,gesture):
		self._moveInTable(row=True,forward=True)

	def script_previousRow(self,gesture):
		self._moveInTable(row=True,forward=False)

	def script_nextColumn(self,gesture):
		self._moveInTable(row=False,forward=True)

	def script_previousColumn(self,gesture):
		self._moveInTable(row=False,forward=False)

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

