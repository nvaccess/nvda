# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""RapidOCR engine implementation using ONNX Runtime for on-device OCR."""

import threading
from typing import List

from logHandler import log
from .engine import OcrEngine


# Language codes supported by RapidOCR with PP-OCRv4/v5 models.
# "auto" uses the default Chinese+English model.
SUPPORTED_LANGUAGES = [
	"auto",
	"ch",
	"en",
	"japan",
	"korean",
	"french",
	"german",
	"arabic",
	"latin",
	"cyrillic",
	"devanagari",
]


class RapidOcrEngine(OcrEngine):
	"""On-device OCR engine backed by RapidOCR + ONNX Runtime.

	Models are loaded lazily on first recognition call.
	Thread-safe for sequential access (one inference at a time).
	"""

	def __init__(self):
		self._engine = None
		self._language: str = "auto"
		self._initialized: bool = False
		self._lock = threading.Lock()

	def initialize(self, language: str = "auto") -> None:
		with self._lock:
			if self._initialized and self._language == language:
				return  # Already initialized with same config
			if self._initialized:
				self._cleanup()

			try:
				from rapidocr import RapidOCR

				self._engine = RapidOCR()
				self._language = language
				self._initialized = True
				log.info(f"RapidOCR engine initialized (language={language})")
			except ImportError:
				log.error(
					"RapidOCR is not installed. Install with: pip install rapidocr onnxruntime",
					exc_info=True,
				)
				raise RuntimeError("RapidOCR package not available")
			except Exception:
				log.error("Failed to initialize RapidOCR engine", exc_info=True)
				raise

	def recognize(self, image) -> list:
		"""Run OCR inference on a BGR image.

		@param image: numpy ndarray, shape (H, W, 3), dtype uint8, BGR format.
		@return: List of (quad, text, confidence) tuples.
		@raises RuntimeError: If engine is not initialized.
		"""
		with self._lock:
			if not self._initialized or self._engine is None:
				raise RuntimeError("OCR engine not initialized. Call initialize() first.")
			result = self._engine(image)
			# RapidOCR >= 3.x returns a RapidOCRResult object.
			# Access .boxes, .txts, .scores or iterate.
			# For compatibility, handle both old tuple format and new object format.
			if result is None:
				return []
			# New API (>= 3.0): result has .boxes, .txts, .scores attributes
			if hasattr(result, "boxes") and result.boxes is not None:
				items = []
				for box, txt, score in zip(result.boxes, result.txts, result.scores):
					items.append((box.tolist() if hasattr(box, "tolist") else box, txt, float(score)))
				return items
			# Legacy API: result is (list_of_results, elapsed)
			if isinstance(result, tuple) and len(result) == 2:
				raw, _ = result
				if raw is None:
					return []
				return raw
			return []

	def get_available_languages(self) -> List[str]:
		return list(SUPPORTED_LANGUAGES)

	def shutdown(self) -> None:
		with self._lock:
			self._cleanup()

	def _cleanup(self):
		"""Release engine resources. Must be called with self._lock held."""
		self._engine = None
		self._initialized = False
		log.debug("RapidOCR engine resources released")

	@property
	def is_initialized(self) -> bool:
		return self._initialized
