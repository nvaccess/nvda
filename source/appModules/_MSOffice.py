import _default
import NVDAObjects
import IAccessibleHandler
import winUser

class appModule(_default.appModule):

	def __init__(self,*args):
		_default.appModule.__init__(self,*args)
		NVDAObjects.IAccessible.registerNVDAObjectClass(self.processID,"RichEdit20W",IAccessibleHandler.ROLE_SYSTEM_TEXT,NVDAObjects.IAccessible.NVDAObject_edit)

	def __del__(self):
		NVDAObjects.IAccessible.unregisterNVDAObjectClass(self.processID,"RichEdit20W",IAccessibleHandler.ROLE_SYSTEM_TEXT)
		_default.appModule.__del__(self)
