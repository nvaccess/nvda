from ctypes import WinError
from ctypes.wintypes import RECT

from locationHelper import RectLTRB, RectLTWH
from logHandler import log
from vision import (
	_isDebug,
)
from .screenCurtain import MAGTRANSFORM, Magnification
from winAPI import _displayTracking
from windowUtils import CustomWindow
import winUser

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
			0, 0, _displayTracking._orientationState.width, _displayTracking._orientationState.height / 4
		)

	def windowProc(self, hwnd: int, msg: int, wParam: int, lParam: int):
		log.debug(f"received window proc message: {msg}")


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
			magWindowRect.left,
			magWindowRect.top,
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
