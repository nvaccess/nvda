import appModuleHandler
import controlTypes

class AppModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self,obj):
		if obj.role==controlTypes.Role.TREEVIEWITEM:
			obj.hasEncodedAccDescription=True
