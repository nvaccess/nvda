# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2006-2022 NV Access Limited, Bill Dengler, Leonard de Ruijter

from typing import (
	Union
)

from comtypes import COMError
import comtypes.client
import oleacc
from IAccessibleHandler import IA2, splitIA2Attribs
import appModuleHandler
import controlTypes
from controlTypes import TextPosition
import textInfos
import colors
from compoundDocuments import CompoundDocument, TreeCompoundTextInfo
from NVDAObjects.IAccessible import IAccessible, IA2TextTextInfo
from NVDAObjects.behaviors import EditableText
from logHandler import log
import speech
import api
import braille
import languageHandler
import vision


class SymphonyTextInfo(IA2TextTextInfo):

	def _getFormatFieldAndOffsets(self,offset,formatConfig,calculateOffsets=True):
		obj = self.obj
		try:
			startOffset,endOffset,attribsString=obj.IAccessibleTextObject.attributes(offset)
		except COMError:
			log.debugWarning("could not get attributes",exc_info=True)
			return textInfos.FormatField(),(self._startOffset,self._endOffset)
		formatField=textInfos.FormatField()
		if not attribsString and offset>0:
			try:
				attribsString=obj.IAccessibleTextObject.attributes(offset-1)[2]
			except COMError:
				pass
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
			color=formatField.pop('CharColor')
		except KeyError:
			color=None
		if color:
			formatField['color']=colors.RGB.fromString(color) 
		try:
			backgroundColor=formatField.pop('CharBackColor')
		except KeyError:
			backgroundColor=None
		if backgroundColor:
			formatField['background-color']=colors.RGB.fromString(backgroundColor)

		# optimisation: Assume a hyperlink occupies a full attribute run.
		try:
			if obj.IAccessibleTextObject.QueryInterface(
				IA2.IAccessibleHypertext
			).hyperlinkIndex(offset) != -1:
				formatField["link"] = True
		except COMError:
			pass

		if offset == 0:
			# Only include the list item prefix on the first line of the paragraph.
			numbering = formatField.get("Numbering")
			if numbering:
				formatField["line-prefix"] = numbering.get("NumberingPrefix") or numbering.get("BulletChar")

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

		return formatField,(startOffset,endOffset)

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
		level = self.IA2Attributes.get("heading-level")
		if level:
			return {"level": int(level)}
		return super(SymphonyText, self).positionInfo


class SymphonyTableCell(IAccessible):
	"""Silences particular states, and redundant column/row numbers"""

	TextInfo=SymphonyTextInfo

	def _get_cellCoordsText(self):
		return super(SymphonyTableCell,self).name

	name=None

	def _get_hasSelection(self):
		return (
			self.selectionContainer
			and 1 < self.selectionContainer.getSelectedItemsCount()
		)

	def _get_states(self):
		states=super(SymphonyTableCell,self).states
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
		if self.IA2Attributes.get('Formula'):
			# #860: Recent versions of Calc expose has formula state via IAccessible 2.
			states.add(controlTypes.State.HASFORMULA)
		return states


class SymphonyIATableCell(SymphonyTableCell):
	"""An overlay class for cells implementing IAccessibleTableCell"""

	def event_selectionAdd(self):
		curFocus = api.getFocusObject()
		if self.table and self.table == curFocus.table:
			curFocus.announceSelectionChange()

	def event_selectionRemove(self):
		self.event_selectionAdd()

	def announceSelectionChange(self):
		if self is api.getFocusObject():
			speech.speakObjectProperties(
				self,
				states=True,
				cellCoordsText=True,
				reason=controlTypes.OutputReason.CHANGE
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
			firstValue = firstAccessible.accValue(0) or ''
			lastAddress = lastAccessible.accName(0)
			lastValue = lastAccessible.accValue(0) or ''
			# Translators: LibreOffice, report selected range of cell coordinates with their values
			return _("{firstAddress} {firstValue} through {lastAddress} {lastValue}").format(
				firstAddress=firstAddress,
				firstValue=firstValue,
				lastAddress=lastAddress,
				lastValue=lastValue
			)
		elif self.rowSpan > 1 or self.columnSpan > 1:
			lastSelected = (
				(self.rowNumber - 1) + (self.rowSpan - 1),
				(self.columnNumber - 1) + (self.columnSpan - 1)
			)
			lastCellUnknown = self.table.IAccessibleTable2Object.cellAt(*lastSelected)
			lastAccessible = lastCellUnknown.QueryInterface(IA2.IAccessible2)
			lastAddress = lastAccessible.accName(0)
			# Translators: LibreOffice, report range of cell coordinates
			return _("{firstAddress} through {lastAddress}").format(
				firstAddress=self._get_name(),
				lastAddress=lastAddress
			)
		return super().cellCoordsText


class SymphonyTable(IAccessible):

	def event_selectionWithIn(self):
		curFocus = api.getFocusObject()
		if self == curFocus.table:
			curFocus.announceSelectionChange()


class SymphonyParagraph(SymphonyText):
	"""Removes redundant information that can be retreaved in other ways."""
	value=None
	description=None


def getDistanceTextForTwips(twips):
	"""Returns a text representation of the distance given in twips,
	converted to the local measurement unit."""
	if languageHandler.useImperialMeasurements():
		val = twips / 1440.0
		# Translators: a measurement in inches
		valText = _("{val:.2f} inches").format(val=val)
	else:
		val = twips * 0.0017638889
		# Translators: a measurement in centimetres
		valText = _("{val:.2f} centimetres").format(val=val)
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
				"cursor positioned {horizontalDistance} from left edge of page, {verticalDistance} from top edge of page"
			).format(horizontalDistance=horizontalDistanceText, verticalDistance=verticalDistanceText)
		except (AttributeError, KeyError):
			return super(SymphonyDocumentTextInfo, self)._get_locationText()


class SymphonyDocument(CompoundDocument):
	TextInfo = SymphonyDocumentTextInfo


class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		role=obj.role
		windowClassName=obj.windowClassName
		if isinstance(obj, IAccessible) and windowClassName in ("SALTMPSUBFRAME", "SALSUBFRAME", "SALFRAME"):
			if role == controlTypes.Role.TABLECELL:
				if obj._IATableCell:
					clsList.insert(0, SymphonyIATableCell)
				else:
					clsList.insert(0, SymphonyTableCell)
			elif role == controlTypes.Role.TABLE and (
				hasattr(obj, "IAccessibleTable2Object")
				or hasattr(obj, "IAccessibleTableObject")
			):
				clsList.insert(0, SymphonyTable)
			elif hasattr(obj, "IAccessibleTextObject"):
				clsList.insert(0, SymphonyText)
			if role == controlTypes.Role.PARAGRAPH:
				clsList.insert(0, SymphonyParagraph)

	def event_NVDAObject_init(self, obj):
		windowClass = obj.windowClassName
		if windowClass in ("SALTMPSUBFRAME", "SALFRAME") and obj.role in (controlTypes.Role.DOCUMENT,controlTypes.Role.TEXTFRAME) and obj.description:
			# This is a word processor document.
			obj.description = None
			obj.treeInterceptorClass = SymphonyDocument
