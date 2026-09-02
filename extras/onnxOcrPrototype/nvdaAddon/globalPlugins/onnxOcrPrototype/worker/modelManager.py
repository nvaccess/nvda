# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NVDA Contributors
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Validated manifest and download support for separately distributed OCR models.

The model manager deliberately uses only the Python standard library. It is used
inside the OCR worker, never in NVDA's main process. Model files are downloaded
to a cache outside the add-on, verified before use and atomically published.
"""

import hashlib
import json
import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.request import Request, urlopen

_MANIFEST_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")
_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
_ALLOWED_URL_SCHEMES = frozenset(("https", "file"))
_DOWNLOAD_CHUNK_SIZE = 1024 * 1024
_MAX_MODEL_FILE_SIZE = 1024 * 1024 * 1024
_MAX_MODEL_BUNDLE_SIZE = 1024 * 1024 * 1024
_UNSAFE_WINDOWS_FILE_NAME_PATTERN = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
_WINDOWS_RESERVED_FILE_STEMS = frozenset(
	("con", "prn", "aux", "nul"),
) | frozenset(f"{prefix}{number}" for prefix in ("com", "lpt") for number in range(1, 10))


class ManifestError(ValueError):
	"""The model manifest is invalid or unsafe."""


class ModelIntegrityError(RuntimeError):
	"""A cached or downloaded model file failed its integrity check."""


@dataclass(frozen=True)
class ModelFile:
	"""One downloadable file declared by a model manifest."""

	key: str
	fileName: str
	url: str
	sha256: str
	sizeBytes: int


@dataclass(frozen=True)
class ModelBundle:
	"""Resolved model files and inference configuration."""

	manifestId: str
	files: dict[str, Path]
	config: dict[str, Any]


@dataclass(frozen=True)
class ModelStatus:
	"""Installation state of one model bundle."""

	manifestId: str
	ready: bool
	missingFiles: tuple[str, ...]
	invalidFiles: tuple[str, ...]


class ModelManager:
	"""Resolve and verify model files in a cache outside the add-on and repository."""

	def __init__(self, cacheRoot: Path) -> None:
		self._cacheRoot = cacheRoot.expanduser().resolve()

	def ensureModels(self, manifestPath: Path) -> ModelBundle:
		"""Download missing files and return a verified model bundle."""
		manifest = self.loadManifest(manifestPath)
		bundleDirectory = self._cacheRoot / manifest["id"]
		bundleDirectory.mkdir(parents=True, exist_ok=True)
		resolvedFiles: dict[str, Path] = {}
		for modelFile in manifest["_validatedFiles"]:
			target = bundleDirectory / modelFile.fileName
			self._ensureFile(modelFile, target)
			resolvedFiles[modelFile.key] = target
		return ModelBundle(
			manifestId=manifest["id"],
			files=resolvedFiles,
			config={key: value for key, value in manifest.items() if key != "_validatedFiles"},
		)

	def getStatus(self, manifestPath: Path) -> ModelStatus:
		"""Return cache status without downloading or importing native libraries."""
		manifest = self.loadManifest(manifestPath)
		bundleDirectory = self._cacheRoot / manifest["id"]
		missingFiles: list[str] = []
		invalidFiles: list[str] = []
		for modelFile in manifest["_validatedFiles"]:
			target = bundleDirectory / modelFile.fileName
			if not target.is_file():
				missingFiles.append(modelFile.key)
				continue
			try:
				self._verifyFile(modelFile, target)
			except (OSError, ModelIntegrityError):
				invalidFiles.append(modelFile.key)
		return ModelStatus(
			manifestId=manifest["id"],
			ready=not missingFiles and not invalidFiles,
			missingFiles=tuple(missingFiles),
			invalidFiles=tuple(invalidFiles),
		)

	@staticmethod
	def loadManifest(manifestPath: Path) -> dict[str, Any]:
		"""Load and validate a supported OCR model manifest."""
		try:
			with manifestPath.open("r", encoding="utf-8") as manifestFile:
				manifest = json.load(manifestFile, object_pairs_hook=ModelManager._objectWithoutDuplicateKeys)
		except (OSError, json.JSONDecodeError) as error:
			raise ManifestError(f"Unable to read model manifest: {error}") from error
		if not isinstance(manifest, dict):
			raise ManifestError("Model manifest root must be an object")
		if manifest.get("schemaVersion") not in (1, 2):
			raise ManifestError("Only model manifest schemaVersion 1 or 2 is supported")
		manifestId = manifest.get("id")
		if (
			not isinstance(manifestId, str)
			or not _MANIFEST_ID_PATTERN.fullmatch(manifestId)
			or not ModelManager._isSafeWindowsPathComponent(manifestId)
		):
			raise ManifestError("Model manifest id is invalid")
		files = manifest.get("files")
		if not isinstance(files, dict) or not files:
			raise ManifestError("Model manifest files must be a non-empty object")
		validatedFiles: list[ModelFile] = []
		for key, value in files.items():
			validatedFiles.append(ModelManager._validateFile(key, value))
		fileNames = [modelFile.fileName.casefold() for modelFile in validatedFiles]
		if len(fileNames) != len(set(fileNames)):
			raise ManifestError("Model manifest file names must be unique")
		if sum(modelFile.sizeBytes for modelFile in validatedFiles) > _MAX_MODEL_BUNDLE_SIZE:
			raise ManifestError(
				f"Model manifest total size must not exceed {_MAX_MODEL_BUNDLE_SIZE} bytes",
			)
		for sectionName in ("detector", "recognizer"):
			if not isinstance(manifest.get(sectionName), dict):
				raise ManifestError(f"Model manifest requires a {sectionName} object")
		fileKeys = set(files)
		detectorModelKey = manifest["detector"].get("modelFile")
		recognizerModelKey = manifest["recognizer"].get("modelFile")
		dictionaryKey = manifest["recognizer"].get("dictionaryFile")
		for description, key in (
			("detector modelFile", detectorModelKey),
			("recognizer modelFile", recognizerModelKey),
		):
			if key not in fileKeys:
				raise ManifestError(f"{description} does not reference a declared file")
		if dictionaryKey is not None and dictionaryKey not in fileKeys:
			raise ManifestError("recognizer dictionaryFile does not reference a declared file")
		if dictionaryKey is None and manifest["schemaVersion"] == 1:
			raise ManifestError("schemaVersion 1 requires recognizer dictionaryFile")
		if manifest["schemaVersion"] == 2:
			ModelManager._validateMetadata(manifest)
		manifest["_validatedFiles"] = validatedFiles
		return manifest

	@staticmethod
	def _objectWithoutDuplicateKeys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
		result: dict[str, Any] = {}
		for key, value in pairs:
			if key in result:
				raise ManifestError(f"Model manifest contains duplicate key {key!r}")
			result[key] = value
		return result

	@staticmethod
	def _isSafeWindowsPathComponent(value: str) -> bool:
		if (
			not value
			or len(value) > 255
			or value.endswith((" ", "."))
			or _UNSAFE_WINDOWS_FILE_NAME_PATTERN.search(value)
		):
			return False
		stem = value.split(".", 1)[0].casefold()
		return stem not in _WINDOWS_RESERVED_FILE_STEMS

	@staticmethod
	def _validateMetadata(manifest: dict[str, Any]) -> None:
		for key in ("displayName", "modelLicense", "modelSource"):
			value = manifest.get(key)
			if not isinstance(value, str) or not value.strip():
				raise ManifestError(f"Model manifest {key} must be a non-empty string")
		languages = manifest.get("languages")
		if (
			not isinstance(languages, list)
			or not languages
			or not all(isinstance(language, str) and language for language in languages)
		):
			raise ManifestError("Model manifest languages must be a non-empty list of strings")

	@staticmethod
	def _validateFile(key: Any, value: Any) -> ModelFile:
		if not isinstance(key, str) or not key:
			raise ManifestError("Model file keys must be non-empty strings")
		if not isinstance(value, dict):
			raise ManifestError(f"Model file {key!r} must be an object")
		fileName = value.get("file")
		if not isinstance(fileName, str) or not ModelManager._isSafeWindowsPathComponent(fileName):
			raise ManifestError(f"Model file {key!r} has an unsafe file name")
		url = value.get("url")
		if not isinstance(url, str) or urlparse(url).scheme not in _ALLOWED_URL_SCHEMES:
			raise ManifestError(f"Model file {key!r} URL must use HTTPS or file")
		sha256 = value.get("sha256")
		if not isinstance(sha256, str) or not _SHA256_PATTERN.fullmatch(sha256):
			raise ManifestError(f"Model file {key!r} requires a lowercase SHA-256 digest")
		sizeBytes = value.get("sizeBytes")
		if type(sizeBytes) is not int or not 0 < sizeBytes <= _MAX_MODEL_FILE_SIZE:
			raise ManifestError(
				f"Model file {key!r} sizeBytes must be between 1 and {_MAX_MODEL_FILE_SIZE}",
			)
		return ModelFile(
			key=key,
			fileName=fileName,
			url=url,
			sha256=sha256,
			sizeBytes=sizeBytes,
		)

	def _ensureFile(self, modelFile: ModelFile, target: Path) -> None:
		if target.exists():
			try:
				self._verifyFile(modelFile, target)
				return
			except (OSError, ModelIntegrityError):
				# A partial/corrupt cache must self-heal. The replacement is still
				# downloaded and verified before the existing file is removed.
				pass
		target.parent.mkdir(parents=True, exist_ok=True)
		downloadPath: Path | None = None
		try:
			with tempfile.NamedTemporaryFile(
				prefix=f".{target.name}.",
				suffix=".part",
				dir=target.parent,
				delete=False,
			) as downloadFile:
				downloadPath = Path(downloadFile.name)
				request = Request(
					modelFile.url,
					headers={"User-Agent": "NVDA-ONNX-OCR-Prototype/0.1"},
				)
				with urlopen(request, timeout=30) as response:
					finalScheme = urlparse(response.geturl()).scheme
					if finalScheme not in _ALLOWED_URL_SCHEMES:
						raise ManifestError("Model download redirected to an unsafe URL scheme")
					totalBytes = 0
					while chunk := response.read(_DOWNLOAD_CHUNK_SIZE):
						downloadFile.write(chunk)
						totalBytes += len(chunk)
						if totalBytes > modelFile.sizeBytes:
							raise ModelIntegrityError(
								f"Downloaded {modelFile.key!r} exceeds declared size",
							)
			self._verifyFile(modelFile, downloadPath)
			os.replace(downloadPath, target)
			downloadPath = None
		finally:
			if downloadPath is not None:
				downloadPath.unlink(missing_ok=True)

	@staticmethod
	def _verifyFile(modelFile: ModelFile, path: Path) -> None:
		if path.stat().st_size != modelFile.sizeBytes:
			raise ModelIntegrityError(f"Size check failed for model file {modelFile.key!r}")
		digest = hashlib.sha256()
		with path.open("rb") as modelFileHandle:
			while chunk := modelFileHandle.read(_DOWNLOAD_CHUNK_SIZE):
				digest.update(chunk)
		if digest.hexdigest() != modelFile.sha256:
			raise ModelIntegrityError(f"SHA-256 check failed for model file {modelFile.key!r}")
