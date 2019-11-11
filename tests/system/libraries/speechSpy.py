#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2018 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import synthDriverHandler
import extensionPoints
import speech

# inform those who want to know that there is new speech
post_speech = extensionPoints.Action()

class SynthDriver(synthDriverHandler.SynthDriver):
	"""A dummy synth driver used by system tests to get speech output
	"""
	name = "speechSpy"
	description = "System test speech spy"

	@classmethod
	def check(cls):
		return True

	supportedSettings = []
	supportedNotifications={synthDriverHandler.synthIndexReached,synthDriverHandler.synthDoneSpeaking}

	def speak(self, speechSequence):
		for item in speechSequence:
			if isinstance(item,speech.IndexCommand):
				synthDriverHandler.synthIndexReached.notify(synth=self,index=item.index)
		synthDriverHandler.synthDoneSpeaking.notify(synth=self)
		post_speech.notify(speechSequence=speechSequence)

	def cancel(self):
		pass
