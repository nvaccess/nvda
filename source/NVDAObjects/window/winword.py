# -*- coding: UTF-8 -*-
#appModules/winword.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2015 NV Access Limited, Manish Agrawal
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import ctypes
import time
from comtypes import COMError, GUID, BSTR
import comtypes.client
import comtypes.automation
import uuid
import operator
import locale
import collections
import sayAllHandler
import eventHandler
import braille
import scriptHandler
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
import treeInterceptorHandler
import browseMode
import review
import inputCore
import api
import re
from cursorManager import CursorManager, ReviewCursorManager
from tableUtils import HeaderCellInfo, HeaderCellTracker
from . import Window
from ..behaviors import EditableTextWithoutAutoSelectDetection
from . import _msOfficeChartConstants 
#Word constants

# wdMeasurementUnits
wdInches=0
wdCentimeters=1
wdMillimeters=2
wdPoints=3
wdPicas=4

wdCollapseEnd=0
wdCollapseStart=1
#Indexing
wdActiveEndAdjustedPageNumber=1
wdActiveEndPageNumber=3
wdNumberOfPagesInDocument=4
wdHorizontalPositionRelativeToPage=5
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
wdGoToBookmark=-1
wdGoToSection=0
wdGoToPage=1
wdGoToTable=2
wdGoToLine=3
wdGoToFootnote=4
wdGoToEndnote=5
wdGoToComment=6
wdGoToField=7
wdGoToGraphic=8
wdGoToObject=9
wdGoToEquation=10
wdGoToHeading=11
wdGoToPercent=12
wdGoToSpellingError=13
wdGoToGrammaticalError=14
wdGoToProofreadingError=15

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

wdFieldFormTextInput=70
wdFieldFormCheckBox=71
wdFieldFormDropDown=83
wdContentControlRichText=0
wdContentControlText=1
wdContentControlPicture=2
wdContentControlComboBox=3
wdContentControlDropdownList=4
wdContentControlBuildingBlockGallery=5
wdContentControlDate=6
wdContentControlGroup=7
wdContentControlCheckBox=8
wdInlineShapeChart=12

wdNoRevision=0
wdRevisionInsert=1
wdRevisionDelete=2
wdRevisionProperty=3
wdRevisionParagraphNumber=4
wdRevisionDisplayField=5
wdRevisionReconcile=6
wdRevisionConflict=7
wdRevisionStyle=8
wdRevisionReplace=9
wdRevisionParagraphProperty=10
wdRevisionTableProperty=11
wdRevisionSectionProperty=12
wdRevisionStyleDefinition=13
wdRevisionMovedFrom=14
wdRevisionMovedTo=15
wdRevisionCellInsertion=16
wdRevisionCellDeletion=17
wdRevisionCellMerge=18

wdRevisionTypeLabels={
	# Translators: a Microsoft Word revision type (inserted content) 
	wdRevisionInsert:_("insertion"),
	# Translators: a Microsoft Word revision type (deleted content) 
	wdRevisionDelete:_("deletion"),
	# Translators: a Microsoft Word revision type (changed content property, e.g. font, color)
	wdRevisionProperty:_("property"),
	# Translators: a Microsoft Word revision type (changed paragraph number)
	wdRevisionParagraphNumber:_("paragraph number"),
	# Translators: a Microsoft Word revision type (display field)
	wdRevisionDisplayField:_("display field"),
	# Translators: a Microsoft Word revision type (reconcile) 
	wdRevisionReconcile:_("reconcile"),
	# Translators: a Microsoft Word revision type (conflicting revision)
	wdRevisionConflict:_("conflict"),
	# Translators: a Microsoft Word revision type (style change)
	wdRevisionStyle:_("style"),
	# Translators: a Microsoft Word revision type (replaced content) 
	wdRevisionReplace:_("replace"),
	# Translators: a Microsoft Word revision type (changed paragraph property, e.g. alignment)
	wdRevisionParagraphProperty:_("paragraph property"),
	# Translators: a Microsoft Word revision type (table)
	wdRevisionTableProperty:_("table property"),
	# Translators: a Microsoft Word revision type (section property) 
	wdRevisionSectionProperty:_("section property"),
	# Translators: a Microsoft Word revision type (style definition)
	wdRevisionStyleDefinition:_("style definition"),
	# Translators: a Microsoft Word revision type (moved from)
	wdRevisionMovedFrom:_("moved from"),
	# Translators: a Microsoft Word revision type (moved to)
	wdRevisionMovedTo:_("moved to"),
	# Translators: a Microsoft Word revision type (inserted table cell)
	wdRevisionCellInsertion:_("cell insertion"),
	# Translators: a Microsoft Word revision type (deleted table cell)
	wdRevisionCellDeletion:_("cell deletion"),
	# Translators: a Microsoft Word revision type (merged table cells)
	wdRevisionCellMerge:_("cell merge"),
}

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

wdFieldTypesToNVDARoles={
	wdFieldFormTextInput:controlTypes.ROLE_EDITABLETEXT,
	wdFieldFormCheckBox:controlTypes.ROLE_CHECKBOX,
	wdFieldFormDropDown:controlTypes.ROLE_COMBOBOX,
}

wdContentControlTypesToNVDARoles={
	wdContentControlRichText:controlTypes.ROLE_EDITABLETEXT,
	wdContentControlText:controlTypes.ROLE_EDITABLETEXT,
	wdContentControlPicture:controlTypes.ROLE_GRAPHIC,
	wdContentControlComboBox:controlTypes.ROLE_COMBOBOX,
	wdContentControlDropdownList:controlTypes.ROLE_COMBOBOX,
	wdContentControlDate:controlTypes.ROLE_EDITABLETEXT,
	wdContentControlGroup:controlTypes.ROLE_GROUPING,
	wdContentControlCheckBox:controlTypes.ROLE_CHECKBOX,
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
	"reportRevisions":32768,
	"reportParagraphIndentation":65536,
}
formatConfigFlag_includeLayoutTables=131072

class WordDocumentHeadingQuickNavItem(browseMode.TextInfoQuickNavItem):

	def __init__(self,nodeType,document,textInfo,level):
		self.level=level
		super(WordDocumentHeadingQuickNavItem,self).__init__(nodeType,document,textInfo)

	def isChild(self,parent):
		if not isinstance(parent,WordDocumentHeadingQuickNavItem):
			return False
		return self.level>parent.level

class WordDocumentCollectionQuickNavItem(browseMode.TextInfoQuickNavItem):
	"""
	A QuickNavItem representing an item that MS Word stores as a collection (e.g. link, table etc).
	"""

	def rangeFromCollectionItem(self,item):
		"""
		Fetches a Microsoft Word range object from a Microsoft Word item in a collection. E.g. a HyperLink object.
		@param item: an item from a collection (E.g. a HyperLink object).
		"""
		return item.range

	def __init__(self,itemType,document,collectionItem):
		"""
		See L{TextInfoQuickNavItem} for itemType and document argument definitions.
		@param collectionItem: an item from an MS Word collection  e.g. HyperLink object.
		"""
		self.collectionItem=collectionItem
		self.rangeObj=self.rangeFromCollectionItem(collectionItem)
		textInfo=BrowseModeWordDocumentTextInfo(document,None,_rangeObj=self.rangeObj)
		super(WordDocumentCollectionQuickNavItem,self).__init__(itemType,document,textInfo)

class WordDocumentCommentQuickNavItem(WordDocumentCollectionQuickNavItem):
	@property
	def label(self):
		author=self.collectionItem.author
		date=self.collectionItem.date
		text=self.collectionItem.range.text
		return _(u"comment: {text} by {author} on {date}").format(author=author,text=text,date=date)

	def rangeFromCollectionItem(self,item):
		return item.scope

class WordDocumentRevisionQuickNavItem(WordDocumentCollectionQuickNavItem):
	@property
	def label(self):
		revisionType=wdRevisionTypeLabels.get(self.collectionItem.type)
		author=self.collectionItem.author or ""
		date=self.collectionItem.date
		description=self.collectionItem.formatDescription or ""
		text=(self.collectionItem.range.text or "")[:100]
		return _(u"{revisionType} {description}: {text} by {author} on {date}").format(revisionType=revisionType,author=author,text=text,date=date,description=description)

class WordDocumentChartQuickNavItem(WordDocumentCollectionQuickNavItem):
	@property
	def label(self):
		text=""
		if self.collectionItem.Chart.HasTitle:
			text=self.collectionItem.Chart.ChartTitle.Text
		else:
			text=self.collectionItem.Chart.Name
		return _(u"{text}").format(text=text)

	def moveTo(self):
		chartNVDAObj = WordChart(windowHandle=self.document.rootNVDAObject.windowHandle, wordApplicationObject=self.rangeObj.Document.Application, wordShapeObject=self.collectionItem)
		eventHandler.queueEvent("gainFocus",chartNVDAObj)

class WinWordCollectionQuicknavIterator(object):
	"""
	Allows iterating over an MS Word collection (e.g. HyperLinks) emitting L{QuickNavItem} objects.
	"""

	quickNavItemClass=WordDocumentCollectionQuickNavItem #: the QuickNavItem class that should be instanciated and emitted. 

	def __init__(self,itemType,document,direction,rangeObj,includeCurrent):
		"""
		See L{QuickNavItemIterator} for itemType, document and direction definitions.
		@param rangeObj: a Microsoft Word range object where the collection should be fetched from.
		@ param includeCurrent: if true then any item at the initial position will be also emitted rather than just further ones. 
		"""
		self.document=document
		self.itemType=itemType
		self.direction=direction if direction else "next"
		self.rangeObj=rangeObj
		self.includeCurrent=includeCurrent

	def collectionFromRange(self,rangeObj):
		"""
		Fetches a Microsoft Word collection object from a Microsoft Word range object. E.g. HyperLinks from a range.
		@param rangeObj: a Microsoft Word range object.
		@return: a Microsoft Word collection object.
		"""
		raise NotImplementedError

	def filter(self,item):
		"""
		Only allows certain items fom a collection to be emitted. E.g. a table who's borders are enabled.
		@param item: an item from a Microsoft Word collection (e.g. HyperLink object).
		@return True if this item should be allowd, false otherwise.
		@rtype: bool
		"""
		return True

	def iterate(self):
		"""
		returns a generator that emits L{QuickNavItem} objects for this collection.
		"""
		if self.direction=="next":
			self.rangeObj.moveEnd(wdStory,1)
		elif self.direction=="previous":
			self.rangeObj.collapse(wdCollapseStart)
			self.rangeObj.moveStart(wdStory,-1)
		items=self.collectionFromRange(self.rangeObj)
		itemCount=items.count
		isFirst=True
		for index in xrange(1,itemCount+1):
			if self.direction=="previous":
				index=itemCount-(index-1)
			collectionItem=items[index]
			item=self.quickNavItemClass(self.itemType,self.document,collectionItem)
			itemRange=item.rangeObj
			# Skip over the item we're already on.
			if not self.includeCurrent and isFirst and ((self.direction=="next" and itemRange.start<=self.rangeObj.start) or (self.direction=="previous" and itemRange.end>self.rangeObj.end)):
				continue
			if not self.filter(collectionItem):
				continue
			yield item
			isFirst=False

