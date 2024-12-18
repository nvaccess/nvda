from ctypes import Structure, byref, WinError, c_float
from ctypes.wintypes import COLORREF, MSG, RECT
import threading
import weakref

import wx

import api
from autoSettingsUtils.autoSettings import SupportedSettingType
from autoSettingsUtils.driverSetting import BooleanDriverSetting
import core
from documentBase import TextContainerObject
from gui.settingsDialogs import AutoSettingsMixin, SettingsPanel
from locationHelper import RectLTRB, RectLTWH
from logHandler import log
from mouseHandler import getTotalWidthAndHeightAndMinimumPosition
from NVDAObjects import NVDAObject
from vision.constants import Context
from vision import (
	providerBase,
	_isDebug,
)
from vision.util import getContextRect
from vision.visionHandlerExtensionPoints import EventExtensionPoints
from winAPI import _displayTracking
from .screenCurtain import MAGTRANSFORM, Magnification
from winAPI._displayTracking import _orientationState
from winAPI.messageWindow import WindowMessage
from windowUtils import CustomWindow
import winGDI
import winUser

_supportedContexts = {Context.FOCUS, Context.NAVIGATOR, Context.BROWSEMODE}

_contextOptionLabelsWithAccelerators = {
	# Translators: shown for a highlighter setting that toggles
	# highlighting the system focus.
	Context.FOCUS: _("Magnify system fo&cus"),
	# Translators: shown for a highlighter setting that toggles
	# highlighting the browse mode cursor.
	Context.BROWSEMODE: _("Magnify browse &mode cursor"),
	# Translators: shown for a highlighter setting that toggles
	# highlighting the navigator object.
	Context.NAVIGATOR: _("Magnify navigator &object"),
}


class MagnifierSettings(providerBase.VisionEnhancementProviderSettings):
	# Default settings for parameters
	magnifierFocus = True
	magnifierNavigator = True
	magnifierBrowseMode = True

	@classmethod
	def getId(cls) -> str:
		return "magnifier"

	@classmethod
	def getDisplayName(cls) -> str:
		# Translators: Description for NVDA's built-in screen highlighter.
		return _("Magnifier")

	def _get_supportedSettings(self) -> SupportedSettingType:
		return [
			BooleanDriverSetting(
				"magnifier%s" % (context[0].upper() + context[1:]),
				_contextOptionLabelsWithAccelerators[context],
				defaultVal=True,
			)
			for context in _supportedContexts
		]


# class VisionWindow(Protocol):
# 	def refresh(self) -> None:
# 		raise NotImplementedError


class MagnifierSettingsPanel(
	AutoSettingsMixin,
	SettingsPanel,
):
	pass


