import ctypes
import winUser
import audio
import baseType

class NVDAObject_window(baseType.NVDAObject):
	"""
An NVDAObject for a window
@ivar windowHandle: The window's handle
@type windowHandle: int
@ivar windowClassName: the window's class
@type windowClassName: string
@ivar windowControlID: the window's control ID
@type windowControlID: int
@ivar windowText: The window's text (using winUser.WM_GETTEXT) 
@type windowText: string
@ivar windowProcessID: The window's [processID,threadID]
@type windowProcessID: list of two ints
"""

	def __init__(self,hwnd):
		baseType.NVDAObject.__init__(self)
		self.windowHandle=hwnd
		l=self._hashLimit
		p=self._hashPrime
		h=self._cachedHash
		h=(h+(hash(self.windowHandle)*p))%l
		self._cachedHash=h

	def _get_name(self):
		return winUser.getWindowText(self.windowHandle)

	def _get_role(self):
		return ROLE_SYSTEM_WINDOW

	def _get_windowClassName(self):
		return winUser.getClassName(self.windowHandle)
 
	def _get_windowControlID(self):
		return winUser.getControlID()

	def _get_typeString(self):
		return self.windowClassName

	def _get_location(self):
		return winUser.getClientRect(self.windowHandle)

	def _get_windowText(self):
		textLength=winUser.sendMessage(self.windowHandle,winUser.WM_GETTEXTLENGTH,0,0)
		textBuf=ctypes.create_unicode_buffer(textLength+2)
		winUser.sendMessage(self.windowHandle,winUser.WM_GETTEXT,textLength+1,textBuf)
		return textBuf.value+u"\0"

	def _get_windowProcessID(self):
		return winUser.getWindowThreadProcessID(self.windowHandle)

