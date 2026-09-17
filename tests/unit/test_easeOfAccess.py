# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Regression tests for saving Windows auto-start settings."""

from types import SimpleNamespace  # noqa: I001
import unittest
from unittest.mock import MagicMock, Mock, patch
from uuid import uuid4
import winreg

import config
from config.registry import EASE_OF_ACCESS_APP_KEY_NAME
import easeOfAccess
from gui import settingsDialogs, startupDialogs


class TestAutoStartRegistry(unittest.TestCase):
	def test_missingKeyAndPreservingOtherApplications(self) -> None:
		"""Use a private temporary key to exercise the actual Windows registry API."""
		path = rf"Software\NVDA_autoStartTest_{uuid4().hex}"
		self.enterContext(
			patch.object(
				easeOfAccess,
				"_RegistryKey",
				SimpleNamespace(EASE_OF_ACCESS=SimpleNamespace(value=path)),
			),
		)
		try:
			config.setStartAfterLogon(True)
			self.assertTrue(config.getStartAfterLogon())
			with winreg.OpenKey(
				winreg.HKEY_CURRENT_USER,
				path,
				access=winreg.KEY_READ | winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY,
			) as key:
				winreg.SetValueEx(key, "Configuration", 0, winreg.REG_SZ, "Narrator")
				config.setStartAfterLogon(True)
				self.assertEqual(
					winreg.QueryValueEx(key, "Configuration")[0],
					f"Narrator,{EASE_OF_ACCESS_APP_KEY_NAME}",
				)
				config.setStartAfterLogon(False)
				self.assertEqual(winreg.QueryValueEx(key, "Configuration")[0], "Narrator")
		finally:
			try:
				winreg.DeleteKeyEx(winreg.HKEY_CURRENT_USER, path, access=winreg.KEY_WOW64_64KEY)
			except FileNotFoundError:
				pass


class TestAutoStartFailures(unittest.TestCase):
	def setUp(self) -> None:
		self.enterContext(patch("easeOfAccess.winreg.OpenKey"))
		self.queryValue = self.enterContext(patch("easeOfAccess.winreg.QueryValueEx"))
		self.queryValue.return_value = ("Narrator", winreg.REG_SZ)
		self.enterContext(patch("easeOfAccess.winreg.CreateKeyEx"))
		self.setValue = self.enterContext(patch("easeOfAccess.winreg.SetValueEx"))
		self.execElevated = self.enterContext(patch("systemUtils.execElevated", return_value=0))

	def test_readFailuresDoNotWriteOrSilentlyDisable(self) -> None:
		self.queryValue.side_effect = OSError("Registry read failed")
		for setter in (config.setStartAfterLogon, config.setStartOnLogonScreen):
			for enable in (False, True):
				with self.subTest(setter=setter, enable=enable), self.assertRaises(OSError):
					setter(enable)
		self.setValue.assert_not_called()
		self.execElevated.assert_not_called()

	def test_nonStringConfigurationIsReportedAndPreserved(self) -> None:
		for value, valueType in ((1, winreg.REG_DWORD), (["Narrator"], winreg.REG_MULTI_SZ)):
			with self.subTest(value=value):
				self.queryValue.return_value = (value, valueType)
				self.assertFalse(config.getStartAfterLogon())
				with self.assertRaises(TypeError):
					config.setStartAfterLogon(True)
		self.setValue.assert_not_called()

	def test_onlyPermissionErrorsRequestElevation(self) -> None:
		self.setValue.side_effect = PermissionError()
		config.setStartOnLogonScreen(True)
		self.execElevated.assert_called_once_with(
			config.SLAVE_FILENAME,
			("config_setStartOnLogonScreen", "1"),
			wait=True,
		)
		self.execElevated.reset_mock()
		self.setValue.side_effect = OSError("Registry write failed")
		with self.assertRaises(OSError):
			config.setStartOnLogonScreen(True)
		self.execElevated.assert_not_called()


