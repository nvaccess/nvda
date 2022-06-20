# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2016-2021 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
from typing import (
	Optional,
	Dict,
)

from comtypes import COMError
from comtypes.hresult import S_OK
import appModuleHandler
import speech
import textUtils
from speech import sayAll
import api
from scriptHandler import willSayAllResume, isScriptWaiting
import controlTypes
from controlTypes import OutputReason
import treeInterceptorHandler
from cursorManager import ReviewCursorManager
import browseMode
from browseMode import BrowseModeDocumentTreeInterceptor
import textInfos
from speech.types import SpeechSequence
from textInfos import DocumentWithPageTurns
from NVDAObjects.IAccessible import IAccessible
from globalCommands import SCRCAT_SYSTEMCARET
from NVDAObjects.IAccessible.ia2TextMozilla import MozillaCompoundTextInfo
from comInterfaces import IAccessible2Lib as IA2
import winUser
import mouseHandler
from logHandler import log
import ui
import config

class ElementsListDialog(browseMode.ElementsListDialog):
	ELEMENT_TYPES = (
		browseMode.ElementsListDialog.ELEMENT_TYPES[0], # Links
	)

class BookPageViewTreeInterceptor(DocumentWithPageTurns,ReviewCursorManager,BrowseModeDocumentTreeInterceptor):
	ElementsListDialog = ElementsListDialog
	TextInfo=treeInterceptorHandler.RootProxyTextInfo
	pageChangeAlreadyHandled = False

	def turnPage(self,previous=False):
		self.rootNVDAObject.turnPage(previous=previous)
		# turnPage waits for a pageChange event before returning,
		# but the pageChange event will still get fired.
		# We need to know that we've already handled it.
		self.pageChangeAlreadyHandled=True

	def event_pageChange(self, obj, nextHandler):
		if self.pageChangeAlreadyHandled:
			# This page change has already been handled.
			self.pageChangeAlreadyHandled = False
			return
		info = self.makeTextInfo(textInfos.POSITION_FIRST)
		self.selection = info
		if not self.rootNVDAObject.hasFocus:
			# Don't report anything if the book area isn't focused.
			return
		info.expand(textInfos.UNIT_LINE)
		speech.speakTextInfo(info, unit=textInfos.UNIT_LINE, reason=OutputReason.CARET)

	def isAlive(self):
		return winUser.isWindow(self.rootNVDAObject.windowHandle)

	def __contains__(self,obj):
		return obj==self.rootNVDAObject

	def _getTableCellAt(self,tableID,startPos,destRow,destCol):
		""" Override of documentBase.DocumentWithTableNavigation._getTableCellAt."""
		# Locate the table in the object ancestry of the given document position. 
		obj=startPos.NVDAObjectAtStart
		while not obj.table and obj!=startPos.obj.rootNVDAObject:
			obj=obj.parent
		if not obj.table:
			# No table could be found
			raise LookupError
		table = obj.table
		try:
			cell = table.IAccessibleTable2Object.cellAt(
				destRow - 1, destCol - 1
			).QueryInterface(IA2.IAccessible2)
			cell = IAccessible(IAccessibleObject=cell, IAccessibleChildID=0)
			# If the cell we fetched is marked as hidden, raise LookupError which will instruct calling code to try an adjacent cell instead.
			if cell.IA2Attributes.get('hidden'):
				raise LookupError("Found hidden cell") 
			# Return the position of the found cell
			return self.makeTextInfo(cell)
		except (COMError, RuntimeError):
			# Any of the above calls could throw a COMError, and sometimes a RuntimeError.
			# Treet this as the cell not existing.
			raise LookupError

	def _changePageScriptHelper(self,gesture,previous=False):
		if isScriptWaiting():
			return
		try:
			self.turnPage(previous=previous)
		except RuntimeError:
			return
		info=self.makeTextInfo(textInfos.POSITION_FIRST)
		self.selection=info
		info.expand(textInfos.UNIT_LINE)
		if not willSayAllResume(gesture):
			speech.speakTextInfo(info, unit=textInfos.UNIT_LINE, reason=OutputReason.CARET)

	def script_moveByPage_forward(self,gesture):
		self._changePageScriptHelper(gesture)
	script_moveByPage_forward.resumeSayAllMode = sayAll.CURSOR.CARET

	def script_moveByPage_back(self,gesture):
		self._changePageScriptHelper(gesture,previous=True)
	script_moveByPage_back.resumeSayAllMode = sayAll.CURSOR.CARET

	def _tabOverride(self,direction):
		return False

	def script_showSelectionOptions(self, gesture):
		fakeSel = self.selection
		if fakeSel.isCollapsed:
			# Double click to access the toolbar; e.g. for annotations.
			try:
				p = fakeSel.pointAtStart
			except NotImplementedError:
				log.debugWarning("Couldn't get point to click")
				return
			log.debug("Double clicking")
			winUser.setCursorPos(p.x, p.y)
			mouseHandler.doPrimaryClick()
			mouseHandler.doPrimaryClick()
			return

		# The user makes a selection using browse mode virtual selection.
		# Update the selection in Kindle.
		# This will cause the options to appear.
		fakeSel.innerTextInfo.updateSelection()
		# The selection might have been adjusted to meet word boundaries,
		# so retrieve and report the selection from Kindle.
		# we can't just use self.makeTextInfo, as that will use our fake selection.
		realSel = self.rootNVDAObject.makeTextInfo(textInfos.POSITION_SELECTION)
		speech.speakTextSelected(realSel.text)
		# Remove our virtual selection and move the caret to the active end.
		fakeSel.innerTextInfo = realSel
		fakeSel.collapse(end=not self._lastSelectionMovedStart)
		self.selection = fakeSel
	# Translators: Describes a command.
	script_showSelectionOptions.__doc__ = _("Shows options related to selected text or text at the cursor")
	script_showSelectionOptions.category = SCRCAT_SYSTEMCARET

	__gestures = {
		"kb:control+c": "showSelectionOptions",
		"kb:applications": "showSelectionOptions",
		"kb:shift+f10": "showSelectionOptions",
	}

	def _iterEmbeddedObjs(self, hypertext, startIndex, direction):
		"""Recursively iterate through all embedded objects in a given direction starting at a given hyperlink index.
		"""
		log.debug("Starting at hyperlink index %d" % startIndex)
		for index in range(startIndex, hypertext.nHyperlinks if direction == "next" else -1, 1 if direction == "next" else -1):
			hl = hypertext.hyperlink(index)
			obj = IAccessible(IAccessibleObject=hl.QueryInterface(IA2.IAccessible2), IAccessibleChildID=0)
			log.debug("Yielding object at index %d" % index)
			yield obj
			try:
				objHt = obj.iaHypertext
			except:
				# This is a graphic, etc. which doesn't support text.
				continue
			log.debug("Object has hypertext. Recursing")
			for subObj in self._iterEmbeddedObjs(objHt, 0 if direction == "next" else objHt.nHyperlinks - 1, direction):
				yield subObj

	NODE_TYPES_TO_ROLES = {
		"link": {controlTypes.Role.LINK, controlTypes.Role.FOOTNOTE},
		"graphic": {controlTypes.Role.GRAPHIC},
		"table": {controlTypes.Role.TABLE},
	}

	def _iterNodesByType(self, nodeType, direction="next", pos=None):
		if not pos:
			pos = self.makeTextInfo(textInfos.POSITION_FIRST if direction == "next" else textInfos.POSITION_LAST)
		obj = pos.innerTextInfo._startObj
		if nodeType=="container":
			while obj!=self.rootNVDAObject:
				if obj.role==controlTypes.Role.TABLE:
					ti=self.makeTextInfo(obj)
					yield browseMode.TextInfoQuickNavItem(nodeType, self, ti)
					return
				obj=obj.parent
			return
		roles = self.NODE_TYPES_TO_ROLES.get(nodeType)
		if not roles:
			raise NotImplementedError
		# Find the first embedded object in the requested direction.
		# Use the text, as enumerating IAccessibleHypertext means more cross-process calls.
		offset = pos.innerTextInfo._start._startOffset
		if direction == "next":
			text = obj.IAccessibleTextObject.text(offset + 1, obj.IAccessibleTextObject.nCharacters)
			embed = text.find(textUtils.OBJ_REPLACEMENT_CHAR)
			if embed != -1:
				embed += offset + 1
		else:
			if offset > 0:
				text = obj.IAccessibleTextObject.text(0, offset)
				embed = text.rfind(textUtils.OBJ_REPLACEMENT_CHAR)
			else:
				# We're at the start; we can't go back any further.
				embed = -1
		log.debug("%s embedded object from offset %d: %d" % (direction, offset, embed))
		hli = -1 if embed == -1 else obj.iaHypertext.hyperlinkIndex(embed)
		while True:
			if hli != -1:
				for embObj in self._iterEmbeddedObjs(obj.iaHypertext, hli, direction):
					if embObj.role in roles:
						ti = self.makeTextInfo(embObj)
						yield browseMode.TextInfoQuickNavItem(nodeType, self, ti)
			# No more embedded objects here.
			# We started in an embedded object, so continue in the parent.
			if obj == self.rootNVDAObject:
				log.debug("At root, stopping")
				break # Can't go any further.
			log.debug("Continuing in parent")
			# Get the index of the embedded object we just came from.
			parent = obj.parent
			if not getattr(parent,'IAccessibleTextObject',None):
				obj=parent
				continue
			hl = obj.IAccessibleObject.QueryInterface(IA2.IAccessibleHyperlink)
			offset = hl.startIndex
			obj=parent
			hli = obj.iaHypertext.hyperlinkIndex(offset)
			# Continue the walk from the next embedded object.
			hli += 1 if direction == "next" else -1

	def script_find(self, gesture):
		# Translators: Reported when a user tries to use a find command when it isn't supported.
		ui.message(_("Not supported in this document"))

	def script_findNext(self, gesture):
		# Translators: Reported when a user tries to use a find command when it isn't supported.
		ui.message(_("Not supported in this document"))

	def script_findPrevious(self, gesture):
		# Translators: Reported when a user tries to use a find command when it isn't supported.
		ui.message(_("Not supported in this document"))

