# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021 NV Access Limited, Cyrille Bougot

"""Unit tests for the speech module.
"""

import unittest
import config
from speech import (
	_getSpellingSpeechAddCharMode,
	_getSpellingCharAddCapNotification,
	_getSpellingSpeechWithoutCharMode,
)
from speech.commands import (
	EndUtteranceCommand,
	CharacterModeCommand,
	PitchCommand,
	BeepCommand,
	LangChangeCommand
)


class Test_getSpellingSpeechAddCharMode(unittest.TestCase):
	def test_symbolNamesAtStartAndEnd(self):
		# Spelling ¡hola!
		seq = (c for c in [
			'inverted exclamation point',
			EndUtteranceCommand(),
			'h',
			EndUtteranceCommand(),
			'o',
			EndUtteranceCommand(),
			'l',
			EndUtteranceCommand(),
			'a',
			EndUtteranceCommand(),
			'bang',
			EndUtteranceCommand()
		])
		expected = repr([
			'inverted exclamation point',
			EndUtteranceCommand(),
			CharacterModeCommand(True),
			'h',
			EndUtteranceCommand(),
			'o',
			EndUtteranceCommand(),
			'l',
			EndUtteranceCommand(),
			'a',
			EndUtteranceCommand(),
			CharacterModeCommand(False),
			'bang',
			EndUtteranceCommand()
		])
		output = _getSpellingSpeechAddCharMode(seq)
		self.assertEqual(repr(list(output)), expected)

	def test_manySymbolNamesInARow(self):
		# Spelling a...b
		seq = (c for c in [
			'a',
			EndUtteranceCommand(),
			'dot',
			EndUtteranceCommand(),
			'dot',
			EndUtteranceCommand(),
			'dot',
			EndUtteranceCommand(),
			'b',
			EndUtteranceCommand()
		])
		expected = repr([
			CharacterModeCommand(True),
			'a',
			EndUtteranceCommand(),
			CharacterModeCommand(False),
			'dot',
			EndUtteranceCommand(),
			'dot',
			EndUtteranceCommand(),
			'dot',
			EndUtteranceCommand(),
			CharacterModeCommand(True),
			'b',
			EndUtteranceCommand()
		])
		output = _getSpellingSpeechAddCharMode(seq)
		self.assertEqual(repr(list(output)), expected)


class Test_getSpellingCharAddCapNotification(unittest.TestCase):
	def test_noNotifications(self):
		expected = repr([
			'A',
		])
		output = _getSpellingCharAddCapNotification(
			speakCharAs='A',
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_pitchNotifications(self):
		expected = repr([
			PitchCommand(offset=30),
			'A',
			PitchCommand()
		])
		output = _getSpellingCharAddCapNotification(
			speakCharAs='A',
			sayCapForCapitals=False,
			capPitchChange=30,
			beepForCapitals=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_beepNotifications(self):
		expected = repr([
			BeepCommand(2000, 50, left=50, right=50),
			'A',
		])
		output = _getSpellingCharAddCapNotification(
			speakCharAs='A',
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=True,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_capNotifications(self):
		expected = repr([
			'cap ',
			'A',
		])
		output = _getSpellingCharAddCapNotification(
			speakCharAs='A',
			sayCapForCapitals=True,
			capPitchChange=0,
			beepForCapitals=False,
		)
		self.assertEqual(repr(list(output)), expected)

	@unittest.skip("Need to implement patching of _ function.")
	def test_capNotificationsWithPlaceHolderAfter(self):
		global _
		originalTranslationFunction = _
		
		def fakeTranslationFunction(s):
			if s == 'cap %s':
				return '%s cap'
			return s
		try:
			expected = repr([
				'A',
				' cap',
			])
			output = _getSpellingCharAddCapNotification(
				speakCharAs='A',
				sayCapForCapitals=True,
				capPitchChange=0,
				beepForCapitals=False,
			)
			self.assertEqual(repr(list(output)), expected)
		finally:
			_ = originalTranslationFunction

	def test_allNotifications(self):
		expected = repr([
			PitchCommand(offset=30),
			BeepCommand(2000, 50, left=50, right=50),
			'cap ',
			'A',
			PitchCommand()
		])
		output = _getSpellingCharAddCapNotification(
			speakCharAs='A',
			sayCapForCapitals=True,
			capPitchChange=30,
			beepForCapitals=True,
		)
		self.assertEqual(repr(list(output)), expected)


class Test_getSpellingSpeechWithoutCharMode(unittest.TestCase):

	def setUp(self):
		config.conf['speech']['autoLanguageSwitching'] = False

	def tearDown(self):
		config.conf['speech']['autoLanguageSwitching'] = True  # Default value
	
	def test_simpleSpelling(self):
		expected = repr([
			'a',
			EndUtteranceCommand(),
			'b',
			EndUtteranceCommand(),
			'c',
			EndUtteranceCommand(),
		])
		output = _getSpellingSpeechWithoutCharMode(
			text='abc',
			locale=None,
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_cap(self):
		expected = repr([
			PitchCommand(offset=30),
			BeepCommand(2000, 50, left=50, right=50),
			'cap ',
			'A',
			PitchCommand(),
			EndUtteranceCommand(),
		])
		output = _getSpellingSpeechWithoutCharMode(
			text='A',
			locale=None,
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=30,
			beepForCapitals=True,
		)
		self.assertEqual(repr(list(output)), expected)
	
	def test_characterMode(self):
		expected = repr([
			'Alfa',
			EndUtteranceCommand(),
		])
		output = _getSpellingSpeechWithoutCharMode(
			text='a',
			locale='en',
			useCharacterDescriptions=True,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_blank(self):
		expected = repr([
			'blank',
			EndUtteranceCommand(),
		])
		output = _getSpellingSpeechWithoutCharMode(
			text='',
			locale=None,
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_onlySpaces(self):
		expected = repr([
			'space',
			EndUtteranceCommand(),
			'tab',
			EndUtteranceCommand(),
		])
		output = _getSpellingSpeechWithoutCharMode(
			text=' \t',
			locale=None,
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_trimRightSpace(self):
		expected = repr([
			'a',
			EndUtteranceCommand(),
		])
		output = _getSpellingSpeechWithoutCharMode(
			text='a   ',
			locale=None,
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_symbol(self):
		expected = repr([
			'bang',
			EndUtteranceCommand(),
		])
		output = _getSpellingSpeechWithoutCharMode(
			text='!',
			locale=None,
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_languageDetection(self):
		config.conf['speech']['autoLanguageSwitching'] = True
		expected = repr([
			LangChangeCommand('fr_FR'),
			'a',
			EndUtteranceCommand(),
		])
		output = _getSpellingSpeechWithoutCharMode(
			text='a',
			locale='fr_FR',
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
		)
		self.assertEqual(repr(list(output)), expected)