class LinkWinWordCollectionQuicknavIterator(WinWordCollectionQuicknavIterator):
	def collectionFromRange(self,rangeObj):
		return rangeObj.hyperlinks

class CommentWinWordCollectionQuicknavIterator(WinWordCollectionQuicknavIterator):
	quickNavItemClass=WordDocumentCommentQuickNavItem
	def collectionFromRange(self,rangeObj):
		return rangeObj.comments

class RevisionWinWordCollectionQuicknavIterator(WinWordCollectionQuicknavIterator):
	quickNavItemClass=WordDocumentRevisionQuickNavItem
	def collectionFromRange(self,rangeObj):
		return rangeObj.revisions

class GraphicWinWordCollectionQuicknavIterator(WinWordCollectionQuicknavIterator):
	def collectionFromRange(self,rangeObj):
		return rangeObj.inlineShapes
	def filter(self,item):
		return 2<item.type<5

class TableWinWordCollectionQuicknavIterator(WinWordCollectionQuicknavIterator):
	def collectionFromRange(self,rangeObj):
		return rangeObj.tables
	def filter(self,item):
		return item.borders.enable

class ChartWinWordCollectionQuicknavIterator(WinWordCollectionQuicknavIterator):
	quickNavItemClass=WordDocumentChartQuickNavItem
	def collectionFromRange(self,rangeObj):
		return rangeObj.inlineShapes
	def filter(self,item):
		return item.type==wdInlineShapeChart

class WordDocumentTextInfo(textInfos.TextInfo):

	# #4852: temporary fix.
	# force mouse reading chunk to sentense to make it what it used to be in 2014.4.
	# We need to however fix line so it does not accidentially scroll.
	def _get_unit_mouseChunk(self):
		unit=super(WordDocumentTextInfo,self).unit_mouseChunk
		if unit==textInfos.UNIT_LINE:
			unit=textInfos.UNIT_SENTENCE
		return unit

	def copyToClipboard(self):
		self._rangeObj.copy()
		return True

	def find(self,text,caseSensitive=False,reverse=False):
		f=self._rangeObj.find
		f.text=text
		f.matchCase=caseSensitive
		f.forward=not reverse
		return f.execute()

	shouldIncludeLayoutTables=True #: layout tables should always be included (no matter the user's browse mode setting).

	def activate(self):
		import mathPres
		mathMl=mathPres.getMathMlFromTextInfo(self)
		if mathMl:
			return mathPres.interactWithMathMl(mathMl)
		newRng=self._rangeObj.Duplicate
		newRng.End=newRng.End+1
		if newRng.InlineShapes.Count >= 1:
			if newRng.InlineShapes[1].Type==wdInlineShapeChart:
				return eventHandler.queueEvent('gainFocus',WordChart(windowHandle=self.obj.windowHandle, wordApplicationObject=self.obj.WinwordDocumentObject.Application, wordShapeObject=newRng.InlineShapes[1]))
		# Handle activating links.
		# It is necessary to expand to word to get a link as the link's first character is never actually in the link!
		tempRange=self._rangeObj.duplicate
		tempRange.expand(wdWord)
		links=tempRange.hyperlinks
		if links.count>0:
			links[1].follow()
			return

	def _expandToLineAtCaret(self):
		lineStart=ctypes.c_int()
		lineEnd=ctypes.c_int()
		res=NVDAHelper.localLib.nvdaInProcUtils_winword_expandToLine(self.obj.appModule.helperLocalBindingHandle,self.obj.documentWindowHandle,self._rangeObj.start,ctypes.byref(lineStart),ctypes.byref(lineEnd))
		if res!=0 or lineStart.value==lineEnd.value or lineStart.value==-1 or lineEnd.value==-1: 
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
			self._rangeObj.endOf(wdStory)
			self._rangeObj.move(wdCharacter,-1)
		elif isinstance(position,textInfos.offsets.Offsets):
			self._rangeObj=self.obj.WinwordSelectionObject.range
			self._rangeObj.SetRange(position.startOffset,position.endOffset)
		else:
			raise NotImplementedError("position: %s"%position)

	def getTextWithFields(self,formatConfig=None):
		if self.isCollapsed: return []
		if self.obj.ignoreFormatting:
			return [self.text]
		extraDetail=formatConfig.get('extraDetail',False) if formatConfig else False
		if not formatConfig:
			formatConfig=config.conf['documentFormatting']
		formatConfig['autoLanguageSwitching']=config.conf['speech'].get('autoLanguageSwitching',False)
		startOffset=self._rangeObj.start
		endOffset=self._rangeObj.end
		text=BSTR()
		formatConfigFlags=sum(y for x,y in formatConfigFlagsMap.iteritems() if formatConfig.get(x,False))
		if self.shouldIncludeLayoutTables:
			formatConfigFlags+=formatConfigFlag_includeLayoutTables
		if self.obj.ignoreEditorRevisions:
			formatConfigFlags&=~formatConfigFlagsMap['reportRevisions']
		res=NVDAHelper.localLib.nvdaInProcUtils_winword_getTextInRange(self.obj.appModule.helperLocalBindingHandle,self.obj.documentWindowHandle,startOffset,endOffset,formatConfigFlags,ctypes.byref(text))
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
					item.field=self._normalizeFormatField(field,extraDetail=extraDetail)
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
		elif role=="chart":
			role=controlTypes.ROLE_CHART
		elif role=="object":
			progid=field.get("progid")
			if progid and progid.startswith("Equation.DSMT"):
				# MathType.
				role=controlTypes.ROLE_MATH
			else:
				role=controlTypes.ROLE_EMBEDDEDOBJECT
		else:
			fieldType=int(field.pop('wdFieldType',-1))
			if fieldType!=-1:
				role=wdFieldTypesToNVDARoles.get(fieldType,controlTypes.ROLE_UNKNOWN)
				if fieldType==wdFieldFormCheckBox and int(field.get('wdFieldResult','0'))>0:
					field['states']=set([controlTypes.STATE_CHECKED])
				elif fieldType==wdFieldFormDropDown:
					field['value']=field.get('wdFieldResult',None)
			fieldStatusText=field.pop('wdFieldStatusText',None)
			if fieldStatusText:
				field['name']=fieldStatusText
				field['alwaysReportName']=True
			else:
				fieldType=int(field.get('wdContentControlType',-1))
				if fieldType!=-1:
					role=wdContentControlTypesToNVDARoles.get(fieldType,controlTypes.ROLE_UNKNOWN)
					if role==controlTypes.ROLE_CHECKBOX:
						fieldChecked=bool(int(field.get('wdContentControlChecked','0')))
						if fieldChecked:
							field['states']=set([controlTypes.STATE_CHECKED])
					fieldTitle=field.get('wdContentControlTitle',None)
					if fieldTitle:
						field['name']=fieldTitle
						field['alwaysReportName']=True
		if role is not None: field['role']=role
		storyType=int(field.pop('wdStoryType',0))
		if storyType:
			name=storyTypeLocalizedLabels.get(storyType,None)
			if name:
				field['name']=name
				field['alwaysReportName']=True
				field['role']=controlTypes.ROLE_FRAME
		# Hack support for lazy fetching of row and column header text values
		class ControlField(textInfos.ControlField): 
			def get(d,name,default=None):
				if name=="table-rowheadertext":
					try:
						cell=self._rangeObj.cells[1]
					except IndexError:
						log.debugWarning("no cells for table row, possibly on end of cell mark")
						return super(ControlField,d).get(name,default)
					return self.obj.fetchAssociatedHeaderCellText(cell,False)
				elif name=="table-columnheadertext":
					try:
						cell=self._rangeObj.cells[1]
					except IndexError:
						log.debugWarning("no cells for table row, possibly on end of cell mark")
						return super(ControlField,d).get(name,default)
					return self.obj.fetchAssociatedHeaderCellText(cell,True)
				else:
					return super(ControlField,d).get(name,default)
		newField=ControlField()
		newField.update(field)
		return newField

	def _normalizeFormatField(self,field,extraDetail=False):
		_startOffset=int(field.pop('_startOffset'))
		_endOffset=int(field.pop('_endOffset'))
		revisionType=int(field.pop('wdRevisionType',0))
		if revisionType==wdRevisionInsert:
			field['revision-insertion']=True
		elif revisionType==wdRevisionDelete:
			field['revision-deletion']=True
		elif revisionType:
			revisionLabel=wdRevisionTypeLabels.get(revisionType,None)
			if revisionLabel:
				field['revision']=revisionLabel
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
		for x in ("first-line-indent","left-indent","right-indent","hanging-indent"):
			v=field.get(x)
			if not v: continue
			v=float(v)
			if abs(v)<0.001:
				v=None
			else:
				v=self.obj.getLocalizedMeasurementTextForPointSize(v)
			field[x]=v
		return field

	def _getLanguageFromLcid(self, lcid):
		"""
		gets a normalized locale from a lcid
		"""
		lang = locale.windows_locale[lcid]
		if lang:
			return languageHandler.normalizeLanguage(lang)

	def expand(self,unit):
		if unit==textInfos.UNIT_LINE: 
			try:
				if self._rangeObj.tables.count>0 and self._rangeObj.cells.count==0:
					unit=textInfos.UNIT_CHARACTER
			except COMError:
				pass
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

	def _move(self,unit,direction,endPoint=None,_rangeObj=None):
		if not _rangeObj:
			_rangeObj=self._rangeObj
		if unit in NVDAUnitsToWordUnits:
			unit=NVDAUnitsToWordUnits[unit]
		else:
			raise NotImplementedError("unit: %s"%unit)
		if endPoint=="start":
			moveFunc=_rangeObj.MoveStart
		elif endPoint=="end":
			moveFunc=_rangeObj.MoveEnd
		else:
			moveFunc=_rangeObj.Move
		res=moveFunc(unit,direction)
		#units higher than character and word expand to contain the last text plus the insertion point offset in the document
		#However move from a character before will incorrectly move to this offset which makes move/expand contridictory to each other
		#Make sure that move fails if it lands on the final offset but the unit is bigger than character/word
		if direction>0 and endPoint!="end" and unit not in (wdCharacter,wdWord)  and (_rangeObj.start+1)==self.obj.WinwordDocumentObject.characters.count:
			return 0
		return res

	def move(self,unit,direction,endPoint=None):
		if unit!=textInfos.UNIT_LINE:
			return self._move(unit,direction,endPoint)
		if direction==0 or direction>1 or direction<-1:
			raise NotImplementedError("moving by line is only supported   collapsed and with a count of 1 or -1")
		oldOffset=self._rangeObj.end if endPoint=="end" else self._rangeObj.start
		newOffset=ctypes.c_long()
		# Try moving by line making use of the selection temporarily
		res=NVDAHelper.localLib.nvdaInProcUtils_winword_moveByLine(self.obj.appModule.helperLocalBindingHandle,self.obj.documentWindowHandle,oldOffset,1 if direction<0 else 0,ctypes.byref(newOffset))
		if res==0:
			res=direction
		newOffset=newOffset.value
		if direction<0 and not endPoint and newOffset==oldOffset:
			# Moving backwards by line seemed to not move.
			# Therefore fallback to moving back a character, expanding to line and collapsing to start instead.
			self.move(textInfos.UNIT_CHARACTER,-1)
			self.expand(unit)
			self.collapse()
		elif direction>0 and not endPoint and newOffset<oldOffset:
			# Moving forward by line seems to have wrapped back before the original position
			# This can happen in some tables with merged rows.
			# Try moving forward by cell, but if that fails, jump past the entire table.
			res=self.move(textInfos.UNIT_CELL,direction,endPoint)
			if res==0:
				self.expand(textInfos.UNIT_TABLE)
				self.collapse(end=True)
		else:
			# the move by line using the selection succeeded. Therefore update this TextInfo's position.
			if not endPoint:
				self._rangeObj.setRange(newOffset,newOffset)
			elif endPoint=="start":
				self._rangeObj.start=newOffset
			elif endPoint=="end":
				self._rangeObj.end=newOffset
		return res

	def _get_bookmark(self):
		return textInfos.offsets.Offsets(self._rangeObj.Start,self._rangeObj.End)

	def updateCaret(self):
		self.obj.WinwordWindowObject.ScrollIntoView(self._rangeObj)
		self.obj.WinwordSelectionObject.SetRange(self._rangeObj.Start,self._rangeObj.Start)

	def updateSelection(self):
		self.obj.WinwordWindowObject.ScrollIntoView(self._rangeObj)
		self.obj.WinwordSelectionObject.SetRange(self._rangeObj.Start,self._rangeObj.End)

	def getMathMl(self, field):
		try:
			import mathType
		except:
			raise LookupError("MathType not installed")
		range = self._rangeObj.Duplicate
		range.Start = int(field["shapeoffset"])
		obj = range.InlineShapes[0].OLEFormat
		try:
			return mathType.getMathMl(obj)
		except:
			raise LookupError("Couldn't get MathML from MathType")