# Version X of magnifier window, simplified painting
# class MagnifierWindow(CustomWindow):
class MagnifierWindowX(CustomWindow):
	className = "Magnifier"
	windowName = "NVDA Magnifier Window Test"
	transparency = 0xFF  # Fully opaque
	windowStyle = winUser.WS_POPUP | winUser.WS_DISABLED
	extendedWindowStyle = (
		# Ensure that the window is on top of all other windows
		winUser.WS_EX_TOPMOST
		# A layered window ensures that L{transparentColor} will be considered transparent, when painted
		| winUser.WS_EX_LAYERED
		# Ensure that the window can't be activated when pressing alt+tab
		| winUser.WS_EX_NOACTIVATE
		# Make this a transparent window,
		# primarily for accessibility APIs to ignore this window when getting a window from a screen point
		| winUser.WS_EX_TRANSPARENT
	)
	transparentColor = 0x00  # Transparent
	magnifierWidth: int = 100
	magnifierHeight: int = 100
	targetLocation = RectLTWH(500, 500, 100, 100)
	magnifierLocation = RectLTWH(0, 0, 100, 100)

	def __init__(self, magnifier: weakref.ReferenceType["Magnifier"]):
		Magnification.MagInitialize()
		if _isDebug():
			log.debug("initializing NVDA Magnifier window")
		super().__init__(
			windowName=self.windowName,
			windowStyle=self.windowStyle,
			extendedWindowStyle=self.extendedWindowStyle,
		)
		winUser.SetLayeredWindowAttributes(
			self.handle,
			self.transparentColor,
			self.transparency,
			winUser.LWA_ALPHA | winUser.LWA_COLORKEY,
		)
		if not winUser.user32.UpdateWindow(self.handle):
			raise WinError()

	def windowProc(self, hwnd: int, msg: int, wParam: int, lParam: int):
		log.debug(f"received window proc message: {msg}")
		if msg == winUser.WM_PAINT:
			self._paint()
		elif msg == winUser.WM_DESTROY:
			Magnification.MagUninitialize()
			winUser.user32.PostQuitMessage(0)
		elif msg == winUser.WM_TIMER:
			self.refresh()
		elif msg == WindowMessage.DISPLAY_CHANGE:
			# wx might not be aware of the display change at this point
			core.callLater(100, self.updateLocationForDisplays)

	def _paint(self):
		log.debug("painting magnifier")
		winUser.user32.SetWindowPos(
			self.handle,
			winUser.HWND_TOPMOST,
			self.magnifierLocation.left,
			self.magnifierLocation.top,
			self.magnifierLocation.width,
			self.magnifierLocation.height,
			winUser.SWP_NOACTIVATE,
		)
		Magnification.MagSetWindowSource(
			self.handle,
			RECT(
				self.targetLocation.left,
				self.targetLocation.top,
				self.targetLocation.right,
				self.targetLocation.bottom,
			),
		)
		log.debug("painted magnifier")

	@classmethod
	def _get__wClass(cls) -> winUser.WNDCLASSEXW:
		wClass = super()._wClass
		# Redraw window when size changes
		wClass.style = winUser.CS_HREDRAW | winUser.CS_VREDRAW
		wClass.hbrBackground = winGDI.gdi32.CreateSolidBrush(COLORREF(cls.transparentColor))
		return wClass

	def refresh(self):
		self._paint()
		# winUser.user32.InvalidateRect(
		# 	self.handle,
		# 	# Rect: invalidate the whole window
		# 	None,
		# 	# Erase?
		# 	True,
		# )