class TestAutoStartDialogs(unittest.TestCase):
	def setUp(self) -> None:
		self.conf = MagicMock()
		self.values = {"general": {}, "keyboard": {"NVDAModifierKeys": 7}}
		self.conf.__getitem__.side_effect = self.values.__getitem__
		self.enterContext(patch.object(config, "conf", self.conf))
		self.afterLogon = self.enterContext(patch.object(config, "setStartAfterLogon"))
		self.messageDialog = self.enterContext(patch("gui.message.MessageDialog"))
		self.enterContext(patch.object(settingsDialogs, "updateCheck", None))
		self.panel = Mock(
			languageNames=[("en", "English")],
			_hasStartAfterLogonChanged=False,
			_hasStartOnLogonScreenChanged=False,
		)
		self.panel.languageList.GetSelection.return_value = 0
		self.panel.startOnLogonScreenCheckBox.IsEnabled.return_value = True

	def test_unreadableAfterLogonSettingIsNotSavedWithoutUserAction(self) -> None:
		with patch("easeOfAccess.winreg.OpenKey", side_effect=PermissionError()):
			initialValue = config.getStartAfterLogon()
		self.assertFalse(initialValue)
		self.panel.startAfterLogonCheckBox.GetValue.return_value = initialValue
		settingsDialogs.GeneralSettingsPanel.onSave(self.panel)
		self.afterLogon.assert_not_called()

		dialog = Mock(kbdNames=["desktop"], _hasStartAfterLogonChanged=False)
		dialog.kbdList.GetSelection.return_value = 0
		dialog.startAfterLogonCheckBox.Value = initialValue
		startupDialogs.WelcomeDialog.onOk(dialog, Mock())
		self.afterLogon.assert_not_called()

	def test_unreadableLogonSettingNeedsUserActionBeforeElevation(self) -> None:
		self.enterContext(patch("easeOfAccess.winreg.OpenKey", side_effect=PermissionError()))
		execElevated = self.enterContext(patch("systemUtils.execElevated", return_value=0))
		self.panel.startOnLogonScreenCheckBox.GetValue.return_value = config.getStartOnLogonScreen()
		self.assertFalse(self.panel.startOnLogonScreenCheckBox.GetValue())

		settingsDialogs.GeneralSettingsPanel.onSave(self.panel)
		execElevated.assert_not_called()

		# An explicit choice must still be saved, even if it ends at the fallback value.
		settingsDialogs.GeneralSettingsPanel._onStartOnLogonScreenChanged(self.panel, Mock())
		settingsDialogs.GeneralSettingsPanel.onSave(self.panel)
		execElevated.assert_called_once_with(
			config.SLAVE_FILENAME,
			("config_setStartOnLogonScreen", "0"),
			wait=True,
		)

	def test_logonSettingRetriesAfterFailureButNotAfterSuccess(self) -> None:
		setter = self.enterContext(patch.object(config, "setStartOnLogonScreen"))
		self.panel.startOnLogonScreenCheckBox.GetValue.return_value = True
		settingsDialogs.GeneralSettingsPanel._onStartOnLogonScreenChanged(self.panel, Mock())
		setter.side_effect = OSError("Registry write failed")
		settingsDialogs.GeneralSettingsPanel.onSave(self.panel)
		self.messageDialog.assert_called_once()
		self.messageDialog.return_value.ShowModal.assert_called_once()
		setter.side_effect = None
		settingsDialogs.GeneralSettingsPanel.onSave(self.panel)
		settingsDialogs.GeneralSettingsPanel.onSave(self.panel)
		self.assertEqual(setter.call_count, 2)
		setter.assert_called_with(True)

	def test_firstSettingFailureDoesNotPreventSavingSecond(self) -> None:
		setter = self.enterContext(patch.object(config, "setStartOnLogonScreen"))
		self.afterLogon.side_effect = PermissionError()
		settingsDialogs.GeneralSettingsPanel._onStartAfterLogonChanged(self.panel, Mock())
		self.panel.startOnLogonScreenCheckBox.GetValue.return_value = True
		settingsDialogs.GeneralSettingsPanel._onStartOnLogonScreenChanged(self.panel, Mock())
		settingsDialogs.GeneralSettingsPanel.onSave(self.panel)
		setter.assert_called_once_with(True)
		self.messageDialog.assert_called_once()
		self.assertIn("preventDisplayTurningOff", self.values["general"])

	def test_welcomeDialogReportsFailureAndSavesOtherSettings(self) -> None:
		dialog = Mock(kbdNames=["desktop"])
		dialog.kbdList.GetSelection.return_value = 0
		self.afterLogon.side_effect = TypeError("Invalid auto-start configuration")
		startupDialogs.WelcomeDialog._onStartAfterLogonChanged(dialog, Mock())
		startupDialogs.WelcomeDialog.onOk(dialog, Mock())
		self.messageDialog.assert_called_once()
		self.messageDialog.return_value.ShowModal.assert_called_once()
		self.conf.save.assert_called_once()
		self.assertEqual(self.values["keyboard"]["keyboardLayout"], "desktop")
		dialog.EndModal.assert_called_once()
