# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2025 NV Access Limited, Leonard de Ruijter, gexgd0419
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from datetime import datetime
from enum import IntEnum
from functools import wraps
import locale
from collections import OrderedDict, deque
import queue
import threading
import time
import winreg
import winBindings.ole32
import winBindings.user32
import winBindings.winmm
from winBindings.mmeapi import WAVEFORMATEX
from comtypes import CoCreateInstance, CoInitialize, COMObject, COMError, GUID, hresult, ReturnHRESULT
from ctypes import (
	addressof,
	byref,
	c_ulong,
	c_ulonglong,
	POINTER,
	c_void_p,
	c_wchar,
	cast,
	create_string_buffer,
	memmove,
	string_at,
	sizeof,
	windll,
)
from ctypes.wintypes import BOOL, DWORD, FILETIME, HANDLE, MSG, WORD
from typing import TYPE_CHECKING, Callable, NamedTuple, Optional
import nvwave
from synthDriverHandler import (
	SynthDriver,
	VoiceInfo,
	synthIndexReached,
	synthDoneSpeaking,
	isDebugForSynthDriver,
)
from logHandler import log
from ._sapi4 import (
	MMSYSERR_NOERROR,
	AudioError,
	SDATA,
	CLSID_MMAudioDest,
	CLSID_TTSEnumerator,
	DriverMessage,
	IAudio,
	IAudioDest,
	IAudioDestNotifySink,
	IAudioMultiMediaDevice,
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
	SynthCommand,
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

	def ITTSBufNotifySink_BookMark(self, this: int, qTimeStamp: int, dwMarkNum: int):
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

	def IUnknown_Release(self, this: int, *args, **kwargs):
		if not self._allowDelete and self._refcnt.value == 1:
			log.debugWarning("ITTSBufNotifySink::Release called too many times by engine")
			return 1
		return super().IUnknown_Release(this, *args, **kwargs)


if TYPE_CHECKING:
	from ctypes import _Pointer

	c_ulonglong_p = _Pointer[c_ulonglong]
	LP_IAudioDestNotifySink = _Pointer[IAudioDestNotifySink]
else:
	c_ulonglong_p = POINTER(c_ulonglong)
	LP_IAudioDestNotifySink = POINTER(IAudioDestNotifySink)

_Bookmark = NamedTuple("Bookmark", [("bytePos", int), ("id", int)])

_lastLoggedTimes: dict[Callable, float] = dict()


def _logTrace(logAll: bool = False, format: str = ""):
	"""
	Decorator that wraps the COM methods, logs the calls,
	and converts COMError exceptions to silent ReturnHRESULTs.

	:param logAll: If true, logs every call. If false (default), omits frequent calls to reduce logs. Errors are always logged.
	:param format: Format specifier for log messages. Provided format arguments are: `args`, `kwargs`, and `result`.
	"""

	def _decorator(func):
		@wraps(func)
		def _wrapper(*args, **kwargs):
			global _lastLoggedTimes
			funcname = func.__name__.split("_")[1]
			try:
				result = func(*args, **kwargs)
				if isDebugForSynthDriver():
					if logAll:
						_lastLoggedTimes.clear()
					logTime = time.time()
					# filter out calls to the same function within 10ms
					if logAll or func not in _lastLoggedTimes or logTime - _lastLoggedTimes[func] > 0.01:
						log.debug(
							f"SAPI4: {funcname} {format.format(args=args, kwargs=kwargs, result=result)}",
						)
						_lastLoggedTimes[func] = logTime
				return result
			except COMError as e:
				errcode = e.hresult
				errtext = e.text
			except ReturnHRESULT as e:
				errcode, errtext = e.args
			if isDebugForSynthDriver():
				try:
					err = AudioError(errcode).name
				except ValueError:
					err = f"{errcode:#x}"
				log.debug(f"SAPI4: {funcname} failed with {err}")
			raise ReturnHRESULT(errcode, errtext)

		return _wrapper

	return _decorator


class _AudioState(IntEnum):
	INVALID = 0
	UNCLAIMED = 1
	CLAIMED = 2
	STARTED = 3
	UNCLAIMING = 4  # will change to CLAIMED after audio completes
	RECLAIMING = 5  # will change to STARTED after audio completes


class _ComThreadTask:
	def __init__(self, func: Callable, *args, **kwargs):
		self.func = func
		self.args = args
		self.kwargs = kwargs
		self.completed = threading.Event()
		self.result = None
		self.exception = None


class _ComThread(threading.Thread):
	"""Thread dedicated to run all SAPI 4 COM-related code."""

	def __init__(self):
		super().__init__(name="Sapi4ComThread")
		self._tasks: queue.SimpleQueue[_ComThreadTask] = queue.SimpleQueue()
		self._ready = threading.Event()
		self.start()  # Start the thread immediately
		self._ready.wait()  # Wait for message queue to be created

	def run(self):
		msg = MSG()
		# Force the message queue to be created first
		PM_NOREMOVE = 0
		windll.user32.PeekMessageW(byref(msg), None, 0, 0, PM_NOREMOVE)
		CoInitialize()
		self._ready.set()
		# Run a message loop, as it's required by SAPI 4.
		# When queueing a new task, post a message to this thread to wake it up.
		# When done, post WM_QUIT to this thread.
		while winBindings.user32.GetMessage(byref(msg), None, 0, 0):
			windll.user32.TranslateMessage(byref(msg))
			windll.user32.DispatchMessageW(byref(msg))
			# Process queued tasks outside window procedures
			# to avoid COM error RPC_E_CANTCALLOUT_INEXTERNALCALL
			# (-2147418107, 0x80010005).
			try:
				while True:
					task = self._tasks.get_nowait()
					try:
						task.result = task.func(*task.args, **task.kwargs)
					except BaseException as e:
						task.exception = e
					finally:
						completed = task.completed
						del task
						completed.set()
			except queue.Empty:
				pass

	def stop(self):
		WM_QUIT = 18
		windll.user32.PostThreadMessageW(self.native_id, WM_QUIT, 0, 0)
		self.join()

	def submit(self, func: Callable, *args, **kwargs) -> _ComThreadTask:
		"""Queue a function to be executed on this thread."""
		if not self.is_alive():
			raise RuntimeError("Thread has been stopped")
		task = _ComThreadTask(func, *args, **kwargs)
		self._tasks.put(task)
		# post a message to wake up the thread
		windll.user32.PostThreadMessageW(self.native_id, 0, 0, 0)
		return task

	def invoke(self, func: Callable, *args, **kwargs):
		"""Invoke a function on this thread synchronously, and return its result."""
		if threading.current_thread() is self:
			# Call directly
			return func(*args, **kwargs)
		task = self.submit(func, *args, **kwargs)
		task.completed.wait()
		if task.exception is not None:
			try:
				raise task.exception
			finally:
				del task
		return task.result


class _ComProxy:
	"""Proxy for SAPI 4 COM object pointers that invokes all COM methods on the specified `_ComThread`.
	All SAPI 4 COM objects should be wrapped by _ComProxy and run on the same _ComThread."""

	def __init__(self, obj, thread: _ComThread):
		"""Constructor.

		:param obj: The COM object pointer to wrap.
		:param thread: The COM thread to run all its COM method calls on. The object should be created on the same thread."""
		self._obj = obj
		self._thread = thread

	def __getattr__(self, name: str):
		attr = getattr(self._obj, name)
		if not callable(attr):
			return attr

		@wraps(attr)
		def _wrapper(*args, **kwargs):
			return self._thread.invoke(attr, *args, **kwargs)

		return _wrapper

	def __del__(self):
		# Release the object on the ComThread as well.
		def _deleter():
			self._obj = None

		self._thread.invoke(_deleter)


BUFFER_LENGTH_S = 2
"""Length of SynthDriverAudio's internal buffer, in seconds.
SAPI4 requires the buffer to be at least 2 seconds."""


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

	def __init__(self, comThread: _ComThread):
		"""Constructor.

		:param comThread: The COM thread that `IAudioDestNotifySink` methods will be called on."""
		if isDebugForSynthDriver():
			log.debug("SAPI4: Initializing WASAPI implementation")
		self._allowDelete = False
		self._notifySink: LP_IAudioDestNotifySink | None = None
		self._deviceState = _AudioState.INVALID
		self._waveFormat: WAVEFORMATEX | None = None
		self._player: nvwave.WavePlayer | None = None
		self._writtenBytes = 0
		self._playedBytes = 0
		self._startTime = datetime.now()
		self._startBytes = 0
		self._freeBytes = 0
		self._audioQueue: deque[bytes] = deque()
		self._bookmarkQueue: deque[_Bookmark] = deque()
		self._audioCond = threading.Condition()
		self._audioStopped = False
		self._audioThread = threading.Thread(target=self._audioThreadFunc, name="Sapi4AudioThread")
		self._level = 0xFFFFFFFF  # defaults to maximum value (0xFFFF) for both channels (low and high word)
		self._comThread = comThread

	def IUnknown_Release(self, this: int, *args, **kwargs) -> int:
		if not self._allowDelete and self._refcnt.value == 1:
			log.debugWarning("SynthDriverAudio was released too many times")
			return 1
		return super().IUnknown_Release(this, *args, **kwargs)

	def terminate(self):
		if isDebugForSynthDriver():
			log.debug("SAPI4: Terminating audio")
		with self._audioCond:
			self._audioStopped = True
			self._audioCond.notify()
		if self._audioThread is not threading.current_thread() and self._audioThread.is_alive():
			self._audioThread.join()
		self._notifySink = None
		self._allowDelete = True

	def _queueNotification(self, func: Callable, *args, **kwargs) -> None:
		"""Queue a notification to be sent to the engine via IAudioDestNotifySink.

		:param func: The IAudioDestNotifySink member function to call.
		:param ...: The arguments required by the member function.
		"""

		def _notify(*args, **kwargs):
			try:
				func(*args, **kwargs)
			except COMError:
				pass  # Ignore returned HRESULT errors

		self._comThread.submit(_notify, *args, **kwargs)

	def _setLevel(self, level: int) -> None:
		self._level = level
		self._player.setVolume(
			left=float(level & 0xFFFF) / 0xFFFF,
			right=float(level >> 16) / 0xFFFF,
		)

	def _initPlayer(self) -> None:
		"""Initialize audio playback based on the wave format provided by the engine."""
		if isDebugForSynthDriver():
			log.debug("SAPI4: Creating wave player")
		self._player = nvwave.WavePlayer(
			channels=self._waveFormat.nChannels,
			samplesPerSec=self._waveFormat.nSamplesPerSec,
			bitsPerSample=self._waveFormat.wBitsPerSample,
			outputDevice=config.conf["audio"]["outputDevice"],
		)
		self._setLevel(self._level)

	@_logTrace(logAll=True)
	def IAudio_Flush(self) -> None:
		"""Clears the object's internal buffer and resets the audio device,
		but does not stop playing the audio data afterwards."""
		if self._deviceState == _AudioState.INVALID:
			raise ReturnHRESULT(AudioError.NEED_WAVE_FORMAT, None)
		self._player.stop()
		with self._audioCond:
			if self._notifySink:
				while self._bookmarkQueue:
					bookmark = self._bookmarkQueue.popleft()
					# Flush all untriggered bookmarks.
					# 1 (TRUE) means that the bookmark is sent because of flushing.
					self._queueNotification(self._notifySink.BookMark, bookmark.id, 1)
			self._audioQueue.clear()
			self._bookmarkQueue.clear()
			self._freeBytes = self._waveFormat.nAvgBytesPerSec * BUFFER_LENGTH_S
			# As byte positions can only increase,
			# set _playedBytes to the current _writtenBytes
			# to make sure that bookmarks that use byte positions still work.
			self._playedBytes = self._writtenBytes

	@_logTrace()
	def IAudio_LevelGet(self) -> int:
		"""Returns the volume level, ranging from 0x0000 to 0xFFFF.
		Low word is for the left (or mono) channel, and high word is for the right channel."""
		if self._deviceState == _AudioState.INVALID:
			raise ReturnHRESULT(AudioError.NEED_WAVE_FORMAT, None)
		return self._level

	@_logTrace(format="{args[1]:#010x}")
	def IAudio_LevelSet(self, dwLevel: int) -> None:
		"""Sets the volume level, ranging from 0x0000 to 0xFFFF.
		Low word is for the left (or mono) channel, and high word is for the right channel."""
		if self._deviceState == _AudioState.INVALID:
			raise ReturnHRESULT(AudioError.NEED_WAVE_FORMAT, None)
		self._setLevel(dwLevel)

	@_logTrace()
	def IAudio_PassNotify(self, pNotifyInterface: c_void_p, IIDNotifyInterface: GUID) -> None:
		"""Passes in an implementation of IAudioDestNotifySink to receive notifications.
		The previous sink, if exists, will be released and replaced.
		Allows specifying NULL for no sink."""
		if IIDNotifyInterface != IAudioDestNotifySink._iid_:
			raise ReturnHRESULT(AudioError.INVALID_NOTIFY_SINK, None)
		if self._notifySink:
			self._notifySink = None
		if pNotifyInterface:
			self._notifySink = cast(pNotifyInterface, LP_IAudioDestNotifySink)

	@_logTrace()
	def IAudio_PosnGet(self) -> int:
		"""Returns the byte position currently being played,
		which should increase monotonically and never reset."""
		if self._deviceState == _AudioState.INVALID:
			raise ReturnHRESULT(AudioError.NEED_WAVE_FORMAT, None)
		return self._playedBytes

	@_logTrace(logAll=True)
	def IAudio_Claim(self) -> None:
		"""Acquires (opens) the multimedia device.
		Called before the engine wants to write audio data.
		`IAudioDestNotifySink::AudioStart()` will be called to notify the engine.
		Previous buffer should not be cleared.
		If Claim is called before unclaiming completes, unclaiming is canceled,
		and neither AudioStop nor AudioStart is notified."""
		if self._deviceState == _AudioState.INVALID:
			raise ReturnHRESULT(AudioError.NEED_WAVE_FORMAT, None)
		elif self._deviceState == _AudioState.UNCLAIMING:
			# cancels unclaiming
			if isDebugForSynthDriver():
				log.debug("SAPI4: Unclaiming cancelled")
			self._deviceState = _AudioState.RECLAIMING
			return
		elif self._deviceState != _AudioState.UNCLAIMED:
			raise ReturnHRESULT(AudioError.ALREADY_CLAIMED, None)
		self._deviceState = _AudioState.CLAIMED
		if self._notifySink:
			self._queueNotification(self._notifySink.AudioStart)

	@_logTrace(logAll=True)
	def IAudio_UnClaim(self) -> None:
		"""Releases the multimedia device asynchronously.
		Called after the engine completes writing all audio data.
		If there is audio in the buffer, it should still be played till the end.
		`IAudioDestNotifySink::AudioStop()` will be called after the audio completely stops."""
		if self._deviceState == _AudioState.INVALID:
			raise ReturnHRESULT(AudioError.NEED_WAVE_FORMAT, None)
		elif self._deviceState == _AudioState.CLAIMED:
			# When not playing, this can finish immediately.
			if self._writtenBytes == self._playedBytes and not self._audioQueue:
				# If all audio is done playing, stop the player.
				self._player.stop()
			self._deviceState = _AudioState.UNCLAIMED
			if self._notifySink:
				self._queueNotification(self._notifySink.AudioStop, 0)  # IANSRSN_NODATA
			if isDebugForSynthDriver():
				log.debug("SAPI4: UnClaim finished")
		elif self._deviceState in (_AudioState.STARTED, _AudioState.RECLAIMING):
			# When playing, wait for the playback to finish.
			if isDebugForSynthDriver():
				log.debug("SAPI4: UnClaiming")
			with self._audioCond:
				self._deviceState = _AudioState.UNCLAIMING
				self._audioCond.notify()
		else:
			raise ReturnHRESULT(AudioError.NOT_CLAIMED, None)

	@_logTrace(logAll=True)
	def IAudio_Start(self) -> None:
		"""Starts (or resumes) playing the audio in the buffer."""
		if self._deviceState == _AudioState.INVALID:
			raise ReturnHRESULT(AudioError.NEED_WAVE_FORMAT, None)
		elif self._deviceState == _AudioState.STARTED:
			raise ReturnHRESULT(AudioError.ALREADY_STARTED, None)
		elif self._deviceState not in (_AudioState.CLAIMED, _AudioState.RECLAIMING):
			raise ReturnHRESULT(AudioError.NOT_CLAIMED, None)
		self._startTime = datetime.now()
		self._startBytes = self._playedBytes
		try:
			self._player.pause(False)
		except OSError:
			log.debugWarning("Error starting audio", exc_info=True)
		with self._audioCond:
			self._deviceState = _AudioState.STARTED
			self._audioCond.notify()

	@_logTrace(logAll=True)
	def IAudio_Stop(self) -> None:
		"""Stops (or pauses) playing, without clearing the buffer.
		If there is audio in the buffer, calling Stop and UnClaim should keep the buffer
		and only pause the playback."""
		if self._deviceState == _AudioState.INVALID:
			raise ReturnHRESULT(AudioError.NEED_WAVE_FORMAT, None)
		elif self._deviceState == _AudioState.STARTED:
			self._deviceState = _AudioState.CLAIMED
		elif self._deviceState not in (_AudioState.UNCLAIMING, _AudioState.RECLAIMING):
			return
		try:
			self._player.pause(True)
		except OSError:
			log.debugWarning("Error stopping audio", exc_info=True)
		with self._audioCond:
			self._audioCond.notify()

	@_logTrace()
	def IAudio_TotalGet(self) -> int:
		"""Returns the total number of bytes written,
		including the unplayed bytes in the buffer,
		which should increase monotonically and never reset."""
		if self._deviceState == _AudioState.INVALID:
			raise ReturnHRESULT(AudioError.NEED_WAVE_FORMAT, None)
		return self._writtenBytes

	@_logTrace()
	def IAudio_ToFileTime(self, pqWord: c_ulonglong_p) -> FILETIME:
		"""Converts a byte position to UTC FILETIME."""
		if not pqWord:
			raise ReturnHRESULT(hresult.E_INVALIDARG, None)
		if self._deviceState == _AudioState.INVALID:
			raise ReturnHRESULT(AudioError.NEED_WAVE_FORMAT, None)
		UNIX_TIME_CONV = 1_1644_473_600
		filetime_ticks = int((self._startTime.timestamp() + UNIX_TIME_CONV) * 10_000_000)
		filetime_ticks += (pqWord[0] - self._startBytes) * 10_000_000 // self._waveFormat.nAvgBytesPerSec
		return FILETIME(filetime_ticks & 0xFFFFFFFF, filetime_ticks >> 32)

	@_logTrace()
	def IAudio_WaveFormatGet(self) -> SDATA:
		"""Gets a copy of the current wave format.
		:returns: A pointer to the WAVEFORMATEX structure.
			Should be freed by the caller using CoTaskMemFree."""
		if self._deviceState == _AudioState.INVALID:
			raise ReturnHRESULT(AudioError.NEED_WAVE_FORMAT, None)
		size = sizeof(WAVEFORMATEX)
		ptr = winBindings.ole32.CoTaskMemAlloc(size)
		if not ptr:
			raise COMError(hresult.E_OUTOFMEMORY, "CoTaskMemAlloc failed", (None, None, None, None, None))
		memmove(ptr, addressof(self._waveFormat), size)
		return SDATA(ptr, size)

	@_logTrace()
	def IAudio_WaveFormatSet(self, dWFEX: SDATA) -> None:
		"""Sets the current wave format. Only integer PCM formats are supported."""
		size = 18  # SAPI4 uses 18 bytes without the final padding
		if not dWFEX.pData or dWFEX.dwSize < size:
			raise ReturnHRESULT(hresult.E_INVALIDARG, None)
		wfx = WAVEFORMATEX()
		memmove(addressof(wfx), dWFEX.pData, size)
		if self._deviceState != _AudioState.INVALID:
			# Setting wave format more than once is not allowed.
			if bytes(wfx) == bytes(self._waveFormat):
				return  # Format not changed, do nothing
			else:
				raise ReturnHRESULT(AudioError.WAVE_DEVICE_BUSY)
		if wfx.wFormatTag != nvwave.WAVE_FORMAT_PCM:
			log.debugWarning("Wave format not supported. Only integer PCM formats are supported.")
			raise ReturnHRESULT(AudioError.WAVE_FORMAT_NOT_SUPPORTED, None)
		self._waveFormat = wfx
		self._initPlayer()
		self._deviceState = _AudioState.UNCLAIMED
		self._freeBytes = wfx.nAvgBytesPerSec * BUFFER_LENGTH_S
		self._audioThread.start()

	@_logTrace(format="{result[0]} bytes free")
	def IAudioDest_FreeSpace(self) -> tuple[DWORD, BOOL]:
		"""Returns the number of bytes that are free in the object's internal buffer.
		:returns: Tuple (dwBytes, fEOF).
			dwBytes: number of bytes available.
			fEOF: TRUE if end-of-file is reached and no more data can be sent.
				  For wave-out devices, this should always be FALSE."""
		if self._deviceState == _AudioState.INVALID:
			raise ReturnHRESULT(AudioError.NEED_WAVE_FORMAT, None)
		return (self._freeBytes, 0)

	@_logTrace(format="{args[2]} bytes written")
	def IAudioDest_DataSet(self, pBuffer: c_void_p, dwSize: int) -> None:
		"""Writes audio data to the end of the object's internal buffer.
		This should not block.
		When data cannot fit in the buffer, this should return AudioError.NOT_ENOUGH_DATA immediately."""
		if not pBuffer:
			raise ReturnHRESULT(hresult.E_INVALIDARG, None)
		if self._deviceState == _AudioState.INVALID:
			raise ReturnHRESULT(AudioError.NEED_WAVE_FORMAT, None)
		elif self._deviceState in (_AudioState.UNCLAIMED, _AudioState.UNCLAIMING):
			log.debugWarning("Audio data written when device is not claimed")
			raise ReturnHRESULT(AudioError.NOT_CLAIMED, None)
		elif self._freeBytes < dwSize:
			raise ReturnHRESULT(AudioError.NOT_ENOUGH_DATA, None)
		with self._audioCond:
			self._audioQueue.append(string_at(pBuffer, dwSize))
			self._writtenBytes += dwSize
			self._freeBytes -= dwSize
			self._audioCond.notify()

	@_logTrace()
	def IAudioDest_BookMark(self, dwMarkID: int) -> None:
		"""Attaches a bookmark to the most recent data in the audio-destination object's internal buffer.
		When the bookmark is reached, `IAudioDestNotifySink::BookMark` is called.
		When Flush is called, untriggered bookmarks should also be triggered."""
		if self._deviceState == _AudioState.INVALID:
			raise ReturnHRESULT(AudioError.NEED_WAVE_FORMAT, None)
		with self._audioCond:
			self._bookmarkQueue.append(_Bookmark(self._writtenBytes, dwMarkID))
			self._audioCond.notify()

	def _audioThreadFunc(self):
		"""Audio thread function that feeds the audio data from queue to WavePlayer."""
		while not self._audioStopped:
			with self._audioCond:
				self._checkBookmarksAndState()
				if self._deviceState not in (
					_AudioState.STARTED,
					_AudioState.UNCLAIMING,
					_AudioState.RECLAIMING,
				):
					self._audioCond.wait()
					continue
				if not self._audioQueue:
					# Since WavePlayer.feed returns before the audio finishes,
					# in order not to lose the final callbacks
					# when there's no more audio to feed,
					# wait with a timeout to give WavePlayer a chance
					# to check the callbacks periodically.
					self._audioCond.wait(0.01)
				item = self._audioQueue.popleft() if self._audioQueue else None
			if item:
				size = len(item)
				self._player.feed(item, size, lambda size=size: self._onChunkFinished(size))
			else:
				# Call feed to let WavePlayer check the callbacks
				self._player.feed(None, 0, None)

	def _onChunkFinished(self, size: int):
		self._playedBytes += size
		self._freeBytes += size
		if self._notifySink:
			self._queueNotification(self._notifySink.FreeSpace, self._freeBytes, 0)

	def _checkBookmarksAndState(self):
		if self._deviceState not in (
			_AudioState.STARTED,
			_AudioState.UNCLAIMING,
			_AudioState.RECLAIMING,
		):
			return
		while self._bookmarkQueue:
			bookmark = self._bookmarkQueue[0]
			if bookmark.bytePos > self._playedBytes:
				break
			if self._notifySink:
				self._queueNotification(self._notifySink.BookMark, bookmark.id, 0)
			self._bookmarkQueue.popleft()
		if self._playedBytes == self._writtenBytes and self._deviceState in (
			_AudioState.UNCLAIMING,
			_AudioState.RECLAIMING,
		):
			self._finishUnClaim()

	def _finishUnClaim(self):
		"""Finishes the asynchronous UnClaim call."""
		if self._deviceState == _AudioState.UNCLAIMING:
			self._deviceState = _AudioState.UNCLAIMED
			if isDebugForSynthDriver():
				log.debug("SAPI4: UnClaim finished")
		elif self._deviceState == _AudioState.RECLAIMING:
			self._deviceState = _AudioState.CLAIMED
			return
		else:
			return
		self._player.stop()
		if self._notifySink:
			# Notify when the device is finally closed
			self._queueNotification(self._notifySink.AudioStop, 0)  # IANSRSN_NODATA


class SynthDriverMMAudio(COMObject):
	"""
	Wrapper around SAPI4's built-in MMAudioDest,
	which can log the interactions between MMAudioDest and the TTS engine.
	"""

	_com_interfaces_ = [IAudio, IAudioDest]

	def __init__(self):
		if isDebugForSynthDriver():
			log.debug("SAPI4: Initializing WinMM implementation")
		self._allowDelete = False
		self.mmdev = CoCreateInstance(CLSID_MMAudioDest, IAudioMultiMediaDevice)
		self.mmdev.DeviceNumSet(_mmDeviceEndpointIdToWaveOutId(config.conf["audio"]["outputDevice"]))
		self.audio = self.mmdev.QueryInterface(IAudio)
		self.audiodest = self.mmdev.QueryInterface(IAudioDest)

	def IUnknown_Release(self, this: int, *args, **kwargs) -> int:
		if not self._allowDelete and self._refcnt.value == 1:
			log.debugWarning("SynthDriverMMAudio was released too many times")
			return 1
		return super().IUnknown_Release(this, *args, **kwargs)

	def terminate(self):
		self._allowDelete = True

	@_logTrace(logAll=True)
	def IAudio_Flush(self) -> None:
		self.audio.Flush()

	@_logTrace()
	def IAudio_LevelGet(self) -> int:
		return self.audio.LevelGet()

	@_logTrace(format="{args[1]:#010x}")
	def IAudio_LevelSet(self, dwLevel: int) -> None:
		return self.audio.LevelSet(dwLevel)

	@_logTrace()
	def IAudio_PassNotify(self, pNotifyInterface: c_void_p, IIDNotifyInterface: GUID) -> None:
		return self.audio.PassNotify(pNotifyInterface, IIDNotifyInterface)

	@_logTrace()
	def IAudio_PosnGet(self) -> int:
		return self.audio.PosnGet()

	@_logTrace(logAll=True)
	def IAudio_Claim(self) -> None:
		self.audio.Claim()

	@_logTrace(logAll=True)
	def IAudio_UnClaim(self) -> None:
		self.audio.UnClaim()

	@_logTrace(logAll=True)
	def IAudio_Start(self) -> None:
		self.audio.Start()

	@_logTrace(logAll=True)
	def IAudio_Stop(self) -> None:
		self.audio.Stop()

	@_logTrace()
	def IAudio_TotalGet(self) -> int:
		return self.audio.TotalGet()

	@_logTrace()
	def IAudio_ToFileTime(self, pqWord: c_ulonglong_p) -> FILETIME:
		return self.audio.ToFileTime(pqWord)

	@_logTrace()
	def IAudio_WaveFormatGet(self) -> SDATA:
		return self.audio.WaveFormatGet()

	@_logTrace()
	def IAudio_WaveFormatSet(self, dWFEX: SDATA) -> None:
		self.audio.WaveFormatSet(dWFEX)

	@_logTrace(format="{result[0]} bytes free")
	def IAudioDest_FreeSpace(self) -> tuple[DWORD, BOOL]:
		return self.audiodest.FreeSpace()

	@_logTrace(format="{args[2]} bytes written")
	def IAudioDest_DataSet(self, pBuffer: c_void_p, dwSize: int) -> None:
		self.audiodest.DataSet(pBuffer, dwSize)

	@_logTrace()
	def IAudioDest_BookMark(self, dwMarkID: int) -> None:
		self.audiodest.BookMark(dwMarkID)


class SynthDriverSink(COMObject):
	_com_interfaces_ = [ITTSNotifySinkW]

	def __init__(self, synthRef: weakref.ReferenceType):
		self.synthRef = synthRef
		self._allowDelete = True
		super().__init__()

	def ITTSNotifySinkW_AudioStart(self, this: int, qTimeStamp: int):
		if isDebugForSynthDriver():
			log.debug("SAPI4: TTSNotifySink AudioStart")
		synth = self.synthRef()
		if synth is None:
			log.debugWarning(
				"Called ITTSNotifySinkW_AudioStart method on ITTSNotifySinkW while driver is dead",
			)
			return
		if synth._bookmarkLists:
			# take the first bookmark list
			synth._bookmarks = synth._bookmarkLists.popleft()

	def ITTSNotifySinkW_AudioStop(self, this: int, qTimeStamp: int):
		if isDebugForSynthDriver():
			log.debug("SAPI4: TTSNotifySink AudioStop")
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

	def IUnknown_Release(self, this: int, *args, **kwargs):
		if not self._allowDelete and self._refcnt.value == 1:
			log.debugWarning("ITTSNotifySinkW::Release called too many times by engine")
			return 1
		return super().IUnknown_Release(this, *args, **kwargs)


class SynthDriver(SynthDriver):
	name = "sapi4"
	description = "Microsoft Speech API version 4"
	supportedSettings = [SynthDriver.VoiceSetting()]
	supportedCommands: set[type[SynthCommand]] = {
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
		self._comThread = _ComThread()
		self._finalIndex: Optional[int] = None
		self._ttsCentral = None
		self._ttsAudio = None
		self._sinkRegKey = DWORD()
		self._bookmarks = None
		self._bookmarkLists = deque()
		self._sink = SynthDriverSink(weakref.ref(self))
		self._sinkPtr = self._sink.QueryInterface(ITTSNotifySinkW)
		self._bufSink = SynthDriverBufSink(weakref.ref(self))
		self._bufSinkPtr = self._bufSink.QueryInterface(ITTSBufNotifySink)
		# HACK: Some buggy engines call Release() too many times on our buf sink.
		# Therefore, don't let the buf sink be deleted before we release it ourselves.
		self._bufSink._allowDelete = False
		# Create COM objects on the dedicated COM thread,
		# and wrap them with _ComProxy so that method calls will happen on the same thread.
		self._ttsEngines = self._comThread.invoke(CoCreateInstance, CLSID_TTSEnumerator, ITTSEnumW)
		self._ttsEngines = _ComProxy(self._ttsEngines, self._comThread)
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
		self._sink._allowDelete = True
		# Release all COM objects before stopping the COM thread.
		self._ttsAttrs = None
		self._ttsCentral = None
		if self._ttsAudio:
			self._ttsAudio.terminate()
			self._ttsAudio = None
		self._ttsEngines = None
		self._comThread.stop()

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
		if isDebugForSynthDriver():
			log.debug("SAPI4: Cancelling")
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
		if isDebugForSynthDriver():
			if switch:
				log.debug("SAPI4: Pausing")
			else:
				log.debug("SAPI4: Unpausing")
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
			self._ttsAttrs = None
			self._ttsCentral = None
			self._ttsAudio.terminate()
			self._ttsAudio = None
		if config.conf["speech"]["useWASAPIForSAPI4"]:
			self._ttsAudio = self._comThread.invoke(SynthDriverAudio, self._comThread)
		else:
			self._ttsAudio = self._comThread.invoke(SynthDriverMMAudio)
		self._ttsCentral = POINTER(ITTSCentralW)()
		self._ttsEngines.Select(self._currentMode.gModeID, byref(self._ttsCentral), self._ttsAudio)
		self._ttsCentral = _ComProxy(self._ttsCentral, self._comThread)
		self._ttsCentral.Register(self._sinkPtr, ITTSNotifySinkW._iid_, byref(self._sinkRegKey))
		self._ttsAttrs = _ComProxy(self._ttsCentral.QueryInterface(ITTSAttributes), self._comThread)
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


def _mmDeviceEndpointIdToWaveOutId(targetEndpointId: str) -> int:
	"""Translate from an MMDevice Endpoint ID string to a WaveOut Device ID number.

	:param targetEndpointId: MMDevice endpoint ID string to translate from, or the default value of the `audio.outputDevice` configuration key for the default output device.
	:return: An integer WaveOut device ID for use with SAPI4.
		If no matching device is found, or the default output device is requested, `-1` is returned, which means output will be handled by Microsoft Sound Mapper.
	"""
	if targetEndpointId != config.conf.getConfigValidation(("audio", "outputDevice")).default:
		targetEndpointIdByteCount = (len(targetEndpointId) + 1) * sizeof(c_wchar)
		currEndpointId = create_string_buffer(targetEndpointIdByteCount)
		currEndpointIdByteCount = DWORD()
		# Defined in mmeapi.h
		waveOutMessage = winBindings.winmm.waveOutMessage
		waveOutGetNumDevs = winBindings.winmm.waveOutGetNumDevs
		for devID in range(waveOutGetNumDevs()):
			# Get the length of this device's endpoint ID string.
			mmr = waveOutMessage(
				HANDLE(devID),
				DriverMessage.QUERY_INSTANCE_ID_SIZE,
				byref(currEndpointIdByteCount),
				None,
			)
			if (mmr != MMSYSERR_NOERROR) or (currEndpointIdByteCount.value != targetEndpointIdByteCount):
				# ID lengths don't match, so this device can't be a match.
				continue
			# Get the device's endpoint ID string.
			mmr = waveOutMessage(
				HANDLE(devID),
				DriverMessage.QUERY_INSTANCE_ID,
				byref(currEndpointId),
				currEndpointIdByteCount,
			)
			if mmr != MMSYSERR_NOERROR:
				continue
			# Decode the endpoint ID string to a python string, and strip the null terminator.
			if (
				currEndpointId.raw[: targetEndpointIdByteCount - sizeof(c_wchar)].decode("utf-16")
				== targetEndpointId
			):
				return devID
	# No matching device found, or default requested explicitly.
	# Return the ID of Microsoft Sound Mapper
	return -1
