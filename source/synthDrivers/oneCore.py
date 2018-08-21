#synthDrivers/oneCore.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2016-2018 Tyler Spivey, NV Access Limited, James Teh
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Synth driver for Windows OneCore voices.
"""

import os
import sys
from collections import OrderedDict
import ctypes
try:
	import _winreg as winreg # Python 2.7 import
except ImportError:
	import winreg # Python 3 import
import wave
import cStringIO
from synthDriverHandler import SynthDriver, VoiceInfo
from logHandler import log
import config
import nvwave
import speech
import speechXml
import languageHandler
import winVersion
import NVDAHelper

#: The number of 100-nanosecond units in 1 second.
HUNDRED_NS_PER_SEC = 10000000 # 1000000000 ns per sec / 100 ns
ocSpeech_Callback = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int, ctypes.c_wchar_p)

class _OcSsmlConverter(speechXml.SsmlConverter):

	def __init__(self, defaultLanguage, rate, pitch, volume):
		super(_OcSsmlConverter, self).__init__(defaultLanguage)
		self._rate = rate
		self._pitch = pitch
		self._volume = volume

	def generateBalancerCommands(self, speechSequence):
		commands = super(_OcSsmlConverter, self).generateBalancerCommands(speechSequence)
		# The EncloseAllCommand from SSML must be first.
		yield next(commands)
		# OneCore doesn't provide a way to set base prosody values.
		# Therefore, the base values need to be set using SSML.
		yield self.convertRateCommand(speech.RateCommand(multiplier=1))
		yield self.convertVolumeCommand(speech.VolumeCommand(multiplier=1))
		yield self.convertPitchCommand(speech.PitchCommand(multiplier=1))
		for command in commands:
			yield command

	def _convertProsody(self, command, attr, default, base):
		if command.multiplier == 1 and base == default:
			# Returning to synth default.
			return speechXml.DelAttrCommand("prosody", attr)
		else:
			# Multiplication isn't supported, only addition/subtraction.
			# The final value must therefore be relative to the synthesizer's default.
			val = base * command.multiplier - default
			return speechXml.SetAttrCommand("prosody", attr, "%d%%" % val)

	def convertRateCommand(self, command):
		return self._convertProsody(command, "rate", 50, self._rate)
	def convertPitchCommand(self, command):
		return self._convertProsody(command, "pitch", 50, self._pitch)
	def convertVolumeCommand(self, command):
		return self._convertProsody(command, "volume", 100, self._volume)

	def convertCharacterModeCommand(self, command):
		# OneCore's character speech sounds weird and doesn't support pitch alteration.
		# Therefore, we don't use it.
		return None

	def convertLangChangeCommand(self, command):
		lcid = languageHandler.localeNameToWindowsLCID(command.lang)
		if lcid is languageHandler.LCID_NONE:
			log.debugWarning("Invalid language: %s" % command.lang)
			return None
		return super(_OcSsmlConverter, self).convertLangChangeCommand(command)

class SynthDriver(SynthDriver):
	name = "oneCore"
	# Translators: Description for a speech synthesizer.
	description = _("Windows OneCore voices")
	supportedSettings = (
		SynthDriver.VoiceSetting(),
		SynthDriver.RateSetting(),
		SynthDriver.PitchSetting(),
		SynthDriver.VolumeSetting(),
	)
	# These are all controlled via SSML, so we only need attributes, not properties.
	rate = None
	pitch = None
	volume = None

	@classmethod
	def check(cls):
		if not hasattr(sys, "frozen"):
			# #3793: Source copies don't report the correct version on Windows 10 because Python isn't manifested for higher versions.
			# We want this driver to work for source copies on Windows 10, so just return True here.
			# If this isn't in fact Windows 10, it will fail when constructed, which is okay.
			return True
		# For binary copies, only present this as an available synth if this is Windows 10.
		return winVersion.winVersion.major >= 10

	def __init__(self):
		super(SynthDriver, self).__init__()
		self._dll = NVDAHelper.getHelperLocalWin10Dll()
		self._dll.ocSpeech_getCurrentVoiceLanguage.restype = ctypes.c_wchar_p
		self._handle = self._dll.ocSpeech_initialize()
		self._callbackInst = ocSpeech_Callback(self._callback)
		self._dll.ocSpeech_setCallback(self._handle, self._callbackInst)
		self._dll.ocSpeech_getVoices.restype = NVDAHelper.bstrReturn
		self._dll.ocSpeech_getCurrentVoiceId.restype = ctypes.c_wchar_p
		self._player= None
		# Initialize state.
		self._queuedSpeech = []
		self._wasCancelled = False
		self._isProcessing = False
		# Initialize the voice to a sane default
		self.voice=self._getDefaultVoice()
		# Set initial values for parameters that can't be queried.
		# This initialises our cache for the value.
		self.rate = 50
		self.pitch = 50
		self.volume = 100

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
		self._player = nvwave.WavePlayer(channels=wav.getnchannels(),
			samplesPerSec=samplesPerSec, bitsPerSample=bytesPerSample * 8,
			outputDevice=config.conf["speech"]["outputDevice"])

	def terminate(self):
		super(SynthDriver, self).terminate()
		self._dll.ocSpeech_terminate(self._handle)
		# Drop the ctypes function instance for the callback,
		# as it is holding a reference to an instance method, which causes a reference cycle.
		self._callbackInst = None

	def cancel(self):
		# Set a flag to tell the callback not to push more audio.
		self._wasCancelled = True
		log.debug("Cancelling")
		# There might be more text pending. Throw it away.
		self._queuedSpeech = []
		if self._player:
			self._player.stop()

	def speak(self, speechSequence):
		conv = _OcSsmlConverter(self.language, self.rate, self.pitch, self.volume)
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

	def _processQueue(self):
		if not self._queuedSpeech:
			# There are no more queued utterances at this point, so call idle.
			# This blocks while waiting for the final chunk to play,
			# so by the time this is done, there might be something queued.
			log.debug("Calling idle on audio player")
			self._player.idle()
		if self._queuedSpeech:
			item = self._queuedSpeech.pop(0)
			self._wasCancelled = False
			log.debug("Begin processing speech")
			self._isProcessing = True
			# ocSpeech_speak is async.
			# It will call _callback in a background thread once done,
			# which will eventually process the queue again.
			self._dll.ocSpeech_speak(self._handle, item)
			return
		log.debug("Queue empty, done processing")
		self._isProcessing = False

	def _callback(self, bytes, len, markers):
		if len == 0:
			# The C++ code will log an error with details.
			log.debugWarning("ocSpeech_speak failed!")
			self._processQueue()
			return
		# This gets called in a background thread.
		stream = cStringIO.StringIO(ctypes.string_at(bytes, len))
		wav = wave.open(stream, "r")
		self._maybeInitPlayer(wav)
		data = wav.readframes(wav.getnframes())
		if markers:
			markers = markers.split('|')
		else:
			markers = []
		prevMarker = None
		prevPos = 0

		# Push audio up to each marker so we can sync the audio with the markers.
		for marker in markers:
			if self._wasCancelled:
				break
			name, pos = marker.split(':')
			pos = int(pos)
			# pos is a time offset in 100-nanosecond units.
			# Convert this to a byte offset.
			# Order the equation so we don't have to do floating point.
			pos = pos * self._bytesPerSec / HUNDRED_NS_PER_SEC
			# Push audio up to this marker.
			self._player.feed(data[prevPos:pos])
			# _player.feed blocks until the previous chunk of audio is complete, not the chunk we just pushed.
			# Therefore, indicate that we've reached the previous marker.
			if prevMarker:
				self.lastIndex = prevMarker
			prevMarker = int(name)
			prevPos = pos
		if self._wasCancelled:
			log.debug("Cancelled, stopped pushing audio")
		else:
			self._player.feed(data[prevPos:])
			if prevMarker:
				self.lastIndex = prevMarker
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
		voicesStr = self._dll.ocSpeech_getVoices(self._handle).split('|')
		for index,voiceStr in enumerate(voicesStr):
			voiceInfo=self._getVoiceInfoFromOnecoreVoiceString(voiceStr)
			# Filter out any invalid voices.
			if not self._isVoiceValid(voiceInfo.ID):
				continue
			voiceInfo.onecoreIndex=index
			voices[voiceInfo.ID] =  voiceInfo
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
		if not langDataPath or not isinstance(langDataPath[0], basestring):
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
		if not voicePath or not isinstance(voicePath[0],basestring):
			log.debugWarning("Invalid voicePath value")
			return False
		if not os.path.isfile(os.path.expandvars(voicePath[0] + '.apm')):
			log.debugWarning("Missing voice file: %s" % voicePath[0] + ".apm")
			return False
		return True

	def _get_voice(self):
		return self._dll.ocSpeech_getCurrentVoiceId(self._handle)

	def _set_voice(self, ID):
		voices = self.availableVoices
		# Try setting the requested voice
		for voice in voices.itervalues():
			if voice.ID == ID:
				self._dll.ocSpeech_setVoice(self._handle, voice.onecoreIndex)
				return
		raise LookupError("No such voice: %s"%ID)

	def _getDefaultVoice(self):
		"""
		Finds the best available voice that can be used as a default.
		It first tries finding a voice with the same language and country as the user's configured Windows language (E.g. en_AU), 
		else one that matches just the language (E.g. en), 
		else simply the first available.
		@returns: the ID of the voice, suitable for passing to self.voice for setting.
		@rtype: string
		"""
		voices = self.availableVoices
		# Try matching to NVDA language
		fullLanguage=languageHandler.getWindowsLanguage()
		for voice in voices.itervalues():
			if voice.language==fullLanguage:
				return voice.ID
		baseLanguage=fullLanguage.split('_')[0]
		if baseLanguage!=fullLanguage:
			for voice in voices.itervalues():
				if voice.language.startswith(baseLanguage):
					return voice.ID
		# Just use the first available
		for voice in voices.itervalues():
			return voice.ID
		raise RuntimeError("No voices available")

	def _get_language(self):
		return self._dll.ocSpeech_getCurrentVoiceLanguage(self._handle)

	def pause(self, switch):
		if self._player:
			self._player.pause(switch)
