# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2012-2023 Mesar Hameed, NV Access Limited, Leonard de Ruijter, Rui Fontes, Cyrille Bougot

"""App module for Poedit 3.4+.
"""

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


class _WindowControlIdOffset(IntEnum):
	"""Window control ID's are not static, however, the order of ids stays the same.
	Therefore, using a wxDataView control in the translations list as a reference,
	we can safely calculate control ids accross releases or instances.
	This class contains window control id offsets relative to the wxDataView window.
	"""

	PRO_IDENTIFIER = -10  # This is a button in the free version
	OLD_SOURCE_TEXT_PRO = 60
	OLD_SOURCE_TEXT = 65
	TRANSLATOR_NOTES_PRO = 63
	TRANSLATOR_NOTES = 68  # 63 in Pro
	COMMENT_PRO = 66
	COMMENT = 71
	TRANSLATION_WARNING = 17
	NEEDS_WORK_SWITCH = 21


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

	_dataViewControlId: int | None
	"""Type definition for auto prop '_get__dataViewControlId'"""

	def _get__dataViewControlId(self) -> int | None:
		fg = api.getForegroundObject()
		dataView = _findDescendantObject(fg.windowHandle, className="wxDataView")
		if not dataView:
			return None
		return dataView.windowControlID

	_isPro: bool
	"""Type definition for auto prop '_get__isPro'"""

	def _get__isPro(self) -> bool:
		"""Returns whether this instance of Poedit is a pro version."""
		obj = self._getNVDAObjectForWindowControlIdOffset(_WindowControlIdOffset.PRO_IDENTIFIER)
		return obj is None

	def _correctWindowControllIdOfset(
			self,
			windowControlIdOffset: _WindowControlIdOffset
	) -> _WindowControlIdOffset:
		"""Corrects a _WindowControlIdOffset when a pro version of Poedit is active."""
		if self._isPro:
			match windowControlIdOffset:
				case _WindowControlIdOffset.OLD_SOURCE_TEXT:
					return _WindowControlIdOffset.OLD_SOURCE_TEXT_PRO
				case _WindowControlIdOffset.TRANSLATOR_NOTES:
					return _WindowControlIdOffset.TRANSLATOR_NOTES_PRO
				case _WindowControlIdOffset.COMMENT:
					return _WindowControlIdOffset.COMMENT_PRO
		return windowControlIdOffset

	def _getNVDAObjectForWindowControlIdOffset(
			self,
			windowControlIdOffset: _WindowControlIdOffset
	) -> Window | None:
		fg = api.getForegroundObject()
		return _findDescendantObject(fg.windowHandle, self._dataViewControlId + windowControlIdOffset)

	_translatorNotesObj: Window | None
	"""Type definition for auto prop '_get__translatorNotesObj'"""

	def _get__translatorNotesObj(self) -> Window | None:
		return self._getNVDAObjectForWindowControlIdOffset(
			self._correctWindowControllIdOfset(_WindowControlIdOffset.TRANSLATOR_NOTES)
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
					pgettext("poedit", "No {description}").format(description=description)
				)
		else:
			ui.message(
				# Translators: this message is reported when NVDA is unable to find
				# a requested window in Poedit.
				# {description} is replaced by the description of the window to be reported, e.g. translator notes
				pgettext("poedit", "Could not find {description} window.").format(description=description)
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
		return self._getNVDAObjectForWindowControlIdOffset(
			self._correctWindowControllIdOfset(_WindowControlIdOffset.COMMENT)
		)

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

	_oldSourceTextObj: Window | None
	"""Type definition for auto prop '_get__oldSourceTextObj'"""

	def _get__oldSourceTextObj(self) -> Window | None:
		return self._getNVDAObjectForWindowControlIdOffset(
			self._correctWindowControllIdOfset(_WindowControlIdOffset.OLD_SOURCE_TEXT)
		)

	@script(
		description=pgettext(
			"poedit",
			# Translators: The description of an NVDA command for Poedit.
			"Reports the old source text, if any. If pressed twice, presents the text in browse mode",
		),
		gesture="kb:control+shift+o",
		category=SCRCAT_POEDIT,
		speakOnDemand=True,
	)
	def script_reportOldSourceText(self, gesture):
		self._reportControlScriptHelper(
			self._oldSourceTextObj,
			# Translators: The description of the "old source text" window in poedit.
			# This text is reported when the given window contains no item to report or could not be found.
			pgettext("poedit", "old source text"),
		)

	_translationWarningObj: Window | None
	"""Type definition for auto prop '_get__translationWarningObj'"""

	def _get__translationWarningObj(self) -> Window | None:
		return self._getNVDAObjectForWindowControlIdOffset(_WindowControlIdOffset.TRANSLATION_WARNING)

	@script(
		description=pgettext(
			"poedit",
			# Translators: The description of an NVDA command for Poedit.
			"Reports a translation warning, if any. If pressed twice, presents the warning in browse mode",
		),
		gesture="kb:control+shift+w",
		category=SCRCAT_POEDIT,
		speakOnDemand=True,
	)
	def script_reportTranslationWarning(self, gesture):
		self._reportControlScriptHelper(
			self._translationWarningObj,
			# Translators: The description of the "translation warning" window in poedit.
			# This text is reported when the given window contains no item to report or could not be found.
			pgettext("poedit", "translation warning"),
		)

	_needsWorkObj: Window | None
	"""Type definition for auto prop '_get__needsWorkObj'"""

	def _get__needsWorkObj(self) -> Window | None:
		obj = self._getNVDAObjectForWindowControlIdOffset(_WindowControlIdOffset.NEEDS_WORK_SWITCH)
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
		l, t, w, h = self.location
		try:
			self.name = NVDAObjects.NVDAObject.objectFromPoint(l + 10, t - 10).name
		except AttributeError:
			return super().name
		return self.name


class PoeditListItem(NVDAObject):
	_warningControlToReport: _WindowControlIdOffset | None
	appModule: AppModule

	def _get__warningControlToReport(self) -> _WindowControlIdOffset | None:
		obj = self.appModule._needsWorkObj
		if obj and controlTypes.State.CHECKED in obj.states:
			return _WindowControlIdOffset.NEEDS_WORK_SWITCH
		obj = self.appModule._oldSourceTextObj
		if obj and not obj.hasIrrelevantLocation:
			return _WindowControlIdOffset.OLD_SOURCE_TEXT
		obj = self.appModule._translationWarningObj
		if obj and obj.parent and obj.parent.parent and not obj.parent.parent.hasIrrelevantLocation:
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
		match self._warningControlToReport:
			case _WindowControlIdOffset.OLD_SOURCE_TEXT:
				tones.beep(495, 50)
			case _WindowControlIdOffset.TRANSLATION_WARNING:
				tones.beep(550, 50)
			case _WindowControlIdOffset.NEEDS_WORK_SWITCH:
				tones.beep(660, 50)
