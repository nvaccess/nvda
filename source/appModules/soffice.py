# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2006-2022 NV Access Limited, Bill Dengler, Leonard de Ruijter

from typing import (
	Optional,
	Union,
)

from comtypes import COMError
import comtypes.client
import oleacc
import time
from IAccessibleHandler import IA2, splitIA2Attribs
import appModuleHandler
import controlTypes
from controlTypes import TextPosition
import textInfos
import colors
from compoundDocuments import CompoundDocument, TreeCompoundTextInfo
from NVDAObjects import NVDAObject
from NVDAObjects.IAccessible import IAccessible, IA2TextTextInfo
from NVDAObjects.behaviors import EditableText
from logHandler import log
from scriptHandler import script
import speech
import api
import braille
import inputCore
import keyboardHandler
import languageHandler
import ui
import vision


class SymphonyUtils:
	"""Helper class providing utility methods."""

	@staticmethod
	def is_toolbar_item(obj: NVDAObject) -> bool:
		"""Whether the given object is part of a toolbar."""
		parent = obj.parent
		while parent:
			if parent.role == controlTypes.Role.TOOLBAR:
				return True
			parent = parent.parent
		return False

	@staticmethod
	def get_id(obj: NVDAObject) -> str | None:
		"""Get value of the "id" object attribute, if set."""
		if not hasattr(obj, "IA2Attributes"):
			return None
		return obj.IA2Attributes.get("id")


