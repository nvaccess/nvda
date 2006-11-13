import _default
import NVDAObjects
from constants import *

class appModule(_default.appModule):

	def __init__(self,*args):
		_default.appModule.__init__(self,*args)
		NVDAObjects.registerNVDAObjectClass("RichEdit20W",ROLE_SYSTEM_TEXT,NVDAObjects.NVDAObject_edit)

	def __del__(self):
		NVDAObjects.unregisterNVDAObjectClass("RichEdit20W",ROLE_SYSTEM_TEXT)
		_default.appModule.__del__(self)
