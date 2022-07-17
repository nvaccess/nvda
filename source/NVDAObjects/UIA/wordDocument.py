# This file is covered by the GNU General Public License.
# A part of NonVisual Desktop Access (NVDA)
# See the file COPYING for more details.
# Copyright (C) 2016-2022 NV Access Limited, Joseph Lee, Jakub Lukowicz

from typing import (
	Optional,
	Dict,
)

import enum
from comtypes import COMError
import winVersion
import mathPres
from scriptHandler import isScriptWaiting
import textInfos
import UIAHandler
import UIAHandler.remote as UIARemote
from logHandler import log
import controlTypes
import ui
import speech
import review
import braille
import browseMode
from UIAHandler.browseMode import (
	UIABrowseModeDocument,
	UIADocumentWithTableNavigation,
	UIATextAttributeQuicknavIterator,
	TextAttribUIATextInfoQuickNavItem
)
from . import UIA, UIATextInfo
from NVDAObjects.window.winword import (
	WordDocument as WordDocumentBase,
	WordDocumentTextInfo as LegacyWordDocumentTextInfo
)
from NVDAObjects import NVDAObject
from scriptHandler import script


"""Support for Microsoft Word via UI Automation."""


class UIACustomAttributeID(enum.IntEnum):
	LINE_NUMBER = 0
	PAGE_NUMBER = 1
	COLUMN_NUMBER = 2
	SECTION_NUMBER = 3
	BOOKMARK_NAME = 4


#: the non-printable unicode character that represents the end of cell or end of row mark in Microsoft Word
END_OF_ROW_MARK = '\x07'


class ElementsListDialog(browseMode.ElementsListDialog):

	ELEMENT_TYPES=(browseMode.ElementsListDialog.ELEMENT_TYPES[0],browseMode.ElementsListDialog.ELEMENT_TYPES[1],
		# Translators: The label of a radio button to select the type of element
		# in the browse mode Elements List dialog.
		("annotation", _("&Annotations")),
		# Translators: The label of a radio button to select the type of element
		# in the browse mode Elements List dialog.
		("error", _("&Errors")),
	)

class RevisionUIATextInfoQuickNavItem(TextAttribUIATextInfoQuickNavItem):
	attribID=UIAHandler.UIA_AnnotationTypesAttributeId
	wantedAttribValues={UIAHandler.AnnotationType_InsertionChange,UIAHandler.AnnotationType_DeletionChange,UIAHandler.AnnotationType_TrackChanges}

	@property
	def label(self):
		text=self.textInfo.text
		if UIAHandler.AnnotationType_InsertionChange in self.attribValues:
			# Translators: The label shown for an insertion change 
			return _(u"insertion: {text}").format(text=text)
		elif UIAHandler.AnnotationType_DeletionChange in self.attribValues:
			# Translators: The label shown for a deletion change 
			return _(u"deletion: {text}").format(text=text)
		else:
			# Translators: The general label shown for track changes 
			return _(u"track change: {text}").format(text=text)

def getCommentInfoFromPosition(position):
	"""
	Fetches information about the comment located at the given position in a word document.
	@param position: a TextInfo representing the span of the comment in the word document.
	@type L{TextInfo}
	@return: A dictionary containing keys of comment, author and date
	@rtype: dict
	"""
	val=position._rangeObj.getAttributeValue(UIAHandler.UIA_AnnotationObjectsAttributeId)
	if not val:
		return
	try:
		UIAElementArray=val.QueryInterface(UIAHandler.IUIAutomationElementArray)
	except COMError:
		return
	for index in range(UIAElementArray.length):
		UIAElement=UIAElementArray.getElement(index)
		UIAElement=UIAElement.buildUpdatedCache(UIAHandler.handler.baseCacheRequest)
		typeID = UIAElement.GetCurrentPropertyValue(UIAHandler.UIA_AnnotationAnnotationTypeIdPropertyId)
		# Use Annotation Type Comment if available
		if typeID == UIAHandler.AnnotationType_Comment:
			comment = UIAElement.GetCurrentPropertyValue(UIAHandler.UIA_NamePropertyId)
			author = UIAElement.GetCurrentPropertyValue(UIAHandler.UIA_AnnotationAuthorPropertyId)
			date = UIAElement.GetCurrentPropertyValue(UIAHandler.UIA_AnnotationDateTimePropertyId)
			return dict(comment=comment, author=author, date=date)
		else:
			obj = UIA(UIAElement=UIAElement)
			if (
				not obj.parent
				# Because the name of this object is language sensetive check if it has UIA Annotation Pattern
				or not obj.parent.UIAElement.getCurrentPropertyValue(
					UIAHandler.UIA_IsAnnotationPatternAvailablePropertyId
				)
			):
				continue
			comment = obj.makeTextInfo(textInfos.POSITION_ALL).text
			tempObj = obj.previous.previous
			authorObj = tempObj or obj.previous
			author = authorObj.name
			if not tempObj:
				return dict(comment=comment, author=author)
			dateObj = obj.previous
			date = dateObj.name
			return dict(comment=comment, author=author, date=date)


