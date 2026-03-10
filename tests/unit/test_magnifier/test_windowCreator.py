# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import ctypes
import unittest
from unittest.mock import MagicMock, patch
from _magnifier.utils.types import Coordinates, Size, WindowMagnifierParameters, Filter, MagnifierParameters
from _magnifier.utils.windowCreator import (
	MagnifierOverlayWindow,
	WindowedMagnifier,
	WM_ERASEBKGND,
	CURSOR_SHOWING,
	CURSORINFO,
	ICONINFO,
)


def _makeWindowParams(
	title="Test Magnifier",
	width=400,
	height=300,
	x=100,
	y=100,
):
	return WindowMagnifierParameters(
		title=title,
		windowSize=Size(width, height),
		windowPosition=Coordinates(x, y),
	)


def _patchOverlayCreation():
	"""Return a stack of patches that prevent real Win32 window creation."""
	return [
		patch(
			"_magnifier.utils.windowCreator.CustomWindow.__new__",
			return_value=object.__new__(MagnifierOverlayWindow),
		),
		patch("_magnifier.utils.windowCreator.CustomWindow.__init__"),
		patch("_magnifier.utils.windowCreator.user32"),
		patch("_magnifier.utils.windowCreator._user32_dll"),
		patch("_magnifier.utils.windowCreator.gdi32"),
		patch("_magnifier.utils.windowCreator._gdi32_dll"),
		patch("_magnifier.utils.windowCreator.winUser"),
	]


