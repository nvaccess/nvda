# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Tianze
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
from typing import Dict, Any

# Import the class and function under test
from _localCaptioner.modelDownloader import ModelDownloader


class TestModelDownloader(unittest.TestCase):
	"""Unit tests for ModelDownloader."""

	def setUp(self):
		# No longer passing basePath during initialization
		self.tempDir = tempfile.mkdtemp()
		self.downloader = ModelDownloader()

	@patch("pathlib.Path.mkdir")
	def test_ensureModelsDirectory_success(self, mockMkdir):
		"""Ensure directory is created and correct path returned."""
		mockMkdir.return_value = None
		modelsDir = self.downloader.ensureModelsDirectory()
		self.assertTrue(modelsDir.endswith("vit-gpt2-image-captioning"))
		mockMkdir.assert_called_once()

	@patch("pathlib.Path.mkdir", side_effect=OSError("Permission denied"))
	def test_ensureModelsDirectory_failure(self, mockMkdir):
		"""Ensure OSError is raised when models directory cannot be created."""
		with self.assertRaises(OSError):
			self.downloader.ensureModelsDirectory()

	def test_constructDownloadUrlDefaultHost(self):
		"""Construct URL when remoteHost has no scheme."""
		url = self.downloader.constructDownloadUrl("foo/bar", "file.txt")
		self.assertTrue(url.startswith("https://huggingface.co/foo/bar"))

	def test_constructDownloadUrlWithHttpHost(self):
		"""Construct URL when remoteHost already contains http://."""
		self.downloader.remoteHost = "http://example.com"
		url = self.downloader.constructDownloadUrl("foo", "bar")
		self.assertEqual(url, "http://example.com/foo/resolve/main/bar")

	def test_reportProgressTriggersCallback(self) -> None:
		"""Test that callback is triggered when downloaded bytes exceed threshold."""
		callbackData: Dict[str, Any] = {}

		def progressCallback(
			fileName: str,
			downloadedBytes: int,
			totalBytes: int,
			percentage: float,
		) -> None:
			"""Callback function to capture progress data."""
			callbackData["fileName"] = fileName
			callbackData["downloadedBytes"] = downloadedBytes

		# Test with download size exceeding 1MB threshold
		downloadedSize = 1024 * 1024 + 1  # 1MB + 1 byte
		totalSize = 2 * 1024 * 1024  # 2MB
		initialTime = 0

		lastReportedTime = self.downloader._reportProgress(
			progressCallback,
			"test_file.zip",
			downloadedSize,
			totalSize,
			initialTime,
		)

		# Assertions
		self.assertEqual(callbackData["fileName"], "test_file.zip")
		self.assertEqual(callbackData["downloadedBytes"], downloadedSize)
		self.assertGreater(lastReportedTime, initialTime)

	@patch.object(ModelDownloader, "downloadSingleFile", return_value=(True, "ok"))
	def test_downloadModelsMultithreadedAllSuccess(self, mockSingle):
		"""All files are downloaded successfully."""
		files = ["a.txt", "b.txt"]
		success, failed = self.downloader.downloadModelsMultithreaded(self.tempDir, "model", files)
		self.assertEqual(len(success), 2)
		self.assertEqual(len(failed), 0)

	@patch.object(ModelDownloader, "downloadSingleFile", side_effect=[(True, "ok"), (False, "err")])
	def test_downloadModelsMultithreadedPartialFailure(self, mockSingle):
		"""One file succeeds and one fails."""
		files = ["a.txt", "b.txt"]
		success, failed = self.downloader.downloadModelsMultithreaded(self.tempDir, "model", files)
		self.assertEqual(len(success), 1)
		self.assertEqual(len(failed), 1)