class WordDocumentTextInfoForTreeInterceptor(WordDocumentTextInfo):

	def _get_shouldIncludeLayoutTables(self):
		return config.conf['documentFormatting']['includeLayoutTables']

class BrowseModeWordDocumentTextInfo(browseMode.BrowseModeDocumentTextInfo,treeInterceptorHandler.RootProxyTextInfo):

	def __init__(self,obj,position,_rangeObj=None):
		if isinstance(position,WordDocument):
			position=textInfos.POSITION_CARET
		super(BrowseModeWordDocumentTextInfo,self).__init__(obj,position,_rangeObj=_rangeObj)

	InnerTextInfoClass=WordDocumentTextInfoForTreeInterceptor

	def _get_focusableNVDAObjectAtStart(self):
		return self.obj.rootNVDAObject

class WordDocumentTreeInterceptor(browseMode.BrowseModeDocumentTreeInterceptor):

	TextInfo=BrowseModeWordDocumentTextInfo

	def _get_isAlive(self):
		return winUser.isWindow(self.rootNVDAObject.windowHandle)

	def __contains__(self,obj):
		return obj==self.rootNVDAObject

	def _get_ElementsListDialog(self):
		return ElementsListDialog

	def _iterHeadings(self,nodeType,direction,rangeObj,includeCurrent):
		neededLevel=int(nodeType[7:]) if len(nodeType)>7 else 0
		isFirst=True
		while True:
			if not isFirst or includeCurrent:
				level=rangeObj.paragraphs[1].outlineLevel
				if level and 0<level<10 and (not neededLevel or neededLevel==level):
					rangeObj.expand(wdParagraph)
					yield WordDocumentHeadingQuickNavItem(nodeType,self,BrowseModeWordDocumentTextInfo(self,None,_rangeObj=rangeObj),level)
			isFirst=False
			if direction=="next":
				newRangeObj=rangeObj.gotoNext(wdGoToHeading)
				if not newRangeObj or newRangeObj.start<=rangeObj.start:
					break
			elif direction=="previous":
				newRangeObj=rangeObj.gotoPrevious(wdGoToHeading)
				if not newRangeObj or newRangeObj.start>=rangeObj.start:
					break
			rangeObj=newRangeObj

	def _iterNodesByType(self,nodeType,direction="next",pos=None):
		if pos:
			rangeObj=pos.innerTextInfo._rangeObj 
		else:
			rangeObj=self.rootNVDAObject.WinwordDocumentObject.range(0,0)
		includeCurrent=False if pos else True
		if nodeType=="link":
			return LinkWinWordCollectionQuicknavIterator(nodeType,self,direction,rangeObj,includeCurrent).iterate()
		elif nodeType=="annotation":
			comments=CommentWinWordCollectionQuicknavIterator(nodeType,self,direction,rangeObj,includeCurrent).iterate()
			revisions=RevisionWinWordCollectionQuicknavIterator(nodeType,self,direction,rangeObj,includeCurrent).iterate()
			return browseMode.mergeQuickNavItemIterators([comments,revisions],direction)
		elif nodeType in ("table","container"):
			 return TableWinWordCollectionQuicknavIterator(nodeType,self,direction,rangeObj,includeCurrent).iterate()
		elif nodeType=="graphic":
			 return GraphicWinWordCollectionQuicknavIterator(nodeType,self,direction,rangeObj,includeCurrent).iterate()
		elif nodeType=="chart":
			return ChartWinWordCollectionQuicknavIterator(nodeType,self,direction,rangeObj,includeCurrent).iterate()
		elif nodeType.startswith('heading'):
			return self._iterHeadings(nodeType,direction,rangeObj,includeCurrent)
		else:
			raise NotImplementedError

	def _activatePosition(self, info=None):
		if not info:
			info=self.makeTextInfo(textInfos.POSITION_CARET)
		info.activate()

	def script_nextRow(self,gesture):
		self.rootNVDAObject._moveInTable(row=True,forward=True)
		braille.handler.handleCaretMove(self)

	def script_previousRow(self,gesture):
		self.rootNVDAObject._moveInTable(row=True,forward=False)
		braille.handler.handleCaretMove(self)

	def script_nextColumn(self,gesture):
		self.rootNVDAObject._moveInTable(row=False,forward=True)
		braille.handler.handleCaretMove(self)

	def script_previousColumn(self,gesture):
		self.rootNVDAObject._moveInTable(row=False,forward=False)
		braille.handler.handleCaretMove(self)

	__gestures={
		"kb:tab":"trapNonCommandGesture",
		"kb:shift+tab":"trapNonCommandGesture",
		"kb:control+alt+upArrow": "previousRow",
		"kb:control+alt+downArrow": "nextRow",
		"kb:control+alt+leftArrow": "previousColumn",
		"kb:control+alt+rightArrow": "nextColumn",
		# We want to fall back to MS Word's real page up and page down, rather than browseMode's faked 25 lines
		"kb:pageUp":None,
		"kb:pageDown":None,
		"kb:shift+pageUp":None,
		"kb:shift+pageDown":None,
	}

