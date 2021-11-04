#NVDAObjects/window.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2019 NV Access Limited, Babbage B.V., Bill Dengler
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import re
import ctypes
import ctypes.wintypes
import winKernel
import winUser
from logHandler import log
import controlTypes
import api
import config
import displayModel
import eventHandler
from NVDAObjects import NVDAObject
from NVDAObjects.behaviors import EditableText, EditableTextWithoutAutoSelectDetection, LiveText
import watchdog
from locationHelper import RectLTWH
from diffHandler import prefer_difflib

re_WindowsForms=re.compile(r'^WindowsForms[0-9]*\.(.*)\.app\..*$')
re_ATL=re.compile(r'^ATL:(.*)$')

try:
	GhostWindowFromHungWindow=ctypes.windll.user32.GhostWindowFromHungWindow
except AttributeError:
	GhostWindowFromHungWindow=None

def isUsableWindow(windowHandle):
	if not ctypes.windll.user32.IsWindowEnabled(windowHandle):
		return False
	if not ctypes.windll.user32.IsWindowVisible(windowHandle):
		return False
	if GhostWindowFromHungWindow and ctypes.windll.user32.GhostWindowFromHungWindow(windowHandle):
		return False
	return True

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
		import oleacc
		self.processHandle=oleacc.GetProcessHandleFromHwnd(self.windowHandle)

	def __del__(self):
		winKernel.closeHandle(self.processHandle)

# We want to work with physical points.
try:
	# Windows >= Vista
	_windowFromPoint = ctypes.windll.user32.WindowFromPhysicalPoint
