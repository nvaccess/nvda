# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2012-2024 Mesar Hameed, NV Access Limited, Leonard de Ruijter, Rui Fontes, Cyrille Bougot

"""App module for Poedit 3.4+."""

from enum import IntEnum

import api
import appModuleHandler
import controlTypes
import NVDAObjects.IAccessible
import tones
import ui
import windowUtils
import winUser
from NVDAObjects import NVDAObject
from NVDAObjects.window import Window
from scriptHandler import getLastScriptRepeatCount, script


LEFT_TO_RIGHT_EMBEDDING = "\u202a"
"""Character often found in translator comments."""

# Translators: The name of a category of NVDA commands.
SCRCAT_POEDIT = _("Poedit")


class _WindowControlId(IntEnum):
	"""Static window control ID's as defined in poedit src/static_ids.h."""

	NEEDS_WORK_SWITCH = 10101
	"""The "Needs work" toggle in editing area at the bottom"""

	TRANSLATION_ISSUE_TEXT = 10102
	"""
	The error or warning line above translation field
	(hidden when there's no issue; ID is of the static text child window with issue's text)
	"""

	PREVIOUS_SOURCE_TEXT = 10103
	"""
	Text of previous source text
	(msgid) for current item (shown in sidebar, may be hidden, is static control with the text)
	"""

	NOTES_FOR_TRANSLATOR = 10104
	"""
	Text of notes for translators (extracted from source code) for current item
	(shown in sidebar, may be hidden, is static control with the text)
	"""

	TRANSLATOR_COMMENT = 10105
	"""
	Text of translator's comment for current item
	(shown in sidebar, may be hidden, is static control with the text)
	"""


def _findDescendantObject(
	parentWindowHandle: int,
	controlId: int | None = None,
	className: str | None = None,
) -> Window | None:
	"""
	Finds a window with the given controlId or class name,
	starting from the window belonging to the given parentWindowHandle,
	and returns the object belonging to it.
	"""
	try:
		obj = NVDAObjects.IAccessible.getNVDAObjectFromEvent(
			windowUtils.findDescendantWindow(parentWindowHandle, controlID=controlId, className=className),
			winUser.OBJID_CLIENT,
			0,
		)
	except LookupError:
		obj = None
	return obj