class SymphonyTextInfo(IA2TextTextInfo):
	# C901 '_getFormatFieldFromLegacyAttributesString' is too complex
	# Note: when working on _getFormatFieldFromLegacyAttributesString, look for opportunities to simplify
	# and move logic out into smaller helper functions.
	# This is legacy code, kept for compatibility reasons.
	def _getFormatFieldFromLegacyAttributesString(  # noqa: C901
		self,
		attribsString: str,
		offset: int,
	) -> textInfos.FormatField:
		"""Get format field with information retrieved from a text
		attributes string containing LibreOffice's legacy custom text
		attributes (used by LibreOffice <= 7.6), instead of attributes
		according to the IAccessible2 text attributes specification
		(used by LibreOffice >= 24.2).

		:param attribsString: Legacy text attributes string.
		:param offset: Character offset for which to retrieve the
		                           attributes.
		:return: Format field containing the text attribute information.
		"""
		formatField = textInfos.FormatField()
		if attribsString:
			formatField.update(splitIA2Attribs(attribsString))

		try:
			escapement = int(formatField["CharEscapement"])
			if escapement < 0:
				formatField["text-position"] = TextPosition.SUBSCRIPT
			elif escapement > 0:
				formatField["text-position"] = TextPosition.SUPERSCRIPT
			else:
				formatField["text-position"] = TextPosition.BASELINE
		except KeyError:
			pass
		try:
			formatField["font-name"] = formatField["CharFontName"]
		except KeyError:
			pass
		try:
			# Translators: Abbreviation for points, a measurement of font size.
			formatField["font-size"] = pgettext("font size", "%s pt") % formatField["CharHeight"]
		except KeyError:
			pass
		try:
			formatField["italic"] = formatField["CharPosture"] == "2"
		except KeyError:
			pass
		try:
			formatField["strikethrough"] = formatField["CharStrikeout"] == "1"
		except KeyError:
			pass
		try:
			underline = formatField["CharUnderline"]
			if underline == "10":
				# Symphony doesn't provide for semantic communication of spelling errors, so we have to rely on the WAVE underline type.
				formatField["invalid-spelling"] = True
			else:
				formatField["underline"] = underline != "0"
		except KeyError:
			pass
		try:
			formatField["bold"] = float(formatField["CharWeight"]) > 100
		except KeyError:
			pass
		try:
			color = formatField.pop("CharColor")
		except KeyError:
			color = None
		if color:
			formatField["color"] = colors.RGB.fromString(color)
		try:
			backgroundColor = formatField.pop("CharBackColor")
		except KeyError:
			backgroundColor = None
		if backgroundColor:
			formatField["background-color"] = colors.RGB.fromString(backgroundColor)

		if offset == 0:
			# Only include the list item prefix on the first line of the paragraph.
			numbering = formatField.get("Numbering")
			if numbering:
				formatField["line-prefix"] = numbering.get("NumberingPrefix") or numbering.get("BulletChar")

		return formatField

	def _getFormatFieldAndOffsetsFromAttributes(
		self,
		offset: int,
		formatConfig: Optional[dict],
		calculateOffsets: bool,
	) -> tuple[textInfos.FormatField, tuple[int, int]]:
		"""Get format field and offset information from either
		attributes according to the IAccessible2 specification
		(for LibreOffice >= 24.2) or from legacy custom
		text attributes (used by LibreOffice <= 7.6 and Apache OpenOffice).
		:param offset: Character offset for which to retrieve the
		                           attributes.
		:param formatConfig: Format configuration.
		:param calculateOffsets: Whether to calculate offsets.
		:return: Format field containing the text attribute information
				 and start and end offset of the attribute run.
		"""
		obj = self.obj
		try:
			startOffset, endOffset, attribsString = obj.IAccessibleTextObject.attributes(offset)
		except COMError:
			log.debugWarning("could not get attributes", exc_info=True)
			return textInfos.FormatField(), (self._startOffset, self._endOffset)

		if not attribsString and offset > 0:
			try:
				attribsString = obj.IAccessibleTextObject.attributes(offset - 1)[2]
			except COMError:
				pass

		# LibreOffice >= 24.2 uses IAccessible2 text attributes, earlier versions use
		# custom attributes, with the attributes string starting with "Version:1;"
		if attribsString and attribsString.startswith("Version:1;"):
			formatField = self._getFormatFieldFromLegacyAttributesString(
				attribsString,
				offset,
			)
		else:
			formatField, (startOffset, endOffset) = super()._getFormatFieldAndOffsets(
				offset,
				formatConfig,
				calculateOffsets,
			)

		return formatField, (startOffset, endOffset)

	def _getFormatFieldAndOffsets(
		self,
		offset: int,
		formatConfig: Optional[dict],
		calculateOffsets: bool = True,
	) -> tuple[textInfos.FormatField, tuple[int, int]]:
		formatField, (startOffset, endOffset) = self._getFormatFieldAndOffsetsFromAttributes(
			offset,
			formatConfig,
			calculateOffsets,
		)
		obj = self.obj

		# optimisation: Assume a hyperlink occupies a full attribute run.
		try:
			if (
				obj.IAccessibleTextObject.QueryInterface(
					IA2.IAccessibleHypertext,
				).hyperlinkIndex(offset)
				!= -1
			):
				formatField["link"] = True
		except COMError:
			pass

		if obj.hasFocus:
			# Symphony exposes some information for the caret position as attributes on the document object.
			# optimisation: Use the tree interceptor to get the document.
			try:
				docAttribs = obj.treeInterceptor.rootNVDAObject.IA2Attributes
			except AttributeError:
				# No tree interceptor, so we can't efficiently fetch this info.
				pass
			else:
				try:
					formatField["page-number"] = docAttribs["page-number"]
				except KeyError:
					pass
				try:
					formatField["line-number"] = docAttribs["line-number"]
				except KeyError:
					pass

		return formatField, (startOffset, endOffset)

	def _getLineOffsets(self, offset):
		start, end = super(SymphonyTextInfo, self)._getLineOffsets(offset)
		if offset == 0 and start == 0 and end == 0:
			# HACK: Symphony doesn't expose any characters at all on empty lines, but this means we don't ever fetch the list item prefix in this case.
			# Fake a character so that the list item prefix will be spoken on empty lines.
			return (0, 1)
		return start, end

	def _getStoryLength(self):
		# HACK: Account for the character faked in _getLineOffsets() so that move() will work.
		return max(super(SymphonyTextInfo, self)._getStoryLength(), 1)


