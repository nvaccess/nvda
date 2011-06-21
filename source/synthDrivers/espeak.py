#synthDrivers/espeak.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from collections import OrderedDict
import _espeak
import Queue
import threading
import languageHandler
from synthDriverHandler import SynthDriver,VoiceInfo,BooleanSynthSetting
import speech
from logHandler import log

class SynthDriver(SynthDriver):
	name = "espeak"
	description = "eSpeak"

	supportedSettings=(
		SynthDriver.VoiceSetting(),
		SynthDriver.VariantSetting(),
		SynthDriver.RateSetting(),
		# Translators: This is the name of the rate boost voice toggle
		# which further increases the speaking rate when enabled.
		BooleanSynthSetting("rateBoost",_("Rate boos&t")),
		SynthDriver.PitchSetting(),
		SynthDriver.InflectionSetting(),
		SynthDriver.VolumeSetting(),
	)

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

	def speak(self,speechSequence):
		textList=[]
		for item in speechSequence:
			if isinstance(item,basestring):
				s=unicode(item)
				# Replace \01, as this is used for embedded commands.
				#Also replace < and > as espeak handles xml
				s.translate({ord(u'\01'):None,ord(u'<'):u'&lt;',ord(u'>'):u'&gt;'})
				textList.append(s)
			elif isinstance(item,speech.IndexCommand):
				textList.append("<mark name=\"%d\" />"%item.index)
			elif isinstance(item,speech.CharacterModeCommand):
				textList.append("<say-as type=\"spell-out\">" if item.state else "</say-as>")
			elif isinstance(item,speech.SpeechCommand):
				log.debugWarning("Unsupported speech command: %s"%item)
			else:
				log.error("Unknown speech: %s"%item)
		text=u"".join(textList)
		_espeak.speak(text)

	def cancel(self):
		_espeak.stop()

	def pause(self,switch):
		_espeak.pause(switch)

	_rateBoost = False
	RATE_BOOST_MULTIPLIER = 3

	def _get_rateBoost(self):
		return self._rateBoost

	def _set_rateBoost(self, enable):
		if enable == self._rateBoost:
			return
		rate = self.rate
		self._rateBoost = enable
		self.rate = rate

	def _get_rate(self):
		val=_espeak.getParameter(_espeak.espeakRATE,1)
		if self._rateBoost:
			val=int(val/self.RATE_BOOST_MULTIPLIER)
		return self._paramToPercent(val,_espeak.minRate,_espeak.maxRate)

	def _set_rate(self,rate):
		val=self._percentToParam(rate, _espeak.minRate, _espeak.maxRate)
		if self._rateBoost:
			val=int(val*self.RATE_BOOST_MULTIPLIER)
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
		voices=OrderedDict()
		for v in _espeak.getVoiceList():
			l=v.languages[1:].split('-')[0:2]
			if len(l)==2:
				language="%s_%s"%(l[0],l[1].upper())
			else:
				language=l[0]
			voices[v.identifier]=VoiceInfo(v.identifier,v.name,language)
		return voices

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
		self._variant = val if val in self._variantDict else "max"
		_espeak.setVoiceAndVariant(variant=self._variant)

	def _getAvailableVariants(self):
		return OrderedDict((ID,VoiceInfo(ID, name)) for ID, name in self._variantDict.iteritems())