def getPresentableCommentInfoFromPosition(commentInfo):
	if "date" not in commentInfo:
		# Translators: The message reported for a comment in Microsoft Word
		return _("Comment: {comment} by {author}").format(**commentInfo)
	# Translators: The message reported for a comment in Microsoft Word
	return _("Comment: {comment} by {author} on {date}").format(**commentInfo)

class CommentUIATextInfoQuickNavItem(TextAttribUIATextInfoQuickNavItem):
	attribID=UIAHandler.UIA_AnnotationTypesAttributeId
	wantedAttribValues={UIAHandler.AnnotationType_Comment,}

	@property
	def label(self):
		commentInfo=getCommentInfoFromPosition(self.textInfo)
		return getPresentableCommentInfoFromPosition(commentInfo)

class WordDocumentTextInfo(UIATextInfo):

	def getMathMl(self, field):
		mathml = field.get('mathml')
		if not mathml:
			raise LookupError("No MathML")
		return mathml

	def _ensureRangeVisibility(self):
		try:
			inView = self.pointAtStart in self.obj.location
		except LookupError:
			inView = False
		if not inView:
			self._rangeObj.ScrollIntoView(True)

	def updateSelection(self):
		# #9611: The document must be scrolled so that the range is visible on screen
		# Otherwise trying to set the selection to the range
		# may cause the selection to remain on the wrong page.
		self._ensureRangeVisibility()
		super().updateSelection()

	def updateCaret(self):
		# #9611: The document must be scrolled so that the range is visible on screen
		# Otherwise trying to set the caret to the range
		# may cause the caret to remain on the wrong page.
		self._ensureRangeVisibility()
		super().updateCaret()

	def _get_locationText(self):
		point = self.pointAtStart
		# UIA has no good way yet to convert coordinates into user-configured distances such as inches or centimetres.
		# Nor can it give us specific distances from the edge of a page.
		# Therefore for now, get the screen coordinates, and if the word object model is available, use our legacy code to get the location text.
		om=self.obj.WinwordWindowObject
		if not om:
			return super(WordDocumentTextInfo,self).locationText
		try:
			r=om.rangeFromPoint(point.x,point.y)
		except (COMError,NameError):
			log.debugWarning("MS Word object model does not support rangeFromPoint")
			return super(WordDocumentTextInfo,self).locationText
		from  NVDAObjects.window.winword import WordDocumentTextInfo as WordObjectModelTextInfo
		i=WordObjectModelTextInfo(self.obj,None,_rangeObj=r)
		return i.locationText

	def _getTextWithFields_text(self,textRange,formatConfig,UIAFormatUnits=None):
		if UIAFormatUnits is None and self.UIAFormatUnits:
			# Word documents must always split by a unit the first time, as an entire text chunk can give valid annotation types 
			UIAFormatUnits=self.UIAFormatUnits
		return super(WordDocumentTextInfo,self)._getTextWithFields_text(textRange,formatConfig,UIAFormatUnits=UIAFormatUnits)

	def _get_controlFieldNVDAObjectClass(self):
		return WordDocumentNode

	def _getControlFieldForUIAObject(self, obj, isEmbedded=False, startOfNode=False, endOfNode=False):
		# Ignore strange editable text fields surrounding most inner fields (links, table cells etc) 
		automationId = obj.UIAAutomationId
		field = super(WordDocumentTextInfo, self)._getControlFieldForUIAObject(
			obj,
			isEmbedded=isEmbedded,
			startOfNode=startOfNode,
			endOfNode=endOfNode
		)
		if automationId.startswith('UIA_AutomationId_Word_Page_'):
			field['page-number'] = automationId.rsplit('_', 1)[-1]
		elif obj.UIAElement.cachedControlType==UIAHandler.UIA_GroupControlTypeId and obj.name:
			field['role']=controlTypes.Role.EMBEDDEDOBJECT
			field['alwaysReportName']=True
		elif obj.role == controlTypes.Role.MATH:
			field['mathml'] = obj.mathMl
		elif obj.UIAElement.cachedControlType==UIAHandler.UIA_CustomControlTypeId and obj.name:
			# Include foot note and endnote identifiers
			field['content']=obj.name
			field['role']=controlTypes.Role.LINK
		if obj.role==controlTypes.Role.LIST or obj.role==controlTypes.Role.EDITABLETEXT:
			field['states'].add(controlTypes.State.READONLY)
			if obj.role==controlTypes.Role.LIST:
				# To stay compatible with the older MS Word implementation, don't expose lists in word documents as actual lists. This suppresses announcement of entering and exiting them.
				# Note that bullets and numbering are still announced of course.
				# Eventually we'll want to stop suppressing this, but for now this is more confusing than good (as in many cases announcing of new bullets when pressing enter causes exit and then enter to be spoken).
				field['role']=controlTypes.Role.EDITABLETEXT
		if obj.role==controlTypes.Role.GRAPHIC:
			# Label graphics with a description before name as name seems to be auto-generated (E.g. "rectangle")
			field['content'] = (
				field.pop('description', None)
				or obj.description
				or field.pop('name', None)
				or obj.name
			)
		# #11430: Read-only tables, such as in the Outlook message viewer
		# should be treated as layout tables,
		# if they have either 1 column or 1 row.
		if (
			obj.appModule.appName == 'outlook'
			and obj.role == controlTypes.Role.TABLE
			and controlTypes.State.READONLY in obj.states
			and (
				obj.rowCount <= 1
				or obj.columnCount <= 1
			)
		):
			field['table-layout'] = True
		return field

	def _getTextFromUIARange(self, textRange):
		t=super(WordDocumentTextInfo,self)._getTextFromUIARange(textRange)
		if t:
			# HTML emails expose a lot of vertical tab chars in their text
			# Really better as carage returns
			t=t.replace('\v','\r')
			# Remove end-of-row markers from the text - they are not useful
			t = t.replace(END_OF_ROW_MARK, '')
		return t

	def _isEndOfRow(self):
		""" Is this textInfo positioned on an end-of-row mark? """
		info=self.copy()
		info.expand(textInfos.UNIT_CHARACTER)
		return info._rangeObj.getText(-1)==u'\u0007'

	def move(self,unit,direction,endPoint=None):
		if endPoint is None:
			res=super(WordDocumentTextInfo,self).move(unit,direction)
			if res==0:
				return 0
			# Skip over end of Row marks
			while self._isEndOfRow():
				if self.move(unit,1 if direction>0 else -1)==0:
					break
			return res
		return super(WordDocumentTextInfo,self).move(unit,direction,endPoint)

	def expand(self,unit):
		super(WordDocumentTextInfo,self).expand(unit)
		# #7970: MS Word refuses to expand to line when on the final line and it is blank.
		# This among other things causes a newly inserted bullet not to be spoken or brailled.
		# Therefore work around this by detecting if the expand to line failed, and moving the end of the range to the end of the document manually.
		if  self.isCollapsed:
			if self.move(unit,1,endPoint="end")==0:
				docInfo=self.obj.makeTextInfo(textInfos.POSITION_ALL)
				self.setEndPoint(docInfo,"endToEnd")

	# C901 'getTextWithFields' is too complex
	# Note: when working on getTextWithFields, look for opportunities to simplify
	# and move logic out into smaller helper functions.
	def getTextWithFields(  # noqa: C901
		self,
		formatConfig: Optional[Dict] = None
	) -> textInfos.TextInfo.TextWithFieldsT:
		fields = None
		# #11043: when a non-collapsed text range is positioned within a blank table cell
		# MS Word does not return the table  cell as an enclosing element,
		# Thus NVDa thinks the range is not inside the cell.
		# This can be detected by asking for the first 2 characters of the range's text,
		# Which will either be an empty string, or the single end-of-row mark.
		# Anything else means it is not on an empty table cell,
		# or the range really does span more than the cell itself.
		# If this situation is detected,
		# copy and collapse the range, and fetch the content from that instead,
		# As a collapsed range on an empty cell does correctly return the table cell as its first enclosing element.
		if not self.isCollapsed:
			rawText = self._rangeObj.GetText(2)
			if not rawText or rawText == END_OF_ROW_MARK:
				r = self.copy()
				r.end = r.start
				fields = super(WordDocumentTextInfo, r).getTextWithFields(formatConfig=formatConfig)
		if fields is None:
			fields = super().getTextWithFields(formatConfig=formatConfig)
		if len(fields)==0: 
			# Nothing to do... was probably a collapsed range.
			return fields

		# MS Word tries to produce speakable math content within equations.
		# However, using mathPlayer with the exposed mathml property on the equation is much nicer.
		# But, we therefore need to remove the inner math content if reading by line
		if not formatConfig or not formatConfig.get('extraDetail'):
			# We really only want to remove content if we can guarantee that mathPlayer is available.
			if mathPres.speechProvider or mathPres.brailleProvider:
				curLevel = 0
				mathLevel = None
				mathStartIndex = None
				mathEndIndex = None
				for index in range(len(fields)):
					field = fields[index]
					if isinstance(field, textInfos.FieldCommand) and field.command == "controlStart":
						curLevel += 1
						if mathLevel is None and field.field.get('mathml'):
							mathLevel = curLevel
							mathStartIndex = index
					elif isinstance(field, textInfos.FieldCommand) and field.command == "controlEnd":
						if curLevel == mathLevel:
							mathEndIndex = index
						curLevel -= 1
				if mathEndIndex is not None:
					del fields[mathStartIndex + 1:mathEndIndex]

		# Sometimes embedded objects and graphics In MS Word can cause a controlStart then a controlEnd with no actual formatChange / text in the middle.
		# SpeakTextInfo always expects that the first lot of controlStarts will always contain some text.
		# Therefore ensure that the first lot of controlStarts does contain some text by inserting a blank formatChange and empty string in this case.
		for index in range(len(fields)):
			field=fields[index]
			if isinstance(field,textInfos.FieldCommand) and field.command=="controlStart":
				continue
			elif isinstance(field,textInfos.FieldCommand) and field.command=="controlEnd":
				formatChange=textInfos.FieldCommand("formatChange",textInfos.FormatField())
				fields.insert(index,formatChange)
				fields.insert(index+1,"")
			break
		##7971: Microsoft Word exposes list bullets as part of the actual text.
		# This then confuses NVDA's braille cursor routing as it expects that there is a one-to-one mapping between characters in the text string and   unit character moves.
		# Therefore, detect when at the start of a list, and strip the bullet from the text string, placing it in the text's formatField as line-prefix.
		listItemStarted=False
		lastFormatField=None
		for index in range(len(fields)):
			field=fields[index]
			if isinstance(field,textInfos.FieldCommand) and field.command=="controlStart":
				if field.field.get('role')==controlTypes.Role.LISTITEM and field.field.get('_startOfNode'):
					# We are in the start of a list item.
					listItemStarted=True
			elif isinstance(field,textInfos.FieldCommand) and field.command=="formatChange":
				# This is the most recent formatField we have seen.
				lastFormatField=field.field
			elif listItemStarted and isinstance(field,str):
				# This is the first text string within the list.
				# Remove the text up to the first space, and store it as line-prefix which NVDA will appropriately speak/braille as a bullet.
				try:
					spaceIndex=field.index(' ')
				except ValueError:
					log.debugWarning("No space found in this text string")
					break
				prefix=field[0:spaceIndex]
				fields[index]=field[spaceIndex+1:]
				lastFormatField['line-prefix']=prefix
				# Let speech know that line-prefix is safe to be spoken always, as it will only be exposed on the very first formatField on the list item.
				lastFormatField['line-prefix_speakAlways']=True
				break
			else:
				# Not a controlStart, formatChange or text string. Nothing to do.
				break
		# Fill in page number attributes where NVDA expects
		try:
			page=fields[0].field['page-number']
		except KeyError:
			page=None
		if page is not None:
			for field in fields:
				if isinstance(field,textInfos.FieldCommand) and isinstance(field.field,textInfos.FormatField):
					field.field['page-number']=page
		# MS Word can sometimes return a higher ancestor in its textRange's children.
		# E.g. a table inside a table header.
		# This does not cause a loop, but does cause information to be doubled
		# Detect these duplicates and remove them from the generated fields.
		seenStarts=set()
		pendingRemoves=[]
		index=0
		for index,field in enumerate(fields):
			if isinstance(field,textInfos.FieldCommand) and field.command=="controlStart":
				runtimeID=field.field['runtimeID']
				if not runtimeID:
					continue
				if runtimeID in seenStarts:
					pendingRemoves.append(field.field)
				else:
					seenStarts.add(runtimeID)
			elif seenStarts:
				seenStarts.clear()
		index=0
		while index<len(fields):
			field=fields[index]
			if isinstance(field,textInfos.FieldCommand) and any(x is field.field for x in pendingRemoves):
				del fields[index]
			else:
				index+=1
		return fields

	def _getFormatFieldAtRange(self, textRange, formatConfig, ignoreMixedValues=False):
		formatField = super()._getFormatFieldAtRange(textRange, formatConfig, ignoreMixedValues=ignoreMixedValues)
		if not formatField:
			return formatField
		if winVersion.getWinVer() >= winVersion.WIN11:
			docElement = self.obj.UIAElement
			if formatConfig['reportLineNumber']:
				lineNumber = UIARemote.msWord_getCustomAttributeValue(
					docElement, textRange, UIACustomAttributeID.LINE_NUMBER
				)
				if isinstance(lineNumber, int):
					formatField.field['line-number'] = lineNumber
			if formatConfig['reportPage']:
				sectionNumber = UIARemote.msWord_getCustomAttributeValue(
					docElement, textRange, UIACustomAttributeID.SECTION_NUMBER
				)
				if isinstance(sectionNumber, int):
					formatField.field['section-number'] = sectionNumber
				if False:
					# #13511: Fetching of text-column-number is disabled
					# as it causes Microsoft Word 16.0.1493 and newer to crash!!
					# This should only be reenabled for versions identified not to crash.
					textColumnNumber = UIARemote.msWord_getCustomAttributeValue(
						docElement, textRange, UIACustomAttributeID.COLUMN_NUMBER
					)
					if isinstance(textColumnNumber, int):
						formatField.field['text-column-number'] = textColumnNumber
		return formatField


