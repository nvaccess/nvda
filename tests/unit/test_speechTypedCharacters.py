# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited

"""Unit tests for speech.speakTypedCharacters.

These cover the lazy resolution of the focus object's protected state. Resolving it
requires a blocking cross-process accessibility call, so it must not happen for
characters which cannot lead to speech (#20654).
"""

import unittest
from unittest.mock import patch

import config
import speech
from config.configFlags import TypingEcho
from speech import speech as speechModule


CTRL_C = "\x03"
"""The character produced by control+c, as delivered to speakTypedCharacters."""

ENTER = "\r"
"""The character produced by the enter key."""

DELETE = chr(0x7F)
"""The delete character produced in some apps by control+backspace."""


class _SpeakTypedCharactersTestCase(unittest.TestCase):
	"""Provides a clean typed word buffer and echo configuration for each test."""

	def setUp(self):
		speechModule.clearTypedWordBuffer()
		speechModule._speechState._suppressSpeakTypedCharactersNumber = 0
		speechModule._speechState._suppressSpeakTypedCharactersTime = None
		self.setEcho(chars=TypingEcho.OFF, words=TypingEcho.OFF)

	def tearDown(self):
		speechModule.clearTypedWordBuffer()

	def setEcho(self, chars: TypingEcho, words: TypingEcho) -> None:
		config.conf["keyboard"]["speakTypedCharacters"] = chars.value
		config.conf["keyboard"]["speakTypedWords"] = words.value

	def speak(self, ch: str, isProtected: bool = False):
		"""Call speakTypedCharacters with the accessibility and speech layers mocked.

		:return: a tuple of (isTypingProtected mock, speakText mock, speakSpelling mock).
		"""
		with (
			patch.object(speechModule.api, "isTypingProtected", return_value=isProtected) as protected,
			patch.object(speechModule, "speakText") as speakText,
			patch.object(speechModule, "speakSpelling") as speakSpelling,
			patch.object(speechModule, "isFocusEditable", return_value=True),
		):
			speech.speakTypedCharacters(ch)
			return protected, speakText, speakSpelling


class TestProtectedStateNotResolvedUnnecessarily(_SpeakTypedCharactersTestCase):
	"""The cross-process fetch must be skipped when it cannot affect the outcome."""

	def test_controlCharacterWithEmptyBuffer(self):
		"""Control+c with nothing buffered cannot produce speech."""
		protected, _speakText, _speakSpelling = self.speak(CTRL_C)
		protected.assert_not_called()

	def test_enterWithEmptyBuffer(self):
		"""Enter is reported the same way as any other control character."""
		protected, _speakText, _speakSpelling = self.speak(ENTER)
		protected.assert_not_called()

	def test_controlCharacterFlushingBufferWithWordEchoOff(self):
		"""A buffered word is discarded without being spoken, so no fetch is needed."""
		speechModule._curWordChars.extend("hi")
		protected, speakText, _speakSpelling = self.speak(CTRL_C)
		protected.assert_not_called()
		speakText.assert_not_called()

	def test_wordEchoLimitedToEditControlsOutsideAnEditControl(self):
		"""If the word will not be spoken, the protected state is never consulted."""
		self.setEcho(chars=TypingEcho.OFF, words=TypingEcho.EDIT_CONTROLS)
		speechModule._curWordChars.extend("hi")
		with (
			patch.object(speechModule.api, "isTypingProtected", return_value=False) as protected,
			patch.object(speechModule, "speakText") as speakText,
			patch.object(speechModule, "isFocusEditable", return_value=False),
		):
			speech.speakTypedCharacters(CTRL_C)
		protected.assert_not_called()
		speakText.assert_not_called()

	def test_characterEchoOffForANonControlCharacter(self):
		"""A letter still needs the protected state, for the word buffer only."""
		protected, _speakText, speakSpelling = self.speak("a")
		# Buffering a letter requires knowing whether to store the real character.
		protected.assert_called_once()
		speakSpelling.assert_not_called()


class TestProtectedStateStillHonoured(_SpeakTypedCharactersTestCase):
	"""Laziness must not weaken the protection of typed passwords."""

	def test_protectedLetterIsBufferedAsProtectedChar(self):
		self.speak("a", isProtected=True)
		self.assertEqual(speechModule._curWordChars, [speechModule.PROTECTED_CHAR])

	def test_unprotectedLetterIsBufferedVerbatim(self):
		self.speak("a", isProtected=False)
		self.assertEqual(speechModule._curWordChars, ["a"])

	def test_protectedWordIsNotSpoken(self):
		self.setEcho(chars=TypingEcho.OFF, words=TypingEcho.ALWAYS)
		speechModule._curWordChars.extend("hi")
		protected, speakText, _speakSpelling = self.speak(" ", isProtected=True)
		protected.assert_called_once()
		speakText.assert_not_called()

	def test_unprotectedWordIsSpoken(self):
		self.setEcho(chars=TypingEcho.OFF, words=TypingEcho.ALWAYS)
		speechModule._curWordChars.extend("hi")
		_protected, speakText, _speakSpelling = self.speak(" ", isProtected=False)
		speakText.assert_called_once_with("hi")

	def test_protectedCharacterIsSpokenAsProtectedChar(self):
		self.setEcho(chars=TypingEcho.ALWAYS, words=TypingEcho.OFF)
		_protected, _speakText, speakSpelling = self.speak("a", isProtected=True)
		speakSpelling.assert_called_once_with(speechModule.PROTECTED_CHAR)

	def test_unprotectedCharacterIsSpokenVerbatim(self):
		self.setEcho(chars=TypingEcho.ALWAYS, words=TypingEcho.OFF)
		_protected, _speakText, speakSpelling = self.speak("a", isProtected=False)
		speakSpelling.assert_called_once_with("a")


class TestProtectedStateResolvedAtMostOnce(_SpeakTypedCharactersTestCase):
	"""The caching must hold, so one character costs at most one fetch."""

	def test_letterWithBothEchoesOn(self):
		"""Buffering and speaking the same character must share one lookup."""
		self.setEcho(chars=TypingEcho.ALWAYS, words=TypingEcho.ALWAYS)
		protected, _speakText, speakSpelling = self.speak("a", isProtected=True)
		protected.assert_called_once()
		speakSpelling.assert_called_once_with(speechModule.PROTECTED_CHAR)

	def test_wordFlushAndCharacterEcho(self):
		"""Flushing a word and echoing the character must share one lookup."""
		self.setEcho(chars=TypingEcho.ALWAYS, words=TypingEcho.ALWAYS)
		speechModule._curWordChars.extend("hi")
		protected, speakText, speakSpelling = self.speak("!", isProtected=False)
		protected.assert_called_once()
		speakText.assert_called_once_with("hi")
		speakSpelling.assert_called_once_with("!")


class TestBufferHandlingUnchanged(_SpeakTypedCharactersTestCase):
	"""Behavior unrelated to the protected state must be preserved."""

	def test_backspaceRemovesLastBufferedCharacter(self):
		speechModule._curWordChars.extend("hi")
		self.speak("\b")
		self.assertEqual(speechModule._curWordChars, ["h"])

	def test_deleteCharacterReturnsEarly(self):
		speechModule._curWordChars.extend("hi")
		protected, speakText, speakSpelling = self.speak(DELETE)
		self.assertEqual(speechModule._curWordChars, ["h", "i"])
		protected.assert_not_called()
		speakText.assert_not_called()
		speakSpelling.assert_not_called()


if __name__ == "__main__":
	unittest.main()
