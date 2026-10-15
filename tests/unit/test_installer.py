# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024-2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the installer module."""

import contextlib
import os
import pathlib
import tempfile
import unittest
from typing import NamedTuple
from unittest.mock import MagicMock, PropertyMock, patch

import installer
import psutil
from gui import installerGui
from parameterized import parameterized


class Test_BatchDeletion(unittest.TestCase):
	"""Tests for deleting previous installation files safely in a batch for the installation process.
	If any file fails to be deleted, the entire operation should be aborted.
	This ensure installations don't end up in a partially uninstalled state.
	"""

	def setUp(self) -> None:
		self._originalTempDir = tempfile.mkdtemp()
		self._sampleFiles = [
			"file1.txt",
			"file2.txt",
			"file3.txt",
		]
		for file in self._sampleFiles:
			pathlib.Path(self._originalTempDir, file).touch(exist_ok=False)

	def tearDown(self) -> None:
		for file in self._sampleFiles:
			f = pathlib.Path(self._originalTempDir, file)
			if f.exists():
				f.unlink()

	def test_deleteFilesSuccess(self):
		installer._deleteFileGroupOrFail(self._originalTempDir, self._sampleFiles)
		for file in self._sampleFiles:
			self.assertFalse(pathlib.Path(self._originalTempDir, file).exists())

	def test_deleteFilesFailure(self):
		with self.assertRaises(installer.RetriableFailure):  # noqa: SIM117
			with open(pathlib.Path(self._originalTempDir, self._sampleFiles[1]), "r"):
				installer._deleteFileGroupOrFail(self._originalTempDir, self._sampleFiles)

		# Assert files are back where they started
		for file in self._sampleFiles:
			self.assertTrue(pathlib.Path(self._originalTempDir, file).exists())

	def test_deleteNonExistantFilesSuccess(self):
		# Delete all expected files
		for file in self._sampleFiles:
			pathlib.Path(self._originalTempDir, file).unlink()

		installer._deleteFileGroupOrFail(self._originalTempDir, self._sampleFiles)
		for file in self._sampleFiles:
			self.assertFalse(pathlib.Path(self._originalTempDir, file).exists())

	def test_deleteNonExistantFileSuccess(self):
		# Delete 1 file
		pathlib.Path(self._originalTempDir, self._sampleFiles[1]).unlink()

		installer._deleteFileGroupOrFail(self._originalTempDir, self._sampleFiles)
		for file in self._sampleFiles:
			self.assertFalse(pathlib.Path(self._originalTempDir, file).exists())


