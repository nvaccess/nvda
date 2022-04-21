# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2016-2021 Tyler Spivey, NV Access Limited, James Teh, Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Synth driver for Windows OneCore voices.
"""

import os
import sys
from collections import OrderedDict
import ctypes
import winreg
import wave
from synthDriverHandler import (
	findAndSetNextSynth,
	isDebugForSynthDriver,
	SynthDriver,
	synthDoneSpeaking,
	synthIndexReached,
	VoiceInfo,
)
import io
from logHandler import log
import config
import nvwave
import queueHandler
import speech
import speechXml
import languageHandler
import winVersion
import NVDAHelper

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

#: The number of 100-nanosecond units in 1 second.
HUNDRED_NS_PER_SEC = 10000000 # 1000000000 ns per sec / 100 ns
ocSpeech_Callback = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int, ctypes.c_wchar_p)

class _OcSsmlConverter(speechXml.SsmlConverter):

	def _convertProsody(self, command, attr, default, base=None):
		if base is None:
			base = default
		if command.multiplier == 1 and base == default:
			# Returning to synth default.
			return speechXml.DelAttrCommand("prosody", attr)
		else:
			# Multiplication isn't supported, only addition/subtraction.
			# The final value must therefore be relative to the synthesizer's default.
			val = base * command.multiplier - default
			return speechXml.SetAttrCommand("prosody", attr, "%d%%" % val)

	def convertRateCommand(self, command):
		return self._convertProsody(command, "rate", 50)

	def convertPitchCommand(self, command):
		return self._convertProsody(command, "pitch", 50)

	def convertVolumeCommand(self, command):
		return self._convertProsody(command, "volume", 100)

	def convertCharacterModeCommand(self, command):
		# OneCore's character speech sounds weird and doesn't support pitch alteration.
		# Therefore, we don't use it.
		return None

	def convertLangChangeCommand(self, command):
		lcid = languageHandler.localeNameToWindowsLCID(command.lang)
		if lcid is languageHandler.LCID_NONE:
			log.debugWarning(f"Invalid language: {command.lang}")
			return None
		return super().convertLangChangeCommand(command)

class _OcPreAPI5SsmlConverter(_OcSsmlConverter):

	def __init__(self, defaultLanguage, rate, pitch, volume):
		super(_OcPreAPI5SsmlConverter, self).__init__(defaultLanguage)
		self._rate = rate
		self._pitch = pitch
		self._volume = volume

	def generateBalancerCommands(self, speechSequence):
		commands = super(_OcPreAPI5SsmlConverter, self).generateBalancerCommands(speechSequence)
		# The EncloseAllCommand from SSML must be first.
		yield next(commands)
		# OneCore didn't provide a way to set base prosody values before API version 5.
		# Therefore, the base values need to be set using SSML.
		yield self.convertRateCommand(RateCommand(multiplier=1))
		yield self.convertVolumeCommand(VolumeCommand(multiplier=1))
		yield self.convertPitchCommand(PitchCommand(multiplier=1))
		for command in commands:
			yield command

	def convertRateCommand(self, command):
		return self._convertProsody(command, "rate", 50, self._rate)

	def convertPitchCommand(self, command):
		return self._convertProsody(command, "pitch", 50, self._pitch)

	def convertVolumeCommand(self, command):
		return self._convertProsody(command, "volume", 100, self._volume)


class OneCoreSynthDriver(SynthDriver):

	MIN_PITCH = 0.0
	MAX_PITCH = 2.0
	MIN_RATE = 0.5
	DEFAULT_MAX_RATE = 1.5
	BOOSTED_MAX_RATE = 6.0
	MAX_CONSECUTIVE_SPEECH_FAILURES = 5

	name = "oneCore"
	# Translators: Description for a speech synthesizer.
	description = _("Windows OneCore voices")
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
		# Only present this as an available synth if this is Windows 10.
		return winVersion.getWinVer() >= winVersion.WIN10

	def _get_supportsProsodyOptions(self):
		self.supportsProsodyOptions = self._dll.ocSpeech_supportsProsodyOptions()
		return self.supportsProsodyOptions

	def _get_supportedSettings(self):
		self.supportedSettings = settings = [
			SynthDriver.VoiceSetting(),
			SynthDriver.RateSetting(),
		]
		if self.supportsProsodyOptions:
			settings.append(SynthDriver.RateBoostSetting())
		settings.extend([
			SynthDriver.PitchSetting(),
			SynthDriver.VolumeSetting(),
		])
		return settings

	def __init__(self):
		super().__init__()
		self._dll = NVDAHelper.getHelperLocalWin10Dll()
		self._dll.ocSpeech_getCurrentVoiceLanguage.restype = ctypes.c_wchar_p
		# Set initial values for parameters that can't be queried when prosody is not supported.
		# This initialises our cache for the value.
		# When prosody is supported, the values are used for cachign reasons.
		self._rate = 50
		self._pitch = 50
		self._volume = 100

		if self.supportsProsodyOptions:
			self._dll.ocSpeech_getPitch.restype = ctypes.c_double
			self._dll.ocSpeech_getVolume.restype = ctypes.c_double
			self._dll.ocSpeech_getRate.restype = ctypes.c_double
		else:
			log.debugWarning("Prosody options not supported")

		self._earlyExitCB = False
		self._callbackInst = ocSpeech_Callback(self._callback)
		self._ocSpeechToken = self._dll.ocSpeech_initialize(self._callbackInst)
		self._dll.ocSpeech_getVoices.restype = NVDAHelper.bstrReturn
		self._dll.ocSpeech_getCurrentVoiceId.restype = ctypes.c_wchar_p
		self._player= None
		# Initialize state.
		self._queuedSpeech = []
		self._wasCancelled = False
		self._isProcessing = False
		# Initialize the voice to a sane default
		self.voice=self._getDefaultVoice()
		self._consecutiveSpeechFailures = 0

	def _maybeInitPlayer(self, wav):
		"""Initialize audio playback based on the wave header provided by the synthesizer.
		If the sampling rate has not changed, the existing player is used.
		Otherwise, a new one is created with the appropriate parameters.
		"""
		samplesPerSec = wav.getframerate()
		if self._player and self._player.samplesPerSec == samplesPerSec:
			return
		if self._player:
			# Finalise any pending audio.
			self._player.idle()
		bytesPerSample = wav.getsampwidth()
		self._bytesPerSec = samplesPerSec * bytesPerSample
		self._player = nvwave.WavePlayer(
			channels=wav.getnchannels(),
			samplesPerSec=samplesPerSec,
			bitsPerSample=bytesPerSample * 8,
			outputDevice=config.conf["speech"]["outputDevice"]
		)

	def terminate(self):
		# prevent any pending callbacks from interacting further with the synth.
		self._earlyExitCB = True
		super().terminate()
		# Terminate the synth, the callback function should no longer be called after this returns.
		self._dll.ocSpeech_terminate(self._ocSpeechToken)
		# Drop the ctypes function instance for the callback and handle,
		# as it is holding a reference to an instance method, which causes a reference cycle.
		self._ocSpeechToken = None
		self._callbackInst = None

	def cancel(self):
		# Set a flag to tell the callback not to push more audio.
		self._wasCancelled = True
		if isDebugForSynthDriver():
			log.debug("Cancelling")
		# There might be more text pending. Throw it away.
		if self.supportsProsodyOptions:
			# In this case however, we must keep any parameter changes.
			self._queuedSpeech = [item for item in self._queuedSpeech
				if not isinstance(item, str)]
		else:
			self._queuedSpeech = []
		if self._player:
			self._player.stop()

	def speak(self, speechSequence):
		if self.supportsProsodyOptions:
			conv = _OcSsmlConverter(self.language)
		else:
			conv = _OcPreAPI5SsmlConverter(self.language, self._rate, self._pitch, self._volume)
		text = conv.convertToXml(speechSequence)
		# #7495: Calling WaveOutOpen blocks for ~100 ms if called from the callback
		# when the SSML includes marks.
		# We're not quite sure why.
		# To work around this, open the device before queuing.
		if self._player:
			self._player.open()
		self._queueSpeech(text)

	def _queueSpeech(self, item):
		self._queuedSpeech.append(item)
		# We only process the queue here if it isn't already being processed.
		if not self._isProcessing:
			self._processQueue()

	@classmethod
	def _percentToParam(self, percent, min, max):
		"""Overrides SynthDriver._percentToParam to return floating point parameter values.
		"""
		return float(percent) / 100 * (max - min) + min

	def _get_pitch(self):
		if not self.supportsProsodyOptions:
			return self._pitch
		rawPitch = self._dll.ocSpeech_getPitch(self._ocSpeechToken)
		return self._paramToPercent(rawPitch, self.MIN_PITCH, self.MAX_PITCH)

	def _set_pitch(self, pitch):
		self._pitch = pitch
		if not self.supportsProsodyOptions:
			return
		rawPitch = self._percentToParam(pitch, self.MIN_PITCH, self.MAX_PITCH)
		self._queuedSpeech.append((self._dll.ocSpeech_setPitch, rawPitch))

	def _get_volume(self):
		if not self.supportsProsodyOptions:
			return self._volume
		rawVolume = self._dll.ocSpeech_getVolume(self._ocSpeechToken)
		return int(rawVolume * 100)

	def _set_volume(self, volume):
		self._volume = volume
		if not self.supportsProsodyOptions:
			return
		rawVolume = volume / 100.0
		self._queuedSpeech.append((self._dll.ocSpeech_setVolume, rawVolume))

	def _get_rate(self):
		if not self.supportsProsodyOptions:
			return self._rate
		rawRate = self._dll.ocSpeech_getRate(self._ocSpeechToken)
		maxRate = self.BOOSTED_MAX_RATE if self._rateBoost else self.DEFAULT_MAX_RATE
		return self._paramToPercent(rawRate, self.MIN_RATE, maxRate)

	def _set_rate(self, rate):
		self._rate = rate
		if not self.supportsProsodyOptions:
			return
		maxRate = self.BOOSTED_MAX_RATE if self._rateBoost else self.DEFAULT_MAX_RATE
		rawRate = self._percentToParam(rate, self.MIN_RATE, maxRate)
		self._queuedSpeech.append((self._dll.ocSpeech_setRate, rawRate))

	_rateBoost = False

	def _get_rateBoost(self):
		return self._rateBoost

	def _set_rateBoost(self, enable):
		if enable == self._rateBoost:
			return
		# Use the cached rate to calculate the new rate with rate boost enabled.
		# If we don't, getting the rate property will return the default rate when initializing the driver and applying settings.
		rate = self._rate
		self._rateBoost = enable
		self.rate = rate

	def _processQueue(self):
		if not self._queuedSpeech and self._player is None:
			# If oneCore speech has not been successful yet the player will not have initialised. (#11544)
			# We can't sync the player in this instance.
			log.debugWarning("Cannot process speech queue as player not set and no speech queued")
			return
		if not self._queuedSpeech:
			# There are no more queued utterances at this point, so call sync.
			# This blocks while waiting for the final chunk to play,
			# so by the time this is done, there might be something queued.
			# #10721: We use sync instead of idle because idle closes the audio
			# device. If there's something in the queue after playing the final chunk,
			# that will result in WaveOutOpen being called in the callback when we
			# push the next chunk of audio. We *really* don't want this because calling
			# WaveOutOpen blocks for ~100 ms if called from the callback when the SSML
			# includes marks, resulting in lag between utterances.
			if isDebugForSynthDriver():
				log.debug("Calling sync on audio player")
			self._player.sync()
		if not self._queuedSpeech:
			# There's still nothing in the queue, so it's okay to call idle now.
			if isDebugForSynthDriver():
				log.debug("Calling idle on audio player")
			self._player.idle()
			synthDoneSpeaking.notify(synth=self)
		while self._queuedSpeech:
			item = self._queuedSpeech.pop(0)
			if isinstance(item, tuple):
				# Parameter change.
				# Note that, if prosody otions aren't supported, this code will never be executed.
				func, value = item
				value = ctypes.c_double(value)
				func(self._ocSpeechToken, value)
				continue
			self._wasCancelled = False
			if isDebugForSynthDriver():
				log.debug("Begin processing speech")
			self._isProcessing = True
			# ocSpeech_speak is async.
			# It will call _callback in a background thread once done,
			# which will eventually process the queue again.
			self._dll.ocSpeech_speak(self._ocSpeechToken, item)
			return
		if isDebugForSynthDriver():
			log.debug("Queue empty, done processing")
		self._isProcessing = False

	def _handleSpeechFailure(self):
		# The C++ code will log an error with details.
		log.error("OneCore synthesizer failed to speak")  # so a warning beep is played when speech fails
		try:
			self._processQueue()
		finally:
			self._consecutiveSpeechFailures += 1
			if self._consecutiveSpeechFailures >= self.MAX_CONSECUTIVE_SPEECH_FAILURES:
				log.debugWarning("Too many consecutive speech failures, changing synth")
				queueHandler.queueFunction(queueHandler.eventQueue, findAndSetNextSynth, self.name)
				self._consecutiveSpeechFailures = 0

	def _callback(self, bytes, len, markers):
		if self._earlyExitCB:
			# prevent any pending callbacks from interacting further with the synth.
			# used during termination.
			return
		if len == 0:
			# Speech failed
			self._handleSpeechFailure()
			return
		else:
			self._consecutiveSpeechFailures = 0
		# This gets called in a background thread.
		stream = io.BytesIO(ctypes.string_at(bytes, len))
		wav = wave.open(stream, "r")
		self._maybeInitPlayer(wav)
		data = wav.readframes(wav.getnframes())
		if markers:
			markers = markers.split('|')
		else:
			markers = []
		prevPos = 0

		# Push audio up to each marker so we can sync the audio with the markers.
		for marker in markers:
			if self._wasCancelled:
				break
			name, pos = marker.split(':')
			index = int(name)
			pos = int(pos)
			# pos is a time offset in 100-nanosecond units.
			# Convert this to a byte offset.
			# Order the equation so we don't have to do floating point.
			pos = pos * self._bytesPerSec // HUNDRED_NS_PER_SEC
			# Push audio up to this marker.
			self._player.feed(data[prevPos:pos],
				onDone=lambda index=index: synthIndexReached.notify(synth=self, index=index))
			prevPos = pos
		if self._wasCancelled:
			if isDebugForSynthDriver():
				log.debug("Cancelled, stopped pushing audio")
		else:
			self._player.feed(data[prevPos:])
			if isDebugForSynthDriver():
				log.debug("Done pushing audio")
		self._processQueue()

	def _getVoiceInfoFromOnecoreVoiceString(self, voiceStr):
		"""
		Produces an NVDA VoiceInfo object representing the given voice string from Onecore speech.
		"""
		# The voice string is made up of the ID, the language, and the display name.
		ID,language,name=voiceStr.split(':')
		language=language.replace('-','_')
		return VoiceInfo(ID,name,language=language)

	def _getAvailableVoices(self):
		voices = OrderedDict()
		# Fetch the full list of voices that Onecore speech knows about.
		# Note that it may give back voices that are uninstalled or broken. 
		voicesStr = self._dll.ocSpeech_getVoices(self._ocSpeechToken).split('|')
		for index,voiceStr in enumerate(voicesStr):
			voiceInfo=self._getVoiceInfoFromOnecoreVoiceString(voiceStr)
			# Filter out any invalid voices.
			if not self._isVoiceValid(voiceInfo.id):
				continue
			voiceInfo.onecoreIndex=index
			voices[voiceInfo.id] =  voiceInfo
		return voices

	def _isVoiceValid(self,ID):
		"""
		Checks that the given voice actually exists and is valid.
		It checks the Registry, and also ensures that its data files actually exist on this machine.
		@param ID: the ID of the requested voice.
		@type ID: string
		@returns: True if the voice is valid, false otherwise.
		@rtype: boolean
		"""
		IDParts = ID.split('\\')
		rootKey = getattr(winreg, IDParts[0])
		subkey = "\\".join(IDParts[1:])
		try:
			hkey = winreg.OpenKey(rootKey, subkey)
		except WindowsError as e:
			log.debugWarning("Could not open registry key %s, %r" % (ID, e))
			return False
		try:
			langDataPath = winreg.QueryValueEx(hkey, 'langDataPath')
		except WindowsError as e:
			log.debugWarning("Could not open registry value 'langDataPath', %r" % e)
			return False
		if not langDataPath or not isinstance(langDataPath[0], str):
			log.debugWarning("Invalid langDataPath value")
			return False
		if not os.path.isfile(os.path.expandvars(langDataPath[0])):
			log.debugWarning("Missing language data file: %s" % langDataPath[0])
			return False
		try:
			voicePath = winreg.QueryValueEx(hkey, 'voicePath')
		except WindowsError as e:
			log.debugWarning("Could not open registry value 'langDataPath', %r" % e)
			return False
		if not voicePath or not isinstance(voicePath[0],str):
			log.debugWarning("Invalid voicePath value")
			return False
		if not os.path.isfile(os.path.expandvars(voicePath[0] + '.apm')):
			log.debugWarning("Missing voice file: %s" % voicePath[0] + ".apm")
			return False
		return True

	def _get_voice(self):
		return self._dll.ocSpeech_getCurrentVoiceId(self._ocSpeechToken)

	def _set_voice(self, id):
		voices = self.availableVoices
		# Try setting the requested voice
		for voice in voices.values():
			if voice.id == id:
				self._dll.ocSpeech_setVoice(self._ocSpeechToken, voice.onecoreIndex)
				return
		raise LookupError("No such voice: %s"%id)

	def _getDefaultVoice(self, pickAny: bool = True) -> str:
		"""
		Finds the best available voice that can be used as a default.
		It first tries finding a voice with the same language as the user's configured NVDA language
		else one that matches the system language.
		else any voice if pickAny is True.
		Uses the Windows locale (eg en_AU) to provide country information for the voice where possible.
		@returns: the ID of the voice, suitable for passing to self.voice for setting.
		"""
		voices = self.availableVoices
		fullWindowsLanguage = languageHandler.getWindowsLanguage()
		baseWindowsLanguage = fullWindowsLanguage.split('_')[0]
		NVDALanguage = languageHandler.getLanguage()
		if NVDALanguage.startswith(baseWindowsLanguage):
			# add country information if it matches
			NVDALanguage = fullWindowsLanguage
		# Try matching to the NVDA language
		for voice in voices.values():
			if voice.language.startswith(NVDALanguage):
				return voice.id
		# Try matching to the system language and country
		if fullWindowsLanguage != NVDALanguage:
			for voice in voices.values():
				if voice.language == fullWindowsLanguage:
					return voice.id
		# Try matching to the system language
		if baseWindowsLanguage not in {fullWindowsLanguage, NVDALanguage}:
			for voice in voices.values():
				if voice.language.startswith(baseWindowsLanguage):
					return voice.id
		if pickAny:
			for voice in voices.values():
				return voice.id
			raise VoiceUnsupportedError("No voices available")
		raise VoiceUnsupportedError("No voices available that match the user language")

	def pause(self, switch):
		if self._player:
			self._player.pause(switch)


# Alias to allow look up by name "SynthDriver"
SynthDriver = OneCoreSynthDriver


class VoiceUnsupportedError(RuntimeError):
	pass
