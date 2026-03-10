# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Windowed magnifier overlay using Win32 native windows.

Provides a magnifier overlay window with three key properties:
1. Invisible to NVDA and accessibility APIs (WS_EX_TRANSPARENT + WS_EX_TOOLWINDOW)
2. Excluded from screen capture to prevent feedback loops (SetWindowDisplayAffinity)
3. Click-through so it doesn't interfere with user interaction (WS_EX_TRANSPARENT + WS_DISABLED)
"""

import ctypes
import ctypes.wintypes

from logHandler import log
import winUser
import winGDI
import winBindings.gdi32 as gdi32
from winBindings import user32
from windowUtils import CustomWindow

from .types import MagnifierParameters, WindowMagnifierParameters, Filter
from .filterHandler import applyBitmapFilter, getBlitRasterOp

#: Window Display Affinity: exclude from screen capture (Windows 10 2004+)
WDA_EXCLUDEFROMCAPTURE: int = 0x00000011
#: WM_PAINT message
WM_PAINT: int = winUser.WM_PAINT
#: WM_DESTROY message
WM_DESTROY: int = winUser.WM_DESTROY
#: WM_ERASEBKGND message
WM_ERASEBKGND: int = 0x0014
#: SetStretchBltMode: high-quality image stretching mode
HALFTONE: int = 4

_user32_dll = ctypes.windll.user32
_gdi32_dll = ctypes.windll.gdi32

_user32_dll.SetWindowDisplayAffinity.argtypes = [ctypes.wintypes.HWND, ctypes.wintypes.DWORD]
_user32_dll.SetWindowDisplayAffinity.restype = ctypes.wintypes.BOOL

_gdi32_dll.SetStretchBltMode.argtypes = [ctypes.wintypes.HDC, ctypes.c_int]
_gdi32_dll.SetStretchBltMode.restype = ctypes.c_int

#: DrawIconEx flag: draw cursor with its normal mask and colour
DI_NORMAL: int = 0x0003
#: CURSORINFO.flags value: the cursor is showing
CURSOR_SHOWING: int = 0x00000001
#: GetSystemMetrics index: default cursor width
SM_CXCURSOR: int = 13
#: GetSystemMetrics index: default cursor height
SM_CYCURSOR: int = 14


class ICONINFO(ctypes.Structure):
	_fields_ = [
		("fIcon", ctypes.wintypes.BOOL),
		("xHotspot", ctypes.wintypes.DWORD),
		("yHotspot", ctypes.wintypes.DWORD),
		("hbmMask", ctypes.wintypes.HBITMAP),
		("hbmColor", ctypes.wintypes.HBITMAP),
	]


class CURSORINFO(ctypes.Structure):
	_fields_ = [
		("cbSize", ctypes.wintypes.DWORD),
		("flags", ctypes.wintypes.DWORD),
		("hCursor", ctypes.wintypes.HANDLE),
		("ptScreenPos", ctypes.wintypes.POINT),
	]


_user32_dll.GetCursorInfo.argtypes = [ctypes.POINTER(CURSORINFO)]
_user32_dll.GetCursorInfo.restype = ctypes.wintypes.BOOL

_user32_dll.GetIconInfo.argtypes = [ctypes.wintypes.HANDLE, ctypes.POINTER(ICONINFO)]
_user32_dll.GetIconInfo.restype = ctypes.wintypes.BOOL

_user32_dll.DrawIconEx.argtypes = [
	ctypes.wintypes.HDC,
	ctypes.c_int,
	ctypes.c_int,
	ctypes.wintypes.HANDLE,
	ctypes.c_int,
	ctypes.c_int,
	ctypes.c_uint,
	ctypes.wintypes.HBRUSH,
	ctypes.c_uint,
]
_user32_dll.DrawIconEx.restype = ctypes.wintypes.BOOL

_user32_dll.GetSystemMetrics.argtypes = [ctypes.c_int]
_user32_dll.GetSystemMetrics.restype = ctypes.c_int


class MagnifierOverlayWindow(CustomWindow):
	"""Win32 native overlay window for displaying magnified screen content.

	This window is:
	- **Invisible to NVDA**: ``WS_EX_TRANSPARENT`` and ``WS_EX_TOOLWINDOW``
	  make the window ignored by accessibility APIs and absent from the taskbar.
	- **Excluded from screen capture**: ``SetWindowDisplayAffinity(WDA_EXCLUDEFROMCAPTURE)``
	  prevents screen-capture APIs (including the Windows Magnifier) from seeing
	  this window, avoiding infinite feedback loops.
	- **Click-through**: the combination of ``WS_DISABLED`` and ``WS_EX_TRANSPARENT``
	  lets all mouse events fall through to the window beneath.
	"""

	className = "NVDAMagnifierOverlay"

	@classmethod
	def _get__wClass(cls):
		wClass = super()._wClass
		wClass.style = winUser.CS_HREDRAW | winUser.CS_VREDRAW
		return wClass

	def __init__(self, windowParams: WindowMagnifierParameters):
		"""Create the overlay window and configure its special properties.

		:param windowParams: Title, size and position for the overlay.
		"""
		super().__init__(
			windowName=windowParams.title,
			windowStyle=winUser.WS_POPUP | winUser.WS_DISABLED,
			extendedWindowStyle=(
				winUser.WS_EX_TOPMOST
				| winUser.WS_EX_LAYERED
				| winUser.WS_EX_NOACTIVATE
				| winUser.WS_EX_TRANSPARENT
				| winUser.WS_EX_TOOLWINDOW
			),
		)

		self._windowWidth: int = windowParams.windowSize.width
		self._windowHeight: int = windowParams.windowSize.height

		# GDI resources for the captured screen region
		self._captureDC = None
		self._captureBitmap = None
		self._oldCaptureBitmap = None
		self._captureWidth: int = 0
		self._captureHeight: int = 0
		self._currentFilter: Filter = Filter.NORMAL

		# Cursor overlay state (updated at each capture frame)
		self._cursorHandle = None
		self._cursorWindowX: int = -1
		self._cursorWindowY: int = -1
		self._cursorHotspotX: int = 0
		self._cursorHotspotY: int = 0

		# Position and size the window
		x, y = windowParams.windowPosition
		user32.SetWindowPos(
			self.handle,
			winUser.HWND_TOPMOST,
			x,
			y,
			self._windowWidth,
			self._windowHeight,
			winUser.SWP_NOACTIVATE,
		)

		# Make the window fully opaque via the layered-window mechanism
		winUser.SetLayeredWindowAttributes(self.handle, 0, 255, winUser.LWA_ALPHA)

		# Exclude from screen capture to prevent feedback loops
		if not _user32_dll.SetWindowDisplayAffinity(self.handle, WDA_EXCLUDEFROMCAPTURE):
			log.warning(
				"SetWindowDisplayAffinity failed – overlay window may cause screen-capture feedback",
			)

		# Show the window without activating it
		user32.ShowWindow(self.handle, winUser.SW_SHOWNA)
		user32.UpdateWindow(self.handle)

	def windowProc(self, hwnd: int, msg: int, wParam: int, lParam: int):
		if msg == WM_PAINT:
			self._paint()
			return 0
		elif msg == WM_ERASEBKGND:
			# Prevent background erasure to avoid flicker
			return 1
		elif msg == WM_DESTROY:
			self._cleanupGDI()
			return 0
		return None

	def updateContent(
		self,
		captureX: int,
		captureY: int,
		captureW: int,
		captureH: int,
		filterType: Filter = Filter.NORMAL,
	) -> None:
		"""Capture a screen region, optionally apply a colour filter, then repaint.

		The captured region is stored in an off-screen memory DC at its native
		resolution.  Scaling to the window size happens during ``WM_PAINT`` via
		``StretchBlt``, keeping the capture step lightweight.

		:param captureX: Screen X of the region to capture.
		:param captureY: Screen Y of the region to capture.
		:param captureW: Width of the region to capture (pixels).
		:param captureH: Height of the region to capture (pixels).
		:param filterType: Colour filter to apply (NORMAL, GRAYSCALE, INVERTED).
		"""
		if captureW <= 0 or captureH <= 0:
			return

		screenDC = user32.GetDC(0)
		try:
			# (Re-)create the capture DC / bitmap when the capture size changes
			if self._captureWidth != captureW or self._captureHeight != captureH:
				self._cleanupGDI()
				self._captureDC = gdi32.CreateCompatibleDC(screenDC)
				self._captureBitmap = gdi32.CreateCompatibleBitmap(screenDC, captureW, captureH)
				self._oldCaptureBitmap = gdi32.SelectObject(self._captureDC, self._captureBitmap)
				self._captureWidth = captureW
				self._captureHeight = captureH

			# Copy the screen region into the off-screen bitmap
			gdi32.StretchBlt(
				self._captureDC,
				0,
				0,
				captureW,
				captureH,
				screenDC,
				captureX,
				captureY,
				captureW,
				captureH,
				winGDI.SRCCOPY,
			)
		finally:
			user32.ReleaseDC(0, screenDC)

		applyBitmapFilter(filterType, self._captureDC, self._captureBitmap, captureW, captureH)

		self._currentFilter = filterType

		# Snapshot cursor position relative to this capture frame
		self._snapshotCursor(captureX, captureY, captureW, captureH)

		# Trigger a WM_PAINT
		user32.InvalidateRect(self.handle, None, False)

	def _paint(self) -> None:
		"""StretchBlt the captured bitmap to the window's client area."""
		with winUser.paint(self.handle) as hdc:
			if self._captureDC and self._captureWidth > 0 and self._captureHeight > 0:
				_gdi32_dll.SetStretchBltMode(hdc, HALFTONE)
				rop = getBlitRasterOp(self._currentFilter)
				gdi32.StretchBlt(
					hdc,
					0,
					0,
					self._windowWidth,
					self._windowHeight,
					self._captureDC,
					0,
					0,
					self._captureWidth,
					self._captureHeight,
					rop,
				)
				# Draw the cursor on top of the magnified content
				self._paintCursor(hdc)

	def _snapshotCursor(
		self,
		captureX: int,
		captureY: int,
		captureW: int,
		captureH: int,
	) -> None:
		"""Record the current cursor position in window coordinates.

		Called once per frame inside :meth:`updateContent`.  If the cursor is
		outside the capture area, or invisible, ``_cursorHandle`` is set to
		``None`` so :meth:`_paintCursor` is a no-op.
		"""
		ci = CURSORINFO()
		ci.cbSize = ctypes.sizeof(CURSORINFO)
		if not _user32_dll.GetCursorInfo(ctypes.byref(ci)) or not (ci.flags & CURSOR_SHOWING):
			self._cursorHandle = None
			return

		cx, cy = ci.ptScreenPos.x, ci.ptScreenPos.y
		relX = cx - captureX
		relY = cy - captureY

		if relX < 0 or relY < 0 or relX >= captureW or relY >= captureH:
			# Cursor is outside the captured area
			self._cursorHandle = None
			return

		# Map cursor position to window (scaled) coordinates
		scaleX = self._windowWidth / captureW
		scaleY = self._windowHeight / captureH
		self._cursorWindowX = int(relX * scaleX)
		self._cursorWindowY = int(relY * scaleY)
		self._cursorHandle = ci.hCursor

		# Retrieve hotspot so we can draw cursor anchored at its click point
		ii = ICONINFO()
		if _user32_dll.GetIconInfo(ci.hCursor, ctypes.byref(ii)):
			self._cursorHotspotX = int(ii.xHotspot * scaleX)
			self._cursorHotspotY = int(ii.yHotspot * scaleY)
			# GetIconInfo allocates bitmaps – always free them
			if ii.hbmMask:
				gdi32.DeleteObject(ii.hbmMask)
			if ii.hbmColor:
				gdi32.DeleteObject(ii.hbmColor)
		else:
			self._cursorHotspotX = 0
			self._cursorHotspotY = 0

	def _paintCursor(self, hdc) -> None:
		"""Draw the cursor glyph on *hdc* using the state from :meth:`_snapshotCursor`."""
		if not self._cursorHandle or self._cursorWindowX < 0:
			return

		if self._captureWidth <= 0:
			return

		scaleFactor = self._windowWidth / self._captureWidth
		sysCursorW = _user32_dll.GetSystemMetrics(SM_CXCURSOR)
		sysCursorH = _user32_dll.GetSystemMetrics(SM_CYCURSOR)
		scaledW = max(1, int(sysCursorW * scaleFactor))
		scaledH = max(1, int(sysCursorH * scaleFactor))

		drawX = self._cursorWindowX - self._cursorHotspotX
		drawY = self._cursorWindowY - self._cursorHotspotY

		_user32_dll.DrawIconEx(
			hdc,
			drawX,
			drawY,
			self._cursorHandle,
			scaledW,
			scaledH,
			0,
			None,
			DI_NORMAL,
		)

	def _cleanupGDI(self) -> None:
		"""Release the off-screen capture DC, bitmap and associated objects."""
		try:
			if self._oldCaptureBitmap and self._captureDC:
				gdi32.SelectObject(self._captureDC, self._oldCaptureBitmap)
				self._oldCaptureBitmap = None
			if self._captureBitmap:
				gdi32.DeleteObject(self._captureBitmap)
				self._captureBitmap = None
			if self._captureDC:
				gdi32.DeleteDC(self._captureDC)
				self._captureDC = None
		except (ctypes.ArgumentError, OSError):
			# Guard against invalid handles (e.g. mock objects during tests)
			pass
		self._captureWidth = 0
		self._captureHeight = 0

	def destroy(self) -> None:
		"""Destroy the window and free all GDI resources."""
		self._cleanupGDI()
		if hasattr(self, "_classAtom"):
			CustomWindow.destroy(self)