class WordDocument(EditableTextWithoutAutoSelectDetection, Window):

	treeInterceptorClass=WordDocumentTreeInterceptor
	shouldCreateTreeInterceptor=False
	TextInfo=WordDocumentTextInfo

	def _get_ignoreEditorRevisions(self):
		try:
			ignore=not self.WinwordWindowObject.view.showRevisionsAndComments
		except COMError:
			log.debugWarning("showRevisionsAndComments",exc_info=True)
			ignore=False
		self.ignoreEditorRevisions=ignore
		return ignore

	#: True if formatting should be ignored (text only) such as for spellCheck error field
	ignoreFormatting=False

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

	def populateHeaderCellTrackerFromHeaderRows(self,headerCellTracker,table):
		rows=table.rows
		numHeaderRows=0
		for rowIndex in xrange(rows.count): 
			try:
				row=rows.item(rowIndex+1)
			except COMError:
				break
			try:
				headingFormat=row.headingFormat
			except (COMError,AttributeError,NameError):
				headingFormat=0
			if headingFormat==-1: # is a header row
				numHeaderRows+=1
			else:
				break
		if numHeaderRows>0:
			headerCellTracker.addHeaderCellInfo(rowNumber=1,columnNumber=1,rowSpan=numHeaderRows,isColumnHeader=True,isRowHeader=False)

	def populateHeaderCellTrackerFromBookmarks(self,headerCellTracker,bookmarks):
		for x in bookmarks: 
			name=x.name
			lowerName=name.lower()
			isColumnHeader=isRowHeader=False
			if lowerName.startswith('title'):
				isColumnHeader=isRowHeader=True
			elif lowerName.startswith('columntitle'):
				isColumnHeader=True
			elif lowerName.startswith('rowtitle'):
				isRowHeader=True
			else:
				continue
			try:
				headerCell=x.range.cells.item(1)
			except COMError:
				continue
			headerCellTracker.addHeaderCellInfo(rowNumber=headerCell.rowIndex,columnNumber=headerCell.columnIndex,name=name,isColumnHeader=isColumnHeader,isRowHeader=isRowHeader)

	_curHeaderCellTrackerTable=None
	_curHeaderCellTracker=None
	def getHeaderCellTrackerForTable(self,table):
		tableRange=table.range
		if not self._curHeaderCellTrackerTable or not tableRange.isEqual(self._curHeaderCellTrackerTable.range):
			self._curHeaderCellTracker=HeaderCellTracker()
			self.populateHeaderCellTrackerFromBookmarks(self._curHeaderCellTracker,tableRange.bookmarks)
			self.populateHeaderCellTrackerFromHeaderRows(self._curHeaderCellTracker,table)
			self._curHeaderCellTrackerTable=table
		return self._curHeaderCellTracker

	def setAsHeaderCell(self,cell,isColumnHeader=False,isRowHeader=False):
		rowNumber=cell.rowIndex
		columnNumber=cell.columnIndex
		headerCellTracker=self.getHeaderCellTrackerForTable(cell.range.tables[1])
		oldInfo=headerCellTracker.getHeaderCellInfoAt(rowNumber,columnNumber)
		if oldInfo:
			if isColumnHeader and not oldInfo.isColumnHeader:
				oldInfo.isColumnHeader=True
			elif isRowHeader and not oldInfo.isRowHeader:
				oldInfo.isRowHeader=True
			else:
				return False
			isColumnHeader=oldInfo.isColumnHeader
			isRowHeader=oldInfo.isRowHeader
		if isColumnHeader and isRowHeader:
			name="Title_"
		elif isRowHeader:
			name="RowTitle_"
		elif isColumnHeader:
			name="ColumnTitle_"
		else:
			raise ValueError("One or both of isColumnHeader or isRowHeader must be True")
		name+=uuid.uuid4().hex
		if oldInfo:
			self.WinwordDocumentObject.bookmarks[oldInfo.name].delete()
			oldInfo.name=name
		else:
			headerCellTracker.addHeaderCellInfo(rowNumber=rowNumber,columnNumber=columnNumber,name=name,isColumnHeader=isColumnHeader,isRowHeader=isRowHeader)
		self.WinwordDocumentObject.bookmarks.add(name,cell.range)
		return True

	def forgetHeaderCell(self,cell,isColumnHeader=False,isRowHeader=False):
		rowNumber=cell.rowIndex
		columnNumber=cell.columnIndex
		if not isColumnHeader and not isRowHeader: 
			return False
		headerCellTracker=self.getHeaderCellTrackerForTable(cell.range.tables[1])
		info=headerCellTracker.getHeaderCellInfoAt(rowNumber,columnNumber)
		if not info or not hasattr(info,'name'):
			return False
		if isColumnHeader and info.isColumnHeader:
			info.isColumnHeader=False
		elif isRowHeader and info.isRowHeader:
			info.isRowHeader=False
		else:
			return False
		headerCellTracker.removeHeaderCellInfo(info)
		self.WinwordDocumentObject.bookmarks(info.name).delete()
		if info.isColumnHeader or info.isRowHeader:
			self.setAsHeaderCell(cell,isColumnHeader=info.isColumnHeader,isRowHeader=info.isRowHeader)
		return True

	def fetchAssociatedHeaderCellText(self,cell,columnHeader=False):
		table=cell.range.tables[1]
		rowNumber=cell.rowIndex
		columnNumber=cell.columnIndex
		headerCellTracker=self.getHeaderCellTrackerForTable(table)
		for info in headerCellTracker.iterPossibleHeaderCellInfosFor(rowNumber,columnNumber,columnHeader=columnHeader):
			textList=[]
			if columnHeader:
				for headerRowNumber in xrange(info.rowNumber,info.rowNumber+info.rowSpan): 
					headerCell=table.cell(headerRowNumber,columnNumber)
					textList.append(headerCell.range.text)
			else:
				for headerColumnNumber in xrange(info.columnNumber,info.columnNumber+info.colSpan): 
					headerCell=table.cell(rowNumber,headerColumnNumber)
					textList.append(headerCell.range.text)
			text=" ".join(textList)
			if text:
				return text

	def script_setColumnHeader(self,gesture):
		scriptCount=scriptHandler.getLastScriptRepeatCount()
		if not config.conf['documentFormatting']['reportTableHeaders']:
			# Translators: a message reported in the SetColumnHeader script for Microsoft Word.
			ui.message(_("Cannot set headers. Please enable reporting of table headers in Document Formatting Settings"))
			return
		try:
			cell=self.WinwordSelectionObject.cells[1]
		except COMError:
			# Translators: a message when trying to perform an action on a cell when not in one in Microsoft word
			ui.message(_("Not in a table cell"))
			return
		if scriptCount==0:
			if self.setAsHeaderCell(cell,isColumnHeader=True,isRowHeader=False):
				# Translators: a message reported in the SetColumnHeader script for Microsoft Word.
				ui.message(_("Set row {rowNumber} column {columnNumber} as start of column headers").format(rowNumber=cell.rowIndex,columnNumber=cell.columnIndex))
			else:
				# Translators: a message reported in the SetColumnHeader script for Microsoft Word.
				ui.message(_("Already set row {rowNumber} column {columnNumber} as start of column headers").format(rowNumber=cell.rowIndex,columnNumber=cell.columnIndex))
		elif scriptCount==1:
			if self.forgetHeaderCell(cell,isColumnHeader=True,isRowHeader=False):
				# Translators: a message reported in the SetColumnHeader script for Microsoft Word.
				ui.message(_("Removed row {rowNumber} column {columnNumber}  from column headers").format(rowNumber=cell.rowIndex,columnNumber=cell.columnIndex))
			else:
				# Translators: a message reported in the SetColumnHeader script for Microsoft Word.
				ui.message(_("Cannot find row {rowNumber} column {columnNumber}  in column headers").format(rowNumber=cell.rowIndex,columnNumber=cell.columnIndex))
	script_setColumnHeader.__doc__=_("Pressing once will set this cell as the first column header for any cells lower and to the right of it within this table. Pressing twice will forget the current column header for this cell.")

	def script_setRowHeader(self,gesture):
		scriptCount=scriptHandler.getLastScriptRepeatCount()
		if not config.conf['documentFormatting']['reportTableHeaders']:
			# Translators: a message reported in the SetRowHeader script for Microsoft Word.
			ui.message(_("Cannot set headers. Please enable reporting of table headers in Document Formatting Settings"))
			return
		try:
			cell=self.WinwordSelectionObject.cells[1]
		except COMError:
			# Translators: a message when trying to perform an action on a cell when not in one in Microsoft word
			ui.message(_("Not in a table cell"))
			return
		if scriptCount==0:
			if self.setAsHeaderCell(cell,isColumnHeader=False,isRowHeader=True):
				# Translators: a message reported in the SetRowHeader script for Microsoft Word.
				ui.message(_("Set row {rowNumber} column {columnNumber} as start of row headers").format(rowNumber=cell.rowIndex,columnNumber=cell.columnIndex))
			else:
				# Translators: a message reported in the SetRowHeader script for Microsoft Word.
				ui.message(_("Already set row {rowNumber} column {columnNumber} as start of row headers").format(rowNumber=cell.rowIndex,columnNumber=cell.columnIndex))
		elif scriptCount==1:
			if self.forgetHeaderCell(cell,isColumnHeader=False,isRowHeader=True):
				# Translators: a message reported in the SetRowHeader script for Microsoft Word.
				ui.message(_("Removed row {rowNumber} column {columnNumber}  from row headers").format(rowNumber=cell.rowIndex,columnNumber=cell.columnIndex))
			else:
				# Translators: a message reported in the SetRowHeader script for Microsoft Word.
				ui.message(_("Cannot find row {rowNumber} column {columnNumber}  in row headers").format(rowNumber=cell.rowIndex,columnNumber=cell.columnIndex))
	script_setRowHeader.__doc__=_("Pressing once will set this cell as the first row header for any cells lower and to the right of it within this table. Pressing twice will forget the current row header for this cell.")

	def script_reportCurrentHeaders(self,gesture):
		cell=self.WinwordSelectionObject.cells[1]
		rowText=self.fetchAssociatedHeaderCellText(cell,False)
		columnText=self.fetchAssociatedHeaderCellText(cell,True)
		ui.message("Row %s, column %s"%(rowText or "empty",columnText or "empty"))

	def _get_WinwordVersion(self):
		if not hasattr(self,'_WinwordVersion'):
			self._WinwordVersion=float(self.WinwordApplicationObject.version)
		return self._WinwordVersion

	def _get_documentWindowHandle(self):
		return self.windowHandle

	def _get_WinwordWindowObject(self):
		if not getattr(self,'_WinwordWindowObject',None): 
			try:
				pDispatch=oleacc.AccessibleObjectFromWindow(self.documentWindowHandle,winUser.OBJID_NATIVEOM,interface=comtypes.automation.IDispatch)
			except (COMError, WindowsError):
				log.debugWarning("Could not get MS Word object model from window %s with class %s"%(self.documentWindowHandle,winUser.getClassName(self.documentWindowHandle)),exc_info=True)
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

	def _WaitForValueChangeForAction(self,action,fetcher,timeout=0.15):
		oldVal=fetcher()
		action()
		startTime=curTime=time.time()
		curVal=fetcher()
		while curVal==oldVal and (curTime-startTime)<timeout:
			time.sleep(0.01)
			curVal=fetcher()
			curTime=time.time()
		return curVal

	def script_toggleBold(self,gesture):
		val=self._WaitForValueChangeForAction(lambda: gesture.send(),lambda: self.WinwordSelectionObject.font.bold)
		if val:
			# Translators: a message when toggling formatting in Microsoft word
			ui.message(_("Bold on"))
		else:
			# Translators: a message when toggling formatting in Microsoft word
			ui.message(_("Bold off"))

	def script_toggleItalic(self,gesture):
		val=self._WaitForValueChangeForAction(lambda: gesture.send(),lambda: self.WinwordSelectionObject.font.italic)
		if val:
			# Translators: a message when toggling formatting in Microsoft word
			ui.message(_("Italic on"))
		else:
			# Translators: a message when toggling formatting in Microsoft word
			ui.message(_("Italic off"))

	def script_toggleUnderline(self,gesture):
		val=self._WaitForValueChangeForAction(lambda: gesture.send(),lambda: self.WinwordSelectionObject.font.underline)
		if val:
			# Translators: a message when toggling formatting in Microsoft word
			ui.message(_("Underline on"))
		else:
			# Translators: a message when toggling formatting in Microsoft word
			ui.message(_("Underline off"))

	def script_toggleAlignment(self,gesture):
		val=self._WaitForValueChangeForAction(lambda: gesture.send(),lambda: self.WinwordSelectionObject.paragraphFormat.alignment)
		alignmentMessages={
			# Translators: a an alignment in Microsoft Word 
			wdAlignParagraphLeft:_("Left aligned"),
			# Translators: a an alignment in Microsoft Word 
			wdAlignParagraphCenter:_("centered"),
			# Translators: a an alignment in Microsoft Word 
			wdAlignParagraphRight:_("Right aligned"),
			# Translators: a an alignment in Microsoft Word 
			wdAlignParagraphJustify:_("Justified"),
		}
		msg=alignmentMessages.get(val)
		if msg:
			ui.message(msg)

	def script_toggleSuperscriptSubscript(self,gesture):
		val=self._WaitForValueChangeForAction(lambda: gesture.send(),lambda: (self.WinwordSelectionObject.font.superscript,self.WinwordSelectionObject.font.subscript))
		if val[0]:
			# Translators: a message when toggling formatting in Microsoft word
			ui.message(_("Superscript"))
		elif val[1]:
			# Translators: a message when toggling formatting in Microsoft word
			ui.message(_("Subscript"))
		else:
			# Translators: a message when toggling formatting in Microsoft word
			ui.message(_("Baseline"))

	def script_increaseDecreaseOutlineLevel(self,gesture):
		val=self._WaitForValueChangeForAction(lambda: gesture.send(),lambda: self.WinwordSelectionObject.paragraphFormat.outlineLevel)
		style=self.WinwordSelectionObject.style.nameLocal
		# Translators: the message when the outline level / style is changed in Microsoft word
		ui.message(_("{styleName} style, outline level {outlineLevel}").format(styleName=style,outlineLevel=val))

	def script_increaseDecreaseFontSize(self,gesture):
		val=self._WaitForValueChangeForAction(lambda: gesture.send(),lambda: self.WinwordSelectionObject.font.size)
		# Translators: a message when increasing or decreasing font size in Microsoft Word
		ui.message(_("{size:g} point font").format(size=val))

	def script_caret_moveByCell(self,gesture):
		gesture.send()
		info=self.makeTextInfo(textInfos.POSITION_SELECTION)
		inTable=info._rangeObj.tables.count>0
		isCollapsed=info.isCollapsed
		if inTable:
			info.expand(textInfos.UNIT_CELL)
			speech.speakTextInfo(info,reason=controlTypes.REASON_FOCUS)
			braille.handler.handleCaretMove(self)

	def script_tab(self,gesture):
		gesture.send()
		info=self.makeTextInfo(textInfos.POSITION_SELECTION)
		inTable=info._rangeObj.tables.count>0
		isCollapsed=info.isCollapsed
		if inTable and isCollapsed:
			info.expand(textInfos.UNIT_CELL)
			isCollapsed=False
		if not isCollapsed:
			speech.speakTextInfo(info,reason=controlTypes.REASON_FOCUS)
		braille.handler.handleCaretMove(self)
		if isCollapsed:
			offset=info._rangeObj.information(wdHorizontalPositionRelativeToPage)
			msg=self.getLocalizedMeasurementTextForPointSize(offset)
			ui.message(msg)
			if info._rangeObj.paragraphs[1].range.start==info._rangeObj.start:
				info.expand(textInfos.UNIT_LINE)
				speech.speakTextInfo(info,unit=textInfos.UNIT_LINE,reason=controlTypes.REASON_CARET)

	def getLocalizedMeasurementTextForPointSize(self,offset):
		options=self.WinwordApplicationObject.options
		useCharacterUnit=options.useCharacterUnit
		if useCharacterUnit:
			offset=offset/self.WinwordSelectionObject.font.size
			# Translators: a measurement in Microsoft Word
			return _("{offset:.3g} characters").format(offset=offset)
		else:
			unit=options.measurementUnit
			if unit==wdInches:
				offset=offset/72.0
				# Translators: a measurement in Microsoft Word
				return _("{offset:.3g} inches").format(offset=offset)
			elif unit==wdCentimeters:
				offset=offset/28.35
				# Translators: a measurement in Microsoft Word
				return _("{offset:.3g} centimeters").format(offset=offset)
			elif unit==wdMillimeters:
				offset=offset/2.835
				# Translators: a measurement in Microsoft Word
				return _("{offset:.3g} millimeters").format(offset=offset)
			elif unit==wdPoints:
				# Translators: a measurement in Microsoft Word
				return _("{offset:.3g} points").format(offset=offset)
			elif unit==wdPicas:
				offset=offset/12.0
				# Translators: a measurement in Microsoft Word
				# See http://support.microsoft.com/kb/76388 for details.
				return _("{offset:.3g} picas").format(offset=offset)

	def script_reportCurrentComment(self,gesture):
		info=self.makeTextInfo(textInfos.POSITION_CARET)
		info.expand(textInfos.UNIT_CHARACTER)
		fields=info.getTextWithFields(formatConfig={'reportComments':True})
		for field in reversed(fields):
			if isinstance(field,textInfos.FieldCommand) and isinstance(field.field,textInfos.FormatField): 
				commentReference=field.field.get('comment')
				if commentReference:
					offset=int(commentReference)
					range=self.WinwordDocumentObject.range(offset,offset+1)
					try:
						text=range.comments[1].range.text
					except COMError:
						break
					if text:
						ui.message(text)
						return
		# Translators: a message when there is no comment to report in Microsoft Word
		ui.message(_("No comments"))
	# Translators: a description for a script
	script_reportCurrentComment.__doc__=_("Reports the text of the comment where the System caret is located.")

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
		try:
			table=info._rangeObj.tables[1]
		except COMError:
			log.debugWarning("Could not get MS Word table object indicated in XML")
			ui.message(_("Not in table"))
			return False
		_cell=table.cell
		getCell=lambda thisIndex,otherIndex: _cell(thisIndex,otherIndex) if row else _cell(otherIndex,thisIndex)
		thisIndex=rowNumber if row else columnNumber
		otherIndex=columnNumber if row else rowNumber
		thisLimit=(rowCount if row else columnCount) if forward else 1
		limitOp=operator.le if forward else operator.ge
		incdecFunc=operator.add if forward else operator.sub
		foundCell=None
		curOtherIndex=otherIndex
		while curOtherIndex>0:
			curThisIndex=incdecFunc(thisIndex,1)
			while limitOp(curThisIndex,thisLimit):
				try:
					foundCell=getCell(curThisIndex,curOtherIndex).range
				except COMError:
					pass
				if foundCell: break
				curThisIndex=incdecFunc(curThisIndex,1)
			if foundCell: break
			curOtherIndex-=1
		if not foundCell:
			ui.message(_("Edge of table"))
			return False
		newInfo=WordDocumentTextInfo(self,textInfos.POSITION_CARET,_rangeObj=foundCell)
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

	def script_nextParagraph(self,gesture):
		info=self.makeTextInfo(textInfos.POSITION_CARET)
		# #4375: can't use self.move here as it may check document.chracters.count which can take for ever on large documents.
		info._rangeObj.move(wdParagraph,1)
		info.updateCaret()
		self._caretScriptPostMovedHelper(textInfos.UNIT_PARAGRAPH,gesture,None)
	script_nextParagraph.resumeSayAllMode=sayAllHandler.CURSOR_CARET

	def script_previousParagraph(self,gesture):
		info=self.makeTextInfo(textInfos.POSITION_CARET)
		# #4375: keeping cemetrical with nextParagraph script. 
		info._rangeObj.move(wdParagraph,-1)
		info.updateCaret()
		self._caretScriptPostMovedHelper(textInfos.UNIT_PARAGRAPH,gesture,None)
	script_previousParagraph.resumeSayAllMode=sayAllHandler.CURSOR_CARET

	__gestures = {
		"kb:control+[":"increaseDecreaseFontSize",
		"kb:control+]":"increaseDecreaseFontSize",
		"kb:control+shift+,":"increaseDecreaseFontSize",
		"kb:control+shift+.":"increaseDecreaseFontSize",
		"kb:control+b":"toggleBold",
		"kb:control+i":"toggleItalic",
		"kb:control+u":"toggleUnderline",
		"kb:control+=":"toggleSuperscriptSubscript",
		"kb:control+shift+=":"toggleSuperscriptSubscript",
		"kb:control+l":"toggleAlignment",
		"kb:control+e":"toggleAlignment",
		"kb:control+r":"toggleAlignment",
		"kb:control+j":"toggleAlignment",
		"kb:alt+shift+rightArrow":"increaseDecreaseOutlineLevel",
		"kb:alt+shift+leftArrow":"increaseDecreaseOutlineLevel",
		"kb:control+shift+n":"increaseDecreaseOutlineLevel",
		"kb:control+alt+1":"increaseDecreaseOutlineLevel",
		"kb:control+alt+2":"increaseDecreaseOutlineLevel",
		"kb:control+alt+3":"increaseDecreaseOutlineLevel",
		"kb:tab": "tab",
		"kb:shift+tab": "tab",
		"kb:NVDA+shift+c":"setColumnHeader",
		"kb:NVDA+shift+r":"setRowHeader",
		"kb:NVDA+shift+h":"reportCurrentHeaders",
		"kb:control+alt+upArrow": "previousRow",
		"kb:control+alt+downArrow": "nextRow",
		"kb:control+alt+leftArrow": "previousColumn",
		"kb:control+alt+rightArrow": "nextColumn",
		"kb:control+downArrow":"nextParagraph",
		"kb:control+upArrow":"previousParagraph",
		"kb:alt+home":"caret_moveByCell",
		"kb:alt+end":"caret_moveByCell",
		"kb:alt+pageUp":"caret_moveByCell",
		"kb:alt+pageDown":"caret_moveByCell",
		"kb:alt+shift+home":"caret_changeSelection",
		"kb:alt+shift+end":"caret_changeSelection",
		"kb:alt+shift+pageUp":"caret_changeSelection",
		"kb:alt+shift+pageDown":"caret_changeSelection",
		"kb:control+pageUp": "caret_moveByLine",
		"kb:control+pageDown": "caret_moveByLine",
		"kb:NVDA+alt+c":"reportCurrentComment",
	}

