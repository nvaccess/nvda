# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2025 NV Access Limited, Peter Vágner, Aleksey Sadovoy, gexgd0419
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from ctypes import POINTER, c_ubyte, c_ulong, c_wchar_p, cast, windll, _Pointer
from enum import IntEnum
import locale
from collections import OrderedDict, deque
from typing import TYPE_CHECKING
import audioDucking
from comInterfaces.SpeechLib import ISpEventSource, ISpNotifySource, ISpNotifySink
import comtypes.client
from comtypes import COMError, COMObject, IUnknown, hresult
import winreg
import nvwave
from objidl import _LARGE_INTEGER, _ULARGE_INTEGER, IStream
from synthDriverHandler import SynthDriver, VoiceInfo, synthIndexReached, synthDoneSpeaking
import config
from logHandler import log
import weakref
import languageHandler

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
from ._sonic import SonicStream, initialize as sonicInitialize


class _SPAudioState(IntEnum):
	# https://docs.microsoft.com/en-us/previous-versions/windows/desktop/ms720596(v=vs.85)
	CLOSED = 0
	STOP = 1
	PAUSE = 2
	RUN = 3


class SpeechVoiceSpeakFlags(IntEnum):
	# https://docs.microsoft.com/en-us/previous-versions/windows/desktop/ms720892(v=vs.85)
	Async = 1
	PurgeBeforeSpeak = 2
	IsXML = 8


class SpeechVoiceEvents(IntEnum):
	# https://msdn.microsoft.com/en-us/previous-versions/windows/desktop/ms720886(v=vs.85)
	StartInputStream = 2
	EndInputStream = 4
	Bookmark = 16


if TYPE_CHECKING:
	LP_c_ubyte = _Pointer[c_ubyte]
	LP_c_ulong = _Pointer[c_ulong]
	LP__ULARGE_INTEGER = _Pointer[_ULARGE_INTEGER]
else:
	LP_c_ubyte = POINTER(c_ubyte)
	LP_c_ulong = POINTER(c_ulong)
	LP__ULARGE_INTEGER = POINTER(_ULARGE_INTEGER)


