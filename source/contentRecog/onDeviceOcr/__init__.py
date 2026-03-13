# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""On-device OCR for NVDA using RapidOCR + ONNX Runtime.

Provides offline text recognition from screen content using PaddleOCR models
(PP-OCRv4/v5) via the RapidOCR library with ONNX Runtime inference.
This recognizer runs entirely on-device with no cloud dependency.
"""

import ctypes
import threading
from typing import Union

import config
from logHandler import log
from contentRecog import (
	ContentRecognizer,
	LinesWordsResult,
	RecogImageInfo,
	onRecognizeResultCallbackT,
)
from .engine import OcrEngineManager
from .resultConverter import convert_rapidocr_result


class OnDeviceOcr(ContentRecognizer):
	"""On-device OCR content recognizer.

	Subclasses ContentRecognizer to integrate with NVDA's content recognition
	framework. Uses RapidOCR + ONNX Runtime for inference in a background thread.
	"""

	@classmethod
	def _get_allowAutoRefresh(cls) -> bool:
		return config.conf["onDeviceOcr"]["autoRefresh"]

	@classmethod
	def _get_autoRefreshInterval(cls) -> int:
		return config.conf["onDeviceOcr"]["autoRefreshInterval"]

	@classmethod
	def _get_autoSayAllOnResult(cls) -> bool:
		return config.conf["onDeviceOcr"]["autoSayAllOnResult"]

	def __init__(self, language: str = None):
		"""
		@param language: The language code for recognition,
			C{None} to use the user's configured language.
		"""
		if language:
			self.language = language
		else:
			self.language = config.conf["onDeviceOcr"]["language"] or "auto"
		self._onResult: onRecognizeResultCallbackT = None

	def getResizeFactor(self, width: int, height: int) -> Union[int, float]:
		"""Upscale small images for better OCR accuracy."""
		if width < 100 or height < 100:
			return 4
		return 1

	def recognize(
		self,
		pixels: ctypes.Array,
		imageInfo: RecogImageInfo,
		onResult: onRecognizeResultCallbackT,
	):
		"""Asynchronously recognize text from screen pixels.

		Spawns a daemon thread for OCR inference. The onResult callback
		will be called from the background thread with either a
		LinesWordsResult or an Exception. The recogUi layer handles
		marshalling the result back to the main thread.
		"""
		self._onResult = onResult

		def _backgroundRecognize():
			try:
				import numpy as np

				engine = OcrEngineManager.get_engine()
				if not engine.is_initialized:
					engine.initialize(language=self.language)

				# --- Pixel format conversion ---
				# screenBitmap.captureImage() returns (RGBQUAD * width * height).
				# RGBQUAD memory layout: [Blue, Green, Red, Reserved] = 4 bytes/pixel.
				# We need BGR numpy array for RapidOCR (OpenCV convention).
				width = imageInfo.recogWidth
				height = imageInfo.recogHeight
				byte_count = width * height * 4

				# from_buffer_copy creates an independent copy, safe after pixels
				# buffer is invalidated. from_buffer would be faster but unsafe.
				flat_buf = (ctypes.c_ubyte * byte_count).from_buffer_copy(pixels)
				arr = np.frombuffer(flat_buf, dtype=np.uint8).reshape((height, width, 4))

				# BGRA[:3] -> BGR. The memory is already in BGR order (Blue=0, Green=1,
				# Red=2), which is exactly what RapidOCR/OpenCV expects.
				# .copy() ensures contiguous memory for ONNX Runtime.
				bgr_image = arr[:, :, :3].copy()

				# --- Run OCR inference ---
				raw_result = engine.recognize(bgr_image)

				# --- Convert results to NVDA format ---
				lines_data = convert_rapidocr_result(raw_result)

				if self._onResult is None:
					return  # Recognition was cancelled

				if lines_data:
					self._onResult(LinesWordsResult(lines_data, imageInfo))
				else:
					# No text detected - return empty result rather than error
					self._onResult(
						LinesWordsResult(
							[[{"x": 0, "y": 0, "width": 1, "height": 1, "text": ""}]],
							imageInfo,
						),
					)

			except Exception as e:
				log.error(f"On-device OCR recognition failed: {e}", exc_info=True)
				if self._onResult is not None:
					self._onResult(RuntimeError(f"On-device OCR failed: {e}"))

		thread = threading.Thread(
			target=_backgroundRecognize,
			name="onDeviceOcr_recognize",
			daemon=True,
		)
		thread.start()

	def cancel(self):
		"""Cancel the recognition in progress (if any)."""
		self._onResult = None
