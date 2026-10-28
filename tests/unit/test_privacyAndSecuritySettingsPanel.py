# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Abdullah Mansour
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Screen Curtain settings must track shortcut actions while retaining checkbox rollback."""

from unittest.mock import patch

import config
import screenCurtain
import wx
from gui.settingsDialogs import PrivacyAndSecuritySettingsPanel

from .test_screenCurtain import _ScreenCurtainTestCase


class TestPrivacyAndSecurityScreenCurtain(_ScreenCurtainTestCase):
	def setUp(self):
		super().setUp()
		self.app = wx.App()
		self.frame = wx.Frame(None)
		# These tests concern Screen Curtain, not changes to NVDA's global logging level.
		self.enterContext(patch("logHandler.isLogLevelForced", return_value=True))

	def tearDown(self):
		self.frame.Destroy()
		self.app.ProcessPendingEvents()
		self.app.Destroy()

	def createPanel(self):
		self.panel = PrivacyAndSecuritySettingsPanel(self.frame)

	def changeCheckbox(self, enabled: bool):
		checkbox = self.panel._screenCurtainEnabledCheckbox
		checkbox.SetValue(enabled)
		event = wx.CommandEvent(wx.EVT_CHECKBOX.typeId, checkbox.GetId())
		event.SetEventObject(checkbox)
		event.SetInt(int(enabled))
		checkbox.ProcessWindowEvent(event)

	def test_shortcutDisableUpdatesCheckbox(self):
		self.curtain.enable(persist=True)
		self.createPanel()
		self.toggleFromShortcut()
		self.assertFalse(self.panel._screenCurtainEnabledCheckbox.IsChecked())

	def test_cancelPreservesShortcutDisable(self):
		self.curtain.enable(persist=True)
		self.createPanel()
		self.toggleFromShortcut()
		self.panel.onDiscard()
		self.assertCurtainState(False, False)

	def test_okPreservesShortcutDisable(self):
		self.curtain.enable(persist=True)
		self.createPanel()
		self.toggleFromShortcut()
		self.panel.onSave()
		self.assertCurtainState(False, False)

	def test_cancelPreservesTemporaryShortcutActivation(self):
		self.createPanel()
		self.toggleFromShortcut()
		self.assertTrue(self.panel._screenCurtainEnabledCheckbox.IsChecked())
		self.panel.onDiscard()
		self.assertCurtainState(True, False)

	def test_cancelPreservesPersistentShortcutActivation(self):
		self.createPanel()
		self.toggleFromShortcut()
		self.toggleFromShortcut(repeatCount=1)
		self.panel.onDiscard()
		self.assertCurtainState(True, True)

	def test_cancelPreservesPersistenceOnlyPromotion(self):
		self.curtain.enable()
		self.createPanel()
		self.toggleFromShortcut(repeatCount=1)
		self.panel.onDiscard()
		self.assertCurtainState(True, True)

	def test_shortcutSupersedesCheckboxPreviewOnOk(self):
		self.createPanel()
		self.changeCheckbox(True)
		self.toggleFromShortcut()
		self.panel.onSave()
		self.assertCurtainState(False, False)

	def test_shortcutSupersedesCheckboxPreviewOnCancel(self):
		self.createPanel()
		self.changeCheckbox(True)
		self.toggleFromShortcut()
		self.toggleFromShortcut(repeatCount=1)
		self.panel.onDiscard()
		self.assertCurtainState(True, True)

	def test_applyThenShortcutDisableAndOk(self):
		self.createPanel()
		self.changeCheckbox(True)
		self.panel.onSave()
		self.toggleFromShortcut()
		self.panel.onSave()
		self.assertCurtainState(False, False)

	def test_applyThenShortcutDisableAndCancel(self):
		self.createPanel()
		self.changeCheckbox(True)
		self.panel.onSave()
		self.toggleFromShortcut()
		self.panel.onDiscard()
		self.assertCurtainState(False, False)

	def test_checkboxAfterShortcutCancelsToTemporaryBaseline(self):
		self.createPanel()
		self.toggleFromShortcut()
		self.changeCheckbox(False)
		self.panel.onDiscard()
		self.assertCurtainState(True, False)

	def test_checkboxAfterShortcutCancelsToPersistentBaseline(self):
		self.createPanel()
		self.toggleFromShortcut()
		self.toggleFromShortcut(repeatCount=1)
		self.changeCheckbox(False)
		self.panel.onDiscard()
		self.assertCurtainState(True, True)

	def test_checkboxOnlyCancelRestoresDisabledState(self):
		self.createPanel()
		self.changeCheckbox(True)
		self.panel.onDiscard()
		self.assertCurtainState(False, False)

	def test_checkboxOnlyCancelRestoresTemporaryState(self):
		self.curtain.enable()
		self.createPanel()
		self.changeCheckbox(False)
		self.panel.onDiscard()
		self.assertCurtainState(True, False)

	def test_checkboxOnlyOkPersistsActivation(self):
		self.createPanel()
		self.changeCheckbox(True)
		self.panel.onSave()
		self.assertCurtainState(True, True)

	def test_untouchedTemporaryActivationStaysTemporary(self):
		self.curtain.enable()
		self.createPanel()
		self.panel.onSave()
		self.assertCurtainState(True, False)

	def test_repeatedApplyThenPreviewCancel(self):
		self.createPanel()
		self.changeCheckbox(True)
		self.panel.onSave()
		self.panel.onSave()
		self.changeCheckbox(False)
		self.panel.onDiscard()
		self.assertCurtainState(True, True)

	def test_hiddenPanelTracksShortcut(self):
		self.createPanel()
		self.panel.onPanelDeactivated()
		self.toggleFromShortcut()
		self.panel.onPanelActivated()
		self.assertTrue(self.panel._screenCurtainEnabledCheckbox.IsChecked())
		self.panel.onDiscard()
		self.assertCurtainState(True, False)

	def test_destroyingPanelRemovesListener(self):
		previousHandlers = tuple(self.stateChanged.handlers)
		self.createPanel()
		self.panel.Destroy()
		self.assertEqual(tuple(self.stateChanged.handlers), previousHandlers)

	def test_destroyingChildKeepsPanelListener(self):
		self.createPanel()
		self.panel._screenCurtainWarnOnLoadCheckbox.Destroy()
		self.toggleFromShortcut()
		self.assertTrue(self.panel._screenCurtainEnabledCheckbox.IsChecked())

	def test_failedPreviewDoesNotSuppressLaterShortcut(self):
		self.createPanel()
		self.isScreenFullyBlack.return_value = False
		self.changeCheckbox(True)
		self.assertFalse(self.panel._screenCurtainEnabledCheckbox.IsChecked())
		self.isScreenFullyBlack.return_value = True
		self.toggleFromShortcut()
		self.assertTrue(self.panel._screenCurtainEnabledCheckbox.IsChecked())
		self.panel.onDiscard()
		self.assertCurtainState(True, False)

	def test_screenCurtainUnavailable(self):
		with patch.object(screenCurtain, "screenCurtain", None):
			self.createPanel()
			self.assertFalse(self.panel._screenCurtainEnabledCheckbox.IsEnabled())
			self.assertFalse(self.panel._screenCurtainEnabledCheckbox.IsChecked())
			self.panel.onSave()
			self.panel.onDiscard()

	def test_reinitializedCurtainUpdatesCheckbox(self):
		self.curtain.enable(persist=True)
		self.createPanel()
		screenCurtain.terminate()
		screenCurtain.initialize()
		replacement = screenCurtain.screenCurtain
		assert replacement is not None
		self.addCleanup(replacement.disable, persist=False)
		self.assertTrue(replacement.enabled)
		self.assertTrue(self.panel._screenCurtainEnabledCheckbox.IsChecked())

	def test_cancelPreservesReinitializedCurtain(self):
		self.curtain.enable(persist=True)
		self.createPanel()
		screenCurtain.terminate()
		screenCurtain.initialize()
		replacement = screenCurtain.screenCurtain
		assert replacement is not None
		self.addCleanup(replacement.disable, persist=False)
		self.panel.onDiscard()
		self.assertTrue(replacement.enabled)
		self.assertTrue(replacement.settings["enabled"])

	def test_saveUsesReinitializedConfiguration(self):
		self.createPanel()
		settings = config.conf["screenCurtain"].dict()
		screenCurtain.terminate()
		config.conf["screenCurtain"] = settings
		screenCurtain.initialize()
		replacement = screenCurtain.screenCurtain
		assert replacement is not None
		self.addCleanup(replacement.disable, persist=False)
		self.changeCheckbox(True)
		self.panel.onSave()
		self.assertTrue(replacement.enabled)
		self.assertTrue(replacement.settings["enabled"])
