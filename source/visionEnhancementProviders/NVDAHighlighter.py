#visionEnhancementProviders/NVDAHighlighter.py
#visionEnhancementProviders/NVDAHighlighter.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018-2019 NV Access Limited, Babbage B.V., Takuya Nishimoto

"""Default highlighter based on GDI Plus."""

from vision import Highlighter, CONTEXT_FOCUS, CONTEXT_NAVIGATOR, CONTEXT_BROWSEMODE, _isDebug
from windowUtils import CustomWindow
import wx
import gui
import api
from ctypes import pointer, byref, WinError
from ctypes.wintypes import COLORREF, MSG
import winUser
from logHandler import log
from mouseHandler import getTotalWidthAndHeightAndMinimumPosition
from locationHelper import RectLTRB, RectLTWH
import config
from collections import namedtuple
import threading
import winGDI
import weakref
from colors import RGB
import core

# Highlighter specific contexts
#: Context for overlapping focus and navigator objects
CONTEXT_FOCUS_NAVIGATOR = "focusNavigatorOverlap"

class HighlightStyle(
	namedtuple("HighlightStyle", ("color", "width", "style", "margin"))
):
	"""Represents the style of a highlight for a particular context.
	@ivar color: THe color to use for the style
	@type color: L{RGB}
	@ivar width: The width of the lines to be drawn, in pixels.
		A higher width reduces the inner dimentions of the rectangle.
		Therefore, if you need to increase the outer dimentions of the rectangle, you need to increase the margin as well.
	@type width: int
	@ivar style: The style of the lines to be drawn;
		One of the C{winGDI.DashStyle*} enumeration constants.
	@type style: int
	@ivar margin: The number of pixels between the highlight's rectangle
		and the rectangle of the object to be highlighted.
		A higher margin increases both the inner and outer dimentions of the highlight's rectangle.
		This value may also be negative.
	@type margin: int
	"""
	__slots__ = ()

class VisionEnhancementProvider(Highlighter):
	name = "NVDAHighlighter"
	# Translators: Description for NVDA's built-in screen highlighter.
	description = _("NVDA Highlighter")
	supportedHighlightContexts = (CONTEXT_FOCUS, CONTEXT_NAVIGATOR, CONTEXT_BROWSEMODE)
	_ContextStyles = {
		CONTEXT_FOCUS: HighlightStyle(RGB(0x03, 0x36, 0xff), 5, winGDI.DashStyleDash, 5),
		CONTEXT_NAVIGATOR: HighlightStyle(RGB(0xff, 0x02, 0x66), 5, winGDI.DashStyleSolid, 5),
		CONTEXT_FOCUS_NAVIGATOR: HighlightStyle(RGB(0x03, 0x36, 0xff), 5, winGDI.DashStyleSolid, 5),
		CONTEXT_BROWSEMODE: HighlightStyle(RGB(0xff, 0xde, 0x03), 2, winGDI.DashStyleSolid, 2),
	}
	refreshInterval = 100

	_contextOptionLabelsWithAccelerators = {
		# Translators: shown for a highlighter setting that toggles
		# highlighting the system focus.
		CONTEXT_FOCUS: _("Highlight system fo&cus"),
		# Translators: shown for a highlighter setting that toggles
		# highlighting the browse mode cursor.
		CONTEXT_BROWSEMODE: _("Highlight browse &mode cursor"),
		# Translators: shown for a highlighter setting that toggles
		# highlighting the navigator object.
		CONTEXT_NAVIGATOR: _("Highlight navigator &object"),
	}
	def _get_supportedSettings(self):
		settings = []
		for context in self.supportedHighlightContexts:
			settings.append(self.HighlightSetting(context, self._contextOptionLabelsWithAccelerators[context]))
		return settings

	def initializeHighlighter(self):
		super(VisionEnhancementProvider, self).initializeHighlighter()
		winGDI.gdiPlusInitialize()
		self.window = None
		self._highlighterThread = threading.Thread(target=self._run)
		self._highlighterThread.daemon = True
		self._highlighterThread.start()

	def terminateHighlighter(self):
		if self._highlighterThread:
			if not winUser.user32.PostThreadMessageW(self._highlighterThread.ident, winUser.WM_QUIT, 0, 0):
				raise WinError()
			self._highlighterThread.join()
			self._highlighterThread = None
		winGDI.gdiPlusTerminate()
		super(VisionEnhancementProvider, self).terminateHighlighter()

	def _run(self):
		if _isDebug():
			log.debug("Starting NVDAHighlighter thread")
		window = self.window = HighlightWindow(self)
		timer = 	winUser.user32.SetTimer(window.handle, 0, self.refreshInterval, None)
		msg = MSG()
		while winUser.getMessage(byref(msg),None,0,0):
			winUser.user32.TranslateMessage(byref(msg))
			winUser.user32.DispatchMessageW(byref(msg))
		if _isDebug():
			log.debug("Quit message received on NVDAHighlighter thread")
		if not winUser.user32.KillTimer(window.handle, 0):
			raise WinError()
		if self.window:
			self.window.destroy()
			self.window = None

	def refresh(self):
		if self.window:
			self.window.refresh()

	def updateContextRect(self, context, rect=None, obj=None):
		super(VisionEnhancementProvider, self).updateContextRect(context, rect, obj)
		self.refresh()

