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
from logHandler import log

import synthDriverHandler
import extensionPoints
from speech.commands import IndexCommand

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
		log.debug(f"Start of Speak: {speechSequence}")
		for item in speechSequence:
			if isinstance(item, IndexCommand):
				log.debug(f"index reached: {item.index}")
				synthDriverHandler.synthIndexReached.notify(synth=self, index=item.index)
		log.debug("done speaking")
		synthDriverHandler.synthDoneSpeaking.notify(synth=self)
		log.debug("post_speech notify start")
		post_speech.notify(speechSequence=speechSequence)
		log.debug("post_speech notify complete")

	def cancel(self):
		pass


SynthDriver = SpeechSpySynthDriver
