# App module for Composable Shell (CShell) input panel
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2017 NV Access Limited, Joseph Lee
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""App module for Windows 10 new touch keyboard panel.
The chief feature is allowing NVDA to announce selected emoji when using the keyboard to search for and select one.
This is applicable on Windows 10 Fall Creators Update."""

import appModuleHandler
import api
import speech
import braille
import ui

class AppModule(appModuleHandler.AppModule):

	def event_UIA_elementSelected(self, obj, nextHandler):
		# #7273: When this is fired on categories, the first emoji from the new category is selected but not announced.
		# Therefore, move the navigator object to that item if possible.
		speech.cancelSpeech()
		if obj.UIAElement.cachedClassName == "ListViewItem":
			obj = obj.parent.previous
			ui.message(obj.name)
			obj = obj.firstChild
		if obj is not None:
			api.setNavigatorObject(obj)
			obj.reportFocus()
			braille.handler.message(braille.getBrailleTextForProperties(name=obj.name, role=obj.role, positionInfo=obj.positionInfo))
		else:
			# Translators: presented when there is no emoji when searching for one in Windows 10 Fall Creators Update and later.
			ui.message(_("No emoji"))
		nextHandler()
