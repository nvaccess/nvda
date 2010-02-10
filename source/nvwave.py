#nvwave.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Provides a simple Python interface to playing audio using the Windows multimedia waveOut functions, as well as other useful utilities.
"""

import threading
from ctypes import *
from ctypes.wintypes import *
import winKernel
import wave
import config

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

# Initialize error checking.
def _winmm_errcheck(res, func, args):
	if res != MMSYSERR_NOERROR:
		buf = create_unicode_buffer(256)
		winmm.waveOutGetErrorTextW(res, buf, sizeof(buf))
		raise WindowsError(res, buf.value)
for func in (
	winmm.waveOutOpen, winmm.waveOutPrepareHeader, winmm.waveOutWrite, winmm.waveOutUnprepareHeader,
	winmm.waveOutPause, winmm.waveOutRestart, winmm.waveOutReset, winmm.waveOutClose,
	winmm.waveOutGetDevCapsW
):
	func.errcheck = _winmm_errcheck

class WavePlayer(object):
	"""Synchronously play a stream of audio.
	To use, construct an instance and feed it waveform audio using L{feed}.
	"""
	#: A lock to prevent WaveOut* functions from being called simultaneously, as this can cause problems even if they are for different HWAVEOUTs.
	_global_waveout_lock = threading.RLock()

	def __init__(self, channels, samplesPerSec, bitsPerSample, outputDevice=WAVE_MAPPER, closeWhenIdle=True):
		"""Constructor.
		@param channels: The number of channels of audio; e.g. 2 for stereo, 1 for mono.
		@type channels: int
		@param samplesPerSec: Samples per second (hz).
		@type samplesPerSec: int
		@param bitsPerSample: The number of bits per sample.
		@type bitsPerSample: int
		@param outputDevice: The device ID or name of the audio output device to use.
		@type outputDevice: int or basestring
		@param closeWhenIdle: If C{True}, close the output device when no audio is being played.
		@type closeWhenIdle: bool
		@note: If C{outputDevice} is a name and no such device exists, the default device will be used.
		@raise WindowsError: If there was an error opening the audio output device.
		"""
		self.channels=channels
		self.samplesPerSec=samplesPerSec
		self.bitsPerSample=bitsPerSample
		if isinstance(outputDevice, basestring):
			outputDevice = outputDeviceNameToID(outputDevice, True)
		self.outputDeviceID = outputDevice
		#: If C{True}, close the output device when no audio is being played.
		#: @type: bool
		self.closeWhenIdle = closeWhenIdle
		self._waveout = None
		self._waveout_event = winKernel.kernel32.CreateEventW(None, False, False, None)
		self._waveout_lock = threading.RLock()
		self._lock = threading.RLock()
		self.open()

	def open(self):
		"""Open the output device.
		This will be called automatically when required.
		It is not an error if the output device is already open.
		"""
		with self._waveout_lock:
			if self._waveout:
				return
			wfx = WAVEFORMATEX()
			wfx.wFormatTag = WAVE_FORMAT_PCM
			wfx.nChannels = self.channels
			wfx.nSamplesPerSec = self.samplesPerSec
			wfx.wBitsPerSample = self.bitsPerSample
			wfx.nBlockAlign = self.bitsPerSample / 8 * self.channels
			wfx.nAvgBytesPerSec = self.samplesPerSec * wfx.nBlockAlign
			waveout = HWAVEOUT(0)
			with self._global_waveout_lock: winmm.waveOutOpen(byref(waveout), self.outputDeviceID, LPWAVEFORMATEX(wfx), self._waveout_event, 0, CALLBACK_EVENT)
			self._waveout = waveout.value
			self._prev_whdr = None

	def feed(self, data):
		"""Feed a chunk of audio data to be played.
		This is normally synchronous.
		However, synchronisation occurs on the previous chunk, rather than the current chunk; i.e. calling this while no audio is playing will begin playing the chunk but return immediately.
		This allows for uninterrupted playback as long as a new chunk is fed before the previous chunk has finished playing.
		@param data: Waveform audio in the format specified when this instance was constructed.
		@type data: str
		@raise WindowsError: If there was an error playing the audio.
		"""
		whdr = WAVEHDR()
		whdr.lpData = data
		whdr.dwBufferLength = len(data)
		with self._lock:
			with self._waveout_lock:
				self.open()
				with self._global_waveout_lock: winmm.waveOutPrepareHeader(self._waveout, LPWAVEHDR(whdr), sizeof(WAVEHDR))
				try:
					with self._global_waveout_lock: winmm.waveOutWrite(self._waveout, LPWAVEHDR(whdr), sizeof(WAVEHDR))
				except WindowsError, e:
					self.close()
					raise e
			self.sync()
			self._prev_whdr = whdr

	def sync(self):
		"""Synchronise with playback.
		This method blocks until the previously fed chunk of audio has finished playing.
		It is called automatically by L{feed}, so usually need not be called directly by the user.
		"""
		with self._lock:
			if not self._prev_whdr:
				return
			assert self._waveout, "waveOut None before wait"
			while not (self._prev_whdr.dwFlags & WHDR_DONE):
				winKernel.waitForSingleObject(self._waveout_event, winKernel.INFINITE)
			with self._waveout_lock:
				assert self._waveout, "waveOut None after wait"
				with self._global_waveout_lock: winmm.waveOutUnprepareHeader(self._waveout, LPWAVEHDR(self._prev_whdr), sizeof(WAVEHDR))
			self._prev_whdr = None

	def pause(self, switch):
		"""Pause or unpause playback.
		@param switch: C{True} to pause playback, C{False} to unpause.
		@type switch: bool
		"""
		with self._waveout_lock:
			if not self._waveout:
				return
			if switch:
				with self._global_waveout_lock: winmm.waveOutPause(self._waveout)
			else:
				with self._global_waveout_lock: winmm.waveOutRestart(self._waveout)

	def idle(self):
		"""Indicate that this player is now idle; i.e. the current continuous segment  of audio is complete.
		This will first call L{sync} to synchronise with playback.
		If L{closeWhenIdle} is C{True}, the output device will be closed.
		A subsequent call to L{feed} will reopen it.
		"""
		with self._lock:
			self.sync()
			with self._waveout_lock:
				if not self._waveout:
					return
				if self.closeWhenIdle:
					self._close()

	def stop(self):
		"""Stop playback.
		"""
		with self._waveout_lock:
			if not self._waveout:
				return
			try:
				with self._global_waveout_lock:
					# Pausing first seems to make waveOutReset respond faster on some systems.
					winmm.waveOutPause(self._waveout)
					winmm.waveOutReset(self._waveout)
			except WindowsError:
				# waveOutReset seems to fail randomly on some systems.
				pass
		# Unprepare the previous buffer and close the output device if appropriate.
		self.idle()

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
		with self._global_waveout_lock: winmm.waveOutClose(self._waveout)
		self._waveout = None

	def __del__(self):
		self.close()
		winKernel.kernel32.CloseHandle(self._waveout_event)
		self._waveout_event = None

def _getOutputDevices():
	caps = WAVEOUTCAPS()
	for devID in xrange(-1, winmm.waveOutGetNumDevs()):
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

def outputDeviceNameToID(name, useDefaultIfInvalid=False):
	"""Obtain the device ID of an output device given its name.
	@param name: The device name.
	@type name: str
	@param useDefaultIfInvalid: C{True} to use the default device (wave mapper) if there is no such device,
		C{False} to raise an exception.
	@return: The device ID.
	@rtype: int
	@raise LookupError: If there is no such device and C{useDefaultIfInvalid} is C{False}.
	"""
	for curID, curName in _getOutputDevices():
		if curName == name:
			return curID

	# No such ID.
	if useDefaultIfInvalid:
		return WAVE_MAPPER
	else:
		raise LookupError("No such device name")

fileWavePlayer = None
fileWavePlayerThread=None
def playWaveFile(fileName, async=True):
	"""plays a specified wave file.
"""
	global fileWavePlayer, fileWavePlayerThread
	f = wave.open(fileName,"r")
	if f is None: raise RuntimeError("can not open file %s"%fileName)
	if fileWavePlayer is not None:
		fileWavePlayer.stop()
	fileWavePlayer = WavePlayer(channels=f.getnchannels(), samplesPerSec=f.getframerate(),bitsPerSample=f.getsampwidth()*8, outputDevice=config.conf["speech"]["outputDevice"])
	fileWavePlayer.feed(f.readframes(f.getnframes()))
	if async:
		if fileWavePlayerThread is not None:
			fileWavePlayerThread.join()
		fileWavePlayerThread=threading.Thread(target=fileWavePlayer.idle)
		fileWavePlayerThread.start()
	else:
		fileWavePlayer.idle()
