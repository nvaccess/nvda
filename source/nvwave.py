# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2007-2025 NV Access Limited, Aleksey Sadovoy, Cyrille Bougot, Peter Vágner, Babbage B.V.,
# Leonard de Ruijter, James Teh
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Provides a simple Python interface to playing audio using the Windows Audio Session API (WASAPI), as well as other useful utilities."""

import threading
import typing
from typing import (
	Optional,
)
from enum import Enum, auto
from ctypes import (
	c_uint,
	byref,
	c_void_p,
	CFUNCTYPE,
	c_float,
	string_at,
)
from comtypes import HRESULT
from comtypes.hresult import E_INVALIDARG
import atexit
import weakref
import time
import garbageHandler
import wave
import config
from logHandler import log, getOnErrorSoundRequested
import os.path
import extensionPoints
import NVDAHelper
import core
import globalVars
from speech import SpeechSequence
from speech.commands import BreakCommand
from synthDriverHandler import pre_synthSpeak
from utils import _deprecate
from winBindings.mmeapi import WAVEFORMATEX as _WAVEFORMATEX

__getattr__ = _deprecate.handleDeprecations(
	_deprecate.MovedSymbol(
		"WAVEFORMATEX",
		"winBindings.mmeapi",
	),
)
"""Module __getattr__ to handle backward compatibility."""

__all__ = (
	"WavePlayer",
	"decide_playWaveFile",
)


decide_playWaveFile = extensionPoints.Decider()
"""
Notifies when a wave file is about to be played,
and allows components or add-ons to decide whether the wave file should be played.
For example, when controlling a remote system,
the remote system must be notified of sounds played on the local system.
Also, registrars should be able to suppress playing sounds if desired.
Handlers are called with the same arguments as L{playWaveFile} as keyword arguments.
"""


WAVE_FORMAT_PCM = 1


def _isDebugForNvWave():
	return config.conf["debugLog"]["nvwave"]


class AudioPurpose(Enum):
	"""The purpose of a particular stream of audio."""

	SPEECH = auto()
	SOUNDS = auto()


def playWaveFile(
	fileName: str,
	asynchronous: bool = True,
	isSpeechWaveFileCommand: bool = False,
):
	"""plays a specified wave file.

	:param fileName: the path to the wave file, usually absolute.
	:param asynchronous: whether the wave file should be played asynchronously
		If ``False``, the calling thread is blocked until the wave has finished playing.
	:param isSpeechWaveFileCommand: whether this wave is played as part of a speech sequence.
	"""
	global fileWavePlayer, fileWavePlayerThread
	f = wave.open(fileName, "r")
	if f is None:
		raise RuntimeError("can not open file %s" % fileName)
	if fileWavePlayer is not None:
		# There are several race conditions where the background thread might feed
		# audio after we call stop here in the main thread. Some of these are
		# difficult to fix with locks because they involve switches between Python
		# and blocking native code. Just keep calling stop until we know that the
		# backgroundd thread is done, which means it was successfully stopped. The
		# background thread sets fileWavePlayer to None when it is done.
		while fileWavePlayer:
			fileWavePlayer.stop()
	if not decide_playWaveFile.decide(
		fileName=fileName,
		asynchronous=asynchronous,
		isSpeechWaveFileCommand=isSpeechWaveFileCommand,
	):
		log.debug(
			"Playing wave file canceled by handler registered to decide_playWaveFile extension point",
		)
		return

	def play():
		global fileWavePlayer
		# #17918: Create a function local copy of the player to avoid cases where it becomes None during playback.
		p = fileWavePlayer
		try:
			p.feed(f.readframes(f.getnframes()))
			p.idle()
		except Exception:
			log.exception("Error playing wave file")
		# #11169: Files might not be played that often. Leaving the device open
		# until the next file is played really shouldn't be a problem regardless of
		# how long we wait, but closing the device seems to hang occasionally.
		# There's no benefit to keeping it open - we're going to create a new
		# player for the next file anyway - so just destroy it now.
		fileWavePlayer = None

	try:
		fileWavePlayer = WavePlayer(
			channels=f.getnchannels(),
			samplesPerSec=f.getframerate(),
			bitsPerSample=f.getsampwidth() * 8,
			outputDevice=config.conf["audio"]["outputDevice"],
			wantDucking=False,
			purpose=AudioPurpose.SOUNDS,
		)
	except OSError as exception:
		# If there are no enabled audio render endpoints connected to the system,
		# attempting to initialise a WASAPI session will fail.
		# Fail gracefully in this case.
		if exception.winerror == -2147023728:  # 0x80070490: ERROR_NOT_FOUND
			# We mustn't log at error level as it may try to play a sound,
			# and that's what caused this exception.
			log.debugWarning("Unable to play wave file as the render endpoint was not found.", exc_info=True)
			return
		# In other cases, we should still raise.
		raise
	if asynchronous:
		fileWavePlayerThread = threading.Thread(
			name=f"{__name__}.playWaveFile({os.path.basename(fileName)})",
			target=play,
			daemon=True,
		)
		fileWavePlayerThread.start()
	else:
		play()


# When exiting, ensure fileWavePlayer is deleted before modules get cleaned up.
# Otherwise, WavePlayer.__del__ will fail with an exception.
@atexit.register
def _cleanup():
	global fileWavePlayer, fileWavePlayerThread
	fileWavePlayer = None
	fileWavePlayerThread = None


def isInError() -> bool:
	return WavePlayer.audioDeviceError_static


wasPlay_callback = CFUNCTYPE(None, c_void_p, c_uint)


class WavePlayer(garbageHandler.TrackedObject):
	"""Synchronously play a stream of audio using WASAPI.
	To use, construct an instance and feed it waveform audio using L{feed}.
	Keeps device open until it is either not available, or WavePlayer is explicitly closed / deleted.
	Will attempt to use the preferred device, if not will fallback to the default device.
	"""

	#: Static variable, if any one WavePlayer instance is in error due to a missing / changing audio device
	# the error applies to all instances
	audioDeviceError_static: bool = False
	#: Maps C++ WasapiPlayer instances to Python WasapiWavePlayer instances.
	#: This allows us to have a single callback in the class rather than on
	#: each instance, which prevents reference cycles.
	_instances = weakref.WeakValueDictionary()
	#: How long (in seconds) to wait before indicating that an audio stream that
	#: hasn't played is idle.
	_IDLE_TIMEOUT: int = 10
	#: How often (in ms) to check whether streams are idle.
	_IDLE_CHECK_INTERVAL: int = 5000
	#: Whether there is a pending stream idle check.
	_isIdleCheckPending: bool = False
	#: Use the default device, this is the configSpec default value.
	DEFAULT_DEVICE_KEY = typing.cast(str, config.conf.getConfigValidation(("audio", "outputDevice")).default)
	#: The silence output device, None if not initialized.
	_silenceDevice: typing.Optional[str] = None

	def __init__(
		self,
		channels: int,
		samplesPerSec: int,
		bitsPerSample: int,
		outputDevice: str = DEFAULT_DEVICE_KEY,
		wantDucking: bool = True,
		purpose: AudioPurpose = AudioPurpose.SPEECH,
	):
		"""Constructor.
		@param channels: The number of channels of audio; e.g. 2 for stereo, 1 for mono.
		@param samplesPerSec: Samples per second (hz).
		@param bitsPerSample: The number of bits per sample.
		@param outputDevice: The name of the audio output device to use, defaults to WasapiWavePlayer.DEFAULT_DEVICE_KEY
		@param wantDucking: if true then background audio will be ducked on Windows 8 and higher
		@param purpose: The purpose of this audio.
		@note: If C{outputDevice} is a name and no such device exists, the default device will be used.
		@raise WindowsError: If there was an error opening the audio output device.
		"""
		self.channels = channels
		self.samplesPerSec = samplesPerSec
		self.bitsPerSample = bitsPerSample
		format = self._format = _WAVEFORMATEX()
		format.wFormatTag = WAVE_FORMAT_PCM
		format.nChannels = channels
		format.nSamplesPerSec = samplesPerSec
		format.wBitsPerSample = bitsPerSample
		format.nBlockAlign: int = bitsPerSample // 8 * channels
		format.nAvgBytesPerSec = samplesPerSec * format.nBlockAlign
		self._audioDucker = None
		if wantDucking:
			import audioDucking

			if audioDucking.isAudioDuckingSupported():
				self._audioDucker = audioDucking.AudioDucker()
		self._purpose = purpose
		if outputDevice == self.DEFAULT_DEVICE_KEY:
			outputDevice = ""
		self._player = NVDAHelper.localLib.wasPlay_create(
			outputDevice,
			format,
			WavePlayer._callback,
		)
		self._doneCallbacks = {}
		self._instances[self._player] = self
		self.open()
		self._lastActiveTime: typing.Optional[float] = None
		self._isPaused: bool = False
		if config.conf["audio"]["audioAwakeTime"] > 0 and WavePlayer._silenceDevice != outputDevice:
			# The output device has changed. (Re)initialize silence.
			if self._silenceDevice is not None:
				NVDAHelper.localLib.wasSilence_terminate()
			if config.conf["audio"]["audioAwakeTime"] > 0:
				NVDAHelper.localLib.wasSilence_init(outputDevice)
				WavePlayer._silenceDevice = outputDevice
		# Enable trimming by default for speech only
		self.enableTrimmingLeadingSilence(
			purpose is AudioPurpose.SPEECH and config.conf["speech"]["trimLeadingSilence"],
		)
		if self._enableTrimmingLeadingSilence:
			self.startTrimmingLeadingSilence()
		self._isLeadingSilenceInserted: bool = False
		pre_synthSpeak.register(self._onPreSpeak)

	@wasPlay_callback
	def _callback(cppPlayer, feedId):
		pyPlayer = WavePlayer._instances[cppPlayer]
		onDone = pyPlayer._doneCallbacks.pop(feedId, None)
		if onDone:
			onDone()

	def __del__(self):
		if not hasattr(self, "_player"):
			# This instance failed to construct properly. Let it die gracefully.
			return
		if not NVDAHelper.localLib:
			# This instance is dying after NVDAHelper was terminated. We can't
			# destroy it in that case, but we're probably exiting anyway.
			return
		if self._player:
			NVDAHelper.localLib.wasPlay_destroy(self._player)
			# Because _instances is a WeakValueDictionary, it will remove the
			# reference to this instance by itself. We don't need to do it explicitly
			# here. Furthermore, doing it explicitly might cause an exception because
			# a weakref callback can run before __del__ in some cases, which would mean
			# it has already been removed from _instances.
			self._player = None
		pre_synthSpeak.unregister(self._onPreSpeak)

	def open(self):
		"""Open the output device.
		This will be called automatically when required.
		It is not an error if the output device is already open.
		"""
		try:
			NVDAHelper.localLib.wasPlay_open(self._player)
		except WindowsError:
			log.warning(
				"Couldn't open specified or default audio device. There may be no audio devices.",
			)
			WavePlayer.audioDeviceError_static = True
			raise
		WavePlayer.audioDeviceError_static = False
		self._setVolumeFromConfig()

	def close(self):
		"""Close the output device."""
		self.stop()

	def feed(
		self,
		data: typing.Union[bytes, c_void_p],
		size: typing.Optional[int] = None,
		onDone: typing.Optional[typing.Callable] = None,
	) -> None:
		"""Feed a chunk of audio data to be played.
		This will block until there is sufficient space in the buffer.
		However, it will return well before the audio is finished playing.
		This allows for uninterrupted playback as long as a new chunk is fed before
		the previous chunk has finished playing.
		@param data: Waveform audio in the format specified when this instance was constructed.
		@param size: The size of the data in bytes if data is a ctypes pointer.
			If data is a Python bytes object, size should be None.
		@param onDone: Function to call when this chunk has finished playing.
		@raise WindowsError: If there was an error initially opening the device.
		"""
		self.open()
		if self._audioDucker:
			self._audioDucker.enable()
		feedId = c_uint() if onDone else None
		# Never treat this instance as idle while we're feeding.
		self._lastActiveTime = None
		# If a BreakCommand is used to insert leading silence in this utterance,
		# turn off trimming temporarily.
		if self._purpose is AudioPurpose.SPEECH and self._isLeadingSilenceInserted:
			self.startTrimmingLeadingSilence(False)
		if not isinstance(data, bytes):
			data = string_at(data, size)
		try:
			NVDAHelper.localLib.wasPlay_feed(
				self._player,
				data,
				size if size is not None else len(data),
				byref(feedId) if onDone else None,
			)
		except WindowsError:
			# #16722: This might occur on a Remote Desktop server when a client session
			# disconnects without exiting NVDA. That will cause audio to become
			# unavailable with an unexpected error code. In any case, the C++
			# WasapiPlayer code will reopen the device when we next try to feed, so
			# just log the error here and return without raising it. Otherwise, we
			# might break code which isn't expecting to handle exceptions from feed
			# such as the oneCore synth driver.
			log.debugWarning("Error feeding audio", exc_info=True)
			return
		if onDone:
			self._doneCallbacks[feedId.value] = onDone
		self._lastActiveTime = time.time()
		self._scheduleIdleCheck()
		if config.conf["audio"]["audioAwakeTime"] > 0:
			NVDAHelper.localLib.wasSilence_playFor(
				1000 * config.conf["audio"]["audioAwakeTime"],
				c_float(config.conf["audio"]["whiteNoiseVolume"] / 100.0),
			)

	def sync(self):
		"""Synchronise with playback.
		This method blocks until the previously fed chunk of audio has finished playing.
		"""
		NVDAHelper.localLib.wasPlay_sync(self._player)

	def idle(self):
		"""Indicate that this player is now idle; i.e. the current continuous segment  of audio is complete."""
		self.sync()
		if self._enableTrimmingLeadingSilence:
			self.startTrimmingLeadingSilence()
		if self._audioDucker:
			self._audioDucker.disable()

	def stop(self):
		"""Stop playback."""
		if self._audioDucker:
			self._audioDucker.disable()
		NVDAHelper.localLib.wasPlay_stop(self._player)
		if self._enableTrimmingLeadingSilence:
			self.startTrimmingLeadingSilence()
		self._lastActiveTime = None
		self._isPaused = False
		self._doneCallbacks = {}
		self._setVolumeFromConfig()

	def pause(self, switch: bool):
		"""Pause or unpause playback.
		@param switch: C{True} to pause playback, C{False} to unpause.
		"""
		if self._audioDucker:
			if switch:
				self._audioDucker.disable()
			else:
				self._audioDucker.enable()
		if switch:
			NVDAHelper.localLib.wasPlay_pause(self._player)
		else:
			NVDAHelper.localLib.wasPlay_resume(self._player)
			# If self._lastActiveTime is None, either no audio has been fed yet or audio
			# is currently being fed. Either way, we shouldn't touch it.
			if self._lastActiveTime:
				self._lastActiveTime = time.time()
				self._scheduleIdleCheck()
		self._isPaused = switch

	def setVolume(
		self,
		*,
		all: Optional[float] = None,
		left: Optional[float] = None,
		right: Optional[float] = None,
	):
		"""Set the volume of one or more channels in this stream.
		Levels must be specified as a number between 0 and 1.
		@param all: The level to set for all channels.
		@param left: The level to set for the left channel.
		@param right: The level to set for the right channel.
		"""
		if all is None and left is None and right is None:
			raise ValueError("At least one of all, left or right must be specified")
		if all is not None:
			if left is not None or right is not None:
				raise ValueError("all specified, so left and right must not be specified")
			left = right = all
		NVDAHelper.localLib.wasPlay_setChannelVolume(self._player, 0, c_float(left))
		try:
			NVDAHelper.localLib.wasPlay_setChannelVolume(self._player, 1, c_float(right))
		except WindowsError as e:
			# E_INVALIDARG indicates that the audio device doesn't support this channel.
			# If we're trying to set all channels, that's fine; we've already set the
			# single channel that this device supports.
			if not (all and e.winerror == E_INVALIDARG):
				raise

	def enableTrimmingLeadingSilence(self, enable: bool) -> None:
		"""Enable or disable automatic leading silence removal.
		This is by default enabled for speech audio, and disabled for non-speech audio."""
		self._enableTrimmingLeadingSilence = enable
		if not enable:
			self.startTrimmingLeadingSilence(False)

	def startTrimmingLeadingSilence(self, start: bool = True) -> None:
		"""Start or stop trimming the leading silence from the next audio chunk."""
		NVDAHelper.localLib.wasPlay_startTrimmingLeadingSilence(self._player, start)

	def _setVolumeFromConfig(self):
		if self._purpose is not AudioPurpose.SOUNDS:
			return
		volume = config.conf["audio"]["soundVolume"]
		if config.conf["audio"]["soundVolumeFollowsVoice"]:
			import synthDriverHandler

			synth = synthDriverHandler.getSynth()
			if synth and synth.isSupported("volume"):
				volume = synth.volume
		self.setVolume(all=volume / 100)

	@classmethod
	def _scheduleIdleCheck(cls):
		if not cls._isIdleCheckPending:
			try:
				core.callLater(
					cls._IDLE_CHECK_INTERVAL,
					cls._idleCheck,
				)
			except core.NVDANotInitializedError:
				# This can happen when playing the start sound. We close the stream after
				# playing a sound anyway, so it's okay that this first idle check doesn't
				# run.
				pass
			cls._isIdleCheckPending = True

	@classmethod
	def _idleCheck(cls):
		"""Check whether there are open audio streams that should be considered
		idle. If there are any, stop them. If there are open streams that
		aren't idle yet, schedule another check.
		This is necessary because failing to stop streams can prevent sleep on some
		systems.
		We do this in a single, class-wide check rather than separately for each
		instance to avoid continually resetting a timer for each call to feed().
		Resetting timers from another thread involves queuing to the main thread.
		Doing that for every chunk of audio would not be very efficient.
		Doing this with a class-wide check means that some checks might not take any
		action and some streams might be stopped a little after the timeout elapses,
		but this isn't problematic for our purposes.
		"""
		cls._isIdleCheckPending = False
		threshold = time.time() - cls._IDLE_TIMEOUT
		stillActiveStream = False
		for player in cls._instances.values():
			if not player._lastActiveTime or player._isPaused:
				# Either no audio has been fed yet, audio is currently being fed or the
				# player is paused. Don't treat this player as idle.
				continue
			if player._lastActiveTime <= threshold:
				try:
					NVDAHelper.localLib.wasPlay_idle(player._player)
					if player._enableTrimmingLeadingSilence:
						player.startTrimmingLeadingSilence()
				except OSError:
					# #16125: IAudioClock::GetPosition sometimes fails with an access
					# violation on a device which has been invalidated. This shouldn't happen
					# and suggests a bug somewhere in NVDA's C++ WASAPI code. Nevertheless,
					# we want to catch this because otherwise, we'll just keep trying to call
					# this every few seconds, which is pointless and annoying. Hopefully, a
					# proper fix for this bug can be found eventually.
					log.exception("Error calling wasPlay_idle")
				player._lastActiveTime = None
			else:
				stillActiveStream = True
		if stillActiveStream:
			# There's still at least one active stream that wasn't idle.
			# Schedule another check here in case feed isn't called for a while.
			cls._scheduleIdleCheck()

	def _onPreSpeak(self, speechSequence: SpeechSequence):
		self._isLeadingSilenceInserted = False
		# Check if leading silence of the current utterance is inserted by a BreakCommand.
		for item in speechSequence:
			if isinstance(item, BreakCommand):
				self._isLeadingSilenceInserted = True
				break
			elif isinstance(item, str):
				break


fileWavePlayer: Optional[WavePlayer] = None
fileWavePlayerThread: threading.Thread | None = None


def initialize():
	NVDAHelper.localLib.wasPlay_create.restype = c_void_p
	for func in (
		NVDAHelper.localLib.wasPlay_startup,
		NVDAHelper.localLib.wasPlay_open,
		NVDAHelper.localLib.wasPlay_feed,
		NVDAHelper.localLib.wasPlay_stop,
		NVDAHelper.localLib.wasPlay_sync,
		NVDAHelper.localLib.wasPlay_idle,
		NVDAHelper.localLib.wasPlay_pause,
		NVDAHelper.localLib.wasPlay_resume,
		NVDAHelper.localLib.wasPlay_setChannelVolume,
		NVDAHelper.localLib.wasSilence_init,
	):
		func.restype = HRESULT
	NVDAHelper.localLib.wasPlay_startup()
	getOnErrorSoundRequested().register(playErrorSound)


def terminate() -> None:
	if WavePlayer._silenceDevice is not None:
		NVDAHelper.localLib.wasSilence_terminate()
	getOnErrorSoundRequested().unregister(playErrorSound)


def playErrorSound() -> None:
	if isInError():
		if _isDebugForNvWave():
			log.debug("No beep for log; nvwave is in error state")
		return
	try:
		playWaveFile(os.path.join(globalVars.appDir, "waves", "error.wav"))
	except Exception:
		pass