class WordDocument_WwN(WordDocument):

	def _get_documentWindowHandle(self):
		w=NVDAHelper.localLib.findWindowWithClassInThread(self.windowThreadID,u"_WwG",True)
		if not w:
			log.debugWarning("Could not find window for class _WwG in thread.")
			w=super(WordDocument_WwN,self).documentWindowHandle
		return w

	def _get_WinwordWindowObject(self):
		window=super(WordDocument_WwN,self).WinwordWindowObject
		if not window: return None
		try:
			return window.application.activeWindow.activePane
		except COMError:
			log.debugWarning("Unable to get activePane")
			return window.application.windows[1].activePane

	__gestures={
		"kb:tab":None,
		"kb:shift+tab":None,
	}

class WordChart(Window):

	role=controlTypes.ROLE_CHART

	def __init__(self,windowHandle, wordApplicationObject, wordShapeObject,keyIndex=0):
		self.windowHandle=windowHandle
		self.wordApplicationObject=wordApplicationObject
		self.wordShapeObject=wordShapeObject
		self.wordChartObject=wordShapeObject.Chart
		self.currentSeriesIndex=0
		self.keyIndex=keyIndex
		self.chartElements={}
		self.keyList=[]
		try:
			seriesCount=self.wordChartObject.SeriesCollection().Count
		except:
			seriesCount=None
		if seriesCount:
			for i in xrange(seriesCount):
				key='series'+str(i+1)
				self.chartElements[key]=(self.focusChartSeries,i+1)
				self.keyList.append(key)
				try:
					trendlinesCount = self.wordChartObject.SeriesCollection(i+1).Trendlines().Count
				except:
					trendlinesCount = None
				if trendlinesCount>=1:
					key=key+"Trendline"
					self.chartElements[key]=(self.focusSeriesTrendline,i+1)
					self.keyList.append(key)
		self.chartElements['otherElements']=(self.focusChartElements, None)
		self.keyList.append('otherElements')
		self.elementsCount=len(self.keyList)
		self.wordShapeObject.Chart.Select()
		super(WordChart,self).__init__(windowHandle=windowHandle)

	def focusSeriesTrendline(self, seriesIndex):
		obj=WordChartSeriesTrendline(windowHandle=self.windowHandle, wordApplicationObject=self.wordApplicationObject, wordShapeObject=self.wordShapeObject, keyIndex=self.keyIndex, seriesIndex=seriesIndex)
		eventHandler.queueEvent('gainFocus',obj)

	def focusChartSeries(self, seriesIndex):
		self.currentSeriesIndex=seriesIndex
		obj=WordChartSeries(windowHandle=self.windowHandle, wordApplicationObject=self.wordApplicationObject, wordShapeObject=self.wordShapeObject, keyIndex=self.keyIndex, seriesIndex=self.currentSeriesIndex)
		self.wordChartObject.SeriesCollection(self.currentSeriesIndex).Select()
		eventHandler.queueEvent('gainFocus',obj)

	def focusChartElements(self):
		obj=WordChartElement(windowHandle=self.windowHandle, wordApplicationObject=self.wordApplicationObject, wordShapeObject=self.wordShapeObject, keyIndex=self.keyIndex)
		eventHandler.queueEvent('gainFocus',obj)

	def _get_name(self):
		if self.wordChartObject.HasTitle:
			name=self.wordChartObject.ChartTitle.Text
		else:
			name=self.wordChartObject.Name
		#find the type of the chart
		chartType = self.wordChartObject.ChartType
		chartTypeText = _msOfficeChartConstants.chartTypeDict.get(chartType,
                # Translators: Reported when the type of a chart is not known.
                                _("unknown"))
		# Translators: Message reporting the title and type of a chart.
		text=_("Chart title: {chartTitle}, type: {chartType}").format(chartTitle=name, chartType=chartTypeText)
		return text

	def _get_description(self):
		count = self.wordChartObject.SeriesCollection().count
		text=""
		if count>0:
			if count == 1:
				# Translators: Indicates that there is 1 series in a chart.
				seriesValueString = _( "There is 1 series in this chart" )
			else:
				# Translators: Indicates the number of series in a chart where there are multiple series.
				seriesValueString = _( "There are total %d series in this chart" ) %(count)
				for i in xrange(1, count+1):
					# Translators: Specifies the number and name of a series when listing series in a chart.
					seriesValueString += ", " + _("series {number} {name}").format(number=i, name=self.wordChartObject.SeriesCollection(i).Name)
				text += seriesValueString
		else:
			# Translators: Indicates that there are no series in a chart.
			text +=_("No Series defined.")
		return text

	def getChartSegment(self):
		chartType = self.wordChartObject.ChartType
		if chartType in (_msOfficeChartConstants.xl3DPie, _msOfficeChartConstants.xl3DPieExploded, _msOfficeChartConstants.xlPie, _msOfficeChartConstants.xlPieExploded, _msOfficeChartConstants.xlPieOfPie):
			# Translators: A slice in a pie chart.
			text=_("slice")
		elif chartType in (_msOfficeChartConstants.xl3DColumn, _msOfficeChartConstants.xl3DColumnClustered, _msOfficeChartConstants.xl3DColumnStacked, _msOfficeChartConstants.xl3DColumnStacked100, _msOfficeChartConstants.xlColumnClustered, _msOfficeChartConstants.xlColumnStacked100, _msOfficeChartConstants.xlColumnStacked):
			# Translators: A column in a column chart.
			text=pgettext('chart','column')
		elif chartType in (_msOfficeChartConstants.xl3DLine, _msOfficeChartConstants.xlLine, _msOfficeChartConstants.xlLineMarkers, _msOfficeChartConstants.xlLineMarkersStacked, _msOfficeChartConstants.xlLineMarkersStacked100, _msOfficeChartConstants.xlLineStacked, _msOfficeChartConstants.xlLineStacked100):
			# Translators: A data point in a line chart.
			text=_("data point")
		else:
			# Translators: A segment of a chart for charts which don't have a specific name for segments.
			text=_("item")
		return text

	def invokeChartElement(self, keyIndex):
		val=self.chartElements[self.keyList[keyIndex]]
		func=val[0]
		arg=val[1]
		if arg==None:
			func()
		else:
			func(arg)
		
	def script_nextChartElement(self,gesture):
		if self.keyIndex == self.elementsCount-1:
			self.keyIndex=0
		else:
			self.keyIndex=self.keyIndex+1
		self.invokeChartElement(self.keyIndex)
	script_nextChartElement.canPropagate=True

	def script_previousChartElement(self,gesture):
		if self.keyIndex == 0:
			self.keyIndex=self.elementsCount-1
		else:
			self.keyIndex=self.keyIndex-1
		self.invokeChartElement(self.keyIndex)
	script_previousChartElement.canPropagate=True

	def script_activatePosition(self,gesture):
		# Toggle browse mode pass-through.
		self.passThrough = True
		self.ignoreTreeInterceptorPassThrough=False
		browseMode.reportPassThrough(self)
	# Translators: Input help mode message for toggle focus and browse mode command in web browsing and other situations.
	script_activatePosition.__doc__=_("Toggles between browse mode and focus mode. When in focus mode, keys will pass straight through to the application, allowing you to interact directly with a control. When in browse mode, you can navigate the document with the cursor, quick navigation keys, etc.")
	script_activatePosition.category=inputCore.SCRCAT_BROWSEMODE

	def script_disablePassThrough(self, gesture):
		rangeStart=self.wordShapeObject.Range.Start
		self.wordApplicationObject.ActiveDocument.Range(rangeStart, rangeStart).Select()
		eventHandler.executeEvent("gainFocus", api.getDesktopObject().objectWithFocus())

	__gestures = {
				"kb:upArrow":"nextChartElement",
				"kb:downArrow":"previousChartElement",
				"kb:leftArrow":"previousChartElement",
				"kb:rightarrow":"nextChartElement",
				"kb:enter": "activatePosition",
				"kb(desktop):numpadEnter":"activatePosition",
				"kb:space": "activatePosition",
				"kb:escape": "disablePassThrough",
	}

