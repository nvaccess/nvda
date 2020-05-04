# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
This module is copied to the scratchPad/synthDrivers folder and set as the synthesizer to capture speech
output during system tests.
Note: The name of this module must match the name of the synth driver, and the configured synthesizer
in the `tests/system/nvdaSettingsFiles/*.ini` files.
"""

import synthDriverHandler
import extensionPoints
import speech

# inform those who want to know that there is new speech
post_speech = extensionPoints.Action()


class SpeechSpySynthDriver(synthDriverHandler.SynthDriver):
	"""A synth driver configured during system tests to capture speech output
	"""
	name = "SpeechSpySynthDriver"  # Name must match configuration files and module.
	description = "System test speech spy"

	@classmethod
	def check(cls):
		return True

	supportedSettings = []
	supportedNotifications = {
		synthDriverHandler.synthIndexReached,
		synthDriverHandler.synthDoneSpeaking
	}

	def speak(self, speechSequence):
		for item in speechSequence:
			if isinstance(item, speech.IndexCommand):
				synthDriverHandler.synthIndexReached.notify(synth=self, index=item.index)
		synthDriverHandler.synthDoneSpeaking.notify(synth=self)
		post_speech.notify(speechSequence=speechSequence)

	def cancel(self):
		pass


SynthDriver = SpeechSpySynthDriver