# Version Y of MagnifierWindow, better tracking
# class MagnifierWindow(VisionWindow, CustomWindow):
class MagnifierWindowY(CustomWindow):
	className = "Magnifier"
	"""
	Class name for window required to match WC_MAGNIFIER
	https://learn.microsoft.com/en-us/windows/win32/winauto/magapi/wc-magnifier
	https://learn.microsoft.com/en-us/windows/win32/winauto/magapi/magapi-magnifier-styles

	TODO: make a constant for this class name
	"""
	windowName = "NVDA Magnifier Window"
	transparency = 0xFF  # Fully opaque
	windowStyle = winUser.WS_POPUP | winUser.WS_DISABLED
	extendedWindowStyle = (
		# Ensure that the window is on top of all other windows
		winUser.WS_EX_TOPMOST
		# A layered window ensures that L{transparentColor} will be considered transparent, when painted
		| winUser.WS_EX_LAYERED
		# Ensure that the window can't be activated when pressing alt+tab
		| winUser.WS_EX_NOACTIVATE
		# Make this a transparent window,
		# primarily for accessibility APIs to ignore this window when getting a window from a screen point
		| winUser.WS_EX_TRANSPARENT
	)
	transparentColor = 0x00  # Transparent
	magnifierWidth: int = 100
	magnifierHeight: int = 100
	targetLocation: RectLTWH
	magnifierLocation: RectLTWH
	magnifierRef: weakref.ReferenceType["Magnifier"]

	def __init__(self, magnifier: weakref.ReferenceType["Magnifier"]):
		if _isDebug():
			log.debug("initializing NVDA Magnifier window")
		super().__init__(
			windowName=self.windowName,
			windowStyle=self.windowStyle,
			extendedWindowStyle=self.extendedWindowStyle,
		)
		# TODO: add config for styles including inversion
		# https://learn.microsoft.com/en-us/windows/win32/winauto/magapi/magapi-magnifier-styles
		self.magnifierRef = weakref.ref(magnifier)
		winUser.SetLayeredWindowAttributes(
			self.handle,
			self.transparentColor,
			self.transparency,
			winUser.LWA_ALPHA | winUser.LWA_COLORKEY,
		)
		self.updateLocationForDisplays()
		if not winUser.user32.UpdateWindow(self.handle):
			raise WinError()

	def windowProc(self, hwnd: int, msg: int, wParam: int, lParam: int):
		if msg == winUser.WM_PAINT:
			self._paint()
			# Ensure the window is top most
			winUser.user32.SetWindowPos(
				self.handle,
				winUser.HWND_TOPMOST,
				0,
				0,
				0,
				0,
				winUser.SWP_NOACTIVATE | winUser.SWP_NOMOVE | winUser.SWP_NOSIZE,
			)
		elif msg == winUser.WM_DESTROY:
			winUser.user32.PostQuitMessage(0)
		elif msg == winUser.WM_TIMER:
			self.refresh()
		elif msg == WindowMessage.DISPLAY_CHANGE:
			# wx might not be aware of the display change at this point
			core.callLater(100, self.updateLocationForDisplays)

	def _paint(self):
		magnifier = self.magnifierRef()
		if not magnifier:
			# The magnifier instance died unexpectedly, kill the window as well
			winUser.user32.PostQuitMessage(0)
			return
		contextRects: dict[Context, RectLTWH] = {}
		for context in magnifier.enabledContexts:
			rect = magnifier.contextToRectMap.get(context)
			if not rect:
				continue
			elif context == Context.NAVIGATOR and contextRects.get(Context.FOCUS) == rect:
				# When the focus overlaps the navigator object, which is usually the case,
				# show a different highlight? style.
				# Focus is in contextRects, do not show the standalone focus highlight?
				contextRects.pop(Context.FOCUS)
				# Navigator object might be in contextRects as well
				contextRects.pop(Context.NAVIGATOR, None)
				context = Context.FOCUS_NAVIGATOR
			contextRects[context] = rect
		if not contextRects:
			return
		with winUser.paint(self.handle) as hdc:
			with winGDI.GDIPlusGraphicsContext(hdc) as graphicsContext:
				for context, rect in contextRects.items():
					Magnification.MagSetWindowSource(
						self.handle,
						RECT(
							self.targetLocation.left,
							self.targetLocation.top,
							self.targetLocation.right,
							self.targetLocation.bottom,
						),
					)
					# TODO: paint magnifier
					# rect = rect.intersection(self.targetLocation)
					# try:
					# 	rect = rect.toLogical(self.handle)
					# except RuntimeError:
					# 	log.debugWarning("", exc_info=True)
					# rect = rect.toClient(self.handle)
					# with winGDI.GDIPlusPen(
					# 	0,
					# 	5,
					# 	winGDI.DashStyleSolid,
					# ) as pen:
					# 	winGDI.gdiPlusDrawRectangle(graphicsContext, pen, *rect.toLTWH())

	def updateLocationForDisplays(self):
		# Generic - refactor:
		if _isDebug():
			log.debug("Updating NVDA Magnifier window location for displays")
		displays = [wx.Display(i).GetGeometry() for i in range(wx.Display.GetCount())]
		screenWidth, screenHeight, minPos = getTotalWidthAndHeightAndMinimumPosition(displays)
		# Hack: Windows has a "feature" that will stop desktop shortcut hotkeys from working
		# when a window is full screen.
		# Removing one line of pixels from the bottom of the screen will fix this.
		self.targetLocation = RectLTWH(minPos.x, minPos.y, screenWidth, screenHeight - 1)

		# Place window before or after the focused object depending on screen width.
		if (self.targetLocation.left + screenWidth + self.magnifierWidth) > _orientationState.width:
			magLeft = self.targetLocation.left - self.magnifierWidth
		else:
			magLeft = self.targetLocation.left + screenWidth
		if (self.targetLocation.top + screenHeight + self.magnifierHeight) > _orientationState.height:
			magTop = self.targetLocation.top - self.magnifierHeight
		else:
			magTop = self.targetLocation.top + screenHeight

		# Generic - refactor:
		self.magnifierLocation = RectLTWH(magLeft, magTop, self.magnifierWidth, self.magnifierHeight)
		if not winUser.user32.SetWindowPos(
			self.handle,
			winUser.HWND_TOPMOST,
			self.magnifierLocation.left,
			self.magnifierLocation.top,
			self.magnifierLocation.width,
			self.magnifierLocation.height,
			winUser.SWP_NOACTIVATE,
		):
			raise WinError()
		winUser.user32.ShowWindow(self.handle, winUser.SW_SHOWNA)

	@classmethod
	def _get__wClass(cls) -> winUser.WNDCLASSEXW:
		wClass = super()._wClass
		# Redraw window when size changes
		wClass.style = winUser.CS_HREDRAW | winUser.CS_VREDRAW
		wClass.hbrBackground = winGDI.gdi32.CreateSolidBrush(COLORREF(cls.transparentColor))
		return wClass

	def refresh(self):
		winUser.user32.InvalidateRect(
			self.handle,
			# Rect: invalidate the whole window
			None,
			# Erase?
			True,
		)

