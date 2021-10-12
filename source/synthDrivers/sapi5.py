# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2021 NV Access Limited, Peter Vágner, Aleksey Sadovoy
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import Callable
import threading
from enum import IntEnum
import locale
from collections import OrderedDict
from ctypes import *
import comtypes.client
from comtypes import COMError
import winreg
import audioDucking
from synthDriverHandler import SynthDriver, VoiceInfo, synthIndexReached, synthDoneSpeaking
import config
import nvwave
from logHandler import log
import weakref

from speech.commands import (
	IndexCommand,
	CharacterModeCommand,
	LangChangeCommand,
	BreakCommand,
	PitchCommand,
	RateCommand,
	VolumeCommand,
	PhonemeCommand,
	SpeechCommand,
)


class SPAudioState(IntEnum):
	CLOSED = 0
	STOP = 1
	PAUSE = 2
	RUN = 3


class SpeechVoiceSpeakFlags(IntEnum):
	# https://docs.microsoft.com/en-us/previous-versions/windows/desktop/ms720892(v=vs.85)
	FlagsAsync = 1
	PurgeBeforeSpeak = 2
	IsXML = 8


class SpeechVoiceEvents(IntEnum):
	# https://msdn.microsoft.com/en-us/previous-versions/windows/desktop/ms720886(v=vs.85)
	EndInputStream = 4
	Bookmark = 16


class AudioDucker(audioDucking.AudioDucker):
	_speechDucked = False
	_lock = threading.Lock()

	def __init__(self, speechEndWaitFunction: Callable[[int], bool]):
		super().__init__()
		self._speechEndWaitFunction = speechEndWaitFunction

	def enable(self):
		if not audioDucking.isAudioDuckingSupported():
			return
		if audioDucking._isDebug():
			log.debug("Starting audio duck for SAPI5")

		with AudioDucker._lock:
			if AudioDucker._speechDucked:
				log.debug("audio already ducked for SAPI5")
				return
			AudioDucker._speechDucked = True

		# The synthDriver will wait until all speech is finished to end ducking
		audioDucking._setDuckingState(True)
		_thread = threading.Thread(target=AudioDucker._disable, args=(self._speechEndWaitFunction,))
		_thread.start()
		return True

	def disable(self):
		AudioDucker._disable(self._speechEndWaitFunction)

	@staticmethod
	def _disable(speechEndWaitFunction: Callable[[int], bool]):
		if not audioDucking.isAudioDuckingSupported():
			return
		if audioDucking._isDebug():
			log.debug("Waiting for speech to end to end audio duck for SAPI5")

		ms_timeout = 5 * 60 * 1000  # 5 min timeout
		# WaitUntilDone waits until all speech is finished
		if not speechEndWaitFunction(ms_timeout) and audioDucking._isDebug():
			log.debugWarning("Couldn't wait for speech to finish")

		audioDucking._setDuckingState(False)
		with AudioDucker._lock:
			AudioDucker._speechDucked = False
		return True


class SapiSink(object):
	"""Handles SAPI event notifications.
	See https://msdn.microsoft.com/en-us/library/ms723587(v=vs.85).aspx
	"""

	def __init__(self, synthRef: weakref.ReferenceType):
		self.synthRef = synthRef

	def Bookmark(self, streamNum, pos, bookmark, bookmarkId):
		synth = self.synthRef()
		if synth is None:
			log.debugWarning("Called Bookmark method on SapiSink while driver is dead")
			return
		synthIndexReached.notify(synth=synth, index=bookmarkId)

	def EndStream(self, streamNum, pos):
		synth = self.synthRef()
		if synth is None:
			log.debugWarning("Called Bookmark method on EndStream while driver is dead")
			return
		synthDoneSpeaking.notify(synth=synth)