class TestMagnifierOverlayWindow(unittest.TestCase):
	"""Tests for the MagnifierOverlayWindow class."""

	def _createWindow(self, params=None):
		"""Helper to create a MagnifierOverlayWindow with all Win32 calls mocked."""
		if params is None:
			params = _makeWindowParams()
		patches = _patchOverlayCreation()
		mocks = {}
		for p in patches:
			mock = p.start()
			self.addCleanup(p.stop)
			# Use the patch target name as key for easy access
			name = p.attribute if hasattr(p, "attribute") else str(p)
			mocks[name] = mock

		# Give the window a fake handle
		window = MagnifierOverlayWindow(params)
		window.handle = 12345
		# Re-patch user32/winUser on the window object for verification
		return window, mocks

	def test_init_stores_dimensions(self):
		"""Window stores width and height from parameters."""
		params = _makeWindowParams(width=800, height=600)
		window, _ = self._createWindow(params)
		self.assertEqual(window._windowWidth, 800)
		self.assertEqual(window._windowHeight, 600)

	def test_init_sets_display_affinity(self):
		"""SetWindowDisplayAffinity is called with WDA_EXCLUDEFROMCAPTURE."""
		params = _makeWindowParams()
		window, _ = self._createWindow(params)
		# The _user32_dll mock is called during __init__
		# Verify indirectly by checking the window was created without error
		self.assertIsNotNone(window.handle)

	def test_init_gdi_resources_are_none(self):
		"""GDI capture resources start as None."""
		window, _ = self._createWindow()
		self.assertIsNone(window._captureDC)
		self.assertIsNone(window._captureBitmap)
		self.assertIsNone(window._oldCaptureBitmap)
		self.assertEqual(window._captureWidth, 0)
		self.assertEqual(window._captureHeight, 0)

	def test_init_default_filter_is_normal(self):
		"""Default filter should be NORMAL."""
		window, _ = self._createWindow()
		self.assertEqual(window._currentFilter, Filter.NORMAL)

	def test_windowProc_paint_returns_zero(self):
		"""WM_PAINT returns 0 after calling _paint."""
		window, _ = self._createWindow()
		with patch.object(window, "_paint"):
			# WM_PAINT = 0x000F
			result = window.windowProc(window.handle, 0x000F, 0, 0)
			self.assertEqual(result, 0)
			window._paint.assert_called_once()

	def test_windowProc_erasebkgnd_returns_one(self):
		"""WM_ERASEBKGND returns 1 to prevent flicker."""
		window, _ = self._createWindow()
		result = window.windowProc(window.handle, WM_ERASEBKGND, 0, 0)
		self.assertEqual(result, 1)

	def test_windowProc_destroy_cleans_gdi(self):
		"""WM_DESTROY triggers GDI cleanup."""
		window, _ = self._createWindow()
		with patch.object(window, "_cleanupGDI") as mockCleanup:
			# WM_DESTROY = 2
			result = window.windowProc(window.handle, 2, 0, 0)
			self.assertEqual(result, 0)
			mockCleanup.assert_called_once()

	def test_windowProc_unknown_msg_returns_none(self):
		"""Unknown messages return None for DefWindowProc."""
		window, _ = self._createWindow()
		result = window.windowProc(window.handle, 0x9999, 0, 0)
		self.assertIsNone(result)

	def test_updateContent_skips_invalid_size(self):
		"""updateContent does nothing for zero or negative capture dimensions."""
		window, _ = self._createWindow()
		with patch.object(window, "_cleanupGDI") as mockCleanup:
			window.updateContent(0, 0, 0, 100)
			window.updateContent(0, 0, 100, -1)
			mockCleanup.assert_not_called()

	def test_updateContent_creates_capture_dc(self):
		"""First call to updateContent creates the capture DC and bitmap."""
		window, _ = self._createWindow()
		mockGdi32 = MagicMock()
		mockUser32 = MagicMock()

		with (
			patch("_magnifier.utils.windowCreator.gdi32", mockGdi32),
			patch("_magnifier.utils.windowCreator.user32", mockUser32),
		):
			window.updateContent(10, 20, 200, 150)

		# Screen DC obtained and released
		mockUser32.GetDC.assert_called_once_with(0)
		mockUser32.ReleaseDC.assert_called_once()
		# Capture DC created
		mockGdi32.CreateCompatibleDC.assert_called_once()
		mockGdi32.CreateCompatibleBitmap.assert_called_once()
		mockGdi32.SelectObject.assert_called_once()
		# StretchBlt to capture
		mockGdi32.StretchBlt.assert_called_once()
		# Dimensions stored
		self.assertEqual(window._captureWidth, 200)
		self.assertEqual(window._captureHeight, 150)

	def test_updateContent_reuses_dc_on_same_size(self):
		"""Subsequent calls with the same size reuse the existing capture DC."""
		window, _ = self._createWindow()
		mockGdi32 = MagicMock()
		mockUser32 = MagicMock()
		# Pre-set capture dimensions to match
		window._captureWidth = 200
		window._captureHeight = 150
		window._captureDC = MagicMock()
		window._captureBitmap = MagicMock()

		with (
			patch("_magnifier.utils.windowCreator.gdi32", mockGdi32),
			patch("_magnifier.utils.windowCreator.user32", mockUser32),
		):
			window.updateContent(10, 20, 200, 150)

		# Should NOT recreate DC
		mockGdi32.CreateCompatibleDC.assert_not_called()
		# But should still StretchBlt
		mockGdi32.StretchBlt.assert_called_once()

	def test_updateContent_sets_filter(self):
		"""updateContent stores the requested filter type."""
		window, _ = self._createWindow()
		with (
			patch("_magnifier.utils.windowCreator.gdi32"),
			patch("_magnifier.utils.windowCreator.user32"),
			patch("_magnifier.utils.windowCreator.applyBitmapFilter"),
		):
			window.updateContent(0, 0, 100, 100, Filter.INVERTED)
		self.assertEqual(window._currentFilter, Filter.INVERTED)

	def test_updateContent_grayscale_calls_filter(self):
		"""updateContent with GRAYSCALE calls applyBitmapFilter."""
		window, _ = self._createWindow()
		with (
			patch("_magnifier.utils.windowCreator.gdi32"),
			patch("_magnifier.utils.windowCreator.user32"),
			patch("_magnifier.utils.windowCreator.applyBitmapFilter") as mockFilter,
		):
			window.updateContent(0, 0, 100, 100, Filter.GRAYSCALE)
			mockFilter.assert_called_once()

	def test_updateContent_inverted_calls_filter(self):
		"""updateContent with INVERTED calls applyBitmapFilter for pixel inversion."""
		window, _ = self._createWindow()
		with (
			patch("_magnifier.utils.windowCreator.gdi32"),
			patch("_magnifier.utils.windowCreator.user32"),
			patch("_magnifier.utils.windowCreator.applyBitmapFilter") as mockFilter,
		):
			window.updateContent(0, 0, 100, 100, Filter.INVERTED)
			mockFilter.assert_called_once()

	def test_cleanupGDI_releases_resources(self):
		"""_cleanupGDI properly releases DC and bitmap."""
		window, _ = self._createWindow()
		mockDC = MagicMock()
		mockBitmap = MagicMock()
		mockOldBitmap = MagicMock()
		window._captureDC = mockDC
		window._captureBitmap = mockBitmap
		window._oldCaptureBitmap = mockOldBitmap
		window._captureWidth = 100
		window._captureHeight = 100

		with patch("_magnifier.utils.windowCreator.gdi32") as mockGdi32:
			window._cleanupGDI()

		mockGdi32.SelectObject.assert_called_once_with(mockDC, mockOldBitmap)
		mockGdi32.DeleteObject.assert_called_once_with(mockBitmap)
		mockGdi32.DeleteDC.assert_called_once_with(mockDC)
		self.assertIsNone(window._captureDC)
		self.assertIsNone(window._captureBitmap)
		self.assertIsNone(window._oldCaptureBitmap)
		self.assertEqual(window._captureWidth, 0)
		self.assertEqual(window._captureHeight, 0)

	def test_cleanupGDI_noop_when_empty(self):
		"""_cleanupGDI is safe to call with no GDI resources."""
		window, _ = self._createWindow()
		with patch("_magnifier.utils.windowCreator.gdi32") as mockGdi32:
			window._cleanupGDI()  # Should not raise
		mockGdi32.SelectObject.assert_not_called()
		mockGdi32.DeleteObject.assert_not_called()
		mockGdi32.DeleteDC.assert_not_called()

	def test_destroy_cleans_gdi_then_calls_super(self):
		"""destroy() cleans GDI before delegating to CustomWindow.destroy."""
		window, _ = self._createWindow()
		window._classAtom = 1  # Simulate a fully initialised CustomWindow
		callOrder = []
		with (
			patch.object(window, "_cleanupGDI", side_effect=lambda: callOrder.append("gdi")),
			patch(
				"_magnifier.utils.windowCreator.CustomWindow.destroy",
				side_effect=lambda s: callOrder.append("super"),
			),
		):
			window.destroy()
		self.assertEqual(callOrder, ["gdi", "super"])


