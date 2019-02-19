#appModules/eclipse.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010-2014 NV Access Limited

import controlTypes
import appModuleHandler
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.behaviors import EditableTextWithSuggestions
import speech
import braille
import ui
import api
import sayAllHandler
import eventHandler
import keyboardHandler


class EclipseTextArea(EditableTextWithSuggestions, IAccessible):

	def event_valueChange(self):
		# #2314: Eclipse incorrectly fires valueChange when the selection changes.
		# Unfortunately, this causes us to speak the entire selection
		# instead of just the changed selection.
		# Therefore, just drop this event.
		pass

	def event_caret(self):
		super(EclipseTextArea, self).event_caret()

		# Check suggestion item and close the list if it is not valid
		try:
			if not self.appModule.selectedItem.name:
				self.event_suggestionsClosed()
				self.appModule.selectedItem = None
		except:
			pass

	def script_closeAutocompleter(self, gesture):
		gesture.send()
		
		# Close the suggestions list if it is opened
		if self.appModule.selectedItem:
			self.event_suggestionsClosed()
			self.appModule.selectedItem = None

	def script_readDocumentation(self, gesture):
		# If there aren't any suggestion selected, there is no way to find quick documentation
		if not self.appModule.selectedItem:
			gesture.send()
			return

		obj = self.appModule.selectedItem.parent.parent.parent.parent.previous.previous
		while obj:
			obj = obj.firstChild
			
			if obj and obj.role == controlTypes.ROLE_DOCUMENT:
				break

		if obj:
			api.setNavigatorObject(obj)
			braille.handler.handleReviewMove()
			sayAllHandler.readText(sayAllHandler.CURSOR_REVIEW)

		else:
			# Translators: When the help popup cannot be found for the selected autocompletion item
			ui.message(_("Cann't find the documentation window."))

	def script_completeInstruction(self, gesture):
		"""
		Performs a standard autocompletion with the `TAB` key.
		"""

		# We need to ensure that the autocompletion popup is open
		if self.appModule.selectedItem:
			self.script_closeAutocompleter(keyboardHandler.KeyboardInputGesture.fromName("enter"))
			return

		# If not, we send the 'tab' key as is
		gesture.send()

	# Translators: Input help mode message for the 'read documentation script
	script_readDocumentation.__doc__ = _("Tries to read documentation for the selected autocompletion item.")

	__gestures = {
		"kb:NVDA+d": "readDocumentation",
		"kb:enter": "closeAutocompleter",
		"KB:tab": "completeInstruction",
		"kb:escape": "closeAutocompleter",
	}


class AutocompletionListItem(IAccessible):

	def event_selection(self):
		if not self.appModule.selectedItem:
			api.getFocusObject().event_suggestionsOpened()

		# This is to ease finding the elp document
		if self.appModule.selectedItem != self:
			self.appModule.selectedItem = self

		# When writing in the editor, the selection event is not fire.
		# This is probably because the items are reused.
		if self.appModule.selectedItemName != self.name:
			self.appModule.selectedItemName = self.name
			speech.cancelSpeech()

			# Reporting as focused should be sufficient
			self.reportFocus()

			# Fixme: I picked up this from UIA SuggestionItem
			braille.handler.message(braille.getBrailleTextForProperties(name=self.name, role=self.role, position=self.positionInfo))

class AppModule(appModuleHandler.AppModule):

	LIST_VIEW_CLASS = "SysListView32"

	# Item and name
	selectedItem = None
	selectedItemName = None

	def __init__(self,processID,appName=None):
		super(AppModule,self).__init__(processID,appName)

	def event_NVDAObject_init(self, obj):
		if obj.windowClassName == "SysTreeView32" and obj.role in (controlTypes.ROLE_TREEVIEWITEM, controlTypes.ROLE_CHECKBOX) and controlTypes.STATE_FOCUSED not in obj.states:
			# Eclipse tree views seem to fire a focus event on the previously focused item before firing focus on the new item (EclipseBug:315339).
			# Try to filter this out.
			obj.shouldAllowIAccessibleFocusEvent = False

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == "SWT_Window0" and obj.role == controlTypes.ROLE_EDITABLETEXT:
			clsList.insert(0, EclipseTextArea)

		try:

			# Autocompletion items are placed outside the main eclipse window
			if (obj.role == controlTypes.ROLE_LISTITEM
				and obj.parent.parent.parent.role == controlTypes.ROLE_DIALOG
				and obj.parent.parent.parent.parent.parent == api.getDesktopObject()
				and obj.parent.parent.parent.parent.simpleNext.role == controlTypes.ROLE_BUTTON):
				clsList.insert(0, AutocompletionListItem)
		except:
			pass