class Test_terminateRunningNVDA(unittest.TestCase):
	"""Tests for finding and ending copies of NVDA which run from the installation folder."""

	_installDir = "C:\\Program Files\\NVDA"
	_installDirX86 = "C:\\Program Files (x86)\\NVDA"

	@parameterized.expand(
		(
			("nvda", "C:\\Program Files\\NVDA\\nvda.exe", True),
			("noUIAccess", "C:\\Program Files\\NVDA\\nvda_noUIAccess.exe", True),
			("differentCase", "c:\\program files\\nvda\\NVDA.EXE", True),
			("x86Dir", "C:\\Program Files (x86)\\NVDA\\nvda.exe", True),
			("slave", "C:\\Program Files\\NVDA\\nvda_slave.exe", False),
			("subfolder", "C:\\Program Files\\NVDA\\lib\\nvda.exe", False),
			("otherFolder", "C:\\Temp\\launcher\\nvda.exe", False),
			("unknown", None, False),
		),
	)
	def test_isTerminableNVDAImage(self, _name: str, imagePath: str | None, expected: bool):
		"""Only nvda.exe and nvda_noUIAccess.exe directly in an installation folder count, in any letter case."""
		self.assertEqual(
			installer._isTerminableNVDAImage(imagePath, [self._installDir, self._installDirX86]),
			expected,
		)

	@staticmethod
	def _fakeProcess(pid: int, exe: str | None) -> MagicMock:
		"""Create a stand-in for a process as returned by :func:`psutil.process_iter` with exe."""
		process = MagicMock(spec=psutil.Process)
		process.pid = pid
		process.info = {"exe": exe}
		return process

	def test_getRunningNVDAProcesses(self):
		"""Only matching copies are found, never the current process or a process without a known path."""
		processes = [
			self._fakeProcess(100, f"{self._installDir}\\nvda.exe"),
			self._fakeProcess(200, f"{self._installDir}\\NVDA_noUIAccess.exe"),
			self._fakeProcess(300, "C:\\Temp\\launcher\\nvda.exe"),
			self._fakeProcess(400, f"{self._installDir}\\notepad.exe"),
			self._fakeProcess(500, None),
			self._fakeProcess(os.getpid(), f"{self._installDir}\\nvda.exe"),
		]
		with patch("installer.psutil.process_iter", return_value=iter(processes)) as processIterMock:
			found = list(installer._getRunningNVDAProcesses([self._installDir]))
		processIterMock.assert_called_once_with(["exe"])
		self.assertEqual([process.pid for process in found], [100, 200])

	def _terminate(self, processes: list[MagicMock]) -> MagicMock:
		"""Run :func:`installer._terminateNVDAProcesses` with the given processes found.

		:param processes: The processes :func:`installer._getRunningNVDAProcesses` finds.
		:return: The mock standing in for :func:`psutil.wait_procs`.
		"""
		with (
			patch("installer._getRunningNVDAProcesses", return_value=processes),
			patch("installer.psutil.wait_procs", return_value=([], [])) as waitProcsMock,
		):
			installer._terminateNVDAProcesses([self._installDir])
		return waitProcsMock

	def test_terminatesFoundProcesses(self):
		"""Every copy found is ended, and the installer waits for them to exit."""
		processes = [
			self._fakeProcess(100, f"{self._installDir}\\nvda.exe"),
			self._fakeProcess(200, f"{self._installDir}\\nvda_noUIAccess.exe"),
		]
		waitProcsMock = self._terminate(processes)
		for process in processes:
			process.kill.assert_called_once_with()
		waitProcsMock.assert_called_once_with(processes, timeout=2)

	def test_continuesAfterFailedTermination(self):
		"""A copy that can't be ended doesn't stop the others, and isn't waited for."""
		processes = [
			self._fakeProcess(100, f"{self._installDir}\\nvda.exe"),
			self._fakeProcess(200, f"{self._installDir}\\nvda.exe"),
		]
		processes[0].kill.side_effect = psutil.AccessDenied(100)
		waitProcsMock = self._terminate(processes)
		processes[1].kill.assert_called_once_with()
		waitProcsMock.assert_called_once_with([processes[1]], timeout=2)

	def _runInstallUntilDelete(self, **installKwargs: bool) -> MagicMock:
		"""Run :func:`installer.install` up to the first file deletion, recording the calls of interest in order."""
		calls = MagicMock()
		calls._deleteFileGroupOrFail.side_effect = installer.RetriableFailure
		with (
			patch("installer._getInstallDirs", return_value=[self._installDir]),
			patch("installer.time.sleep"),
			patch("installer._terminateNVDAProcesses", calls._terminateNVDAProcesses),
			patch("installer._deleteFileGroupOrFail", calls._deleteFileGroupOrFail),
			self.assertRaises(installer.RetriableFailure),
		):
			installer.install(**installKwargs)
		return calls

	def test_installTerminatesBeforeDeleting(self):
		"""When asked, install ends the running copies before it deletes the NVDA executables."""
		calls = self._runInstallUntilDelete(shouldTerminateRunningNVDA=True)
		self.assertEqual(
			[c[0] for c in calls.mock_calls],
			["_terminateNVDAProcesses", "_deleteFileGroupOrFail"],
		)
		calls._terminateNVDAProcesses.assert_called_once_with([self._installDir])

	def test_installDoesNotTerminateByDefault(self):
		"""By default, install doesn't end any running copies."""
		calls = self._runInstallUntilDelete()
		calls._terminateNVDAProcesses.assert_not_called()
		calls._deleteFileGroupOrFail.assert_called_once()


