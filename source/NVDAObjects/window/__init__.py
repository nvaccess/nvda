#NVDAObjects/window.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import re
import ctypes
import ctypes.wintypes
import winKernel
import winUser
from logHandler import log
import controlTypes
from NVDAObjects import NVDAObject

re_WindowsForms=re.compile(r'^WindowsForms[0-9]*\.(.*)\.app\..*$')
re_ATL=re.compile(r'^ATL:(.*)$')


class WindowProcessHandleContainer(object):
	"""
	Manages a Windows process handle. On instanciation it retreaves an open process handle from the process of the provided window, and closes the handle on deletion. 
	@ivar windowHandle: the handle of the window the whos process handle was requested
	@type windowHandle: int
	@ivar processHandle: The actual handle which can be used in any win32 calls that need it.
	@type processHandle: int
	"""
 
	def __init__(self,windowHandle):
		"""
		@param windowHandle: the handle of the window whos process handle should be retreaved.
		@type windowHandle: int
		"""
		self.windowHandle=windowHandle
		import IAccessibleHandler
		self.processHandle=IAccessibleHandler.getProcessHandleFromHwnd(self.windowHandle)

	def __del__(self):
		winKernel.closeHandle(self.processHandle)

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

	@classmethod
	def findBestAPIClass(cls,windowHandle=None):
		windowClassName=winUser.getClassName(windowHandle)
		if windowClassName=="#32769":
			return Window
		import JABHandler
		if JABHandler.isJavaWindow(windowHandle):
			import NVDAObjects.JAB
			return NVDAObjects.JAB.JAB
		import NVDAObjects.IAccessible
		return NVDAObjects.IAccessible.IAccessible

	@classmethod
	def findBestClass(cls,clsList,kwargs):
		windowClassName=winUser.getClassName(kwargs['windowHandle']) if 'windowHandle' in kwargs else None
		windowClassName=cls.normalizeWindowClassName(windowClassName)
		newCls=Window
		if windowClassName=="#32769":
			newCls=Desktop
		elif windowClassName=="#32771":
			newCls=TaskList
		elif windowClassName=="Edit":
			newCls=__import__("edit",globals(),locals(),[]).Edit
		elif windowClassName=="RichEdit":
			newCls=__import__("edit",globals(),locals(),[]).RichEdit
		elif windowClassName=="RichEdit20":
			newCls=__import__("edit",globals(),locals(),[]).RichEdit20
		elif windowClassName=="RICHEDIT50W":
			newCls=__import__("edit",globals(),locals(),[]).RichEdit50
		elif windowClassName=="Scintilla":
			newCls=__import__("scintilla",globals(),locals(),[]).Scintilla
		elif windowClassName=="AkelEditW":
			newCls=__import__("akelEdit",globals(),locals(),[]).AkelEdit
		elif windowClassName=="AkelEditA":
			newCls=__import__("akelEdit",globals(),locals(),[]).AkelEdit
		elif windowClassName=="ConsoleWindowClass":
			newCls=__import__("winConsole",globals(),locals(),[]).WinConsole
		elif windowClassName=="_WwG":
			newCls=__import__("winword",globals(),locals(),[]).WordDocument
		elif windowClassName=="EXCEL7":
			newCls=__import__("excel",globals(),locals(),[]).ExcelGrid
		clsList.append(newCls)
		if newCls!=Window:
			clsList.append(Window)
		return super(Window,cls).findBestClass(clsList,kwargs)

	@classmethod
	def objectFromPoint(cls,x,y,oldNVDAObject=None):
		windowHandle=ctypes.windll.user32.WindowFromPoint(ctypes.wintypes.POINT(x,y))
		if not windowHandle:
			windowHandle=ctypes.windll.user32.GetDesktopWindow()
		APIClass=Window.findBestAPIClass(windowHandle=windowHandle)
		if APIClass!=Window and issubclass(APIClass,Window) and APIClass.objectFromPoint.im_func!=Window.objectFromPoint.im_func:
			return APIClass.objectFromPoint(x,y,oldNVDAObject=oldNVDAObject,windowHandle=windowHandle)
		newNVDAObject=APIClass(windowHandle=windowHandle)
		if oldNVDAObject==newNVDAObject:
			return oldNVDAObject
		return newNVDAObject

	@classmethod
	def objectWithFocus(cls):
		fg=winUser.getForegroundWindow()
		threadID=winUser.getWindowThreadProcessID(fg)[1]
		threadInfo=winUser.getGUIThreadInfo(threadID)
		windowHandle=threadInfo.hwndFocus
		if not windowHandle:
			windowHandle=fg
		APIClass=Window.findBestAPIClass(windowHandle=windowHandle)
		if APIClass!=Window and issubclass(APIClass,Window) and APIClass.objectWithFocus.im_func!=Window.objectWithFocus.im_func:
			return APIClass.objectWithFocus(windowHandle=windowHandle)
		return APIClass(windowHandle=windowHandle)

	@classmethod
	def objectInForeground(cls):
		windowHandle=winUser.getForegroundWindow()
		if not windowHandle:
			log.debugWarning("no foreground window")
			return None
		APIClass=Window.findBestAPIClass(windowHandle=windowHandle)
		if APIClass!=Window and issubclass(APIClass,Window) and APIClass.objectInForeground.im_func!=Window.objectInForeground.im_func:
			return APIClass.objectInForeground(windowHandle=windowHandle)
		return APIClass(windowHandle=windowHandle)

	def __init__(self,windowHandle=None,windowClassName=None):
		if not windowHandle:
			pass #raise ValueError("invalid or not specified window handle")
		if windowClassName:
			self.windowClassName=windowClassName
		self.windowHandle=windowHandle
		NVDAObject.__init__(self)

	def _isEqual(self,other):
		return super(Window,self)._isEqual(other) and other.windowHandle==self.windowHandle

	def _get_name(self):
		return winUser.getWindowText(self.windowHandle)

	def _get_role(self):
		return controlTypes.ROLE_WINDOW

	def _get_windowClassName(self):
		if hasattr(self,"_windowClassName"):
			return self._windowClassName
		name=winUser.getClassName(self.windowHandle)
 		self._windowClassName=name
		return name

	def _get_windowControlID(self):
		if not hasattr(self,"_windowControlID"):
			self._windowControlID=winUser.getControlID(self.windowHandle)
		return self._windowControlID

	def _get_location(self):
		r=ctypes.wintypes.RECT()
		ctypes.windll.user32.GetWindowRect(self.windowHandle,ctypes.byref(r))
		return (r.left,r.top,r.right-r.left,r.bottom-r.top)

	def _get_windowText(self):
		textLength=winUser.sendMessage(self.windowHandle,winUser.WM_GETTEXTLENGTH,0,0)
		textBuf=ctypes.create_unicode_buffer(textLength+2)
		winUser.sendMessage(self.windowHandle,winUser.WM_GETTEXT,textLength+1,textBuf)
		return textBuf.value+u"\0"

	def _get_processID(self):
		if hasattr(self,"_processIDThreadID"):
			return self._processIDThreadID[0]
		self._processIDThreadID=winUser.getWindowThreadProcessID(self.windowHandle)
		return self._processIDThreadID[0]

	def _get_windowThreadID(self):
		if hasattr(self,"_processIDThreadID"):
			return self._processIDThreadID[1]
		self._processIDThreadID=winUser.getWindowThreadProcessID(self.windowHandle)
		return self._processIDThreadID[1]

	def _get_next(self):
		nextWindow=winUser.getWindow(self.windowHandle,winUser.GW_HWNDNEXT)
		while nextWindow and (not winUser.isWindowVisible(nextWindow) or not winUser.isWindowEnabled(nextWindow)):
			nextWindow=winUser.getWindow(nextWindow,winUser.GW_HWNDNEXT)
		if nextWindow:
			return Window(windowHandle=nextWindow)

	def _get_previous(self):
		prevWindow=winUser.getWindow(self.windowHandle,winUser.GW_HWNDPREV)
		while prevWindow and (not winUser.isWindowVisible(prevWindow) or not winUser.isWindowEnabled(prevWindow)):
			prevWindow=winUser.getWindow(prevWindow,winUser.GW_HWNDPREV)
		if prevWindow:
			return Window(windowHandle=prevWindow)

	def _get_firstChild(self):
		childWindow=winUser.getTopWindow(self.windowHandle)
		while childWindow and (not winUser.isWindowVisible(childWindow) or not winUser.isWindowEnabled(childWindow)):
			childWindow=winUser.getWindow(childWindow,winUser.GW_HWNDNEXT)
		if childWindow:
			return Window(windowHandle=childWindow)

	def _get_parent(self):
		parentHandle=winUser.getAncestor(self.windowHandle,winUser.GA_PARENT)
		if parentHandle:
			return Window(windowHandle=parentHandle)

	def _get_states(self):
		states=super(Window,self)._get_states()
		style=self.windowStyle
		if not style&winUser.WS_VISIBLE:
			states.add(controlTypes.STATE_INVISIBLE)
		if style&winUser.WS_DISABLED:
			states.add(controlTypes.STATE_UNAVAILABLE)
		return states

	def _get_windowStyle(self):
		return winUser.getWindowStyle(self.windowHandle)

	def _get_isWindowUnicode(self):
		if not hasattr(self,'_isWindowUnicode'):
			self._isWindowUnicode=bool(ctypes.windll.user32.IsWindowUnicode(self.windowHandle))
 		return self._isWindowUnicode

	def _get_processHandle(self):
		if not hasattr(self,'_processHandleContainer'):
			self._processHandleContainer=WindowProcessHandleContainer(self.windowHandle)
		return self._processHandleContainer.processHandle

	@classmethod
	def normalizeWindowClassName(cls,name):
		"""
		Removes unneeded information from a window class name (e.g. ATL: and windows forms info), and or maps it to a much more well-known compatible class name.
		Conversions are also cached for future normalizations. 
		@param name: the window class name to normalize
		@type name: string
		@returns: the normalized window class name
		@rtype: string
		"""
		try:
			return cls.normalizedWindowClassNameCache[name]
		except KeyError:
			pass
		newName=windowClassMap.get(name,None)
		if not newName:
			for r in (re_WindowsForms,re_ATL):
				m=re.match(r,name)
				if m:
					newName=m.group(1)
					newName=windowClassMap.get(newName,newName)
					break
		if not newName:
			newName=name
		cls.normalizedWindowClassNameCache[name]=newName
		return newName

	normalizedWindowClassNameCache={}