class SymphonyText(IAccessible, EditableText):
	TextInfo = SymphonyTextInfo

	def _get_positionInfo(self):
		# LibreOffice versions >= 5.0 report the "level" attribute that's
		# handled in the base class, but Apache OpenOffice doesn't,
		# so check for the custom "heading-level" attribute first
		level = self.IA2Attributes.get("heading-level")
		if level:
			return {"level": int(level)}
		return super(SymphonyText, self).positionInfo

	def event_valueChange(self) -> None:
		# announce new value to indicate formatting change if registered gesture
		# triggered the change in toolbar item's value/text
		if SymphonyDocument.isFormattingChangeAnnouncementEnabled(self):
			message = self.IAccessibleTextObject.text(0, -1)
			ui.message(message)
			# disable announcement until next registered keypress enables it again
			SymphonyDocument.announceFormattingGestureChange = False

		return super().event_valueChange()


class SymphonyTableCell(IAccessible):
	"""Silences particular states, and redundant column/row numbers"""

	TextInfo = SymphonyTextInfo

	def _get_cellCoordsText(self):
		return super(SymphonyTableCell, self).name

	name = None

	def _get_hasSelection(self):
		return self.selectionContainer and 1 < self.selectionContainer.getSelectedItemsCount()

	def _get_states(self):
		states = super(SymphonyTableCell, self).states
		states.discard(controlTypes.State.MULTILINE)
		states.discard(controlTypes.State.EDITABLE)
		if controlTypes.State.SELECTED not in states and controlTypes.State.FOCUSED in states:
			# #8988: Cells in Libre Office do not have the selected state when a single cell is selected (i.e. has focus).
			# Since #8898, the negative selected state is announced for table cells with the selectable state.
			if self.hasSelection:
				# The selected state is never added to a focused object, even though it is selected.
				# We assume our focus is in the selection.
				states.add(controlTypes.State.SELECTED)
			else:
				# Remove SELECTABLE to ensure the negative SELECTED state isn't spoken for focused cells.
				states.discard(controlTypes.State.SELECTABLE)
		if self.IA2Attributes.get("Formula"):
			# #860: Recent versions of Calc expose has formula state via IAccessible 2.
			states.add(controlTypes.State.HASFORMULA)
		return states


class SymphonyIATableCell(SymphonyTableCell):
	"""An overlay class for cells implementing IAccessibleTableCell"""

	def event_selectionAdd(self):
		curFocus = api.getFocusObject()
		if (
			self.table
			and self.table == curFocus.table
			and self.table.IAccessibleTable2Object.nSelectedCells > 0
		):
			curFocus.announceSelectionChange()

	def event_selectionRemove(self):
		self.event_selectionAdd()

	def announceSelectionChange(self):
		if self is api.getFocusObject():
			speech.speakObjectProperties(
				self,
				states=True,
				cellCoordsText=True,
				reason=controlTypes.OutputReason.CHANGE,
			)
		braille.handler.handleUpdate(self)
		vision.handler.handleUpdate(self, property="states")

	def _get_cellCoordsText(self):
		if self.hasSelection and controlTypes.State.FOCUSED in self.states:
			count = self.table.IAccessibleTable2Object.nSelectedCells
			selection = self.table.IAccessibleObject.accSelection
			enumObj = selection.QueryInterface(oleacc.IEnumVARIANT)
			firstChild: Union[int, comtypes.client.dynamic._Dispatch]
			firstChild, _retrievedCount = enumObj.Next(1)
			# skip over all except the last element
			enumObj.Skip(count - 2)
			lastChild: Union[int, comtypes.client.dynamic._Dispatch]
			lastChild, _retrieveCount = enumObj.Next(1)
			# in LibreOffice 7.3.0, the IEnumVARIANT returns a child ID,
			# in LibreOffice >= 7.4, it returns an IDispatch
			if isinstance(firstChild, int):
				tableAccessible = self.table.IAccessibleTable2Object.QueryInterface(IA2.IAccessible2)
				firstAccessible = tableAccessible.accChild(firstChild).QueryInterface(IA2.IAccessible2)
				lastAccessible = tableAccessible.accChild(lastChild).QueryInterface(IA2.IAccessible2)
			elif isinstance(firstChild, comtypes.client.dynamic._Dispatch):
				firstAccessible = firstChild.QueryInterface(IA2.IAccessible2)
				lastAccessible = lastChild.QueryInterface(IA2.IAccessible2)
			else:
				raise RuntimeError(f"Unexpected LibreOffice object {firstChild}, type: {type(firstChild)}")
			firstAddress = firstAccessible.accName(0)
			firstValue = firstAccessible.accValue(0) or ""
			lastAddress = lastAccessible.accName(0)
			lastValue = lastAccessible.accValue(0) or ""
			# Translators: LibreOffice, report selected range of cell coordinates with their values
			return _("{firstAddress} {firstValue} through {lastAddress} {lastValue}").format(
				firstAddress=firstAddress,
				firstValue=firstValue,
				lastAddress=lastAddress,
				lastValue=lastValue,
			)
		elif self.rowSpan > 1 or self.columnSpan > 1:
			lastSelected = (
				(self.rowNumber - 1) + (self.rowSpan - 1),
				(self.columnNumber - 1) + (self.columnSpan - 1),
			)
			lastCellUnknown = self.table.IAccessibleTable2Object.cellAt(*lastSelected)
			lastAccessible = lastCellUnknown.QueryInterface(IA2.IAccessible2)
			lastAddress = lastAccessible.accName(0)
			# Translators: LibreOffice, report range of cell coordinates
			return _("{firstAddress} through {lastAddress}").format(
				firstAddress=self._get_name(),
				lastAddress=lastAddress,
			)
		return super().cellCoordsText


