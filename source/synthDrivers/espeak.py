# -*- coding: UTF-8 -*-
#synthDrivers/espeak.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2007-2019 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Leonard de Ruijter
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
from collections import OrderedDict
from . import _espeak
import threading
import languageHandler
from synthDriverHandler import SynthDriver, VoiceInfo, synthIndexReached, synthDoneSpeaking
import speech
from logHandler import log

from speech.commands import (
	IndexCommand,
	CharacterModeCommand,
	LangChangeCommand,
	BreakCommand,
	PitchCommand,
	RateCommand,
	VolumeCommand,
	PhonemeCommand,
)

class SynthDriver(SynthDriver):
	name = "espeak"
	description = "eSpeak NG"

	supportedSettings=(
		SynthDriver.VoiceSetting(),
		SynthDriver.VariantSetting(),
		SynthDriver.RateSetting(),
		SynthDriver.RateBoostSetting(),
		SynthDriver.PitchSetting(),
		SynthDriver.InflectionSetting(),
		SynthDriver.VolumeSetting(),
	)
	supportedCommands = {
		IndexCommand,
		CharacterModeCommand,
		LangChangeCommand,
		BreakCommand,
		PitchCommand,
		RateCommand,
		VolumeCommand,
		PhonemeCommand,
	}
	supportedNotifications = {synthIndexReached, synthDoneSpeaking}

	@classmethod
	def check(cls):
		return True

	def __init__(self):
		_espeak.initialize(self._onIndexReached)
		log.info("Using eSpeak NG version %s" % _espeak.info())
		lang=languageHandler.getLanguage()
		_espeak.setVoiceByLanguage(lang)
		self._language=lang
		self._variantDict=_espeak.getVariantDict()
		self.variant="max"
		self.rate=30
		self.pitch=40
		self.inflection=75

	def _get_language(self):
		return self._language

	PROSODY_ATTRS = {
		PitchCommand: "pitch",
		VolumeCommand: "volume",
		RateCommand: "rate",
	}

	IPA_TO_ESPEAK = {
		u"θ": u"T",
		u"s": u"s",
		u"ˈ": u"'",
	}

	def _processText(self, text):
		# We need to make several replacements.
		return text.translate({
			0x1: None, # used for embedded commands
			0x3C: u"&lt;", # <: because of XML
			0x3E: u"&gt;", # >: because of XML
			0x5B: u" [", # [: [[ indicates phonemes
		})

	def speak(self,speechSequence):
		defaultLanguage=self._language
		textList=[]
		langChanged=False
		prosody={}
		# We output malformed XML, as we might close an outer tag after opening an inner one; e.g.
		# <voice><prosody></voice></prosody>.
		# However, eSpeak doesn't seem to mind.
		for item in speechSequence:
			if isinstance(item,str):
				textList.append(self._processText(item))
			elif isinstance(item, IndexCommand):
				textList.append("<mark name=\"%d\" />"%item.index)
			elif isinstance(item, CharacterModeCommand):
				textList.append("<say-as interpret-as=\"characters\">" if item.state else "</say-as>")
			elif isinstance(item, LangChangeCommand):
				if langChanged:
					textList.append("</voice>")
				textList.append("<voice xml:lang=\"%s\">"%(item.lang if item.lang else defaultLanguage).replace('_','-'))
				langChanged=True
			elif isinstance(item, BreakCommand):
				textList.append('<break time="%dms" />' % item.time)
			elif type(item) in self.PROSODY_ATTRS:
				if prosody:
					# Close previous prosody tag.
					textList.append("</prosody>")
				attr=self.PROSODY_ATTRS[type(item)]
				if item.multiplier==1:
					# Returning to normal.
					try:
						del prosody[attr]
					except KeyError:
						pass
				else:
					prosody[attr]=int(item.multiplier* 100)
				if not prosody:
					continue
				textList.append("<prosody")
				for attr,val in prosody.items():
					textList.append(' %s="%d%%"'%(attr,val))
				textList.append(">")
			elif isinstance(item, PhonemeCommand):
				# We can't use str.translate because we want to reject unknown characters.
				try:
					phonemes="".join([self.IPA_TO_ESPEAK[char] for char in item.ipa])
					# There needs to be a space after the phoneme command.
					# Otherwise, eSpeak will announce a subsequent SSML tag instead of processing it.
					textList.append(u"[[%s]] "%phonemes)
				except KeyError:
					log.debugWarning("Unknown character in IPA string: %s"%item.ipa)
					if item.text:
						textList.append(self._processText(item.text))
			else:
				log.error("Unknown speech: %s"%item)
		# Close any open tags.
		if langChanged:
			textList.append("</voice>")
		if prosody:
			textList.append("</prosody>")
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
			l=_espeak.decodeEspeakString(v.languages[1:])
			# #7167: Some languages names contain unicode characters EG: Norwegian Bokmål
			name=_espeak.decodeEspeakString(v.name)
			# #5783: For backwards compatibility, voice identifies should always be lowercase
			identifier=os.path.basename(_espeak.decodeEspeakString(v.identifier)).lower()
			voices[identifier]=VoiceInfo(identifier,name,l)
		return voices

	def _get_voice(self):
		curVoice=getattr(self,'_voice',None)
		if curVoice: return curVoice
		curVoice = _espeak.getCurrentVoice()
		if not curVoice:
			return ""
		# #5783: For backwards compatibility, voice identifies should always be lowercase
		return _espeak.decodeEspeakString(curVoice.identifier).split('+')[0].lower()

	def _set_voice(self, identifier):
		if not identifier:
			return
		# #5783: For backwards compatibility, voice identifies should always be lowercase
		identifier=identifier.lower()
		if "\\" in identifier:
			identifier=os.path.basename(identifier)
		self._voice=identifier
		try:
			_espeak.setVoiceAndVariant(voice=identifier,variant=self._variant)
		except:
			self._voice=None
			raise
		self._language=super(SynthDriver,self).language

	def _onIndexReached(self, index):
		if index is not None:
			synthIndexReached.notify(synth=self, index=index)
		else:
			synthDoneSpeaking.notify(synth=self)

	def terminate(self):
		_espeak.terminate()

	def _get_variant(self):
		return self._variant

	def _set_variant(self,val):
		self._variant = val if val in self._variantDict else "max"
		_espeak.setVoiceAndVariant(variant=self._variant)

	def _getAvailableVariants(self):
		return OrderedDict((ID,VoiceInfo(ID, name)) for ID, name in self._variantDict.items())
