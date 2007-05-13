import time
from ctypes import *
from ctypes.wintypes import *

winmm = windll.winmm

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
WAVE_MAPPER = UINT(-1)
MMSYSERR_NOERROR = 0

CALLBACK_NULL = 0
CALLBACK_FUNCTION = 0x30000
#waveOutProc = CFUNCTYPE(HANDLE, UINT, DWORD, DWORD, DWORD)
#WOM_DONE = 0x3bd

class WavePlayer:

	def __init__(self, channels, samplesPerSec, bitsPerSample):
		self.channels=channels
		self.samplesPerSec=samplesPerSec
		self.bitsPerSample=bitsPerSample
		wfx = WAVEFORMATEX()
		wfx.wFormatTag = WAVE_FORMAT_PCM
		wfx.nChannels = channels
		wfx.nSamplesPerSec = samplesPerSec
		wfx.wBitsPerSample = bitsPerSample
		wfx.nBlockAlign = bitsPerSample / 8 * channels
		wfx.nAvgBytesPerSec = samplesPerSec * wfx.nBlockAlign
		waveout = HANDLE(0)
		res = winmm.waveOutOpen(byref(waveout), WAVE_MAPPER, LPWAVEFORMATEX(wfx), DWORD(0), DWORD(0), DWORD(CALLBACK_NULL))
		if res != MMSYSERR_NOERROR:
			raise RuntimeError("Error opening wave device: code %d" % res)
		self._waveout = waveout.value
		self._prev_whdr = None

	def feed(self, data):
		try:
			whdr = WAVEHDR()
			whdr.lpData = data
			whdr.dwBufferLength = len(data)
			res = winmm.waveOutPrepareHeader(self._waveout, LPWAVEHDR(whdr), sizeof(WAVEHDR))
			if res != MMSYSERR_NOERROR:
				raise RuntimeError("Error preparing buffer: code %d" % res)
			res = winmm.waveOutWrite(self._waveout, LPWAVEHDR(whdr), sizeof(WAVEHDR))
			self.sync()
			if res != MMSYSERR_NOERROR:
				self.close()
				self.__init__(self.channels,self.samplesPerSec,self.bitsPerSample)
				raise RuntimeError("Error writing wave data: code %d" % res)
			self._prev_whdr = whdr
		except:
			debug.writeException("player.feed")

	def sync(self):
		# todo: Wait for an event instead of spinning.
		while self._prev_whdr and not (self._prev_whdr.dwFlags & WHDR_DONE):
			time.sleep(0.005)
		if not self._prev_whdr:
			return
		res = winmm.waveOutUnprepareHeader(self._waveout, LPWAVEHDR(self._prev_whdr), sizeof(WAVEHDR))
		if res != MMSYSERR_NOERROR:
			raise RuntimeError("Error unpreparing buffer: code %d" % res)
		self._prev_whdr = None

	def stop(self):
		winmm.waveOutReset(self._waveout)
		# Unprepare the previous buffer.
		self.sync()

	def close(self):
		self.stop()
		winmm.waveOutClose(self._waveout)
		self._waveout = None
