import controlTypes
from .IAccessible import IAccessible

class Adobe(IAccessible):
	pass

	def event_valueChange(self,obj,nextHandler):
		if obj.role in (controlTypes.ROLE_DOCUMENT,controlTypes.ROLE_PAGE):
			self.rootNVDAObject=obj
			self.fillVBuf()
