import keyUtils
import speech
import api
import braille
import controlTypes
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.behaviors import Dialog
import _default
import eventHandler

class LogonDialog(Dialog):

	role = controlTypes.ROLE_DIALOG
	isPresentableFocusAncestor = True

	def event_gainFocus(self):
		child = self.firstChild
		if child and controlTypes.STATE_FOCUSED in child.states and not eventHandler.isPendingEvents("gainFocus"):
			# UIA reports that focus is on the top level pane, even when it's actually on the frame below.
			# This causes us to incorrectly use UIA for the top level pane, which causes this pane to be spoken again when the focus moves.
			# Therefore, bounce the focus to the correct object.
			eventHandler.queueEvent("gainFocus", child)
			return

		return super(LogonDialog, self).event_gainFocus()

class XPPasswordField(IAccessible):

	def initOverlayClass(self):
		for key, script in (
			("extendedUp", "changeUser"),
			("extendedDown", "changeUser"),
		):
			self.bindKey_runtime(key, script)

	def _get_name(self):
		# Focus automatically jumps to the password field when a user is selected. This field has no name.
		# This means that the new selected user is not reported.
		# Therefore, override the name of the password field to be the selected user name.
		# When the user is changed, the parent list item changes.
		# However, the cached parent isn't updated, so force it to update.
		self.parent = self._get_parent()
		try:
			return self.parent.name
		except:
			return super(XPPasswordField, self).name

	def script_changeUser(self, key):
		# The up and down arrow keys change the selected user, but there's no reliable NVDA event for detecting this.
		oldName = self.name
		keyUtils.sendKey(key)
		if oldName == self.name or controlTypes.STATE_FOCUSED not in self.states:
			return
		self.event_gainFocus()

class AppModule(_default.AppModule):

	def event_NVDAObject_init(self, obj):
		if obj.windowClassName == "NativeHWNDHost" and obj.parent and not obj.parent.parent:
			# This is the top level pane of the XP logon screen.
			# Make sure it is always presented.
			obj.isPresentableFocusAncestor = True

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		windowClass = obj.windowClassName

		if windowClass == "AUTHUI.DLL: LogonUI Logon Window" and obj.parent and not obj.parent.parent:
			clsList.insert(0, LogonDialog)
			return

		if windowClass == "Edit" and not obj.name:
			parent = obj.parent
			if parent and parent.role == controlTypes.ROLE_LISTITEM:
				clsList.insert(0, XPPasswordField)
				return

	def event_gainFocus(self,obj,nextHandler):
		if obj.windowClassName=="DirectUIHWND" and obj.role==controlTypes.ROLE_BUTTON and not obj.next:
			prev=obj.previous
			if prev and prev.role==controlTypes.ROLE_STATICTEXT:
				# This is for a popup message in the logon dialog.
				# Present the dialog again so the message will be reported.
				speech.speakObjectProperties(api.getForegroundObject(),name=True,role=True,description=True)
				braille.invalidateCachedFocusAncestors(1)
		nextHandler()
