#tones.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Utilities to generate and play tones"""

import nvwave
import config
import globalVars
from logHandler import log
from ctypes import create_string_buffer, byref
import threading

SAMPLE_RATE = 44100
CHUNK_LENGTH = 45

_tonesThread = None

def _generateBeep(hz, length, left, right):
	from NVDAHelper import generateBeep
	bufSize=generateBeep(None,hz,length,left,right)
	buf=create_string_buffer(bufSize)
	generateBeep(buf,hz,length,left,right)
	return buf.raw

class TonesThread(threading.Thread):

	def __init__(self, *args, **kwargs):
		super(TonesThread, self).__init__(*args, **kwargs)
		self._player = nvwave.WavePlayer(channels=2, samplesPerSec=int(SAMPLE_RATE), bitsPerSample=16, outputDevice=config.conf["speech"]["outputDevice"], closeWhenIdle=False)
		self._hz = None
		self._length = 0
		self._left = None
		self._right = None
		self._requestEvent = threading.Event()
		self._keepRunning = True

	def request(self, hz, length, left, right):
		self._requestEvent.set()
		self._hz = hz
		self._length = length
		self._left = left
		self._right = right

	def run(self):
		while True:
			if self._length <= 0:
				# There is no request currently playing, so wait for another one.
				self._requestEvent.wait()
				if not self._keepRunning:
					break

			# Signal that we're now playing the last request.
			self._requestEvent.clear()

			self._player.feed(_generateBeep(self._hz, CHUNK_LENGTH, self._left, self._right))
			if not self._requestEvent.isSet():
				# There hasn't been a new request, so keep playing the current one in the next iteration if it hasn't finished.
				self._length -= CHUNK_LENGTH

			if self._length <= 0:
				# We've fed the last chunk of the current request.
				# Wait until the chunk finishes actually playing or until a new request arrives.
				self._requestEvent.wait(CHUNK_LENGTH / 1000.0)
				if self._length <= 0:
					# There has been no new request, so we're idle.
					self._player.idle()

	def terminate(self):
		self._keepRunning = False
		self._requestEvent.set()

def beep(hz,length,left=50,right=50):
	"""Plays a tone at the given hz, length, and stereo balance.
	@param hz: pitch in hz of the tone
	@type hz: float
	@param length: length of the tone in ms
	@type length: integer
	@param left: volume of the left channel (0 to 100)
	@type left: integer
	@param right: volume of the right channel (0 to 100)
	@type right: float
	""" 
	log.io("Beep at pitch %s, for %s ms, left volume %s, right volume %s"%(hz,length,left,right))
	if not _tonesThread:
		return
	_tonesThread.request(hz, length, left, right)

def initialize():
	global _tonesThread
	_tonesThread = TonesThread()
	_tonesThread.start()

def terminate():
	_tonesThread.terminate()
