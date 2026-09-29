# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NVDA Contributors
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Regression tests for typed echo, protected text and the terminal word buffer."""

import unittest
from itertools import product
from unittest.mock import Mock, call, patch

import config
from config.configFlags import TypingEcho
from speech import speech as speechModule


class TestSpeakTypedCharacters(unittest.TestCase):
	"""Exercise typed echo without consulting real accessibility objects."""

	def setUp(self) -> None:
		self.keyboardConfig: dict[str, int] = {
			"speakTypedCharacters": TypingEcho.OFF.value,
			"speakTypedWords": TypingEcho.OFF.value,
		}
		self.wordChars: list[str] = []
		self.speechState: speechModule.SpeechState = speechModule.SpeechState()
		self.enterContext(patch.object(config, "conf", {"keyboard": self.keyboardConfig}))
		self.enterContext(patch.object(speechModule, "_curWordChars", self.wordChars))
		self.enterContext(patch.object(speechModule, "_speechState", self.speechState))
		self.isTypingProtected: Mock = self.enterContext(
			patch.object(speechModule.api, "isTypingProtected", return_value=False),
		)
		self.isFocusEditable: Mock = self.enterContext(
			patch.object(speechModule, "isFocusEditable", return_value=True),
		)
		self.speakText: Mock = self.enterContext(patch.object(speechModule, "speakText"))
		self.speakSpelling: Mock = self.enterContext(patch.object(speechModule, "speakSpelling"))
		self.enterContext(patch.object(speechModule.time, "time", return_value=100.0))
		self.enterContext(patch.object(speechModule.log, "isEnabledFor", return_value=True))
		self.logIO: Mock = self.enterContext(patch.object(speechModule.log, "io"))

	def _setModes(self, characters: TypingEcho, words: TypingEcho) -> None:
		self.keyboardConfig["speakTypedCharacters"] = characters.value
		self.keyboardConfig["speakTypedWords"] = words.value

	def _type(self, text: str) -> None:
		for character in text:
			speechModule.speakTypedCharacters(character)

	def _resetOutput(self) -> None:
		self.wordChars.clear()
		self.speakText.reset_mock()
		self.speakSpelling.reset_mock()
		self.isTypingProtected.reset_mock()
		self.isFocusEditable.reset_mock()
		self.logIO.reset_mock()

	def test_disabledEchoMaintainsMaskedTerminalBufferWithoutQueryingFocus(self) -> None:
		self.isTypingProtected.side_effect = AssertionError("Must not query accessibility objects")
		# EnhancedTermTypedCharSupport relies on the buffer length, including combining marks.
		self._type("aé3\u0301")
		self.assertEqual(self.wordChars, [speechModule.PROTECTED_CHAR] * 4)
		self._type("\b")
		self.assertEqual(len(self.wordChars), 3)
		self._type("\x7f")
		self.assertEqual(len(self.wordChars), 3)
		self._type("\t")
		self.assertEqual(self.wordChars, [])
		self.logIO.assert_called_once_with("typed word: " + speechModule.PROTECTED_CHAR * 3)
		self._type("\b")
		self.assertEqual(self.wordChars, [])
		self.isTypingProtected.assert_not_called()
		self.isFocusEditable.assert_not_called()
		self.speakText.assert_not_called()
		self.speakSpelling.assert_not_called()

	def test_controlCharactersFlushWithoutBeingSpelled(self) -> None:
		for mode, delimiter in product((TypingEcho.OFF, TypingEcho.ALWAYS), ("\t", "\n", "\x01")):
			with self.subTest(mode=mode, delimiter=repr(delimiter)):
				self._resetOutput()
				self._setModes(mode, mode)
				self._type("ab" + delimiter)
				self.assertEqual(self.wordChars, [])
				if mode == TypingEcho.ALWAYS:
					self.speakText.assert_called_once_with("ab")
					self.assertEqual(self.speakSpelling.call_args_list, [call("a"), call("b")])
				else:
					self.isTypingProtected.assert_not_called()
					self.speakText.assert_not_called()
					self.speakSpelling.assert_not_called()

	def test_deleteDoesNotConsumeCharacterSuppression(self) -> None:
		self.speechState._suppressSpeakTypedCharactersNumber = 2
		self.speechState._suppressSpeakTypedCharactersTime = 99.95
		self._type("\x7f")
		self.assertEqual(self.speechState._suppressSpeakTypedCharactersNumber, 2)
		self.assertEqual(self.speechState._suppressSpeakTypedCharactersTime, 99.95)
		self.isTypingProtected.assert_not_called()

	def test_suppressionStillExpiresOrConsumesCharacters(self) -> None:
		for mode, timestamp in product((TypingEcho.OFF, TypingEcho.ALWAYS), (99.95, 99.0)):
			with self.subTest(mode=mode, timestamp=timestamp):
				self._resetOutput()
				self._setModes(mode, TypingEcho.OFF)
				self.speechState._suppressSpeakTypedCharactersNumber = 2
				self.speechState._suppressSpeakTypedCharactersTime = timestamp
				self._type("a")
				if timestamp == 99.95:
					self.assertEqual(self.speechState._suppressSpeakTypedCharactersNumber, 1)
					self.assertEqual(self.speechState._suppressSpeakTypedCharactersTime, timestamp)
				else:
					self.assertEqual(self.speechState._suppressSpeakTypedCharactersNumber, 0)
					self.assertIsNone(self.speechState._suppressSpeakTypedCharactersTime)
				if mode == TypingEcho.ALWAYS and timestamp == 99.0:
					self.speakSpelling.assert_called_once_with("a")
				else:
					self.speakSpelling.assert_not_called()
				if mode == TypingEcho.OFF:
					self.isTypingProtected.assert_not_called()

	def test_enabledModesKeepFocusAndProtectionChecks(self) -> None:
		for characters, words, editable, protected in product(
			TypingEcho,
			TypingEcho,
			(False, True),
			(False, True),
		):
			if characters == words == TypingEcho.OFF:
				continue
			with self.subTest(characters=characters, words=words, editable=editable, protected=protected):
				self._resetOutput()
				self._setModes(characters, words)
				self.isFocusEditable.return_value = editable
				self.isTypingProtected.return_value = protected
				self._type("ab")
				self.assertEqual(
					self.wordChars,
					[speechModule.PROTECTED_CHAR] * 2 if protected else ["a", "b"],
				)
				self._type(" ")
				self.assertEqual(self.isTypingProtected.call_count, 3)
				self.assertEqual(self.wordChars, [])
				if characters == TypingEcho.ALWAYS or (characters == TypingEcho.EDIT_CONTROLS and editable):
					expected: list[str] = [speechModule.PROTECTED_CHAR] * 3 if protected else ["a", "b", " "]
					self.assertEqual(self.speakSpelling.call_args_list, [call(value) for value in expected])
				else:
					self.speakSpelling.assert_not_called()
				if not protected and (
					words == TypingEcho.ALWAYS or (words == TypingEcho.EDIT_CONTROLS and editable)
				):
					self.speakText.assert_called_once_with("ab")
				else:
					self.speakText.assert_not_called()
				if protected:
					self.logIO.assert_called_once_with("typed word: " + speechModule.PROTECTED_CHAR * 2)

	def test_enablingEchoDoesNotRevealPreviouslySilentCharacters(self) -> None:
		self.isTypingProtected.side_effect = AssertionError("Disabled echo must not query protection")
		self._type("secret")
		self.isTypingProtected.assert_not_called()
		self.assertEqual(self.wordChars, [speechModule.PROTECTED_CHAR] * 6)
		self.isTypingProtected.side_effect = None
		self._setModes(TypingEcho.ALWAYS, TypingEcho.ALWAYS)
		self._type("z ")
		self.speakText.assert_called_once_with(speechModule.PROTECTED_CHAR * 6 + "z")
		self.assertEqual(self.speakSpelling.call_args_list, [call("z"), call(" ")])
		self.assertEqual(self.isTypingProtected.call_count, 2)
		self.assertEqual(self.wordChars, [])