class WordBrowseModeDocument(UIABrowseModeDocument):

	def _shouldSetFocusToObj(self, obj: NVDAObject) -> bool:
		# Ignore strange editable text fields surrounding most inner fields (links, table cells etc) 
		if (
			obj.role == controlTypes.Role.EDITABLETEXT
			and obj.UIAAutomationId.startswith('UIA_AutomationId_Word_Content')
		):
			return False
		elif obj.role == controlTypes.Role.MATH:
			# Don't set focus to math equations otherwise they cannot be interacted  with mathPlayer.
			return False
		return super()._shouldSetFocusToObj(obj)

	def shouldPassThrough(self,obj,reason=None):
		# Ignore strange editable text fields surrounding most inner fields (links, table cells etc) 
		if (
			obj.role == controlTypes.Role.EDITABLETEXT
			and obj.UIAAutomationId.startswith('UIA_AutomationId_Word_Content')
		):
			return False
		elif obj.role == controlTypes.Role.MATH:
			# Don't  activate focus mode for math equations otherwise they cannot be interacted  with mathPlayer.
			return False
		return super(WordBrowseModeDocument,self).shouldPassThrough(obj,reason=reason)

	def script_tab(self,gesture):
		oldBookmark=self.rootNVDAObject.makeTextInfo(textInfos.POSITION_SELECTION).bookmark
		gesture.send()
		noTimeout,newInfo=self.rootNVDAObject._hasCaretMoved(oldBookmark,timeout=1)
		if not newInfo:
			return
		info=self.makeTextInfo(textInfos.POSITION_SELECTION)
		if not info.isCollapsed:
			speech.speakTextInfo(info, reason=controlTypes.OutputReason.FOCUS)
	script_shiftTab=script_tab

	def _iterNodesByType(self,nodeType,direction="next",pos=None):
		if nodeType=="annotation":
			comments=UIATextAttributeQuicknavIterator(CommentUIATextInfoQuickNavItem,nodeType,self,pos,direction=direction)
			revisions=UIATextAttributeQuicknavIterator(RevisionUIATextInfoQuickNavItem,nodeType,self,pos,direction=direction)
			return browseMode.mergeQuickNavItemIterators([comments,revisions],direction)
		return super(WordBrowseModeDocument,self)._iterNodesByType(nodeType,direction=direction,pos=pos)

	ElementsListDialog=ElementsListDialog

