import keyUtils
from NVDAObjects.IAccessible import IAccessible
import _default

class PasswordField(IAccessible):

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
		try:
			# The accessibility hierarchy is totally screwed here, so NVDA gets confused.
			# Therefore, we'll have to do it the ugly way...
			return self.IAccessibleObject.accParent.accName(0)
		except:
			return super(PasswordField, self).name

	def script_changeUser(self, key):
		# The up and down arrow keys change the selected user, but there's no reliable NVDA event for detecting this.
		oldName = self.name
		keyUtils.sendKey(key)
		if oldName == self.name:
			return
		self.event_gainFocus()

class AppModule(_default.AppModule):

	def event_NVDAObject_init(self, obj):
		if obj.windowClassName == "NativeHWNDHost" and obj.parent and not obj.parent.parent:
			# Make sure the top level pane is always presented.
			obj.isPresentableFocusAncestor = True
			return

		if obj.windowClassName == "Edit" and not obj.name and not obj.parent:
			self.overlayCustomNVDAObjectClass(obj, PasswordField, outerMost=True)
			obj.bindKeys()
			return
