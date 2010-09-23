import _default
import controlTypes

class AppModule(_default.AppModule):

	def event_NVDAObject_init(self,obj):
		if obj.role==controlTypes.ROLE_TREEVIEWITEM:
			obj.hasEncodedAccDescription=True
