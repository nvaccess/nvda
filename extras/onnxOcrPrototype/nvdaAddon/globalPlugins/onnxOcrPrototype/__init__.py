# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NVDA Contributors
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""NVDA integration for an isolated, on-device ONNX OCR worker."""

import ctypes
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

import addonHandler
import config
import globalPluginHandler
import gui
import ui
from contentRecog import (
	ContentRecognizer,
	LinesWordsResult,
	RecogImageInfo,
	onRecognizeResultCallbackT,
	recogUi,
)
from locationHelper import RectLTWH
from logHandler import log
from scriptHandler import script
from utils.security import objectBelowLockScreenAndWindowsIsLocked

addonHandler.initTranslation()

from .capture import getAdaptiveResizeFactor, isCaptureSizeSupported
from .client import OcrWorkerClient, OcrWorkerResult
from .settings import OnDeviceOcrSettingsPanel

_CONFIG_SECTION = "onDeviceOcr"
_WORKER_PYTHON_ENV = "NVDA_ONNX_OCR_WORKER_PYTHON"
_WORKER_EXECUTABLE_ENV = "NVDA_ONNX_OCR_WORKER_EXE"
_MANIFEST_ENV = "NVDA_ONNX_OCR_MANIFEST"
_MODEL_DIRECTORY_ENV = "NVDA_ONNX_OCR_MODEL_DIR"
_TEST_DOUBLE_ENV = "NVDA_ONNX_OCR_TEST_DOUBLE"
_TEST_DOUBLE_DELAY_ENV = "NVDA_ONNX_OCR_TEST_DOUBLE_DELAY_SECONDS"
_MODEL_MANIFESTS = {
	"tiny": "ppocr-v6-tiny.json",
	"small": "ppocr-v6-small.json",
}

config.conf.spec[_CONFIG_SECTION] = {
	"modelProfile": "option('tiny', 'small', default='tiny')",
	"autoSayAllOnResult": "boolean(default=True)",
	"workerIdleTimeoutSeconds": "integer(default=120, min=0, max=3600)",
}


class OnDeviceOcrConfigurationError(RuntimeError):
	"""The on-device OCR installation or configuration is incomplete."""


def _isEnabledEnvironmentValue(name: str) -> bool:
	return os.environ.get(name, "").strip().lower() in ("1", "true", "yes", "on")


def _testDoubleDelaySeconds() -> float:
	rawValue = os.environ.get(_TEST_DOUBLE_DELAY_ENV, "0").strip()
	try:
		delaySeconds = float(rawValue)
	except ValueError as error:
		raise OnDeviceOcrConfigurationError(
			f"{_TEST_DOUBLE_DELAY_ENV} must be a number between 0 and 10",
		) from error
	if not 0 <= delaySeconds <= 10:
		raise OnDeviceOcrConfigurationError(
			f"{_TEST_DOUBLE_DELAY_ENV} must be between 0 and 10",
		)
	return delaySeconds


def _modelDirectory() -> Path:
	configuredDirectory = os.environ.get(_MODEL_DIRECTORY_ENV)
	if configuredDirectory:
		return Path(configuredDirectory).expanduser()
	localAppData = os.environ.get("LOCALAPPDATA", tempfile.gettempdir())
	return Path(localAppData) / "nvda" / "onDeviceOcr" / "models"


def _configurationSignature() -> tuple[str, bool, int, str, str, str, str, bool, str]:
	settings = config.conf[_CONFIG_SECTION]
	return (
		str(settings["modelProfile"]),
		bool(settings["autoSayAllOnResult"]),
		int(settings["workerIdleTimeoutSeconds"]),
		os.environ.get(_MANIFEST_ENV, ""),
		os.environ.get(_WORKER_EXECUTABLE_ENV, ""),
		os.environ.get(_WORKER_PYTHON_ENV, ""),
		os.environ.get(_MODEL_DIRECTORY_ENV, ""),
		_isEnabledEnvironmentValue(_TEST_DOUBLE_ENV),
		os.environ.get(_TEST_DOUBLE_DELAY_ENV, ""),
	)


class OnDeviceOcrRecognizer(ContentRecognizer):
	"""Adapt NVDA's content-recognition API to the external OCR worker."""

	def __init__(self) -> None:
		pluginDirectory = Path(__file__).resolve().parent
		workerMain = pluginDirectory / "workerMain.py"
		configuredExecutable = os.environ.get(_WORKER_EXECUTABLE_ENV)
		configuredPython = os.environ.get(_WORKER_PYTHON_ENV)
		packagedExecutable = pluginDirectory / "workerRuntime" / "onnxOcrWorker.exe"
		workerExecutable: Path | None = None
		workerPython: Path | None = None
		if configuredExecutable:
			workerExecutable = Path(configuredExecutable).expanduser()
		elif configuredPython:
			workerPython = Path(configuredPython).expanduser()
		elif packagedExecutable.is_file():
			workerExecutable = packagedExecutable
		elif Path(sys.executable).stem.lower().startswith("python"):
			# Development checkout only. Installed NVDA uses nvda.exe and therefore
			# requires the packaged worker or an explicit development override.
			workerPython = Path(sys.executable)
		else:
			raise OnDeviceOcrConfigurationError(
				"The isolated OCR worker executable is missing",
			)
		workerPath = workerExecutable or workerPython
		assert workerPath is not None
		if not workerPath.is_file():
			raise OnDeviceOcrConfigurationError(f"OCR worker does not exist: {workerPath}")

		useTestDouble = _isEnabledEnvironmentValue(_TEST_DOUBLE_ENV)
		configuredManifest = os.environ.get(_MANIFEST_ENV)
		if configuredManifest:
			manifestPath = Path(configuredManifest).expanduser()
		else:
			profile = str(config.conf[_CONFIG_SECTION]["modelProfile"])
			manifestName = _MODEL_MANIFESTS.get(profile)
			if manifestName is None:
				raise OnDeviceOcrConfigurationError(f"Unknown OCR model profile: {profile}")
			manifestPath = pluginDirectory / "models" / manifestName
		if not useTestDouble and not manifestPath.is_file():
			raise OnDeviceOcrConfigurationError(f"OCR model manifest does not exist: {manifestPath}")

		self._autoSayAllOnResult = bool(config.conf[_CONFIG_SECTION]["autoSayAllOnResult"])
		self._client = OcrWorkerClient(
			workerPython=workerPython,
			workerExecutable=workerExecutable,
			workerMain=workerMain,
			manifestPath=manifestPath,
			modelDirectory=_modelDirectory(),
			useTestDouble=useTestDouble,
			testDoubleDelaySeconds=_testDoubleDelaySeconds() if useTestDouble else 0,
			idleTimeoutSeconds=int(config.conf[_CONFIG_SECTION]["workerIdleTimeoutSeconds"]),
		)

	def _get_autoSayAllOnResult(self) -> bool:
		return self._autoSayAllOnResult

	def getResizeFactor(self, width: int, height: int) -> int | float:
		"""Improve small-control OCR without enlarging normal captures."""
		return getAdaptiveResizeFactor(width, height)

	def validateCaptureBounds(self, location: RectLTWH) -> bool:
		"""Prevent a pathological navigator object from allocating an excessive frame."""
		if location.width <= 0 or location.height <= 0:
			# Let NVDA's content-recognition UI report its standard not-visible message.
			return True
		if isCaptureSizeSupported(location.width, location.height):
			return True
		# Translators: Reported when a navigator object is too large to capture safely for OCR.
		ui.message(_("The current navigator object is too large for on-device OCR."))
		return False

	def validateObject(self, nav: Any) -> bool:
		"""Do not capture content hidden below the Windows lock screen."""
		return not objectBelowLockScreenAndWindowsIsLocked(nav)

	def recognize(
		self,
		pixels: ctypes.Array[Any],
		imageInfo: RecogImageInfo,
		onResult: onRecognizeResultCallbackT,
	) -> None:
		"""Copy the captured frame and submit it without loading ML libraries in NVDA."""
		stride = imageInfo.recogWidth * 4
		frameSize = stride * imageInfo.recogHeight
		try:
			frame = ctypes.string_at(ctypes.addressof(pixels), frameSize)
			self._client.recognize(
				frame,
				width=imageInfo.recogWidth,
				height=imageInfo.recogHeight,
				stride=stride,
				onResult=lambda result: self._onWorkerResult(result, imageInfo, onResult),
			)
		except Exception as error:  # noqa: BLE001 - ContentRecognizer must report every submission failure.
			onResult(error)

	@staticmethod
	def _onWorkerResult(
		result: OcrWorkerResult | Exception,
		imageInfo: RecogImageInfo,
		onResult: onRecognizeResultCallbackT,
	) -> None:
		if isinstance(result, Exception):
			log.error("On-device OCR worker returned an error: %s", result)
			onResult(result)
			return
		lineCount = len(result.lines)
		wordCount = sum(len(line) for line in result.lines)
		log.info(
			"On-device OCR worker returned %d lines and %d regions; metrics=%r",
			lineCount,
			wordCount,
			result.metrics,
		)
		if not result.lines:
			onResult(RuntimeError("No text was recognized"))
			return
		onResult(LinesWordsResult(result.lines, imageInfo))

	def cancel(self) -> None:
		"""Cancel native inference by terminating the isolated worker."""
		self._client.cancel()

	def terminate(self) -> None:
		"""Release the worker client and its warm process."""
		self._client.terminate()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	"""Expose on-device OCR through an NVDA command and settings category."""

	def __init__(self) -> None:
		super().__init__()
		self._recognizer: OnDeviceOcrRecognizer | None = None
		self._recognizerSignature: tuple[str, bool, int, str, str, str, str, bool, str] | None = None
		if OnDeviceOcrSettingsPanel not in gui.settingsDialogs.NVDASettingsDialog.categoryClasses:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(OnDeviceOcrSettingsPanel)

	def _getRecognizer(self) -> OnDeviceOcrRecognizer:
		signature = _configurationSignature()
		if self._recognizer is None or signature != self._recognizerSignature:
			if self._recognizer is not None:
				self._recognizer.terminate()
			self._recognizer = None
			self._recognizerSignature = None
			recognizer = OnDeviceOcrRecognizer()
			self._recognizer = recognizer
			self._recognizerSignature = signature
		return self._recognizer

	@script(
		# Translators: Describes a command which recognizes the navigator object using on-device OCR.
		description=_("Recognizes the current navigator object using on-device OCR"),
		gesture="kb:NVDA+alt+o",
	)
	@gui.blockAction.when(gui.blockAction.Context.SECURE_MODE)
	def script_recognizeWithOnDeviceOcr(self, gesture: Any) -> None:
		try:
			recognizer = self._getRecognizer()
		except Exception:
			log.exception("On-device OCR is not configured")
			# Translators: Reported when the isolated OCR worker is unavailable.
			ui.message(_("On-device OCR is not available. Reinstall the add-on or check its settings."))
			return
		recogUi.recognizeNavigatorObject(recognizer)

	def terminate(self) -> None:
		if self._recognizer is not None:
			self._recognizer.terminate()
			self._recognizer = None
		if OnDeviceOcrSettingsPanel in gui.settingsDialogs.NVDASettingsDialog.categoryClasses:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(OnDeviceOcrSettingsPanel)
		super().terminate()