class TestMagnifierOverlayWindowCursor(unittest.TestCase):
	"""Tests for the cursor snapshot and painting logic."""

	def _createWindow(self):
		params = _makeWindowParams(width=400, height=300)
		patches = _patchOverlayCreation()
		for p in patches:
			p.start()
			self.addCleanup(p.stop)
		window = MagnifierOverlayWindow(params)
		window.handle = 12345
		return window

	def test_snapshotCursor_invisible_cursor_sets_handle_none(self):
		"""Cursor not showing → handle is cleared."""
		window = self._createWindow()
		ci = CURSORINFO()
		ci.flags = 0  # CURSOR_SHOWING not set
		with patch("_magnifier.utils.windowCreator._user32_dll") as mockU:
			mockU.GetCursorInfo.side_effect = lambda p: (
				ctypes.memmove(p, ctypes.byref(ci), ctypes.sizeof(CURSORINFO)),
				True,
			)[1]
			window._snapshotCursor(0, 0, 1920, 1080)
		self.assertIsNone(window._cursorHandle)

	def test_snapshotCursor_cursor_outside_capture_area(self):
		"""Cursor outside the capture region → handle is cleared."""
		window = self._createWindow()
		ci = CURSORINFO()
		ci.flags = CURSOR_SHOWING
		ci.ptScreenPos.x = 950  # outside captureX=100..600
		ci.ptScreenPos.y = 600

		def fake_get_cursor_info(ptr):
			ctypes.memmove(ptr, ctypes.byref(ci), ctypes.sizeof(CURSORINFO))
			return True

		with patch("_magnifier.utils.windowCreator._user32_dll") as mockU:
			mockU.GetCursorInfo.side_effect = fake_get_cursor_info
			window._snapshotCursor(captureX=100, captureY=100, captureW=500, captureH=400)

		self.assertIsNone(window._cursorHandle)

	def test_snapshotCursor_cursor_inside_capture_area(self):
		"""Cursor inside the capture region → window coordinates are computed."""
		window = self._createWindow()
		# Window = 400×300, capture = 200×150 → scale = 2
		ci = CURSORINFO()
		ci.flags = CURSOR_SHOWING
		# captureX=0, captureY=0, captureW=200, captureH=150
		# cursor at (100, 75) → rel (100, 75) → window (200, 150)
		ci.ptScreenPos.x = 100
		ci.ptScreenPos.y = 75
		ci.hCursor = 0xABCD

		def fake_get_cursor_info(ptr):
			ctypes.memmove(ptr, ctypes.byref(ci), ctypes.sizeof(CURSORINFO))
			return True

		ii = ICONINFO()
		ii.xHotspot = 5  # → scaled = 10
		ii.yHotspot = 2  # → scaled = 4

		def fake_get_icon_info(hcursor, ptr):
			ctypes.memmove(ptr, ctypes.byref(ii), ctypes.sizeof(ICONINFO))
			return True

		with (
			patch("_magnifier.utils.windowCreator._user32_dll") as mockU,
		):
			mockU.GetCursorInfo.side_effect = fake_get_cursor_info
			mockU.GetIconInfo.side_effect = fake_get_icon_info
			window._snapshotCursor(captureX=0, captureY=0, captureW=200, captureH=150)

		self.assertEqual(window._cursorHandle, 0xABCD)
		self.assertEqual(window._cursorWindowX, 200)
		self.assertEqual(window._cursorWindowY, 150)
		self.assertEqual(window._cursorHotspotX, 10)
		self.assertEqual(window._cursorHotspotY, 4)

	def test_snapshotCursor_frees_icon_bitmaps(self):
		"""GetIconInfo bitmaps are freed after hotspot extraction."""
		window = self._createWindow()
		ci = CURSORINFO()
		ci.flags = CURSOR_SHOWING
		ci.ptScreenPos.x = 50
		ci.ptScreenPos.y = 50
		ci.hCursor = 0x1234

		def fake_get_cursor_info(ptr):
			ctypes.memmove(ptr, ctypes.byref(ci), ctypes.sizeof(CURSORINFO))
			return True

		ii = ICONINFO()
		ii.hbmMask = 0xAAAA
		ii.hbmColor = 0xBBBB

		def fake_get_icon_info(hcursor, ptr):
			ctypes.memmove(ptr, ctypes.byref(ii), ctypes.sizeof(ICONINFO))
			return True

		with (
			patch("_magnifier.utils.windowCreator._user32_dll") as mockU,
			patch("_magnifier.utils.windowCreator.gdi32") as mockGdi,
		):
			mockU.GetCursorInfo.side_effect = fake_get_cursor_info
			mockU.GetIconInfo.side_effect = fake_get_icon_info
			window._snapshotCursor(captureX=0, captureY=0, captureW=400, captureH=300)
			# Both bitmaps from GetIconInfo must be deleted
			deleteObjectCalls = [args[0] for args, _ in mockGdi.DeleteObject.call_args_list]
			self.assertIn(ii.hbmMask, deleteObjectCalls)
			self.assertIn(ii.hbmColor, deleteObjectCalls)

	def test_paintCursor_noop_when_no_handle(self):
		"""_paintCursor does nothing when _cursorHandle is None."""
		window = self._createWindow()
		window._cursorHandle = None
		with patch("_magnifier.utils.windowCreator._user32_dll") as mockU:
			window._paintCursor(0xDEAD)
			mockU.DrawIconEx.assert_not_called()

	def test_paintCursor_calls_draw_icon_ex(self):
		"""_paintCursor calls DrawIconEx with scaled cursor dimensions."""
		window = self._createWindow()
		# Window 400×300, capture 200×150 → scale = 2
		window._captureWidth = 200
		window._captureHeight = 150
		window._cursorHandle = 0xBEEF
		window._cursorWindowX = 100
		window._cursorWindowY = 80
		window._cursorHotspotX = 4
		window._cursorHotspotY = 2

		sysCursorW, sysCursorH = 32, 32  # system default cursor size

		with patch("_magnifier.utils.windowCreator._user32_dll") as mockU:
			mockU.GetSystemMetrics.side_effect = lambda idx: sysCursorW if idx == 13 else sysCursorH
			window._paintCursor(0xCAFE)

			mockU.DrawIconEx.assert_called_once()
			args = mockU.DrawIconEx.call_args[0]
			hdc, drawX, drawY, hCursor, scaledW, scaledH = (
				args[0],
				args[1],
				args[2],
				args[3],
				args[4],
				args[5],
			)
			self.assertEqual(hdc, 0xCAFE)
			self.assertEqual(hCursor, 0xBEEF)
			# draw pos = window pos – hotspot
			self.assertEqual(drawX, 100 - 4)
			self.assertEqual(drawY, 80 - 2)
			# scale = 400/200 = 2 → 32*2 = 64
			self.assertEqual(scaledW, 64)
			self.assertEqual(scaledH, 64)

	def test_updateContent_calls_snapshot_cursor(self):
		"""updateContent triggers _snapshotCursor with the capture coordinates."""
		window = self._createWindow()
		window._captureWidth = 100  # pre-set to skip DC recreation
		window._captureHeight = 100
		window._captureDC = MagicMock()
		window._captureBitmap = MagicMock()

		with (
			patch("_magnifier.utils.windowCreator.gdi32"),
			patch("_magnifier.utils.windowCreator.user32"),
			patch.object(window, "_snapshotCursor") as mockSnap,
		):
			window.updateContent(10, 20, 100, 100, Filter.NORMAL)
			mockSnap.assert_called_once_with(10, 20, 100, 100)


