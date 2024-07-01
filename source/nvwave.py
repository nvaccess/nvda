# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2007-2023 NV Access Limited, Aleksey Sadovoy, Cyrille Bougot, Peter Vágner, Babbage B.V.,
# Leonard de Ruijter, James Teh
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Provides a simple Python interface to playing audio using the Windows multimedia waveOut functions, as well as other useful utilities.
"""

import threading
import typing
from typing import (
	Optional,
	Callable,
)
from enum import Enum, auto
from ctypes import (
	windll,
	POINTER,
	Structure,
	c_uint,
	create_unicode_buffer,
	sizeof,
	byref,
	c_void_p,
	CFUNCTYPE,
	string_at,
	c_float,
)
from ctypes.wintypes import (
	HANDLE,
	WORD,
	DWORD,
	LPSTR,
	WCHAR,
	UINT,
	LPUINT
)
from comtypes import HRESULT
from comtypes.hresult import E_INVALIDARG
import atexit
import weakref
import time
import garbageHandler
import winKernel
import wave
import config
from logHandler import log, getOnErrorSoundRequested
import os.path
import extensionPoints
import NVDAHelper
import core
import globalVars


__all__ = (
	"WavePlayer",
	"getOutputDeviceNames",
	"outputDeviceIDToName",
	"outputDeviceNameToID",
	"decide_playWaveFile",
)

winmm = windll.winmm

HWAVEOUT = HANDLE
LPHWAVEOUT = POINTER(HWAVEOUT)

decide_playWaveFile = extensionPoints.Decider()
"""
Notifies when a wave file is about to be played,
and allows components or add-ons to decide whether the wave file should be played.
For example, when controlling a remote system,
the remote system must be notified of sounds played on the local system.
Also, registrars should be able to suppress playing sounds if desired.
Handlers are called with the same arguments as L{playWaveFile} as keyword arguments.
"""


class WAVEFORMATEX(Structure):
	_fields_ = [
		("wFormatTag", WORD),
		("nChannels", WORD),
		("nSamplesPerSec", DWORD),
		("nAvgBytesPerSec", DWORD),
		("nBlockAlign", WORD),
		("wBitsPerSample", WORD),
		("cbSize", WORD)
	]
LPWAVEFORMATEX = POINTER(WAVEFORMATEX)

class WAVEHDR(Structure):
	pass
LPWAVEHDR = POINTER(WAVEHDR)
WAVEHDR._fields_ = [
	("lpData", LPSTR),
	("dwBufferLength", DWORD),
	("dwBytesRecorded", DWORD),
	("dwUser", DWORD),
	("dwFlags", DWORD),
	("dwLoops", DWORD),
	("lpNext", LPWAVEHDR),
	("reserved", DWORD)
]
WHDR_DONE = 1

WAVE_FORMAT_PCM = 1
WAVE_MAPPER = -1
MMSYSERR_NOERROR = 0

CALLBACK_NULL = 0
#CALLBACK_FUNCTION = 0x30000
CALLBACK_EVENT = 0x50000
#waveOutProc = CFUNCTYPE(HANDLE, UINT, DWORD, DWORD, DWORD)
#WOM_DONE = 0x3bd

MAXPNAMELEN = 32
class WAVEOUTCAPS(Structure):
	_fields_ = [
		('wMid', WORD),
		('wPid', WORD),
		('vDriverVersion', c_uint),
		('szPname', WCHAR*MAXPNAMELEN),
		('dwFormats', DWORD),
		('wChannels', WORD),
		('wReserved1', WORD),
		('dwSupport', DWORD),
	]


# Set argument types.
winmm.waveOutOpen.argtypes = (LPHWAVEOUT, UINT, LPWAVEFORMATEX, DWORD, DWORD, DWORD)
winmm.waveOutGetID.argtypes = (HWAVEOUT, LPUINT)


# Initialize error checking.
def _winmm_errcheck(res, func, args):
	if res != MMSYSERR_NOERROR:
		buf = create_unicode_buffer(256)
		winmm.waveOutGetErrorTextW(res, buf, sizeof(buf))
		raise WindowsError(res, buf.value)
for func in (
	winmm.waveOutOpen, winmm.waveOutPrepareHeader, winmm.waveOutWrite, winmm.waveOutUnprepareHeader,
	winmm.waveOutPause, winmm.waveOutRestart, winmm.waveOutReset, winmm.waveOutClose,
	winmm.waveOutGetDevCapsW,
	winmm.waveOutGetID,
):
	func.errcheck = _winmm_errcheck


def _isDebugForNvWave():
	return config.conf["debugLog"]["nvwave"]


class AudioPurpose(Enum):
	"""The purpose of a particular stream of audio.
	"""
	SPEECH = auto()
	SOUNDS = auto()


class WinmmWavePlayer(garbageHandler.TrackedObject):
	"""Synchronously play a stream of audio.
	To use, construct an instance and feed it waveform audio using L{feed}.
	Keeps device open until it is either not available, or WavePlayer is explicitly closed / deleted.
	Will attempt to use the preferred device, if not will fallback to the WAVE_MAPPER device.
	When not using the preferred device, when idle devices will be checked to see if the preferred
	device has become available again. If so, it will be re-instated.
	"""
	#: Static variable, if any one WavePlayer instance is in error due to a missing / changing audio device
	# the error applies to all instances
	audioDeviceError_static: bool = False
	#: Minimum length of buffer (in ms) before audio is played.
	MIN_BUFFER_MS = 300
	#: Flag used to signal that L{stop} has been called.
	STOPPING = "stopping"
	#: A lock to prevent WaveOut* functions from being called simultaneously,
	# as this can cause problems even if they are for different HWAVEOUTs.
	_global_waveout_lock = threading.RLock()

	#: A signal handle, used by the winmm device to signal whenever the state of the waveform buffer changes.
	# Use WaitForSingleObject or WaitForMultipleObjects to wait for the event.
	# When the event is signaled, you can get the current state of the waveform buffer by checking the
	# dwFlags member of the WAVEHDR structure.
	_waveout_event: HANDLE = None

	#: The number of milliseconds that we should wait on the _waveout_event to be signaled. This
	# is a fallback, when audio is cancelled (via self.stop) the signal is triggered.
	_waveout_event_wait_ms = 100
	_audioDucker=None
	#: Used to allow the device to temporarily be changed and return
	# to the preferred device when it becomes available
	_preferredDeviceName: str
	#: The currently set device name.
	_outputDeviceName: str
	#: The id of the device when it was opened.
	# It is set to None when the device is closed again.
	_outputDeviceID: int
	#: Use the default device, this is the configSpec default value.
	DEFAULT_DEVICE_KEY = "default"

	def __init__(
			self,
			channels: int,
			samplesPerSec: int,
			bitsPerSample: int,
			outputDevice: typing.Union[str, int] = WAVE_MAPPER,
			closeWhenIdle: bool = False,
			wantDucking: bool = True,
			buffered: bool = False,
			purpose: AudioPurpose = AudioPurpose.SPEECH,
		):
		"""Constructor.
		@param channels: The number of channels of audio; e.g. 2 for stereo, 1 for mono.
		@param samplesPerSec: Samples per second (hz).
		@param bitsPerSample: The number of bits per sample.
		@param outputDevice: The device ID or name of the audio output device to use.
		@param closeWhenIdle: If C{True}, close the output device when no audio is being played.
		@param wantDucking: if true then background audio will be ducked on Windows 8 and higher
		@param buffered: Whether to buffer small chunks of audio to prevent audio glitches.
		@note: If C{outputDevice} is a name and no such device exists, the default device will be used.
		@raise WindowsError: If there was an error opening the audio output device.
		"""
		self.channels=channels
		self.samplesPerSec=samplesPerSec
		self.bitsPerSample=bitsPerSample

		self._setCurrentDevice(preferredDevice=outputDevice)
		self._preferredDeviceName = self._outputDeviceName

		if wantDucking:
			import audioDucking
			if audioDucking.isAudioDuckingSupported():
				self._audioDucker=audioDucking.AudioDucker()
		#: If C{True}, close the output device when no audio is being played.
		#: @type: bool
		self.closeWhenIdle = closeWhenIdle
		if buffered:
			#: Minimum size of the buffer before audio is played.
			#: However, this is ignored if an C{onDone} callback is provided to L{feed}.
			BITS_PER_BYTE = 8
			MS_PER_SEC = 1000
			self._minBufferSize = samplesPerSec * channels * (bitsPerSample / BITS_PER_BYTE) / MS_PER_SEC * self.MIN_BUFFER_MS
			self._buffer = b""
		else:
			self._minBufferSize = None
		#: Function to call when the previous chunk of audio has finished playing.
		self._prevOnDone = None
		self._waveout = None
		self._waveout_event = winKernel.kernel32.CreateEventW(None, False, False, None)
		self._waveout_lock = threading.RLock()
		self._lock = threading.RLock()
		self.open()

	def _setCurrentDevice(self, preferredDevice: typing.Union[str, int]) -> None:
		""" Sets the _outputDeviceID and _outputDeviceName to the preferredDevice if
		it is available, otherwise falls back to WAVE_MAPPER.
		@param preferredDevice: The preferred device to use.
		"""
		if preferredDevice == WAVE_MAPPER or preferredDevice == self.DEFAULT_DEVICE_KEY:
			self._outputDeviceID = WAVE_MAPPER
			self._outputDeviceName = "WAVE_MAPPER"
			return
		try:
			if isinstance(preferredDevice, str):
				self._outputDeviceID = outputDeviceNameToID(
					preferredDevice,
					useDefaultIfInvalid=True  # fallback to WAVE_MAPPER
				)
				# If default is used, get the appropriate name.
				self._outputDeviceName = outputDeviceIDToName(self._outputDeviceID)
			elif isinstance(preferredDevice, int):
				self._outputDeviceID = preferredDevice
				self._outputDeviceName = outputDeviceIDToName(preferredDevice)
			else:
				raise TypeError("outputDevice")
		except (LookupError, TypeError):
			log.warning(
				f"Unsupported WavePlayer device argument: {preferredDevice}"
				f" Falling back to WAVE_MAPPER"
			)
			self._setCurrentDevice(WAVE_MAPPER)

	def _isPreferredDeviceOpen(self) -> bool:
		if self._waveout is None:
			return False
		if _isDebugForNvWave():
			log.debug(
				f"preferred device: {self._preferredDeviceName}"
				f" current device name: {self._outputDeviceName} (id: {self._outputDeviceID})"
			)
		return self._outputDeviceName == self._preferredDeviceName

	def _isPreferredDeviceAvailable(self) -> bool:
		"""
		@note: Depending on number of devices being fetched, this may take some time (~3ms)
		@return: True if the preferred device is available
		"""
		for ID, name in _getOutputDevices():
			if name == self._preferredDeviceName:
				if _isDebugForNvWave():
					log.debug("preferred Device is Available")
				return True

		if _isDebugForNvWave():
			log.debug("preferred Device is not available")
		return False

	def open(self):
		"""Open the output device.
		This will be called automatically when required.
		It is not an error if the output device is already open.
		"""
		with self._waveout_lock:
			if self._waveout:
				return
			if _isDebugForNvWave():
				log.debug(
					f"Calling winmm.waveOutOpen."
					f" outputDeviceName: {self._outputDeviceName}"
					f" outputDeviceID: {self._outputDeviceID}"
				)
			wfx = WAVEFORMATEX()
			wfx.wFormatTag = WAVE_FORMAT_PCM
			wfx.nChannels = self.channels
			wfx.nSamplesPerSec = self.samplesPerSec
			wfx.wBitsPerSample = self.bitsPerSample
			wfx.nBlockAlign: int = self.bitsPerSample // 8 * self.channels
			wfx.nAvgBytesPerSec = self.samplesPerSec * wfx.nBlockAlign
			waveout = HWAVEOUT(0)
			try:
				with self._global_waveout_lock:
					winmm.waveOutOpen(
						byref(waveout),
						self._outputDeviceID,
						LPWAVEFORMATEX(wfx),
						self._waveout_event,
						0,
						CALLBACK_EVENT
					)
			except WindowsError:
				lastOutputDeviceID = self._outputDeviceID
				self._handleWinmmError(message="Error opening")
				if lastOutputDeviceID != WAVE_MAPPER:
					if _isDebugForNvWave():
						log.debug("Falling back to WAVE_MAPPER")
					self._setCurrentDevice(WAVE_MAPPER)
					self.open()
				else:
					log.warning("Unable to open WAVE_MAPPER device, there may be no audio devices.")
					WavePlayer.audioDeviceError_static = True
					raise  # can't open the default device.
				return
			self._waveout: typing.Optional[int] = waveout.value
			self._prev_whdr = None
			WavePlayer.audioDeviceError_static = False

	def feed(
			self,
			data: typing.Union[bytes, c_void_p],
			size: typing.Optional[int] = None,
			onDone: typing.Optional[typing.Callable] = None
	) -> None:
		"""Feed a chunk of audio data to be played.
		This is normally synchronous.
		However, synchronisation occurs on the previous chunk, rather than the current chunk;
		i.e. calling this while no audio is playing will begin playing the chunk
		but return immediately.
		This allows for uninterrupted playback as long as a new chunk is fed before
		the previous chunk has finished playing.
		@param data: Waveform audio in the format specified when this instance was constructed.
		@param size: The size of the data in bytes if data is a ctypes pointer.
			If data is a Python bytes object, size should be None.
		@param onDone: Function to call when this chunk has finished playing.
		@raise WindowsError: If there was an error playing the audio.
		"""
		if size is not None:
			data = string_at(data, size)
		if not self._minBufferSize:
			self._feedUnbuffered_handleErrors(data, onDone=onDone)
			return
		self._buffer += data
		# If onDone was specified, we must play audio regardless of the minimum buffer size
		# so we can accurately call onDone at the end of this chunk.
		if onDone or len(self._buffer) > self._minBufferSize:
			data = self._buffer
			self._buffer = b""
			self._feedUnbuffered_handleErrors(data, onDone=onDone)

	def _feedUnbuffered_handleErrors(self, data, onDone=None) -> bool:
		"""Tries to feed the device, on error resets the device and tries again.
		@return: False if second attempt fails
		"""
		try:
			self._feedUnbuffered(data, onDone=onDone)
			return True
		except WindowsError:
			log.warning("Error during feed. Resetting the device.")
			try:
				self._close()  # don't try to call stop on a "broken" device.
				self._setCurrentDevice(self._preferredDeviceName)
				self.open()
				self._feedUnbuffered(data, onDone=onDone)
			except Exception:
				log.debugWarning("Unable to send data to audio device on second attempt.", exc_info=True)
				return False

	def _feedUnbuffered(self, data, onDone=None):
		"""
		@note: Raises WindowsError on invalid device (see winmm functions
		"""
		if self._audioDucker and not self._audioDucker.enable():
			return
		whdr = WAVEHDR()
		whdr.lpData = data
		whdr.dwBufferLength = len(data)
		with self._lock:
			with self._waveout_lock:
				self.open()  # required if close on idle see _idleUnbuffered
				if self._prevOnDone is not self.STOPPING:
					# If we are stopping, waveOutReset has already been called.
					# Pushing more data confuses the state of nvWave
					with self._global_waveout_lock:
						winmm.waveOutPrepareHeader(self._waveout, LPWAVEHDR(whdr), sizeof(WAVEHDR))
						winmm.waveOutWrite(self._waveout, LPWAVEHDR(whdr), sizeof(WAVEHDR))
			self.sync()  # sync must still be called even if stopping, so that waveOutUnprepareHeader can be called
			self._prev_whdr = whdr
			# Don't call onDone if stop was called,
			# as this chunk has been truncated in that case.
			if self._prevOnDone is not self.STOPPING:
				self._prevOnDone = onDone

	def sync(self):
		"""Synchronise with playback.
		This method blocks until the previously fed chunk of audio has finished playing.
		It is called automatically by L{feed}, so usually need not be called directly by the user.

		Note: it must be possible to call stop concurrently with sync, sync should be considered to be blocking
		the synth driver thread most of the time (ie sync waiting for the last pushed block of audio to
		complete, via the 'winKernal.waitForSingleObject' mechanism)
		"""
		with self._lock:
			if not self._prev_whdr:
				return
			assert self._waveout, "waveOut None before wait"
			while (
				not (self._prev_whdr.dwFlags & WHDR_DONE)
				# In case some sound driver can not keep track of the whdr from previous buffers, ensure that
				# 'waitForSingleObject' can not block for long, and exit this loop if stopping.
				and self._prevOnDone is not self.STOPPING
			):
				winKernel.waitForSingleObject(self._waveout_event, self._waveout_event_wait_ms)
			with self._waveout_lock:
				assert self._waveout, "waveOut None after wait"
				with self._global_waveout_lock:
					try:
						winmm.waveOutUnprepareHeader(self._waveout, LPWAVEHDR(self._prev_whdr), sizeof(WAVEHDR))
					except WindowsError:
						# The device may have become unavailable.
						# It is uncertain if this buffer was actually finished, assume that it
						# did finish the worst case is dropped audio which is better than repeating audio.
						# Log the error, close the device and set _waveout to None. A new device will be opened when
						# required.
						# Don't return early, let the wave header (_prev_whdr) to be reset and
						# allow _prevOnDone to be called.
						self._handleWinmmError(message="UnprepareHeader")
			self._prev_whdr = None
			if self._prevOnDone not in (None, self.STOPPING):
				try:
					self._prevOnDone()
				except:  # noqa: E722
					log.exception("Error calling onDone")
				self._prevOnDone = None

	def pause(self, switch):
		"""Pause or unpause playback.
		@param switch: C{True} to pause playback, C{False} to unpause.
		@type switch: bool
		"""
		if self._audioDucker and self._waveout:
			if switch:
				self._audioDucker.disable()
			else:
				self._audioDucker.enable()
		with self._waveout_lock:
			if not self._waveout:
				return
			with self._global_waveout_lock:
				if switch:
					self._safe_winmm_call(winmm.waveOutPause, "Pause")
				else:
					self._safe_winmm_call(winmm.waveOutRestart, "Restart")

	def idle(self):
		"""Indicate that this player is now idle; i.e. the current continuous segment  of audio is complete.
		This will first call L{sync} to synchronise with playback.
		If L{closeWhenIdle} is C{True}, the output device will be closed.
		A subsequent call to L{feed} will reopen it.
		"""
		if not self._minBufferSize:
			return self._idleUnbuffered()
		if self._buffer:
			buffer = self._buffer
			self._buffer = b""
			self._feedUnbuffered_handleErrors(buffer)

		return self._idleUnbuffered()

	def _idleUnbuffered(self):
		with self._lock:
			self.sync()
			with self._waveout_lock:
				if not self._waveout:
					return
				if self.closeWhenIdle:
					if _isDebugForNvWave():
						log.debug("Closing due to idle.")
					self._close()  # Idle so no need to call stop.
				else:
					with self._global_waveout_lock:
						if not self._isPreferredDeviceOpen() and self._isPreferredDeviceAvailable():
							if _isDebugForNvWave():
								log.debug("Attempt re-open of preferred device.")
							self._close()  # Idle so no need to call stop.
							self._setCurrentDevice(self._preferredDeviceName)
							self.open()
			if self._audioDucker: self._audioDucker.disable()  # noqa: E701

	def stop(self):
		"""Stop playback.
		"""
		if self._audioDucker: self._audioDucker.disable()  # noqa: E701
		if self._minBufferSize:
			self._buffer = b""
		with self._waveout_lock:
			if not self._waveout:
				return
			self._prevOnDone = self.STOPPING
			with self._global_waveout_lock:
				# Pausing first seems to make waveOutReset respond faster on some systems.
				success = self._safe_winmm_call(winmm.waveOutPause, "Pause")
				success &= self._safe_winmm_call(winmm.waveOutReset, "Reset")
				# Allow fall through to idleUnbuffered if either pause or reset fail.

				# The documentation is not explicit about whether waveOutReset will signal the event,
				# so trigger it to be sure that sync isn't blocking on 'waitForSingleObject'.
				windll.kernel32.SetEvent(self._waveout_event)
				if not success:
					return
		# Unprepare the previous buffer and close the output device if appropriate.
		self._idleUnbuffered()
		self._prevOnDone = None

	def close(self):
		"""Close the output device.
		"""
		self.stop()
		with self._lock:
			with self._waveout_lock:
				if not self._waveout:
					return
				self._close()

	def _close(self):
		if _isDebugForNvWave():
			log.debug("Calling winmm.waveOutClose")
		with self._global_waveout_lock:
			if not self._waveout:
				return
			try:
				# don't use '_safe_winmm_call' here, on error it would re-enter _close infinitely
				winmm.waveOutClose(self._waveout)
			except WindowsError:
				log.debug("Error closing the device, it may have been removed.", exc_info=True)
		self._waveout = None

	def __del__(self):
		self.close()
		winKernel.kernel32.CloseHandle(self._waveout_event)
		self._waveout_event = None
		super().__del__()

	def _handleWinmmError(self, message: str):
		if _isDebugForNvWave():
			log.debug(
				f"Winmm Error: {message}"
				f" outputDeviceName: {self._outputDeviceName}"
				f" with id: {self._outputDeviceID}",
				stack_info=True
			)
		WavePlayer.audioDeviceError_static = True
		self._close()

	def _safe_winmm_call(
			self,
			winmmCall: Callable[[Optional[int]], None],
			messageOnFailure: str
	) -> bool:
		if not self._waveout:
			return False
		try:
			winmmCall(self._waveout)
			return True
		except WindowsError:
			# device will be closed and _waveout set to None,
			# triggering re-open.
			self._handleWinmmError(message=messageOnFailure)
			return False


WavePlayer = WinmmWavePlayer

def _getOutputDevices():
	"""Generator, returning device ID and device Name in device ID order.
		@note: Depending on number of devices being fetched, this may take some time (~3ms)
	"""
	caps = WAVEOUTCAPS()
	for devID in range(-1, winmm.waveOutGetNumDevs()):
		try:
			winmm.waveOutGetDevCapsW(devID, byref(caps), sizeof(caps))
			yield devID, caps.szPname
		except WindowsError:
			# It seems that in certain cases, Windows includes devices which cannot be accessed.
			pass


def getOutputDeviceNames():
	"""Obtain the names of all audio output devices on the system.
	@return: The names of all output devices on the system.
	@rtype: [str, ...]
	@note: Depending on number of devices being fetched, this may take some time (~3ms)
	"""
	return [name for ID, name in _getOutputDevices()]

def outputDeviceIDToName(ID):
	"""Obtain the name of an output device given its device ID.
	@param ID: The device ID.
	@type ID: int
	@return: The device name.
	@rtype: str
	"""
	caps = WAVEOUTCAPS()
	try:
		winmm.waveOutGetDevCapsW(ID, byref(caps), sizeof(caps))
	except WindowsError:
		raise LookupError("No such device ID")
	return caps.szPname


def outputDeviceNameToID(name: str, useDefaultIfInvalid=False) -> int:
	"""Obtain the device ID of an output device given its name.
	@param name: The device name.
	@param useDefaultIfInvalid: C{True} to use the default device (wave mapper) if there is no such device,
		C{False} to raise an exception.
	@return: The device ID.
	@raise LookupError: If there is no such device and C{useDefaultIfInvalid} is C{False}.
	@note: Depending on number of devices, and the position of the device in the list,
	this may take some time (~3ms)
	"""
	for curID, curName in _getOutputDevices():
		if curName == name:
			return curID

	# No such ID.
	if useDefaultIfInvalid:
		return WAVE_MAPPER
	else:
		raise LookupError("No such device name")


fileWavePlayer: Optional[WavePlayer] = None
fileWavePlayerThread = None


def playWaveFile(
		fileName: str,
		asynchronous: bool = True,
		isSpeechWaveFileCommand: bool = False
):
	"""plays a specified wave file.
	@param fileName: the path to the wave file, usually absolute.
	@param asynchronous: whether the wave file should be played asynchronously
		If C{False}, the calling thread is blocked until the wave has finished playing.
	@param isSpeechWaveFileCommand: whether this wave is played as part of a speech sequence.
	"""
	global fileWavePlayer, fileWavePlayerThread
	f = wave.open(fileName,"r")
	if f is None: raise RuntimeError("can not open file %s"%fileName)  # noqa: E701
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
		isSpeechWaveFileCommand=isSpeechWaveFileCommand
	):
		log.debug(
			"Playing wave file canceled by handler registered to decide_playWaveFile extension point"
		)
		return

	def play():
		global fileWavePlayer
		try:
			fileWavePlayer.feed(f.readframes(f.getnframes()))
			fileWavePlayer.idle()
		except Exception:
			log.exception("Error playing wave file")
		# #11169: Files might not be played that often. Leaving the device open
		# until the next file is played really shouldn't be a problem regardless of
		# how long we wait, but closing the device seems to hang occasionally.
		# There's no benefit to keeping it open - we're going to create a new
		# player for the next file anyway - so just destroy it now.
		fileWavePlayer = None

	fileWavePlayer = WavePlayer(
		channels=f.getnchannels(),
		samplesPerSec=f.getframerate(),
		bitsPerSample=f.getsampwidth() * 8,
		outputDevice=config.conf["speech"]["outputDevice"],
		wantDucking=False,
		purpose=AudioPurpose.SOUNDS
	)
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


class WasapiWavePlayer(garbageHandler.TrackedObject):
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
	DEFAULT_DEVICE_KEY = "default"
	#: The silence output device, None if not initialized.
	_silenceDevice: typing.Optional[str] = None

	def __init__(
			self,
			channels: int,
			samplesPerSec: int,
			bitsPerSample: int,
			outputDevice: typing.Union[str, int] = WAVE_MAPPER,
			closeWhenIdle: bool = False,
			wantDucking: bool = True,
			buffered: bool = False,
			purpose: AudioPurpose = AudioPurpose.SPEECH,
	):
		"""Constructor.
		@param channels: The number of channels of audio; e.g. 2 for stereo, 1 for mono.
		@param samplesPerSec: Samples per second (hz).
		@param bitsPerSample: The number of bits per sample.
		@param outputDevice: The name of the audio output device to use,
			WAVE_MAPPER for default.
		@param closeWhenIdle: Deprecated; ignored.
		@param wantDucking: if true then background audio will be ducked on Windows 8 and higher
		@param buffered: Whether to buffer small chunks of audio to prevent audio glitches.
		@param purpose: The purpose of this audio.
		@note: If C{outputDevice} is a name and no such device exists, the default device will be used.
		@raise WindowsError: If there was an error opening the audio output device.
		"""
		self.channels = channels
		self.samplesPerSec = samplesPerSec
		self.bitsPerSample = bitsPerSample
		format = self._format = WAVEFORMATEX()
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
		if self._isDefaultDevice(outputDevice):
			outputDevice = ""
		self._player = NVDAHelper.localLib.wasPlay_create(
			outputDevice,
			format,
			WasapiWavePlayer._callback
		)
		self._doneCallbacks = {}
		self._instances[self._player] = self
		self.open()
		self._lastActiveTime: typing.Optional[float] = None
		self._isPaused: bool = False
		if (
			config.conf["audio"]["audioAwakeTime"] > 0
			and WasapiWavePlayer._silenceDevice != outputDevice
		):
			# The output device has changed. (Re)initialize silence.
			if self._silenceDevice is not None:
				NVDAHelper.localLib.wasSilence_terminate()
			if config.conf["audio"]["audioAwakeTime"] > 0:
				NVDAHelper.localLib.wasSilence_init(outputDevice)
				WasapiWavePlayer._silenceDevice = outputDevice

	@wasPlay_callback
	def _callback(cppPlayer, feedId):
		pyPlayer = WasapiWavePlayer._instances[cppPlayer]
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

	def open(self):
		"""Open the output device.
		This will be called automatically when required.
		It is not an error if the output device is already open.
		"""
		try:
			NVDAHelper.localLib.wasPlay_open(self._player)
		except WindowsError:
			log.warning(
				"Couldn't open specified or default audio device. "
				"There may be no audio devices."
			)
			WavePlayer.audioDeviceError_static = True
			raise
		WasapiWavePlayer.audioDeviceError_static = False
		self._setVolumeFromConfig()

	def close(self):
		"""Close the output device.
		"""
		self.stop()

	def feed(
			self,
			data: typing.Union[bytes, c_void_p],
			size: typing.Optional[int] = None,
			onDone: typing.Optional[typing.Callable] = None
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
		try:
			NVDAHelper.localLib.wasPlay_feed(
				self._player,
				data,
				size if size is not None else len(data),
				byref(feedId) if onDone else None
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
		"""Indicate that this player is now idle; i.e. the current continuous segment  of audio is complete.
		"""
		self.sync()
		if self._audioDucker:
			self._audioDucker.disable()

	def stop(self):
		"""Stop playback.
		"""
		if self._audioDucker:
			self._audioDucker.disable()
		NVDAHelper.localLib.wasPlay_stop(self._player)
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
			right: Optional[float] = None
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
					cls._idleCheck
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
				NVDAHelper.localLib.wasPlay_idle(player._player)
				player._lastActiveTime = None
			else:
				stillActiveStream = True
		if stillActiveStream:
			# There's still at least one active stream that wasn't idle.
			# Schedule another check here in case feed isn't called for a while.
			cls._scheduleIdleCheck()

	@classmethod
	def _isDefaultDevice(cls, name):
		if name in (WAVE_MAPPER, cls.DEFAULT_DEVICE_KEY):
			return True
		# Check if this is the WinMM sound mapper device, which means default.
		return name == next(_getOutputDevices())[1]


def initialize():
	global WavePlayer
	if not config.conf["audio"]["WASAPI"]:
		getOnErrorSoundRequested().register(playErrorSound)
		return
	WavePlayer = WasapiWavePlayer
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
	if WasapiWavePlayer._silenceDevice is not None:
		NVDAHelper.localLib.wasSilence_terminate()
	getOnErrorSoundRequested().unregister(playErrorSound)


def usingWasapiWavePlayer() -> bool:
	return issubclass(WavePlayer, WasapiWavePlayer)


def playErrorSound() -> None:
	if isInError():
		if _isDebugForNvWave():
			log.debug("No beep for log; nvwave is in error state")
		return
	try:
		playWaveFile(os.path.join(globalVars.appDir, "waves", "error.wav"))
	except Exception:
		pass
