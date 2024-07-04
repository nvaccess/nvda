# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
This module is copied to the scratchPad/synthDrivers folder and set as the synthesizer to capture speech
output during system tests.
Note: The name of this module must match the name of the synth driver, and the configured synthesizer
in the `tests/system/nvdaSettingsFiles/*.ini` files.
"""

import queue
import threading
import time

from logHandler import log

import synthDriverHandler
import extensionPoints
from speech.commands import IndexCommand
from speech.types import SpeechSequence

# inform those who want to know that there is new speech
post_speech = extensionPoints.Action()


class SpeechSpySynthDriver(synthDriverHandler.SynthDriver):
	"""A synth driver configured during system tests to capture speech output"""

	name = "SpeechSpySynthDriver"  # Name must match configuration files and module.
	description = "System test speech spy"

	def __init__(self):
		super().__init__()
		self._queuedSpeech: queue.SimpleQueue[SpeechSequence] = queue.SimpleQueue()
		self._cancel = False
		self._continue = True
		self._speechStarted = False
		self._doSpeechThread = threading.Thread(
			target=self._processSpeech,
			name="speech spy synth driver",
			daemon=True,
		)
		self._doSpeechThread.start()

	def terminate(self):
		self._cancel = True
		self._continue = False
		self._doSpeechThread.join()

	@classmethod
	def check(cls):
		return True

	supportedSettings = []
	supportedNotifications = {
		synthDriverHandler.synthIndexReached,
		synthDriverHandler.synthDoneSpeaking,
	}
	POLL_INTERVAL_SECS = 0.3

	def speak(self, speechSequence: SpeechSequence):
		log.debug(f"Sequence: {speechSequence}")
		self._cancel = False
		try:
			self._queuedSpeech.put(speechSequence, block=True, timeout=1)
		except queue.Full:
			log.error("Speech queue is full")

	def _doDoneSpeaking(self):
		log.debug("Done speaking, notifying synthDriverHandler")
		synthDriverHandler.synthDoneSpeaking.notify(synth=self)
		_yieldThread()

	def _doIndexReached(self, item: IndexCommand):
		log.debug(f"Speech IndexCommand reached: {item.index}, notifying synthDriverHandler")
		synthDriverHandler.synthIndexReached.notify(synth=self, index=item.index)
		_yieldThread()

	def _doNotifySequenceProcessed(self, speechSequence: SpeechSequence):
		log.debug("Before notify post_speech")
		post_speech.notify(speechSequence=speechSequence)
		log.debug("After post_speech notify")

	def _processSpeech(self):
		while self._continue:
			if self._cancel:
				# Allow _queuedSpeech to be cleared and ready to read from again.
				_yieldThread()
			else:
				try:
					speechSequence = self._queuedSpeech.get(
						block=True,
						timeout=self.POLL_INTERVAL_SECS,  # interruptable so that NVDA can exit.
					)
				except queue.Empty:
					if self._speechStarted:
						self._doDoneSpeaking()
						self._speechStarted = False
					continue
				self._speechStarted = True
				self._processSpeechSequence(speechSequence)
		log.debug("Stopping")

	def _processSpeechSequence(self, speechSequence: SpeechSequence):
		log.debug(f"Sequence: {speechSequence}")
		for item in speechSequence:
			if self._cancel:
				log.debug("Cancelled")
				# stop immediately, don't call done speaking
				return
			if isinstance(item, IndexCommand):
				self._doIndexReached(item)

		if self._cancel:
			# stop immediately, don't call done speaking
			return
		self._doNotifySequenceProcessed(speechSequence)

	def cancel(self):
		self._cancel = True
		log.debug("Cancelling")
		while not self._queuedSpeech.empty():
			log.debug("discarding.")
			try:
				self._queuedSpeech.get(
					block=True,  # incase _doSpeechThread is still reading.
					timeout=0.01,
				)
			except queue.Empty:
				log.debug("No items in queue.")

		self._speechStarted = False
		self._cancel = True


SynthDriver = SpeechSpySynthDriver


def _yieldThread():
	"""Intended to allow the main thread to process pending events."""
	time.sleep(0)
