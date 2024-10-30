# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019-2024 NV Access Limited, Cyrille Bougot

"""App module for Microsoft Word.
Word and Outlook share a lot of code and components. This app module gathers the code that is relevant for
Microsoft Word only.
"""

import appModuleHandler
from scriptHandler import script
import ui
from NVDAObjects.IAccessible.winword import WordDocument as IAccessibleWordDocument
from NVDAObjects.UIA.wordDocument import WordDocument as UIAWordDocument
from NVDAObjects.window.winword import WordDocument
from utils.displayString import DisplayStringIntEnum


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
			return curView.displayString
		except AttributeError:
			return super()._get_description()

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

	__gestures = {
		"kb:control+shift+b": "toggleBold",
		"kb:control+shift+w": "toggleUnderline",
		"kb:control+shift+a": "toggleCaps",
	}