class SymphonyTable(IAccessible):
	def event_selectionWithIn(self):
		curFocus = api.getFocusObject()
		if self == curFocus.table:
			curFocus.announceSelectionChange()


class SymphonyButton(IAccessible):
	def event_stateChange(self) -> None:
		# announce new state of toggled toolbar button to indicate formatting change
		# if registered gesture resulted in button state change
		if SymphonyDocument.isFormattingChangeAnnouncementEnabled(self):
			states = self.states
			enabled = controlTypes.State.PRESSED in states or controlTypes.State.CHECKED in states
			# button's accessible name is the font attribute, e.g. "Bold", "Italic"
			if enabled:
				# Translators: a message when toggling formatting (e.g. bold, italic) in LibreOffice
				message = _("{textAttribute} on").format(textAttribute=self.name)
			else:
				# Translators: a message when toggling formatting (e.g. bold, italic) in LibreOffice
				message = _("{textAttribute} off").format(textAttribute=self.name)
			ui.message(message)
			# disable announcement until next registered keypress enables it again
			SymphonyDocument.announceFormattingGestureChange = False

		return super().event_stateChange()


class SymphonyParagraph(SymphonyText):
	"""Removes redundant information that can be retreaved in other ways."""

	value = None
	description = None


def getDistanceTextForTwips(twips):
	"""Returns a text representation of the distance given in twips,
	converted to the local measurement unit."""
	if languageHandler.useImperialMeasurements():
		val = twips / 1440.0
		valText = ngettext(
			# Translators: a measurement in inches
			"{val:.2f} inch",
			"{val:.2f} inches",
			val,
		).format(val=val)
	else:
		val = twips * 0.0017638889
		valText = ngettext(
			# Translators: a measurement in centimetres
			"{val:.2f} centimetre",
			"{val:.2f} centimetres",
			val,
		).format(val=val)
	return valText


class SymphonyDocumentTextInfo(TreeCompoundTextInfo):
	def _get_locationText(self):
		try:
			# if present, use document attributes to get cursor position relative to page
			docAttribs = self.obj.rootNVDAObject.IA2Attributes
			horizontalPos = int(docAttribs["cursor-position-in-page-horizontal"])
			horizontalDistanceText = getDistanceTextForTwips(horizontalPos)
			verticalPos = int(docAttribs["cursor-position-in-page-vertical"])
			verticalDistanceText = getDistanceTextForTwips(verticalPos)
			return _(
				# Translators: LibreOffice, report cursor position in the current page
				"cursor positioned {horizontalDistance} from left edge of page, {verticalDistance} from top edge of page",
			).format(horizontalDistance=horizontalDistanceText, verticalDistance=verticalDistanceText)
		except (AttributeError, KeyError):
			return super(SymphonyDocumentTextInfo, self)._get_locationText()


