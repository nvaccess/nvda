import appModuleHandler
import controlTypes
import gui

class appModule(appModuleHandler.appModule):

	def event_NVDAObject_init(self, obj):
		# It seems that context menus always get the name "context" and this cannot be overridden.
		# Fudge the name of the NVDA system tray menu to make it more friendly.
		if obj.role == controlTypes.ROLE_POPUPMENU and not obj.parent.parent:
			obj.name=gui.appTitle
