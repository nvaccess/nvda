#NVDAObjects/window.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import weakref
import ctypes
import virtualBuffers
import appModuleHandler
import winUser
import speech
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

	def __init__(self,windowHandle):
		baseType.NVDAObject.__init__(self)
		self.windowHandle=windowHandle
		if not hasattr(self,'appModule'):
			try:
				self.appModule=weakref.ref(appModuleHandler.getAppModuleFromWindow(windowHandle))
			except:
				self.appModule=lambda: None
		virtualBuffer=virtualBuffers.getVirtualBuffer(self)
		if virtualBuffer is not None:
			self.virtualBuffer=weakref.ref(virtualBuffer)
		else:
			self.virtualBuffer=lambda: None
		if hasattr(self.appModule(),'event_NVDAObject_init'):
			self.appModule().event_NVDAObject_init(self)

	def __hash__(self):
		return self.windowHandle

	def _get_name(self):
		return winUser.getWindowText(self.windowHandle)

	def _get_windowClassName(self):
		return winUser.getClassName(self.windowHandle)
 
	def _get_windowControlID(self):
		return winUser.getControlID(self.windowHandle)

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
