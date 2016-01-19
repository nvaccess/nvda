#appModules/eclipse.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010-2014 NV Access Limited

import controlTypes
import appModuleHandler
from NVDAObjects.IAccessible import IAccessible
import speech
import ui
import api
import sayAllHandler
import eventHandler

# Translators: This will be the name of the list that contains the autocompleter suggestions:
AUTOCOMPLETION_LIST_NAME = _("Autocompletion List")

class EclipseTextArea(IAccessible):

	def event_valueChange(self):
		# #2314: Eclipse incorrectly fires valueChange when the selection changes.
		# Unfortunately, this causes us to speak the entire selection
		# instead of just the changed selection.
		# Therefore, just drop this event.
		pass

class AutocompletionListView(IAccessible):

	def _get_name(self):
		return AUTOCOMPLETION_LIST_NAME

	def event_hide(self):
		# NVDA filters the hide events, even requesting them, so it doesn't work:
		eventHandler.executeEvent("gainFocus", api.getDesktopObject().objectWithFocus())

class AutocompletionListItem(IAccessible):

	def event_selection(self):
		# Fixme: I don't know if it is the correct way to do this.

		# It's to prevent multiple focus event being sent, I.E when you press CTRL or Shift.
		if self.appModule.selectedItem != self:
			self.appModule.selectedItem = self
			eventHandler.executeEvent("gainFocus", self)

	def script_closeAutocompleter(self, gesture):
		gesture.send()
		self.appModule.selectedItem = None
		eventHandler.executeEvent("gainFocus", api.getDesktopObject().objectWithFocus())

	def script_readDocumentation(self, gesture):
		obj = api.getDesktopObject()

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
			# Translators: This will be spoken if the script cann't find the documentation text for the selected autocompletion entry
			ui.message(_("Cann't find documentation for this entry."))
			return

		ui.message(obj.basicText)

	script_readDocumentation.__doc__ = _("Tries to read documentation for this Autocompletion entry.")

	__gestures = {
		"kb:NVDA+d": "readDocumentation",
		"kb:enter": "closeAutocompleter",
		"kb:escape": "closeAutocompleter",
	}

class AppModule(appModuleHandler.AppModule):

	LIST_VIEW_CLASS = "SysListView32"
	selectedItem = None

	def __init__(self,processID,appName=None):
		super(AppModule,self).__init__(processID,appName)
		eventHandler.requestEvents("hide", processID, self.LIST_VIEW_CLASS)

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
				and obj.parent.parent.parent.parent.next.firstChild.role == controlTypes.ROLE_BUTTON):
				clsList.insert(0, AutocompletionListItem)
		except:
			pass

		try:
			if (obj.role == controlTypes.ROLE_LIST
				and obj.parent.parent.role == controlTypes.ROLE_DIALOG
				and obj.parent.parent.parent.parent == api.getDesktopObject()
				and obj.parent.parent.parent.next.firstChild.role == controlTypes.ROLE_BUTTON):
				clsList.insert(0, AutocompletionListView)
		except:
			pass
