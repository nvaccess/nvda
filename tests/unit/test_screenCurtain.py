# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Abdullah Mansour
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Screen Curtain state changes, including persistence-only shortcut actions."""

import unittest
from unittest.mock import patch

import config
import extensionPoints
import globalCommands
import screenCurtain
from screenCurtain import _screenCurtain

from .test_globalCommands import _FakeInputGesture


class _ScreenCurtainTestCase(unittest.TestCase):
	def setUp(self):
		originalSettings = config.conf["screenCurtain"].dict()
		self.addCleanup(config.conf.__setitem__, "screenCurtain", originalSettings)
		config.conf["screenCurtain"].update(
			{"enabled": False, "warnOnLoad": False, "playToggleSounds": False},
		)
		# Exercise the real state machine without touching the user's physical display or magnifier.
		for function in (
			"MagInitialize",
			"MagUninitialize",
			"MagSetFullscreenColorEffect",
			"MagShowSystemCursor",
		):
			self.enterContext(patch.object(_screenCurtain.magnification, function, return_value=True))
		self.isScreenFullyBlack = self.enterContext(
			patch.object(_screenCurtain, "isScreenFullyBlack", return_value=True),
		)
		self.enterContext(patch("_magnifier.getMagnifier", return_value=None))
		self.enterContext(patch.object(globalCommands.ui, "message"))
		self.curtain = _screenCurtain.ScreenCurtain()
		self.addCleanup(self.curtain.disable, persist=False)
		self.enterContext(patch.object(screenCurtain, "screenCurtain", self.curtain))
		# Keep each test's listeners isolated, including when testing pre-fix source.
		self.stateChanged = extensionPoints.Action()
		self.enterContext(
			patch.object(_screenCurtain, "_postScreenCurtainStateChange", self.stateChanged, create=True),
		)
		self.observedStates = []
		self.stateChanged.register(self._recordState)
		self.commands = globalCommands.GlobalCommands()
		self.gesture = _FakeInputGesture()

	def toggleFromShortcut(self, repeatCount: int = 0):
		with patch.object(globalCommands, "getLastScriptRepeatCount", return_value=repeatCount):
			self.commands.script_toggleScreenCurtain(self.gesture)

	def assertCurtainState(self, enabled: bool, persisted: bool):
		self.assertEqual((self.curtain.enabled, self.curtain.settings["enabled"]), (enabled, persisted))

	def _recordState(self):
		self.observedStates.append((self.curtain.enabled, self.curtain.settings["enabled"]))


class TestScreenCurtainState(_ScreenCurtainTestCase):
	def test_persistAlreadyEnabledTemporaryCurtain(self):
		self.curtain.enable()
		self.curtain.enable(persist=True)
		self.assertCurtainState(True, True)

	def test_notifyTemporaryActivation(self):
		self.curtain.enable()
		self.assertEqual(self.observedStates, [(True, False)])

	def test_notifyPersistentActivation(self):
		self.curtain.enable(persist=True)
		self.assertEqual(self.observedStates, [(True, True)])

	def test_notifyDeactivation(self):
		self.curtain.enable(persist=True)
		self.observedStates.clear()
		self.curtain.disable()
		self.assertEqual(self.observedStates, [(False, False)])

	def test_shortcutPromotionNotifiesPersistenceChange(self):
		self.toggleFromShortcut()
		self.toggleFromShortcut(repeatCount=1)
		self.assertEqual(self.observedStates, [(True, False), (True, True)])

	def test_unchangedCallsDoNotNotifyAgain(self):
		self.curtain.enable()
		self.curtain.enable()
		self.curtain.enable(persist=True)
		self.curtain.enable(persist=True)
		self.curtain.disable()
		self.curtain.disable()
		self.assertEqual(self.observedStates, [(True, False), (True, True), (False, False)])

	def test_failedActivationDoesNotNotify(self):
		self.isScreenFullyBlack.return_value = False
		with self.assertRaises(RuntimeError):
			self.curtain.enable(persist=True)
		self.assertCurtainState(False, False)
		self.assertEqual(self.observedStates, [])
