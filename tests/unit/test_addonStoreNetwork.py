# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Christopher Pross
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the addonStore.network module."""

import unittest
from unittest.mock import patch, MagicMock

from addonStore.network import AddonFileDownloader
from NVDAState import WritePaths


class TestAddonFileDownloaderInit(unittest.TestCase):
	"""Tests for AddonFileDownloader.__init__ error handling of shutil.rmtree."""

	def setUp(self):
		self.downloader = None

	def tearDown(self):
		if self.downloader is not None and self.downloader._executor is not None:
			with patch("addonStore.network.NVDAState.shouldWriteToDisk", return_value=False):
				self.downloader.cancelAll()

	@patch("addonStore.network.log.error")
	@patch("addonStore.network.pathlib.Path.mkdir")
	@patch("addonStore.network.os.path.exists", return_value=True)
	@patch("addonStore.network.shutil.rmtree", side_effect=OSError("locked by cloud sync"))
	@patch("addonStore.network.NVDAState.shouldWriteToDisk", return_value=True)
	def test_init_rmtreeOSError_doesNotCrashAndLogsError(
		self,
		mockShouldWrite: MagicMock,
		mockRmtree: MagicMock,
		mockExists: MagicMock,
		mockMkdir: MagicMock,
		mockLogError: MagicMock,
	) -> None:
		"""AddonFileDownloader should not crash and should log an error when rmtree raises OSError."""
		try:
			self.downloader = AddonFileDownloader()
		except OSError as e:
			self.fail(f"AddonFileDownloader raised OSError when it should have been caught: {e}")
		mockRmtree.assert_called_once_with(WritePaths.addonStoreDownloadDir)
		mockMkdir.assert_called_once()
		mockLogError.assert_called_once()

	@patch("addonStore.network.pathlib.Path.mkdir")
	@patch("addonStore.network.os.path.exists", return_value=True)
	@patch("addonStore.network.shutil.rmtree")
	@patch("addonStore.network.NVDAState.shouldWriteToDisk", return_value=True)
	def test_init_rmtreeSucceeds_downloadsDirectoryCleanedAndRecreated(
		self,
		mockShouldWrite: MagicMock,
		mockRmtree: MagicMock,
		mockExists: MagicMock,
		mockMkdir: MagicMock,
	) -> None:
		"""AddonFileDownloader should call rmtree and mkdir when shouldWriteToDisk is True."""
		self.downloader = AddonFileDownloader()
		mockRmtree.assert_called_once_with(WritePaths.addonStoreDownloadDir)
		mockMkdir.assert_called_once()

	@patch("addonStore.network.pathlib.Path.mkdir")
	@patch("addonStore.network.os.path.exists", return_value=False)
	@patch("addonStore.network.shutil.rmtree")
	@patch("addonStore.network.NVDAState.shouldWriteToDisk", return_value=True)
	def test_init_downloadDirNotExists_rmtreeNotCalledButMkdirCalled(
		self,
		mockShouldWrite: MagicMock,
		mockRmtree: MagicMock,
		mockExists: MagicMock,
		mockMkdir: MagicMock,
	) -> None:
		"""AddonFileDownloader should skip rmtree but still call mkdir when download dir does not exist."""
		self.downloader = AddonFileDownloader()
		mockRmtree.assert_not_called()
		mockMkdir.assert_called_once()

	@patch("addonStore.network.pathlib.Path.mkdir")
	@patch("addonStore.network.shutil.rmtree")
	@patch("addonStore.network.NVDAState.shouldWriteToDisk", return_value=False)
	def test_init_shouldNotWriteToDisk_rmtreeNotCalled(
		self,
		mockShouldWrite: MagicMock,
		mockRmtree: MagicMock,
		mockMkdir: MagicMock,
	) -> None:
		"""AddonFileDownloader should not call rmtree or mkdir when shouldWriteToDisk is False."""
		self.downloader = AddonFileDownloader()
		mockRmtree.assert_not_called()
		mockMkdir.assert_not_called()


class TestAddonFileDownloaderCancelAll(unittest.TestCase):
	"""Tests for AddonFileDownloader.cancelAll error handling of shutil.rmtree."""

	def setUp(self):
		self.downloader = None

	def tearDown(self):
		if self.downloader is not None and self.downloader._executor is not None:
			with patch("addonStore.network.NVDAState.shouldWriteToDisk", return_value=False):
				self.downloader.cancelAll()

	def _createDownloader(self) -> None:
		"""Create an AddonFileDownloader and assign to self.downloader.

		shouldWriteToDisk is patched to False to skip __init__ rmtree.
		"""
		with patch("addonStore.network.NVDAState.shouldWriteToDisk", return_value=False):
			self.downloader = AddonFileDownloader()

	@patch("addonStore.network.log.error")
	@patch("addonStore.network.os.path.exists", return_value=True)
	@patch("addonStore.network.shutil.rmtree", side_effect=OSError("access denied"))
	@patch("addonStore.network.NVDAState.shouldWriteToDisk", return_value=True)
	def test_cancelAll_rmtreeOSError_doesNotCrashAndLogsError(
		self,
		mockShouldWrite: MagicMock,
		mockRmtree: MagicMock,
		mockExists: MagicMock,
		mockLogError: MagicMock,
	) -> None:
		"""cancelAll should not crash and should log an error when rmtree raises OSError."""
		self._createDownloader()
		try:
			self.downloader.cancelAll()
		except OSError as e:
			self.fail(f"cancelAll raised OSError when it should have been caught: {e}")
		mockLogError.assert_called_once()

	@patch("addonStore.network.shutil.rmtree")
	@patch("addonStore.network.os.path.exists", return_value=False)
	@patch("addonStore.network.NVDAState.shouldWriteToDisk", return_value=True)
	def test_cancelAll_dirNotExists_rmtreeNotCalled(
		self,
		mockShouldWrite: MagicMock,
		mockExists: MagicMock,
		mockRmtree: MagicMock,
	) -> None:
		"""cancelAll should not call rmtree when the download directory does not exist."""
		self._createDownloader()
		self.downloader.cancelAll()
		mockRmtree.assert_not_called()

	@patch("addonStore.network.os.path.exists", return_value=True)
	@patch("addonStore.network.shutil.rmtree")
	@patch("addonStore.network.NVDAState.shouldWriteToDisk", return_value=True)
	def test_cancelAll_rmtreeSucceeds_directoryRemoved(
		self,
		mockShouldWrite: MagicMock,
		mockRmtree: MagicMock,
		mockExists: MagicMock,
	) -> None:
		"""cancelAll should call rmtree when completing normally."""
		self._createDownloader()
		self.downloader.cancelAll()
		mockRmtree.assert_called_once_with(WritePaths.addonStoreDownloadDir)

	@patch("addonStore.network.shutil.rmtree")
	@patch("addonStore.network.NVDAState.shouldWriteToDisk", return_value=False)
	def test_cancelAll_shouldNotWriteToDisk_rmtreeNotCalled(
		self,
		mockShouldWrite: MagicMock,
		mockRmtree: MagicMock,
	) -> None:
		"""cancelAll should not call rmtree when shouldWriteToDisk is False."""
		self._createDownloader()
		self.downloader.cancelAll()
		mockRmtree.assert_not_called()
