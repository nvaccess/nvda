#synthDrivers/espeak.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import _espeak
import Queue
import threading
import languageHandler
import synthDriverHandler
from logHandler import log

class SynthDriver(synthDriverHandler.SynthDriver):
	name = "espeak"
	description = "eSpeak"

	hasVoice=True
	hasPitch=True
	hasRate=True
	hasVolume=True
	hasVariant=True
	hasInflection=True

	@classmethod
	def check(cls):
		return True

	def __init__(self):
		_espeak.initialize()
		log.info("Using eSpeak version %s" % _espeak.info())
		lang=languageHandler.getLanguage()
		_espeak.setVoiceByLanguage(lang)
		self._variantDict=_espeak.getVariantDict()
		self.variant="max"
		self.rate=30
		self.pitch=40
		self.inflection=75

	def speakText(self,text,index=None):
		_espeak.speak(text, index=index)

	def cancel(self):
		_espeak.stop()

	def pause(self,switch):
		_espeak.pause(switch)

	def _get_rate(self):
		val=_espeak.getParameter(_espeak.espeakRATE,1)
		return self._paramToPercent(val,_espeak.minRate,_espeak.maxRate)

	def _set_rate(self,rate):
		val=self._percentToParam(rate, _espeak.minRate, _espeak.maxRate)
		_espeak.setParameter(_espeak.espeakRATE,val,0)

	def _get_pitch(self):
		val=_espeak.getParameter(_espeak.espeakPITCH,1)
		return self._paramToPercent(val,_espeak.minPitch,_espeak.maxPitch)

	def _set_pitch(self,pitch):
		val=self._percentToParam(pitch, _espeak.minPitch, _espeak.maxPitch)
		_espeak.setParameter(_espeak.espeakPITCH,val,0)

	def _get_inflection(self):
		val=_espeak.getParameter(_espeak.espeakRANGE,1)
		return self._paramToPercent(val,_espeak.minPitch,_espeak.maxPitch)

	def _set_inflection(self,val):
		val=self._percentToParam(val, _espeak.minPitch, _espeak.maxPitch)
		_espeak.setParameter(_espeak.espeakRANGE,val,0)

	def _get_volume(self):
		return _espeak.getParameter(_espeak.espeakVOLUME,1)

	def _set_volume(self,volume):
		_espeak.setParameter(_espeak.espeakVOLUME,volume,0)

	def _getAvailableVoices(self):
		return [synthDriverHandler.VoiceInfo(voice.identifier, "%s (%s)" % (voice.name, voice.identifier)) for voice in _espeak.getVoiceList()]

	def _get_voice(self):
		curVoice = _espeak.getCurrentVoice()
		if not curVoice:
			return ""
		return curVoice.identifier.split('+')[0]

	def _set_voice(self, identifier):
		if not identifier:
			return
		_espeak.setVoiceAndVariant(voice=identifier)

	def _get_lastIndex(self):
		return _espeak.lastIndex

	def terminate(self):
		_espeak.terminate()

	def _get_variant(self):
		return self._variant

	def _set_variant(self,val):
		self._variant = val if val in self._variantDict else "none"
		_espeak.setVoiceAndVariant(variant=val)

	def _getAvailableVariants(self):
		return [synthDriverHandler.VoiceInfo(ID, name) for ID, name in self._variantDict.iteritems()]
