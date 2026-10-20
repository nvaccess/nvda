# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024-2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the installer module."""

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

	@staticmethod
	def _fakeProcess(pid: int, exe: str | None) -> MagicMock:
		"""Create a stand-in for a process as returned by :func:`psutil.process_iter` with exe."""
		process = MagicMock(spec=psutil.Process)
		process.pid = pid
		process.info = {"exe": exe}
		return process

	@parameterized.expand(
		(
			("nvda", "C:\\Program Files\\NVDA\\nvda.exe", True),
			("slave", "C:\\Program Files\\NVDA\\nvda_slave.exe", True),
			("differentCase", "c:\\program files\\nvda\\NVDA.EXE", True),
			("x86Dir", "C:\\Program Files (x86)\\NVDA\\nvda.exe", True),
			("otherExe", "C:\\Program Files\\NVDA\\notepad.exe", False),
			("subfolder", "C:\\Program Files\\NVDA\\lib\\nvda.exe", False),
			("otherFolder", "C:\\Temp\\launcher\\nvda.exe", False),
			("unknown", None, False),
		),
	)
	def test_getRunningNVDAProcesses_matchesPath(self, _name: str, imagePath: str | None, expected: bool):
		"""The NVDA executables are found when they run directly from an installation folder.
		Other executables, subfolders and other folders are not found.
		"""
		with patch("installer.psutil.process_iter", return_value=iter([self._fakeProcess(100, imagePath)])):
			found = list(installer._getRunningNVDAProcesses([self._installDir, self._installDirX86]))
		self.assertEqual(bool(found), expected)

	def test_getRunningNVDAProcesses_skipsCurrentProcess(self):
		"""The current process is never found."""
		process = self._fakeProcess(os.getpid(), f"{self._installDir}\\nvda.exe")
		with patch("installer.psutil.process_iter", return_value=iter([process])):
			found = list(installer._getRunningNVDAProcesses([self._installDir]))
		self.assertEqual(found, [])

	def test_waitForRunningNVDAProcesses(self):
		"""A copy that exits during the wait is not returned, a copy that keeps running is."""
		exiting = self._fakeProcess(100, f"{self._installDir}\\nvda.exe")
		exiting.is_running.side_effect = [True, False]
		staying = self._fakeProcess(200, f"{self._installDir}\\nvda.exe")
		staying.is_running.return_value = True
		with (
			patch("installer._getRunningNVDAProcesses", return_value=iter([exiting, staying])),
			patch("installer.time.monotonic", side_effect=[0, 1, 4]),
			patch("installer.time.sleep"),
		):
			remaining = installer._waitForRunningNVDAProcesses([self._installDir], timeout=3)
		self.assertEqual(remaining, [staying])

	def test_waitForRunningNVDAProcesses_noneRunning(self):
		"""Without running copies, nothing is waited for."""
		with (
			patch("installer._getRunningNVDAProcesses", return_value=iter([])),
			patch("installer.time.sleep") as sleepMock,
		):
			self.assertEqual(installer._waitForRunningNVDAProcesses([self._installDir]), [])
		sleepMock.assert_not_called()

	def test_terminateProcesses(self):
		"""Every copy is ended. A copy that can't be ended doesn't stop the others, and isn't waited for."""
		failing = self._fakeProcess(100, f"{self._installDir}\\nvda.exe")
		failing.kill.side_effect = psutil.AccessDenied(100)
		ending = self._fakeProcess(200, f"{self._installDir}\\nvda.exe")
		with patch("installer.psutil.wait_procs", return_value=([ending], [])) as waitProcsMock:
			installer._terminateProcesses([failing, ending])
		ending.kill.assert_called_once_with()
		waitProcsMock.assert_called_once_with([ending], timeout=2)


class Test_doInstallTerminateRunningNVDA(unittest.TestCase):
	"""Tests for asking whether to end running copies of NVDA before installing."""

	def setUp(self):
		self.progressDialogMock = self.enterContext(patch("gui.installerGui.gui.IndeterminateProgressDialog"))
		self.errorMock = self.enterContext(patch("gui.installerGui._showInstallationFailedError"))
		self.enterContext(patch("gui.installerGui._isOtherNVDARunning", return_value=True))
		self.execElevatedMock = self.enterContext(
			patch("gui.installerGui.systemUtils.execElevated", return_value=1),
		)

	@parameterized.expand(((False, "0"), (True, "1")))
	def test_passesTerminateFlagToSlave(self, isOtherNVDARunning: bool, expected: str):
		"""After the user agrees, the elevated slave is told to end the running copies."""
		with (
			patch("gui.installerGui._isOtherNVDARunning", return_value=isOtherNVDARunning),
			patch("gui.installerGui._confirmTerminateRunningNVDA", return_value=True),
		):
			installerGui.doInstall(isUpdate=True)
		self.execElevatedMock.assert_called_once_with(
			installerGui.config.SLAVE_FILENAME,
			["install", "1", "0", expected],
			wait=True,
			handleAlreadyElevated=True,
		)

	def test_noFailsInstallation(self):
		"""Answering No closes the progress dialog, shows the installation failed error and doesn't install."""
		with patch("gui.installerGui._confirmTerminateRunningNVDA", return_value=False):
			installerGui.doInstall(isUpdate=True)
		self.progressDialogMock.return_value.done.assert_called_once_with()
		self.errorMock.assert_called_once_with()
		self.execElevatedMock.assert_not_called()

	@parameterized.expand((("freshInstall", False, False), ("silent", True, True)))
	def test_neverAsks(self, _name: str, isUpdate: bool, silent: bool):
		"""Fresh and silent installations never ask and never end running copies."""
		with patch("gui.installerGui._confirmTerminateRunningNVDA") as confirmMock:
			installerGui.doInstall(isUpdate=isUpdate, silent=silent)
		confirmMock.assert_not_called()
		self.assertEqual(self.execElevatedMock.call_args.args[1][3], "0")


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
