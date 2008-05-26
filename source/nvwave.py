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

# Set argument types.
winmm.waveOutOpen.argtypes = (LPHWAVEOUT, UINT, LPWAVEFORMATEX, DWORD, DWORD, DWORD)

# Initialise error checking.
def _winmm_errcheck(res, func, args):
	if res != MMSYSERR_NOERROR:
		raise RuntimeError("%s: code %d" % (func.__name__, res))
for func in (
		winmm.waveOutOpen, winmm.waveOutPrepareHeader, winmm.waveOutWrite, winmm.waveOutUnprepareHeader,
		winmm.waveOutPause, winmm.waveOutRestart, winmm.waveOutReset, winmm.waveOutClose
):
	func.errcheck = _winmm_errcheck

class WavePlayer(object):
	"""Synchronously play a stream of audio.
	To use, construct an instance and feed it waveform audio using L{feed}.
	"""

	def __init__(self, channels, samplesPerSec, bitsPerSample, outputDeviceNumber=WAVE_MAPPER):
		"""Constructor.
		@param channels: The number of channels of audio; e.g. 2 for stereo, 1 for mono.
		@type channels: int
		@param samplesPerSec: Samples per second (hz).
		@type samplesPerSec: int
		@param bitsPerSample: The number of bits per sample.
		@type bitsPerSample: int
		@param outputDeviceNumber: The number of the audio output device to use.
		@type outputDeviceNumber: int
		@raise RuntimeError: If there was an error opening the audio output device.
		"""
		self.channels=channels
		self.samplesPerSec=samplesPerSec
		self.bitsPerSample=bitsPerSample
		self.outputDeviceNumber=outputDeviceNumber
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
		winmm.waveOutOpen(byref(waveout), self.outputDeviceNumber, LPWAVEFORMATEX(wfx), 0, 0, CALLBACK_NULL)
		self._waveout = waveout.value
		self._prev_whdr = None

	def feed(self, data):
		"""Feed a chunk of audio data to be played.
		This is normally synchronous.
		However, synchronisation occurs on the previous chunk, rather than the current chunk; i.e. calling this while no audio is playing will begin playing the chunk but return immediately.
		This allows for uninterrupted playback as long as a new chunk is fed before the previous chunk has finished playing.
		@param data: Waveform audio in the format specified when this instance was constructed.
		@type data: str
		@raise RuntimeError: If there was an error playing the audio.
		"""
		whdr = WAVEHDR()
		whdr.lpData = data
		whdr.dwBufferLength = len(data)
		winmm.waveOutPrepareHeader(self._waveout, LPWAVEHDR(whdr), sizeof(WAVEHDR))
		try:
			winmm.waveOutWrite(self._waveout, LPWAVEHDR(whdr), sizeof(WAVEHDR))
			self.sync()
		except RuntimeError, e:
			self.close()
			self._open()
			raise e
		with self._whdr_lock:
			self._prev_whdr = whdr

	def sync(self):
		"""Synchronise with playback.
		This method blocks until the previously fed chunk of audio has finished playing.
		It is called by L{feed} to wait for the previous chunk of audio to finish playing.
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
		winmm.waveOutReset(self._waveout)
		# Unprepare the previous buffer.
		self.sync()

	def close(self):
		"""Close the output device.
		@postcondition: The audio device is closed; this instance is no longer useable.
		"""
		self.stop()
		winmm.waveOutClose(self._waveout)
		self._waveout = None
