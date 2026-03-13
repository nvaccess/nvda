# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Abstract OCR engine interface and engine lifecycle manager.

This module defines the contract for on-device OCR engines and provides
a manager class that handles lazy initialization and cleanup.
The abstraction allows swapping the underlying engine (e.g., from RapidOCR
to another ONNX-based engine) without modifying the recognizer class.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from logHandler import log


class OcrEngine(ABC):
	"""Abstract base class for on-device OCR engines.

	Implementations must handle their own model loading/unloading.
	The recognize() method receives a BGR numpy array and returns
	a list of (quad, text, confidence) tuples.
	"""

	@abstractmethod
	def initialize(self, language: str = "auto") -> None:
		"""Initialize or re-initialize the engine for the given language.

		May download models on first call. Must be safe to call multiple times;
		if already initialized with the same language, should be a no-op.

		@param language: Language code (e.g., "auto", "ch", "en", "japan").
		@raises RuntimeError: If initialization fails.
		"""
		...

	@abstractmethod
	def recognize(self, image) -> list:
		"""Run OCR on an image.

		@param image: numpy ndarray in BGR format, shape (H, W, 3), dtype uint8.
		@return: List of (quad_coords, text, confidence) tuples.
			quad_coords: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
			text: str
			confidence: float 0.0-1.0
		"""
		...

	@abstractmethod
	def get_available_languages(self) -> List[str]:
		"""Return list of supported language codes."""
		...

	@abstractmethod
	def shutdown(self) -> None:
		"""Release all resources (ONNX sessions, model memory)."""
		...

	@property
	@abstractmethod
	def is_initialized(self) -> bool:
		"""Whether the engine has been initialized and is ready for recognition."""
		...


class OcrEngineManager:
	"""Singleton manager for the on-device OCR engine.

	Uses lazy initialization: the engine is created on first access,
	not at NVDA startup, to avoid unnecessary startup delay and memory usage.
	"""

	_instance: Optional[OcrEngine] = None

	@classmethod
	def get_engine(cls) -> OcrEngine:
		"""Get or create the OCR engine instance.

		@return: The active OcrEngine instance.
		"""
		if cls._instance is None:
			from .rapidOcrEngine import RapidOcrEngine

			cls._instance = RapidOcrEngine()
			log.debug("On-device OCR engine created (not yet initialized)")
		return cls._instance

	@classmethod
	def shutdown(cls) -> None:
		"""Shut down and release the engine instance."""
		if cls._instance is not None:
			try:
				cls._instance.shutdown()
			except Exception:
				log.error("Error during OCR engine shutdown", exc_info=True)
			cls._instance = None
			log.debug("On-device OCR engine manager shut down")