class WordDocumentNode(UIA):
	TextInfo=WordDocumentTextInfo

	def _get_mathMl(self):
		try:
			return self._getUIACacheablePropertyValue(self._UIACustomProps.word_mathml.id)
		except COMError:
			pass
		return None

	def _get_role(self):
		if self.mathMl:
			return controlTypes.Role.MATH
		role=super(WordDocumentNode,self).role
		# Footnote / endnote elements currently have a role of unknown. Force them to editableText so that theyr text is presented correctly
		if role==controlTypes.Role.UNKNOWN:
			role=controlTypes.Role.EDITABLETEXT
		return role

class WordDocument(UIADocumentWithTableNavigation,WordDocumentNode,WordDocumentBase):
	treeInterceptorClass=WordBrowseModeDocument
	shouldCreateTreeInterceptor=False
	announceEntireNewLine=True

	# Microsoft Word duplicates the full title of the document on this control, which is redundant as it appears in the title of the app itself.
	name=u""

	def event_textChange(self):
		# Ensure Braille is updated when text changes,
		# As Microsoft Word does not fire caret events when typing text, even though the caret does move.
		braille.handler.handleCaretMove(self)

	def event_UIA_notification(self, activityId=None, **kwargs):
		# #10851: in recent Word 365 releases, UIA notification will cause NVDA to announce edit functions
		# such as "delete back word" when Control+Backspace is pressed.
		if activityId == "AccSN2":  # Delete activity ID
			return
		super(WordDocument, self).event_UIA_notification(**kwargs)

	# The following overide of the EditableText._caretMoveBySentenceHelper private method
	# Falls back to the MS Word object model if available.
	# This override should be removed as soon as UI Automation in MS Word has the ability to move by sentence.
	def _caretMoveBySentenceHelper(self, gesture, direction):
		if isScriptWaiting():
			return
		if not self.WinwordSelectionObject:
			# Legacy object model not available.
			# Translators: a message when navigating by sentence is unavailable in MS Word
			ui.message(_("Navigating by sentence not supported in this document"))
			gesture.send()
			return
		# Using the legacy object model,
		# Move the caret to the next sentence in the requested direction.
		legacyInfo = LegacyWordDocumentTextInfo(self, textInfos.POSITION_CARET)
		legacyInfo.move(textInfos.UNIT_SENTENCE, direction)
		# Save the start of the sentence for future use
		legacyStart = legacyInfo.copy()
		# With the legacy object model,
		# Move the caret to the end of the new sentence.
		legacyInfo.move(textInfos.UNIT_SENTENCE, 1)
		legacyInfo.updateCaret()
		# Fetch the caret position (end of the next sentence) with UI automation.
		endInfo = self.makeTextInfo(textInfos.POSITION_CARET)
		# Move the caret back to the start of the next sentence,
		# where it should be left for the user.
		legacyStart.updateCaret()
		# Fetch the new caret position (start of the next sentence) with UI Automation.
		startInfo = self.makeTextInfo(textInfos.POSITION_CARET)
		# Make a UI automation text range spanning the entire next sentence.
		info = startInfo.copy()
		info.end = endInfo.end
		# Speak the sentence moved to
		speech.speakTextInfo(info, unit=textInfos.UNIT_SENTENCE, reason=controlTypes.OutputReason.CARET)
		# Forget the word currently being typed as the user has moved the caret somewhere else.
		speech.clearTypedWordBuffer()
		# Alert review and braille the caret has moved to its new position
		review.handleCaretMove(info)
		braille.handler.handleCaretMove(self)

	@script(
		gesture="kb:NVDA+alt+c",
		# Translators: a description for a script that reports the comment at the caret.
		description=_("Reports the text of the comment where the System caret is located.")
	)
	def script_reportCurrentComment(self,gesture):
		caretInfo=self.makeTextInfo(textInfos.POSITION_CARET)
		commentInfo = getCommentInfoFromPosition(caretInfo)
		if commentInfo is not None:
			ui.message(getPresentableCommentInfoFromPosition(commentInfo))
		else:
			# Translators: a message when there is no comment to report in Microsoft Word
			ui.message(_("No comments"))
		return
