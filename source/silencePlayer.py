import threading
import nvwave
import config

class SilencePlayer(threading.Thread):
	"""
	Plays silence on the configured audio output device, to aide in audio ducking.
	Once instantiated, call enable() to start the silence, and disable() to stop.
	"""

	_sampleRate=22050
	_bitDepth=16
	_channels=1

	def __init__(self):
		# Create silence of about 200 ms in length
		self._data='\x00'*(self._sampleRate/2)
		self._wavePlayer=None
		self._initEvent=threading.Event()
		self._wakeEvent=threading.Event()
		super(SilencePlayer,self).__init__()
		self.daemon=True
		self.start()

	def run(self):
		self._initEvent.set()
		# Keep either waiting on an event, or feeding silence to the audio device
		while True:
			if not self._wakeEvent.isSet():
				# Ensure that the correct audio device is used each time it starts playing silence
				self._wavePlayer=None
				self._wakeEvent.wait()
			if not self._wavePlayer:
				self._wavePlayer=nvwave.WavePlayer(channels=self._channels, samplesPerSec=self._sampleRate, bitsPerSample=self._bitDepth, outputDevice=config.conf["speech"]["outputDevice"],wantDucking=False)
			self._wavePlayer.feed(self._data)

	def disable(self):
		""" Stops playing silence"""
		if self._wakeEvent.isSet():
			self._wakeEvent.clear()
			self._wavePlayer.stop()

	def enable(self):
		"""Starts playing silence"""
		if not self._wakeEvent.isSet():
			self._wakeEvent.set()
