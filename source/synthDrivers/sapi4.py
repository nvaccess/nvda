# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2025 NV Access Limited, Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from datetime import datetime
import locale
from collections import OrderedDict, deque
import threading
import winreg
from comtypes import CoCreateInstance, COMObject, COMError, GUID, hresult, ReturnHRESULT
from ctypes import (
	addressof,
	byref,
	c_ulong,
	c_ulonglong,
	POINTER,
	c_void_p,
	cast,
	memmove,
	string_at,
	sizeof,
	windll,
)
from ctypes.wintypes import BOOL, DWORD, FILETIME, WORD
from typing import TYPE_CHECKING, Optional, TypeAlias
import nvwave
from synthDriverHandler import SynthDriver, VoiceInfo, synthIndexReached, synthDoneSpeaking
from logHandler import log
from ._sapi4 import (
	AudioError,
	SDATA,
	CLSID_TTSEnumerator,
	IAudio,
	IAudioDest,
	IAudioDestNotifySink,
	ITTSAttributes,
	ITTSBufNotifySink,
	ITTSCentralW,
	ITTSEnumW,
	ITTSNotifySinkW,
	TextSDATA,
	TTSATTR_MAXPITCH,
	TTSATTR_MAXSPEED,
	TTSATTR_MAXVOLUME,
	TTSATTR_MINPITCH,
	TTSATTR_MINSPEED,
	TTSATTR_MINVOLUME,
	TTSDATAFLAG_TAGGED,
	TTSFEATURE_PITCH,
	TTSFEATURE_SPEED,
	TTSFEATURE_VOLUME,
	TTSMODEINFO,
	VOICECHARSET,
)
import config
import weakref

from speech.commands import (
	IndexCommand,
	SpeechCommand,
	CharacterModeCommand,
	BreakCommand,
	PitchCommand,
	RateCommand,
	VolumeCommand,
	BaseProsodyCommand,
)
from speech.types import SpeechSequence


class SynthDriverBufSink(COMObject):
	_com_interfaces_ = [ITTSBufNotifySink]

	def __init__(self, synthRef: weakref.ReferenceType):
		self.synthRef = synthRef
		self._allowDelete = True
		super().__init__()

	def ITTSBufNotifySink_BookMark(self, this, qTimeStamp: int, dwMarkNum: int):
		synth = self.synthRef()
		if synth is None:
			log.debugWarning(
				"Called ITTSBufNotifySink_BookMark method on ITTSBufNotifySink while driver is dead",
			)
			return
		synthIndexReached.notify(synth=synth, index=dwMarkNum)
		if synth._finalIndex == dwMarkNum:
			synth._finalIndex = None
			synthDoneSpeaking.notify(synth=synth)
		# remove already triggered bookmarks
		while synth._bookmarks:
			if synth._bookmarks.popleft() == dwMarkNum:
				break

	def IUnknown_Release(self, this, *args, **kwargs):
		if not self._allowDelete and self._refcnt.value == 1:
			log.debugWarning("ITTSBufNotifySink::Release called too many times by engine")
			return 1
		return super(SynthDriverBufSink, self).IUnknown_Release(this, *args, **kwargs)


if TYPE_CHECKING:
	from ctypes import _Pointer

	c_ulonglong_p = _Pointer[c_ulonglong]
	LP_IAudioDestNotifySink = _Pointer[IAudioDestNotifySink]
else:
	c_ulonglong_p = POINTER(c_ulonglong)
	LP_IAudioDestNotifySink = POINTER(IAudioDestNotifySink)

AudioT: TypeAlias = bytes
BookmarkT: TypeAlias = int


