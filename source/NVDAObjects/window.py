#NVDAObjects/window.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import weakref
import ctypes
import virtualBuffers
import appModuleHandler
import winUser
import speech
from NVDAObjects import NVDAObject

class Window(NVDAObject):
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

	def __init__(self,windowHandle=None,windowClassName=None):
		if not windowHandle:
			raise ArguementError("invalid or not specified window handle")
		NVDAObject.__init__(self)
		if windowClassName:
			self.windowClassName=windowClassName
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
		return int(self.windowHandle)

	def _get_name(self):
		return winUser.getWindowText(self.windowHandle)

	def _get_windowClassName(self):
		if hasattr(self,"_windowClassName"):
			return self._windowClassName
		name=winUser.getClassName(self.windowHandle)
 		self._windowClassName=name
		return name

	def _get_windowControlID(self):
		if hasattr(self,"_windowControlID"):
			return self._windowControlID
		ID=winUser.getControlID(self.windowHandle)
		self._windowControlID=ID
		return ID

	def _get_location(self):
		return winUser.getClientRect(self.windowHandle)

	def _get_windowText(self):
		textLength=winUser.sendMessage(self.windowHandle,winUser.WM_GETTEXTLENGTH,0,0)
		textBuf=ctypes.create_unicode_buffer(textLength+2)
		winUser.sendMessage(self.windowHandle,winUser.WM_GETTEXT,textLength+1,textBuf)
		return textBuf.value+u"\0"

	def _get_windowProcessID(self):
		if hasattr(self,"_processIDThreadID"):
			return self._processIDThreadID[0]
		self._processIDThreadID=winUser.getWindowThreadProcessID(self.windowHandle)
		return self._processIDThreadID[0]

	def _get_windowThreadID(self):
		if hasattr(self,"_processIDThreadID"):
			return self._processIDThreadID[1]
		self._processIDThreadID=winUser.getWindowThreadProcessID(self.windowHandle)
		return self._processIDThreadID[1]

	def _get_parent(self):
		parentHandle=winUser.getAncestor(self.windowHandle,winUser.GA_PARENT)
		if parentHandle:
			return self.__class__(windowHandle=parentHandle)