WindowClassName = "MagnifierWindow"
WindowTitle = "Screen Magnifier Sample"
WC_MAGNIFIER = "Magnifier"
RESTOREDWINDOWSTYLES = (
	winUser.WS_SIZEBOX
	| winUser.WS_SYSMENU
	| winUser.WS_CLIPCHILDREN
	| winUser.WS_CAPTION
	| winUser.WS_MAXIMIZEBOX
)


class HostWindow(CustomWindow):
	className = WindowClassName
	windowName = WindowTitle
	windowsStyle = RESTOREDWINDOWSTYLES
	extendedWindowStyle = (
		# Ensure that the window is on top of all other windows
		winUser.WS_EX_TOPMOST
		# A layered window ensures that L{transparentColor} will be considered transparent, when painted
		| winUser.WS_EX_LAYERED
	)

	def __init__(self, magnificationFactor: int = 2):
		super().__init__(
			windowName=self.windowName,
			windowStyle=self.windowsStyle,
			extendedWindowStyle=self.extendedWindowStyle,
			parent=None,
		)
		winUser.SetLayeredWindowAttributes(
			self.handle,
			0x00,
			0xFF,
			winUser.LWA_ALPHA,
		)
		if not winUser.user32.SetWindowPos(
			self.handle,
			winUser.HWND_TOPMOST,
			self.targetRect.left,
			self.targetRect.top,
			self.targetRect.width,
			int(self.targetRect.height),
			winUser.SWP_NOACTIVATE | winUser.SWP_NOMOVE | winUser.SWP_NOSIZE,
		):
			raise WinError()
		if not winUser.user32.UpdateWindow(self.handle):
			raise WinError()
		self.magnifierWindow = MagnifierWindow(self, magnificationFactor)

	@property
	def targetRect(self) -> RectLTRB:
		# Top quarter of screen
		return RectLTRB(
			0,
			0,
			_displayTracking._orientationState.width,
			_displayTracking._orientationState.height / 4,
		)

	def windowProc(self, hwnd: int, msg: int, wParam: int, lParam: int):
		log.debug(f"received window proc message: {msg}")


## Closest copy of Windows magnifier sample code
class MagnifierWindow(CustomWindow):
	className = WC_MAGNIFIER
	windowName = "MagnifierWindow"
	windowStyle = winUser.WS_CHILD | winUser.MS_SHOWMAGNIFIEDCURSOR | winUser.WS_VISIBLE

	def __init__(self, hostWindow: HostWindow, magnificationFactor: int = 2):
		self.hostWindow = hostWindow
		self.magnificationFactor = magnificationFactor
		if _isDebug():
			log.debug("initializing NVDA Magnifier window")
		super().__init__(
			windowName=self.windowName,
			windowStyle=self.windowStyle,
			parent=hostWindow.handle,
		)

		magWindowRect = self.magWindowRect
		if not winUser.user32.SetWindowPos(
			self.handle,
			winUser.HWND_TOPMOST,
			0,
			0,
			magWindowRect.width,
			magWindowRect.height,
			winUser.SWP_NOACTIVATE | winUser.SWP_NOMOVE | winUser.SWP_NOSIZE,
		):
			raise WinError()
		if not winUser.user32.UpdateWindow(self.handle):
			raise WinError()

		Magnification.MagSetWindowSource(self.handle, RECT(200, 200, 700, 700))
		Magnification.MagSetWindowTransform(self.handle, MAGTRANSFORM(self.magnificationFactor))

	@property
	def magWindowRect(self) -> RectLTWH:
		r = winUser.getClientRect(self.hostWindow.handle)
		return RectLTRB(
			r.left,
			r.top,
			r.right,
			r.bottom,
		).toLTWH()

	def windowProc(self, hwnd: int, msg: int, wParam: int, lParam: int):
		log.debug(f"received window proc message: {msg}")


