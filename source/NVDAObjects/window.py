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

	def getName(self):
		return winUser.getWindowText(self.hwnd)
	name=property(fget=getName)

	role=ROLE_SYSTEM_WINDOW

	def getClassName(self):
		return winUser.getClassName(self.hwnd)
	className=property(fget=getClassName)
 
	def getControlID(self):
		return winUser.getControlID()
	controlID=property(fget=getControlID)

	def getTypeString(self):
		return "%s %s"%(self.getClassName(),NVDAObjects.getRoleName(self.role))
	typeString=property(fget=getTypeString)

	def getLocation(self):
		return winUser.getClientRect(self.hwnd)
	location=property(fget=getLocation)

	def getText(self):
		textLength=winUser.sendMessage(self.hwnd,WM_GETTEXTLENGTH,0,0)
		textBuf=ctypes.create_unicode_buffer(textLength+2)
		winUser.sendMessage(self.hwnd,WM_GETTEXT,textLength+1,textBuf)
		return textBuf.value+u"\0"
	text=property(fget=getText)

	def getProcessID(self):
		return winUser.getWindowThreadProcessID(self.hwnd)
	processID=property(fget=getProcessID)