class SymphonyDocument(CompoundDocument):
	TextInfo = SymphonyDocumentTextInfo

	# variables used for handling announcements resulting from gestures
	GESTURE_ANNOUNCEMENT_TIMEOUT: float = 2.0  # Seconds
	announceFormattingGestureChange: bool = False
	formattingGestureObjectIds: list[str] = []
	lastFormattingGestureEventTime: float = 0

	@staticmethod
	def isFormattingChangeAnnouncementEnabled(obj: NVDAObject) -> bool:
		if not SymphonyDocument.announceFormattingGestureChange:
			return False

		# don't announce if too much time has passed since last gesture
		if time.time() > (
			SymphonyDocument.lastFormattingGestureEventTime + SymphonyDocument.GESTURE_ANNOUNCEMENT_TIMEOUT
		):
			return False

		# only toolbar items are of interest
		if not SymphonyUtils.is_toolbar_item(obj):
			return False

		# If announcement is restricted to objects with specific IDs, check whether
		# object or its parent has an ID that matches.
		# (For editable comboboxes, the value change event is triggered for the edit
		# that's a child of the combobox which has the corresponding ID.)
		if (
			SymphonyDocument.formattingGestureObjectIds
			and (SymphonyUtils.get_id(obj) not in SymphonyDocument.formattingGestureObjectIds)
			and (SymphonyUtils.get_id(obj.parent) not in SymphonyDocument.formattingGestureObjectIds)
		):
			return False

		return True

	# override base class implementation because that one assumes
	# that the text retrieved from the text info for the text unit
	# is the same as the text that actually gets removed, which at
	# least isn't true for Writer paragraphs when removing a word
	# followed by whitespace using Ctrl+Backspace
	def _backspaceScriptHelper(self, unit: str, gesture: inputCore.InputGesture):
		try:
			oldInfo = self.makeTextInfo(textInfos.POSITION_CARET)
			ia2TextObj = oldInfo._start.obj.IAccessibleTextObject
			oldCaretOffset = ia2TextObj.caretOffset
			oldText = ia2TextObj.text(0, ia2TextObj.nCharacters)
		except NotImplementedError:
			gesture.send()
			return

		gesture.send()

		newInfo = self.makeTextInfo(textInfos.POSITION_CARET)
		ia2TextObj = newInfo._start.obj.IAccessibleTextObject
		newCaretOffset = ia2TextObj.caretOffset
		newText = ia2TextObj.text(0, ia2TextObj.nCharacters)

		# double-check check that text between previous and current
		# caret position was deleted and announce it
		deletedText = oldText[newCaretOffset:oldCaretOffset]
		if newText == oldText[0:newCaretOffset] + oldText[oldCaretOffset:]:
			if len(deletedText) > 1:
				speech.speakMessage(deletedText)
			else:
				speech.speakSpelling(deletedText)
				self._caretScriptPostMovedHelper(None, gesture, newInfo)
		else:
			log.warning("Backspace did not remove text as expected.")

	@script(
		gestures=[
			# paragraph style: Body Text
			"kb:control+0",
			# paragraph style: Heading 1
			"kb:control+1",
			# paragraph style: Heading 2
			"kb:control+2",
			# paragraph style: Heading 3
			"kb:control+3",
			# paragraph style: Heading 4
			"kb:control+4",
			# paragraph style: Heading 5
			"kb:control+5",
			# bold
			"kb:control+b",
			# double underline
			"kb:control+d",
			# italic
			"kb:control+i",
			# underline
			"kb:control+u",
			# superscript
			"kb:control+shift+p",
			# subscript
			"kb:control+shift+b",
			# align left
			"kb:control+l",
			# align center
			"kb:control+e",
			# align right
			"kb:control+r",
			# justified
			"kb:control+j",
			# decrease font size
			"kb:control+[",
			# increase font size
			"kb:control+]",
		],
	)
	def script_changeTextFormatting(self, gesture: inputCore.InputGesture):
		"""Reset time and enable announcement of newly changed state/text of toolbar
		items related to text formatting.
		See also :func:`SymphonyButton.event_stateChange` and
		:func:`SymphonyText.event_valueChange`.
		"""
		SymphonyDocument.announceFormattingGestureChange = True

		# changing paragraph style can imply more related formatting changes (e.g. font size, bold,...);
		# restrict announcement to the paragraph style combobox via its ID
		if isinstance(gesture, keyboardHandler.KeyboardInputGesture) and gesture.displayName in [
			"ctrl+0",
			"ctrl+1",
			"ctrl+2",
			"ctrl+3",
			"ctrl+4",
			"ctrl+5",
		]:
			SymphonyDocument.formattingGestureObjectIds = ["applystyle"]
		else:
			SymphonyDocument.formattingGestureObjectIds = []

		SymphonyDocument.lastFormattingGestureEventTime = time.time()
		# send gesture
		gesture.send()


