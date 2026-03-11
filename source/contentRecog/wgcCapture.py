# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Pratik Patel
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Content recognizer using Windows.Graphics.Capture.

Captures window content via CreateForWindow, which reads from the DWM compositor
before the Magnification API color transform. This allows OCR to work while
Screen Curtain is active, without exposing screen content to sighted observers.
"""

import json
from collections.abc import Callable
from ctypes import c_uint

import api
import config
import winUser
from NVDAHelper.localWin10 import (
	wgcCapture_isSupported,
	wgcCapture_initialize,
	wgcCapture_recognizeWindow,
	wgcCapture_recognizeWindowRegion,
	wgcCapture_terminate,
	wgcCapture_Callback as _wgcCapture_Callback,
)
from logHandler import log
from . import ContentRecognizer, LinesWordsResult, RecogImageInfo


def isSupported() -> bool:
	"""Check whether WGC capture and OCR are available (Win10 1903+)."""
	try:
		return bool(wgcCapture_isSupported())
	except (OSError, AttributeError):
		return False


def _getRootWindow(hwnd: int) -> int:
	"""Walk up to the root owner window required by CreateForWindow."""
	root = winUser.getAncestor(hwnd, winUser.GA_ROOT)
	return root if root else hwnd


class WgcOcr(ContentRecognizer):
	"""OCR recognizer using Windows.Graphics.Capture.

	Works when Screen Curtain is active because WGC captures from the
	DWM compositor before the Magnification API transform.
	"""

	@classmethod
	def _get_allowAutoRefresh(cls) -> bool:
		return config.conf["uwpOcr"]["autoRefresh"]

	@classmethod
	def _get_autoRefreshInterval(cls) -> int:
		return config.conf["uwpOcr"]["autoRefreshInterval"]

	@classmethod
	def _get_autoSayAllOnResult(cls) -> bool:
		return config.conf["uwpOcr"]["autoSayAllOnResult"]

	def getResizeFactor(self, width: int, height: int) -> int:
		"""WGC captures at native resolution; no resize needed."""
		return 1

	def __init__(self, language: str | None = None):
		"""
		:param language: BCP-47 language code for OCR, or C{None} to use
			the user's configured Windows OCR language.
		"""
		from contentRecog.uwpOcr import getConfigLanguage

		self.language: str = language or getConfigLanguage()
		self._handle = None
		self._onResult: Callable | None = None
		self._cCallbackRef = None

	def recognize(self, pixels, imageInfo: RecogImageInfo, onResult: Callable) -> None:
		"""Capture the target window via HWND and run OCR.

		:param pixels: Ignored. WGC captures its own frames via HWND.
			Kept for ContentRecognizer interface compatibility.
		:param imageInfo: Screen region information for the recognition area.
		:param onResult: Callback invoked with a L{LinesWordsResult} or C{Exception}.
		"""
		self._onResult = onResult

		hwnd = self._getTargetHwnd(imageInfo)
		if not hwnd:
			log.error("wgcCapture: could not find target HWND")
			self._fireResult(RuntimeError("wgcCapture: no target HWND"))
			return

		@_wgcCapture_Callback
		def callback(resultJson):
			self._onCppResult(resultJson, imageInfo, hwnd)

		self._cCallbackRef = callback

		self._handle = wgcCapture_initialize(self.language, self._cCallbackRef)
		if not self._handle:
			log.error("wgcCapture: failed to initialize (language=%s)", self.language)
			self._fireResult(RuntimeError("WGC OCR initialization failed"))
			return

		windowRect = winUser.getWindowRect(hwnd)
		if windowRect:
			relX = max(0, imageInfo.screenLeft - windowRect[0])
			relY = max(0, imageInfo.screenTop - windowRect[1])
			wgcCapture_recognizeWindowRegion(
				self._handle,
				hwnd,
				c_uint(relX),
				c_uint(relY),
				c_uint(imageInfo.screenWidth),
				c_uint(imageInfo.screenHeight),
			)
		else:
			wgcCapture_recognizeWindow(self._handle, hwnd)

	def _getTargetHwnd(self, imageInfo: RecogImageInfo) -> int | None:
		"""Get the top-level HWND for the target screen location."""
		nav = api.getNavigatorObject()
		if nav and hasattr(nav, "windowHandle") and nav.windowHandle:
			return _getRootWindow(nav.windowHandle)
		return None

	def _onCppResult(
		self,
		resultJson: str | None,
		imageInfo: RecogImageInfo,
		hwnd: int,
	) -> None:
		"""Parse C++ OCR JSON results into L{LinesWordsResult}.

		Called from the C++ completion callback. Handles cleanup of the
		native instance (matching the uwpOcr pattern where terminate is
		called inside the callback, never while async work is in-flight).
		"""
		# If _onResult is None, recognition was cancelled.
		if self._onResult:
			if resultJson:
				try:
					data = json.loads(resultJson)
					self._onResult(LinesWordsResult(data, imageInfo))
				except (json.JSONDecodeError, KeyError, TypeError) as e:
					log.error("wgcCapture: failed to parse OCR result: %s", e)
					self._onResult(RuntimeError(f"WGC OCR parse error: {e}"))
			else:
				log.debugWarning("wgcCapture: OCR returned no results")
				self._onResult(RuntimeError("WGC OCR returned no results"))
		# Clean up the native instance now that the coroutine has completed.
		wgcCapture_terminate(self._handle)
		self._cCallbackRef = None
		self._handle = None

	def cancel(self) -> None:
		"""Cancel pending recognition.

		Marks recognition as cancelled so results are ignored when the
		C++ callback fires. Does not terminate the native instance
		(the callback handles cleanup when C++ signals completion).
		"""
		self._onResult = None

	def validateObject(self, nav) -> bool:
		"""WGC requires a valid HWND on the navigator object."""
		return bool(getattr(nav, "windowHandle", None))