class Test_doInstallTerminateRunningNVDA(unittest.TestCase):
	"""Tests for asking the user whether to end running copies of NVDA before installing."""

	@staticmethod
	def _patchRunningNVDA(isRunning: bool, confirm: bool):
		"""Patch finding running copies of NVDA and the question whether to end them.

		:return: An exit stack holding the patches,
			and the mock standing in for :func:`installerGui._confirmTerminateRunningNVDA`.
		"""
		stack = contextlib.ExitStack()
		stack.enter_context(
			patch("gui.installerGui.installer._getInstallDirs", return_value=["C:\\Program Files\\NVDA"]),
		)
		stack.enter_context(
			patch(
				"gui.installerGui.installer._getRunningNVDAProcesses",
				return_value=[MagicMock(spec=psutil.Process)] if isRunning else [],
			),
		)
		confirmMock = stack.enter_context(
			patch("gui.installerGui._confirmTerminateRunningNVDA", return_value=confirm),
		)
		return stack, confirmMock

	@parameterized.expand(((False, "0"), (True, "1")))
	def test_doInstall_passesTerminateFlagToSlave(self, shouldTerminateRunningNVDA: bool, expected: str):
		"""doInstall passes whether to end running copies to the elevated slave."""
		with (
			patch("gui.installerGui.gui.IndeterminateProgressDialog"),
			patch("gui.installerGui.systemUtils.execElevated", return_value=1) as execElevatedMock,
			patch("gui.installerGui.gui.messageBox"),
		):
			installerGui.doInstall(shouldTerminateRunningNVDA=shouldTerminateRunningNVDA)
		self.assertEqual(execElevatedMock.call_args.args[1][-1], expected)

	def _onInstall(self, isRunning: bool, confirm: bool) -> tuple[MagicMock, MagicMock, MagicMock]:
		"""Press Install on the install screen.

		:return: The mocks standing in for the install screen,
			:func:`installerGui._confirmTerminateRunningNVDA` and :func:`installerGui.doInstall`.
		"""
		dialog = MagicMock()
		dialog.isUpdate = False
		stack, confirmMock = self._patchRunningNVDA(isRunning, confirm)
		with (
			stack,
			patch("gui.installerGui._warnAndConfirmIfInstallingRemotely", return_value=True),
			patch("gui.installerGui.doInstall") as doInstallMock,
			patch("gui.installerGui.wx.GetApp"),
		):
			installerGui.InstallerDialog.onInstall(dialog, None)
		return dialog, confirmMock, doInstallMock

	def test_onInstall_noRunningCopies_doesNotAsk(self):
		"""Without running copies, the install screen installs without asking."""
		_dialog, confirmMock, doInstallMock = self._onInstall(isRunning=False, confirm=False)
		confirmMock.assert_not_called()
		self.assertFalse(doInstallMock.call_args.kwargs["shouldTerminateRunningNVDA"])

	def test_onInstall_userAgrees_passesTerminateFlag(self):
		"""Answering Yes on the install screen installs and ends the running copies."""
		_dialog, confirmMock, doInstallMock = self._onInstall(isRunning=True, confirm=True)
		confirmMock.assert_called_once()
		self.assertTrue(doInstallMock.call_args.kwargs["shouldTerminateRunningNVDA"])

	def test_onInstall_userDeclines_staysOnInstallScreen(self):
		"""Answering No keeps the install screen open and doesn't install."""
		dialog, _confirmMock, doInstallMock = self._onInstall(isRunning=True, confirm=False)
		doInstallMock.assert_not_called()
		dialog.Hide.assert_not_called()

	def _doSilentInstall(
		self,
		isRunning: bool,
		confirm: bool,
		installSilent: bool = False,
	) -> tuple[MagicMock, MagicMock, MagicMock]:
		"""Run :func:`installerGui.doSilentInstall`, as for an update or a silent installation.

		:return: The mocks standing in for :func:`installerGui._confirmTerminateRunningNVDA`,
			:func:`installerGui.doInstall` and :func:`installerGui._showInstallationFailedError`.
		"""
		stack, confirmMock = self._patchRunningNVDA(isRunning, confirm)
		with (
			stack,
			patch.object(installerGui.globalVars.appArgs, "installSilent", installSilent),
			patch.object(installerGui.globalVars.appArgs, "enableStartOnLogon", None),
			patch(
				"gui.installerGui.installer._comparePreviousInstall",
				return_value=installer.ComparisonState.FRESH_INSTALL,
			),
			patch("gui.installerGui.doInstall") as doInstallMock,
			patch("gui.installerGui._showInstallationFailedError") as errorMock,
		):
			installerGui.doSilentInstall()
		return confirmMock, doInstallMock, errorMock

	def test_doSilentInstall_userAgrees_passesTerminateFlag(self):
		"""Answering Yes during an update installs and ends the running copies."""
		_confirmMock, doInstallMock, errorMock = self._doSilentInstall(isRunning=True, confirm=True)
		self.assertTrue(doInstallMock.call_args.kwargs["shouldTerminateRunningNVDA"])
		errorMock.assert_not_called()

	def test_doSilentInstall_userDeclines_showsError(self):
		"""Answering No during an update shows the installation failed error and doesn't install."""
		_confirmMock, doInstallMock, errorMock = self._doSilentInstall(isRunning=True, confirm=False)
		doInstallMock.assert_not_called()
		errorMock.assert_called_once_with()

	def test_doSilentInstall_installSilent_neverAsksOrTerminates(self):
		"""A silent installation never asks and never ends running copies."""
		confirmMock, doInstallMock, _errorMock = self._doSilentInstall(
			isRunning=True,
			confirm=True,
			installSilent=True,
		)
		confirmMock.assert_not_called()
		self.assertFalse(doInstallMock.call_args.kwargs["shouldTerminateRunningNVDA"])


