# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the keyboardHandler module."""

import ctypes
import unittest
from unittest.mock import MagicMock, patch

import inputCore
import keyboardHandler
import vkCodes
import winInputHook
import winUser
from keyboardHandler import KeyboardInputGesture, getNVDAModifierKeys


class TestFromName(unittest.TestCase):
	"""Tests for KeyboardInputGesture.fromName."""

	def test_mainKeyLast(self):
		gesture = KeyboardInputGesture.fromName("control+alt+upArrow")
		vk, ext = vkCodes.byName["uparrow"]
		self.assertEqual(gesture.vkCode, vk)
		self.assertEqual(gesture.isExtended, ext)
		self.assertEqual(
			gesture.modifiers,
			{(winUser.VK_CONTROL, False), (winUser.VK_MENU, False)},
		)

	def test_mainKeyNotLast(self):
		gesture = KeyboardInputGesture.fromName("alt+b+control")
		self.assertEqual(gesture.vkCode, ord("B"))
		self.assertEqual(
			gesture.modifiers,
			{(winUser.VK_CONTROL, False), (winUser.VK_MENU, False)},
		)

	def test_mainKeyFirst(self):
		gesture = KeyboardInputGesture.fromName("upArrow+control+alt")
		vk, ext = vkCodes.byName["uparrow"]
		self.assertEqual(gesture.vkCode, vk)
		self.assertEqual(gesture.isExtended, ext)
		self.assertEqual(
			gesture.modifiers,
			{(winUser.VK_CONTROL, False), (winUser.VK_MENU, False)},
		)

	def test_sameGestureRegardlessOfOrder(self):
		self.assertEqual(
			KeyboardInputGesture.fromName("alt+control+b").normalizedIdentifiers,
			KeyboardInputGesture.fromName("alt+b+control").normalizedIdentifiers,
		)

	def test_modifiersOnly(self):
		gesture = KeyboardInputGesture.fromName("control+alt")
		self.assertEqual(gesture.vkCode, winUser.VK_MENU)
		self.assertEqual(gesture.modifiers, {(winUser.VK_CONTROL, False)})

	def test_singleModifier(self):
		gesture = KeyboardInputGesture.fromName("alt")
		self.assertEqual(gesture.vkCode, winUser.VK_MENU)
		self.assertEqual(gesture.modifiers, set())

	def test_nvdaModifierWithMainKey(self):
		gesture = KeyboardInputGesture.fromName("NVDA+b")
		self.assertEqual(gesture.vkCode, ord("B"))
		self.assertIn(getNVDAModifierKeys()[0], gesture.modifiers)

	def test_multipleMainKeys(self):
		with self.assertRaises(ValueError):
			KeyboardInputGesture.fromName("control+b+c")

	def test_duplicateMainKey(self):
		with self.assertRaises(ValueError):
			KeyboardInputGesture.fromName("control+b+b")

	def test_unknownKeyName(self):
		with self.assertRaises(ValueError):
			KeyboardInputGesture.fromName("control+bogus")

	def test_emptyName(self):
		with self.assertRaises(ValueError):
			KeyboardInputGesture.fromName("")