class SynthDriverAudio(COMObject):
	"""
	Implements IAudio and IAudioDest to receive streamed in audio data.
	An instance of this class will be passed to,
	and be used by the TTS engine.

	Typically, an engine does the following things to output audio.
	(Note that different engines may have different implementations)

	- Initialize, such as setting wave format with `WaveFormatSet`, setting notify sink with `PassNotify`, etc.
	- Call `Claim` to prepare the audio output.
	- Call `DataSet` to prepare some initial audio data.
	- Call `Start` to start playing.
	- Call `DataSet` to provide more audio data,
	  and call `BookMark` when the engine want to know when audio reaches a specific point.
	- Call `UnClaim` when all the audio has been written. The audio will still be played to the end.
	- When pausing the audio, it calls `Stop` and `UnClaim`.
	- When unpausing the audio, it calls `Claim` and `Start`.
	- When resetting the audio, it calls `Stop`, `Flush`, and `UnClaim`.
	  `Stop` and `UnClaim` will not clear the buffer, but `Flush` will.
	"""

	_com_interfaces_ = [IAudio, IAudioDest]

	def __init__(self):
		self._notifySink: LP_IAudioDestNotifySink | None = None
		self._deviceClaimed = False
		self._deviceStarted = False
		self._deviceUnClaiming = False
		self._deviceUnClaimingBytePos: int | None = None
		self._waveFormat: nvwave.WAVEFORMATEX | None = None
		self._player: nvwave.WavePlayer | None = None
		self._writtenBytes = 0
		self._playedBytes = 0
		self._startTime = datetime.now()
		self._startBytes = 0
		self._audioQueue: deque[AudioT | BookmarkT] = deque()
		self._audioCond = threading.Condition()
		self._audioStopped = False
		self._audioThread = threading.Thread(target=self._audioThreadFunc)
		self._audioThread.start()
		self._level = 0xFFFFFFFF  # defaults to maximum value (0xFFFF) for both channels (low and high word)

	def terminate(self):
		with self._audioCond:
			self._audioStopped = True
			self._audioCond.notify()
		if self._audioThread is not threading.current_thread():
			self._audioThread.join()
		self._notifySink = None

	def __del__(self):
		self.terminate()

	def _maybeInitPlayer(self) -> None:
		"""Initialize audio playback based on the wave format provided by the engine.
		If the format has not changed, the existing player is used.
		Otherwise, a new one is created with the appropriate parameters."""
		if self._player:
			# Reuse the previous player if possible (using the same format)
			if (
				self._player.channels == self._waveFormat.nChannels
				and self._player.samplesPerSec == self._waveFormat.nSamplesPerSec
				and self._player.bitsPerSample == self._waveFormat.wBitsPerSample
			):
				return  # same format, use the previous player
			# different format, close and recreate a new player
			self._player.stop()
		self._player = nvwave.WavePlayer(
			channels=self._waveFormat.nChannels,
			samplesPerSec=self._waveFormat.nSamplesPerSec,
			bitsPerSample=self._waveFormat.wBitsPerSample,
			outputDevice=config.conf["audio"]["outputDevice"],
		)
		self._player.open()
		self.IAudio_LevelSet(self._level)

	def IAudio_Flush(self) -> None:
		"""Clears the object's internal buffer and resets the audio device,
		but does not stop playing the audio data afterwards."""
		if self._player:
			self._player.stop()
		with self._audioCond:
			if self._notifySink:
				while self._audioQueue:
					item = self._audioQueue.popleft()
					if isinstance(item, BookmarkT):
						# Flush all untriggered bookmarks.
						# 1 (TRUE) means that the bookmark is sent because of flushing.
						self._notifySink.BookMark(item, 1)
			self._audioQueue.clear()

	def IAudio_LevelGet(self) -> int:
		"""Returns the volume level, ranging from 0x0000 to 0xFFFF.
		Low word is for the left (or mono) channel, and high word is for the right channel."""
		return self._level

	def IAudio_LevelSet(self, dwLevel: int) -> None:
		"""Sets the volume level, ranging from 0x0000 to 0xFFFF.
		Low word is for the left (or mono) channel, and high word is for the right channel."""
		self._level = dwLevel
		if dwLevel & 0xFFFF0000:
			self._player.setVolume(left=float(dwLevel & 0xFFFF) / 0xFFFF, right=float(dwLevel >> 16) / 0xFFFF)
		else:
			self._player.setVolume(all=float(dwLevel) / 0xFFFF)

	def IAudio_PassNotify(self, pNotifyInterface: c_void_p, IIDNotifyInterface: GUID) -> None:
		"""Passes in an implementation of IAudioDestNotifySink to receive notifications.
		The previous sink, if exists, will be released and replaced.
		Allows specifying NULL for no sink."""
		if IIDNotifyInterface != IAudioDestNotifySink._iid_:
			log.debugWarning("Only IAudioDestNotifySink is allowed")
			raise ReturnHRESULT(AudioError.INVALID_NOTIFY_SINK, None)
		if self._notifySink:
			self._notifySink = None
		if pNotifyInterface:
			self._notifySink = cast(pNotifyInterface, LP_IAudioDestNotifySink)

	def IAudio_PosnGet(self) -> int:
		"""Returns the byte position currently being played,
		which should increase monotonically and never reset."""
		return self._playedBytes

	def IAudio_Claim(self) -> None:
		"""Acquires (opens) the multimedia device.
		Called before the engine wants to write audio data.
		`IAudioDestNotifySink::AudioStart()` will be called to notify the engine.
		Previous buffer should not be cleared.
		If Claim is called before unclaiming completes, unclaiming is canceled,
		and neither AudioStop nor AudioStart is notified."""
		if not self._waveFormat:
			raise ReturnHRESULT(AudioError.NEED_WAVE_FORMAT, None)
		with self._audioCond:
			if self._deviceUnClaiming:
				# Unclaiming is cancelled, but nothing else is touched.
				self._deviceUnClaiming = False
				self._deviceUnClaimingBytePos = None
				return
		if self._deviceClaimed:
			raise ReturnHRESULT(AudioError.ALREADY_CLAIMED, None)
		self._maybeInitPlayer()
		self._deviceClaimed = True
		if self._notifySink:
			self._notifySink.AudioStart()

	def IAudio_UnClaim(self) -> None:
		"""Releases the multimedia device asynchronously.
		Called after the engine completes writing all audio data.
		If there is audio in the buffer, it should still be played till the end.
		`IAudioDestNotifySink::AudioStop()` will be called after the audio completely stops."""
		if not self._deviceClaimed:
			raise ReturnHRESULT(AudioError.NOT_CLAIMED, None)
		if self._deviceStarted:
			# When playing, wait for the playback to finish.
			with self._audioCond:
				self._deviceUnClaiming = True
				self._deviceUnClaimingBytePos = self._writtenBytes
				self._audioCond.notify()
		else:
			# When not playing, this can finish immediately.
			if self._writtenBytes == self._playedBytes and not self._audioQueue:
				# If all audio is done playing, stop the player.
				self._player.stop()
			self._deviceClaimed = False
			if self._notifySink:
				self._notifySink.AudioStop(0)  # IANSRSN_NODATA

	def IAudio_Start(self) -> None:
		"""Starts (or resumes) playing the audio in the buffer."""
		if self._deviceStarted:
			raise ReturnHRESULT(AudioError.ALREADY_STARTED, None)
		if not self._deviceClaimed:
			raise ReturnHRESULT(AudioError.NOT_CLAIMED, None)
		self._startTime = datetime.now()
		self._startBytes = self._playedBytes
		try:
			self._player.pause(False)
		except OSError:
			log.debugWarning("Error starting audio", exc_info=True)
		with self._audioCond:
			self._deviceStarted = True
			self._audioCond.notify()

	def IAudio_Stop(self) -> None:
		"""Stops (or pauses) playing, without clearing the buffer.
		If there is audio in the buffer, calling Stop and UnClaim should keep the buffer
		and only pause the playback."""
		if not self._deviceStarted:
			return  # no error returned
		try:
			self._player.pause(True)
		except OSError:
			log.debugWarning("Error stopping audio", exc_info=True)
		with self._audioCond:
			self._deviceStarted = False
			self._audioCond.notify()

	def IAudio_TotalGet(self) -> int:
		"""Returns the total number of bytes written,
		including the unplayed bytes in the buffer,
		which should increase monotonically and never reset."""
		return self._writtenBytes

	def IAudio_ToFileTime(self, pqWord: c_ulonglong_p) -> None:
		"""Converts a byte position to UTC FILETIME."""
		if not self._waveFormat:
			raise ReturnHRESULT(AudioError.NEED_WAVE_FORMAT, None)
		UNIX_TIME_CONV = 1_1644_473_600
		filetime_ticks = int((self._startTime.timestamp() + UNIX_TIME_CONV) * 10_000_000)
		filetime_ticks += (pqWord[0] - self._startBytes) * 10_000_000 // self._waveFormat.nAvgBytesPerSec
		return FILETIME(filetime_ticks & 0xFFFFFFFF, filetime_ticks >> 32)

	def IAudio_WaveFormatGet(self) -> SDATA:
		"""Gets a copy of the current wave format.
		:returns: A pointer to the WAVEFORMATEX structure.
			Should be freed by the caller using CoTaskMemFree."""
		if not self._waveFormat:
			raise ReturnHRESULT(AudioError.NEED_WAVE_FORMAT, None)
		size = sizeof(nvwave.WAVEFORMATEX)
		ptr = windll.ole32.CoTaskMemAlloc(size)
		if not ptr:
			raise COMError(hresult.E_OUTOFMEMORY, "CoTaskMemAlloc failed", (None, None, None, None, None))
		memmove(ptr, addressof(self._waveFormat), size)
		return SDATA(ptr, size)

	def IAudio_WaveFormatSet(self, dWFEX: SDATA) -> None:
		"""Sets the current wave format. Only integer PCM formats are supported."""
		size = 18  # SAPI4 uses 18 bytes without the final padding
		if dWFEX.dwSize < size:
			log.debugWarning("Invalid wave format size")
			raise ReturnHRESULT(hresult.E_INVALIDARG, None)
		pWfx = cast(dWFEX.pData, POINTER(nvwave.WAVEFORMATEX))
		if pWfx[0].wFormatTag != nvwave.WAVE_FORMAT_PCM:
			log.debugWarning("Wave format not supported. Only integer PCM formats are supported.")
			raise ReturnHRESULT(AudioError.WAVE_FORMAT_NOT_SUPPORTED, None)
		if self._deviceStarted or self._audioQueue:
			log.debugWarning("Cannot change wave format during playback.")
			raise ReturnHRESULT(AudioError.WAVE_FORMAT_NOT_SUPPORTED, None)
		self._waveFormat = nvwave.WAVEFORMATEX()
		memmove(addressof(self._waveFormat), pWfx, size)

	def _getFreeSpace(self) -> int:
		if not self._waveFormat:
			raise ReturnHRESULT(AudioError.NEED_WAVE_FORMAT, None)
		return self._waveFormat.nAvgBytesPerSec // 5  # always 200ms

	def IAudioDest_FreeSpace(self) -> tuple[DWORD, BOOL]:
		"""Returns the number of bytes that are free in the object's internal buffer.
		:returns: Tuple (dwBytes, fEOF).
			dwBytes: number of bytes available.
			fEOF: TRUE if end-of-file is reached and no more data can be sent."""
		return (self._getFreeSpace(), 0)

	def IAudioDest_DataSet(self, pBuffer: c_void_p, dwSize: int) -> None:
		"""Writes audio data to the end of the object's internal buffer.
		This should not block.
		When data cannot fit in the buffer, this should return AudioError.NOT_ENOUGH_DATA immediately."""
		if not self._deviceClaimed or self._deviceUnClaiming:
			log.debugWarning("Audio data written when device is not claimed")
			raise ReturnHRESULT(AudioError.NOT_CLAIMED, None)
		with self._audioCond:
			self._audioQueue.append(string_at(pBuffer, dwSize))
			self._writtenBytes += dwSize
			self._audioCond.notify()

	def IAudioDest_BookMark(self, dwMarkID: BookmarkT) -> None:
		"""Attaches a bookmark to the most recent data in the audio-destination object's internal buffer.
		When the bookmark is reached, `IAudioDestNotifySink::BookMark` is called.
		When Flush is called, untriggered bookmarks should also be triggered."""
		with self._audioCond:
			self._audioQueue.append(dwMarkID)

	def _audioThreadFunc(self):
		"""Audio thread function that feeds the audio data from queue to WavePlayer."""
		while True:
			with self._audioCond:
				while not self._audioStopped and not (self._deviceStarted and self._audioQueue):
					if self._deviceStarted:
						# Since WavePlayer.feed returns before the audio finishes,
						# in order not to lose the final callbacks
						# when there's no more audio to feed,
						# wait with a timeout to give WavePlayer a chance
						# to check the callbacks periodically.
						self._audioCond.wait(0.1)
					else:
						self._audioCond.wait()
					if self._deviceStarted and self._audioQueue:
						break
					if not self._player:
						continue
					if self._deviceUnClaimingBytePos is not None:
						# Closing in progress, wait for the audio to finish
						self._player.feed(
							None,
							0,
							lambda bytePos=self._deviceUnClaimingBytePos: self._finishUnClaim(bytePos),
						)
						self._deviceUnClaimingBytePos = None
					else:
						# Call feed to let WavePlayer check the callbacks
						self._player.feed(None, 0, None)
				if self._audioStopped:
					return
				item = self._audioQueue.popleft()
			if isinstance(item, AudioT):
				self._player.feed(item, len(item), lambda item=item: self._onChunkFinished(item))
			elif isinstance(item, BookmarkT):
				if self._playedBytes == self._writtenBytes:
					self._onBookmark(item)  # trigger immediately
				else:
					self._player.feed(None, 0, lambda item=item: self._onBookmark(item))

	def _onChunkFinished(self, chunk: AudioT):
		self._playedBytes += len(chunk)
		if self._notifySink:
			self._notifySink.FreeSpace(self._getFreeSpace(), 0)

	def _onBookmark(self, dwMarkID: BookmarkT):
		if self._notifySink:
			self._notifySink.BookMark(dwMarkID, 0)

	def _finishUnClaim(self, bytePos: int):
		"""Finishes the asynchronous UnClaim call.

		:param bytePos: The written byte count when this UnClaim request is made.
			This is checked to prevent triggering on outdated UnClaim requests."""
		if not self._deviceUnClaiming or self._writtenBytes != bytePos:
			return
		self._player.stop()
		self._deviceStarted = False
		self._deviceUnClaiming = False
		self._deviceClaimed = False
		if self._notifySink:
			# Notify when the device is finally closed
			self._notifySink.AudioStop(0)  # IANSRSN_NODATA


