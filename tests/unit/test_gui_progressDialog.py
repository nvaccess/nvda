# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for :class:`gui.progressDialog._DeterminateProgressDialog`."""

import threading
import types
import unittest
from typing import Self
from unittest.mock import Mock, patch

from gui.progressDialog import _DeterminateProgressDialog
from utils._progress import ProgressStep


class _Steps(ProgressStep):
	FIRST = 1
	SECOND = 2

	@property
	def _displayStringLabels(self) -> dict[Self, str]:
		return {_Steps.FIRST: "First step", _Steps.SECOND: "Second step"}

	@property
	def _startPercentages(self) -> dict[Self, int]:
		return {_Steps.FIRST: 0, _Steps.SECOND: 50}


class Test_remoteProgress(unittest.TestCase):
	def tearDown(self) -> None:
		_DeterminateProgressDialog._remoteProgressReceiver = None

	def test_receiveRemoteProgress_registersDialogOnlyWhileActive(self):
		dialog = Mock()
		with _DeterminateProgressDialog.receiveRemoteProgress(dialog, _Steps):
			self.assertEqual(_DeterminateProgressDialog._remoteProgressReceiver, (dialog, _Steps))
		self.assertIsNone(_DeterminateProgressDialog._remoteProgressReceiver)

	def test_receiveRemoteProgress_unregistersDialogOnError(self):
		dialog = Mock()
		with (
			self.assertRaises(RuntimeError),
			_DeterminateProgressDialog.receiveRemoteProgress(dialog, _Steps),
		):
			raise RuntimeError
		self.assertIsNone(_DeterminateProgressDialog._remoteProgressReceiver)

	def test_knownStep_setsStep(self):
		dialog = Mock()
		_DeterminateProgressDialog._remoteProgressReceiver = (dialog, _Steps)
		_DeterminateProgressDialog._handleRemoteProgress(1, 42)
		dialog.setStep.assert_called_once_with(_Steps.FIRST, 42)

	def test_unknownStep_isIgnored(self):
		dialog = Mock()
		_DeterminateProgressDialog._remoteProgressReceiver = (dialog, _Steps)
		_DeterminateProgressDialog._handleRemoteProgress(3, 42)
		dialog.setStep.assert_not_called()

	def test_withoutReceiver_isIgnored(self):
		_DeterminateProgressDialog._handleRemoteProgress(1, 42)


class Test_setProgress(unittest.TestCase):
	def setUp(self) -> None:
		self._dialog = types.SimpleNamespace(_latestLock=threading.Lock(), _latest=(0, "Initial"))

	def _setProgress(self, percentage: int, message: str | None = None) -> None:
		_DeterminateProgressDialog.setProgress(self._dialog, percentage, message)

	def test_percentage_isClampedBelowHundred(self):
		self._setProgress(150)
		self.assertEqual(self._dialog._latest, (99, "Initial"))
		self._setProgress(-5)
		self.assertEqual(self._dialog._latest, (0, "Initial"))

	def test_message_isKeptWhenNoNewMessage(self):
		self._setProgress(10, "Copying")
		self._setProgress(11)
		self.assertEqual(self._dialog._latest, (11, "Copying"))


class Test_setStep(unittest.TestCase):
	def test_withoutPercentage_setsStartPercentage(self):
		dialog = Mock()
		_DeterminateProgressDialog.setStep(dialog, _Steps.SECOND)
		dialog.setProgress.assert_called_once_with(50, "Second step")

	def test_withPercentage_setsPercentage(self):
		dialog = Mock()
		_DeterminateProgressDialog.setStep(dialog, _Steps.FIRST, 42)
		dialog.setProgress.assert_called_once_with(42, "First step")

	def test_withZeroPercentage_setsZero(self):
		dialog = Mock()
		_DeterminateProgressDialog.setStep(dialog, _Steps.SECOND, 0)
		dialog.setProgress.assert_called_once_with(0, "Second step")


class Test_applyLatest(unittest.TestCase):
	def setUp(self) -> None:
		self._dialog = types.SimpleNamespace(
			_latestLock=threading.Lock(),
			_latest=(0, "Initial"),
			_shown=(0, "Initial"),
			_shouldReportProgress=Mock(return_value=True),
			Update=Mock(),
		)

	def _applyLatest(self, latest: tuple[int, str]) -> None:
		self._dialog._latest = latest
		with patch("gui.progressDialog.ui.message") as self._uiMessage:
			_DeterminateProgressDialog._applyLatest(self._dialog)

	def test_unchanged_updatesNothing(self):
		self._applyLatest((0, "Initial"))
		self._dialog.Update.assert_not_called()
		self._uiMessage.assert_not_called()

	def test_newPercentage_updatesOnlyPercentage(self):
		self._applyLatest((10, "Initial"))
		self._dialog.Update.assert_called_once_with(10)
		self._uiMessage.assert_not_called()
		self.assertEqual(self._dialog._shown, (10, "Initial"))

	def test_newMessage_isShownAndReported(self):
		self._applyLatest((10, "Copying"))
		self._dialog.Update.assert_called_once_with(10, "Copying")
		self._uiMessage.assert_called_once_with("Copying")

	def test_newMessage_isNotReportedWhenProgressIsNotReported(self):
		self._dialog._shouldReportProgress.return_value = False
		self._applyLatest((10, "Copying"))
		self._dialog.Update.assert_called_once_with(10, "Copying")
		self._uiMessage.assert_not_called()
