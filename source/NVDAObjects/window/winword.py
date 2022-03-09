# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2020 NV Access Limited, Manish Agrawal, Derek Riemer, Babbage B.V.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


import ctypes
import time
from typing import (
	Optional,
	Dict,
)

from comtypes import COMError, GUID, BSTR
import comtypes.client
import comtypes.automation
import uuid
import operator
import locale
import collections
import colorsys
import eventHandler
import braille
from scriptHandler import script
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
from controlTypes import TextPosition
import treeInterceptorHandler
import browseMode
import review
from cursorManager import CursorManager, ReviewCursorManager
from tableUtils import HeaderCellInfo, HeaderCellTracker
from . import Window
from ..behaviors import EditableTextWithoutAutoSelectDetection
from . import _msOfficeChart
import locationHelper

#Word constants

#wdLineSpacing rules
wdLineSpaceSingle=0
wdLineSpace1pt5=1
wdLineSpaceDouble=2
wdLineSpaceAtLeast=3
wdLineSpaceExactly=4
wdLineSpaceMultiple=5

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
wdVerticalPositionRelativeToPage=6
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

# MsoThemeColorSchemeIndex 
msoThemeAccent1=5
msoThemeAccent2=6
msoThemeAccent3=7
msoThemeAccent4=8
msoThemeAccent5=9
msoThemeAccent6=10
msoThemeDark1=1
msoThemeDark2=3
msoThemeFollowedHyperlink=12
msoThemeHyperlink=11
msoThemeLight1=2
msoThemeLight2=4

# WdThemeColorIndex 
wdNotThemeColor=-1
wdThemeColorAccent1=4
wdThemeColorAccent2=5
wdThemeColorAccent3=6
wdThemeColorAccent4=7
wdThemeColorAccent5=8
wdThemeColorAccent6=9
wdThemeColorBackground1=12
wdThemeColorBackground2=14
wdThemeColorHyperlink=10
wdThemeColorHyperlinkFollowed=11
wdThemeColorMainDark1=0
wdThemeColorMainDark2=2
wdThemeColorMainLight1=1
wdThemeColorMainLight2=3
wdThemeColorText1=13
wdThemeColorText2=15

# Word Field types
FIELD_TYPE_REF = 3 # cross reference field
FIELD_TYPE_HYPERLINK = 88 # hyperlink field

# Mapping from http://www.wordarticles.com/Articles/Colours/2007.php#UIConsiderations
WdThemeColorIndexToMsoThemeColorSchemeIndex={
	wdThemeColorMainDark1:msoThemeDark1,
	wdThemeColorMainLight1:msoThemeLight1,
	wdThemeColorMainDark2:msoThemeDark2,
	wdThemeColorMainLight2:msoThemeLight2,
	wdThemeColorAccent1:msoThemeAccent1,
	wdThemeColorAccent2:msoThemeAccent2,
	wdThemeColorAccent3:msoThemeAccent3,
	wdThemeColorAccent4:msoThemeAccent4,
	wdThemeColorAccent5:msoThemeAccent5,
	wdThemeColorAccent6:msoThemeAccent6,
	wdThemeColorHyperlink:msoThemeHyperlink,
	wdThemeColorHyperlinkFollowed:msoThemeFollowedHyperlink,
	wdThemeColorBackground1:msoThemeLight1,
	wdThemeColorText1:msoThemeDark1,
	wdThemeColorBackground2:msoThemeLight2,
	wdThemeColorText2:msoThemeDark2,
}

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
	wdFieldFormTextInput:controlTypes.Role.EDITABLETEXT,
	wdFieldFormCheckBox:controlTypes.Role.CHECKBOX,
	wdFieldFormDropDown:controlTypes.Role.COMBOBOX,
}