class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		role = obj.role
		windowClassName = obj.windowClassName
		if isinstance(obj, IAccessible) and windowClassName in ("SALTMPSUBFRAME", "SALSUBFRAME", "SALFRAME"):
			if role == controlTypes.Role.TABLECELL:
				if obj._IATableCell:
					clsList.insert(0, SymphonyIATableCell)
				else:
					clsList.insert(0, SymphonyTableCell)
			elif role in {controlTypes.Role.BUTTON, controlTypes.Role.DROPDOWNBUTTON}:
				clsList.insert(0, SymphonyButton)
			elif role == controlTypes.Role.TABLE and (
				hasattr(obj, "IAccessibleTable2Object") or hasattr(obj, "IAccessibleTableObject")
			):
				clsList.insert(0, SymphonyTable)
			elif hasattr(obj, "IAccessibleTextObject") and role in {
				controlTypes.Role.EDITABLETEXT,
				controlTypes.Role.HEADING,
			}:
				clsList.insert(0, SymphonyText)
			if role in {controlTypes.Role.BLOCKQUOTE, controlTypes.Role.PARAGRAPH}:
				clsList.insert(0, SymphonyParagraph)

	def event_NVDAObject_init(self, obj):
		windowClass = obj.windowClassName
		if (
			windowClass in ("SALTMPSUBFRAME", "SALFRAME")
			and obj.role in (controlTypes.Role.DOCUMENT, controlTypes.Role.TEXTFRAME)
			and obj.description
		):
			# This is a word processor document.
			obj.description = None
			obj.treeInterceptorClass = SymphonyDocument

	def searchStatusBar(self, obj: NVDAObject, max_depth: int = 5) -> Optional[NVDAObject]:
		"""Searches for and returns the status bar object
		if either the object itself or one of its recursive children
		(up to the given depth) has the corresponding role."""
		if obj.role == controlTypes.Role.STATUSBAR:
			return obj
		if max_depth < 1 or obj.role not in {
			controlTypes.Role.DIALOG,
			controlTypes.Role.FRAME,
			controlTypes.Role.OPTIONPANE,
			controlTypes.Role.ROOTPANE,
			controlTypes.Role.WINDOW,
		}:
			return None
		for child in obj.children:
			status_bar = self.searchStatusBar(child, max_depth - 1)
			if status_bar:
				return status_bar
		return None

	def _get_statusBar(self) -> Optional[NVDAObject]:
		return self.searchStatusBar(api.getForegroundObject())

	def getStatusBarText(self, obj: NVDAObject) -> str:
		text = ""
		for child in obj.children:
			if hasattr(child, "IAccessibleTextObject"):
				textObj = child.IAccessibleTextObject
				if textObj:
					if text:
						text += " "
					text += textObj.textAtOffset(0, IA2.IA2_TEXT_BOUNDARY_ALL)[2]
		return text
