# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019-2024 NV Access Limited, Cyrille Bougot

"""App module for Microsoft Word.
Word and Outlook share a lot of code and components. This app module gathers the code that is relevant for
Microsoft Word only.
"""

import api
import appModuleHandler
import controlTypes
import globalCommands
import speech
from scriptHandler import script, getLastScriptRepeatCount
import ui
from NVDAObjects.IAccessible.winword import WordDocument as IAccessibleWordDocument
from NVDAObjects.UIA.wordDocument import WordDocument as UIAWordDocument
from NVDAObjects.window.winword import WordDocument


class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if UIAWordDocument in clsList or IAccessibleWordDocument in clsList:
			clsList.insert(0, WinwordWordDocument)

	@script(
		category=globalCommands.SCRCAT_FOCUS,
		description=_(
			# Translators: Input help mode message for report title bar command in Microsoft Word.
			"In Microsoft Word, reports the title and the layout of the current document. If pressed twice, spells this information. If pressed three times, copies it to the clipboard"
		),
		gesture="kb:NVDA+t",
		speakOnDemand=True,
	)
	def script_title(self, gesture):
		title = api.getForegroundObject().name
		statusBar = api.getStatusBar()
		if statusBar is not None:
			for child in statusBar.children:
				if controlTypes.state.State.PRESSED in child.states:
					documentLayout = child.name
					foregroundWindowName = title
					title = f"{foregroundWindowName} - {documentLayout}"
					break
		repeatCount = getLastScriptRepeatCount()
		if repeatCount == 0:
			ui.message(title)
		elif repeatCount == 1:
			speech.speakSpelling(title)
		else:
			api.copyToClip(title, notify=True)


class WinwordWordDocument(WordDocument):
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