class TestDiscardReleasedModifiers(unittest.TestCase):
	"""Tests that modifiers whose key up was never received stop being tracked (#21083)."""

	LEFT_CONTROL = (winUser.VK_LCONTROL, False)
	RIGHT_SHIFT = (winUser.VK_RSHIFT, False)
	NVDA_KEY = (winUser.VK_INSERT, True)

	def setUp(self) -> None:
		#: The virtual key codes Windows reports as being held down.
		self.keysDownInWindows: set[int] = set()
		self.manager = MagicMock(isInputHelpActive=False, lastModifierWasInSayAll=False)
		self.manager.executeGesture.side_effect = inputCore.NoInputGestureAction
		self.watchdogObserver = MagicMock(isAttemptingRecovery=False)
		for target, name, value in (
			(inputCore, "manager", self.manager),
			(keyboardHandler, "_watchdogObserver", self.watchdogObserver),
			(keyboardHandler, "passKeyThroughCount", -1),
			(keyboardHandler.api, "getFocusObject", MagicMock(return_value=None)),
			(keyboardHandler, "currentModifiers", set()),
			(keyboardHandler, "trappedKeys", set()),
			(keyboardHandler, "stickyNVDAModifier", None),
			(keyboardHandler, "stickyNVDAModifierLocked", False),
			(keyboardHandler, "lastNVDAModifier", None),
			(keyboardHandler, "lastNVDAModifierReleaseTime", None),
			(keyboardHandler, "bypassNVDAModifier", False),
			(keyboardHandler, "keyCounter", 0),
			(keyboardHandler, "ignoreInjected", False),
			(keyboardHandler.winUser, "getAsyncKeyState", self._getAsyncKeyState),
			# The result must not depend on whether Sticky Keys is enabled on the machine running the tests.
			(keyboardHandler.winUser, "getSystemStickyKeys", MagicMock(return_value=MagicMock(dwFlags=0))),
		):
			patcher = patch.object(target, name, value)
			patcher.start()
			self.addCleanup(patcher.stop)

	def _getAsyncKeyState(self, vkCode: int) -> int:
		# GetAsyncKeyState returns a SHORT, so its most significant bit makes the value negative.
		return -0x8000 if vkCode in self.keysDownInWindows else 0

	def test_releasedModifierDiscarded(self) -> None:
		# The low bit only means the key was pressed since an earlier query, not that it is still down.
		for state in (0, 1):
			with (
				self.subTest(state=state),
				patch.object(keyboardHandler.winUser, "getAsyncKeyState", return_value=state),
			):
				keyboardHandler.currentModifiers.add(self.LEFT_CONTROL)
				keyboardHandler._discardReleasedModifiers()
				self.assertEqual(keyboardHandler.currentModifiers, set())

	def test_heldModifierKept(self) -> None:
		keyboardHandler.currentModifiers.add(self.LEFT_CONTROL)
		self.keysDownInWindows.add(winUser.VK_LCONTROL)
		keyboardHandler._discardReleasedModifiers()
		self.assertEqual(keyboardHandler.currentModifiers, {self.LEFT_CONTROL})

	def test_onlyReleasedModifiersDiscarded(self) -> None:
		keyboardHandler.currentModifiers.update((self.LEFT_CONTROL, self.RIGHT_SHIFT))
		self.keysDownInWindows.add(winUser.VK_RSHIFT)
		keyboardHandler._discardReleasedModifiers()
		self.assertEqual(keyboardHandler.currentModifiers, {self.RIGHT_SHIFT})

	def test_trappedModifierKept(self) -> None:
		"""Windows never sees a key NVDA trapped, so it reporting the key as up means nothing."""
		keyboardHandler.currentModifiers.add(self.NVDA_KEY)
		keyboardHandler.trappedKeys.add(self.NVDA_KEY)
		keyboardHandler._discardReleasedModifiers()
		self.assertEqual(keyboardHandler.currentModifiers, {self.NVDA_KEY})

	def test_stickyNVDAModifierKept(self) -> None:
		"""A latched NVDA modifier is intentionally tracked after its key has been released."""
		keyboardHandler.currentModifiers.add(self.NVDA_KEY)
		keyboardHandler.stickyNVDAModifier = self.NVDA_KEY
		keyboardHandler._discardReleasedModifiers()
		self.assertEqual(keyboardHandler.currentModifiers, {self.NVDA_KEY})

	def test_sayAllStateClearedOnlyWhenLastModifierReleased(self) -> None:
		"""A missed release must not make the next navigation command resume say all."""
		for held in (False, True):
			with self.subTest(held=held):
				keyboardHandler.currentModifiers.add(self.LEFT_CONTROL)
				if held:
					self.keysDownInWindows.add(winUser.VK_LCONTROL)
				self.manager.lastModifierWasInSayAll = True
				keyboardHandler._discardReleasedModifiers()
				self.assertEqual(self.manager.lastModifierWasInSayAll, held)

	def test_releasedModifierDiscardedWhenKeyDownReceivedPromptly(self) -> None:
		keyboardHandler.currentModifiers.add(self.LEFT_CONTROL)
		with patch.object(keyboardHandler.winInputHook, "_getCurrentKeyEventDelay", return_value=0):
			keyboardHandler._discardReleasedModifiers()
		self.assertEqual(keyboardHandler.currentModifiers, set())

	def test_modifierKeptWhenKeyDownReceivedLate(self) -> None:
		"""Windows has moved on from a key down received late, so its current state proves nothing."""
		keyboardHandler.currentModifiers.add(self.LEFT_CONTROL)
		with patch.object(
			keyboardHandler.winInputHook,
			"_getCurrentKeyEventDelay",
			return_value=keyboardHandler._MAX_KEY_DOWN_DELAY_TO_CHECK_MODIFIERS_MS + 1,
		):
			keyboardHandler._discardReleasedModifiers()
		self.assertEqual(keyboardHandler.currentModifiers, {self.LEFT_CONTROL})

	def test_keyDownDoesNotUseModifierWhoseKeyUpWasMissed(self) -> None:
		"""A key pressed after a missed modifier release must not be treated as modified."""
		# Control goes down, but NVDA will ignore its injected release.
		keyboardHandler.internal_keyDownEvent(winUser.VK_LCONTROL, 0, False, False)
		self.keysDownInWindows.add(winUser.VK_LCONTROL)
		self.assertEqual(keyboardHandler.currentModifiers, {self.LEFT_CONTROL})
		# An injected release during send() is ignored by NVDA, but still reaches Windows.
		with patch.object(keyboardHandler, "ignoreInjected", True):
			self.assertTrue(keyboardHandler.internal_keyUpEvent(winUser.VK_LCONTROL, 0, False, True))
		self.keysDownInWindows.discard(winUser.VK_LCONTROL)
		self.assertEqual(keyboardHandler.currentModifiers, {self.LEFT_CONTROL})
		keyboardHandler.internal_keyDownEvent(ord("A"), 0, False, False)
		gesture = self.manager.executeGesture.call_args.args[0]
		self.assertEqual(gesture.vkCode, ord("A"))
		self.assertEqual(gesture.modifiers, set())
		self.assertEqual(keyboardHandler.currentModifiers, set())

	def test_modifierKeptIfStateQueryFinishesAfterHookTimeout(self) -> None:
		"""A stall during the Windows query must not strip Ctrl from a delayed Ctrl+C."""
		keyboardHandler.currentModifiers.add(self.LEFT_CONTROL)
		event = winInputHook.KBDLLHOOKSTRUCT(vkCode=ord("C"), time=1000)
		with (
			patch.object(winInputHook, "keyDownCallback", keyboardHandler.internal_keyDownEvent),
			patch.object(winInputHook.kernel32, "GetTickCount", return_value=1000) as tickCount,
			patch.object(winInputHook.user32, "CallNextHookEx", return_value=0),
			patch.object(keyboardHandler.winUser, "getAsyncKeyState") as getState,
		):

			def getStateAfterStall(vkCode: int) -> int:
				# Windows processed the later Ctrl release while the hook thread was stalled.
				tickCount.return_value = 3000
				return 0

			getState.side_effect = getStateAfterStall
			winInputHook.keyboardHook(winInputHook.HC_ACTION, 0, ctypes.addressof(event))
		self.assertEqual(self.manager.executeGesture.call_args.args[0].modifiers, {self.LEFT_CONTROL})
		self.assertEqual(keyboardHandler.currentModifiers, {self.LEFT_CONTROL})

	def test_lateKeyDownKeepsModifierUntilNextPromptKeyDown(self) -> None:
		"""A delayed Ctrl+C keeps Ctrl; the next timely key clears the missed release."""
		keyboardHandler.currentModifiers.add(self.LEFT_CONTROL)
		event = winInputHook.KBDLLHOOKSTRUCT(vkCode=ord("C"), time=1000)
		with (
			patch.object(winInputHook, "keyDownCallback", keyboardHandler.internal_keyDownEvent),
			patch.object(winInputHook.kernel32, "GetTickCount", return_value=3400),
			patch.object(winInputHook.user32, "CallNextHookEx", return_value=0),
		):
			winInputHook.keyboardHook(winInputHook.HC_ACTION, 0, ctypes.addressof(event))
			self.assertEqual(self.manager.executeGesture.call_args.args[0].modifiers, {self.LEFT_CONTROL})
			event.vkCode = ord("A")
			event.time = 3400
			winInputHook.keyboardHook(winInputHook.HC_ACTION, 0, ctypes.addressof(event))
			self.assertEqual(self.manager.executeGesture.call_args.args[0].modifiers, set())
		self.assertEqual(keyboardHandler.currentModifiers, set())

	def test_modifierStateAcrossWatchdogRecovery(self) -> None:
		"""Recovery preserves held modifiers and repairs missed releases without executing scripts."""
		for released, keyUpDelivered in ((False, False), (True, False), (True, True)):
			with self.subTest(released=released, keyUpDelivered=keyUpDelivered):
				keyboardHandler.currentModifiers.clear()
				self.keysDownInWindows.clear()
				keyboardHandler.internal_keyDownEvent(winUser.VK_LCONTROL, 0, False, False)
				self.keysDownInWindows.add(winUser.VK_LCONTROL)
				self.watchdogObserver.isAttemptingRecovery = True
				self.manager.executeGesture.reset_mock()
				if released:
					if keyUpDelivered:
						self.assertTrue(
							keyboardHandler.internal_keyUpEvent(winUser.VK_LCONTROL, 0, False, False),
						)
					self.keysDownInWindows.discard(winUser.VK_LCONTROL)
				self.assertTrue(keyboardHandler.internal_keyDownEvent(ord("B"), 0, False, False))
				self.manager.executeGesture.assert_not_called()
				self.watchdogObserver.isAttemptingRecovery = False
				keyboardHandler.internal_keyDownEvent(ord("A"), 0, False, False)
				expectedModifiers = set() if released else {self.LEFT_CONTROL}
				self.assertEqual(self.manager.executeGesture.call_args.args[0].modifiers, expectedModifiers)
