# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2010-2022 NV Access Limited, 2026 Islam Benmebarek

"""NVDAObjects for the Chromium browser project"""

import typing
import unicodedata
from typing import Dict, Optional
from comtypes import COMError

import config
import controlTypes
from NVDAObjects import NVDAObjectTextInfo
from NVDAObjects.IAccessible import IAccessible, IA2TextTextInfo
from virtualBuffers.gecko_ia2 import Gecko_ia2 as GeckoVBuf, Gecko_ia2_TextInfo as GeckoVBufTextInfo
from . import ia2Web
from logHandler import log

if typing.TYPE_CHECKING:
	# F401 imported but unused, actually used as a string within type annotation (to avoid having to import
	# at run time)
	from treeInterceptorHandler import TreeInterceptor  # noqa: F401

supportedAriaDetailsRoles: Dict[str, Optional[controlTypes.Role]] = {
	"unknown": None,  # no explicit role, should be reported as "details"
	"comment": controlTypes.Role.COMMENT,
	"doc-footnote": controlTypes.Role.FOOTNOTE,
	# These roles are current unsupported by IAccessible2,
	# and as such, have not been fully implemented in NVDA.
	# They can only be fetched via the IA2Attribute "details-roles",
	# which is only supported in Chrome.
	# Currently maps to the IA2 role ROLE_LIST_ITEM
	"doc-endnote": None,  # controlTypes.Role.ENDNOTE
	# Currently maps to the IA2 role ROLE_PARAGRAPH
	"definition": None,  # controlTypes.Role.DEFINITION
}
"""
details-roles attribute is only defined in Chrome as of May 2022.
Refer to ComputeDetailsRoles:
https://chromium.googlesource.com/chromium/src/+/main/ui/accessibility/platform/ax_platform_node_base.cc#2419
"""


class ChromeVBufTextInfo(GeckoVBufTextInfo):
	def _calculateDescriptionFrom(self, attrs) -> controlTypes.DescriptionFrom:
		"""Overridable calculation of DescriptionFrom
		@param attrs: source attributes for the TextInfo
		@return: the origin for accDescription.
		@note: Chrome provides 'IAccessible2::attribute_description-from' which declares the origin used for
			accDescription. Chrome also provides `IAccessible2::attribute_description` to maintain compatibility
			with FireFox.
		"""
		ia2attrDescriptionFrom = attrs.get("IAccessible2::attribute_description-from")
		try:
			return controlTypes.DescriptionFrom(ia2attrDescriptionFrom)
		except ValueError:
			if ia2attrDescriptionFrom:
				log.debugWarning(f"Unknown 'description-from' IA2Attribute value: {ia2attrDescriptionFrom}")
		# fallback to Firefox approach
		return super()._calculateDescriptionFrom(attrs)

	def _normalizeControlField(self, attrs):
		attrs = super()._normalizeControlField(attrs)
		if (
			attrs["role"] == controlTypes.Role.TOGGLEBUTTON
			and controlTypes.State.CHECKABLE in attrs["states"]
		):
			# In Chromium, the checkable state is exposed erroneously on toggle buttons.
			attrs["states"].discard(controlTypes.State.CHECKABLE)

		if (
			attrs["role"] == controlTypes.Role.GROUPING
			and attrs.get("IAccessible2::attribute_tag", "").lower() == "figure"
		):
			# Chromium doesn't expose the `<figure>` element as a figure.
			attrs["role"] = controlTypes.Role.FIGURE
		return attrs


class ChromeVBuf(GeckoVBuf):
	TextInfo = ChromeVBufTextInfo

	def __contains__(self, obj):
		if obj.windowHandle != self.rootNVDAObject.windowHandle:
			return False
		if not isinstance(obj, ia2Web.Ia2Web):
			# #4080: Input composition NVDAObjects are the same window but not IAccessible2!
			return False
		accId = obj.IA2UniqueID
		if accId == self.rootID:
			return True
		try:
			self.rootNVDAObject.IAccessibleObject.accChild(accId)
		except COMError:
			return False
		return not self._isNVDAObjectInApplication(obj)


class Document(ia2Web.Document):
	def _get_treeInterceptorClass(self) -> typing.Type["TreeInterceptor"]:
		shouldLoadVBufOnBusyFeatureFlag = bool(
			config.conf["virtualBuffers"]["loadChromiumVBufOnBusyState"],
		)
		vBufUnavailableStates = {  # if any of these are in states, don't return ChromeVBuf
			controlTypes.State.EDITABLE,
		}
		if not shouldLoadVBufOnBusyFeatureFlag:
			log.debug(
				f"loadChromiumVBufOnBusyState feature flag is {shouldLoadVBufOnBusyFeatureFlag},"
				" vBuf WILL NOT be loaded when state of the document is busy.",
			)
			vBufUnavailableStates.add(controlTypes.State.BUSY)
		else:
			log.debug(
				f"loadChromiumVBufOnBusyState feature flag is {shouldLoadVBufOnBusyFeatureFlag},"
				" vBuf WILL be loaded when state of the document is busy.",
			)
		if self.states.intersection(vBufUnavailableStates):
			return super().treeInterceptorClass
		return ChromeVBuf