class _ShouldWarnBeforeUpdateFactors(NamedTuple):
	remoteEnabled: bool
	isConnectedAsFollower: bool
	isUserAnAdmin: bool
	expectedReturn: bool = False


class testFollowerWarning(unittest.TestCase):
	@parameterized.expand(
		(
			_ShouldWarnBeforeUpdateFactors(
				remoteEnabled=False,
				isConnectedAsFollower=False,
				isUserAnAdmin=False,
			),
			_ShouldWarnBeforeUpdateFactors(
				remoteEnabled=False,
				isConnectedAsFollower=False,
				isUserAnAdmin=True,
			),
			_ShouldWarnBeforeUpdateFactors(
				remoteEnabled=False,
				isConnectedAsFollower=True,
				isUserAnAdmin=False,
			),
			_ShouldWarnBeforeUpdateFactors(
				remoteEnabled=False,
				isConnectedAsFollower=True,
				isUserAnAdmin=True,
			),
			_ShouldWarnBeforeUpdateFactors(
				remoteEnabled=True,
				isConnectedAsFollower=False,
				isUserAnAdmin=False,
			),
			_ShouldWarnBeforeUpdateFactors(
				remoteEnabled=True,
				isConnectedAsFollower=False,
				isUserAnAdmin=True,
			),
			_ShouldWarnBeforeUpdateFactors(
				remoteEnabled=True,
				isConnectedAsFollower=True,
				isUserAnAdmin=False,
				expectedReturn=True,
			),
			_ShouldWarnBeforeUpdateFactors(
				remoteEnabled=True,
				isConnectedAsFollower=True,
				isUserAnAdmin=True,
			),
		),
	)
	def test_shouldWarnBeforeUpdate(
		self,
		remoteEnabled: bool,
		isConnectedAsFollower: bool,
		isUserAnAdmin: bool,
		expectedReturn: bool,
	):
		with (
			patch("winBindings.shell32.IsUserAnAdmin", return_value=isUserAnAdmin),
			patch(
				"_remoteClient.client.RemoteClient",
				isConnectedAsFollower=isConnectedAsFollower,
			) as patchedRemoteClient,
			patch.dict(
				"_remoteClient.__dict__",
				_remoteClient=patchedRemoteClient if remoteEnabled else None,
			),
		):
			self.assertEqual(installerGui._shouldWarnBeforeUpdate(), expectedReturn)


