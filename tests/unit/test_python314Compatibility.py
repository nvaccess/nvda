# A part of NonVisual Desktop Access (NVDA)
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Regression tests for control flow moved out of finally blocks."""

import unittest  # noqa: I001
from contextlib import ExitStack
from types import SimpleNamespace
from unittest.mock import Mock, patch

import braille.display.driver
from brailleDisplayDrivers import seikantk
import globalCommands
import keyboardHandler
import screenCurtain


class TestSeikaTermination(unittest.TestCase):
	def test_deviceClosedWhenBaseTerminationFails(self):
		driver = object.__new__(seikantk.BrailleDisplayDriver)
		driver._dev = Mock()
		with (
			patch.object(
				braille.display.driver.BrailleDisplayDriver, "terminate", side_effect=RuntimeError()
			),
			self.assertRaises(RuntimeError),
		):
			driver.terminate()
		driver._dev.close.assert_called_once()

	def test_uninitializedDeviceDoesNotSuppressBaseError(self):
		driver = object.__new__(seikantk.BrailleDisplayDriver)
		driver._dev = None
		with (
			patch.object(
				braille.display.driver.BrailleDisplayDriver, "terminate", side_effect=RuntimeError()
			),
			self.assertRaises(RuntimeError),
		):
			driver.terminate()

	def test_uninitializedDeviceCanTerminate(self):
		driver = object.__new__(seikantk.BrailleDisplayDriver)
		driver._dev = None
		with patch.object(braille.display.driver.BrailleDisplayDriver, "terminate") as terminate:
			driver.terminate()
		terminate.assert_called_once()


class TestKeyDownRecovery(unittest.TestCase):
	def setUp(self):
		stack = self.enterContext(ExitStack())
		self.observer = SimpleNamespace(isAttemptingRecovery=False)
		self.manager = SimpleNamespace(executeGesture=Mock())
		values = {
			"_watchdogObserver": self.observer,
			"currentModifiers": set(),
			"trappedKeys": set(),
			"keyCounter": 0,
			"passKeyThroughCount": -1,
			"lastNVDAModifier": None,
			"lastNVDAModifierReleaseTime": None,
			"bypassNVDAModifier": False,
			"stickyNVDAModifier": None,
			"stickyNVDAModifierLocked": False,
			"ignoreInjected": False,
		}
		for name, value in values.items():
			stack.enter_context(patch.object(keyboardHandler, name, value))
		stack.enter_context(patch.object(keyboardHandler.inputCore, "manager", self.manager))
		self.decide = stack.enter_context(
			patch.object(keyboardHandler.inputCore.decide_handleRawKey, "decide", return_value=True)
		)
		stack.enter_context(
			patch.object(
				keyboardHandler.winUser, "getSystemStickyKeys", return_value=SimpleNamespace(dwFlags=0)
			)
		)
		stack.enter_context(
			patch.object(
				keyboardHandler,
				"KeyboardInputGesture",
				return_value=SimpleNamespace(isModifier=False, isNVDAModifierKey=False),
			)
		)
		stack.enter_context(patch.object(keyboardHandler, "shouldUseToUnicodeEx", return_value=False))
		self.getFocus = stack.enter_context(patch.object(keyboardHandler.api, "getFocusObject"))

	def test_executedGestureRemainsTrapped(self):
		self.assertFalse(keyboardHandler.internal_keyDownEvent(ord("A"), 30, False, False))
		self.manager.executeGesture.assert_called_once()
		self.assertIn((ord("A"), False), keyboardHandler.trappedKeys)
		self.getFocus.assert_called_once()

	def test_recoveryStartedByGesturePassesKeyAndSkipsTypedCharacters(self):
		def startRecovery(gesture):
			self.observer.isAttemptingRecovery = True

		self.manager.executeGesture.side_effect = startRecovery
		self.assertTrue(keyboardHandler.internal_keyDownEvent(ord("A"), 30, False, False))
		self.manager.executeGesture.assert_called_once()
		self.getFocus.assert_not_called()

	def test_rawKeyVetoStillBlocksDuringRecovery(self):
		self.observer.isAttemptingRecovery = True
		self.decide.return_value = False
		self.assertFalse(keyboardHandler.internal_keyDownEvent(ord("A"), 30, False, False))
		self.manager.executeGesture.assert_not_called()
		self.getFocus.assert_not_called()

	def test_ignoredInjectionStillRunsCleanup(self):
		with patch.object(keyboardHandler, "ignoreInjected", True):
			self.assertTrue(keyboardHandler.internal_keyDownEvent(ord("A"), 30, False, True))
		self.manager.executeGesture.assert_not_called()
		self.getFocus.assert_called_once()


class TestScreenCurtainDisable(unittest.TestCase):
	def test_disableReportsSuccessAndFailure(self):
		for error in (None, RuntimeError("termination failed")):
			with self.subTest(error=error), ExitStack() as stack:
				curtain = SimpleNamespace(enabled=True, disable=Mock(side_effect=error))
				stack.enter_context(patch.object(screenCurtain, "screenCurtain", curtain))
				stack.enter_context(patch.object(globalCommands, "getLastScriptRepeatCount", return_value=0))
				stack.enter_context(
					patch.object(globalCommands.GlobalCommands, "_tempEnableScreenCurtain", True)
				)
				message = stack.enter_context(patch.object(globalCommands.ui, "message"))
				commands = globalCommands.GlobalCommands()
				commands.script_toggleScreenCurtain(Mock())
				curtain.disable.assert_called_once()
				message.assert_called_once()
				self.assertEqual(message.call_args.args[0], commands._toggleScreenCurtainMessage)

	def test_disableDoesNotSuppressSystemExit(self):
		curtain = SimpleNamespace(enabled=True, disable=Mock(side_effect=SystemExit()))
		with (
			patch.object(screenCurtain, "screenCurtain", curtain),
			patch.object(globalCommands, "getLastScriptRepeatCount", return_value=0),
			patch.object(globalCommands.GlobalCommands, "_tempEnableScreenCurtain", True),
			patch.object(globalCommands.ui, "message") as message,
			self.assertRaises(SystemExit),
		):
			globalCommands.GlobalCommands().script_toggleScreenCurtain(Mock())
		message.assert_called_once()