class WordChartSeriesTrendline(WordChart):

	role=controlTypes.ROLE_CHARTELEMENT
	_trendlineTypeMap = {
								# Translators: Indicates that trendline type is Exponential
								_msOfficeChartConstants.xlExponential: _("Exponential"),
								# Translators: Indicates that trendline type is Linear
								_msOfficeChartConstants.xlLinear: _("Linear"),
								# Translators: Indicates that trendline type is Logarithmic
								_msOfficeChartConstants.xlLogarithmic: _("Logarithmic"),
								# Translators: Indicates that trendline type is Moving Average
								_msOfficeChartConstants.xlMovingAvg: _("Moving Average"),
								# Translators: Indicates that trendline type is Polynomial
								_msOfficeChartConstants.xlPolynomial: _("Polynomial"),
								# Translators: Indicates that trendline type is Power
								_msOfficeChartConstants.xlPower: _("Power") 
	}

	def __init__(self, windowHandle, wordApplicationObject, wordShapeObject, keyIndex, seriesIndex, trendlineIndex=1):
		self.windowHandle=windowHandle
		self.wordApplicationObject=wordApplicationObject
		self.seriesIndex=seriesIndex
		self.trendlineIndex=trendlineIndex
		self.wordChartObject=wordShapeObject.Chart
		self.trendlinesCount=self.currentSeries.Trendlines().Count
		self.currentTrendline=self.currentSeries.Trendlines(self.trendlineIndex)
		super(WordChartSeriesTrendline, self).__init__(windowHandle=windowHandle, wordApplicationObject=wordApplicationObject, wordShapeObject=wordShapeObject, keyIndex=keyIndex)

	def _get_name(self):
		if self.currentTrendline.DisplayEquation or self.currentTrendline.DisplayRSquared:
			label=self.currentTrendline.DataLabel.Text
			#Translators: Substitute superscript two by square for R square value
			label=label.replace(u"²", _( " square " ))
			label=re.sub(r'([a-zA-Z]+)([2])',r'\1 square', label)
			label=re.sub(r'([a-zA-Z]+)([3])',r'\1 cube', label)
			label=re.sub(r'([a-zA-Z]+)([-]*[04-9][0-9]*)',r'\1 to the power \2', label)
			#Translators: Substitute - by minus in trendline equations.
			label=label.replace(u"-",_(" minus "))
			# Translators: This message gives trendline type and name for selected series
			output=_("{seriesName} trendline type: {trendlineType}, name: {trendlineName}, label: {trendlineLabel} ").format(seriesName=self.wordChartObject.SeriesCollection(self.seriesIndex).Name, trendlineType=self._trendlineTypeMap[self.currentTrendline.Type], trendlineName=self.currentTrendline.Name, trendlineLabel=label)
		else:
			# Translators: This message gives trendline type and name for selected series
			output=_("{seriesName} trendline type: {trendlineType}, name: {trendlineName} ").format(seriesName=self.wordChartObject.SeriesCollection(self.seriesIndex).Name, trendlineType=self._trendlineTypeMap[self.currentTrendline.Type], trendlineName=self.currentTrendline.Name)
		return output

	def invokeTrendline(self, trendlineIndex):
		obj=WordChartSeriesTrendline(windowHandle=self.windowHandle, wordApplicationObject=self.wordApplicationObject, wordShapeObject=self.wordShapeObject, keyIndex=self.keyIndex, seriesIndex=self.seriesIndex, trendlineIndex=trendlineIndex)
		self.currentTrendline.Select()
		eventHandler.queueEvent('gainFocus',obj)

	def script_previousTrendline(self, gesture):
		if self.trendlinesCount > 1:
			if self.trendlineIndex==1:
				self.trendlineIndex=self.trendlinesCount
			else:
				self.trendlineIndex=self.trendlineIndex-1
			self.invokeTrendline(self.trendlineIndex)

	def script_nextTrendline(self, gesture):
		if self.trendlinesCount > 1:
			if self.trendlineIndex==self.trendlinesCount:
				self.trendlineIndex=1
			else:
				self.trendlineIndex=self.trendlineIndex+1
			self.invokeTrendline(self.trendlineIndex)

	__gestures = {
				"kb:leftArrow":"previousTrendline",
				"kb:rightArrow":"nextTrendline",
	}

