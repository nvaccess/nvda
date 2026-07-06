# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Dedicated low-level mouse hook for the magnifier.

Runs in its own thread so it stays responsive even when the wx main thread is
busy (e.g. at high Windows display scale factors), which is the root cause of
the DPI-related lag compared to the built-in Windows Magnifier.
"""

import ctypes
import threading
from ctypes import byref
from ctypes.wintypes import MSG
from logHandler import log
from winBindings import user32
from winInputHook import MSLLHOOKSTRUCT, HC_ACTION, WH_MOUSE_LL

WM_MOUSEMOVE: int = 0x0200
WM_QUIT: int = 0x0012
PM_NOREMOVE: int = 0x0000


class MagnifierMouseHook:
	"""Installs a WH_MOUSE_LL hook in a dedicated thread. Calls onMouseMove(x, y) on every mouse move."""

	def __init__(self, onMouseMove):
		self._onMouseMove = onMouseMove
		self._thread: threading.Thread | None = None
		self._cCallback = None  # kept alive to prevent GC of the ctypes callback
		self._hookReady = threading.Event()
		self._hookInstalled: bool = False

	def start(self) -> None:
		self._thread = threading.Thread(target=self._run, name="magnifierMouseHook", daemon=True)
		self._thread.start()
		self._hookReady.wait(timeout=1.0)

	def stop(self) -> None:
		thread = self._thread
		if not thread:
			self._cCallback = None
			return
		if thread.ident is None or not user32.PostThreadMessage(thread.ident, WM_QUIT, 0, 0):
			log.error(
				f"Failed to post WM_QUIT to magnifier mouse hook thread (error {ctypes.GetLastError()})",
			)
		thread.join()
		self._thread = None
		self._cCallback = None

	def _run(self) -> None:
		windowsMessage = MSG()
		# Ensure the thread message queue exists so PostThreadMessage(WM_QUIT) succeeds.
		user32.PeekMessage(byref(windowsMessage), None, 0, 0, PM_NOREMOVE)

		def _onRawMouseEvent(code, eventType, mouseDataPointer):
			if code == HC_ACTION and eventType == WM_MOUSEMOVE:
				mouseData = MSLLHOOKSTRUCT.from_address(mouseDataPointer)
				try:
					self._onMouseMove(mouseData.pt.x, mouseData.pt.y)
				except Exception:
					log.exception("Error in magnifier mouse hook callback")
			return user32.CallNextHookEx(0, code, eventType, mouseDataPointer)

		self._cCallback = user32.HOOKPROC(_onRawMouseEvent)
		hookHandle = user32.SetWindowsHookEx(WH_MOUSE_LL, self._cCallback, None, 0)
		self._hookInstalled = bool(hookHandle)
		self._hookReady.set()
		if not hookHandle:
			log.error(f"Failed to install magnifier mouse hook (error {ctypes.GetLastError()})")
			return

		try:
			while True:
				result = user32.GetMessage(byref(windowsMessage), None, 0, 0)
				if result == 0:
					break
				if result == -1:
					log.error(
						f"GetMessage failed in magnifier mouse hook thread (error {ctypes.GetLastError()})",
					)
					break
		finally:
			user32.UnhookWindowsHookEx(hookHandle)