class Magnifier(providerBase.VisionEnhancementProvider):
	_refreshInterval = 100
	customWindowClass = HostWindow
	_settings = MagnifierSettings()
	_window: customWindowClass | None = None
	enabledContexts: tuple[Context]  # type info for autoprop: L{_get_enableContexts}
	_magnifierThread: threading.Thread
	_magnifierRunningEvent: threading.Event

	@classmethod  # override
	def getSettings(cls) -> MagnifierSettings:
		return cls._settings

	@classmethod  # override
	def getSettingsPanelClass(cls) -> MagnifierSettingsPanel:
		"""Returns the class to be used in order to construct a settings panel for the provider.
		@remarks: When None is returned, L{gui.settingsDialogs.VisionProviderSubPanel_Wrapper} is used.
		"""
		return MagnifierSettingsPanel

	@classmethod  # override
	def canStart(cls) -> bool:
		return True

	def registerEventExtensionPoints(  # override
		self,
		extensionPoints: EventExtensionPoints,
	) -> None:
		extensionPoints.post_focusChange.register(self.handleFocusChange)
		extensionPoints.post_reviewMove.register(self.handleReviewMove)
		extensionPoints.post_browseModeMove.register(self.handleBrowseModeMove)

	def __init__(self):
		super().__init__()
		log.debug("Starting Magnifier")
		self.contextToRectMap = {}
		winGDI.gdiPlusInitialize()
		self._magnifierThread = threading.Thread(
			name=f"{self.__class__.__module__}.{self.__class__.__qualname__}",
			target=self._run,
			daemon=True,
		)
		self._magnifierRunningEvent = threading.Event()
		self._magnifierThread.start()
		# Make sure the thread doesn't exit early.
		waitResult = self._magnifierRunningEvent.wait(0.2)
		if waitResult is False or not self._magnifierThread.is_alive():
			raise RuntimeError("Magnifier thread wasn't able to initialize correctly")
		Magnification.MagInitialize()

	def terminate(self):
		Magnification.MagUninitialize()
		log.debug("Terminating Magnifier")
		if self._magnifierThread and self._window and self._window.handle:
			if not winUser.user32.PostThreadMessageW(self._magnifierThread.ident, winUser.WM_QUIT, 0, 0):
				raise WinError()
			else:
				self._magnifierThread.join()
			self._magnifierThread = None
		winGDI.gdiPlusTerminate()
		self.contextToRectMap.clear()
		super().terminate()

	def _run(self):
		try:
			if _isDebug():
				log.debug("Starting Magnifier thread")

			self._window = self.customWindowClass(self)
			timer = winUser.WinTimer(self._window.handle, 0, self._refreshInterval, None)
			self._magnifierRunningEvent.set()  # notify main thread that initialisation was successful
			msg = MSG()
			while (res := winUser.getMessage(byref(msg), None, 0, 0)) > 0:
				winUser.user32.TranslateMessage(byref(msg))
				winUser.user32.DispatchMessageW(byref(msg))
			if res == -1:
				# See the return value section of
				# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getmessage
				raise WinError()
			if _isDebug():
				log.debug("Quit message received on Magnifier thread")
			timer.terminate()
			self._window.destroy()
		except Exception:
			log.exception("Exception in Magnifier thread")

	def updateContextRect(
		self,
		context: Context,
		rect: RectLTRB | None = None,
		obj: TextContainerObject | None = None,
	):
		"""Updates the position rectangle of the magnifier for the specified context.
		If rect is specified, the method directly writes the rectangle to the contextToRectMap.
		Otherwise, it will call L{getContextRect}
		"""
		if context not in self.enabledContexts:
			return
		if rect is None:
			try:
				rect = getContextRect(context, obj=obj)
			except (LookupError, NotImplementedError, RuntimeError, TypeError):
				rect = None
		self.contextToRectMap[context] = rect

	def handleFocusChange(self, obj: NVDAObject):
		self.updateContextRect(context=Context.FOCUS, obj=obj)
		if not api.isObjectInActiveTreeInterceptor(obj):
			self.contextToRectMap.pop(Context.BROWSEMODE, None)
		else:
			self.handleBrowseModeMove()

	def handleReviewMove(self, context: Context):
		self.updateContextRect(context=Context.NAVIGATOR)

	def handleBrowseModeMove(self, obj: NVDAObject | None = None):
		self.updateContextRect(context=Context.BROWSEMODE)

	def refresh(self):
		"""Refreshes the screen positions of the enabled magnifier."""
		if self._window and self._window.handle:
			self._window.refresh()

	def _get_enabledContexts(self) -> tuple[Context]:
		"""Gets the contexts for which the magnifier is enabled."""
		return tuple(
			context
			for context in _supportedContexts
			if getattr(self.getSettings(), "magnifier%s" % (context[0].upper() + context[1:]))
		)


VisionEnhancementProvider = Magnifier
