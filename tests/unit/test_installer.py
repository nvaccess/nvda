# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024-2025 NV Access Limited

"""Unit tests for the installer module."""

import pathlib
import tempfile
from typing import NamedTuple
import unittest
from unittest.mock import patch, PropertyMock

from parameterized import parameterized

from gui import installerGui
from gui.message import DisplayableError
import installer


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
		with self.assertRaises(installer.RetriableFailure):
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
		with patch("winBindings.shell32.IsUserAnAdmin", return_value=isUserAnAdmin):
			with patch(
				"_remoteClient.client.RemoteClient",
				isConnectedAsFollower=isConnectedAsFollower,
			) as patchedRemoteClient:
				with patch.dict(
					"_remoteClient.__dict__",
					_remoteClient=patchedRemoteClient if remoteEnabled else None,
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


class Test_CreatePortableDirectoryNormalization(unittest.TestCase):
	"""Tests for path handling in onCreatePortable (#20159)."""

	def _validate(self, path: str) -> tuple[str | None, str | None]:
		"""Call _validatePortableDirectory with the given path.
		Returns (result, error_message).
		"""
		import ntpath

		with (
			patch("gui.installerGui.os.path.isabs", side_effect=ntpath.isabs),
			patch("gui.installerGui.os.path.splitroot", side_effect=ntpath.splitroot),
			patch("gui.installerGui.os.path.expandvars", side_effect=lambda p: p),
			patch("gui.installerGui.os.path.abspath", return_value="C:\\NVDA"),
		):
			try:
				result = installerGui._validatePortableDirectory(path)
			except DisplayableError as e:
				result = None
				errorMsg = e.displayMessage
			else:
				errorMsg = None
		return result, errorMsg

	def test_emptyPath_showsError(self):
		result, errorMsg = self._validate("")
		self.assertIsNone(result)
		self.assertIn("Please specify a directory", errorMsg)

	def test_bareDriveLetter_showsSpecificError(self):
		result, errorMsg = self._validate("c:")
		self.assertIsNone(result)
		self.assertIn("c:\\", errorMsg)

	def test_driveWithRelativePath_showsBareDriveError(self):
		result, errorMsg = self._validate("c:foo")
		self.assertIsNone(result)
		self.assertIn("c:\\", errorMsg)

	def test_relativePath_showsError(self):
		result, errorMsg = self._validate("foo")
		self.assertIsNone(result)
		errorText = _(
			"Please specify the absolute path where the portable copy should be created. "
			"It must start with a drive letter (e.g. C:). "
			"It may include system variables (e.g. %temp%, %homepath%) as placeholders for parts of the path.\n"
			"Current path: {path}. ",
		).format(path="foo")
		self.assertEqual(errorMsg, errorText)

	def test_absolutePath_isAccepted(self):
		result, errorMsg = self._validate("c:\\")
		self.assertEqual(result, "C:\\NVDA")
		self.assertIsNone(errorMsg)

	def test_absolutePathWithDrive_isAccepted(self):
		result, errorMsg = self._validate("d:\\NVDA")
		self.assertEqual(result, "C:\\NVDA")
		self.assertIsNone(errorMsg)