class SynthDriverSink(COMObject):
	_com_interfaces_ = [ITTSNotifySinkW]

	def __init__(self, synthRef: weakref.ReferenceType):
		self.synthRef = synthRef
		super().__init__()

	def ITTSNotifySinkW_AudioStart(self, this, qTimeStamp: int):
		synth = self.synthRef()
		if synth is None:
			log.debugWarning(
				"Called ITTSNotifySinkW_AudioStart method on ITTSNotifySinkW while driver is dead",
			)
			return
		if synth._bookmarkLists:
			# take the first bookmark list
			synth._bookmarks = synth._bookmarkLists.popleft()

	def ITTSNotifySinkW_AudioStop(self, this, qTimeStamp: int):
		synth = self.synthRef()
		if synth is None:
			log.debugWarning(
				"Called ITTSNotifySinkW_AudioStop method on ITTSNotifySinkW while driver is dead",
			)
			return
		# trigger all untriggered bookmarks
		if synth._bookmarks:
			while synth._bookmarks:
				synthIndexReached.notify(synth=synth, index=synth._bookmarks.popleft())
			# if there are untriggered bookmarks, synthDoneSpeaking hasn't been triggered yet.
			# Trigger synthDoneSpeaking after triggering all bookmarks
			synth._finalIndex = None
			synthDoneSpeaking.notify(synth=synth)
		synth._bookmarks = None