class Test_comparePreviousInstall(unittest.TestCase):
	def test_freshInstall_whenNoInstallDirsExist(self):
		with (
			patch.object(
				installer.WritePaths.__class__,
				"installDir",
				new_callable=PropertyMock,
				return_value="C:\\Program Files\\NVDA",
			),
			patch.object(
				installer.WritePaths.__class__,
				"_installDirX86",
				new_callable=PropertyMock,
				return_value="C:\\Program Files (x86)\\NVDA",
			),
			patch("installer.os.path.isdir", return_value=False),
			patch("installer.fileUtils.getFileVersionInfo") as getVersionMock,
		):
			result = installer._comparePreviousInstall()
			self.assertEqual(result, installer.ComparisonState.FRESH_INSTALL)
			getVersionMock.assert_not_called()

	def test_unknown_whenOldVersionLookupFails_inInstallDir(self):
		installDir = "C:\\Program Files\\NVDA"
		oldSlavePath = str(pathlib.Path(installDir) / "nvda_slave.exe")

		def _isdir(path: str) -> bool:
			return path == installDir

		def _getVersion(path: str, field: str):
			if path == oldSlavePath:
				raise OSError("locked")
			self.fail("Current version lookup should not occur when old version lookup fails.")

		with (
			patch.object(
				installer.WritePaths.__class__,
				"installDir",
				new_callable=PropertyMock,
				return_value=installDir,
			),
			patch.object(
				installer.WritePaths.__class__,
				"_installDirX86",
				new_callable=PropertyMock,
				return_value="C:\\Program Files (x86)\\NVDA",
			),
			patch("installer.os.path.isdir", side_effect=_isdir),
			patch(
				"installer.fileUtils.getFileVersionInfo",
				side_effect=_getVersion,
			),
		):
			self.assertEqual(installer._comparePreviousInstall(), installer.ComparisonState.UNKNOWN)

	def test_unknown_whenOldVersionLookupFails_inX86InstallDir(self):
		installDir = "C:\\Program Files\\NVDA"
		installDirX86 = "C:\\Program Files (x86)\\NVDA"
		oldSlavePathX86 = str(pathlib.Path(installDirX86) / "nvda_slave.exe")

		def _isdir(path: str) -> bool:
			return path == installDirX86

		def _getVersion(path: str, field: str):
			if path == oldSlavePathX86:
				raise RuntimeError("bad version metadata")
			self.fail("Current version lookup should not occur when old version lookup fails.")

		with (
			patch.object(
				installer.WritePaths.__class__,
				"installDir",
				new_callable=PropertyMock,
				return_value=installDir,
			),
			patch.object(
				installer.WritePaths.__class__,
				"_installDirX86",
				new_callable=PropertyMock,
				return_value=installDirX86,
			),
			patch("installer.os.path.isdir", side_effect=_isdir),
			patch(
				"installer.fileUtils.getFileVersionInfo",
				side_effect=_getVersion,
			),
		):
			self.assertEqual(installer._comparePreviousInstall(), installer.ComparisonState.UNKNOWN)

	def test_unknown_whenCurrentVersionLookupFails(self):
		installDir = "C:\\Program Files\\NVDA"
		oldSlavePath = str(pathlib.Path(installDir) / "nvda_slave.exe")

		def _isdir(path: str) -> bool:
			return path == installDir

		def _getVersion(path: str, field: str):
			if path == oldSlavePath:
				return {"FileVersion": "2025.1.0"}
			if path == "nvda_slave.exe":
				raise OSError("missing current executable version")
			self.fail(f"Unexpected path: {path}")

		with (
			patch.object(
				installer.WritePaths.__class__,
				"installDir",
				new_callable=PropertyMock,
				return_value=installDir,
			),
			patch.object(
				installer.WritePaths.__class__,
				"_installDirX86",
				new_callable=PropertyMock,
				return_value=None,
			),
			patch("installer.os.path.isdir", side_effect=_isdir),
			patch(
				"installer.fileUtils.getFileVersionInfo",
				side_effect=_getVersion,
			),
		):
			self.assertEqual(installer._comparePreviousInstall(), installer.ComparisonState.UNKNOWN)

	def test_unknown_whenVersionParsingFails(self):
		installDir = "C:\\Program Files\\NVDA"
		oldSlavePath = str(pathlib.Path(installDir) / "nvda_slave.exe")

		def _isdir(path: str) -> bool:
			return path == installDir

		def _getVersion(path: str, field: str):
			if path == oldSlavePath:
				return {"FileVersion": None}
			if path == "nvda_slave.exe":
				return {"FileVersion": "2025.1.0"}
			self.fail(f"Unexpected path: {path}")

		with (
			patch.object(
				installer.WritePaths.__class__,
				"installDir",
				new_callable=PropertyMock,
				return_value=installDir,
			),
			patch.object(
				installer.WritePaths.__class__,
				"_installDirX86",
				new_callable=PropertyMock,
				return_value=None,
			),
			patch("installer.os.path.isdir", side_effect=_isdir),
			patch(
				"installer.fileUtils.getFileVersionInfo",
				side_effect=_getVersion,
			),
		):
			self.assertEqual(installer._comparePreviousInstall(), installer.ComparisonState.UNKNOWN)

	def test_unknown_whenPreviousVersionContainsPrereleaseTag(self):
		installDir = "C:\\Program Files\\NVDA"
		oldSlavePath = str(pathlib.Path(installDir) / "nvda_slave.exe")

		def _isdir(path: str) -> bool:
			return path == installDir

		def _getVersion(path: str, field: str):
			if path == oldSlavePath:
				return {"FileVersion": "2026.1.beta1"}
			if path == "nvda_slave.exe":
				return {"FileVersion": "2025.1.0"}
			self.fail(f"Unexpected path: {path}")

		with (
			patch.object(
				installer.WritePaths.__class__,
				"installDir",
				new_callable=PropertyMock,
				return_value=installDir,
			),
			patch.object(
				installer.WritePaths.__class__,
				"_installDirX86",
				new_callable=PropertyMock,
				return_value=None,
			),
			patch("installer.os.path.isdir", side_effect=_isdir),
			patch(
				"installer.fileUtils.getFileVersionInfo",
				side_effect=_getVersion,
			),
		):
			self.assertEqual(installer._comparePreviousInstall(), installer.ComparisonState.UNKNOWN)

	def test_downgrade_whenPreviousInstallIsNewer(self):
		installDir = "C:\\Program Files\\NVDA"
		oldSlavePath = str(pathlib.Path(installDir) / "nvda_slave.exe")

		def _isdir(path: str) -> bool:
			return path == installDir

		def _getVersion(path: str, field: str):
			if path == oldSlavePath:
				return {"FileVersion": "2026.1.0"}
			if path == "nvda_slave.exe":
				return {"FileVersion": "2025.1.0"}
			self.fail(f"Unexpected path: {path}")

		with (
			patch.object(
				installer.WritePaths.__class__,
				"installDir",
				new_callable=PropertyMock,
				return_value=installDir,
			),
			patch.object(
				installer.WritePaths.__class__,
				"_installDirX86",
				new_callable=PropertyMock,
				return_value=None,
			),
			patch("installer.os.path.isdir", side_effect=_isdir),
			patch(
				"installer.fileUtils.getFileVersionInfo",
				side_effect=_getVersion,
			),
		):
			self.assertEqual(installer._comparePreviousInstall(), installer.ComparisonState.DOWNGRADE)

	def test_upgrade_whenPreviousInstallIsOlder(self):
		installDir = "C:\\Program Files\\NVDA"
		oldSlavePath = str(pathlib.Path(installDir) / "nvda_slave.exe")

		def _isdir(path: str) -> bool:
			return path == installDir

		def _getVersion(path: str, field: str):
			if path == oldSlavePath:
				return {"FileVersion": "2024.4.0"}
			if path == "nvda_slave.exe":
				return {"FileVersion": "2025.1.0"}
			self.fail(f"Unexpected path: {path}")

		with (
			patch.object(
				installer.WritePaths.__class__,
				"installDir",
				new_callable=PropertyMock,
				return_value=installDir,
			),
			patch.object(
				installer.WritePaths.__class__,
				"_installDirX86",
				new_callable=PropertyMock,
				return_value=None,
			),
			patch("installer.os.path.isdir", side_effect=_isdir),
			patch(
				"installer.fileUtils.getFileVersionInfo",
				side_effect=_getVersion,
			),
		):
			self.assertEqual(installer._comparePreviousInstall(), installer.ComparisonState.UPGRADE)

	def test_reinstall_whenVersionsAreEqual(self):
		installDir = "C:\\Program Files\\NVDA"
		oldSlavePath = str(pathlib.Path(installDir) / "nvda_slave.exe")

		def _isdir(path: str) -> bool:
			return path == installDir

		def _getVersion(path: str, field: str):
			if path == oldSlavePath:
				return {"FileVersion": "2025.1.0"}
			if path == "nvda_slave.exe":
				return {"FileVersion": "2025.1.0"}
			self.fail(f"Unexpected path: {path}")

		with (
			patch.object(
				installer.WritePaths.__class__,
				"installDir",
				new_callable=PropertyMock,
				return_value=installDir,
			),
			patch.object(
				installer.WritePaths.__class__,
				"_installDirX86",
				new_callable=PropertyMock,
				return_value=None,
			),
			patch("installer.os.path.isdir", side_effect=_isdir),
			patch(
				"installer.fileUtils.getFileVersionInfo",
				side_effect=_getVersion,
			),
		):
			self.assertEqual(installer._comparePreviousInstall(), installer.ComparisonState.REINSTALL)

	def test_prefersPrimaryInstallDir_whenBothPrimaryAndX86Exist(self):
		installDir = "C:\\Program Files\\NVDA"
		installDirX86 = "C:\\Program Files (x86)\\NVDA"
		oldSlavePath = str(pathlib.Path(installDir) / "nvda_slave.exe")
		oldSlavePathX86 = str(pathlib.Path(installDirX86) / "nvda_slave.exe")

		def _isdir(path: str) -> bool:
			return path in (installDir, installDirX86)

		def _getVersion(path: str, field: str):
			if path == oldSlavePath:
				return {"FileVersion": "2024.4.0"}
			if path == oldSlavePathX86:
				self.fail("x86 install path should not be used when primary install dir exists.")
			if path == "nvda_slave.exe":
				return {"FileVersion": "2025.1.0"}
			self.fail(f"Unexpected path: {path}")

		with (
			patch.object(
				installer.WritePaths.__class__,
				"installDir",
				new_callable=PropertyMock,
				return_value=installDir,
			),
			patch.object(
				installer.WritePaths.__class__,
				"_installDirX86",
				new_callable=PropertyMock,
				return_value=installDirX86,
			),
			patch("installer.os.path.isdir", side_effect=_isdir),
			patch(
				"installer.fileUtils.getFileVersionInfo",
				side_effect=_getVersion,
			),
		):
			self.assertEqual(installer._comparePreviousInstall(), installer.ComparisonState.UPGRADE)
