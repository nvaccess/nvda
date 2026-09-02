# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NVDA Contributors
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Direct ONNX Runtime adapter for detector/CTC-recognizer PP-OCR models."""

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .modelManager import ModelBundle


class InferenceConfigurationError(ValueError):
	"""The model manifest is not compatible with this prototype adapter."""


@dataclass(frozen=True)
class _Box:
	left: int
	top: int
	right: int
	bottom: int

	@property
	def width(self) -> int:
		return self.right - self.left

	@property
	def height(self) -> int:
		return self.bottom - self.top

	@property
	def centerY(self) -> float:
		return (self.top + self.bottom) / 2


class TestDoubleAdapter:
	"""Deterministic adapter used to validate NVDA wiring without native dependencies."""

	def __init__(self, delaySeconds: float = 0) -> None:
		self._delaySeconds = max(0, delaySeconds)
		self.lastMetrics: dict[str, int | float | str] = {}

	def recognizeFrame(
		self,
		framePath: Path,
		*,
		width: int,
		height: int,
		stride: int,
	) -> list[list[dict[str, int | str]]]:
		"""Validate the frame and return one predictable line."""
		expectedSize = stride * height
		if framePath.stat().st_size != expectedSize:
			raise ValueError("BGRA frame size does not match its metadata")
		startedAt = time.perf_counter()
		if self._delaySeconds:
			time.sleep(self._delaySeconds)
		self.lastMetrics = {
			"totalSeconds": time.perf_counter() - startedAt,
			"detectedRegions": 1,
			"recognizedRegions": 1,
			"provider": "test-double",
		}
		return [
			[
				{
					"x": 0,
					"y": 0,
					"width": width,
					"height": height,
					"text": f"OCR test double: {width} by {height} pixels",
				},
			],
		]


class OnnxPaddleOcrAdapter:
	"""Run PP-OCR detector and CTC recognizer models using ONNX Runtime directly.

	The implementation is optimized for horizontal desktop UI text. It avoids
	OpenCV, Pillow, PaddleOCR and RapidOCR at runtime. DB regions are extracted
	with a run-length connected-component pass and expanded with a rectangular
	approximation of DB ``unclip``. A low-confidence horizontal crop can be
	deskewed by its foreground principal axis. Perspective correction and
	arbitrary rotated text remain outside this implementation's declared scope.
	"""

	def __init__(self, modelBundle: ModelBundle) -> None:
		try:
			import numpy
			import onnxruntime
		except ImportError as error:
			raise RuntimeError(
				f"The OCR worker requires NumPy and ONNX Runtime; native runtime loading failed: {error}",
			) from error
		self._numpy = numpy
		self._onnxruntime = onnxruntime
		self._config = modelBundle.config
		self._detectorConfig = self._requireSection("detector")
		self._recognizerConfig = self._requireSection("recognizer")
		providers = self._config.get("providers", ["CPUExecutionProvider"])
		if not isinstance(providers, list) or not all(isinstance(provider, str) for provider in providers):
			raise InferenceConfigurationError("providers must be a list of strings")
		detectorPath = self._resolveConfiguredFile(
			modelBundle,
			self._detectorConfig,
			"modelFile",
		)
		recognizerPath = self._resolveConfiguredFile(
			modelBundle,
			self._recognizerConfig,
			"modelFile",
		)
		sessionOptions = onnxruntime.SessionOptions()
		sessionOptions.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL
		sessionOptions.enable_cpu_mem_arena = bool(self._config.get("enableCpuMemoryArena", False))
		threadCount = self._config.get("intraOpNumThreads")
		if isinstance(threadCount, int) and threadCount > 0:
			sessionOptions.intra_op_num_threads = threadCount
		self._detector = onnxruntime.InferenceSession(
			str(detectorPath),
			sess_options=sessionOptions,
			providers=providers,
		)
		self._recognizer = onnxruntime.InferenceSession(
			str(recognizerPath),
			sess_options=sessionOptions,
			providers=providers,
		)
		self._detectorInputName = self._inputName(self._detector, self._detectorConfig)
		self._recognizerInputName = self._inputName(self._recognizer, self._recognizerConfig)
		self._characters = self._loadCharacters(modelBundle)
		self.lastMetrics: dict[str, int | float | str] = {}

	def recognizeFrame(
		self,
		framePath: Path,
		*,
		width: int,
		height: int,
		stride: int,
	) -> list[list[dict[str, int | str | float]]]:
		"""Recognize a BGRA frame and return NVDA ``LinesWordsResult`` data."""
		startedAt = time.perf_counter()
		bgrImage = self._readBgraFrame(framePath, width=width, height=height, stride=stride)
		detectionStartedAt = time.perf_counter()
		boxes = self._detect(bgrImage)
		detectionSeconds = time.perf_counter() - detectionStartedAt
		if not boxes and self._config.get("recognizeFullImageWhenNoDetection", False):
			boxes = [_Box(0, 0, width, height)]
		recognizedBoxes: list[tuple[_Box, str, float]] = []
		deskewedRegions = 0
		recognitionStartedAt = time.perf_counter()
		minimumConfidence = float(self._recognizerConfig.get("minimumConfidence", 0))
		for box in boxes:
			crop = bgrImage[box.top : box.bottom, box.left : box.right]
			text, confidence = self._recognizeCrop(crop)
			if confidence < minimumConfidence:
				deskewedCrop = self._deskewCrop(crop)
				if deskewedCrop is not None:
					deskewedText, deskewedConfidence = self._recognizeCrop(deskewedCrop)
					if deskewedConfidence > confidence:
						text = deskewedText
						confidence = deskewedConfidence
						deskewedRegions += 1
			if text and confidence >= minimumConfidence:
				recognizedBoxes.append((box, text, confidence))
		lines = self._toLines(recognizedBoxes)
		self.lastMetrics = {
			"totalSeconds": time.perf_counter() - startedAt,
			"detectionSeconds": detectionSeconds,
			"recognitionSeconds": time.perf_counter() - recognitionStartedAt,
			"detectedRegions": len(boxes),
			"recognizedRegions": len(recognizedBoxes),
			"deskewedRegions": deskewedRegions,
			"provider": self._detector.get_providers()[0],
		}
		return lines

	def _requireSection(self, name: str) -> dict[str, Any]:
		section = self._config.get(name)
		if not isinstance(section, dict):
			raise InferenceConfigurationError(f"{name} configuration is missing")
		return section

	@staticmethod
	def _resolveConfiguredFile(
		modelBundle: ModelBundle,
		section: dict[str, Any],
		key: str,
	) -> Path:
		fileKey = section.get(key)
		try:
			return modelBundle.files[fileKey]
		except (KeyError, TypeError) as error:
			raise InferenceConfigurationError(f"{key} does not reference a resolved model file") from error

	@staticmethod
	def _inputName(session: Any, config: dict[str, Any]) -> str:
		configuredName = config.get("inputName")
		if configuredName is not None:
			if not isinstance(configuredName, str) or not configuredName:
				raise InferenceConfigurationError("inputName must be null or a non-empty string")
			return configuredName
		inputs = session.get_inputs()
		if len(inputs) != 1:
			raise InferenceConfigurationError("A model with multiple inputs requires inputName")
		return inputs[0].name

	def _loadCharacters(self, modelBundle: ModelBundle) -> list[str]:
		metadata = self._recognizer.get_modelmeta().custom_metadata_map
		metadataKey = self._recognizerConfig.get("characterMetadataKey", "character")
		if metadataKey in metadata:
			characters = metadata[metadataKey].splitlines()
		else:
			dictionaryKey = self._recognizerConfig.get("dictionaryFile")
			try:
				dictionaryPath = modelBundle.files[dictionaryKey]
			except (KeyError, TypeError) as error:
				raise InferenceConfigurationError(
					"Recognizer has no embedded character metadata and no dictionaryFile",
				) from error
			with dictionaryPath.open("r", encoding="utf-8") as dictionaryFile:
				characters = [line.rstrip("\r\n") for line in dictionaryFile]
		characters = [character for character in characters if character]
		if self._recognizerConfig.get("useSpaceCharacter", True) and " " not in characters:
			characters.append(" ")
		if not characters:
			raise InferenceConfigurationError("Recognition dictionary is empty")
		return characters

	def _readBgraFrame(self, framePath: Path, *, width: int, height: int, stride: int) -> Any:
		if width <= 0 or height <= 0 or stride < width * 4 or stride % 4:
			raise ValueError("Invalid BGRA frame metadata")
		expectedSize = stride * height
		if framePath.stat().st_size != expectedSize:
			raise ValueError("BGRA frame size does not match its metadata")
		bgra = self._numpy.memmap(
			framePath,
			dtype=self._numpy.uint8,
			mode="r",
			shape=(height, stride // 4, 4),
		)
		# NVDA captures BGRA and PP-OCR's OpenCV reference pipeline consumes BGR.
		# Keeping the first three channels avoids a subtle red/blue swap.
		return self._numpy.asarray(bgra[:, :width, :3]).copy()

	def _detect(self, rgbImage: Any) -> list[_Box]:
		height, width = rgbImage.shape[:2]
		maxSide = self._positiveInt(self._detectorConfig, "maxSide", 960)
		scale = min(1.0, maxSide / max(height, width))
		targetHeight = max(32, round((height * scale) / 32) * 32)
		targetWidth = max(32, round((width * scale) / 32) * 32)
		resized = self._resizeBilinear(rgbImage, targetHeight, targetWidth)
		tensor = self._normalizeImage(resized, self._detectorConfig)
		output = self._detector.run(None, {self._detectorInputName: tensor})[0]
		probabilityMap = self._numpy.asarray(output).squeeze()
		if probabilityMap.ndim != 2:
			raise RuntimeError(f"Detector output must reduce to 2 dimensions, got {probabilityMap.shape}")
		pixelThreshold = float(self._detectorConfig.get("pixelThreshold", 0.3))
		boxThreshold = float(self._detectorConfig.get("boxThreshold", 0.5))
		minimumArea = self._positiveInt(self._detectorConfig, "minimumComponentArea", 8)
		unclipRatio = float(self._detectorConfig.get("unclipRatio", 1.6))
		if unclipRatio < 0:
			raise InferenceConfigurationError("unclipRatio cannot be negative")
		if self._detectorConfig.get("useDilation", True):
			mask = probabilityMap >= pixelThreshold
			mask = mask | self._numpy.pad(mask[1:, :], ((0, 1), (0, 0)))
			mask = mask | self._numpy.pad(mask[:, 1:], ((0, 0), (0, 1)))
		else:
			mask = probabilityMap >= pixelThreshold
		components = self._connectedComponents(
			mask,
			probabilityMap,
			minimumArea=minimumArea,
			minimumScore=boxThreshold,
		)
		mapHeight, mapWidth = probabilityMap.shape
		boxes: list[_Box] = []
		for left, top, right, bottom in components:
			componentWidth = right - left + 1
			componentHeight = bottom - top + 1
			area = componentWidth * componentHeight
			perimeter = max(1, 2 * (componentWidth + componentHeight))
			expansion = area * unclipRatio / perimeter
			scaledLeft = max(0, int((left - expansion) * width / mapWidth))
			scaledTop = max(0, int((top - expansion) * height / mapHeight))
			scaledRight = min(width, int((right + 1 + expansion) * width / mapWidth))
			scaledBottom = min(height, int((bottom + 1 + expansion) * height / mapHeight))
			if scaledRight > scaledLeft and scaledBottom > scaledTop:
				boxes.append(_Box(scaledLeft, scaledTop, scaledRight, scaledBottom))
		return boxes

	def _connectedComponents(
		self,
		mask: Any,
		probabilityMap: Any,
		*,
		minimumArea: int,
		minimumScore: float,
	) -> list[tuple[int, int, int, int]]:
		# Label horizontal runs and union only overlapping runs in adjacent rows.
		# Runtime is proportional to the number of runs rather than foreground pixels.
		parents: list[int] = []
		bounds: list[list[int | float]] = []

		def find(label: int) -> int:
			while parents[label] != label:
				parents[label] = parents[parents[label]]
				label = parents[label]
			return label

		def union(first: int, second: int) -> int:
			firstRoot = find(first)
			secondRoot = find(second)
			if firstRoot == secondRoot:
				return firstRoot
			parents[secondRoot] = firstRoot
			firstBounds = bounds[firstRoot]
			secondBounds = bounds[secondRoot]
			firstBounds[0] = min(firstBounds[0], secondBounds[0])
			firstBounds[1] = min(firstBounds[1], secondBounds[1])
			firstBounds[2] = max(firstBounds[2], secondBounds[2])
			firstBounds[3] = max(firstBounds[3], secondBounds[3])
			firstBounds[4] += secondBounds[4]
			firstBounds[5] += secondBounds[5]
			return firstRoot

		previousRuns: list[tuple[int, int, int]] = []
		for y, row in enumerate(mask):
			padded = self._numpy.pad(row.astype(self._numpy.int8), (1, 1))
			transitions = self._numpy.flatnonzero(self._numpy.diff(padded))
			rowScoreCumulative = self._numpy.concatenate(
				(self._numpy.array([0.0]), self._numpy.cumsum(probabilityMap[y], dtype=float)),
			)
			currentRuns: list[tuple[int, int, int]] = []
			previousIndex = 0
			for start, end in transitions.reshape(-1, 2):
				start = int(start)
				end = int(end)
				label = len(parents)
				parents.append(label)
				area = end - start
				scoreSum = float(rowScoreCumulative[end] - rowScoreCumulative[start])
				bounds.append([start, y, end - 1, y, area, scoreSum])
				while previousIndex < len(previousRuns) and previousRuns[previousIndex][1] < start:
					previousIndex += 1
				candidateIndex = previousIndex
				while candidateIndex < len(previousRuns) and previousRuns[candidateIndex][0] < end:
					previousStart, previousEnd, previousLabel = previousRuns[candidateIndex]
					if previousEnd >= start and previousStart < end:
						label = union(label, previousLabel)
					candidateIndex += 1
				currentRuns.append((start, end, label))
			previousRuns = currentRuns

		components: list[tuple[int, int, int, int]] = []
		for label, component in enumerate(bounds):
			if find(label) != label:
				continue
			left, top, right, bottom, area, scoreSum = component
			if area >= minimumArea and scoreSum / area >= minimumScore:
				components.append((int(left), int(top), int(right), int(bottom)))
		return components

	def _deskewCrop(self, crop: Any) -> Any | None:
		"""Deskew a failed horizontal-text crop using its foreground principal axis."""
		maximumAngle = self._recognizerConfig.get("deskewMaximumAngle", 0)
		if type(maximumAngle) not in (int, float) or not 0 <= maximumAngle <= 30:
			raise InferenceConfigurationError("deskewMaximumAngle must be between 0 and 30")
		if maximumAngle == 0 or min(crop.shape[:2]) < 3:
			return None
		minimumAngle = self._recognizerConfig.get("deskewMinimumAngle", 2)
		if type(minimumAngle) not in (int, float) or not 0 <= minimumAngle <= maximumAngle:
			raise InferenceConfigurationError(
				"deskewMinimumAngle must be between 0 and deskewMaximumAngle",
			)
		minimumAspectRatio = self._recognizerConfig.get("deskewMinimumAspectRatio", 4)
		if type(minimumAspectRatio) not in (int, float) or minimumAspectRatio <= 1:
			raise InferenceConfigurationError("deskewMinimumAspectRatio must be greater than 1")
		foregroundThreshold = self._positiveInt(
			self._recognizerConfig,
			"deskewForegroundThreshold",
			20,
		)
		if foregroundThreshold > 255:
			raise InferenceConfigurationError("deskewForegroundThreshold must be at most 255")

		border = self._numpy.concatenate((crop[0], crop[-1], crop[:, 0], crop[:, -1]))
		background = self._numpy.median(border, axis=0)
		foreground = self._foregroundMask(crop, background, foregroundThreshold)
		trimmed = self._trimToForeground(crop, foreground)
		if trimmed is None:
			return None
		trimmedCrop, trimmedMask = trimmed
		y, x = self._numpy.nonzero(trimmedMask)
		if len(x) < 20:
			return None
		x = x.astype(self._numpy.float64)
		y = y.astype(self._numpy.float64)
		x -= x.mean()
		y -= y.mean()
		covarianceX = float(self._numpy.mean(x * x))
		covarianceY = float(self._numpy.mean(y * y))
		covarianceXY = float(self._numpy.mean(x * y))
		angle = 0.5 * self._numpy.degrees(
			self._numpy.arctan2(2 * covarianceXY, covarianceX - covarianceY),
		)
		trace = covarianceX + covarianceY
		discriminant = ((covarianceX - covarianceY) ** 2 + 4 * covarianceXY**2) ** 0.5
		majorVariance = (trace + discriminant) / 2
		minorVariance = max((trace - discriminant) / 2, 1e-9)
		if majorVariance / minorVariance < minimumAspectRatio:
			return None
		if abs(angle) < minimumAngle or abs(angle) > maximumAngle:
			return None
		rotated = self._rotateBilinear(trimmedCrop, float(angle), background)
		rotatedForeground = self._foregroundMask(rotated, background, foregroundThreshold)
		rotatedTrimmed = self._trimToForeground(rotated, rotatedForeground)
		return rotatedTrimmed[0] if rotatedTrimmed is not None else None

	def _foregroundMask(self, image: Any, background: Any, threshold: int) -> Any:
		difference = self._numpy.abs(image.astype(self._numpy.float32) - background)
		return self._numpy.max(difference, axis=2) >= threshold

	def _trimToForeground(self, image: Any, foreground: Any) -> tuple[Any, Any] | None:
		y, x = self._numpy.nonzero(foreground)
		if len(x) < 20:
			return None
		padding = max(2, round(min(image.shape[:2]) * 0.025))
		left = max(0, int(x.min()) - padding)
		right = min(image.shape[1], int(x.max()) + padding + 1)
		top = max(0, int(y.min()) - padding)
		bottom = min(image.shape[0], int(y.max()) + padding + 1)
		return image[top:bottom, left:right], foreground[top:bottom, left:right]

	def _rotateBilinear(self, image: Any, angleDegrees: float, fillColor: Any) -> Any:
		"""Rotate an image with expansion, using image-coordinate counter-clockwise angles."""
		height, width = image.shape[:2]
		angle = self._numpy.radians(angleDegrees)
		cosine = float(self._numpy.cos(angle))
		sine = float(self._numpy.sin(angle))
		outputWidth = max(1, int(self._numpy.ceil(abs(width * cosine) + abs(height * sine))))
		outputHeight = max(1, int(self._numpy.ceil(abs(height * cosine) + abs(width * sine))))
		output = self._numpy.empty((outputHeight, outputWidth, image.shape[2]), dtype=self._numpy.uint8)
		output[:] = self._numpy.asarray(fillColor, dtype=self._numpy.uint8)
		# Limit transient coordinate/interpolation arrays for wide desktop captures.
		for rowStart in range(0, outputHeight, 128):
			rowEnd = min(rowStart + 128, outputHeight)
			outputY, outputX = self._numpy.mgrid[rowStart:rowEnd, 0:outputWidth]
			centeredX = outputX - (outputWidth - 1) / 2
			centeredY = outputY - (outputHeight - 1) / 2
			sourceX = cosine * centeredX - sine * centeredY + (width - 1) / 2
			sourceY = sine * centeredX + cosine * centeredY + (height - 1) / 2
			valid = (sourceX >= 0) & (sourceX <= width - 1) & (sourceY >= 0) & (sourceY <= height - 1)
			x0 = self._numpy.floor(sourceX).astype(int)
			y0 = self._numpy.floor(sourceY).astype(int)
			x0 = self._numpy.clip(x0, 0, width - 1)
			y0 = self._numpy.clip(y0, 0, height - 1)
			x1 = self._numpy.minimum(x0 + 1, width - 1)
			y1 = self._numpy.minimum(y0 + 1, height - 1)
			xWeight = (sourceX - x0)[..., self._numpy.newaxis]
			yWeight = (sourceY - y0)[..., self._numpy.newaxis]
			top = image[y0, x0] * (1 - xWeight) + image[y0, x1] * xWeight
			bottom = image[y1, x0] * (1 - xWeight) + image[y1, x1] * xWeight
			interpolated = self._numpy.clip(top * (1 - yWeight) + bottom * yWeight, 0, 255)
			outputBlock = output[rowStart:rowEnd]
			outputBlock[valid] = interpolated[valid].astype(self._numpy.uint8)
		return output

	def _recognizeCrop(self, crop: Any) -> tuple[str, float]:
		targetHeight = self._positiveInt(self._recognizerConfig, "height", 48)
		maxWidth = self._positiveInt(self._recognizerConfig, "maxWidth", 2048)
		height, width = crop.shape[:2]
		targetWidth = max(1, min(maxWidth, round(width * targetHeight / height)))
		resized = self._resizeBilinear(crop, targetHeight, targetWidth)
		modelWidth = max(32, int(self._numpy.ceil(targetWidth / 32)) * 32)
		padded = self._numpy.zeros((targetHeight, modelWidth, 3), dtype=self._numpy.uint8)
		padded[:, :targetWidth] = resized
		tensor = self._normalizeImage(padded, self._recognizerConfig)
		output = self._recognizer.run(None, {self._recognizerInputName: tensor})[0]
		probabilities = self._asTimeClassMatrix(output)
		return self._decodeCtc(probabilities)

	def _normalizeImage(self, image: Any, config: dict[str, Any]) -> Any:
		mean = self._vector(config, "mean")
		scale = self._vector(config, "scale")
		normalized = image.astype(self._numpy.float32) / 255.0
		normalized = (normalized - mean) * scale
		return self._numpy.transpose(normalized, (2, 0, 1))[self._numpy.newaxis, ...]

	def _vector(self, config: dict[str, Any], key: str) -> Any:
		value = config.get(key)
		if not isinstance(value, list) or len(value) != 3:
			raise InferenceConfigurationError(f"{key} must contain three numbers")
		try:
			return self._numpy.asarray(value, dtype=self._numpy.float32)
		except (TypeError, ValueError) as error:
			raise InferenceConfigurationError(f"{key} must contain three numbers") from error

	def _asTimeClassMatrix(self, output: Any) -> Any:
		matrix = self._numpy.asarray(output)
		if matrix.ndim == 3 and matrix.shape[0] == 1:
			matrix = matrix[0]
		elif matrix.ndim == 3 and matrix.shape[1] == 1:
			matrix = matrix[:, 0, :]
		if matrix.ndim != 2:
			raise RuntimeError(f"Recognizer output must reduce to [time, classes], got {matrix.shape}")
		rowSums = matrix.sum(axis=1)
		isProbability = (
			float(matrix.min()) >= 0
			and float(matrix.max()) <= 1
			and float(self._numpy.mean(self._numpy.abs(rowSums - 1))) < 0.05
		)
		if not isProbability:
			matrix = matrix - matrix.max(axis=1, keepdims=True)
			matrix = self._numpy.exp(matrix)
			matrix /= matrix.sum(axis=1, keepdims=True)
		return matrix

	def _decodeCtc(self, probabilities: Any) -> tuple[str, float]:
		blankIndex = int(self._recognizerConfig.get("blankIndex", 0))
		characterIndexOffset = int(self._recognizerConfig.get("characterIndexOffset", 1))
		indices = probabilities.argmax(axis=1)
		confidences = probabilities.max(axis=1)
		decoded: list[str] = []
		decodedConfidences: list[float] = []
		previousIndex: int | None = None
		for rawIndex, rawConfidence in zip(indices, confidences, strict=True):
			index = int(rawIndex)
			if index != blankIndex and index != previousIndex:
				characterIndex = index - characterIndexOffset
				if 0 <= characterIndex < len(self._characters):
					decoded.append(self._characters[characterIndex])
					decodedConfidences.append(float(rawConfidence))
			previousIndex = index
		confidence = sum(decodedConfidences) / len(decodedConfidences) if decodedConfidences else 0.0
		return "".join(decoded).strip(), confidence

	def _resizeBilinear(self, image: Any, targetHeight: int, targetWidth: int) -> Any:
		sourceHeight, sourceWidth = image.shape[:2]
		if (sourceHeight, sourceWidth) == (targetHeight, targetWidth):
			return image.copy()
		y = self._numpy.linspace(0, sourceHeight - 1, targetHeight)
		x = self._numpy.linspace(0, sourceWidth - 1, targetWidth)
		y0 = self._numpy.floor(y).astype(int)
		x0 = self._numpy.floor(x).astype(int)
		y1 = self._numpy.minimum(y0 + 1, sourceHeight - 1)
		x1 = self._numpy.minimum(x0 + 1, sourceWidth - 1)
		yWeight = (y - y0)[:, None, None]
		xWeight = (x - x0)[None, :, None]
		top = image[y0[:, None], x0[None, :]] * (1 - xWeight) + image[y0[:, None], x1[None, :]] * xWeight
		bottom = image[y1[:, None], x0[None, :]] * (1 - xWeight) + image[y1[:, None], x1[None, :]] * xWeight
		return self._numpy.clip(top * (1 - yWeight) + bottom * yWeight, 0, 255).astype(
			self._numpy.uint8,
		)

	@staticmethod
	def _positiveInt(config: dict[str, Any], key: str, default: int) -> int:
		value = config.get(key, default)
		if type(value) is not int or value <= 0:
			raise InferenceConfigurationError(f"{key} must be a positive integer")
		return value

	@staticmethod
	def _toLines(
		recognizedBoxes: list[tuple[_Box, str, float]],
	) -> list[list[dict[str, int | str | float]]]:
		lineBoxes: list[list[tuple[_Box, str, float]]] = []
		for item in sorted(recognizedBoxes, key=lambda value: (value[0].centerY, value[0].left)):
			box = item[0]
			for line in lineBoxes:
				lineCenter = sum(lineItem[0].centerY for lineItem in line) / len(line)
				lineHeight = max(lineItem[0].height for lineItem in line)
				if abs(box.centerY - lineCenter) <= max(box.height, lineHeight) * 0.6:
					line.append(item)
					break
			else:
				lineBoxes.append([item])
		lines: list[list[dict[str, int | str | float]]] = []
		for line in lineBoxes:
			words = []
			for box, text, confidence in sorted(line, key=lambda value: value[0].left):
				words.append(
					{
						"x": box.left,
						"y": box.top,
						"width": box.width,
						"height": box.height,
						"text": text,
						"confidence": confidence,
					},
				)
			lines.append(words)
		return lines