class SynthDriver(SynthDriver):
	name = "sapi4"
	description = "Microsoft Speech API version 4"
	supportedSettings = [SynthDriver.VoiceSetting()]
	supportedCommands = {
		IndexCommand,
		CharacterModeCommand,
		BreakCommand,
	}
	supportedNotifications = {synthIndexReached, synthDoneSpeaking}

	@classmethod
	def check(cls):
		try:
			winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"CLSID\%s" % CLSID_TTSEnumerator).Close()
			return True
		except WindowsError:
			return False

	def _fetchEnginesList(self):
		enginesList = []
		self._ttsEngines.Reset()
		while True:
			mode = TTSMODEINFO()
			fetched = c_ulong()
			try:
				self._ttsEngines.Next(1, byref(mode), byref(fetched))
			except:  # noqa: E722
				log.error("can't get next engine", exc_info=True)
				break
			if fetched.value == 0:
				break
			enginesList.append(mode)
		return enginesList

	def __init__(self):
		self._finalIndex: Optional[int] = None
		self._ttsCentral = None
		self._sinkRegKey = DWORD()
		self._bookmarks = None
		self._bookmarkLists = deque()
		self._sink = SynthDriverSink(weakref.ref(self))
		self._sinkPtr = self._sink.QueryInterface(ITTSNotifySinkW)
		self._bufSink = SynthDriverBufSink(weakref.ref(self))
		self._bufSinkPtr = self._bufSink.QueryInterface(ITTSBufNotifySink)
		self._ttsAudio: SynthDriverAudio | None = None
		# HACK: Some buggy engines call Release() too many times on our buf sink.
		# Therefore, don't let the buf sink be deleted before we release it ourselves.
		self._bufSink._allowDelete = False
		self._ttsEngines = CoCreateInstance(CLSID_TTSEnumerator, ITTSEnumW)
		self._enginesList = self._fetchEnginesList()
		if len(self._enginesList) == 0:
			raise RuntimeError("No Sapi4 engines available")
		self._rateDelta = 0
		self._pitchDelta = 0
		self._volume = 100
		self._paused = False
		self.voice = str(self._enginesList[0].gModeID)

	def terminate(self):
		self._bufSink._allowDelete = True
		if self._ttsAudio:
			self._ttsAudio.terminate()
		self._ttsCentral = None
		self._ttsAttrs = None

	def speak(self, speechSequence: SpeechSequence):
		textList = []
		charMode = False
		unprocessedSequence = speechSequence
		bookmarks = deque()
		# #15500: Some SAPI4 voices reset all prosody when they receive any prosody command,
		# whereas other voices never undo prosody changes when a sequence is interrupted.
		# Add all default values to the start and end of the sequence,
		# but avoid duplicating the first command, if any,
		# And only add the defaults when there is a prosody command in the sequence.
		supportedProsody = [c for c in self.supportedCommands if issubclass(c, BaseProsodyCommand)]
		prosodyToAdd = []
		if any(type(i) in supportedProsody for i in unprocessedSequence):
			prosodyToAdd.extend(c() for c in supportedProsody)
		speechSequence = [c for c in prosodyToAdd if not isinstance(unprocessedSequence[0], type(c))]
		speechSequence.extend(unprocessedSequence)
		# To be sure, add all default values to the end of the sequence.
		# This might cause multiple cases of prosody resets, but better safe than sorry.
		speechSequence.extend(prosodyToAdd)
		lastHandledIndexInSequence = 0
		for item in speechSequence:
			if isinstance(item, str):
				textList.append(item.replace("\\", "\\\\"))
			elif isinstance(item, IndexCommand):
				textList.append("\\mrk=%d\\" % item.index)
				bookmarks.append(item.index)
				lastHandledIndexInSequence = item.index
			elif isinstance(item, CharacterModeCommand):
				textList.append("\\RmS=1\\" if item.state else "\\RmS=0\\")
				charMode = item.state
			elif isinstance(item, BreakCommand):
				textList.append(f"\\Pau={item.time}\\")
			elif isinstance(item, PitchCommand):
				val = self._percentToParam(item.newValue, self._minPitch, self._maxPitch)
				textList.append(f"\\Pit={val}\\")
			elif isinstance(item, RateCommand):
				val = self._percentToParam(item.newValue, self._minRate, self._maxRate)
				textList.append(f"\\Spd={val}\\")
			elif isinstance(item, VolumeCommand):
				val = self._percentToParam(item.newValue, self._minVolume, self._maxVolume)
				# If you specify a value greater than 65535, the engine assumes that you want to set the
				# left and right channels separately and converts the value to a double word,
				# using the low word for the left channel and the high word for the right channel.
				val |= val << 16
				textList.append(f"\\Vol={val}\\")
			elif isinstance(item, SpeechCommand):
				log.debugWarning("Unsupported speech command: %s" % item)
			else:
				log.error("Unknown speech: %s" % item)
		# lastHandledIndexInSequence is the index denoting the end of the speech sequence.
		# store it on the driver to support the synthDoneSpeaking notification.
		self._finalIndex = lastHandledIndexInSequence
		if charMode:
			# Some synths stay in character mode if we don't explicitly disable it.
			textList.append("\\RmS=0\\")
		# Some SAPI4 synthesizers complete speech sequence just after the last text
		# and ignore any indexes passed after it
		# Therefore we add the pause of 1ms at the end
		textList.append("\\PAU=1\\")
		text = "".join(textList)
		self._bookmarkLists.append(bookmarks)
		flags = TTSDATAFLAG_TAGGED
		self._ttsCentral.TextData(
			VOICECHARSET.CHARSET_TEXT,
			flags,
			TextSDATA(text),
			self._bufSinkPtr,
			ITTSBufNotifySink._iid_,
		)

	def cancel(self):
		try:
			# cancel all pending bookmarks
			self._bookmarkLists.clear()
			self._bookmarks = None
			if self._paused:
				# Unpause the voice before resetting,
				# because some voices keep the pausing state
				# even after resetting.
				self._ttsCentral.AudioResume()
				self._paused = False
			self._ttsCentral.AudioReset()
		except COMError:
			log.debugWarning("Error cancelling speech", exc_info=True)
		finally:
			self._finalIndex = None

	def pause(self, switch: bool):
		if switch:
			try:
				self._ttsCentral.AudioPause()
			except COMError:
				log.debugWarning("Error pausing speech", exc_info=True)
		else:
			self._ttsCentral.AudioResume()
		self._paused = switch

	def removeSetting(self, name):
		# Putting it here because currently no other synths make use of it. OrderedDict, where you are?
		for i, s in enumerate(self.supportedSettings):
			if s.id == name:
				del self.supportedSettings[i]
				return

	def _set_voice(self, val):
		try:
			val = GUID(val)
		except:  # noqa: E722
			val = self._enginesList[0].gModeID
		mode = None
		for mode in self._enginesList:
			if mode.gModeID == val:
				break
		if mode is None:
			raise ValueError("no such mode: %s" % val)
		self._currentMode = mode
		if self._ttsAudio:
			self._ttsAudio.terminate()
		self._ttsAudio = SynthDriverAudio()
		if self._ttsCentral:
			try:
				# Some SAPI4 synthesizers may fail this call.
				self._ttsCentral.UnRegister(self._sinkRegKey)
			except COMError:
				log.debugWarning("Error unregistering ITTSCentral sink", exc_info=True)
			# Some SAPI4 synthesizers assume that only one instance of ITTSCentral
			# will be created by the client, and will stop working if more are created.
			# Here we make sure that the previous _ttsCentral is released
			# before the next _ttsCentral is created.
			self._ttsCentral = None
			self._ttsAttrs = None
		self._ttsCentral = POINTER(ITTSCentralW)()
		self._ttsEngines.Select(self._currentMode.gModeID, byref(self._ttsCentral), self._ttsAudio)
		self._ttsCentral.Register(self._sinkPtr, ITTSNotifySinkW._iid_, byref(self._sinkRegKey))
		self._ttsAttrs = self._ttsCentral.QueryInterface(ITTSAttributes)
		# Find out rate limits
		hasRate = bool(mode.dwFeatures & TTSFEATURE_SPEED)
		if hasRate:
			try:
				oldVal = DWORD()
				self._ttsAttrs.SpeedGet(byref(oldVal))
				self._defaultRate = oldVal.value
				self._ttsAttrs.SpeedSet(TTSATTR_MINSPEED)
				newVal = DWORD()
				self._ttsAttrs.SpeedGet(byref(newVal))
				self._minRate = newVal.value
				self._ttsAttrs.SpeedSet(TTSATTR_MAXSPEED)
				self._ttsAttrs.SpeedGet(byref(newVal))
				# ViaVoice (and perhaps other synths) doesn't seem to like the speed being set to maximum.
				self._maxRate = newVal.value - 1
				val = max(self._minRate, min(self._maxRate, self._defaultRate + self._rateDelta))
				self._ttsAttrs.SpeedSet(val)
				if self._maxRate <= self._minRate:
					hasRate = False
			except COMError:
				hasRate = False
		if hasRate:
			if not self.isSupported("rate"):
				self.supportedSettings.insert(1, SynthDriver.RateSetting())
			self.supportedCommands.add(RateCommand)
		else:
			if self.isSupported("rate"):
				self.removeSetting("rate")
			if RateCommand in self.supportedCommands:
				self.supportedCommands.remove(RateCommand)
		# Find out pitch limits
		hasPitch = bool(mode.dwFeatures & TTSFEATURE_PITCH)
		if hasPitch:
			try:
				oldVal = WORD()
				self._ttsAttrs.PitchGet(byref(oldVal))
				self._defaultPitch = oldVal.value
				self._ttsAttrs.PitchSet(TTSATTR_MINPITCH)
				newVal = WORD()
				self._ttsAttrs.PitchGet(byref(newVal))
				self._minPitch = newVal.value
				self._ttsAttrs.PitchSet(TTSATTR_MAXPITCH)
				self._ttsAttrs.PitchGet(byref(newVal))
				self._maxPitch = newVal.value
				val = max(self._minPitch, min(self._maxPitch, self._defaultPitch + self._pitchDelta))
				self._ttsAttrs.PitchSet(val)
				if self._maxPitch <= self._minPitch:
					hasPitch = False
			except COMError:
				hasPitch = False
		if hasPitch:
			if not self.isSupported("pitch"):
				self.supportedSettings.insert(2, SynthDriver.PitchSetting())
			self.supportedCommands.add(PitchCommand)
		else:
			if self.isSupported("pitch"):
				self.removeSetting("pitch")
			if PitchCommand in self.supportedCommands:
				self.supportedCommands.remove(PitchCommand)
		# Find volume limits
		hasVolume = bool(mode.dwFeatures & TTSFEATURE_VOLUME)
		if hasVolume:
			try:
				oldVal = DWORD()
				self._ttsAttrs.VolumeGet(byref(oldVal))
				self._ttsAttrs.VolumeSet(TTSATTR_MINVOLUME)
				newVal = DWORD()
				self._ttsAttrs.VolumeGet(byref(newVal))
				self._minVolume = newVal.value & 0xFFFF
				self._ttsAttrs.VolumeSet(TTSATTR_MAXVOLUME)
				self._ttsAttrs.VolumeGet(byref(newVal))
				self._maxVolume = newVal.value & 0xFFFF
				self._set_volume(self._volume)
				if self._maxVolume <= self._minVolume:
					hasVolume = False
			except COMError:
				hasVolume = False
		if hasVolume:
			if not self.isSupported("volume"):
				self.supportedSettings.insert(3, SynthDriver.VolumeSetting())
			self.supportedCommands.add(VolumeCommand)
		else:
			if self.isSupported("volume"):
				self.removeSetting("volume")
			if VolumeCommand in self.supportedCommands:
				self.supportedCommands.remove(VolumeCommand)

	def _get_voice(self):
		return str(self._currentMode.gModeID)

	def _getAvailableVoices(self):
		voices = OrderedDict()
		for mode in self._enginesList:
			ID = str(mode.gModeID)
			name = "%s - %s" % (mode.szModeName, mode.szProductName)
			try:
				language = locale.windows_locale[mode.language.LanguageID]
			except KeyError:
				language = None
			voices[ID] = VoiceInfo(ID, name, language)
		return voices

	def _get_rate(self) -> int:
		val = DWORD()
		self._ttsAttrs.SpeedGet(byref(val))
		return self._paramToPercent(val.value, self._minRate, self._maxRate)

	def _set_rate(self, val: int):
		val = self._percentToParam(val, self._minRate, self._maxRate)
		self._ttsAttrs.SpeedSet(val)
		self._rateDelta = val - self._defaultRate

	def _get_pitch(self) -> int:
		val = WORD()
		self._ttsAttrs.PitchGet(byref(val))
		return self._paramToPercent(val.value, self._minPitch, self._maxPitch)

	def _set_pitch(self, val: int):
		val = self._percentToParam(val, self._minPitch, self._maxPitch)
		self._ttsAttrs.PitchSet(val)
		self._pitchDelta = val - self._defaultPitch

	def _get_volume(self) -> int:
		val = DWORD()
		self._ttsAttrs.VolumeGet(byref(val))
		return self._paramToPercent(val.value & 0xFFFF, self._minVolume, self._maxVolume)

	def _set_volume(self, val: int):
		self._volume = val
		val = self._percentToParam(val, self._minVolume, self._maxVolume)
		# If you specify a value greater than 65535, the engine assumes that you want to set the
		# left and right channels separately and converts the value to a double word,
		# using the low word for the left channel and the high word for the right channel.
		val |= val << 16
		self._ttsAttrs.VolumeSet(val)
