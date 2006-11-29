import ctypes
import winUser
from constants import *
import baseType

class NVDAObject_window(baseType.NVDAObject):

	def __init__(self,hwnd):
		baseType.NVDAObject.__init__(self)
		self.hwnd=hwnd

	def __hash__(self):
		return self.hwnd

	def __eq__(self,other):
		if hash(self)==hash(other):
			return True
		else:
			return False

	def __ne__(self,other):
		if hash(self)!=hash(other):
			return True
		else:
			return False

	def _get_name(self):
		return winUser.getWindowText(self.hwnd)

	def _get_role(self):
		return ROLE_SYSTEM_WINDOW

	def _get_className(self):
		return winUser.getClassName(self.hwnd)
 
	def _get_controlID(self):
		return winUser.getControlID()

	def _get_typeString(self):
		return "%s %s"%(self.getClassName(),NVDAObjects.getRoleName(self.role))

	def _get_location(self):
		return winUser.getClientRect(self.hwnd)

	def _get_text(self):
		textLength=winUser.sendMessage(self.hwnd,WM_GETTEXTLENGTH,0,0)
		textBuf=ctypes.create_unicode_buffer(textLength+2)
		winUser.sendMessage(self.hwnd,WM_GETTEXT,textLength+1,textBuf)
		return textBuf.value+u"\0"

	def _get_processID(self):
		return winUser.getWindowThreadProcessID(self.hwnd)
