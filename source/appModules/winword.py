# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019-2025 NV Access Limited, Cyrille Bougot

"""App module for Microsoft Word.
Word and Outlook share a lot of code and components. This app module gathers the code that is relevant for
Microsoft Word only.
"""

import appModuleHandler
from scriptHandler import script
import ui
from logHandler import log
from NVDAObjects.IAccessible.winword import WordDocument as IAccessibleWordDocument
from NVDAObjects.UIA.wordDocument import WordDocument as UIAWordDocument
from NVDAObjects.window.winword import (
	WordDocument,
	WdOutlineLevel,
)
from utils.displayString import DisplayStringIntEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	import inputCore


class ViewType(DisplayStringIntEnum):
	"""Enumeration containing the possible view types in Word documents:.
	https://learn.microsoft.com/en-us/office/vba/api/word.wdviewtype
	"""

	DRAFT = 1
	OUTLINE = 2
	PRINT = 3
	WEB = 6
	READ = 7

	@property
	def _displayStringLabels(self):
		return {
			# Translators: One of the view types in Word documents.
			ViewType.DRAFT: _("DRAFT"),
			# Translators: One of the view types in Word documents.
			ViewType.OUTLINE: _("Outline"),
			# Translators: One of the view types in Word documents.
			ViewType.PRINT: _("Print layout"),
			# Translators: One of the view types in Word documents.
			ViewType.WEB: _("Web layout"),
			# Translators: One of the view types in Word documents.
			ViewType.READ: _("Read mode"),
		}


class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if UIAWordDocument in clsList or IAccessibleWordDocument in clsList:
			clsList.insert(0, WinwordWordDocument)


class WinwordWordDocument(WordDocument):
	def _get_description(self) -> str:
		try:
			curView = self.WinwordWindowObject.view.Type
			description = super().description
			if isinstance(description, str) and not description.isspace():
				return f"{ViewType(curView).displayString} {description}"
			return ViewType(curView).displayString
		except AttributeError:
			return super()._get_description()

	@script(gestures=["kb:control+alt+o", "kb:control+alt+p"])
	def script_changeViewType(self, gesture: "inputCore.InputGesture") -> None:
		if not self.WinwordWindowObject:
			# We cannot fetch the Word object model, so we therefore cannot report the status change.
			# The object model may be unavailable because it's within Windows Defender Application Guard.
			# In this case, just let the gesture through and don't report anything.
			return gesture.send()
		val = self._WaitForValueChangeForAction(
			lambda: gesture.send(),
			lambda: self.WinwordWindowObject.view.Type,
		)
		ui.message(ViewType(val).displayString)

	@script(gesture="kb:control+shift+e")
	def script_toggleChangeTracking(self, gesture):
		if not self.WinwordDocumentObject:
			# We cannot fetch the Word object model, so we therefore cannot report the status change.
			# The object model may be unavailable because it's within Windows Defender Application Guard.
			# In this case, just let the gesture through and don't report anything.
			return gesture.send()
		val = self._WaitForValueChangeForAction(
			lambda: gesture.send(),
			lambda: self.WinwordDocumentObject.TrackRevisions,
		)
		if val:
			# Translators: a message when toggling change tracking in Microsoft word
			ui.message(_("Change tracking on"))
		else:
			# Translators: a message when toggling change tracking in Microsoft word
			ui.message(_("Change tracking off"))

	@script(
		gestures=[
			"kb:alt+shift+-",
			"kb:alt+shift+=",
			"kb:alt+shift+numpadPlus",
			"kb:alt+shift+numpadMinus",
			"kb:numLock+shift+alt+numpadPlus",
			"kb:numLock+shift+alt+numpadMinus",
		],
	)
	def script_collapseOrExpandHeading(self, gesture: "inputCore.InputGesture") -> None:
		if not self.WinwordSelectionObject:
			# We cannot fetch the Word object model, so we therefore cannot report the collapsed state change.
			# The object model may be unavailable because this is a pure UIA implementation such as Windows 10 Mail,
			# or it's within Windows Defender Application Guard.
			# In this case, just let the gesture through and don't report anything.
			gesture.send()
			return
		if self.WinwordWindowObject.view.Type in [ViewType.OUTLINE, ViewType.DRAFT]:
			# In draft mode, collapsing headings is not available.
			# In Outline view, paragraph.CollapsedState does not report the correct value.
			# So do not report anything in these modes
			gesture.send()
			return
		maxParagraphs = 50
		for nParagraph, paragraph in enumerate(self.WinwordSelectionObject.paragraphs):
			if paragraph.outlineLevel != WdOutlineLevel.BODY_TEXT:
				break
			if nParagraph >= maxParagraphs:
				log.debugWarning("Too many paragraphs selected")
				gesture.send()
				return
		else:
			gesture.send()
			# Translators: a message when collapsing or expanding headings in MS Word
			ui.message(_("No heading selected"))
			return
		val = self._WaitForValueChangeForAction(
			lambda: gesture.send(),
			lambda: paragraph.CollapsedState,
		)
		if val:
			# Translators: a message when collapsing a heading in MS Word
			msg = _("Collapsed")
		else:
			# Translators: a message when expanding a heading in MS Word
			msg = _("Expanded")
		ui.message(msg)

	__gestures = {
		"kb:control+shift+b": "toggleBold",
		"kb:control+shift+w": "toggleUnderline",
		"kb:control+shift+a": "toggleCaps",
	}