wdContentControlTypesToNVDARoles={
	wdContentControlRichText:controlTypes.Role.EDITABLETEXT,
	wdContentControlText:controlTypes.Role.EDITABLETEXT,
	wdContentControlPicture:controlTypes.Role.GRAPHIC,
	wdContentControlComboBox:controlTypes.Role.COMBOBOX,
	wdContentControlDropdownList:controlTypes.Role.COMBOBOX,
	wdContentControlDate:controlTypes.Role.EDITABLETEXT,
	wdContentControlGroup:controlTypes.Role.GROUPING,
	wdContentControlCheckBox:controlTypes.Role.CHECKBOX,
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

formatConfigFlagsMap = {
	"reportFontName": 0x1,
	"reportFontSize": 0x2,
	"reportFontAttributes": 0x4,
	"reportColor": 0x8,
	"reportAlignment": 0x10,
	"reportStyle": 0x20,
	"reportSpellingErrors": 0x40,
	"reportPage": 0x80,
	"reportLineNumber": 0x100,
	"reportTables": 0x200,
	"reportLists": 0x400,
	"reportLinks": 0x800,
	"reportComments": 0x1000,
	"reportHeadings": 0x2000,
	"autoLanguageSwitching": 0x4000,
	"reportRevisions": 0x8000,
	"reportParagraphIndentation": 0x10000,
	"reportLineSpacing": 0x40000,
	"reportSuperscriptsAndSubscripts": 0x80000,
	"reportGraphics": 0x100000,
}
formatConfigFlag_includeLayoutTables = 0x20000

# Map some characters from 0 to Unicode. Meant to be used with bullets only.
# Doesn't care about the actual font, so can give incorrect Unicode in rare cases.
mapPUAToUnicode = {
	# from : to # fontname
	u'\uF06E': u'\u25A0',  # Wingdings (black square)
	u'\uF076': u'\u2756',  # Wingdings (black diamond minus white x
	u'\uF0A7': u'\u25AA',  # Symbol (black small square)
	u'\uF0A8': u'\u2666',  # Symbol (black diamond suit)
	u'\uF0B7': u'\u2022',  # Symbol (bullet)
	u'\uF0D8': u'\u2B9A',  # Wingdings (three-D top-lighted RIGHTWARDS equilateral arrowhead)
	u'\uF0E8': u'\U0001f87a',  # Wingdings (wide-headed rightwards heavy barb arrow)
	u'\uF0F0': u'\u21E8',  # Wingdings (right white arrow)
	u'\uF0FC': u'\u2714',  # Wingdings (heavy check mark)
}

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
		# Translators: The label shown for a comment in the NVDA Elements List dialog in Microsoft Word.
		# {text}, {author} and {date} will be replaced by the corresponding details about the comment.
		return _(u"comment: {text} by {author} on {date}").format(author=author,text=text,date=date)

	def rangeFromCollectionItem(self,item):
		return item.scope

class WordDocumentFieldQuickNavItem(WordDocumentCollectionQuickNavItem):
	def rangeFromCollectionItem(self,item):
		return item.result

class WordDocumentRevisionQuickNavItem(WordDocumentCollectionQuickNavItem):
	@property
	def label(self):
		revisionType=wdRevisionTypeLabels.get(self.collectionItem.type)
		author=self.collectionItem.author or ""
		date=self.collectionItem.date
		description=self.collectionItem.formatDescription or ""
		text=(self.collectionItem.range.text or "")[:100]
		# Translators: The label shown for an editor revision (tracked change)  in the NVDA Elements List dialog in Microsoft Word.
		# {revisionType} will be replaced with the type of revision; e.g. insertion, deletion or property.
		# {description} will be replaced with a description of the formatting changes, if any.
		# {text}, {author} and {date} will be replaced by the corresponding details about the revision.
		return _(u"{revisionType} {description}: {text} by {author} on {date}").format(revisionType=revisionType,author=author,text=text,date=date,description=description)

class WordDocumentChartQuickNavItem(WordDocumentCollectionQuickNavItem):
	@property
	def label(self):
		text=""
		if self.collectionItem.Chart.HasTitle:
			text=self.collectionItem.Chart.ChartTitle.Text
		else:
			text=self.collectionItem.Chart.Name
		return u"{text}".format(text=text)

	def moveTo(self):
		chartNVDAObj = _msOfficeChart.OfficeChart(windowHandle= self.document.rootNVDAObject.windowHandle, officeApplicationObject=self.rangeObj.Document.Application, officeChartObject=self.collectionItem.Chart , initialDocument  = self.document.rootNVDAObject )
		eventHandler.queueEvent("gainFocus",chartNVDAObj)

class WordDocumentSpellingErrorQuickNavItem(WordDocumentCollectionQuickNavItem):

	def rangeFromCollectionItem(self,item):
		return item

	@property
	def label(self):
		text=self.collectionItem.text
		# Translators: The label shown for a spelling error in the NVDA Elements List dialog in Microsoft Word.
		# {text} will be replaced with the text of the spelling error.
		return _(u"spelling: {text}").format(text=text)

class WinWordCollectionQuicknavIterator(object):
	"""
	Allows iterating over an MS Word collection (e.g. HyperLinks) emitting L{QuickNavItem} objects.
	"""

	quickNavItemClass=WordDocumentCollectionQuickNavItem #: the QuickNavItem class that should be instanciated and emitted. 

	def __init__(self,itemType,document,direction,rangeObj,includeCurrent):
		"""
		See L{QuickNavItemIterator} for itemType, document and direction definitions.
		@param rangeObj: a Microsoft Word range object where the collection should be fetched from.
		@param includeCurrent: if true then any item at the initial position will be also emitted
			rather than just further ones.
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
		for index in range(1,itemCount+1):
			if self.direction=="previous":
				index=itemCount-(index-1)
			collectionItem=items[index]
			try:
				item=self.quickNavItemClass(self.itemType,self.document,collectionItem)
			except COMError:
				message = ("Error iterating over item with "
					"type: {type}, iteration direction: {dir}, total item count: {count}, item at index: {index}"
					"\nThis could be caused by an issue with some element within or a corruption of the word document."
					).format(type=self.itemType, dir=self.direction, count=itemCount, index=index)
				log.debugWarning(message ,exc_info=True)
				continue
			itemRange=item.rangeObj
			# Skip over the item we're already on.
			if not self.includeCurrent and isFirst and ((self.direction=="next" and itemRange.start<=self.rangeObj.start) or (self.direction=="previous" and itemRange.end>self.rangeObj.end)):
				continue
			if not self.filter(collectionItem):
				continue
			yield item
			isFirst=False

class LinkWinWordCollectionQuicknavIterator(WinWordCollectionQuicknavIterator):
	quickNavItemClass=WordDocumentFieldQuickNavItem
	def collectionFromRange(self,rangeObj):
		return rangeObj.fields

	def filter(self, item):
		t = item.type
		if t == FIELD_TYPE_REF:
			fieldText = item.code.text.strip().split(' ')
			# ensure that the text has a \\h in it
			return any( fieldText[i] == '\\h' for i in range(2, len(fieldText)) )
		return t == FIELD_TYPE_HYPERLINK


class CommentWinWordCollectionQuicknavIterator(WinWordCollectionQuicknavIterator):
	quickNavItemClass=WordDocumentCommentQuickNavItem
	def collectionFromRange(self,rangeObj):
		return rangeObj.comments

class RevisionWinWordCollectionQuicknavIterator(WinWordCollectionQuicknavIterator):
	quickNavItemClass=WordDocumentRevisionQuickNavItem
	def collectionFromRange(self,rangeObj):
		return rangeObj.revisions

class SpellingErrorWinWordCollectionQuicknavIterator(WinWordCollectionQuicknavIterator):
	quickNavItemClass=WordDocumentSpellingErrorQuickNavItem
	def collectionFromRange(self,rangeObj):
		return rangeObj.spellingErrors

class GraphicWinWordCollectionQuicknavIterator(WinWordCollectionQuicknavIterator):
	def collectionFromRange(self,rangeObj):
		return rangeObj.inlineShapes
	def filter(self,item):
		return 2<item.type<5

class TableWinWordCollectionQuicknavIterator(WinWordCollectionQuicknavIterator):
	def collectionFromRange(self,rangeObj):
		return rangeObj.tables

	def filter(self,item):
		return config.conf["documentFormatting"]["includeLayoutTables"] or item.borders.enable


class ChartWinWordCollectionQuicknavIterator(WinWordCollectionQuicknavIterator):
	quickNavItemClass=WordDocumentChartQuickNavItem

	def collectionFromRange(self,rangeObj):
		return rangeObj.inlineShapes

	def filter(self,item):
		return item.type==wdInlineShapeChart


class LazyControlField_RowAndColumnHeaderText(textInfos.ControlField):

	def __init__(self, ti):
		self._ti = ti
		super().__init__()

	def get(self, name, default=None):
		if name == "table-rowheadertext":
			try:
				cell = self._ti._rangeObj.cells[1]
			except IndexError:
				log.debugWarning("no cells for table row, possibly on end of cell mark")
				return super().get(name, default)
			return self._ti.obj.fetchAssociatedHeaderCellText(cell, False)
		elif name == "table-columnheadertext":
			try:
				cell = self._ti._rangeObj.cells[1]
			except IndexError:
				log.debugWarning("no cells for table row, possibly on end of cell mark")
				return super().get(name, default)
			return self._ti.obj.fetchAssociatedHeaderCellText(cell, True)
		else:
			return super().get(name, default)

class WordDocumentTextInfo(textInfos.TextInfo):

	# #4852: temporary fix.
	# force mouse reading chunk to sentense to make it what it used to be in 2014.4.
	# We need to however fix line so it does not accidentially scroll.
	def _get_unit_mouseChunk(self):
		unit=super(WordDocumentTextInfo,self).unit_mouseChunk
		if unit==textInfos.UNIT_LINE:
			unit=textInfos.UNIT_SENTENCE
		return unit

	def _get_locationText(self):
		textList=[]
		# #8994: MS Word can only give accurate distances (taking paragraph indenting into account) when directly querying the selection. 
		r=self._rangeObj
		s=self.obj.WinwordSelectionObject
		if s.isEqual(r):
			r=s
		else:
			return super(WordDocumentTextInfo,self).locationText
		offset=r.information(wdHorizontalPositionRelativeToPage)
		distance=self.obj.getLocalizedMeasurementTextForPointSize(offset)
		# Translators: a distance from the left edge of the page in Microsoft Word
		textList.append(_("{distance} from left edge of page").format(distance=distance))
		offset=r.information(wdVerticalPositionRelativeToPage)
		distance=self.obj.getLocalizedMeasurementTextForPointSize(offset)
		# Translators: a distance from the left edge of the page in Microsoft Word
		textList.append(_("{distance} from top edge of page").format(distance=distance))
		return ", ".join(textList)

	def copyToClipboard(self, notify):
		self._rangeObj.copy()
		if notify:
			ui.reportTextCopiedToClipboard(self.text)
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
				return eventHandler.queueEvent('gainFocus',_msOfficeChart.OfficeChart(windowHandle= self.obj.windowHandle, officeApplicationObject=self.obj.WinwordDocumentObject.Application, officeChartObject=newRng.InlineShapes[1].Chart , initialDocument = self.obj ))
		# Handle activating links.
		# It is necessary to expand to word to get a link as the link's first character is never actually in the link!
		tempRange=self._rangeObj.duplicate
		tempRange.expand(wdWord)
		links=tempRange.hyperlinks
		if links.count>0:
			links[1].follow()
			return
		tempRange.expand(wdParagraph)
		fields=tempRange.fields
		for field in (fields.item(i) for i in range(1, fields.count+1)):
			if field.type != FIELD_TYPE_REF:
				continue
			fResult = field.result
			fResult.moveStart(wdCharacter,-1) # move back one visible character (passed the hidden text eg the code for the reference).
			fResStart = fResult.start +1 # don't include the character before the hidden text.
			fResEnd = fResult.end
			rObjStart = self._rangeObj.start
			rObjEnd = self._rangeObj.end
			# check to see if the _rangeObj is inside the fResult range
			if not (fResStart <= rObjStart and fResEnd >= rObjEnd):
				continue
			# text will be something like ' REF _Ref457210120 \\h '
			fieldText = field.code.text.strip().split(' ')
			# the \\h field indicates that the field is a link
			if not any( fieldText[i] == '\\h' for i in range(2, len(fieldText)) ):
				log.debugWarning("no \\h for field xref: %s" % field.code.text)
				continue
			bookmarkKey = fieldText[1] # we want the _Ref12345 part
			# get book mark start, we need to look at the whole document to find the bookmark.
			tempRange.Expand(wdStory)
			bMark = tempRange.bookmarks(bookmarkKey)
			self._rangeObj.setRange(bMark.start, bMark.start)
			self.updateCaret()
			tiCopy = self.copy()
			tiCopy.expand(textInfos.UNIT_LINE)
			speech.speakTextInfo(tiCopy, reason=controlTypes.OutputReason.FOCUS)
			braille.handler.handleCaretMove(self)
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
		if isinstance(position, locationHelper.Point):
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
		elif isinstance(position,WordDocumentTextInfo):
			# copying from one textInfo to another
			self._rangeObj=position._rangeObj.duplicate
		else:
			raise NotImplementedError("position: %s"%position)

	# C901 'getTextWithFields' is too complex
	# Note: when working on getTextWithFields, look for opportunities to simplify
	# and move logic out into smaller helper functions.
	def getTextWithFields(  # noqa: C901
		self,
		formatConfig: Optional[Dict] = None
	) -> textInfos.TextInfo.TextWithFieldsT:
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
		# #9067: format config flags map is a dictionary.
		formatConfigFlags=sum(y for x,y in formatConfigFlagsMap.items() if formatConfig.get(x,False))
		if self.shouldIncludeLayoutTables:
			formatConfigFlags+=formatConfigFlag_includeLayoutTables
		if self.obj.ignoreEditorRevisions:
			formatConfigFlags&=~formatConfigFlagsMap['reportRevisions']
		if self.obj.ignorePageNumbers:
			formatConfigFlags&=~formatConfigFlagsMap['reportPage']
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
			elif index>0 and isinstance(item,str) and item.isspace():
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
			role=controlTypes.Role.HEADING
		elif role=="table":
			role=controlTypes.Role.TABLE
			field['table-rowcount']=int(field.get('table-rowcount',0))
			field['table-columncount']=int(field.get('table-columncount',0))
		elif role=="tableCell":
			role=controlTypes.Role.TABLECELL
			field['table-rownumber']=int(field.get('table-rownumber',0))
			field['table-columnnumber']=int(field.get('table-columnnumber',0))
		elif role=="footnote":
			role=controlTypes.Role.FOOTNOTE
		elif role=="endnote":
			role=controlTypes.Role.ENDNOTE
		elif role=="graphic":
			role=controlTypes.Role.GRAPHIC
		elif role=="chart":
			role=controlTypes.Role.CHART
		elif role=="object":
			progid=field.get("progid")
			if progid and progid.startswith("Equation.DSMT"):
				# MathType.
				role=controlTypes.Role.MATH
			else:
				role=controlTypes.Role.EMBEDDEDOBJECT
		else:
			fieldType=int(field.pop('wdFieldType',-1))
			if fieldType!=-1:
				role=wdFieldTypesToNVDARoles.get(fieldType,controlTypes.Role.UNKNOWN)
				if fieldType==wdFieldFormCheckBox and int(field.get('wdFieldResult','0'))>0:
					field['states']=set([controlTypes.State.CHECKED])
				elif fieldType==wdFieldFormDropDown:
					field['value']=field.get('wdFieldResult',None)
			fieldStatusText=field.pop('wdFieldStatusText',None)
			if fieldStatusText:
				field['name']=fieldStatusText
				field['alwaysReportName']=True
			else:
				fieldType=int(field.get('wdContentControlType',-1))
				if fieldType!=-1:
					role=wdContentControlTypesToNVDARoles.get(fieldType,controlTypes.Role.UNKNOWN)
					if role==controlTypes.Role.CHECKBOX:
						fieldChecked=bool(int(field.get('wdContentControlChecked','0')))
						if fieldChecked:
							field['states']=set([controlTypes.State.CHECKED])
					fieldTitle=field.get('wdContentControlTitle',None)
					if fieldTitle:
						field['name']=fieldTitle
						field['alwaysReportName']=True
		if role is not None: field['role']=role
		if role==controlTypes.Role.TABLE and field.get('longdescription'):
			field['states']=set([controlTypes.State.HASLONGDESC])
		storyType=int(field.pop('wdStoryType',0))
		if storyType:
			name=storyTypeLocalizedLabels.get(storyType,None)
			if name:
				field['name']=name
				field['alwaysReportName']=True
				field['role']=controlTypes.Role.FRAME
		newField = LazyControlField_RowAndColumnHeaderText(self)
		newField.update(field)
		return newField

	def _normalizeFormatField(self,field,extraDetail=False):
		_startOffset=int(field.pop('_startOffset'))
		_endOffset=int(field.pop('_endOffset'))
		lineSpacingRule=field.pop('wdLineSpacingRule',None)
		lineSpacingVal=field.pop('wdLineSpacing',None)
		if lineSpacingRule is not None:
			lineSpacingRule=int(lineSpacingRule)
			if lineSpacingRule==wdLineSpaceSingle:
				# Translators: single line spacing
				field['line-spacing']=pgettext('line spacing value',"single")
			elif lineSpacingRule==wdLineSpaceDouble:
				# Translators: double line spacing
				field['line-spacing']=pgettext('line spacing value',"double")
			elif lineSpacingRule==wdLineSpace1pt5:
				# Translators:  line spacing of 1.5 lines
				field['line-spacing']=pgettext('line spacing value',"1.5 lines")
			elif lineSpacingRule==wdLineSpaceExactly:
				field['line-spacing'] = pgettext(
					'line spacing value',
					# Translators: line spacing of exactly x point
					"exactly {space:.1f} pt"
				).format(space=float(lineSpacingVal))
			elif lineSpacingRule==wdLineSpaceAtLeast:
				# Translators: line spacing of at least x point
				field['line-spacing']=pgettext('line spacing value',"at least %.1f pt")%float(lineSpacingVal)
			elif lineSpacingRule==wdLineSpaceMultiple:
				# Translators: line spacing of x lines
				field['line-spacing']=pgettext('line spacing value',"%.1f lines")%(float(lineSpacingVal)/12.0)
		revisionType=int(field.pop('wdRevisionType',0))
		if revisionType==wdRevisionInsert:
			field['revision-insertion']=True
		elif revisionType==wdRevisionDelete:
			field['revision-deletion']=True
		elif revisionType:
			revisionLabel=wdRevisionTypeLabels.get(revisionType,None)
			if revisionLabel:
				field['revision']=revisionLabel
		textPosition = field.pop('text-position', TextPosition.BASELINE)
		field['text-position'] = TextPosition(textPosition)
		color=field.pop('color',None)
		if color is not None:
			field['color']=self.obj.winwordColorToNVDAColor(int(color))
		try:
			languageId = int(field.pop('wdLanguageId',0))
			if languageId:
				field['language']=languageHandler.windowsLCIDToLocaleName(languageId)
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
		bullet=field.get('line-prefix')
		if bullet and len(bullet)==1:
			field['line-prefix']=mapPUAToUnicode.get(bullet,bullet)
		return field

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
		if end:
			newEndOffset = self._rangeObj.end
			# the new endOffset should not have become smaller than the old endOffset, this could cause an infinite loop in
			# a case where you called move end then collapse until the size of the range is no longer being reduced.
			# For an example of this see sayAll (specifically readTextHelper_generator in sayAll.py)
			if newEndOffset < oldEndOffset :
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
		if (direction>0 and endPoint!="end"
			and unit not in (wdCharacter,wdWord) # moving by units of line or more
			and (_rangeObj.start+1) == self.obj.WinwordDocumentObject.range().end # character after the range start is the end of the document range
			):
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

	def _get_pointAtStart(self):
		left = ctypes.c_int()
		top = ctypes.c_int()
		width = ctypes.c_int()
		height = ctypes.c_int()
		try:
			self.obj.WinwordWindowObject.GetPoint(ctypes.byref(left), ctypes.byref(top), ctypes.byref(width), ctypes.byref(height), self._rangeObj)
		except COMError:
			raise LookupError
		if not any((left.value, top.value, width.value, height.value)):
			raise LookupError
		return locationHelper.Point(left.value, top.value)

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
		rangeObj = self._rangeObj.Duplicate
		rangeObj.Start = int(field["shapeoffset"])
		obj = rangeObj.InlineShapes[0].OLEFormat
		try:
			return mathType.getMathMl(obj)
		except:
			log.debugWarning("Error fetching math with mathType", exc_info=True)
			raise LookupError("Couldn't get MathML from MathType")

class BrowseModeWordDocumentTextInfo(browseMode.BrowseModeDocumentTextInfo,treeInterceptorHandler.RootProxyTextInfo):

	def __init__(self,obj,position,_rangeObj=None):
		if isinstance(position,WordDocument):
			position=textInfos.POSITION_CARET
		super(BrowseModeWordDocumentTextInfo,self).__init__(obj,position,_rangeObj=_rangeObj)

	def _get_focusableNVDAObjectAtStart(self):
		return self.obj.rootNVDAObject

class WordDocumentTreeInterceptor(browseMode.BrowseModeDocumentTreeInterceptor):

	TextInfo=BrowseModeWordDocumentTextInfo

	def _activateLongDesc(self,controlField):
		longDesc=controlField.get('longdescription')
		# Translators: the title of the message dialog desplaying an MS Word table description.
		ui.browseableMessage(longDesc,_("Table description"))

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
		elif nodeType=="error":
			return SpellingErrorWinWordCollectionQuicknavIterator(nodeType,self,direction,rangeObj,includeCurrent).iterate()
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

class WordDocument(Window):

	def winwordColorToNVDAColor(self,val):
		if val>=0:
			# normal RGB value
			return colors.RGB.fromCOLORREF(val).name
		elif (val&0xffffffff)==0xff000000:
			# Translators: the default (automatic) color in Microsoft Word
			return _("default color")
		elif ((val>>28)&0xf)==0xd and ((val>>16)&0xff)==0x00:
			# An MS word color index Plus intencity
			# Made up of MS Word Theme Color index, hsv value ratio (MS Word darker percentage) and hsv saturation ratio (MS Word lighter percentage)
			# Info: http://www.wordarticles.com/Articles/Colours/2007.php#UIConsiderations
			saturationRatio=(val&0xff)/255.0
			valueRatio=((val>>8)&0xff)/255.0
			themeColorIndex=(val>>24)&0x0f
			# Convert the MS Word theme color index to an MS Office color scheme index
			schemeColorIndex=WdThemeColorIndexToMsoThemeColorSchemeIndex[themeColorIndex]
			# Lookup the  rgb value for the MS Office scheme color index based on the current theme
			colorref=self.WinwordDocumentObject.documentTheme.themeColorScheme(schemeColorIndex).rgb
			# Convert the rgb value to hsv and apply the saturation and value ratios
			rgb=tuple(x/255.0 for x in colors.RGB.fromCOLORREF(colorref))
			hsv=colorsys.rgb_to_hsv(*rgb)
			hsv=(hsv[0],hsv[1]*saturationRatio,hsv[2]*valueRatio)
			rgb=colorsys.hsv_to_rgb(*hsv)
			name=colors.RGB(rgb[0]*255,rgb[1]*255,rgb[2]*255).name
			return name
		else:
			raise ValueError("Unknown color format %x %x %x %x"%((val>>24)&0xff,(val>>16)&0xff,(val>>8)&0xff,val&0xff))

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
		if not self.WinwordSelectionObject:
			# We cannot fetch the Word object model, so we therefore cannot report the format change.
			# The object model may be unavailable because this is a pure UIA implementation such as Windows 10 Mail, or its within Windows Defender Application Guard.
			# Eventually UIA will have its own way of detecting format changes at the cursor. For now, just let the gesture through and don't erport anything.
			return gesture.send()
		val=self._WaitForValueChangeForAction(lambda: gesture.send(),lambda: self.WinwordSelectionObject.font.bold)
		if val:
			# Translators: a message when toggling formatting in Microsoft word
			ui.message(_("Bold on"))
		else:
			# Translators: a message when toggling formatting in Microsoft word
			ui.message(_("Bold off"))

	def script_toggleItalic(self,gesture):
		if not self.WinwordSelectionObject:
			# We cannot fetch the Word object model, so we therefore cannot report the format change.
			# The object model may be unavailable because this is a pure UIA implementation such as Windows 10 Mail, or its within Windows Defender Application Guard.
			# Eventually UIA will have its own way of detecting format changes at the cursor. For now, just let the gesture through and don't erport anything.
			return gesture.send()
		val=self._WaitForValueChangeForAction(lambda: gesture.send(),lambda: self.WinwordSelectionObject.font.italic)
		if val:
			# Translators: a message when toggling formatting in Microsoft word
			ui.message(_("Italic on"))
		else:
			# Translators: a message when toggling formatting in Microsoft word
			ui.message(_("Italic off"))

	def script_toggleUnderline(self,gesture):
		if not self.WinwordSelectionObject:
			# We cannot fetch the Word object model, so we therefore cannot report the format change.
			# The object model may be unavailable because this is a pure UIA implementation such as Windows 10 Mail, or its within Windows Defender Application Guard.
			# Eventually UIA will have its own way of detecting format changes at the cursor. For now, just let the gesture through and don't erport anything.
			return gesture.send()
		val=self._WaitForValueChangeForAction(lambda: gesture.send(),lambda: self.WinwordSelectionObject.font.underline)
		if val:
			# Translators: a message when toggling formatting in Microsoft word
			ui.message(_("Underline on"))
		else:
			# Translators: a message when toggling formatting in Microsoft word
			ui.message(_("Underline off"))

	def script_toggleAlignment(self,gesture):
		if not self.WinwordSelectionObject:
			# We cannot fetch the Word object model, so we therefore cannot report the format change.
			# The object model may be unavailable because this is a pure UIA implementation such as Windows 10 Mail, or its within Windows Defender Application Guard.
			# Eventually UIA will have its own way of detecting format changes at the cursor. For now, just let the gesture through and don't erport anything.
			return gesture.send()
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

	@script(gestures=["kb:control+m", "kb:control+shift+m", "kb:control+t", "kb:control+shift+t"])
	def script_changeParagraphLeftIndent(self, gesture):
		if not self.WinwordSelectionObject:
			# We cannot fetch the Word object model, so we therefore cannot report the format change.
			# The object model may be unavailable because this is a pure UIA implementation such as Windows 10 Mail,
			# or it's within Windows Defender Application Guard.
			# For now, just let the gesture through and don't report anything.
			return gesture.send()
		margin = self.WinwordDocumentObject.PageSetup.LeftMargin
		val = self._WaitForValueChangeForAction(
			lambda: gesture.send(),
			lambda: self.WinwordSelectionObject.paragraphFormat.LeftIndent
		)
		msg = self.getLocalizedMeasurementTextForPointSize(margin + val)
		ui.message(msg)

	def script_toggleSuperscriptSubscript(self,gesture):
		if not self.WinwordSelectionObject:
			# We cannot fetch the Word object model, so we therefore cannot report the format change.
			# The object model may be unavailable because this is a pure UIA implementation such as Windows 10 Mail, or its within Windows Defender Application Guard.
			# Eventually UIA will have its own way of detecting format changes at the cursor. For now, just let the gesture through and don't erport anything.
			return gesture.send()
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

	def script_moveParagraphDown(self,gesture):
		oldBookmark=self.makeTextInfo(textInfos.POSITION_CARET).bookmark
		gesture.send()
		if self._hasCaretMoved(oldBookmark)[0]:
			info=self.makeTextInfo(textInfos.POSITION_SELECTION)
			info.collapse()
			info.move(textInfos.UNIT_PARAGRAPH,-1,endPoint="start")
			lastParaText=info.text.strip()
			if lastParaText:
				# Translators: a message reported when a paragraph is moved below another paragraph
				ui.message(_("Moved below %s")%lastParaText)
			else:
				# Translators: a message reported when a paragraph is moved below a blank paragraph 
				ui.message(_("Moved below blank paragraph"))

	def script_moveParagraphUp(self,gesture):
		oldBookmark=self.makeTextInfo(textInfos.POSITION_CARET).bookmark
		gesture.send()
		if self._hasCaretMoved(oldBookmark)[0]:
			info=self.makeTextInfo(textInfos.POSITION_SELECTION)
			info.collapse()
			info.move(textInfos.UNIT_PARAGRAPH,1)
			info.expand(textInfos.UNIT_PARAGRAPH)
			lastParaText=info.text.strip()
			if lastParaText:
				# Translators: a message reported when a paragraph is moved above another paragraph
				ui.message(_("Moved above %s")%lastParaText)
			else:
				# Translators: a message reported when a paragraph is moved above a blank paragraph 
				ui.message(_("Moved above blank paragraph"))

	def script_increaseDecreaseOutlineLevel(self,gesture):
		if not self.WinwordSelectionObject:
			# We cannot fetch the Word object model, so we therefore cannot report the format change.
			# The object model may be unavailable because this is a pure UIA implementation such as Windows 10 Mail, or its within Windows Defender Application Guard.
			# Eventually UIA will have its own way of detecting format changes at the cursor. For now, just let the gesture through and don't erport anything.
			return gesture.send()
		val=self._WaitForValueChangeForAction(lambda: gesture.send(),lambda: self.WinwordSelectionObject.paragraphFormat.outlineLevel)
		style=self.WinwordSelectionObject.style.nameLocal
		# Translators: the message when the outline level / style is changed in Microsoft word
		ui.message(_("{styleName} style, outline level {outlineLevel}").format(styleName=style,outlineLevel=val))

	def script_increaseDecreaseFontSize(self,gesture):
		if not self.WinwordSelectionObject:
			# We cannot fetch the Word object model, so we therefore cannot report the format change.
			# The object model may be unavailable because this is a pure UIA implementation such as Windows 10 Mail, or its within Windows Defender Application Guard.
			# Eventually UIA will have its own way of detecting format changes at the cursor. For now, just let the gesture through and don't erport anything.
			return gesture.send()
		val=self._WaitForValueChangeForAction(lambda: gesture.send(),lambda: self.WinwordSelectionObject.font.size)
		# Translators: a message when increasing or decreasing font size in Microsoft Word
		ui.message(_("{size:g} point font").format(size=val))

	@script(gesture="kb:control+shift+8")
	def script_toggleDisplayNonprintingCharacters(self, gesture):
		if not self.WinwordWindowObject:
			# We cannot fetch the Word object model, so we therefore cannot report the status change.
			# The object model may be unavailable because this is a pure UIA implementation such as Windows 10 Mail,
			# or it's within Windows Defender Application Guard.
			# In this case, just let the gesture through and don't report anything.
			return gesture.send()
		val = self._WaitForValueChangeForAction(
			lambda: gesture.send(),
			lambda: self.WinwordWindowObject.ActivePane.View.ShowAll
		)
		if val:
			# Translators: a message when toggling Display Nonprinting Characters in Microsoft word
			ui.message(_("Display nonprinting characters"))
		else:
			# Translators: a message when toggling Display Nonprinting Characters in Microsoft word
			ui.message(_("Hide nonprinting characters"))

	@script(gestures=["kb:tab", "kb:shift+tab"])
	def script_tab(self,gesture):
		"""
		A script for the tab key which:
		* if in a table, announces the newly selected cell or new cell where the caret is, or 
		* If not in a table, announces the distance of the caret from the left edge of the document, and any remaining text on that line.
		"""
		gesture.send()
		self.reportTab()

	def reportTab(self):
		selectionObj=self.WinwordSelectionObject
		inTable=selectionObj.tables.count>0 if selectionObj else False
		info=self.makeTextInfo(textInfos.POSITION_SELECTION)
		isCollapsed=info.isCollapsed
		if inTable and isCollapsed:
			info.expand(textInfos.UNIT_PARAGRAPH)
			isCollapsed=info.isCollapsed
		if not isCollapsed:
			speech.speakTextInfo(info, reason=controlTypes.OutputReason.FOCUS)
		braille.handler.handleCaretMove(self)
		if selectionObj and isCollapsed:
			offset=selectionObj.information(wdHorizontalPositionRelativeToPage)
			msg=self.getLocalizedMeasurementTextForPointSize(offset)
			ui.message(msg)
			if selectionObj.paragraphs[1].range.start==selectionObj.start:
				info.expand(textInfos.UNIT_LINE)
				speech.speakTextInfo(info, unit=textInfos.UNIT_LINE, reason=controlTypes.OutputReason.CARET)

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

	def script_changeLineSpacing(self,gesture):
		if not self.WinwordSelectionObject:
			# We cannot fetch the Word object model, so we therefore cannot report the format change.
			# The object model may be unavailable because this is a pure UIA implementation such as Windows 10 Mail, or its within Windows Defender Application Guard.
			# Eventually UIA will have its own way of detecting format changes at the cursor. For now, just let the gesture through and don't erport anything.
			return gesture.send()
		val=self._WaitForValueChangeForAction(lambda: gesture.send(),lambda:self.WinwordSelectionObject.ParagraphFormat.LineSpacingRule)
		if val == wdLineSpaceSingle:
			# Translators: a message when switching to single line spacing  in Microsoft word
			ui.message(_("Single line spacing"))
		elif val == wdLineSpaceDouble:
			# Translators: a message when switching to double line spacing  in Microsoft word
			ui.message(_("Double line spacing"))
		elif val == wdLineSpace1pt5:
			# Translators: a message when switching to 1.5 line spaceing  in Microsoft word
			ui.message(_("1.5 line spacing"))

	def initOverlayClass(self):
		if isinstance(self, EditableTextWithoutAutoSelectDetection):
			self.bindGesture("kb:alt+shift+home", "caret_changeSelection")
			self.bindGesture("kb:alt+shift+end", "caret_changeSelection")
			self.bindGesture("kb:alt+shift+pageUp", "caret_changeSelection",)
			self.bindGesture("kb:alt+shift+pageDown", "caret_changeSelection",)

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
		"kb:alt+shift+downArrow":"moveParagraphDown",
		"kb:alt+shift+upArrow":"moveParagraphUp",
		"kb:alt+shift+rightArrow":"increaseDecreaseOutlineLevel",
		"kb:alt+shift+leftArrow":"increaseDecreaseOutlineLevel",
		"kb:control+shift+n":"increaseDecreaseOutlineLevel",
		"kb:control+alt+1":"increaseDecreaseOutlineLevel",
		"kb:control+alt+2":"increaseDecreaseOutlineLevel",
		"kb:control+alt+3":"increaseDecreaseOutlineLevel",
		"kb:control+1":"changeLineSpacing",
		"kb:control+2":"changeLineSpacing",
		"kb:control+5":"changeLineSpacing",
		"kb:control+pageUp": "caret_moveByLine",
		"kb:control+pageDown": "caret_moveByLine",
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

class ElementsListDialog(browseMode.ElementsListDialog):

	ELEMENT_TYPES=(browseMode.ElementsListDialog.ELEMENT_TYPES[0],browseMode.ElementsListDialog.ELEMENT_TYPES[1],
		# Translators: The label of a radio button to select the type of element
		# in the browse mode Elements List dialog.
		("annotation", _("&Annotations")),
		# Translators: The label of a radio button to select the type of element
		# in the browse mode Elements List dialog.
		("chart", _("&Charts")),
		# Translators: The label of a radio button to select the type of element
		# in the browse mode Elements List dialog.
		("error", _("&Errors")),
	)
