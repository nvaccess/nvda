# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2011-2026 NV Access Limited, Davy Kager, Joseph Lee, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Progress dialogs."""

import threading
from collections.abc import Generator
from contextlib import contextmanager

import config
import tones
import ui
import winUser
import wx
from logHandler import log
from utils._progress import ProgressStep

import gui


class _ProgressDialog(wx.ProgressDialog):
	"""Base class for NVDA's progress dialogs."""

	def __init__(self, parent: wx.Window, title: str, message: str, **kwargs):
		super().__init__(title, message, parent=parent, **kwargs)
		self.CentreOnScreen()
		self.Raise()

	def IsActive(self):
		# 4714: In wxPython 3, ProgressDialog.IsActive always seems to return False.
		return winUser.isDescendantWindow(winUser.getForegroundWindow(), self.Handle)

	def _shouldReportProgress(self) -> bool:
		"""Whether progress should be reported according to the progress bar output settings."""
		pbConf = config.conf["presentation"]["progressBarUpdates"]
		if pbConf["progressBarOutputMode"] == "off":
			return False
		return pbConf["reportBackgroundProgressBars"] or self.IsActive()

	def done(self):
		"""Close the dialog, beeping when progress is reported with beeps."""
		pbConf = config.conf["presentation"]["progressBarUpdates"]
		if pbConf["progressBarOutputMode"] in ("beep", "both") and self._shouldReportProgress():
			tones.beep(1760, 40)
		self.Hide()
		self.Destroy()


class _DeterminateProgressDialog(_ProgressDialog):
	"""A progress dialog that shows how far an operation has progressed, with the elapsed and remaining time.

	Progress can be set from any thread with :meth:`setProgress`.
	While :meth:`receiveRemoteProgress` is active, another process can report progress
	through ``nvdaControllerInternal_progressNotify``.
	"""

	_remoteProgressReceiver: "tuple[_DeterminateProgressDialog, type[ProgressStep]] | None" = None
	"""The dialog that receives progress from another process, with the enum of the steps that process reports."""

	def __init__(self, parent: wx.Window, title: str, message: str):
		"""
		:param parent: The parent window.
		:param title: The title of the dialog.
		:param message: The initial message of the dialog.
		"""
		super().__init__(
			parent,
			title,
			message,
			style=wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME,
		)
		self._latestLock = threading.Lock()
		self._latest = self._shown = (0, message)
		self._timer = gui.NonReEntrantTimer(self._applyLatest)
		self._timer.Start(100)

	def setProgress(self, percentage: int, message: str | None = None) -> None:
		"""Set the progress shown in the dialog.
		This can be called from any thread.

		:param percentage: The overall progress, from 0 to 100.
			The dialog shows at most 99.
		:param message: The new message of the dialog, or ``None`` to keep the current message.
		"""
		percentage = min(max(percentage, 0), 99)
		with self._latestLock:
			self._latest = (percentage, self._latest[1] if message is None else message)

	def setStep(self, step: ProgressStep, percentage: int | None = None) -> None:
		"""Show the current step of the operation.
		This can be called from any thread.

		:param step: The current step. The dialog message shows its display string.
		:param percentage: The overall progress, or ``None`` for the start percentage of the step.
		"""
		self.setProgress(step.startPercentage if percentage is None else percentage, step.displayString)

	def _applyLatest(self) -> None:
		with self._latestLock:
			latest = self._latest
		if latest == self._shown:
			return
		percentage, message = latest
		if message != self._shown[1]:
			if self._shouldReportProgress():
				ui.message(message)
			self.Update(percentage, message)
		else:
			self.Update(percentage)
		self._shown = latest

	@contextmanager
	def receiveRemoteProgress(self, steps: type[ProgressStep]) -> Generator[None]:
		"""Show the progress that another process reports through ``nvdaControllerInternal_progressNotify``.

		:param steps: The enum of the steps the other process reports.
			The dialog message shows the display string of the current step.
		"""
		_DeterminateProgressDialog._remoteProgressReceiver = (self, steps)
		try:
			yield
		finally:
			_DeterminateProgressDialog._remoteProgressReceiver = None

	@classmethod
	def _handleRemoteProgress(cls, step: int, percentage: int) -> None:
		"""Show progress reported by another process.
		This is called from an RPC thread.

		:param step: The value of the step the other process is in.
		:param percentage: The overall progress of the other process.
		"""
		receiver = cls._remoteProgressReceiver
		if receiver is None:
			log.debugWarning(f"No dialog receives remote progress, ignoring {step=}, {percentage=}")
			return
		dialog, steps = receiver
		try:
			stepMember = steps(step)
		except ValueError:
			log.debugWarning(f"Unknown step {step} for {steps.__qualname__}")
			return
		dialog.setStep(stepMember, percentage)

	def done(self):
		self._timer.Stop()
		super().done()