class WordChartElement(WordChart):

	role=controlTypes.ROLE_CHARTELEMENT
	_axisMap={
				_msOfficeChartConstants.xlCategory: {
													# Translators: Indicates Primary Category Axis
													_msOfficeChartConstants.xlPrimary: _("Primary Category Axis"),
													# Translators: Indicates Secondary Category Axis
													_msOfficeChartConstants.xlSecondary: _("Secondary Category Axis")},
				_msOfficeChartConstants.xlValue: {
													# Translators: Indicates Primary Value Axis
													_msOfficeChartConstants.xlPrimary: _("Primary Value Axis"),
													# Translators: Indicates Secondary Value Axis
													_msOfficeChartConstants.xlSecondary: _("Secondary Value Axis")},
				_msOfficeChartConstants.xlSeriesAxis: {
													# Translators: Indicates Primary Series Axis
													_msOfficeChartConstants.xlPrimary: _("Primary Series Axis"),
													# Translators: Indicates Secondary Series Axis
													_msOfficeChartConstants.xlSecondary: _("Secondary Series Axis")}
	}

	def __init__(self,windowHandle, wordApplicationObject, wordShapeObject, keyIndex, elementIndex=0):
		self.windowHandle=windowHandle
		self.wordApplicationObject=wordApplicationObject
		self.elementIndex=elementIndex
		self.keyIndex=keyIndex
		self.wordShapeObject=wordShapeObject
		self.wordChartObject=wordShapeObject.Chart
		self.elementKeyList=[]
		if self.wordChartObject.HasTitle:
			self.elementKeyList.append('chartTitle')
		# Enumerations for chart object in Excel and Word are same
		for axisType in [_msOfficeChartConstants.xlCategory, _msOfficeChartConstants.xlValue, _msOfficeChartConstants.xlSeriesAxis]:
			for axisGroup in [_msOfficeChartConstants.xlPrimary, _msOfficeChartConstants.xlSecondary]:
				if self.wordChartObject.HasAxis(axisType, axisGroup):
					self.elementKeyList.append(self._axisMap[axisType][axisGroup])
					if self.wordChartObject.Axes(axisType, axisGroup).HasTitle:
						self.elementKeyList.append(self._axisMap[axisType][axisGroup]+' Title')
		self.elementKeyList.append('chartArea')
		
		self.elementKeyList.append('plotArea')

		if self.wordChartObject.HasLegend:
			self.elementKeyList.append('legend')

		if self.wordChartObject.HasDataTable:
			self.elementKeyList.append('dataTable')

		self.chartElementsCount=len(self.elementKeyList)
		super(WordChartElement,self).__init__(windowHandle=windowHandle, wordApplicationObject=wordApplicationObject, wordShapeObject=wordShapeObject, keyIndex=keyIndex)

	def _get_name(self):
		#Translators: Speak text chart elements when virtual row of chart elements is reached while navigation
		return _("Chart Elements")

	def focusChartElement(self, key):
		if 'Axis' in key:
			splitKey=key.split()
			if splitKey[0]=='Primary':
				axisGroup=_msOfficeChartConstants.xlPrimary
			elif splitKey[0]=='Secondary':
				axisGroup=_msOfficeChartConstants.xlSecondary
			if splitKey[1]=='Category':
				axisType=_msOfficeChartConstants.xlCategory
			elif splitKey[1]=='Value':
				axisType=_msOfficeChartConstants.xlValue
			elif splitKey[1]=='Series':
				axisType=_msOfficeChartConstants.xlSeriesAxis
			if 'Axis Title' in key:
				obj=WordChartAxisTitle(windowHandle=self.windowHandle, wordApplicationObject=self.wordApplicationObject, wordShapeObject=self.wordShapeObject, axisType=axisType, axisGroup=axisGroup, keyIndex=self.keyIndex, elementIndex=self.elementIndex)
				self.wordChartObject.Axes(axisType, axisGroup).AxisTitle.Select()
			else:
				obj=WordChartAxis(windowHandle=self.windowHandle, wordApplicationObject=self.wordApplicationObject, wordShapeObject=self.wordShapeObject, axisType=axisType, axisGroup=axisGroup, keyIndex=self.keyIndex, elementIndex=self.elementIndex)
				self.wordChartObject.Axes(axisType, axisGroup).Select()
		elif key=='chartTitle':
			obj=WordChartTitle(windowHandle=self.windowHandle, wordApplicationObject=self.wordApplicationObject, wordShapeObject=self.wordShapeObject, keyIndex=self.keyIndex, elementIndex=self.elementIndex)
			self.wordChartObject.ChartTitle.Select()
		elif key=='chartArea':
			obj=WordChartArea(windowHandle=self.windowHandle, wordApplicationObject=self.wordApplicationObject, wordShapeObject=self.wordShapeObject,  keyIndex=self.keyIndex, elementIndex=self.elementIndex)
			self.wordChartObject.ChartArea.Select()
		elif key=='plotArea':
			obj=WordChartPlotArea(windowHandle=self.windowHandle, wordApplicationObject=self.wordApplicationObject, wordShapeObject=self.wordShapeObject,  keyIndex=self.keyIndex, elementIndex=self.elementIndex)
			self.wordChartObject.PlotArea.Select()
		elif key=='legend':
			obj=WordChartLegend(windowHandle=self.windowHandle, wordApplicationObject=self.wordApplicationObject, wordShapeObject=self.wordShapeObject,  keyIndex=self.keyIndex, elementIndex=self.elementIndex)
			self.wordChartObject.Legend.Select()
		elif key=='dataTable':
			obj=WordChartDataTable(windowHandle=self.windowHandle, wordApplicationObject=self.wordApplicationObject, wordShapeObject=self.wordShapeObject, keyIndex=self.keyIndex, elementIndex=self.elementIndex)
			self.wordChartObject.DataTable.Select()
		eventHandler.queueEvent('gainFocus',obj)

	def script_previousElement(self,gesture):
		if self.elementIndex == 0:
			self.elementIndex=self.chartElementsCount-1
		else:
			self.elementIndex=self.elementIndex-1
		key=self.elementKeyList[self.elementIndex]
		self.focusChartElement(key)
	script_previousElement.canPropagate=True

	def script_nextElement(self,gesture):
		if self.elementIndex == self.chartElementsCount-1:
			self.elementIndex=0
		else:
			self.elementIndex=self.elementIndex+1
		key=self.elementKeyList[self.elementIndex]
		self.focusChartElement(key)
	script_nextElement.canPropagate=True

	__gestures = {
				"kb:leftArrow":"previousElement",
				"kb:rightArrow":"nextElement",
	}

class WordChartDataTable(WordChartElement):
	def __init__(self,windowHandle, wordApplicationObject, wordShapeObject, keyIndex, elementIndex):
		super(WordChartDataTable,self).__init__(windowHandle=windowHandle, wordApplicationObject=wordApplicationObject, wordShapeObject=wordShapeObject, keyIndex=keyIndex, elementIndex=elementIndex)

	def _get_name(self):
		#Translators: Data Table will be spoken when chart element Data Table is selected
		return _("Data Table")

class WordChartLegend(WordChartElement):
	def __init__(self,windowHandle, wordApplicationObject, wordShapeObject, keyIndex, elementIndex):
		self.chartLegend=wordShapeObject.Chart.Legend
		super(WordChartLegend,self).__init__(windowHandle=windowHandle, wordApplicationObject=wordApplicationObject, wordShapeObject=wordShapeObject, keyIndex=keyIndex, elementIndex=elementIndex)

	def _get_name(self):
		return self.chartLegend.Name

class WordChartArea(WordChartElement):
	def __init__(self,windowHandle, wordApplicationObject, wordShapeObject, keyIndex, elementIndex):
		super(WordChartArea,self).__init__(windowHandle=windowHandle, wordApplicationObject=wordApplicationObject, wordShapeObject=wordShapeObject, keyIndex=keyIndex, elementIndex=elementIndex)

	def _get_name(self):
		#Translators: Chart area will be spoken when chart element chart area is selected
		return _( "Chart area, height: {chartAreaHeight} points, width: {chartAreaWidth} points, top: {chartAreaTop} points, left: {chartAreaLeft} points").format ( chartAreaHeight = self.wordChartObject.ChartArea.Height , chartAreaWidth = self.wordChartObject.ChartArea.Width , chartAreaTop = self.wordChartObject.ChartArea.Top , chartAreaLeft = self.wordChartObject.ChartArea.Left)

class WordChartPlotArea(WordChartElement):
	def __init__(self,windowHandle, wordApplicationObject, wordShapeObject, keyIndex, elementIndex):
		super(WordChartPlotArea,self).__init__(windowHandle=windowHandle, wordApplicationObject=wordApplicationObject, wordShapeObject=wordShapeObject, keyIndex=keyIndex, elementIndex=elementIndex)

	def _get_name(self):
		#Translators: Plot area will be spoken when chart element chart area is selected
		return _( "Plot area, inside height: {plotAreaInsideHeight:.0f} points, inside width: {plotAreaInsideWidth:.0f} points, inside top: {plotAreaInsideTop:.0f} points, inside left: {plotAreaInsideLeft:.0f} points").format ( plotAreaInsideHeight = self.wordChartObject.PlotArea.InsideHeight , plotAreaInsideWidth = self.wordChartObject.PlotArea.InsideWidth , plotAreaInsideTop = self.wordChartObject.PlotArea.InsideTop , plotAreaInsideLeft = self.wordChartObject.PlotArea.InsideLeft )

class WordChartTitle(WordChartElement):
	def __init__(self,windowHandle, wordApplicationObject, wordShapeObject, keyIndex, elementIndex):
		self.chartTitle=wordShapeObject.Chart.ChartTitle.Text
		super(WordChartTitle,self).__init__(windowHandle=windowHandle, wordApplicationObject=wordApplicationObject, wordShapeObject=wordShapeObject, keyIndex=keyIndex, elementIndex=elementIndex)

	def _get_name(self):
		# Translators: Message reporting the chart title
		text= _("Chart title: {chartTitle}").format(chartTitle=self.chartTitle)
		return text

