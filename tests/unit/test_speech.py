# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021 NV Access Limited, Cyrille Bougot

"""Unit tests for the speech module.
"""

import unittest
from speech import _getSpellingSpeechAddCharMode, _getSpellingCharAddCapNotification
from speech.commands import EndUtteranceCommand, CharacterModeCommand, PitchCommand, BeepCommand


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
			'a',
		])
		output = _getSpellingCharAddCapNotification(
			speakCharAs='a',
			sayCapForCapitals=False,
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
