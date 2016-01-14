#appModules/eclipse.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010-2014 NV Access Limited

import controlTypes
import appModuleHandler
from NVDAObjects.IAccessible import IAccessible
import ui
import api

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

class AutocompletionListItem(IAccessible):

	def event_selection(self):
		# Fixme: I don't know if it is the correct way to do this.

		# I think that you can feel more confortable if the text editor gain the focus after the item becomes hidden.
		if self.appModule.textEditor == None:
			self.appModule.textEditor = api.getFocusObject()

		if self.appModule.selectedItem != self:
			self.appModule.selectedItem = self
			api.setFocusObject(self)
			self.reportFocus()

	def script_returnToTextEditor(self, gesture):
		# We need to send the gesture to hide the autocompletion window
		gesture.send()

		# Retrieve the focus to the editor
		if self.appModule.textEditor:
			api.setFocusObject(self.appModule.textEditor)
			self.appModule.textEditor.reportFocus()
			
			# And prevent confusing events
			self.appModule.textEditor = None
		
		# And clean up the selected list item because we don't need it
		self.appModule.selectedItem = None

	def script_readDocumentation(self, gesture):
		obj = api.getDesktopObject().simpleFirstChild
		if obj.role == controlTypes.ROLE_DOCUMENT:
			ui.message(obj.basicText)

	__gestures = {
		"kb:escape": "returnToTextEditor",
		"kb:enter": "returnToTextEditor",
		"kb:NVDA+d": "readDocumentation",
	}

class AppModule(appModuleHandler.AppModule):

	textEditor = None
	selectedItem = None

	def event_NVDAObject_init(self, obj):
		if obj.windowClassName == "SysTreeView32" and obj.role in (controlTypes.ROLE_TREEVIEWITEM, controlTypes.ROLE_CHECKBOX) and controlTypes.STATE_FOCUSED not in obj.states:
			# Eclipse tree views seem to fire a focus event on the previously focused item before firing focus on the new item (EclipseBug:315339).
			# Try to filter this out.
			obj.shouldAllowIAccessibleFocusEvent = False

		# I don't know why this doesn't work properly:
		# try:
			# if obj.role == controlTypes.ROLE_LIST and obj.simpleParent.simpleParent == api.getDesktopObject():
				# This is just to change the object's name:
				# obj.name = AUTOCOMPLETION_LIST_NAME
		# except:
			# pass

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == "SWT_Window0" and obj.role == controlTypes.ROLE_EDITABLETEXT:
			clsList.insert(0, EclipseTextArea)

		# This does, but freezes the script a lot:
		# try:
			# if obj.role == controlTypes.ROLE_LIST and obj.simpleParent.simpleParent == api.getDesktopObject():
				# clsList.insert(0, AutocompletionListView)
		# except:
			# pass

		try:
			if obj.role == controlTypes.ROLE_LISTITEM and obj.simpleParent.simpleParent.simpleParent == api.getDesktopObject():
				clsList.insert(0, AutocompletionListItem)
		except:
			pass
