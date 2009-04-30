import _default

class AppModule(_default.AppModule):

	def event_NVDAObject_init(self, obj):
		if obj.windowClassName == "NativeHWNDHost" and obj.parent and not obj.parent.parent:
			# Make sure the top level pane is always presented.
			obj.isPresentableFocusAncestor = True
			return

		if obj.windowClassName == "Edit" and not obj.name and not obj.parent:
			# Focus automatically jumps to the password field when a user is selected. This field has no name.
			# This means that the new selected user is not reported.
			# Therefore, override the name of the password field to be the selected user name.
			try:
				# The accessibility hierarchy is totally screwed here, so NVDA gets confused.
				# Therefore, we'll have to do it the ugly way...
				obj.name = obj.IAccessibleObject.accParent.accName(0)
			except:
				pass
			return
