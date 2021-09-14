# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2007-2021 NV Access Limited, Aleksey Sadovoy, Cyrille Bougot, Peter Vágner
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
from ctypes import (
	windll,
	POINTER,
	Structure,
	c_uint,
	create_unicode_buffer,
	sizeof,
	byref,
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
import atexit
import garbageHandler
import winKernel
import wave
import config
from logHandler import log
import os.path

__all__ = (
	"WavePlayer", "getOutputDeviceNames", "outputDeviceIDToName", "outputDeviceNameToID",
)

winmm = windll.winmm

HWAVEOUT = HANDLE
LPHWAVEOUT = POINTER(HWAVEOUT)

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


class WavePlayer(garbageHandler.TrackedObject):
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
			buffered: bool = False
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
						log.debug(f"Falling back to WAVE_MAPPER")
					self._setCurrentDevice(WAVE_MAPPER)
					self.open()
				else:
					log.warning(f"Unable to open WAVE_MAPPER device, there may be no audio devices.")
					WavePlayer.audioDeviceError_static = True
					raise  # can't open the default device.
				return
			self._waveout: typing.Optional[int] = waveout.value
			self._prev_whdr = None
			WavePlayer.audioDeviceError_static = False

	def feed(
			self,
			data: bytes,
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
		@param onDone: Function to call when this chunk has finished playing.
		@raise WindowsError: If there was an error playing the audio.
		"""
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
				except:
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
			if self._audioDucker: self._audioDucker.disable()

	def stop(self):
		"""Stop playback.
		"""
		if self._audioDucker: self._audioDucker.disable()
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


def playWaveFile(fileName, asynchronous=True):
	"""plays a specified wave file.
	@param asynchronous: whether the wave file should be played asynchronously
	@type asynchronous: bool
	"""
	global fileWavePlayer, fileWavePlayerThread
	f = wave.open(fileName,"r")
	if f is None: raise RuntimeError("can not open file %s"%fileName)
	if fileWavePlayer is not None:
		fileWavePlayer.stop()
	fileWavePlayer = WavePlayer(
		channels=f.getnchannels(),
		samplesPerSec=f.getframerate(),
		bitsPerSample=f.getsampwidth() * 8,
		outputDevice=config.conf["speech"]["outputDevice"],
		wantDucking=False
	)
	fileWavePlayer.feed(f.readframes(f.getnframes()))
	if asynchronous:
		if fileWavePlayerThread is not None:
			fileWavePlayerThread.join()
		fileWavePlayerThread = threading.Thread(
			name=f"{__name__}.playWaveFile({os.path.basename(fileName)})",
			target=fileWavePlayer.idle
		)
		fileWavePlayerThread.start()
	else:
		fileWavePlayer.idle()

# When exiting, ensure fileWavePlayer is deleted before modules get cleaned up.
# Otherwise, WavePlayer.__del__ will fail with an exception.
@atexit.register
def _cleanup():
	global fileWavePlayer, fileWavePlayerThread
	fileWavePlayer = None
	fileWavePlayerThread = None


def isInError() -> bool:
	return WavePlayer.audioDeviceError_static
