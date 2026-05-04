# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Christopher Pross, Cary-rowen
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the addonStore.network module."""

from concurrent.futures import Future
from typing import Any
import unittest
from unittest.mock import patch, MagicMock

from addonStore.network import AddonFileDownloader
from NVDAState import WritePaths


def _makeAddonData() -> MagicMock:
	addonData = MagicMock()
	addonData.model.addonId = "testAddon"
	addonData.model.tempDownloadPath = r"C:\temp\testAddon.download"
	return addonData


class _FakeExecutor:
	def __init__(self) -> None:
		self.submitCalls: list[tuple[Any, tuple[Any, ...], dict[str, Any], Future[Any]]] = []
		self.shutdownCalls: list[bool] = []

	def submit(self, fn: Any, *args: Any, **kwargs: Any) -> Future[Any]:
		future: Future[Any] = Future()
		self.submitCalls.append((fn, args, kwargs, future))
		return future

	def shutdown(self, wait: bool = False) -> None:
		self.shutdownCalls.append(wait)


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

	@patch("addonStore.network.NVDAState.shouldWriteToDisk", return_value=False)
	def test_cancelAll_whenExecutorAlreadyNone_doesNotCrash(
		self,
		mockShouldWrite: MagicMock,
	) -> None:
		"""cancelAll should tolerate being called after a previous cancelAll shut down the executor."""
		self._createDownloader()
		self.downloader.cancelAll()
		self.downloader.cancelAll()
		self.assertIsNone(self.downloader._executor)

	@patch("addonStore.network.ThreadPoolExecutor")
	@patch("addonStore.network.NVDAState.shouldWriteToDisk", return_value=False)
	def test_downloadAfterCancelAll_recreatesExecutor(
		self,
		mockShouldWrite: MagicMock,
		mockThreadPoolExecutor: MagicMock,
	) -> None:
		"""download should recreate the executor after cancelAll shuts it down."""
		firstExecutor = _FakeExecutor()
		secondExecutor = _FakeExecutor()
		mockThreadPoolExecutor.side_effect = [firstExecutor, secondExecutor]
		self.downloader = AddonFileDownloader()

		self.downloader.cancelAll()
		self.assertIsNone(self.downloader._executor)
		self.assertEqual(firstExecutor.shutdownCalls, [False])

		addonData = _makeAddonData()
		self.downloader.download(addonData, MagicMock(), MagicMock())

		self.assertIs(self.downloader._executor, secondExecutor)
		self.assertEqual(len(secondExecutor.submitCalls), 1)
		_, submitArgs, submitKwargs, future = secondExecutor.submitCalls[0]
		tempDownloadPath = self.downloader._activeDownloadPaths[addonData]
		self.assertEqual(submitArgs, (addonData, tempDownloadPath))
		self.assertEqual(submitKwargs, {})
		self.assertIs(self.downloader._pending[future].addonData, addonData)
		self.assertEqual(self.downloader._pending[future].tempDownloadPath, tempDownloadPath)
		self.assertEqual(self.downloader.progress[addonData], 0)

	@patch("addonStore.network.ThreadPoolExecutor")
	@patch("addonStore.network.NVDAState.shouldWriteToDisk", return_value=False)
	def test_downloadAfterCancelAll_runningAttemptDoesNotReplaceNewAttemptState(
		self,
		mockShouldWrite: MagicMock,
		mockThreadPoolExecutor: MagicMock,
	) -> None:
		"""A cancelled retry should keep the new attempt active until it finishes."""
		firstExecutor = _FakeExecutor()
		secondExecutor = _FakeExecutor()
		mockThreadPoolExecutor.side_effect = [firstExecutor, secondExecutor]
		self.downloader = AddonFileDownloader()

		addonData = _makeAddonData()
		onCompleteFirst = MagicMock()
		onCompleteSecond = MagicMock()

		self.downloader.download(addonData, onCompleteFirst, MagicMock())
		_, _, _, firstFuture = firstExecutor.submitCalls[0]
		firstFuture.set_running_or_notify_cancel()
		firstTempDownloadPath = self.downloader._activeDownloadPaths[addonData]

		self.downloader.cancelAll()
		self.downloader.download(addonData, onCompleteSecond, MagicMock())
		_, _, _, secondFuture = secondExecutor.submitCalls[0]
		secondTempDownloadPath = self.downloader._activeDownloadPaths[addonData]

		self.assertNotEqual(
			firstTempDownloadPath,
			secondTempDownloadPath,
		)

		firstFuture.set_result(None)

		self.assertEqual(self.downloader._activeDownloadPaths[addonData], secondTempDownloadPath)
		self.assertEqual(self.downloader.progress[addonData], 0)
		self.assertNotIn(firstFuture, self.downloader._pending)
		self.assertIn(secondFuture, self.downloader._pending)
		onCompleteFirst.assert_not_called()

	@patch("addonStore.network.ThreadPoolExecutor")
	@patch("addonStore.network.NVDAState.shouldWriteToDisk", return_value=False)
	def test_download_progressRemovalCancelsActiveAttempt(
		self,
		mockShouldWrite: MagicMock,
		mockThreadPoolExecutor: MagicMock,
	) -> None:
		"""Removing progress should remain a cancellation signal for an active download."""
		executor = _FakeExecutor()
		mockThreadPoolExecutor.return_value = executor
		self.downloader = AddonFileDownloader()
		addonData = _makeAddonData()
		onComplete = MagicMock()

		self.downloader.download(addonData, onComplete, MagicMock())
		_, _, _, future = executor.submitCalls[0]
		self.downloader.progress.pop(addonData, None)

		future.set_result(None)

		self.assertNotIn(addonData, self.downloader._activeDownloadPaths)
		self.assertNotIn(future, self.downloader._pending)
		onComplete.assert_not_called()

	@patch("addonStore.network.pathlib.Path.mkdir")
	@patch("addonStore.network.os.path.exists", side_effect=[False, True, False])
	@patch("addonStore.network.shutil.rmtree")
	@patch("addonStore.network.ThreadPoolExecutor")
	@patch("addonStore.network.NVDAState.shouldWriteToDisk", return_value=True)
	def test_downloadAfterCancelAll_recreatesDownloadDirectory(
		self,
		mockShouldWrite: MagicMock,
		mockThreadPoolExecutor: MagicMock,
		mockRmtree: MagicMock,
		mockExists: MagicMock,
		mockMkdir: MagicMock,
	) -> None:
		"""download should recreate the download directory after cancelAll removes it."""
		mockThreadPoolExecutor.side_effect = [_FakeExecutor(), _FakeExecutor()]
		self.downloader = AddonFileDownloader()

		self.downloader.cancelAll()
		self.downloader.download(_makeAddonData(), MagicMock(), MagicMock())

		self.assertEqual(mockMkdir.call_count, 2)
		mockRmtree.assert_called_once_with(WritePaths.addonStoreDownloadDir)
