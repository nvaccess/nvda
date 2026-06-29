# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Dedicated low-level mouse hook for the magnifier.

Runs in its own thread so it stays responsive even when the wx main thread is
busy (e.g. at high Windows display scale factors), which is the root cause of
the DPI-related smoothness regression compared to the built-in Windows Magnifier.
"""

import ctypes
import threading
from ctypes import byref
from ctypes.wintypes import MSG
from logHandler import log
from winBindings import user32, kernel32
from winInputHook import MSLLHOOKSTRUCT, HC_ACTION, WH_MOUSE_LL

WM_MOUSEMOVE: int = 0x0200
_WM_QUIT: int = 0x0012


class MagnifierMouseHook:
	"""
	Installs a WH_MOUSE_LL hook in a dedicated thread with its own message pump.
	Calls onMouseMove(x, y) for every WM_MOUSEMOVE event.

	The dedicated thread keeps mouse tracking independent of wx main-thread load.
	"""

	def __init__(self, onMouseMove):
		self._onMouseMove = onMouseMove
		self._thread: threading.Thread | None = None
		self._threadId: int | None = None
		self._hookProc = None  # must be kept alive to prevent GC of ctypes callback
		self._ready = threading.Event()

	def start(self) -> None:
		self._ready.clear()
		self._thread = threading.Thread(
			target=self._run,
			name="magnifierMouseHook",
			daemon=True,
		)
		self._thread.start()
		self._ready.wait(timeout=1.0)

	def stop(self) -> None:
		if self._threadId:
			user32.PostThreadMessage(self._threadId, _WM_QUIT, 0, 0)
			self._threadId = None
		if self._thread:
			self._thread.join(timeout=1.0)
			self._thread = None
		self._hookProc = None

	def _run(self) -> None:
		self._threadId = ctypes.windll.kernel32.GetCurrentThreadId()

		def _hookFunc(code, wParam, lParam):
			if code == HC_ACTION and wParam == WM_MOUSEMOVE:
				msll = MSLLHOOKSTRUCT.from_address(lParam)
				try:
					self._onMouseMove(msll.pt.x, msll.pt.y)
				except Exception:
					log.exception("Error in magnifier mouse hook callback")
			return user32.CallNextHookEx(0, code, wParam, lParam)

		self._hookProc = user32.HOOKPROC(_hookFunc)

		hookHandle = user32.SetWindowsHookEx(
			WH_MOUSE_LL,
			self._hookProc,
			kernel32.GetModuleHandle(None),
			0,
		)

		if not hookHandle:
			log.error(f"Failed to install magnifier mouse hook (error {ctypes.GetLastError()})")

		self._ready.set()

		msg = MSG()
		while user32.GetMessage(byref(msg), None, 0, 0):
			pass

		if hookHandle:
			user32.UnhookWindowsHookEx(hookHandle)
