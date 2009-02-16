import _default
import controlTypes
import gui

class AppModule(_default.AppModule):

	def event_NVDAObject_init(self, obj):
		# It seems that context menus always get the name "context" and this cannot be overridden.
		# Fudge the name of the NVDA system tray menu to make it more friendly.
		if obj.role == controlTypes.ROLE_POPUPMENU and not obj.parent.parent:
			obj.name=gui.appTitle

	def event_gainFocus(self, obj, nextHandler):
		if obj.role == controlTypes.ROLE_PANE and controlTypes.STATE_INVISIBLE in obj.states:
			return
		nextHandler()

	# Silence invisible panes for gainFocus and stateChange as well.
	event_foreground = event_stateChange = event_gainFocus
