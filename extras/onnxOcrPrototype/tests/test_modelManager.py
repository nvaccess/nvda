# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NVDA Contributors
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# ruff: noqa: I001

import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

_PLUGIN_DIRECTORY = Path(__file__).resolve().parents[1] / "nvdaAddon" / "globalPlugins" / "onnxOcrPrototype"
sys.path.insert(0, str(_PLUGIN_DIRECTORY))

from worker.modelManager import ManifestError, ModelIntegrityError, ModelManager


class TestModelManager(unittest.TestCase):
	def setUp(self) -> None:
		self._temporaryDirectory = tempfile.TemporaryDirectory()
		self.addCleanup(self._temporaryDirectory.cleanup)
		self._root = Path(self._temporaryDirectory.name)
		self._sourceDirectory = self._root / "source"
		self._sourceDirectory.mkdir()
		self._sourceFiles = {
			"detector": self._writeSource("detector.onnx", b"detector"),
			"recognizer": self._writeSource("recognizer.onnx", b"recognizer"),
			"dictionary": self._writeSource("dictionary.txt", b"a\nb\n"),
		}

	def _writeSource(self, name: str, content: bytes) -> Path:
		path = self._sourceDirectory / name
		path.write_bytes(content)
		return path

	def _writeManifest(
		self,
		*,
		detectorFileName: str = "detector.onnx",
		schemaVersion: int = 1,
		includeDictionary: bool = True,
	) -> Path:
		files = {}
		for key, source in self._sourceFiles.items():
			if key == "dictionary" and not includeDictionary:
				continue
			files[key] = {
				"file": detectorFileName if key == "detector" else source.name,
				"url": source.as_uri(),
				"sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
				"sizeBytes": source.stat().st_size,
			}
		manifest = {
			"schemaVersion": schemaVersion,
			"id": "test-model",
			"files": files,
			"detector": {"modelFile": "detector"},
			"recognizer": {"modelFile": "recognizer"},
		}
		if includeDictionary:
			manifest["recognizer"]["dictionaryFile"] = "dictionary"
		if schemaVersion == 2:
			manifest.update(
				{
					"displayName": "Test model",
					"modelLicense": "Apache-2.0",
					"modelSource": "https://example.com/test-model",
					"languages": ["English"],
				},
			)
		path = self._root / "manifest.json"
		path.write_text(json.dumps(manifest), encoding="utf-8")
		return path

	def test_downloadsAndVerifiesFiles(self) -> None:
		manager = ModelManager(self._root / "cache")
		manifestPath = self._writeManifest()
		self.assertFalse(manager.getStatus(manifestPath).ready)
		bundle = manager.ensureModels(manifestPath)
		self.assertEqual(bundle.manifestId, "test-model")
		self.assertEqual(bundle.files["detector"].read_bytes(), b"detector")
		self.assertEqual(bundle.files["recognizer"].read_bytes(), b"recognizer")
		self.assertEqual(bundle.files["dictionary"].read_bytes(), b"a\nb\n")
		self.assertNotEqual(bundle.files["detector"], self._sourceFiles["detector"])
		self.assertTrue(manager.getStatus(manifestPath).ready)

	def test_schemaTwoAllowsEmbeddedRecognizerDictionary(self) -> None:
		bundle = ModelManager(self._root / "cache").ensureModels(
			self._writeManifest(schemaVersion=2, includeDictionary=False),
		)
		self.assertEqual(set(bundle.files), {"detector", "recognizer"})

	def test_corruptCacheIsReplaced(self) -> None:
		manager = ModelManager(self._root / "cache")
		manifestPath = self._writeManifest()
		bundle = manager.ensureModels(manifestPath)
		bundle.files["detector"].write_bytes(b"corrupt")
		status = manager.getStatus(manifestPath)
		self.assertFalse(status.ready)
		self.assertEqual(status.invalidFiles, ("detector",))
		repairedBundle = manager.ensureModels(manifestPath)
		self.assertEqual(repairedBundle.files["detector"].read_bytes(), b"detector")

	def test_rejectsPathTraversal(self) -> None:
		manifestPath = self._writeManifest(detectorFileName="../detector.onnx")
		with self.assertRaises(ManifestError):
			ModelManager(self._root / "cache").ensureModels(manifestPath)

	def test_rejectsWindowsUnsafeFileNamesOnEveryPlatform(self) -> None:
		for fileName in ("..\\detector.onnx", "CON.onnx", "model.onnx.", "model:onxx"):
			with self.subTest(fileName=fileName):
				manifestPath = self._writeManifest(detectorFileName=fileName)
				with self.assertRaises(ManifestError):
					ModelManager.loadManifest(manifestPath)

	def test_rejectsWindowsReservedManifestId(self) -> None:
		manifestPath = self._writeManifest()
		manifest = json.loads(manifestPath.read_text(encoding="utf-8"))
		manifest["id"] = "NUL"
		manifestPath.write_text(json.dumps(manifest), encoding="utf-8")
		with self.assertRaises(ManifestError):
			ModelManager.loadManifest(manifestPath)

	def test_rejectsDuplicateJsonKeys(self) -> None:
		manifestPath = self._writeManifest()
		manifestText = manifestPath.read_text(encoding="utf-8")
		manifestPath.write_text(manifestText[:-1] + ', "id": "shadowed"}', encoding="utf-8")
		with self.assertRaises(ManifestError):
			ModelManager.loadManifest(manifestPath)

	def test_rejectsIncorrectHash(self) -> None:
		manifestPath = self._writeManifest()
		manifest = json.loads(manifestPath.read_text(encoding="utf-8"))
		manifest["files"]["detector"]["sha256"] = "0" * 64
		manifestPath.write_text(json.dumps(manifest), encoding="utf-8")
		with self.assertRaises(ModelIntegrityError):
			ModelManager(self._root / "cache").ensureModels(manifestPath)

	def test_rejectsMissingDeclaredSize(self) -> None:
		manifestPath = self._writeManifest()
		manifest = json.loads(manifestPath.read_text(encoding="utf-8"))
		del manifest["files"]["detector"]["sizeBytes"]
		manifestPath.write_text(json.dumps(manifest), encoding="utf-8")
		with self.assertRaises(ManifestError):
			ModelManager(self._root / "cache").ensureModels(manifestPath)

	def test_rejectsBooleanDeclaredSize(self) -> None:
		manifestPath = self._writeManifest()
		manifest = json.loads(manifestPath.read_text(encoding="utf-8"))
		manifest["files"]["detector"]["sizeBytes"] = True
		manifestPath.write_text(json.dumps(manifest), encoding="utf-8")
		with self.assertRaises(ManifestError):
			ModelManager.loadManifest(manifestPath)

	def test_rejectsDuplicateFileNamesCaseInsensitively(self) -> None:
		manifestPath = self._writeManifest()
		manifest = json.loads(manifestPath.read_text(encoding="utf-8"))
		manifest["files"]["recognizer"]["file"] = "DETECTOR.onnx"
		manifestPath.write_text(json.dumps(manifest), encoding="utf-8")
		with self.assertRaises(ManifestError):
			ModelManager.loadManifest(manifestPath)

	def test_rejectsBundleLargerThanOneGiB(self) -> None:
		manifestPath = self._writeManifest()
		manifest = json.loads(manifestPath.read_text(encoding="utf-8"))
		manifest["files"]["detector"]["sizeBytes"] = 600 * 1024 * 1024
		manifest["files"]["recognizer"]["sizeBytes"] = 600 * 1024 * 1024
		manifestPath.write_text(json.dumps(manifest), encoding="utf-8")
		with self.assertRaises(ManifestError):
			ModelManager.loadManifest(manifestPath)


if __name__ == "__main__":
	unittest.main()
