# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2012-2023 Mesar Hameed, NV Access Limited, Leonard de Ruijter

"""App module for Poedit.
"""

from enum import IntEnum
from typing import Optional
import api
import appModuleHandler
import controlTypes
from scriptHandler import script, getLastScriptRepeatCount
import tones
import ui
from NVDAObjects import NVDAObject
import windowUtils
import NVDAObjects.IAccessible
import winUser


LEFT_TO_RIGHT_EMBEDDING = '\u202a'
"""Character often found in translator comments."""


class _WindowControlIdOffset(IntEnum):
	"""Window control ID's in poedit tend to be stable within one release, then change in a new release.
	However, the order of ids stays the same.
	Therefore, using the first sub window of the main foreground as a reference,
	we can safely calculate control ids accross releases.
	This class contains window control id offsets relative to the first sub window of the main foreground window.
	"""
	OLD_SOURCE_TEXT = 77
	TRANSLATOR_NOTES = 80
	COMMENT = 83
	TRANSLATION_WARNING = 28


def _getObjectWithControlId(parentWindowHandle: int, controlId: int) -> Optional[NVDAObject]:
	"""
	Finds a window with the given controlId, starting from the window belonging to the given parentWindowHandle.
	"""
	try:
		obj = NVDAObjects.IAccessible.getNVDAObjectFromEvent(
			windowUtils.findDescendantWindow(parentWindowHandle, controlID=controlId),
			winUser.OBJID_CLIENT,
			0
		)
	except LookupError:
		obj = None
	return obj


class AppModule(appModuleHandler.AppModule):

	def _getNVDAObjectForWindowControlIdOffset(self, windowControlIdOffset: _WindowControlIdOffset):
		fg = api.getForegroundObject()
		return _getObjectWithControlId(
			fg.windowHandle,
			fg.firstChild.windowControlID + windowControlIdOffset
		)

	def _reportControlScriptHelper(self, windowControlIdOffset: _WindowControlIdOffset, description: str):
		obj = self._getNVDAObjectForWindowControlIdOffset(windowControlIdOffset)
		if obj:
			if not obj.hasIrrelevantLocation and not obj.parent.parent.hasIrrelevantLocation:
				message = obj.name.replace(LEFT_TO_RIGHT_EMBEDDING, '')
				repeats = getLastScriptRepeatCount()
				if repeats == 0:
					ui.message(message)
				else:
					ui.browseableMessage(message, description.title())
			else:
				ui.message(
					# Translators: this message is reported when there is nothing
					# to be presented to the user in Poedit.
					# {description} is replaced by the description of the window to be reported, e.g. translator notes
					pgettext("poedit", "No {description}").format(description=description)
				)
		else:
			# Translators: this message is reported when NVDA is unable to find
			# a requested window in Poedit.
			# {description} is replaced by the description of the window to be reported, e.g. translator notes
			ui.message(pgettext("poedit", "Could not find {description} window.").format(description=description))

	@script(
		description=pgettext(
			"poedit",
			# Translators: The description of an NVDA command for Poedit.
			"Reports any notes for translators. If pressed twice, presents the notes in browse mode"
		),
		gesture="kb:control+shift+a",
	)
	def script_reportAutoCommentsWindow(self, gesture):
		self._reportControlScriptHelper(
			_WindowControlIdOffset.TRANSLATOR_NOTES,
			# Translators: The description of the "Translator notes" window in poedit.
			# This text is reported when the given window contains no item to report or could not be found.
			pgettext("poedit", "notes for translators")
		)

	@script(
		description=pgettext(
			"poedit",
			# Translators: The description of an NVDA command for Poedit.
			"Reports any comment in the comments window. If pressed twice, presents the comment in browse mode"
		),
		gesture="kb:control+shift+c",
	)
	def script_reportCommentsWindow(self, gesture):
		self._reportControlScriptHelper(
			_WindowControlIdOffset.COMMENT,
			# Translators: The description of the "comment" window in poedit.
			# This text is reported when the given window contains no item to report or could not be found.
			pgettext("poedit", "comment")
		)

	@script(
		description=pgettext(
			"poedit",
			# Translators: The description of an NVDA command for Poedit.
			"Reports the old source text, if any. If pressed twice, presents the text in browse mode"
		),
		gesture="kb:control+shift+o",
	)
	def script_reportOldSourceText(self, gesture):
		self._reportControlScriptHelper(
			_WindowControlIdOffset.OLD_SOURCE_TEXT,
			# Translators: The description of the "old source text" window in poedit.
			# This text is reported when the given window contains no item to report or could not be found.
			pgettext("poedit", "old source text")
		)

	@script(
		description=pgettext(
			"poedit",
			# Translators: The description of an NVDA command for Poedit.
			"Reports a translation warning, if any. If pressed twice, presents the warning in browse mode"
		),
		gesture="kb:control+shift+w",
	)
	def script_reportTranslationWarning(self, gesture):
		self._reportControlScriptHelper(
			_WindowControlIdOffset.TRANSLATION_WARNING,
			# Translators: The description of the "translation warning" window in poedit.
			# This text is reported when the given window contains no item to report or could not be found.
			pgettext("poedit", "translation warning")
		)

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.role == controlTypes.Role.LISTITEM and obj.windowClassName == "wxWindowNR":
			clsList.insert(0, PoeditListItem)
		elif (
			obj.role in (controlTypes.Role.EDITABLETEXT, controlTypes.Role.DOCUMENT)
			and obj.windowClassName == "RICHEDIT50W"
		):
			clsList.insert(0, PoeditRichEdit)


class PoeditRichEdit(NVDAObject):

	def _get_name(self,) -> str:
		# These rich edit controls are incorrectly labeled.
		# Oleacc doesn't return any name, and UIA defaults to RichEdit Control.
		# The label object is positioned just above the field on the screen.
		l, t, w, h = self.location
		try:
			self.name = NVDAObjects.NVDAObject.objectFromPoint(l + 10, t - 10).name
		except AttributeError:
			return super().name
		return self.name


class PoeditListItem(NVDAObject):

	_warningControlToReport: Optional[_WindowControlIdOffset]

	def _get__warningControlToReport(self) -> Optional[_WindowControlIdOffset]:
		obj = self.appModule._getNVDAObjectForWindowControlIdOffset(_WindowControlIdOffset.OLD_SOURCE_TEXT)
		if obj and not obj.hasIrrelevantLocation:
			return _WindowControlIdOffset.OLD_SOURCE_TEXT
		obj = self.appModule._getNVDAObjectForWindowControlIdOffset(_WindowControlIdOffset.TRANSLATION_WARNING)
		if (
			obj
			and obj.parent and obj.parent.parent
			and not obj.parent.parent.hasIrrelevantLocation
		):
			return _WindowControlIdOffset.TRANSLATION_WARNING
		return None

	def _get_name(self):
		name = super().name
		if self._warningControlToReport or not self.description:
			# This translation has a warning.
			# Prepend an asterix (*) to the name
			name = f"* {name}"
		self.name = name
		return self.name

	def reportFocus(self):
		super().reportFocus()
		if not self.description:
			# This item is untranslated
			tones.beep(440, 50)
			return
		warning = self._warningControlToReport
		if warning is _WindowControlIdOffset.OLD_SOURCE_TEXT:
			tones.beep(550, 50)
		elif warning is _WindowControlIdOffset.TRANSLATION_WARNING:
			tones.beep(660, 50)
