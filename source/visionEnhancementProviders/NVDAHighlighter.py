#visionEnhancementProviders/NVDAHighlighter.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018-2019 NV Access Limited, Babbage B.V., Takuya Nishimoto

"""Default highlighter based on wx."""

from vision import Highlighter, CONTEXT_FOCUS, CONTEXT_NAVIGATOR, CONTEXT_CARET
import wx
import gui
import api
from ctypes.wintypes import COLORREF
import winUser
from logHandler import log
from mouseHandler import getTotalWidthAndHeightAndMinimumPosition
import cursorManager
from locationHelper import RectLTRB
import config
from collections import namedtuple

# Highlighter specific contexts
#: Context for overlapping focus and navigator objects
CONTEXT_FOCUS_NAVIGATOR = "focusNavigatorOverlap"

class ContextStyle(namedtuple("ContextStyle", ("color", "width", "style", "margin"))):
	pass

class VisionEnhancementProvider(Highlighter):
	name = "NVDAHighlighter"
	# Translators: Description for NVDA's built-in screen highlighter.
	description = _("NVDA Highlighter")
	supportedHighlightContexts = (CONTEXT_FOCUS, CONTEXT_NAVIGATOR, CONTEXT_CARET)
	_contextStyles = {
		CONTEXT_FOCUS: ContextStyle(wx.Colour(0x03, 0x36, 0xff, 0xff), 5, wx.PENSTYLE_SHORT_DASH, 5),
		CONTEXT_NAVIGATOR: ContextStyle(wx.Colour(0xff, 0x02, 0x66, 0xff), 5, wx.PENSTYLE_SOLID, 5),
		CONTEXT_FOCUS_NAVIGATOR: ContextStyle(wx.Colour(0x03, 0x36, 0xff, 0xff), 5, wx.PENSTYLE_SOLID, 5),
		CONTEXT_CARET: ContextStyle(wx.Colour(0xff, 0xde, 0x03, 0xff), 2, wx.PENSTYLE_SOLID, 0),
	}
	_refreshInterval = 100

	def __init__(self, *roles):
		self.window = None
		self._refreshTimer = None
		super(Highlighter, self).__init__(*roles)

	def initializeHighlighter(self):
		super(VisionEnhancementProvider, self).initializeHighlighter()
		self.window = HighlightWindow(self)
		self._refreshTimer = gui.NonReEntrantTimer(self.refresh)
		self._refreshTimer.Start(self._refreshInterval)

	def terminateHighlighter(self):
		if self._refreshTimer:
			self._refreshTimer.Stop()
			self._refreshTimer = None
		if self.window:
			self.window.Destroy()
			self.window = None
		super(VisionEnhancementProvider, self).terminateHighlighter()

	def updateContextRect(self, context, rect=None, obj=None):
		super(VisionEnhancementProvider, self).updateContextRect(context, rect, obj)
		# Though a refresh happens once per core cycle,
		# force a refresh for a change to avoid delays.
		self.refresh()

	def refresh(self):
		# Trigger a refresh of the highlight window, which will call onPaint
		if self.window:
			self.window.Refresh()

	def onPaint(self, event):
		window= event.GetEventObject()
		dc = wx.PaintDC(window)
		dc.Background = wx.TRANSPARENT_BRUSH
		# Note: Not sure whether this clearing is strictly necessary here.
		dc.Clear()
		dc.Brush = wx.TRANSPARENT_BRUSH
		contextRects = {}
		for context in self.enabledHighlightContexts:
			rect = self.contextToRectMap.get(context)
			if not rect:
				continue
			if context == CONTEXT_CARET and not isinstance(api.getCaretObject(), cursorManager.CursorManager):
				# Non virtual carets are currently not supported.
				# As they are physical, they are visible by themselves.
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
		for context, rect in contextRects.items():
			contextStyle = self._contextStyles[context]
			dc.Pen = wx.ThePenList.FindOrCreatePen(contextStyle.color, contextStyle.width, contextStyle.style)
			try:
				rect = rect.expandOrShrink(contextStyle.margin).toClient(window.Handle).toLogical(window.Handle)
			except RuntimeError:
				pass
			dc.DrawRectangle(*rect.toLTWH())

class HighlightWindow(wx.Frame):
	transparency = 0xff

	def updateLocationForDisplays(self):
		displays = [ wx.Display(i).GetGeometry() for i in xrange(wx.Display.GetCount()) ]
		screenWidth, screenHeight, minPos = getTotalWidthAndHeightAndMinimumPosition(displays)
		self.Position = minPos
		# Hack: Windows has a "feature" that will stop desktop shortcut hotkeys from working when a window is full screen.
		# Removing one line of pixels from the bottom of the screen will fix this.
		self.Size = (screenWidth, screenHeight -1)

	def __init__(self, highlighter):
		super(HighlightWindow, self).__init__(gui.mainFrame, style=wx.NO_BORDER | wx.STAY_ON_TOP | wx.FULL_REPAINT_ON_RESIZE | wx.FRAME_NO_TASKBAR)
		self.updateLocationForDisplays()
		self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
		exstyle = winUser.getExtendedWindowStyle(self.Handle) | winUser.WS_EX_LAYERED
		winUser.setExtendedWindowStyle(self.Handle, exstyle)
		winUser.SetLayeredWindowAttributes(self.Handle, None, self.transparency, winUser.LWA_ALPHA | winUser.LWA_COLORKEY)
		self.Bind(wx.EVT_PAINT, highlighter.onPaint)
		self.ShowWithoutActivating()
		wx.CallAfter(self.Disable)

