# App module for Composable Shell (CShell) input panel
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2017-2018 NV Access Limited, Joseph Lee
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""App module for Windows 10 Modern Keyboard aka new touch keyboard panel.
The chief feature is allowing NVDA to announce selected emoji when using the keyboard to search for and select one.
Another feature is to announce candidates for misspellings if suggestions for hardware keyboard is selected.
This is applicable on Windows 10 Fall Creators Update and later."""

import appModuleHandler
import api
import speech
import braille
import ui

class AppModule(appModuleHandler.AppModule):

	def event_UIA_elementSelected(self, obj, nextHandler):
		# #7273: When this is fired on categories, the first emoji from the new category is selected but not announced.
		# Therefore, move the navigator object to that item if possible.
		# However, in recent builds, name change event is also fired.
		# For consistent experience, report the new category first by traversing through controls.
		speech.cancelSpeech()
		# And no, if running on build 17040 and if this is typing suggestion, do not announce candidate window changes, as it is duplicate announcement and is anoying.
		if obj.UIAElement.cachedAutomationID == "IME_Candidate_Window":
			return
		candidate = obj
		if obj.UIAElement.cachedClassName == "ListViewItem":
			# The difference between emoji panel and suggestions list is absence of categories/emoji separation.
			# If dealing with keyboard entry suggestions (build 17040 and later), return immediately.
			candidate = obj.parent.previous
			if candidate is None:
				return
			ui.message(candidate.name)
			obj = candidate.firstChild
		if obj is not None:
			api.setNavigatorObject(obj)
			obj.reportFocus()
			braille.handler.message(braille.getBrailleTextForProperties(name=obj.name, role=obj.role, positionInfo=obj.positionInfo))
		else:
			# Translators: presented when there is no emoji when searching for one in Windows 10 Fall Creators Update and later.
			ui.message(_("No emoji"))
		nextHandler()

	def event_UIA_window_windowOpen(self, obj, nextHandler):
		# Make sure to announce most recently used emoji first in post-1709 builds.
		# Fake the announcement by locating 'most recently used" category and calling selected event on this.
		if obj.childCount == 3:
			self.event_UIA_elementSelected(obj.lastChild.firstChild, nextHandler)
		nextHandler()