except AttributeError:
	_windowFromPoint = ctypes.windll.user32.WindowFromPoint

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
	def getPossibleAPIClasses(cls,kwargs,relation=None):
		windowHandle=kwargs['windowHandle']
		windowClassName=winUser.getClassName(windowHandle)
		#The desktop window should stay as a window
		if windowClassName=="#32769":
			return
		#If this window has a ghost window its too dangerous to try any higher APIs 
		if GhostWindowFromHungWindow and GhostWindowFromHungWindow(windowHandle):
			return
		if windowClassName=="EXCEL7" and (relation=='focus' or isinstance(relation,tuple)): 
			from . import excel
			yield excel.ExcelCell 
		if windowClassName=="EXCEL:":
			from .excel import ExcelDropdown as newCls
			yield newCls
		import JABHandler
		if JABHandler.isJavaWindow(windowHandle):
			import NVDAObjects.JAB
			yield NVDAObjects.JAB.JAB 
		import UIAHandler
		if UIAHandler.handler and UIAHandler.handler.isUIAWindow(windowHandle):
			import NVDAObjects.UIA
			yield NVDAObjects.UIA.UIA
		import NVDAObjects.IAccessible
		yield NVDAObjects.IAccessible.IAccessible

	def findOverlayClasses(self,clsList):
		windowClassName=self.normalizeWindowClassName(self.windowClassName)
		newCls=None
		if windowClassName=="#32769":
			newCls=Desktop
		elif windowClassName=="Edit":
			from .edit import Edit as newCls
		elif windowClassName=="RichEdit":
			from .edit import RichEdit as newCls
		elif windowClassName in ("RichEdit20","REComboBox20W"):
			from .edit import RichEdit20 as newCls
		elif windowClassName=="RICHEDIT50W":
			from .edit import RichEdit50 as newCls
		elif windowClassName in ("Scintilla","TScintilla"):
			from .scintilla import Scintilla as newCls
		elif windowClassName in ("AkelEditW", "AkelEditA"):
			from .akelEdit import AkelEdit as newCls
		elif windowClassName=="EXCEL7":
			from .excel import Excel7Window as newCls
		if newCls:
			clsList.append(newCls)

		# If none of the chosen classes seem to support text editing
		# but there is a caret currently in the window,
		# check whether this window exposes its content without using the display model.
		# If not, use the displayModelEditableText class to emulate text editing capabilities
		if not any(issubclass(cls,EditableText) for cls in clsList):
			gi=winUser.getGUIThreadInfo(self.windowThreadID)
			if gi.hwndCaret==self.windowHandle and gi.flags&winUser.GUI_CARETBLINKING:
				if self.windowTextLineCount:
					from .edit import UnidentifiedEdit
					clsList.append(UnidentifiedEdit)
				else:
					clsList.append(DisplayModelEditableText)

		clsList.append(Window)
		super(Window,self).findOverlayClasses(clsList)

	@classmethod
	def kwargsFromSuper(cls,kwargs,relation=None):
		windowHandle=None
		if relation in ('focus','foreground'):
			windowHandle=winUser.getForegroundWindow()
			if not windowHandle: windowHandle=winUser.getDesktopWindow()
			if windowHandle and relation=="focus":
				threadID=winUser.getWindowThreadProcessID(windowHandle)[1]
				threadInfo=winUser.getGUIThreadInfo(threadID)
				if threadInfo.hwndFocus: windowHandle=threadInfo.hwndFocus
		elif isinstance(relation,tuple):
			windowHandle=_windowFromPoint(ctypes.wintypes.POINT(relation[0],relation[1]))
		if not windowHandle:
			return False
		kwargs['windowHandle']=windowHandle
		return True

	def __init__(self,windowHandle=None):
		if not windowHandle:
			raise ValueError("invalid or not specified window handle")
		self.windowHandle=windowHandle
		super(Window,self).__init__()

	def _isEqual(self,other):
		return super(Window,self)._isEqual(other) and other.windowHandle==self.windowHandle

	def _get_name(self):
		return winUser.getWindowText(self.windowHandle)

	def _get_role(self):
		return controlTypes.Role.WINDOW

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
		return RectLTWH.fromCompatibleType(r)

	def _get_displayText(self):
		"""The text at this object's location according to the display model for this object's window."""
		import displayModel
		import textInfos
		return displayModel.DisplayModelTextInfo(self,textInfos.POSITION_ALL).text

	def redraw(self):
		"""Redraw the display for this object.
		"""
		left, top, width, height = self.location
		left, top = winUser.ScreenToClient(self.windowHandle, left, top)
		winUser.RedrawWindow(self.windowHandle,
			winUser.RECT(left, top, left + width, top + height), None,
			winUser.RDW_INVALIDATE | winUser.RDW_UPDATENOW)

	def _get_windowText(self):
		textLength=watchdog.cancellableSendMessage(self.windowHandle,winUser.WM_GETTEXTLENGTH,0,0)
		textBuf=ctypes.create_unicode_buffer(textLength+2)
		watchdog.cancellableSendMessage(self.windowHandle,winUser.WM_GETTEXT,textLength+1,textBuf)
		return textBuf.value

	def _get_windowTextLineCount(self):
		return watchdog.cancellableSendMessage(self.windowHandle,winUser.EM_GETLINECOUNT,0,0)

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
		while nextWindow and not isUsableWindow(nextWindow):
			nextWindow=winUser.getWindow(nextWindow,winUser.GW_HWNDNEXT)
		if nextWindow:
			return Window(windowHandle=nextWindow)

	def _get_previous(self):
		prevWindow=winUser.getWindow(self.windowHandle,winUser.GW_HWNDPREV)
		while prevWindow and not isUsableWindow(prevWindow):
			prevWindow=winUser.getWindow(prevWindow,winUser.GW_HWNDPREV)
		if prevWindow:
			return Window(windowHandle=prevWindow)

	def _get_firstChild(self):
		childWindow=winUser.getTopWindow(self.windowHandle)
		while childWindow and not isUsableWindow(childWindow):
			childWindow=winUser.getWindow(childWindow,winUser.GW_HWNDNEXT)
		if childWindow:
			return Window(windowHandle=childWindow)

	def _get_lastChild(self):
		childWindow=winUser.getTopWindow(self.windowHandle)
		nextWindow=winUser.getWindow(childWindow,winUser.GW_HWNDNEXT)
		while nextWindow:
			childWindow=nextWindow
			nextWindow=winUser.getWindow(childWindow,winUser.GW_HWNDNEXT)
		while childWindow and not isUsableWindow(childWindow):
			childWindow=winUser.getWindow(childWindow,winUser.GW_HWNDPREV)
		if childWindow:
			return Window(windowHandle=childWindow)

	def _get_parent(self):
		parentHandle=winUser.getAncestor(self.windowHandle,winUser.GA_PARENT)
		if parentHandle:
			#Because we, we need to get the APIclass manually need to  set the relation as parent
			kwargs=dict(windowHandle=parentHandle)
			APIClass=Window.findBestAPIClass(kwargs,relation="parent")
			return APIClass(**kwargs) if APIClass else None

	def _get_isInForeground(self):
		fg=winUser.getForegroundWindow()
		return self.windowHandle==fg or winUser.isDescendantWindow(fg,self.windowHandle)

	def _get_states(self):
		states=super(Window,self)._get_states()
		style=self.windowStyle
		if not style&winUser.WS_VISIBLE:
			states.add(controlTypes.State.INVISIBLE)
		if style&winUser.WS_DISABLED:
			states.add(controlTypes.State.UNAVAILABLE)
		return states

	def _get_windowStyle(self):
		return winUser.getWindowStyle(self.windowHandle)

	def _get_extendedWindowStyle(self):
		return winUser.getExtendedWindowStyle(self.windowHandle)

	def _get_isWindowUnicode(self):
		if not hasattr(self,'_isWindowUnicode'):
			self._isWindowUnicode=bool(ctypes.windll.user32.IsWindowUnicode(self.windowHandle))
		return self._isWindowUnicode

	def correctAPIForRelation(self,obj,relation=None):
		if not obj:
			return None
		newWindowHandle=obj.windowHandle
		oldWindowHandle=self.windowHandle
		if newWindowHandle and oldWindowHandle and newWindowHandle!=oldWindowHandle:
			kwargs=dict(windowHandle=newWindowHandle)
			newAPIClass=Window.findBestAPIClass(kwargs,relation=relation)
			oldAPIClass=self.APIClass
			if newAPIClass and newAPIClass!=oldAPIClass:
				return newAPIClass(chooseBestAPI=False,**kwargs)
		return obj

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

	def _get_devInfo(self):
		info = super(Window, self).devInfo
		info.append("windowHandle: %r" % self.windowHandle)
		try:
			ret = repr(self.windowClassName)
		except Exception as e:
			ret = "exception: %s" % e
		info.append("windowClassName: %s" % ret)
		try:
			ret = repr(self.windowControlID)
		except Exception as e:
			ret = "exception: %s" % e
		info.append("windowControlID: %s" % ret)
		try:
			ret = repr(self.windowStyle)
		except Exception as e:
			ret = "exception: %s" % e
		info.append("windowStyle: %s" % ret)
		try:
			ret = repr(self.extendedWindowStyle)
		except Exception as e:
			ret = "exception: %s" % e
		info.append("extendedWindowStyle: %s" % ret)
		try:
			ret = repr(self.windowThreadID)
		except Exception as e:
			ret = "exception: %s" % e
		info.append("windowThreadID: %s" % ret)
		formatLong = self._formatLongDevInfoString
		try:
			ret = formatLong(self.windowText)
		except Exception as e:
			ret = "exception: %s" % e
		info.append("windowText: %s" % ret)
		try:
			self.redraw()
			ret = formatLong(self.displayText)
		except Exception as e:
			ret = "exception: %s" % e
		info.append("displayText: %s" % ret)
		return info

