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

COMPLETION_DIALOG_LABEL = u"Press 'Ctrl+Space' to show Template Proposals "
AUTOCOMPLETION_LIST_NAME = u"Autocompletion List"

class EclipseTextArea(IAccessible):

	def event_valueChange(self):
		# #2314: Eclipse incorrectly fires valueChange when the selection changes.
		# Unfortunately, this causes us to speak the entire selection
		# instead of just the changed selection.
		# Therefore, just drop this event.
		pass

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
	floatingHelp = None

	def event_NVDAObject_init(self, obj):
		if obj.windowClassName == "SysTreeView32" and obj.role in (controlTypes.ROLE_TREEVIEWITEM, controlTypes.ROLE_CHECKBOX) and controlTypes.STATE_FOCUSED not in obj.states:
			# Eclipse tree views seem to fire a focus event on the previously focused item before firing focus on the new item (EclipseBug:315339).
			# Try to filter this out.
			obj.shouldAllowIAccessibleFocusEvent = False
		try:
			if obj.role == controlTypes.ROLE_LIST and obj.parent.next.firstChild.name == COMPLETION_DIALOG_LABEL:
				# Fixme: Just change the name of the object to allow the detection of children items.
				obj.name = AUTOCOMPLETION_LIST_NAME
		except: pass

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == "SWT_Window0" and obj.role == controlTypes.ROLE_EDITABLETEXT:
			clsList.insert(0, EclipseTextArea)
		try:
			if obj.role == controlTypes.ROLE_LISTITEM and obj.parent.role == controlTypes.ROLE_LIST and obj.parent.name == AUTOCOMPLETION_LIST_NAME:
				clsList.insert(0, AutocompletionListItem)
		except: pass