class ComboboxListItem(IAccessible):
	"""
	Represents a list item inside a combo box.
	"""

	def _get_focusRedirect(self):
		# Chrome 68 and below fires focus on the active list item of combo boxes even when the combo box is collapsed.
		# We get around this by redirecting focus back up to the combo box itself if the list inside is invisible (I.e. the combo box is collapsed).
		if self.parent and controlTypes.State.INVISIBLE in self.parent.states:
			return self.parent.parent


class ToggleButton(ia2Web.Ia2Web):
	def _get_states(self):
		# In Chromium, the checkable state is exposed erroneously on toggle buttons.
		states = super().states
		states.discard(controlTypes.State.CHECKABLE)
		return states


class PresentationalList(ia2Web.Ia2Web):
	"""
	Ensures that lists like UL, DL and OL always have the readonly state.
	A work-around for issue #7562
	allowing us to differentiate presentational lists from interactive lists
	(such as of size greater 1 and ARIA list boxes).
	In firefox, this is possible by the presence of a read-only state,
	even in a content editable.
	"""

	def _get_states(self):
		states = super().states
		states.add(controlTypes.State.READONLY)
		return states


class Figure(ia2Web.Ia2Web):
	def _get_role(self) -> controlTypes.Role:
		return controlTypes.Role.FIGURE


def _containsMultipleWhitespaceSeparatedWords(text: str) -> bool:
	foundWordCharacter = False
	foundWhitespaceAfterWord = False
	for character in text:
		if character.isalnum():
			if foundWhitespaceAfterWord:
				return True
			foundWordCharacter = True
		elif foundWordCharacter and character.isspace():
			foundWhitespaceAfterWord = True
	return False


def _isWordCharacter(character: str) -> bool:
	"""Return whether a character can occur within a word for boundary validation."""
	category = unicodedata.category(character)
	return category[0] in ("L", "M", "N") or category == "Pc"


def _rangeCutsThroughWord(textInfo: IA2TextTextInfo, start: int, end: int) -> bool:
	"""Return whether either edge of a range splits a Unicode word."""
	if start > 0:
		startContext = textInfo._getTextRange(start - 1, start + 1)
		if len(startContext) == 2 and all(_isWordCharacter(character) for character in startContext):
			return True
	endContext = textInfo._getTextRange(max(0, end - 1), end + 1)
	return len(endContext) == 2 and all(_isWordCharacter(character) for character in endContext)


class ChromiumIA2TextTextInfo(IA2TextTextInfo):
	"""Raw text information for editable text exposed by Chromium."""

	def _getWordOffsets(self, offset: int) -> tuple[int, int]:
		ia2Offsets = super()._getWordOffsets(offset)
		wordText = self._getTextRange(*ia2Offsets)
		if not (
			_containsMultipleWhitespaceSeparatedWords(wordText) or _rangeCutsThroughWord(self, *ia2Offsets)
		):
			return ia2Offsets
		# Chromium can expose a word boundary that overlaps another word or cuts through one
		# for mixed-direction text.
		# Its caret offsets are still correct, so use NVDA's configured segmentation as a fallback.
		return super(IA2TextTextInfo, self)._getWordOffsets(offset)


def _getRawTextInfoClass(obj) -> type[IA2TextTextInfo] | type[NVDAObjectTextInfo]:
	if obj.TextInfo is NVDAObjectTextInfo:
		return NVDAObjectTextInfo
	return ChromiumIA2TextTextInfo


class EditorTextInfo(ia2Web.MozillaCompoundTextInfo):
	"""The TextInfo for edit areas such as edit fields and documents in Chromium."""

	def _makeRawTextInfo(self, obj, position):
		return _getRawTextInfoClass(obj)(obj, position)

	def _isCaretAtEndOfLine(self, caretObj: IAccessible) -> bool:
		# Detecting if the caret is at the end of the line in Chromium is not currently possible
		# as Chromium's IAccessibleText::textAtOffset with IA2_OFFSET_CARET returns the first character of the next line,
		# which is what we are trying to avoid in the first place.
		# #17039: In some scenarios such as in large files in VS Code,
		# this call is extreamly costly for no actual bennifit right now,
		# so we are disabling it for Chromium.
		return False


class Editor(ia2Web.Editor):
	"""The NVDAObject for edit areas such as edit fields and documents in Chromium."""

	TextInfo = EditorTextInfo


def findExtraOverlayClasses(obj, clsList):
	"""Determine the most appropriate class(es) for Chromium objects.
	This works similarly to L{NVDAObjects.NVDAObject.findOverlayClasses} except that it never calls any other findOverlayClasses method.
	"""
	if (
		obj.role == controlTypes.Role.LISTITEM
		and obj.parent
		and obj.parent.parent
		and obj.parent.parent.role == controlTypes.Role.COMBOBOX
	):
		clsList.append(ComboboxListItem)
	elif obj.role == controlTypes.Role.TOGGLEBUTTON:
		clsList.append(ToggleButton)
	elif obj.role == controlTypes.Role.LIST and obj.IA2Attributes.get("tag") in ("ul", "dl", "ol"):
		clsList.append(PresentationalList)
	elif obj.role == controlTypes.Role.GROUPING and obj.IA2Attributes.get("tag", "").casefold() == "figure":
		clsList.append(Figure)
	ia2Web.findExtraOverlayClasses(
		obj,
		clsList,
		documentClass=Document,
	)
	if ia2Web.Editor in clsList:
		clsList.insert(0, Editor)
