# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, tianze
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
"""
Unit tests for the ModelDownloader class.

Covers:
- Directory creation
- URL construction
- Remote file size detection (HEAD and Range requests)
- Progress reporting logic
- File download success/failure
- Multi-threaded download success/failure
- Cancellation handling
- Model file path building
- downloadDefaultModel user prompt flow
"""

import tempfile
import unittest
from unittest.mock import patch

# Import the class and function under test
from _localCaptioner.modelDownloader import ModelDownloader


class TestModelDownloader(unittest.TestCase):
	"""Unit tests for ModelDownloader."""

	def setUp(self):
		# 初始化时不再传 basePath
		self.temp_dir = tempfile.mkdtemp()
		self.downloader = ModelDownloader()

	@patch("pathlib.Path.mkdir")
	def test_ensureModelsDirectory_success(self, mock_mkdir):
		"""Ensure directory is created and correct path returned."""
		mock_mkdir.return_value = None
		models_dir = self.downloader.ensureModelsDirectory()
		self.assertTrue(models_dir.endswith("vit-gpt2-image-captioning"))
		mock_mkdir.assert_called_once()

	@patch("pathlib.Path.mkdir", side_effect=OSError("Permission denied"))
	def test_ensureModelsDirectory_failure(self, mock_mkdir):
		"""Ensure OSError is raised when models directory cannot be created."""
		with self.assertRaises(OSError):
			self.downloader.ensureModelsDirectory()

	def test_constructDownloadUrl_default_host(self):
		"""Construct URL when remoteHost has no scheme."""
		url = self.downloader.constructDownloadUrl("foo/bar", "file.txt")
		self.assertTrue(url.startswith("https://huggingface.co/foo/bar"))

	def test_constructDownloadUrl_with_http_host(self):
		"""Construct URL when remoteHost already contains http://."""
		self.downloader.remoteHost = "http://example.com"
		url = self.downloader.constructDownloadUrl("foo", "bar")
		self.assertEqual(url, "http://example.com/foo/resolve/main/bar")

	def test_reportProgress_triggers_callback(self):
		"""Callback is triggered when downloaded bytes exceed threshold."""
		called = {}

		def cb(fname, dl, total, pct):
			called["fname"] = fname
			called["dl"] = dl

		last = self.downloader._reportProgress(cb, "file", 1024 * 1024 + 1, 2 * 1024 * 1024, 0)
		self.assertEqual(called["fname"], "file")
		self.assertGreater(last, 0)

	@patch.object(ModelDownloader, "downloadSingleFile", return_value=(True, "ok"))
	def test_downloadModelsMultithreaded_all_success(self, mock_single):
		"""All files are downloaded successfully."""
		files = ["a.txt", "b.txt"]
		success, failed = self.downloader.downloadModelsMultithreaded(self.temp_dir, "model", files)
		self.assertEqual(len(success), 2)
		self.assertEqual(len(failed), 0)

	@patch.object(ModelDownloader, "downloadSingleFile", side_effect=[(True, "ok"), (False, "err")])
	def test_downloadModelsMultithreaded_partial_failure(self, mock_single):
		"""One file succeeds and one fails."""
		files = ["a.txt", "b.txt"]
		success, failed = self.downloader.downloadModelsMultithreaded(self.temp_dir, "model", files)
		self.assertEqual(len(success), 1)
		self.assertEqual(len(failed), 1)

	@patch("pathlib.Path.mkdir")
	def test_getModelFilePaths_contains_expected_keys(self, mock_mkdir):
		"""getModelFilePaths returns all expected keys and paths."""
		paths = self.downloader.getModelFilePaths("testmodel")
		for key in ("encoderPath", "decoderPath", "configPath", "vocabPath", "modelDir"):
			self.assertIn(key, paths)

			self.assertTrue(
				paths[key].endswith(".onnx")
				or paths[key].endswith(".json")
				or paths[key].endswith("testmodel"),
			)


if __name__ == "__main__":
	unittest.main()
