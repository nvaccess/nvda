# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2025 NV Access Limited, Peter Vágner, Aleksey Sadovoy, gexgd0419
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from ctypes import (
	HRESULT,
	POINTER,
	WINFUNCTYPE,
	byref,
	c_ubyte,
	c_ulong,
	c_void_p,
	c_wchar_p,
	cast,
	create_unicode_buffer,
	memmove,
	memset,
	sizeof,
	windll,
)
from enum import IntEnum
import locale
from collections import OrderedDict, deque
import threading
from typing import TYPE_CHECKING, NamedTuple, Generator
import audioDucking
from comInterfaces.SpeechLib import (
	_LARGE_INTEGER,
	_ULARGE_INTEGER,
	GUID,
	ISpAudio,
	ISpEventSource,
	ISpEventSink,
	ISpNotifySource,
	ISpNotifySink,
	ISpVoice,
	SPAUDIOSTATE,
	SPEVENT,
	WAVEFORMATEX,
)
import comtypes.client
from comtypes import COMError, COMObject, IUnknown, hresult
import winreg
import nvwave
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


class _SpeakRequest(NamedTuple):
	text: str
	bookmarks: deque[int]


if TYPE_CHECKING:
	from ctypes import _Pointer
else:

	class _Pointer:
		def __class_getitem__(cls, item: type) -> type:
			return POINTER(item)


class _SPEventLParamType(IntEnum):
	UNDEFINED = 0
	TOKEN = 1
	OBJECT = 2
	POINTER = 3
	STRING = 4


# Function types for calling COM methods
_Com_AddRef = WINFUNCTYPE(c_ulong)(1, "AddRef")
_Com_Release = WINFUNCTYPE(c_ulong)(2, "Release")
_ISpEventSource_GetEvents = WINFUNCTYPE(HRESULT, c_ulong, POINTER(SPEVENT), POINTER(c_ulong))(11, "GetEvents")

SPDFID_WaveFormatEx = GUID("{c31adbae-527f-4ff5-a230-f62bb61ff70c}")


class _SapiEvent(SPEVENT):
	def clear(self) -> None:
		"""Clear and free related data."""
		if self.elParamType in (_SPEventLParamType.TOKEN, _SPEventLParamType.OBJECT):
			_Com_Release(cast(self.lParam, c_void_p))
		elif self.elParamType in (_SPEventLParamType.POINTER, _SPEventLParamType.STRING):
			windll.ole32.CoTaskMemFree(cast(self.lParam, c_void_p))
		memset(byref(self), 0, sizeof(self))

	def __del__(self):
		self.clear()

	@staticmethod
	def copy(dst: SPEVENT, src: SPEVENT) -> None:
		memmove(byref(dst), byref(src), sizeof(src))
		if not src.lParam:
			return dst
		if src.elParamType == _SPEventLParamType.POINTER:
			dst.lParam = windll.ole32.CoTaskMemAlloc(src.wParam)
			if not dst.lParam:
				raise COMError(hresult.E_OUTOFMEMORY, "CoTaskMemAlloc failed", (None, None, None, None, None))
			memmove(dst.lParam, src.lParam, src.wParam)
		elif src.elParamType == _SPEventLParamType.STRING:
			strbuf = create_unicode_buffer(cast(src.lParam, c_wchar_p).value)
			bufsize = sizeof(strbuf)
			dst.lParam = windll.ole32.CoTaskMemAlloc(bufsize)
			if not dst.lParam:
				raise COMError(hresult.E_OUTOFMEMORY, "CoTaskMemAlloc failed", (None, None, None, None, None))
			memmove(dst.lParam, byref(strbuf), bufsize)
		elif src.elParamType in (_SPEventLParamType.TOKEN, _SPEventLParamType.OBJECT):
			_Com_AddRef(cast(src.lParam, c_void_p))

	def copyTo(self, dst: SPEVENT) -> None:
		_SapiEvent.copy(dst, self)

	def copyFrom(self, src: SPEVENT) -> None:
		_SapiEvent.copy(self, src)

	def getFrom(self, eventSource: _Pointer[ISpEventSource]) -> bool:
		"""Get one event from the event source and store it in this object.
		Return False if there is no event."""
		self.clear()
		# Use the raw ctypes.WINFUNCTYPE to call ISpEventSource::GetEvents()
		# instead of using comtypes, because we want to retrieve the event in-place
		# rather than letting comtypes allocating a new SPEVENT structure.
		hr = _ISpEventSource_GetEvents(eventSource, 1, byref(self), None)
		return hr == hresult.S_OK

	@staticmethod
	def enumerateFrom(eventSource: _Pointer[ISpEventSource]) -> Generator["_SapiEvent", None, None]:
		"""Enumerate all events in the event source."""
		while True:
			event = _SapiEvent()
			if not event.getFrom(eventSource):
				break
			yield event

	def getString(self) -> str:
		"""Get the string parameter stored in lParam."""
		if self.elParamType != _SPEventLParamType.STRING:
			raise TypeError("The lParam of this event is not a string")
		return cast(self.lParam, c_wchar_p).value