class BookPageViewTextInfo(MozillaCompoundTextInfo):

	def _get_locationText(self):
		curLocation=self.obj.IA2Attributes.get('kindle-first-visible-location-number')
		maxLocation=self.obj.IA2Attributes.get('kindle-max-location-number')
		pageNumber=self.obj.pageNumber
		# Translators: A position in a Kindle book
		# xgettext:no-python-format
		text=_("{bookPercentage}%, location {curLocation} of {maxLocation}").format(bookPercentage=int((float(curLocation)/float(maxLocation))*100),curLocation=curLocation,maxLocation=maxLocation)
		if pageNumber:
			# Translators: a page in a Kindle book
			text+=", "+_("Page {pageNumber}").format(pageNumber=pageNumber)
		return text

	def getTextWithFields(self, formatConfig: Optional[Dict] = None) -> textInfos.TextInfo.TextWithFieldsT:
		if not formatConfig:
			formatConfig = config.conf["documentFormatting"]
		items = super(BookPageViewTextInfo, self).getTextWithFields(formatConfig=formatConfig)
		for item in items:
			if isinstance(item, textInfos.FieldCommand) and item.command == "formatChange":
				if formatConfig['reportPage']:
					item.field['page-number'] = self.obj.pageNumber
			elif (isinstance(item, textInfos.FieldCommand) and item.command == "controlStart"
					and item.field.get("mathMl")):
				# We have MathML, so don't report alt text (if any) as content.
				item.field.pop("content", None)
		return items

	def getFormatFieldSpeech(
			self,
			attrs: textInfos.Field,
			attrsCache: Optional[textInfos.Field] = None,
			formatConfig: Optional[Dict[str, bool]] = None,
			reason: Optional[OutputReason] = None,
			unit: Optional[str] = None,
			extraDetail: bool = False,
			initialFormat: bool = False
	) -> SpeechSequence:
		out: SpeechSequence = []
		comment = attrs.get("kindle-user-note")
		if comment:
			# For now, we report this the same way we do comments.
			attrs["comment"] = comment
		highlight = attrs.get("kindle-highlight")
		oldHighlight = attrsCache.get("kindle-highlight") if attrsCache is not None else None
		if oldHighlight != highlight:
			translation = (
				# Translators: Reported when text is highlighted.
				_("highlight") if highlight else
				# Translators: Reported when text is not highlighted.
				_("no highlight")
			)
			out.append(translation)
		popular = attrs.get("kindle-popular-highlight-count")
		oldPopular = attrsCache.get("kindle-popular-highlight-count") if attrsCache is not None else None
		if oldPopular != popular:
			translation = (
				# Translators: Reported in Kindle when text has been identified as a popular highlight;
				# i.e. it has been highlighted by several people.
				# %s is replaced with the number of people who have highlighted this text.
				_("%s highlighted") % popular if popular else
				# Translators: Reported when moving out of a popular highlight.
				_("out of popular highlight")
			)
			out.append(translation)

		superSpeech = super(BookPageViewTextInfo, self).getFormatFieldSpeech(
			attrs,
			attrsCache=attrsCache,
			formatConfig=formatConfig,
			reason=reason,
			unit=unit,
			extraDetail=extraDetail,
			initialFormat=initialFormat
		)
		out.extend(superSpeech)
		textInfos._logBadSequenceTypes(out)
		return out

	def updateSelection(self):
		# hack: For now, we need to do all selection on the root.
		# This means only entire embedded objects can be selected.
		if self._startObj == self.obj:
			sel = self._start.copy()
		else:
			log.debug("Start object isn't root, getting embedding")
			sel = self._getEmbedding(self._startObj)
			assert sel.obj == self.obj
		if self._endObj == self.obj:
			end = self._end
		else:
			log.debug("End object isn't root, getting embedding")
			end = self._getEmbedding(self._endObj)
			assert end.obj == self.obj
		sel.setEndPoint(end, "endToEnd")
		log.debug("Setting selection to (%d, %d)" % (sel._startOffset, sel._endOffset))
		sel.updateSelection()

	def _getControlFieldForObject(self, obj, ignoreEditableText=True):
		field = super(BookPageViewTextInfo, self)._getControlFieldForObject(obj, ignoreEditableText=ignoreEditableText)
		if field and field["role"] == controlTypes.Role.MATH:
			try:
				field["mathMl"] = obj.mathMl
			except LookupError:
				pass
		return field

	def getMathMl(self, field):
		mathMl = field.get("mathMl")
		if not mathMl:
			raise LookupError("No mathml attribute")
		return mathMl

