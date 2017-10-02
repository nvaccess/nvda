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
import ui
import api
import sayAllHandler
import eventHandler


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

		# This may be needed to be changed accordingly to the windows version, but I am unsure
		obj = api.getDesktopObject().firstChild.next

		# It works for Java and XML editor.
		while(obj):

			# Check it first
			if (obj.role == controlTypes.ROLE_DOCUMENT) or (obj.role == controlTypes.ROLE_EDITABLETEXT):
				break

			# Try to find the help window
			obj = obj.firstChild

			if not obj:
				break

		if not obj:
			# Translators: This will be spoken if the script cannot find the documentation text for the selected autocompletion entry
			ui.message(_("Cannot find documentation for this entry."))
			return

		ui.message(obj.basicText)

	# Translators: Input help mode message for the 'read documentation script
	script_readDocumentation.__doc__ = _("Tries to read documentation for this Autocompletion entry.")

	__gestures = {
		"kb:NVDA+d": "readDocumentation",
		"kb:enter": "closeAutocompleter",
		"kb:escape": "closeAutocompleter",
	}


class AutocompletionListItem(IAccessible):

	def event_selection(self):
		# This is to avoid duplicated selection events:
		if not self.appModule.selectedItem:
			api.getDesktopObject().objectWithFocus().event_suggestionsOpened()

		# It's to prevent multiple focus event being sent, I.E when you press CTRL or Shift.
		if self.appModule.selectedItem != self:
			self.appModule.selectedItem = self
			
			# Speak suggestion
			speech.cancelSpeech()
			self.reportFocus()

class AppModule(appModuleHandler.AppModule):

	LIST_VIEW_CLASS = "SysListView32"
	selectedItem = None

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
			if (obj.role == controlTypes.ROLE_LISTITEM
				and obj.parent.parent.parent.role == controlTypes.ROLE_DIALOG
				and obj.parent.parent.parent.parent.parent == api.getDesktopObject()
				and obj.parent.parent.parent.parent.simpleNext.role == controlTypes.ROLE_BUTTON):
				clsList.insert(0, AutocompletionListItem)
		except:
			pass