class AppModule(appModuleHandler.AppModule):
	cachePropertiesByDefault = True

	def _getNVDAObjectForWindowControlId(
		self,
		windowControlId: _WindowControlId,
	) -> Window | None:
		fg = api.getForegroundObject()
		return _findDescendantObject(fg.windowHandle, windowControlId)

	_translatorNotesObj: Window | None
	"""Type definition for auto prop '_get__translatorNotesObj'"""

	def _get__translatorNotesObj(self) -> Window | None:
		return self._getNVDAObjectForWindowControlId(
			_WindowControlId.NOTES_FOR_TRANSLATOR,
		)

	def _reportControlScriptHelper(self, obj: Window, description: str):
		if obj:
			if not obj.hasIrrelevantLocation and not obj.parent.parent.hasIrrelevantLocation:
				message = obj.name.replace(LEFT_TO_RIGHT_EMBEDDING, "")
				repeats = getLastScriptRepeatCount()
				if repeats == 0:
					ui.message(message)
				else:
					ui.browseableMessage(message, description.title())
			else:
				ui.message(
					# Translators: this message is reported when there is nothing
					# to be presented to the user in Poedit.
					# {description} is replaced by the description of the window to be reported,
					# e.g. translator notes
					pgettext("poedit", "No {description}").format(description=description),
				)
		else:
			ui.message(
				# Translators: this message is reported when NVDA is unable to find
				# a requested window in Poedit.
				# {description} is replaced by the description of the window to be reported, e.g. translator notes
				pgettext("poedit", "Could not find {description} window.").format(description=description),
			)

	@script(
		description=pgettext(
			"poedit",
			# Translators: The description of an NVDA command for Poedit.
			"Reports any notes for translators. If pressed twice, presents the notes in browse mode",
		),
		gesture="kb:control+shift+a",
		category=SCRCAT_POEDIT,
		speakOnDemand=True,
	)
	def script_reportAutoCommentsWindow(self, gesture):
		self._reportControlScriptHelper(
			self._translatorNotesObj,
			# Translators: The description of the "Translator notes" window in poedit.
			# This text is reported when the given window contains no item to report or could not be found.
			pgettext("poedit", "notes for translators"),
		)

	_commentObj: Window | None
	"""Type definition for auto prop '_get__commentObj'"""

	def _get__commentObj(self) -> Window | None:
		return self._getNVDAObjectForWindowControlId(_WindowControlId.TRANSLATOR_COMMENT)

	@script(
		description=pgettext(
			"poedit",
			# Translators: The description of an NVDA command for Poedit.
			"Reports any comment in the comments window. "
			"If pressed twice, presents the comment in browse mode",
		),
		gesture="kb:control+shift+c",
		category=SCRCAT_POEDIT,
		speakOnDemand=True,
	)
	def script_reportCommentsWindow(self, gesture):
		self._reportControlScriptHelper(
			self._commentObj,
			# Translators: The description of the "comment" window in poedit.
			# This text is reported when the given window contains no item to report or could not be found.
			pgettext("poedit", "comment"),
		)

	_previousSourceTextObj: Window | None
	"""Type definition for auto prop '_get__previousSourceTextObj'"""

	def _get__previousSourceTextObj(self) -> Window | None:
		return self._getNVDAObjectForWindowControlId(
			_WindowControlId.PREVIOUS_SOURCE_TEXT,
		)

	@script(
		description=pgettext(
			"poedit",
			# Translators: The description of an NVDA command for Poedit.
			"Reports the previous source text, if any. If pressed twice, presents the text in browse mode",
		),
		gesture="kb:control+shift+o",
		category=SCRCAT_POEDIT,
		speakOnDemand=True,
	)
	def script_reportOldSourceText(self, gesture):
		self._reportControlScriptHelper(
			self._previousSourceTextObj,
			# Translators: The description of the "previous source text" window in poedit.
			# This text is reported when the given window contains no item to report or could not be found.
			pgettext("poedit", "previous source text"),
		)

	_translationIssueObj: Window | None
	"""Type definition for auto prop '_get__translationIssueObj'"""

	def _get__translationIssueObj(self) -> Window | None:
		return self._getNVDAObjectForWindowControlId(
			_WindowControlId.TRANSLATION_ISSUE_TEXT,
		)

	@script(
		description=pgettext(
			"poedit",
			# Translators: The description of an NVDA command for Poedit.
			"Reports a translation issue, if any. If pressed twice, presents the warning in browse mode",
		),
		gesture="kb:control+shift+w",
		category=SCRCAT_POEDIT,
		speakOnDemand=True,
	)
	def script_reportTranslationWarning(self, gesture):
		self._reportControlScriptHelper(
			self._translationIssueObj,
			# Translators: The description of the "translation issue" window in poedit.
			# This text is reported when the given window contains no item to report or could not be found.
			pgettext("poedit", "translation issue"),
		)

	_needsWorkObj: Window | None
	"""Type definition for auto prop '_get__needsWorkObj'"""

	def _get__needsWorkObj(self) -> Window | None:
		obj = self._getNVDAObjectForWindowControlId(
			_WindowControlId.NEEDS_WORK_SWITCH,
		)
		if obj and obj.role == controlTypes.Role.CHECKBOX:
			return obj
		return None

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.role == controlTypes.Role.LISTITEM and obj.windowClassName == "wxWindowNR":
			clsList.insert(0, PoeditListItem)
		elif (
			obj.role in (controlTypes.Role.EDITABLETEXT, controlTypes.Role.DOCUMENT)
			and obj.windowClassName == "RICHEDIT50W"
		):
			clsList.insert(0, PoeditRichEdit)


class PoeditRichEdit(NVDAObject):
	def _get_name(self) -> str:
		# These rich edit controls are incorrectly labeled.
		# Oleacc doesn't return any name, and UIA defaults to RichEdit Control.
		# The label object is positioned just above the field on the screen.
		l, t, w, h = self.location  # noqa: E741
		try:
			self.name = NVDAObjects.NVDAObject.objectFromPoint(l + 10, t - 10).name
		except AttributeError:
			return super().name
		return self.name


class PoeditListItem(NVDAObject):
	_warningControlToReport: _WindowControlId | None
	appModule: AppModule

	def _get__warningControlToReport(self) -> int | None:
		obj = self.appModule._previousSourceTextObj
		if obj and not obj.hasIrrelevantLocation:
			return _WindowControlId.PREVIOUS_SOURCE_TEXT
		obj = self.appModule._translationIssueObj
		if obj and obj.parent and obj.parent.parent and not obj.parent.parent.hasIrrelevantLocation:
			return _WindowControlId.TRANSLATION_ISSUE_TEXT
		obj = self.appModule._needsWorkObj
		if obj and controlTypes.State.CHECKED in obj.states:
			return _WindowControlId.NEEDS_WORK_SWITCH
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
		match self._warningControlToReport:
			case _WindowControlId.PREVIOUS_SOURCE_TEXT:
				tones.beep(495, 50)
			case _WindowControlId.TRANSLATION_ISSUE_TEXT:
				tones.beep(550, 50)
			case _WindowControlId.NEEDS_WORK_SWITCH:
				tones.beep(660, 50)
