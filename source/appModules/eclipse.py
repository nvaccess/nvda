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
from speech import sayAll
import eventHandler
import keyboardHandler
from scriptHandler import script

class EclipseTextArea(EditableTextWithSuggestions, IAccessible):

	def event_suggestionsClosed(self):
		super(EclipseTextArea, self).event_suggestionsClosed()
		self.appModule.selectedItem = None
		self.appModule.selectedItemName = None

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
			if self.appModule.selectedItem and not self.appModule.selectedItem.name:
				self.event_suggestionsClosed()
		except:
			pass

	@script(
		gestures = ["kb:enter", "kb:escape"]
	)
	def script_closeAutocompleter(self, gesture):
		gesture.send()

		# Close the suggestions list if it is opened
		if self.appModule.selectedItem:
			self.event_suggestionsClosed()

	@script(
		# Translators: Input help mode message for the 'read documentation script
		description = _("Tries to read documentation for the selected autocompletion item."),
		gesture = "kb:nvda+d"
	)
	def script_readDocumentation(self, gesture):
		rootDocumentationWindow = None

		# If there aren't any suggestion selected, there is no way to find quick documentation
		if not self.appModule.selectedItem:
			gesture.send()
			return

		# Try to locate the documentation document
		try:
			rootDocumentationWindow = self.appModule.selectedItem.parent.parent.parent.parent.previous.previous
		except AttributeError:
			pass

		# In XML documents this is different, maybe in other editors too
		# so we try to locate the root window again
		if not rootDocumentationWindow or not rootDocumentationWindow.appModule == self.appModule:
			try:
				rootDocumentationWindow = self.appModule.selectedItem.parent.parent.parent.parent.previous
			except AttributeError:
				pass

		# Check if this object is from the same appModule
		if rootDocumentationWindow and rootDocumentationWindow.appModule == self.appModule:
			api.setNavigatorObject(rootDocumentationWindow)
			
			documentObj = rootDocumentationWindow

			while documentObj:
				if documentObj.firstChild:
					documentObj = documentObj.firstChild

					# In some editors the help document is a HTML ones
					# On XML documents, for example, it is a simple read-only editable text
					if documentObj.role in (controlTypes.Role.DOCUMENT, controlTypes.Role.EDITABLETEXT):
						break
				else:
					break

			if documentObj.role == controlTypes.Role.DOCUMENT:
				api.setNavigatorObject(documentObj)
				braille.handler.handleReviewMove()
				sayAll.SayAllHandler.readText(sayAll.CURSOR.REVIEW)

			elif documentObj.role == controlTypes.Role.EDITABLETEXT:
				ui.message(documentObj.value)

		else:
			# Translators: When the help popup cannot be found for the selected autocompletion item
			ui.message(_("Cann't find the documentation window."))

	@script(
		gesture="kb:tab"
	)
	def script_completeInstruction(self, gesture):
		"""
		Performs a standard autocompletion with the `TAB` key, like in other editors.
		"""

		# We need to ensure that the autocompletion popup is open
		if self.appModule.selectedItem:
			self.script_closeAutocompleter(keyboardHandler.KeyboardInputGesture.fromName("enter"))
			return

		# If not, we send the 'tab' key as is
		gesture.send()

class AutocompletionListItem(IAccessible):

	def event_selection(self):
		if not self.appModule.selectedItem:
			api.getFocusObject().event_suggestionsOpened()

		# This is to ease finding the elp document
		if self.appModule.selectedItem != self:
			self.appModule.selectedItem = self

		# If autocompletion popup is open and you write some text in the
		# document, the selection event is not fired. For some reason, neither
		# nameChange, so we need this check:
		if self.appModule.selectedItemName != self.name:
			self.appModule.selectedItemName = self.name
			speech.cancelSpeech()

			# Reporting as focused should be sufficient
			self.reportFocus()

			# Simply calling `reportFocus` doesn't output the text in braille
			# and reporting with `ui.message` needs an extra translation string when reporting position info
			braille.handler.message(braille.getPropertiesBraille(
				name=self.name,
				role=self.role,
				positionInfo=self.positionInfo
			))

class AppModule(appModuleHandler.AppModule):
	LIST_VIEW_CLASS = "SysListView32"

	# Item and name
	selectedItem = None
	selectedItemName = None

	def __init__(self,processID,appName=None):
		super(AppModule,self).__init__(processID,appName)

	def event_NVDAObject_init(self, obj):
		if obj.windowClassName == "SysTreeView32" and obj.role in (controlTypes.Role.TREEVIEWITEM, controlTypes.Role.CHECKBOX) and controlTypes.State.FOCUSED not in obj.states:
			# Eclipse tree views seem to fire a focus event on the previously focused item before firing focus on the new item (EclipseBug:315339).
			# Try to filter this out.
			obj.shouldAllowIAccessibleFocusEvent = False

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == "SWT_Window0" and obj.role == controlTypes.Role.EDITABLETEXT:
			clsList.insert(0, EclipseTextArea)

		try:

			# Autocompletion items are placed outside the main eclipse window
			if (obj.role == controlTypes.Role.LISTITEM
				and obj.parent.parent.parent.role == controlTypes.Role.DIALOG
				and obj.parent.parent.parent.parent.parent == api.getDesktopObject()
				and obj.parent.parent.parent.parent.simpleNext.role == controlTypes.Role.BUTTON):
				clsList.insert(0, AutocompletionListItem)
		except:
			pass
