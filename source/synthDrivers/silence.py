#synthDrivers/silence.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2014 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import synthDriverHandler
import speech

class SynthDriver(synthDriverHandler.SynthDriver):
	"""A dummy synth driver used to disable speech in NVDA.
	"""
	name="silence"
	# Translators: Description for a speech synthesizer.
	description=_("No speech")

	@classmethod
	def check(cls):
		return True

	supportedSettings=[]

	def speak(self, speechSequence):
		self.lastIndex = None
		for item in speechSequence:
			if isinstance(item, speech.IndexCommand):
				self.lastIndex = item.index

	def cancel(self):
		self.lastIndex = None
