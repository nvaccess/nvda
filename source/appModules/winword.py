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


class ViewTypes(DisplayStringIntEnum):
	"""Enumeration containing the possible view types in Word documents."""

	DRAFT = 1
	OUTLINE = 2
	PRINT = 3
	WEB = 6
	READ = 7

	@property
	def _displayStringLabels(self):
		return {
			# Translators: One of the view types in Word documents.
			ViewTypes.DRAFT: _("DRAFT"),
			# Translators: One of the view types in Word documents.
			ViewTypes.OUTLINE: _("Outline"),
			# Translators: One of the view types in Word documents.
			ViewTypes.PRINT: _("Print layout"),
			# Translators: One of the view types in Word documents.
			ViewTypes.WEB: _("Web layout"),
			# Translators: One of the view types in Word documents.
			ViewTypes.READ: _("Read mode"),
		}


class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if UIAWordDocument in clsList or IAccessibleWordDocument in clsList:
			clsList.insert(0, WinwordWordDocument)


class WinwordWordDocument(WordDocument):
	def _get_description(self) -> str:
		curView = self.WinwordWindowObject.view.Type
		return ViewTypes(curView).displayString

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