class SynthDriverAudioStream(COMObject):
	"""
	Implements IStream to receive streamed-in audio data.
	Should be wrapped in an SpCustomStream
	(which also provides the wave format information),
	then set as the AudioOutputStream.
	"""

	_com_interfaces_ = [IStream]

	def __init__(self, synthRef: weakref.ReferenceType):
		self.synthRef = synthRef
		self._writtenBytes = 0

	def ISequentialStream_RemoteWrite(
		self,
		this: int,
		pv: LP_c_ubyte,
		cb: int,
		pcbWritten: LP_c_ulong,
	) -> int:
		"""This is called when SAPI wants to write (output) a wave data chunk.
		:param pv: A pointer to the first wave data byte.
		:param cb: The number of bytes to write.
		:param pcbWritten: A pointer to a variable where the actual number of bytes written will be stored.
			Can be null.
		:returns: HRESULT code.
		"""
		synth = self.synthRef()
		if pcbWritten:
			pcbWritten[0] = 0
		if synth is None:
			log.debugWarning("Called Write method on AudioStream while driver is dead")
			return hresult.E_UNEXPECTED
		if not synth.isSpeaking:
			return hresult.E_FAIL
		synth.sonicStream.writeShort(pv, cb // 2 // synth.sonicStream.channels)
		audioData = synth.sonicStream.readShort()
		synth.player.feed(audioData, len(audioData) * 2)
		if pcbWritten:
			pcbWritten[0] = cb
		self._writtenBytes += cb
		return hresult.S_OK

	def IStream_RemoteSeek(
		self,
		this: int,
		dlibMove: _LARGE_INTEGER,
		dwOrigin: int,
		plibNewPosition: LP__ULARGE_INTEGER,
	) -> int:
		"""This is called when SAPI wants to get the current stream position.
		Seeking to another position is not supported.
		:param dlibMove: The displacement to be added to the location indicated by the dwOrigin parameter.
			Only 0 is supported.
		:param dwOrigin: The origin for the displacement specified in dlibMove.
			Only 1 (STREAM_SEEK_CUR) is supported.
		:param plibNewPosition: A pointer to a ULARGE_INTEGER where the current stream position will be stored.
			Can be null.
		:returns: HRESULT code.
		"""
		if dwOrigin == 1 and dlibMove.QuadPart == 0:
			# SAPI is querying the current position.
			if plibNewPosition:
				plibNewPosition[0].QuadPart = self._writtenBytes
			return hresult.S_OK
		return hresult.E_NOTIMPL

	def IStream_Commit(self, grfCommitFlags: int):
		"""This is called when MSSP wants to flush the written data.
		Does nothing."""
		pass


class SapiSink(COMObject):
	"""
	Implements ISpNotifySink to handle SAPI event notifications.
	Should be passed to ISpNotifySource::SetNotifySink().
	Notifications will be sent on the original thread,
	instead of being routed to the main thread.
	"""

	_com_interfaces_ = [ISpNotifySink]

	def __init__(self, synthRef: weakref.ReferenceType):
		self.synthRef = synthRef

	def ISpNotifySink_Notify(self):
		"""This is called when there's a new event notification.
		Queued events will be retrieved."""
		synth = self.synthRef()
		if synth is None:
			log.debugWarning("Called Notify method on SapiSink while driver is dead")
			return
		# Get all queued events
		eventSource = synth.tts.QueryInterface(ISpEventSource)
		while True:
			# returned tuple: (event, numFetched)
			eventTuple = eventSource.GetEvents(1)  # Get one event
			if eventTuple[1] != 1:
				break
			event = eventTuple[0]
			if event.eEventId == 1:  # SPEI_START_INPUT_STREAM
				self.StartStream(event.ulStreamNum, event.ullAudioStreamOffset)
			elif event.eEventId == 2:  # SPEI_END_INPUT_STREAM
				self.EndStream(event.ulStreamNum, event.ullAudioStreamOffset)
			elif event.eEventId == 4:  # SPEI_TTS_BOOKMARK
				self.Bookmark(
					event.ulStreamNum,
					event.ullAudioStreamOffset,
					cast(event.lParam, c_wchar_p).value,
					event.wParam,
				)
			# free lParam
			if event.elParamType == 1 or event.elParamType == 2:  # token or object
				pUnk = cast(event.lParam, POINTER(IUnknown))
				del pUnk
			elif event.elParamType == 3 or event.elParamType == 4:  # pointer or string
				windll.ole32.CoTaskMemFree(event.lParam)

	def StartStream(self, streamNum: int, pos: int):
		synth = self.synthRef()
		if synth._audioDucker:
			if audioDucking._isDebug():
				log.debug("Enabling audio ducking due to starting speech stream")
			synth._audioDucker.enable()
		# The stream has been started. Move the bookmark list to _streamBookmarks.
		if streamNum in synth._streamBookmarksNew:
			synth._streamBookmarks[streamNum] = synth._streamBookmarksNew[streamNum]
			del synth._streamBookmarksNew[streamNum]
		synth.isSpeaking = True

	def Bookmark(self, streamNum: int, pos: int, bookmark: str, bookmarkId: int):
		synth = self.synthRef()
		if not synth.isSpeaking or not synth.player:
			return
		# Bookmark event is raised before the audio after that point.
		# Queue an IndexReached event at this point.
		synth.player.feed(None, 0, lambda: self.onIndexReached(streamNum, bookmarkId))

	def EndStream(self, streamNum: int, pos: int):
		synth = self.synthRef()
		if synth.player:
			# Flush the stream and get the remaining data.
			synth.sonicStream.flush()
			audioData = synth.sonicStream.readShort()
			synth.player.feed(audioData, len(audioData) * 2)
			synth.player.idle()
		# trigger all untriggered bookmarks
		if streamNum in synth._streamBookmarks:
			for bookmark in synth._streamBookmarks[streamNum]:
				synthIndexReached.notify(synth=synth, index=bookmark)
			del synth._streamBookmarks[streamNum]
		synth.isSpeaking = False
		synthDoneSpeaking.notify(synth=synth)
		if synth._audioDucker:
			if audioDucking._isDebug():
				log.debug("Disabling audio ducking due to speech stream end")
			synth._audioDucker.disable()

	def onIndexReached(self, streamNum: int, index: int):
		synth = self.synthRef()
		if synth is None:
			log.debugWarning("Called onIndexReached method on SapiSink while driver is dead")
			return
		synthIndexReached.notify(synth=synth, index=index)
		# remove already triggered bookmarks
		if streamNum in synth._streamBookmarks:
			bookmarks = synth._streamBookmarks[streamNum]
			while bookmarks:
				if bookmarks.popleft() == index:
					break


class SynthDriver(SynthDriver):
	supportedSettings = (
		SynthDriver.VoiceSetting(),
		SynthDriver.RateSetting(),
		SynthDriver.RateBoostSetting(),
		SynthDriver.PitchSetting(),
		SynthDriver.VolumeSetting(),
		SynthDriver.UseWasapiSetting(),
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

	COM_CLASS = "SAPI.SPVoice"
	CUSTOMSTREAM_COM_CLASS = "SAPI.SpCustomStream"

	name = "sapi5"
	description = "Microsoft Speech API version 5"

	@classmethod
	def check(cls):
		try:
			r = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, cls.COM_CLASS)
			r.Close()
			return True
		except:  # noqa: E722
			return False

	ttsAudioStream = (
		None  #: Holds the ISPAudio interface for the current voice, to aid in stopping and pausing audio
	)
	_audioDucker: audioDucking.AudioDucker | None = None

	def __init__(self, _defaultVoiceToken=None):
		"""
		@param _defaultVoiceToken: an optional sapi voice token which should be used as the default voice (only useful for subclasses)
		@type _defaultVoiceToken: ISpeechObjectToken
		"""
		self._pitch = 50
		self._rate = 50
		self._volume = 100
		self._useWasapi = True
		self.player: nvwave.WavePlayer | None = None
		self.sonicStream: SonicStream | None = None
		self.isSpeaking = False
		self._rateBoost = False
		self._initTts(_defaultVoiceToken)
		# key = stream num, value = deque of bookmarks
		self._streamBookmarks = dict()  # bookmarks in currently speaking streams
		self._streamBookmarksNew = dict()  # bookmarks for streams that haven't been started

	def terminate(self):
		self.tts = None
		if self.player:
			self.player.close()
			self.player = None

	def _getAvailableVoices(self):
		voices = OrderedDict()
		v = self._getVoiceTokens()
		# #2629: Iterating uses IEnumVARIANT and GetBestInterface doesn't work on tokens returned by some token enumerators.
		# Therefore, fetch the items by index, as that method explicitly returns the correct interface.
		for i in range(len(v)):
			try:
				ID = v[i].Id
				name = v[i].GetDescription()
				try:
					language = locale.windows_locale[int(v[i].getattribute("language").split(";")[0], 16)]
				except KeyError:
					language = None
			except COMError:
				log.warning("Could not get the voice info. Skipping...")
			voices[ID] = VoiceInfo(ID, name, language)
		return voices

	def _getVoiceTokens(self):
		"""Provides a collection of sapi5 voice tokens. Can be overridden by subclasses if tokens should be looked for in some other registry location."""
		return self.tts.getVoices()

	def _get_rate(self):
		return self._rate

	def _get_rateBoost(self):
		return self._rateBoost

	def _get_pitch(self):
		return self._pitch

	def _get_volume(self) -> int:
		return self._volume

	def _get_voice(self):
		return self.tts.voice.Id

	def _get_useWasapi(self) -> bool:
		return self._useWasapi

	def _get_lastIndex(self):
		bookmark = self.tts.status.LastBookmark
		if bookmark != "" and bookmark is not None:
			return int(bookmark)
		else:
			return None

	@classmethod
	def _percentToParam(cls, percent, min, max) -> float:
		"""Overrides SynthDriver._percentToParam to return floating point parameter values."""
		return float(percent) / 100 * (max - min) + min

	def _percentToRate(self, percent):
		return (percent - 50) // 5

	def _set_rate(self, rate):
		self._rate = rate
		if not self.sonicStream:
			self.tts.Rate = self._percentToRate(rate)
			return
		if self._rateBoost:
			# When rate boost is enabled, use sonicStream to change the speed.
			# Supports 0.5x~6x speed.
			self.tts.Rate = 0
			self.sonicStream.speed = self._percentToParam(rate, 0.5, 6.0)
		else:
			# When rate boost is disabled, let the voice itself change the speed.
			self.tts.Rate = self._percentToRate(rate)
			self.sonicStream.speed = 1

	def _set_rateBoost(self, enable: bool):
		if enable == self._rateBoost:
			return
		rate = self._rate
		self._rateBoost = enable
		self.rate = rate

	def _set_pitch(self, value):
		# pitch is really controled with xml around speak commands
		self._pitch = value

	def _set_volume(self, value):
		self._volume = value
		self.tts.Volume = value

	def _initAudioDevice(self):
		# SAPI5 automatically selects the system default audio device, so there's no use doing work if the user has selected to use the system default.
		# Besides, our default value is not a valid endpoint ID.
		if (outputDevice := config.conf["audio"]["outputDevice"]) != config.conf.getConfigValidation(
			("audio", "outputDevice"),
		).default:
			for audioOutput in self.tts.GetAudioOutputs():
				# SAPI's audio output IDs are registry keys. It seems that the final path segment is the endpoint ID.
				if audioOutput.Id.endswith(outputDevice):
					self.tts.audioOutput = audioOutput
					break

	def _initWasapiAudio(self):
		fmt = self.tts.AudioOutputStream.Format
		wfx = fmt.GetWaveFormatEx()
		# Force the wave format to be 16-bit integer (which Sonic uses internally).
		# SAPI will convert the format for us if it isn't supported by the voice.
		wfx.FormatTag = nvwave.WAVE_FORMAT_PCM
		wfx.BitsPerSample = 16
		fmt.SetWaveFormatEx(wfx)
		self.player = nvwave.WavePlayer(
			channels=wfx.Channels,
			samplesPerSec=wfx.SamplesPerSec,
			bitsPerSample=wfx.BitsPerSample,
			outputDevice=config.conf["audio"]["outputDevice"],
		)
		audioStream = SynthDriverAudioStream(weakref.ref(self))
		# Use SpCustomStream to wrap our IStream implementation and the correct wave format
		customStream = comtypes.client.CreateObject(self.CUSTOMSTREAM_COM_CLASS)
		customStream.BaseStream = audioStream
		customStream.Format = fmt
		self.tts.AudioOutputStream = customStream
		sonicInitialize()
		self.sonicStream = SonicStream(wfx.SamplesPerSec, wfx.Channels)

	def _initLegacyAudio(self):
		if audioDucking.isAudioDuckingSupported():
			self._audioDucker = audioDucking.AudioDucker()
		from comInterfaces.SpeechLib import ISpAudio

		try:
			self.ttsAudioStream = self.tts.audioOutputStream.QueryInterface(ISpAudio)
		except COMError:
			log.debugWarning("SAPI5 voice does not support ISPAudio")
			self.ttsAudioStream = None

	def _initTts(self, voice: str | None = None):
		self.tts = comtypes.client.CreateObject(self.COM_CLASS)
		if voice:
			# #749: It seems that SAPI 5 doesn't reset the audio parameters when the voice is changed,
			# but only when the audio output is changed.
			# Therefore, set the voice before setting the audio output.
			# Otherwise, we will get poor speech quality in some cases.
			self.tts.voice = voice

		if self.player:
			self.player.close()
			self.player = None
		self.sonicStream = None
		self.ttsAudioStream = None
		self._audioDucker = None

		self._initAudioDevice()
		if self.useWasapi:
			self._initWasapiAudio()
		else:
			self._initLegacyAudio()

		# Set event notify sink
		self.tts.EventInterests = (
			SpeechVoiceEvents.StartInputStream | SpeechVoiceEvents.Bookmark | SpeechVoiceEvents.EndInputStream
		)
		notifySource = self.tts.QueryInterface(ISpNotifySource)
		notifySource.SetNotifySink(SapiSink(weakref.ref(self)))

	def _set_voice(self, value):
		tokens = self._getVoiceTokens()
		# #2629: Iterating uses IEnumVARIANT and GetBestInterface doesn't work on tokens returned by some token enumerators.
		# Therefore, fetch the items by index, as that method explicitly returns the correct interface.
		for i in range(len(tokens)):
			voice = tokens[i]
			if value == voice.Id:
				break
		else:
			# Voice not found.
			return
		self._initTts(voice=voice)
		# As _initTts resets the voice parameters on the tts object, set them back to current values.
		self._set_rate(self._rate)
		self._set_volume(self._volume)

	def _set_useWasapi(self, value: bool):
		if value == self._useWasapi:
			return
		self._useWasapi = value
		self.voice = self.voice  # reload the current voice

	def _percentToPitch(self, percent):
		return percent // 2 - 25

	IPA_TO_SAPI = {
		"θ": "th",
		"s": "s",
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
			if ipaChar == "ˈ":
				outAfter = "1"
				continue
			out.append(self.IPA_TO_SAPI[ipaChar])
			if outAfter:
				out.append(outAfter)
				outAfter = None
		if outAfter:
			out.append(outAfter)
		return " ".join(out)

	def speak(self, speechSequence):
		textList = []
		bookmarks = deque()

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
				bookmarks.append(item.index)
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
					textList.append(
						'<pron sym="%s">%s</pron>' % (self._convertPhoneme(item.ipa), item.text or ""),
					)
				except LookupError:
					log.debugWarning("Couldn't convert character in IPA string: %s" % item.ipa)
					if item.text:
						textList.append(item.text)
			elif isinstance(item, LangChangeCommand):
				lcid = (
					languageHandler.localeNameToWindowsLCID(item.lang)
					if item.lang
					else languageHandler.LCID_NONE
				)
				if lcid is languageHandler.LCID_NONE:
					try:
						del tags["lang"]
					except KeyError:
						pass
				else:
					tags["lang"] = {"langid": "%x" % lcid}
				tagsChanged[0] = True
			elif isinstance(item, SpeechCommand):
				log.debugWarning("Unsupported speech command: %s" % item)
			else:
				log.error("Unknown speech: %s" % item)
		# Close any tags that are still open.
		tags.clear()
		tagsChanged[0] = True
		outputTags()

		text = "".join(textList)
		flags = SpeechVoiceSpeakFlags.IsXML | SpeechVoiceSpeakFlags.Async
		if self.useWasapi:
			streamNum = self.tts.Speak(text, flags)
		else:
			streamNum = self._speak_legacy(text, flags)
		# When Speak returns, the previous stream may not have been ended.
		# So the bookmark list is stored in another dict until this stream starts.
		self._streamBookmarksNew[streamNum] = bookmarks

	def _speak_legacy(self, text: str, flags: int) -> int:
		"""Legacy way of calling SpVoice.Speak that uses a temporary audio ducker."""
		# Ducking should be complete before the synth starts producing audio.
		# For this to happen, the speech method must block until ducking is complete.
		# Ducking should be disabled when the synth is finished producing audio.
		# Note that there may be calls to speak with a string that results in no audio,
		# it is important that in this case the audio does not get stuck ducked.
		# When there is no audio produced the startStream and endStream handlers are not called.
		# To prevent audio getting stuck ducked, it is unducked at the end of speech.
		# There are some known issues:
		# - When there is no audio produced by the synth, a user may notice volume lowering (ducking) temporarily.
		# - If the call to startStream handler is delayed significantly, users may notice a variation in volume
		# (as ducking is disabled at the end of speak, and re-enabled when the startStream handler is called)

		# A note on the synchronicity of components of this approach:
		# SAPISink.StartStream event handler (callback):
		# the synth speech is not blocked by this event callback.
		# SAPISink.EndStream event handler (callback):
		# assumed also to be async but not confirmed. Synchronicity is irrelevant to the current approach.
		# AudioDucker.disable returns before the audio is completely unducked.
		# AudioDucker.enable() ducking will complete before the function returns.
		# It is not possible to "double duck the audio", calling twice yields the same result as calling once.
		# AudioDucker class instances count the number of enables/disables,
		# in order to unduck there must be no remaining enabled audio ducker instances.
		# Due to this a temporary audio ducker is used around the call to speak.
		# SAPISink.StartStream: Ducking here may allow the early speech to start before ducking is completed.
		if audioDucking.isAudioDuckingSupported():
			tempAudioDucker = audioDucking.AudioDucker()
		else:
			tempAudioDucker = None
		if tempAudioDucker:
			if audioDucking._isDebug():
				log.debug("Enabling audio ducking due to speak call")
			tempAudioDucker.enable()
		try:
			return self.tts.Speak(text, flags)
		finally:
			if tempAudioDucker:
				if audioDucking._isDebug():
					log.debug("Disabling audio ducking after speak call")
				tempAudioDucker.disable()

	def cancel(self):
		# SAPI5's default means of stopping speech can sometimes lag at end of speech, especially with Win8 / Win 10 Microsoft Voices.
		# Therefore  instruct the audio player to stop first, before interupting and purging any remaining speech.
		self.isSpeaking = False
		if self.player:
			self.player.stop()
			self.sonicStream.flush()
			self.sonicStream.readShort()  # discard data left in stream
		if self.ttsAudioStream:
			self.ttsAudioStream.setState(_SPAudioState.STOP, 0)
		self.tts.Speak(None, SpeechVoiceSpeakFlags.Async | SpeechVoiceSpeakFlags.PurgeBeforeSpeak)
		if self._audioDucker:
			if audioDucking._isDebug():
				log.debug("Disabling audio ducking due to setting output audio state to stop")
			self._audioDucker.disable()

	def pause(self, switch: bool):
		if self.player:
			self.player.pause(switch)
		# SAPI5's default means of pausing in most cases is either extremely slow
		# (e.g. takes more than half a second) or does not work at all.
		# Therefore instruct the underlying audio interface to pause instead.
		if self.ttsAudioStream:
			oldState = self.ttsAudioStream.GetStatus().State
			if switch and oldState == _SPAudioState.RUN:
				# pausing
				if self._audioDucker:
					if audioDucking._isDebug():
						log.debug("Disabling audio ducking due to setting output audio state to pause")
					self._audioDucker.disable()
				self.ttsAudioStream.setState(_SPAudioState.PAUSE, 0)
			elif not switch and oldState == _SPAudioState.PAUSE:
				# unpausing
				if self._audioDucker:
					if audioDucking._isDebug():
						log.debug("Enabling audio ducking due to setting output audio state to run")
					self._audioDucker.enable()
				self.ttsAudioStream.setState(_SPAudioState.RUN, 0)
