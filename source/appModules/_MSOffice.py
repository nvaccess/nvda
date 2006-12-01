import _default
import NVDAObjects
from constants import *
import winUser

class appModule(_default.appModule):

	def __init__(self,*args):
		_default.appModule.__init__(self,*args)
		NVDAObjects.MSAA.registerNVDAObjectClass(self.processID,"RichEdit20W",ROLE_SYSTEM_TEXT,NVDAObjects.MSAA.NVDAObject_edit)

	def __del__(self):
		NVDAObjects.MSAA.unregisterNVDAObjectClass(self.processID,"RichEdit20W",ROLE_SYSTEM_TEXT)
		_default.appModule.__del__(self)