class WordChartAxis(WordChartElement):
	def __init__(self,windowHandle, wordApplicationObject, wordShapeObject, axisType, axisGroup, keyIndex, elementIndex):
		self.wordChartObject=wordShapeObject.Chart
		self.axisType=axisType
		self.axisGroup=axisGroup
		super(WordChartAxis,self).__init__(windowHandle=windowHandle, wordApplicationObject=wordApplicationObject, wordShapeObject=wordShapeObject, keyIndex=keyIndex, elementIndex=elementIndex)

	def _get_name(self):
		return self._axisMap[self.axisType][self.axisGroup]

class WordChartAxisTitle(WordChartElement):

	role=controlTypes.ROLE_CHARTELEMENT

	def __init__(self,windowHandle, wordApplicationObject, wordShapeObject, axisType, axisGroup, keyIndex, elementIndex):
		self.wordChartObject=wordShapeObject.Chart
		self.axisType=axisType
		self.axisGroup=axisGroup
		super(WordChartAxisTitle,self).__init__(windowHandle=windowHandle, wordApplicationObject=wordApplicationObject, wordShapeObject=wordShapeObject, keyIndex=keyIndex, elementIndex=elementIndex)

	def _get_name(self):
		# Translators: Message reporting axis name and axis title
		text= _("{axisName} title: {axisTitle}").format(axisName=self._axisMap[self.axisType][self.axisGroup], axisTitle=self.wordChartObject.Axes(self.axisType, self.axisGroup).AxisTitle.Text)
		return text

class WordChartSeries(WordChart):
	def __init__(self,windowHandle, wordApplicationObject, wordShapeObject, keyIndex, seriesIndex, pointIndex=0):
		self.seriesIndex=seriesIndex
		self.currentPointIndex=pointIndex
		self.wordShapeObject=wordShapeObject
		self.keyIndex=keyIndex
		self.seriesCount=wordShapeObject.Chart.SeriesCollection().Count
		self.currentSeries=wordShapeObject.Chart.SeriesCollection(self.seriesIndex)
		self.pointsCollection=self.currentSeries.Points()
		self.pointsCount=self.pointsCollection.Count
		super(WordChartSeries,self).__init__(windowHandle=windowHandle, wordApplicationObject=wordApplicationObject, wordShapeObject=wordShapeObject, keyIndex=keyIndex)

	def _get_name(self):
		# Translators: Details about a series in a chart. For example, this might report "foo series 1 of 2"
		seriesText=_("{seriesName} series {seriesIndex} of {seriesCount}").format( seriesName = self.currentSeries.Name , seriesIndex = self.seriesIndex , seriesCount = self.seriesCount )
		return seriesText

	def getPointIndex(self, direction):
		if self.pointsCount > 1:
			if direction=="previous":
				if self.currentPointIndex==1:
					self.currentPointIndex=self.pointsCount
				else:
					self.currentPointIndex=self.currentPointIndex-1
			elif direction=="next":
				if self.currentPointIndex==self.pointsCount:
					self.currentPointIndex=1
				else:
					self.currentPointIndex=self.currentPointIndex+1
		return self.currentPointIndex

	def invokePoint(self, pointIndex):
		point=WordChartPoint(windowHandle=self.windowHandle, wordApplicationObject=self.wordApplicationObject, wordShapeObject=self.wordShapeObject, keyIndex=self.keyIndex, seriesIndex=self.seriesIndex, pointIndex=pointIndex)
		self.currentSeries.Points(pointIndex).Select()
		eventHandler.queueEvent("gainFocus", point )
		
	def script_previousPoint(self,gesture):
		self.currentPointIndex=self.getPointIndex("previous")
		self.invokePoint(self.currentPointIndex)
	script_previousPoint.canPropagate=True

	def script_nextPoint(self,gesture):
		self.currentPointIndex=self.getPointIndex("next")
		self.invokePoint(self.currentPointIndex)
	script_nextPoint.canPropagate=True

	def script_reportColor(self, gesture):
		if self.wordChartObject.ChartType in (_msOfficeChartConstants.xlPie, _msOfficeChartConstants.xlPieExploded, _msOfficeChartConstants.xlPieOfPie):
			#Translators: Message to be spoken to report Slice Color in Pie Chart
			ui.message ( _( "Slice color: {colorName} ").format(colorName=colors.RGB.fromCOLORREF(int( self.currentSeries.Points(self.currentPointIndex).Format.Fill.ForeColor.RGB) ).name  ) )
		else:
			#Translators: Message to be spoken to report Series Color
			ui.message ( _( "Series color: {colorName} ").format(colorName=colors.RGB.fromCOLORREF(int( self.currentSeries.Interior.Color ) ).name  ) )

	__gestures = {
				"kb(laptop):leftArrow":"previousPoint",
				"kb(desktop):leftArrow":"previousPoint",
				"kb(laptop):rightArrow":"nextPoint",
				"kb(desktop):rightArrow":"nextPoint",
				"kb:NVDA+5": "reportColor",
	}

class WordChartPoint(WordChartSeries):

	role=controlTypes.ROLE_CHARTELEMENT

	def __init__(self, windowHandle, wordApplicationObject, wordShapeObject, keyIndex, seriesIndex, pointIndex):
		self.pointIndex=pointIndex
		self.seriesIndex=seriesIndex
		self.currentSeries=self.wordChartObject.SeriesCollection(self.seriesIndex)
		super(WordChartPoint,self).__init__(windowHandle=windowHandle, wordApplicationObject=wordApplicationObject, wordShapeObject=wordShapeObject, keyIndex=keyIndex, seriesIndex=seriesIndex, pointIndex=pointIndex)

	def _get_name(self):
		count=self.currentSeries.Points().Count
		if isinstance( self.currentSeries.XValues[self.pointIndex-1] , float):
			excelSeriesXValue = int(self.currentSeries.XValues[self.pointIndex-1] )
		else:
			excelSeriesXValue = self.currentSeries.XValues[self.pointIndex-1]
		output=""
		if self.wordChartObject.ChartType in (_msOfficeChartConstants.xlLine, _msOfficeChartConstants.xlLineMarkers , _msOfficeChartConstants.xlLineMarkersStacked, _msOfficeChartConstants.xlLineMarkersStacked100, _msOfficeChartConstants.xlLineStacked, _msOfficeChartConstants.xlLineStacked100):
			if self.pointIndex > 1:
				if self.currentSeries.Values[self.pointIndex-1] == self.currentSeries.Values[self.pointIndex - 2]:
					# Translators: For line charts, indicates no change from the previous data point on the left
					output += _( "no change from point {previousIndex}, ").format( previousIndex = self.pointIndex-1 )
				elif self.currentSeries.Values[self.pointIndex-1] > self.currentSeries.Values[self.pointIndex-2]:
					# Translators: For line charts, indicates an increase from the previous data point on the left
					output += _( "Increased by {incrementValue} from point {previousIndex}, ").format( incrementValue = self.currentSeries.Values[self.pointIndex-1] - self.currentSeries.Values[self.pointIndex-2] , previousIndex = self.pointIndex-1 )
				else:
					# Translators: For line charts, indicates a decrease from the previous data point on the left
					output += _( "decreased by {decrementValue} from point {previousIndex}, ").format( decrementValue = self.currentSeries.Values[self.pointIndex-2] - self.currentSeries.Values[self.pointIndex-1] , previousIndex = self.pointIndex-1 )
		if self.wordChartObject.HasAxis(_msOfficeChartConstants.xlCategory) and self.wordChartObject.Axes(_msOfficeChartConstants.xlCategory).HasTitle:
			# Translators: Specifies the category of a data point.
			# {categoryAxisTitle} will be replaced with the title of the category axis; e.g. "Month".
			# {categoryAxisData} will be replaced with the category itself; e.g. "January".
			output += _( "{categoryAxisTitle} {categoryAxisData}: ").format( categoryAxisTitle = self.wordChartObject.Axes(_msOfficeChartConstants.xlCategory).AxisTitle.Text , categoryAxisData = excelSeriesXValue )
		else:
			# Translators: Specifies the category of a data point.
			# {categoryAxisData} will be replaced with the category itself; e.g. "January".
			output += _( "Category {categoryAxisData}: ").format( categoryAxisData = excelSeriesXValue )
		if self.wordChartObject.HasAxis(_msOfficeChartConstants.xlValue) and self.wordChartObject.Axes(_msOfficeChartConstants.xlValue).HasTitle:
			# Translators: Specifies the value of a data point.
			# {valueAxisTitle} will be replaced with the title of the value axis; e.g. "Amount".
			# {valueAxisData} will be replaced with the value itself; e.g. "1000".
			output +=  _( "{valueAxisTitle} {valueAxisData}").format( valueAxisTitle = self.wordChartObject.Axes(_msOfficeChartConstants.xlValue).AxisTitle.Text , valueAxisData = self.currentSeries.Values[self.pointIndex-1])
		else:
			# Translators: Specifies the value of a data point.
			# {valueAxisData} will be replaced with the value itself; e.g. "1000".
			output +=  _( "value {valueAxisData}").format( valueAxisData = self.currentSeries.Values[self.pointIndex-1])
		if self.wordChartObject.ChartType in (_msOfficeChartConstants.xlPie, _msOfficeChartConstants.xlPieExploded, _msOfficeChartConstants.xlPieOfPie):
			import math
			total = math.fsum( self.currentSeries.Values )
			# Translators: Details about a slice of a pie chart.
			# For example, this might report "fraction 25.25 percent slice 1 of 5"
			output += _( " fraction {fractionValue:.2f} Percent slice {pointIndex} of {pointCount}").format( fractionValue = self.currentSeries.Values[self.pointIndex-1] / total *100.00 , pointIndex = self.pointIndex , pointCount = count )
		else:
			# Translators: Details about a segment of a chart.
			# For example, this might report "column 1 of 5"
			output += _( " {segmentType} {pointIndex} of {pointCount}").format( segmentType = self.getChartSegment() ,  pointIndex = self.pointIndex , pointCount = count )
		return output

class ElementsListDialog(browseMode.ElementsListDialog):

	ELEMENT_TYPES=(browseMode.ElementsListDialog.ELEMENT_TYPES[0],browseMode.ElementsListDialog.ELEMENT_TYPES[1],
		# Translators: The label of a radio button to select the type of element
		# in the browse mode Elements List dialog.
		("annotation", _("&Annotations")),
		# Translators: The label of a radio button to select the type of element
		# in the browse mode Elements List dialog.
		("chart", _("&Charts")),
	)
