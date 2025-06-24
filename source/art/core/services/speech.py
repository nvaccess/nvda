# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Speech service for ART - handles speech from ART synthesizers."""

import queue
import threading
from typing import Dict, List

import nvwave
import Pyro5.api
from logHandler import log

from .base import BaseService


@Pyro5.api.expose
class SpeechService(BaseService):
	"""Receives speech from synthesizers running in ART and manages audio playback."""

	def __init__(self):
		super().__init__("SpeechService")
		self._registeredSynths: Dict[str, dict] = {}
		self._audioQueues: Dict[str, queue.Queue] = {}
		self._audioPlayers: Dict[str, nvwave.WavePlayer] = {}
		self._playbackThreads: Dict[str, threading.Thread] = {}
		self._stopEvents: Dict[str, threading.Event] = {}

	def registerSynthDriver(
		self,
		name: str,
		description: str,
		addon_name: str,
		supportedCommands: List[str],
		supportedNotifications: List[str],
	) -> bool:
		"""Register a synthesizer driver from ART.

		@param name: The synthesizer name (must match the module name)
		@param description: Human-readable description
		@param addon_name: The addon that provides this synth
		@param supportedCommands: List of supported command class names
		@param supportedNotifications: List of supported notifications
		@return: True if registration successful
		"""
		log.debug(f"SpeechService.registerSynthDriver called: name={name}, addon={addon_name}")
		try:
			self._registeredSynths[name] = {
				"description": description,
				"addon_name": addon_name,
				"supportedCommands": supportedCommands,
				"supportedNotifications": supportedNotifications,
				"isActive": False,
			}

			# Initialize audio infrastructure for this synth
			self._audioQueues[name] = queue.Queue()
			self._stopEvents[name] = threading.Event()

			log.info(f"Registered ART synthesizer: {name} from addon {addon_name}")
			log.debug(f"Supported commands: {supportedCommands}")
			log.debug(f"Supported notifications: {supportedNotifications}")

			# Generate a proxy synthesizer in Core
			log.debug(f"Generating proxy for {name}")
			from art.synthProxyGenerator import ARTSynthProxyGenerator

			proxy_class = ARTSynthProxyGenerator.generateProxy(addon_name, name, description)
			log.debug(f"Generated proxy class: {proxy_class}")

			# Note: synthDriverHandler.getSynthList() now dynamically queries ART for available synths

			log.debug(f"Registration completed successfully for {name}")
			return True
		except Exception:
			self._log_error("registerSynthDriver", name)
			return False

	def unregisterSynthDriver(self, name: str) -> bool:
		"""Unregister a synthesizer driver.

		@param name: The synthesizer name to unregister
		@return: True if unregistration successful
		"""
		try:
			if name in self._registeredSynths:
				# Stop any active playback
				if name in self._stopEvents:
					self._stopEvents[name].set()

				# Clean up resources
				if name in self._playbackThreads:
					thread = self._playbackThreads[name]
					if thread.is_alive():
						thread.join(timeout=1.0)
					del self._playbackThreads[name]

				if name in self._audioPlayers:
					self._audioPlayers[name].close()
					del self._audioPlayers[name]

				# Remove registrations
				del self._registeredSynths[name]
				if name in self._audioQueues:
					del self._audioQueues[name]
				if name in self._stopEvents:
					del self._stopEvents[name]

				log.info(f"Unregistered ART synthesizer: {name}")
				return True
			return False
		except Exception:
			self._log_error("unregisterSynthDriver", name)
			return False

	def notifyIndexReached(self, synthName: str, index: int):
		"""Handle index reached notification from ART synth.

		@param synthName: The synthesizer reporting the index
		@param index: The index that was reached
		"""
		try:
			log.debug(f"ART synth {synthName} reached index {index}")

			# TODO: Trigger the synthIndexReached extension point

		except Exception:
			self._log_error("notifyIndexReached", f"{synthName}, index={index}")

	def notifySpeechDone(self, synthName: str):
		"""Handle speech done notification from ART synth.

		@param synthName: The synthesizer that finished speaking
		"""
		try:
			log.debug(f"ART synth {synthName} finished speaking")

			# TODO: Trigger the synthDoneSpeaking extension point

		except Exception:
			self._log_error("notifySpeechDone", synthName)

	def receiveAudioData(
		self,
		synthName: str,
		audioData: bytes,
		sampleRate: int = 22050,
		channels: int = 1,
		bitsPerSample: int = 16,
		isLastChunk: bool = False,
	) -> bool:
		"""Receive PCM audio data from ART synth.

		@param synthName: The synthesizer sending audio
		@param audioData: Raw PCM audio data
		@param sampleRate: Sample rate in Hz
		@param channels: Number of channels (1=mono, 2=stereo)
		@param bitsPerSample: Bits per sample (usually 16)
		@param isLastChunk: Whether this is the last chunk of audio
		@return: True if audio was queued successfully
		"""
		try:
			if synthName not in self._registeredSynths:
				log.warning(f"Received audio from unregistered synth: {synthName}")
				return False

			# Ensure we have a player for this synth with correct format
			if synthName not in self._audioPlayers:
				self._createAudioPlayer(synthName, sampleRate, channels, bitsPerSample)

			# Queue the audio data
			self._audioQueues[synthName].put((audioData, isLastChunk))

			# Start playback thread if not running
			if synthName not in self._playbackThreads or not self._playbackThreads[synthName].is_alive():
				self._startPlaybackThread(synthName)

			log.debug(f"Queued {len(audioData)} bytes of audio from {synthName}")
			return True

		except Exception:
			self._log_error("receiveAudioData", f"{synthName}, {len(audioData)} bytes")
			return False

	def _createAudioPlayer(self, synthName: str, sampleRate: int, channels: int, bitsPerSample: int):
		"""Create a wave player for the given audio format."""
		try:
			# Get output device from config
			import config

			outputDevice = config.conf["speech"]["outputDevice"]

			player = nvwave.WavePlayer(
				channels=channels,
				samplesPerSec=sampleRate,
				bitsPerSample=bitsPerSample,
				outputDevice=outputDevice,
				buffered=True,
			)
			self._audioPlayers[synthName] = player
			log.debug(
				f"Created audio player for {synthName}: {sampleRate}Hz, {channels}ch, {bitsPerSample}bit"
			)

		except Exception:
			self._log_error("_createAudioPlayer", synthName)
			raise

	def _startPlaybackThread(self, synthName: str):
		"""Start the audio playback thread for a synth."""
		thread = threading.Thread(target=self._playbackLoop, args=(synthName,), name=f"ART-Audio-{synthName}")
		thread.daemon = True
		thread.start()
		self._playbackThreads[synthName] = thread
		log.debug(f"Started playback thread for {synthName}")

	def _playbackLoop(self, synthName: str):
		"""Audio playback loop for a synth."""
		audioQueue = self._audioQueues[synthName]
		player = self._audioPlayers[synthName]
		stopEvent = self._stopEvents[synthName]

		try:
			while not stopEvent.is_set():
				try:
					# Get audio data with timeout
					audioData, isLastChunk = audioQueue.get(timeout=0.1)

					# Feed to player
					player.feed(audioData)

					# If this was the last chunk, wait for playback to complete
					if isLastChunk:
						player.idle()
						self.notifySpeechDone(synthName)

				except queue.Empty:
					continue
				except Exception:
					log.exception(f"Error in playback loop for {synthName}")

		finally:
			log.debug(f"Playback thread ending for {synthName}")

	def cancelSpeech(self, synthName: str) -> bool:
		"""Cancel any ongoing speech for a synth.

		@param synthName: The synthesizer to cancel
		@return: True if cancelled successfully
		"""
		try:
			if synthName in self._audioQueues:
				# Clear the queue
				while not self._audioQueues[synthName].empty():
					try:
						self._audioQueues[synthName].get_nowait()
					except queue.Empty:
						break

				# Stop the player
				if synthName in self._audioPlayers:
					self._audioPlayers[synthName].stop()

				log.debug(f"Cancelled speech for {synthName}")
				return True
			return False

		except Exception:
			self._log_error("cancelSpeech", synthName)
			return False

	def pauseSpeech(self, synthName: str, pause: bool) -> bool:
		"""Pause or resume speech for a synth.

		@param synthName: The synthesizer to pause/resume
		@param pause: True to pause, False to resume
		@return: True if successful
		"""
		try:
			if synthName in self._audioPlayers:
				self._audioPlayers[synthName].pause(pause)
				log.debug(f"{'Paused' if pause else 'Resumed'} speech for {synthName}")
				return True
			return False

		except Exception:
			self._log_error("pauseSpeech", f"{synthName}, pause={pause}")
			return False

	def getRegisteredSynths(self) -> Dict[str, dict]:
		"""Get information about all registered ART synthesizers.

		@return: Dictionary of synth info keyed by synth name
		"""
		return self._registeredSynths.copy()
