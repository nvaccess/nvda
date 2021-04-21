# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021 NV Access Limited, Cyrille Bougot

"""Unit tests for the speech module.
"""
import unittest
import gettext
import typing
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


class Translation_Fake(gettext.NullTranslations):
	originalTranslationFunction: gettext.NullTranslations
	translationResults: typing.Dict[str, str]

	def __init__(self, originalTranslationFunction: gettext.NullTranslations):
		self.originalTranslationFunction = originalTranslationFunction
		self.translationResults = {}
		super().__init__()

	def gettext(self, msg: str) -> str:
		if msg in self.translationResults:
			return self.translationResults[msg]
		return self.originalTranslationFunction.gettext(msg)


class Test_getSpellingCharAddCapNotification(unittest.TestCase):
	translationsFake: Translation_Fake

	@classmethod
	def setUpClass(cls):
		from . import translations as originalTranslationClass
		cls.translationsFake = Translation_Fake(originalTranslationClass)
		cls.translationsFake.install()

	@classmethod
	def tearDownClass(cls):
		cls.translationsFake.originalTranslationFunction.install()

	def tearDown(self) -> None:
		self.translationsFake.translationResults.clear()
	
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

	def test_capNotificationsWithPlaceHolderBefore(self):
		self.translationsFake.translationResults["cap %s"] = "%s cap"
		expected = repr(['A', ' cap', ])  # for English this would be "cap A"
		output = _getSpellingCharAddCapNotification(
			speakCharAs='A',
			sayCapForCapitals=True,
			capPitchChange=0,
			beepForCapitals=False,
		)
		self.assertEqual(repr(list(output)), expected)

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
		# Restore default value
		config.conf['speech']['autoLanguageSwitching'] = config.conf.getConfigValidation(
			['speech', 'autoLanguageSwitching']
		).default
	
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
			sayCapForCapitals=True,
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