class BookPageView(DocumentWithPageTurns,IAccessible):
	"""Allows navigating page text content with the arrow keys."""

	treeInterceptorClass=BookPageViewTreeInterceptor
	TextInfo=BookPageViewTextInfo

	def _get_pageNumber(self):
		try:
			first=self.IA2Attributes['kindle-first-visible-physical-page-label']
			last=self.IA2Attributes['kindle-last-visible-physical-page-label']
		except KeyError:
			try:
				first=self.IA2Attributes['kindle-first-visible-physical-page-number']
				last=self.IA2Attributes['kindle-last-visible-physical-page-number']
			except KeyError:
				return None
		if first!=last:
			return "%s to %s"%(first,last)
		else:
			return first

	def turnPage(self,previous=False):
		if self.IAccessibleActionObject.doAction(1 if previous else 0) != S_OK:
			raise RuntimeError("no more pages")
		self.invalidateCache()

class PageTurnFocusIgnorer(IAccessible):

	def _get_shouldAllowIAccessibleFocusEvent(self):
		# hack: When turning pages to a new section, Kindle  fires focus on the new section in the table of contents treeview.
		# We must ignore this focus event as it is a hinderance to a screen reader user while reading the book.
		focus = api.getFocusObject()
		if isinstance(focus, BookPageView) and focus.hasFocus:
			# The book area reports that it still has the focus, so this event is bogus.
			return False
		return super(PageTurnFocusIgnorer,self).shouldAllowIAccessibleFocusEvent

class Math(IAccessible):

	def _get_mathMl(self):
		mathMl = self.IA2Attributes.get("mathml")
		if not mathMl:
			raise LookupError
		return mathMl

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		if isinstance(obj,IAccessible):
			clsList.insert(0,PageTurnFocusIgnorer)
			if (
				(
					isinstance(obj.IAccessibleObject, IA2.IAccessible2)
					and obj.IA2Attributes.get("class") == "KindleBookPageView"
				)
				# We must rely on .name in Kindle <= 1.19.
				or (hasattr(obj,'IAccessibleTextObject') and obj.name=="Book Page View")
			):
				clsList.insert(0,BookPageView)
			elif obj.role == controlTypes.Role.MATH:
				clsList.insert(0, Math)
		return clsList

	def event_NVDAObject_init(self, obj):
		if (
			isinstance(obj, IAccessible)
			and isinstance(obj.IAccessibleObject, IA2.IAccessible2)
			and obj.role == controlTypes.Role.LINK
		):
			xRoles = obj.IA2Attributes.get("xml-roles", "").split(" ")
			if "kindle-footnoteref" in xRoles:
				obj.role = controlTypes.Role.FOOTNOTE
