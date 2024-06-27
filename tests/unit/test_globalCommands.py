# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023 NV Access Limited, Łukasz Golonka
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Set of unit tests veryfying behavior of scripts defined in ``globalCommands``."""

import unittest

import config
import globalCommands
import inputCore
import speech


class _FakeInputGesture(inputCore.InputGesture):

	"""An input gesture which does nothing, but can be passed to scripts."""

	def _get_identifiers(self):
		"""Implemented just to satisfy base class requirements, where this is defined as abstract."""
		raise RuntimeError("Should not be required in tests.")


class SpeechModeSwitching(unittest.TestCase):

	"""Verifies that switching between speech modes with `NVDA+s` works.

	Ideally we will also ensure that name of the new speech mode is presented to the user,
	but we don't yet track calls to ``speech.speak``, so can't make any assertions on what has been spoken.
	"""

	@staticmethod
	def _getCurrSpeechMode() -> speech.SpeechMode:
		"""A convenience helper which retrieves currently set speech mode."""
		return speech.getState().speechMode

	@staticmethod
	def _setDisabledSpeechModes(modesToExclude: tuple[speech.SpeechMode, ...]) -> None:
		"""Disables given modes in the config."""
		disabledModes: list[int] = []
		for modeIndex, mode in enumerate(speech.SpeechMode):
			if mode in modesToExclude:
				disabledModes.append(modeIndex)
		if len(disabledModes) > len(speech.SpeechMode) - 2:
			raise RuntimeError("At least two modes have to be enabled.")
		config.conf["speech"]["excludedSpeechModes"] = disabledModes

	def setUp(self) -> None:
		self._origSpeechMode = speech.getState().speechMode
		self._defaultDisabledSpeechModes = config.conf["speech"]["excludedSpeechModes"]
		# The new speech mode is shown in Braille, but displaying messages requires WX to be initialized.
		# Just disable showing messages for these tests.
		self._oldShowBraileMessagesVal = config.conf["braille"]["showMessages"]
		config.conf["braille"]["showMessages"] = 0  # Disabled

	def tearDown(self) -> None:
		config.conf["speech"]["excludedSpeechModes"] = self._defaultDisabledSpeechModes
		speech.setSpeechMode(self._origSpeechMode)
		config.conf["braille"]["showMessages"] = self._oldShowBraileMessagesVal

	@staticmethod
	def _executeSpeechModeCycleScript():
		globalCommands.commands.script_speechMode(_FakeInputGesture())

	def test_cyclesThroughAllModesByDefault(self):
		"""By default keyboard command should switch between all available speech modes."""
		seenModes = set()
		for __ in range(len(speech.SpeechMode)):
			self._executeSpeechModeCycleScript()
			seenModes.add(self._getCurrSpeechMode())
		self.assertEqual(seenModes, set(speech.SpeechMode))
		# Just to make sure, verify that we returned to the mode set initially.
		self.assertEqual(self._getCurrSpeechMode(), self._origSpeechMode)

	def test_nextModeIsUsed(self):
		"""Next speech mode is picked when the currently selected is not the last one."""
		# Verify that expected mode is set initially.
		self.assertEqual(self._getCurrSpeechMode(), speech.SpeechMode.talk)
		self._executeSpeechModeCycleScript()
		self.assertEqual(self._getCurrSpeechMode(), speech.SpeechMode.onDemand)

	def test_cyclingWrapsNoMoreModes(self):
		"""When the selected speech mode is last on the list, the next press should switch to a first one."""
		speech.setSpeechMode(speech.SpeechMode.onDemand)
		self._executeSpeechModeCycleScript()
		self.assertEqual(self._getCurrSpeechMode(), speech.SpeechMode.off)

	def test_nextModePickedWhenEnabled(self):
		"""When the next mode in the list is enabled, pressing the command once should switch to it."""
		self._setDisabledSpeechModes((speech.SpeechMode.off, speech.SpeechMode.beeps))
		self._executeSpeechModeCycleScript()
		self.assertEqual(self._getCurrSpeechMode(), speech.SpeechMode.onDemand)

	def test_nextModeDisabledMoreModesInTheList(self):
		"""Next mode is disabled, yet there are more modes in the list, so no need to wrap to the first one."""
		self._setDisabledSpeechModes((speech.SpeechMode.beeps,))
		speech.setSpeechMode(speech.SpeechMode.off)
		self._executeSpeechModeCycleScript()
		self.assertEqual(self._getCurrSpeechMode(), speech.SpeechMode.talk)

	def test_nextModeDisabledNoMoreModes(self):
		"""When the next mode is disabled, switching wraps to the first mode."""
		self._setDisabledSpeechModes((speech.SpeechMode.onDemand,))
		self._executeSpeechModeCycleScript()
		self.assertEqual(self._getCurrSpeechMode(), speech.SpeechMode.off)

	def test_nextModesDisabledFirstEnabledNotAtTheBeginning(self):
		"""Script has to wrap, mode at the beginning of the list is disabled, first enabled one is picked."""
		self._setDisabledSpeechModes((speech.SpeechMode.off, speech.SpeechMode.onDemand))
		self._executeSpeechModeCycleScript()
		self.assertEqual(self._getCurrSpeechMode(), speech.SpeechMode.beeps)

	def test_onlyEnabledModesAvailableForSwitching(self):
		"""Execute script multiple times and make sure we never switched to one of the disabled modes."""
		self._setDisabledSpeechModes((speech.SpeechMode.off, speech.SpeechMode.onDemand))
		seenModes = set()
		for __ in range(30):  # Chosen arbitrarily, so that script wraps multiple times.
			self._executeSpeechModeCycleScript()
			seenModes.add(self._getCurrSpeechMode())
		self.assertEqual(seenModes, {speech.SpeechMode.talk, speech.SpeechMode.beeps})