class WindowedMagnifier:
	"""Mixin for magnifiers that display content in a separate overlay window.

	Uses a native Win32 overlay window (:class:`MagnifierOverlayWindow`) to
	ensure the magnified view is:

	* invisible to NVDA and other accessibility tools,
	* excluded from screen capture (no infinite feedback with the system magnifier),
	* fully click-through.
	"""

	def __init__(self, windowMagnifierParameters: WindowMagnifierParameters):
		"""Create the overlay window.

		:param windowMagnifierParameters: Configuration for the overlay window.
		"""
		self.windowMagnifierParameters = windowMagnifierParameters
		self._overlayWindow: MagnifierOverlayWindow | None = MagnifierOverlayWindow(
			windowMagnifierParameters,
		)

	def _setContent(self, magnifierParameters: MagnifierParameters, zoomLevel: float) -> None:
		"""Capture screen content and display it in the overlay window.

		:param magnifierParameters: What area to capture and which filter to apply.
		:param zoomLevel: Current zoom level (already factored into *magnifierParameters*).
		"""
		if not self._overlayWindow or not self._overlayWindow.handle:
			log.debug("No overlay window available for content update")
			return

		self._overlayWindow.updateContent(
			captureX=magnifierParameters.coordinates.x,
			captureY=magnifierParameters.coordinates.y,
			captureW=magnifierParameters.magnifierSize.width,
			captureH=magnifierParameters.magnifierSize.height,
			filterType=magnifierParameters.filter,
		)

	def _destroyWindow(self) -> None:
		"""Destroy the overlay window and release all resources."""
		if self._overlayWindow:
			self._overlayWindow.destroy()
			self._overlayWindow = None
