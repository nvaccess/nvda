import keyUtils
import speech
import api
import braille
import controlTypes
from NVDAObjects.IAccessible import IAccessible, Dialog
import _default

class LogonDialog(Dialog):

	def _get_role(self):
		return controlTypes.ROLE_DIALOG

	def _get_description(self):
		return self.getDialogText(self.parent.firstChild)

class XPPasswordField(IAccessible):

	def bindKeys(self):
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
		if obj.windowClassName in ("NativeHWNDHost", "AUTHUI.DLL: LogonUI Logon Window") and obj.parent and not obj.parent.parent:
			# Make sure the top level pane is always presented.
			obj.isPresentableFocusAncestor = True
			if obj.windowClassName=="AUTHUI.DLL: LogonUI Logon Window":
				obj.__class__=LogonDialog
			return

		if obj.windowClassName == "Edit" and not obj.name:
			parent = obj.parent
			if parent.role == controlTypes.ROLE_LISTITEM:
				self.overlayCustomNVDAObjectClass(obj, XPPasswordField, outerMost=True)
				obj.bindKeys()
				return

	def event_gainFocus(self,obj,nextHandler):
		if obj.windowClassName=="DirectUIHWND" and obj.role==controlTypes.ROLE_BUTTON:
			prev=obj.previous
			if prev and prev.role==controlTypes.ROLE_STATICTEXT:
				speech.speakObjectProperties(api.getForegroundObject(),name=True,role=True,description=True)
				braille.invalidateCachedFocusAncestors(1)
		nextHandler()