class HighlightWindow(CustomWindow):
	transparency = 0xff
	className = u"NVDAHighlighter"
	windowName = u"NVDA Highlighter Window"
	windowStyle = winUser.WS_POPUP | winUser.WS_DISABLED
	extendedWindowStyle = winUser.WS_EX_TOPMOST | winUser.WS_EX_LAYERED

	@classmethod
	def _get__wClass(cls):
		wClass = super(HighlightWindow, cls)._wClass
		wClass.style = winUser.CS_HREDRAW | winUser.CS_VREDRAW
		return wClass

	def updateLocationForDisplays(self):
		if _isDebug():
			log.debug("Updating NVDAHighlighter window location for displays")
		displays = [ wx.Display(i).GetGeometry() for i in xrange(wx.Display.GetCount()) ]
		screenWidth, screenHeight, minPos = getTotalWidthAndHeightAndMinimumPosition(displays)
		# Hack: Windows has a "feature" that will stop desktop shortcut hotkeys from working when a window is full screen.
		# Removing one line of pixels from the bottom of the screen will fix this.
		left = minPos.x
		top = minPos.y
		width = screenWidth
		height = screenHeight-1
		self.location = RectLTWH(left, top, width, height)
		winUser.user32.ShowWindow(self.handle, winUser.SW_HIDE)
		if not winUser.user32.SetWindowPos(
			self.handle,
			winUser.HWND_TOPMOST,
			left, top, width, height,
			winUser.SWP_NOACTIVATE
		):
			raise WinError()
		winUser.user32.ShowWindow(self.handle, winUser.SW_SHOWNA)

	def __init__(self, highlighter):
		if _isDebug():
			log.debug("initializing NVDAHighlighter window")
		super(HighlightWindow, self).__init__(
			windowName=self.windowName,
			windowStyle=self.windowStyle,
			extendedWindowStyle=self.extendedWindowStyle,
			parent=gui.mainFrame.Handle
		)
		self.highlighterRef = weakref.ref(highlighter)
		self.transparentBrush = winGDI.gdi32.CreateSolidBrush(COLORREF(0))
		winUser.SetLayeredWindowAttributes(self.handle, None, self.transparency, winUser.LWA_ALPHA | winUser.LWA_COLORKEY)
		self.updateLocationForDisplays()
		if not winUser.user32.UpdateWindow(self.handle):
			raise WinError()

	def windowProc(self, hwnd, msg, wParam, lParam):
		if msg == winUser.WM_PAINT:
			self._paint()
			# Ensure the window is top most
			winUser.user32.SetWindowPos(
				self.handle,
				winUser.HWND_TOPMOST,
				0, 0, 0, 0,
				winUser.SWP_NOACTIVATE | winUser.SWP_NOMOVE | winUser.SWP_NOSIZE
			)
		elif msg == winUser.WM_DESTROY:
			winUser.user32.PostQuitMessage(0)
		elif msg == winUser.WM_TIMER:
			self.refresh()
		elif msg == winUser.WM_DISPLAYCHANGE:
			# wx might not be aware of the display change at this point
			core.callLater(100, self.updateLocationForDisplays)

	def _paint(self):
		highlighter = self.highlighterRef()
		if not highlighter:
			# The highlighter instance died unexpectedly, kill the window as well
			winUser.user32.PostQuitMessage(0)
			return
		contextRects = {}
		for context in highlighter.enabledHighlightContexts:
			rect = highlighter.contextToRectMap.get(context)
			if not rect:
				continue
			elif context == CONTEXT_NAVIGATOR and contextRects.get(CONTEXT_FOCUS) == rect:
				# When the focus overlaps the navigator object, which is usually the case,
				# show a different highlight style.
				# Focus is in contextRects, do not show the standalone focus highlight.
				contextRects.pop(CONTEXT_FOCUS)
				# Navigator object might be in contextRects as well
				contextRects.pop(CONTEXT_NAVIGATOR, None)
				context = CONTEXT_FOCUS_NAVIGATOR
			contextRects[context] = rect
		if not contextRects:
			return
		windowRect = winUser.getClientRect(self.handle)
		with winUser.paint(self.handle) as hdc:
			winUser.user32.FillRect(hdc, byref(windowRect), self.transparentBrush)
			with winGDI.GDIPlusGraphicsContext(hdc) as graphicsContext:
				for context, rect in contextRects.items():
					HighlightStyle = highlighter._ContextStyles[context]
					# Before calculating logical coordinates,
					# make sure the rectangle falls within the highlighter window
					rect = rect.intersection(self.location)
					try:
						rect = rect.toLogical(self.handle)
					except RuntimeError:
						log.debugWarning("", exc_info=True)
					rect = rect.toClient(self.handle)
					try:
						rect = rect.expandOrShrink(HighlightStyle.margin)
					except RuntimeError:
						pass
					with winGDI.GDIPlusPen(
						HighlightStyle.color.toGDIPlusARGB(),
						HighlightStyle.width,
						HighlightStyle.style
					) as pen:
						winGDI.gdiPlusDrawRectangle(graphicsContext, pen, *rect.toLTWH())

	def refresh(self):
		winUser.user32.InvalidateRect(self.handle, None, True)
