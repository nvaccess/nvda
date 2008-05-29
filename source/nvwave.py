#nvwave.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Provides a simple Python interface to playing audio using the Windows multimedia waveOut functions, as well as other useful utilities.
"""

from __future__ import with_statement
import time
import threading
from ctypes import *
from ctypes.wintypes import *

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

# Initialise error checking.
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

	def __init__(self, channels, samplesPerSec, bitsPerSample, outputDevice=WAVE_MAPPER):
		"""Constructor.
		@param channels: The number of channels of audio; e.g. 2 for stereo, 1 for mono.
		@type channels: int
		@param samplesPerSec: Samples per second (hz).
		@type samplesPerSec: int
		@param bitsPerSample: The number of bits per sample.
		@type bitsPerSample: int
		@param outputDevice: The device ID or name of the audio output device to use.
		@type outputDevice: int or basestring
		@note: If C{outputDevice} is a name and no such device exists, the default device will be used.
		@raise WindowsError: If there was an error opening the audio output device.
		"""
		self.channels=channels
		self.samplesPerSec=samplesPerSec
		self.bitsPerSample=bitsPerSample
		if isinstance(outputDevice, basestring):
			outputDevice = outputDeviceNameToID(outputDevice, True)
		self.outputDeviceID = outputDevice
		self._open()
		self._whdr_lock = threading.RLock()

	def _open(self):
		wfx = WAVEFORMATEX()
		wfx.wFormatTag = WAVE_FORMAT_PCM
		wfx.nChannels = self.channels
		wfx.nSamplesPerSec = self.samplesPerSec
		wfx.wBitsPerSample = self.bitsPerSample
		wfx.nBlockAlign = self.bitsPerSample / 8 * self.channels
		wfx.nAvgBytesPerSec = self.samplesPerSec * wfx.nBlockAlign
		waveout = HWAVEOUT(0)
		winmm.waveOutOpen(byref(waveout), self.outputDeviceID, LPWAVEFORMATEX(wfx), 0, 0, CALLBACK_NULL)
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
		winmm.waveOutPrepareHeader(self._waveout, LPWAVEHDR(whdr), sizeof(WAVEHDR))
		try:
			winmm.waveOutWrite(self._waveout, LPWAVEHDR(whdr), sizeof(WAVEHDR))
			self.sync()
		except WindowsError, e:
			self.close()
			self._open()
			raise e
		with self._whdr_lock:
			self._prev_whdr = whdr

	def sync(self):
		"""Synchronise with playback.
		This method blocks until the previously fed chunk of audio has finished playing.
		It need only be called directly if there is no more audio to feed, but synchronisation is nevertheless desired.
		"""
		with self._whdr_lock:
			if not self._prev_whdr:
				return
			# todo: Wait for an event instead of spinning.
			while not (self._prev_whdr.dwFlags & WHDR_DONE):
				time.sleep(0.005)
			winmm.waveOutUnprepareHeader(self._waveout, LPWAVEHDR(self._prev_whdr), sizeof(WAVEHDR))
			self._prev_whdr = None

	def pause(self, switch):
		"""Pause or unpause playback.
		@param switch: C{True} to pause playback, C{False} to unpause.
		@type switch: bool
		"""
		if switch:
			winmm.waveOutPause(self._waveout)
		else:
			winmm.waveOutRestart(self._waveout)

	def stop(self):
		"""Stop playback.
		"""
		try:
			winmm.waveOutReset(self._waveout)
		except WindowsError:
			# waveOutReset seems to fail randomly on some systems.
			pass
		# Unprepare the previous buffer.
		self.sync()

	def close(self):
		"""Close the output device.
		@postcondition: The audio device is closed; this instance is no longer useable.
		"""
		self.stop()
		winmm.waveOutClose(self._waveout)
		self._waveout = None

def _getOutputDevices():
	caps = WAVEOUTCAPS()
	for devID in xrange(-1, winmm.waveOutGetNumDevs()):
		windll.winmm.waveOutGetDevCapsW(devID, byref(caps), sizeof(caps))
		yield devID, caps.szPname

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
		windll.winmm.waveOutGetDevCapsW(ID, byref(caps), sizeof(caps))
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
		return -1
	else:
		raise LookupError("No such device name")