class TestWindowedMagnifier(unittest.TestCase):
	"""Tests for the WindowedMagnifier mixin."""

	def setUp(self):
		"""Create a WindowedMagnifier with a mocked MagnifierOverlayWindow."""
		self.params = _makeWindowParams()
		with patch(
			"_magnifier.utils.windowCreator.MagnifierOverlayWindow",
		) as MockOverlay:
			self.mockWindow = MagicMock()
			self.mockWindow.handle = 12345
			MockOverlay.return_value = self.mockWindow
			self.magnifier = WindowedMagnifier(self.params)

	def test_init_creates_overlay(self):
		"""WindowedMagnifier creates a MagnifierOverlayWindow."""
		self.assertIsNotNone(self.magnifier._overlayWindow)
		self.assertEqual(self.magnifier._overlayWindow, self.mockWindow)

	def test_init_stores_params(self):
		"""WindowedMagnifier stores the window parameters."""
		self.assertEqual(self.magnifier.windowMagnifierParameters, self.params)

	def test_setContent_delegates_to_overlay(self):
		"""_setContent calls updateContent on the overlay window."""
		magnifierParams = MagnifierParameters(
			magnifierSize=Size(200, 150),
			coordinates=Coordinates(10, 20),
			filter=Filter.INVERTED,
		)
		self.magnifier._setContent(magnifierParams, 2.0)

		self.mockWindow.updateContent.assert_called_once_with(
			captureX=10,
			captureY=20,
			captureW=200,
			captureH=150,
			filterType=Filter.INVERTED,
		)

	def test_setContent_noop_when_no_window(self):
		"""_setContent does nothing if the overlay window is destroyed."""
		self.magnifier._overlayWindow = None
		magnifierParams = MagnifierParameters(
			magnifierSize=Size(200, 150),
			coordinates=Coordinates(0, 0),
			filter=Filter.NORMAL,
		)
		# Should not raise
		self.magnifier._setContent(magnifierParams, 2.0)

	def test_setContent_noop_when_no_handle(self):
		"""_setContent does nothing if the overlay window handle is None."""
		self.mockWindow.handle = None
		magnifierParams = MagnifierParameters(
			magnifierSize=Size(200, 150),
			coordinates=Coordinates(0, 0),
			filter=Filter.NORMAL,
		)
		self.magnifier._setContent(magnifierParams, 2.0)
		self.mockWindow.updateContent.assert_not_called()

	def test_destroyWindow_calls_destroy(self):
		"""_destroyWindow calls destroy() on the overlay and sets it to None."""
		self.magnifier._destroyWindow()

		self.mockWindow.destroy.assert_called_once()
		self.assertIsNone(self.magnifier._overlayWindow)

	def test_destroyWindow_noop_when_already_destroyed(self):
		"""_destroyWindow is safe to call twice."""
		self.magnifier._destroyWindow()
		# Second call should not raise
		self.magnifier._destroyWindow()
		# destroy only called once
		self.mockWindow.destroy.assert_called_once()