class SynthDriver(SynthDriver):
	supportedSettings=(SynthDriver.VoiceSetting(),SynthDriver.RateSetting(),SynthDriver.PitchSetting(),SynthDriver.VolumeSetting())
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

	COM_CLASS = "SAPI.SPVoice"

	name="sapi5"
	description="Microsoft Speech API version 5"

	@classmethod
	def check(cls):
		try:
			r=winreg.OpenKey(winreg.HKEY_CLASSES_ROOT,cls.COM_CLASS)
			r.Close()
			return True
		except:
			return False

	ttsAudioStream=None #: Holds the ISPAudio interface for the current voice, to aid in stopping and pausing audio

	def __init__(self,_defaultVoiceToken=None):
		"""
		@param _defaultVoiceToken: an optional sapi voice token which should be used as the default voice (only useful for subclasses)
		@type _defaultVoiceToken: ISpeechObjectToken
		"""
		self._pitch=50
		self._initTts(_defaultVoiceToken)
		self._audioDucker = AudioDucker(self.tts.WaitUntilDone)

	def terminate(self):
		self._eventsConnection = None
		self.tts = None

	def _getAvailableVoices(self):
		voices=OrderedDict()
		v=self._getVoiceTokens()
		# #2629: Iterating uses IEnumVARIANT and GetBestInterface doesn't work on tokens returned by some token enumerators.
		# Therefore, fetch the items by index, as that method explicitly returns the correct interface.
		for i in range(len(v)):
			try:
				ID=v[i].Id
				name=v[i].GetDescription()
				try:
					language=locale.windows_locale[int(v[i].getattribute('language').split(';')[0],16)]
				except KeyError:
					language=None
			except COMError:
				log.warning("Could not get the voice info. Skipping...")
			voices[ID]=VoiceInfo(ID,name,language)
		return voices

	def _getVoiceTokens(self):
		"""Provides a collection of sapi5 voice tokens. Can be overridden by subclasses if tokens should be looked for in some other registry location."""
		return self.tts.getVoices()

	def _get_rate(self):
		return (self.tts.rate*5)+50

	def _get_pitch(self):
		return self._pitch

	def _get_volume(self):
		return self.tts.volume

	def _get_voice(self):
		return self.tts.voice.Id
 
	def _get_lastIndex(self):
		bookmark=self.tts.status.LastBookmark
		if bookmark!="" and bookmark is not None:
			return int(bookmark)
		else:
			return None

	def _percentToRate(self, percent):
		return (percent - 50) // 5

	def _set_rate(self,rate):
		self.tts.Rate = self._percentToRate(rate)

	def _set_pitch(self,value):
		#pitch is really controled with xml around speak commands
		self._pitch=value

	def _set_volume(self,value):
		self.tts.Volume = value

	def _initTts(self, voice=None):
		self.tts=comtypes.client.CreateObject(self.COM_CLASS)
		if voice:
			# #749: It seems that SAPI 5 doesn't reset the audio parameters when the voice is changed,
			# but only when the audio output is changed.
			# Therefore, set the voice before setting the audio output.
			# Otherwise, we will get poor speech quality in some cases.
			self.tts.voice = voice
		outputDeviceID=nvwave.outputDeviceNameToID(config.conf["speech"]["outputDevice"], True)
		if outputDeviceID>=0:
			self.tts.audioOutput=self.tts.getAudioOutputs()[outputDeviceID]
		self._eventsConnection = comtypes.client.GetEvents(self.tts, SapiSink(weakref.ref(self)))
		self.tts.EventInterests = SpeechVoiceEvents.Bookmark | SpeechVoiceEvents.EndInputStream
		from comInterfaces.SpeechLib import ISpAudio
		try:
			self.ttsAudioStream=self.tts.audioOutputStream.QueryInterface(ISpAudio)
		except COMError:
			log.debugWarning("SAPI5 voice does not support ISPAudio") 
			self.ttsAudioStream=None

	def _set_voice(self,value):
		tokens = self._getVoiceTokens()
		# #2629: Iterating uses IEnumVARIANT and GetBestInterface doesn't work on tokens returned by some token enumerators.
		# Therefore, fetch the items by index, as that method explicitly returns the correct interface.
		for i in range(len(tokens)):
			voice=tokens[i]
			if value==voice.Id:
				break
		else:
			# Voice not found.
			return
		self._initTts(voice=voice)

	def _percentToPitch(self, percent):
		return percent // 2 - 25

	IPA_TO_SAPI = {
		u"θ": u"th",
		u"s": u"s",
	}
	def _convertPhoneme(self, ipa):
		# We only know about US English phonemes.
		# Rather than just ignoring unknown phonemes, SAPI throws an exception.
		# Therefore, don't bother with any other language.
		if self.tts.voice.GetAttribute("language") != "409":
			raise LookupError("No data for this language")
		out = []
		outAfter = None
		for ipaChar in ipa:
			if ipaChar == u"ˈ":
				outAfter = u"1"
				continue
			out.append(self.IPA_TO_SAPI[ipaChar])
			if outAfter:
				out.append(outAfter)
				outAfter = None
		if outAfter:
			out.append(outAfter)
		return u" ".join(out)

	def speak(self, speechSequence):
		textList = []

		# NVDA SpeechCommands are linear, but XML is hierarchical.
		# Therefore, we track values for non-empty tags.
		# When a tag changes, we close all previously opened tags and open new ones.
		tags = {}
		# We have to use something mutable here because it needs to be changed by the inner function.
		tagsChanged = [True]
		openedTags = []
		def outputTags():
			if not tagsChanged[0]:
				return
			for tag in reversed(openedTags):
				textList.append("</%s>" % tag)
			del openedTags[:]
			for tag, attrs in tags.items():
				textList.append("<%s" % tag)
				for attr, val in attrs.items():
					textList.append(' %s="%s"' % (attr, val))
				textList.append(">")
				openedTags.append(tag)
			tagsChanged[0] = False

		pitch = self._pitch
		# Pitch must always be specified in the markup.
		tags["pitch"] = {"absmiddle": self._percentToPitch(pitch)}
		rate = self.rate
		volume = self.volume

		for item in speechSequence:
			if isinstance(item, str):
				outputTags()
				textList.append(item.replace("<", "&lt;"))
			elif isinstance(item, IndexCommand):
				textList.append('<Bookmark Mark="%d" />' % item.index)
			elif isinstance(item, CharacterModeCommand):
				if item.state:
					tags["spell"] = {}
				else:
					try:
						del tags["spell"]
					except KeyError:
						pass
				tagsChanged[0] = True
			elif isinstance(item, BreakCommand):
				textList.append('<silence msec="%d" />' % item.time)
			elif isinstance(item, PitchCommand):
				tags["pitch"] = {"absmiddle": self._percentToPitch(int(pitch * item.multiplier))}
				tagsChanged[0] = True
			elif isinstance(item, VolumeCommand):
				if item.multiplier == 1:
					try:
						del tags["volume"]
					except KeyError:
						pass
				else:
					tags["volume"] = {"level": int(volume * item.multiplier)}
				tagsChanged[0] = True
			elif isinstance(item, RateCommand):
				if item.multiplier == 1:
					try:
						del tags["rate"]
					except KeyError:
						pass
				else:
					tags["rate"] = {"absspeed": self._percentToRate(int(rate * item.multiplier))}
				tagsChanged[0] = True
			elif isinstance(item, PhonemeCommand):
				try:
					textList.append(u'<pron sym="%s">%s</pron>'
						% (self._convertPhoneme(item.ipa), item.text or u""))
				except LookupError:
					log.debugWarning("Couldn't convert character in IPA string: %s" % item.ipa)
					if item.text:
						textList.append(item.text)
			elif isinstance(item, SpeechCommand):
				log.debugWarning("Unsupported speech command: %s" % item)
			else:
				log.error("Unknown speech: %s" % item)
		# Close any tags that are still open.
		tags.clear()
		tagsChanged[0] = True
		outputTags()

		text = "".join(textList)
		flags = SpeechVoiceSpeakFlags.IsXML | SpeechVoiceSpeakFlags.FlagsAsync
		self._audioDucker.enable()
		self.tts.Speak(text, flags)

	def cancel(self):
		# SAPI5's default means of stopping speech can sometimes lag at end of speech, especially with Win8 / Win 10 Microsoft Voices.
		# Therefore  instruct the underlying audio interface to stop first, before interupting and purging any remaining speech.
		if self.ttsAudioStream:
			self.ttsAudioStream.setState(SPAudioState.STOP, 0)
		self.tts.Speak(None, 1 | SpeechVoiceSpeakFlags.PurgeBeforeSpeak)
		self._audioDucker.disable()

	def pause(self, switch: bool):
		# SAPI5's default means of pausing in most cases is either extremely slow
		# (e.g. takes more than half a second) or does not work at all.
		# Therefore instruct the underlying audio interface to pause instead.
		if self.ttsAudioStream:
			if switch:
				self.ttsAudioStream.setState(SPAudioState.PAUSE, 0)
				self._audioDucker.disable()
			else:
				self._audioDucker.enable()
				self.ttsAudioStream.setState(SPAudioState.RUN, 0)