class SynthDriverAudioStream(COMObject):
	"""
	Implements IStream to receive streamed-in audio data.
	Should be wrapped in an SpCustomStream
	(which also provides the wave format information),
	then set as the AudioOutputStream.
	"""

	_com_interfaces_ = [ISpAudio, ISpEventSource, ISpEventSink]

	def __init__(self, synthRef: weakref.ReferenceType["SynthDriver"]):
		self.synthRef = synthRef
		self._writtenBytes = 0
		self.waveFormat = WAVEFORMATEX()
		self._writeDefaultFormat(self.waveFormat)
		self._events: deque[_SapiEvent] = deque()
		self._notifySink = None

	def ISequentialStream_RemoteWrite(
		self,
		this: int,
		pv: _Pointer[c_ubyte],
		cb: int,
		pcbWritten: _Pointer[c_ulong],
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
		if synth._isCancelling:
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
		plibNewPosition: _Pointer[_ULARGE_INTEGER],
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
		if dwOrigin == 1 and dlibMove == 0:
			# SAPI is querying the current position.
			if plibNewPosition:
				plibNewPosition[0] = self._writtenBytes
			return hresult.S_OK
		return hresult.E_NOTIMPL

	def IStream_Commit(self, grfCommitFlags: int):
		"""This is called when MSSP wants to flush the written data.
		Does nothing."""
		pass

	def ISpStreamFormat_GetFormat(self, pguidFormatId: _Pointer[GUID]) -> _Pointer[WAVEFORMATEX]:
		# pguidFormatId is actually an out parameter
		pguidFormatId.contents = SPDFID_WaveFormatEx
		pwfx = cast(windll.ole32.CoTaskMemAlloc(sizeof(WAVEFORMATEX)), POINTER(WAVEFORMATEX))
		if not pwfx:
			raise COMError(hresult.E_OUTOFMEMORY, "CoTaskMemAlloc failed", (None, None, None, None, None))
		memmove(pwfx, byref(self.waveFormat), sizeof(WAVEFORMATEX))
		return pwfx

	def ISpAudio_SetState(self, NewState: SPAUDIOSTATE, ullReserved: int):
		pass

	def ISpAudio_SetFormat(self, rguidFmtId: _Pointer[GUID], pWaveFormatEx: _Pointer[WAVEFORMATEX]):
		if rguidFmtId.contents != SPDFID_WaveFormatEx:
			return
		memmove(byref(self.waveFormat), pWaveFormatEx, sizeof(WAVEFORMATEX))
		# Force the wave format to be 16-bit integer (which Sonic uses internally).
		# SAPI will convert the format for us if it isn't supported by the voice.
		wfx = self.waveFormat
		wfx.wFormatTag = nvwave.WAVE_FORMAT_PCM
		wfx.cbSize = 0
		if wfx.nChannels > 2:
			wfx.nChannels = 2
		wfx.wBitsPerSample = 16
		wfx.nBlockAlign = wfx.nChannels * 2
		wfx.nAvgBytesPerSec = wfx.nSamplesPerSec * wfx.nBlockAlign

	@staticmethod
	def _writeDefaultFormat(wfx: WAVEFORMATEX) -> None:
		# default format: 48kHz 16-bit stereo
		wfx.wFormatTag = nvwave.WAVE_FORMAT_PCM
		wfx.cbSize = 0
		wfx.nChannels = 2
		wfx.nSamplesPerSec = 48000
		wfx.wBitsPerSample = 16
		wfx.nBlockAlign = 4
		wfx.nAvgBytesPerSec = 48000 * 4

	def ISpAudio_GetDefaultFormat(self) -> tuple[GUID, _Pointer[WAVEFORMATEX]]:
		pwfx = cast(windll.ole32.CoTaskMemAlloc(sizeof(WAVEFORMATEX)), POINTER(WAVEFORMATEX))
		if not pwfx:
			raise COMError(hresult.E_OUTOFMEMORY, "CoTaskMemAlloc failed", (None, None, None, None, None))
		self._writeDefaultFormat(pwfx.contents)
		return (SPDFID_WaveFormatEx, pwfx)

	def ISpAudio_EventHandle(self) -> c_void_p:
		return None

	def ISpNotifySource_SetNotifySink(self, pNotifySink: _Pointer[ISpNotifySink]):
		self._notifySink = pNotifySink

	def ISpNotifySource_GetNotifyEventHandle(self) -> c_void_p:
		return None

	def ISpEventSource_SetInterest(self, ullEventInterest: int, ullQueuedInterest: int):
		pass

	def ISpEventSource_GetEvents(
		self, this: int, ulCount: int, pEventArray: _Pointer[SPEVENT], pulFetched: _Pointer[c_ulong]
	):
		countToFetch = min(ulCount, len(self._events))
		if pulFetched:
			pulFetched[0] = countToFetch
		for i in range(countToFetch):
			self._events.popleft().copyTo(pEventArray[i])

	def ISpEventSink_AddEvents(self, pEventArray: _Pointer[SPEVENT], ulCount: int):
		for i in range(ulCount):
			event = _SapiEvent()
			event.copyFrom(pEventArray[i])
			self._events.append(event)
		if self._notifySink:
			self._notifySink.Notify()


class SapiSink(COMObject):
	"""
	Implements ISpNotifySink to handle SAPI event notifications.
	Should be passed to ISpNotifySource::SetNotifySink().
	Notifications will be sent on the original thread,
	instead of being routed to the main thread.
	"""

	_com_interfaces_ = [ISpNotifySink]

	def __init__(self, synthRef: weakref.ReferenceType["SynthDriver"]):
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
		for event in _SapiEvent.enumerateFrom(eventSource):
			if event.eEventId == 1:  # SPEI_START_INPUT_STREAM
				self.StartStream(event.ulStreamNum, event.ullAudioStreamOffset)
			elif event.eEventId == 2:  # SPEI_END_INPUT_STREAM
				self.EndStream(event.ulStreamNum, event.ullAudioStreamOffset)
			elif event.eEventId == 4:  # SPEI_TTS_BOOKMARK
				self.Bookmark(
					event.ulStreamNum,
					event.ullAudioStreamOffset,
					event.getString(),
					event.wParam,
				)

	def StartStream(self, streamNum: int, pos: int):
		synth = self.synthRef()
		if synth._audioDucker:
			if audioDucking._isDebug():
				log.debug("Enabling audio ducking due to starting speech stream")
			synth._audioDucker.enable()

	def Bookmark(self, streamNum: int, pos: int, bookmark: str, bookmarkId: int):
		synth = self.synthRef()
		if synth._isCancelling:
			return
		if synth.player:
			# Bookmark event is raised before the audio after that point.
			# Queue an IndexReached event at this point.
			synth.player.feed(None, 0, lambda: self.onIndexReached(streamNum, bookmarkId))
		else:
			# Bookmark notifications should be sent immediately when WASAPI is off.
			self.onIndexReached(streamNum, bookmarkId)

	def EndStream(self, streamNum: int, pos: int):
		synth = self.synthRef()
		if synth._isCancelling:
			return
		if synth.player:
			# Flush the stream and get the remaining data.
			synth.sonicStream.flush()
			audioData = synth.sonicStream.readShort()
			synth.player.feed(audioData, len(audioData) * 2)
		# trigger all untriggered bookmarks
		if synth._bookmarkLists:
			for bookmark in synth._bookmarkLists[0]:
				synthIndexReached.notify(synth=synth, index=bookmark)
			synth._bookmarkLists.pop()
		synthDoneSpeaking.notify(synth=synth)
		if synth.player:
			# notify the thread
			with synth._threadCond:
				synth._requestCompleted = True
				synth._threadCond.notify()
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
		if synth._bookmarkLists:
			bookmarks = synth._bookmarkLists[0]
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
		self._isCancelling = False
		self._isTerminating = False
		self._rateBoost = False
		self._initTts(_defaultVoiceToken)
		self._bookmarkLists: deque[deque[int]] = deque()
		self._thread = threading.Thread(target=self._speakThread, name="Sapi5SpeakThread")
		self._threadCond = threading.Condition()
		self._speakRequests: deque[_SpeakRequest] = deque()
		self._requestCompleted = False
		self._thread.start()

	def terminate(self):
		# Wake up and wait for the speak thread.
		self._isTerminating = True
		with self._threadCond:
			self._threadCond.notify_all()
		self._thread.join()
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

	def _initWasapiAudio(self):
		audioObject = SynthDriverAudioStream(weakref.ref(self))
		spVoice = self.tts.QueryInterface(ISpVoice)
		spVoice.SetOutput(audioObject, True)
		wfx = audioObject.waveFormat

		self.player = nvwave.WavePlayer(
			channels=wfx.nChannels,
			samplesPerSec=wfx.nSamplesPerSec,
			bitsPerSample=wfx.wBitsPerSample,
			outputDevice=config.conf["audio"]["outputDevice"],
		)

		sonicInitialize()
		self.sonicStream = SonicStream(wfx.nSamplesPerSec, wfx.nChannels)

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

	def _speakThread(self):
		# Handles speak requests in the queue one by one.
		# Only one request will be processed (spoken) at a time.
		# We don't use SAPI5's built-in speech queue,
		# because SpVoice.Speak() waits for SAPI5's audio thread,
		# and if the audio thread waits for WavePlayer.idle(),
		# SpVoice.Speak() will also block, causing dead-locks sometimes (#18298).
		# Here we manage the queue ourselves, and call WavePlayer.idle() here
		# to avoid blocking the audio thread or the main thread.

		# condition variable predicates
		def requestsAvailable() -> bool:
			return self._speakRequests or self._isCancelling or self._isTerminating

		def requestCompleted() -> bool:
			return self._requestCompleted or self._isCancelling or self._isTerminating

		request: _SpeakRequest | None = None

		# Process requests one by one.
		while not self._isTerminating:
			# Fetch the next request
			with self._threadCond:
				self._threadCond.wait_for(requestsAvailable)
				if self._speakRequests:
					request = self._speakRequests.popleft()
					self._requestCompleted = False
			if request is not None:  # There is one request
				text, bookmarks = request
				self._bookmarkLists.append(bookmarks)
				try:
					# Process one request, and wait for it to finish
					self.tts.Speak(text, SpeechVoiceSpeakFlags.IsXML | SpeechVoiceSpeakFlags.Async)
					with self._threadCond:
						self._threadCond.wait_for(requestCompleted)
				except Exception:
					self._bookmarkLists.pop()
					log.error("Error speaking", exc_info=True)
				request = None
				if not requestsAvailable():
					# No more requests, so call idle().
					self.player.idle()
			if self._isCancelling:
				self.tts.Speak(None, SpeechVoiceSpeakFlags.Async | SpeechVoiceSpeakFlags.PurgeBeforeSpeak)
				# clear the queue
				with self._threadCond:
					self._speakRequests.clear()
					self._bookmarkLists.clear()
					if self.sonicStream:
						self.sonicStream.flush()
						self.sonicStream.readShort()  # discard data left in stream
					self._isCancelling = False

	def speak(self, speechSequence):
		textList = []
		bookmarks: deque[int] = deque()

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
			with self._threadCond:  # put the request in queue and wake up the thread
				self._speakRequests.append(_SpeakRequest(text, bookmarks))
				self._threadCond.notify()
		else:
			self._bookmarkLists.append(bookmarks)
			try:
				self._speak_legacy(text, flags)
			except:
				self._bookmarkLists.pop()
				raise

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
		self._isCancelling = True
		if self.player:
			self.player.stop()  # stop the audio and stop waiting for idle()
			with self._threadCond:  # wake up the thread
				self._threadCond.notify()
		if self.ttsAudioStream:
			self.ttsAudioStream.setState(_SPAudioState.STOP, 0)
			self.tts.Speak(None, SpeechVoiceSpeakFlags.Async | SpeechVoiceSpeakFlags.PurgeBeforeSpeak)
			if self._audioDucker:
				if audioDucking._isDebug():
					log.debug("Disabling audio ducking due to setting output audio state to stop")
				self._audioDucker.disable()
			self._bookmarkLists.clear()

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
