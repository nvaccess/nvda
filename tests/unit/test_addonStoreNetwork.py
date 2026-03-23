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

	@patch("addonStore.network.log.debugWarning")
	@patch("addonStore.network.pathlib.Path.mkdir")
	@patch("addonStore.network.os.path.exists", return_value=True)
	@patch("addonStore.network.shutil.rmtree", side_effect=OSError("locked by cloud sync"))
	@patch("addonStore.network.NVDAState.shouldWriteToDisk", return_value=True)
	def test_init_rmtreeOSError_doesNotCrashAndLogsWarning(
		self,
		mockShouldWrite: MagicMock,
		mockRmtree: MagicMock,
		mockExists: MagicMock,
		mockMkdir: MagicMock,
		mockLogWarning: MagicMock,
	) -> None:
		"""AddonFileDownloader should not crash and should log a warning when rmtree raises OSError."""
		try:
			AddonFileDownloader()
		except OSError as e:
			self.fail(f"AddonFileDownloader raised OSError when it should have been caught: {e}")
		mockRmtree.assert_called_once_with(WritePaths.addonStoreDownloadDir)
		mockMkdir.assert_called_once()
		mockLogWarning.assert_called_once()

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
		AddonFileDownloader()
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
		AddonFileDownloader()
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
		AddonFileDownloader()
		mockRmtree.assert_not_called()
		mockMkdir.assert_not_called()


class TestAddonFileDownloaderCancelAll(unittest.TestCase):
	"""Tests for AddonFileDownloader.cancelAll error handling of shutil.rmtree."""

	def _createDownloader(self) -> AddonFileDownloader:
		"""Create an AddonFileDownloader with shouldWriteToDisk=False to skip __init__ rmtree."""
		with patch("addonStore.network.NVDAState.shouldWriteToDisk", return_value=False):
			return AddonFileDownloader()

	@patch("addonStore.network.log.debugWarning")
	@patch("addonStore.network.shutil.rmtree", side_effect=OSError("access denied"))
	@patch("addonStore.network.NVDAState.shouldWriteToDisk", return_value=True)
	def test_cancelAll_rmtreeOSError_doesNotCrashAndLogsWarning(
		self,
		mockShouldWrite: MagicMock,
		mockRmtree: MagicMock,
		mockLogWarning: MagicMock,
	) -> None:
		"""cancelAll should not crash and should log a warning when rmtree raises OSError."""
		downloader = self._createDownloader()
		try:
			downloader.cancelAll()
		except OSError as e:
			self.fail(f"cancelAll raised OSError when it should have been caught: {e}")
		mockLogWarning.assert_called_once()

	@patch("addonStore.network.log.debugWarning")
	@patch("addonStore.network.shutil.rmtree", side_effect=FileNotFoundError("no such directory"))
	@patch("addonStore.network.NVDAState.shouldWriteToDisk", return_value=True)
	def test_cancelAll_rmtreeFileNotFound_doesNotCrashAndLogsWarning(
		self,
		mockShouldWrite: MagicMock,
		mockRmtree: MagicMock,
		mockLogWarning: MagicMock,
	) -> None:
		"""cancelAll should not crash and should log a warning when the download directory does not exist."""
		downloader = self._createDownloader()
		try:
			downloader.cancelAll()
		except FileNotFoundError as e:
			self.fail(f"cancelAll raised FileNotFoundError when it should have been caught: {e}")
		mockLogWarning.assert_called_once()

	@patch("addonStore.network.shutil.rmtree")
	@patch("addonStore.network.NVDAState.shouldWriteToDisk", return_value=True)
	def test_cancelAll_rmtreeSucceeds_directoryRemoved(
		self,
		mockShouldWrite: MagicMock,
		mockRmtree: MagicMock,
	) -> None:
		"""cancelAll should call rmtree when completing normally."""
		downloader = self._createDownloader()
		downloader.cancelAll()
		mockRmtree.assert_called_once_with(WritePaths.addonStoreDownloadDir)

	@patch("addonStore.network.shutil.rmtree")
	@patch("addonStore.network.NVDAState.shouldWriteToDisk", return_value=False)
	def test_cancelAll_shouldNotWriteToDisk_rmtreeNotCalled(
		self,
		mockShouldWrite: MagicMock,
		mockRmtree: MagicMock,
	) -> None:
		"""cancelAll should not call rmtree when shouldWriteToDisk is False."""
		downloader = self._createDownloader()
		downloader.cancelAll()
		mockRmtree.assert_not_called()