class Desktop(Window):

	isPresentableFocusAncestor = False

	def _get_name(self):
		return _("Desktop")


class DisplayModelEditableText(EditableTextWithoutAutoSelectDetection, Window):

	role=controlTypes.Role.EDITABLETEXT
	TextInfo = displayModel.EditableTextDisplayModelTextInfo

	def event_valueChange(self):
		# Don't report value changes for editable text fields.
		pass

class DisplayModelLiveText(LiveText, Window):
	TextInfo = displayModel.EditableTextDisplayModelTextInfo

	def startMonitoring(self):
		# Force the window to be redrawn, as our display model might be out of date.
		self.redraw()
		displayModel.requestTextChangeNotifications(self, True)
		super(DisplayModelLiveText, self).startMonitoring()

	def stopMonitoring(self):
		super(DisplayModelLiveText, self).stopMonitoring()
		displayModel.requestTextChangeNotifications(self, False)

	def _get_diffAlgo(self):
		# #12974: The display model gives us only one screen of text at a time.
		# Use Difflib to reduce choppiness in reading.
		return prefer_difflib()


windowClassMap={
	"EDIT":"Edit",
	"TTntEdit.UnicodeClass":"Edit",
	"TMaskEdit":"Edit",
	"TTntMemo.UnicodeClass":"Edit",
	"TRichEdit":"RichEdit20",
	"TRichViewEdit":"Edit",
	"TInEdit.UnicodeClass":"Edit",
	"TInEdit":"Edit",
	"TEdit":"Edit",
	"TFilenameEdit":"Edit",
	"TSpinEdit":"Edit",
	"ThunderRT6TextBox":"Edit",
	"TMemo":"Edit",
	"RICHEDIT":"RichEdit",
	"TPasswordEdit":"Edit",
	"THppEdit.UnicodeClass":"Edit",
	"TUnicodeTextEdit.UnicodeClass":"Edit",
	"TTextEdit":"Edit",
	"TPropInspEdit":"Edit",
	"TFilterbarEdit.UnicodeClass":"Edit",
	"EditControl":"Edit",
	"TNavigableTntMemo.UnicodeClass":"Edit",
	"TNavigableTntEdit.UnicodeClass":"Edit",
	"TAltEdit.UnicodeClass":"Edit",
	"TAltEdit":"Edit",
	"TDefEdit":"Edit",
	"TRichEditViewer":"RichEdit",
	"WFMAINRE":"RichEdit20",
	"RichEdit20A":"RichEdit20",
	"RichEdit20W":"RichEdit20",
	"TChatRichEdit":"RichEdit20",
	"TAccessibleEdit":"Edit",
	"TskRichEdit.UnicodeClass":"RichEdit20",
	"RichEdit20WPT":"RichEdit20",
	"RICHEDIT60W":"RICHEDIT50W",
	"TChatRichEdit.UnicodeClass":"RichEdit20",
	"TMyRichEdit":"RichEdit20",
	"TExRichEdit":"RichEdit20",
	"RichTextWndClass":"RichEdit20",
	"TSRichEdit":"RichEdit20",
	"TRxRichEdit":"RichEdit20",
	"ScintillaWindowImpl":"Scintilla",
	"RICHEDIT60W_WLXPRIVATE":"RICHEDIT50W",
	"TNumEdit":"Edit",
	"TAccessibleRichEdit":"RichEdit20",
}