class TaskList(Window):
	isPresentableFocusAncestor = False

class Desktop(Window):

	isPresentableFocusAncestor = False

	def _get_name(self):
		return _("Desktop")

windowClassMap={
	"EDIT":"Edit",
	"TTntEdit.UnicodeClass":"Edit",
	"TMaskEdit":"Edit",
	"TTntMemo.UnicodeClass":"Edit",
	"TRichEdit":"Edit",
	"TRichViewEdit":"Edit",
	"TInEdit.UnicodeClass":"Edit",
	"TEdit":"Edit",
	"TFilenameEdit":"Edit",
	"TSpinEdit":"Edit",
	"ThunderRT6TextBox":"Edit",
	"TMemo":"Edit",
	"RICHEDIT":"Edit",
	"TPasswordEdit":"Edit",
	"THppEdit.UnicodeClass":"Edit",
	"TUnicodeTextEdit.UnicodeClass":"Edit",
	"TTextEdit":"Edit",
	"TPropInspEdit":"Edit",
	"TFilterbarEdit.UnicodeClass":"Edit",
	"EditControl":"Edit",
	"TNavigableTntMemo.UnicodeClass":"Edit",
	"TNavigableTntEdit.UnicodeClass":"Edit",
	"TRichEditViewer":"RichEdit",
	"RichEdit20A":"RichEdit20",
	"RichEdit20W":"RichEdit20",
	"TskRichEdit.UnicodeClass":"RichEdit20",
	"RichEdit20WPT":"RichEdit20",
}
