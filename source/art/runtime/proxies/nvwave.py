# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU Lesser General Public License.
# See the file COPYING for more details.

"""NVWave module proxy for add-ons running in ART."""

import ctypes
import queue
import threading
import uuid

import Pyro5.api

from .base import ServiceProxyMixin


def playWaveFile(
	fileName: str,
	asynchronous: bool = True,
	isSpeechWaveFileCommand: bool = False,
) -> None:
	"""Play a wave file through NVDA's audio system.

	@param fileName: Path to the wave file to play
	@param asynchronous: Whether to play asynchronously (default True)
	@param isSpeechWaveFileCommand: Whether this is part of a speech sequence (default False)
	"""
	service = _NVWaveProxy._get_service()
	if service:
		try:
			service.playWaveFile(
				fileName=fileName, asynchronous=asynchronous, isSpeechWaveFileCommand=isSpeechWaveFileCommand
			)
		except Exception:
			# Silently fail like the original nvwave.playWaveFile
			pass


def isInError() -> bool:
	"""Check if the audio device is in an error state.

	@return: True if there's an audio device error, False otherwise
	"""
	result = _NVWaveProxy._call_service("isInError")
	return result if result is not None else False


class _NVWaveProxy(ServiceProxyMixin):
	"""Internal proxy class for nvwave service."""

	_service_env_var = "NVDA_ART_NVWAVE_SERVICE_URI"


class WavePlayer:
	"""Fake WavePlayer that routes audio through the synthesizer's _sendAudioData method.

	This allows synthesizers that create WavePlayer instances to work unchanged in ART.
	Audio is routed through the synthesizer's existing audio infrastructure.

	IMPORTANT: Uses a worker thread to avoid blocking the eSpeak native callback,
	preventing race conditions and segmentation faults.
	"""

	def __init__(self, channels=1, samplesPerSec=22050, bitsPerSample=16, outputDevice=None, buffered=True):
		self.channels = channels
		self.samplesPerSec = samplesPerSec
		self.bitsPerSample = bitsPerSample
		self.outputDevice = outputDevice
		self.buffered = buffered
		self._closed = False

		# Callback management for onDone callbacks
		self._pending_callbacks = {}
		self._callback_lock = threading.Lock()
		self._next_callback_id = 1

		# Each thread needs its own RPC proxy due to Pyro5 ownership restrictions
		self._thread_proxies = {}

		# Find the synth instance to route audio through
		# NOTE: We don't try to find it immediately because the synthesizer
		# might not have called setSynthInstance() yet during initialization.
		# We'll find it lazily in feed().
		self._synthInstance = None
		self._synthInstanceChecked = False

		# Create queue and worker thread to avoid blocking eSpeak callbacks
		self._audioQueue = queue.Queue()
		self._workerThread = threading.Thread(
			target=self._audioWorker, name=f"WavePlayer-{id(self)}", daemon=True
		)
		self._workerThread.start()

	def feed(self, data, size=None, onDone=None):
		"""Queue audio data for playback.

		IMPORTANT: This method is called from eSpeak's native callback thread.
		To prevent race conditions and segfaults, we immediately copy the audio
		data and queue it for processing by a worker thread.

		@param data: Audio data (bytes or ctypes pointer)
		@param size: Size in bytes if data is a ctypes pointer
		@param onDone: Optional callback function to call when this audio chunk finishes playing
		"""
		import logging

		logger = logging.getLogger("ART.WavePlayer")

		if self._closed:
			logger.debug("feed() called on closed WavePlayer")
			return

		try:
			# CRITICAL: Immediately convert ctypes pointer to bytes to avoid race condition
			# The eSpeak library expects this callback to return quickly
			if hasattr(data, "value") and size is not None:
				# Handle ctypes.c_void_p and similar pointer types
				byte_data = ctypes.string_at(data, size)
				logger.debug(f"Converted ctypes pointer to {len(byte_data)} bytes")
			elif isinstance(data, ctypes.POINTER(ctypes.c_int16)):
				# Handle POINTER(c_int16) specifically
				if size is None:
					raise ValueError("size must be specified for ctypes pointer")
				byte_data = ctypes.string_at(data, size)
				logger.debug(f"Converted ctypes POINTER(c_int16) to {len(byte_data)} bytes")
			else:
				byte_data = bytes(data)
				logger.debug(f"Got {len(byte_data)} bytes of audio data directly")

			# Handle onDone callback if provided
			callback_id = None
			if onDone is not None:
				with self._callback_lock:
					callback_id = self._next_callback_id
					self._next_callback_id += 1
					self._pending_callbacks[callback_id] = onDone
				logger.debug(f"Stored onDone callback with ID {callback_id}")

			# Queue the audio data and callback ID for processing by worker thread
			# This ensures the eSpeak callback returns immediately
			if not self._closed:
				self._audioQueue.put((byte_data, callback_id))
				logger.debug(f"Queued {len(byte_data)} bytes for worker thread with callback_id: {callback_id}")

		except Exception as e:
			logger.exception(f"Error in feed(): {e}")

	def stop(self):
		"""Stop playback immediately."""
		# Audio stopping is handled by the speech service
		pass

	def pause(self, switch):
		"""Pause or resume playback.

		@param switch: True to pause, False to resume
		"""
		# Pause/resume is handled by the speech service
		pass

	def idle(self):
		"""Wait for playback to complete via RPC proxy to NVDA Core."""
		import logging

		logger = logging.getLogger("ART.WavePlayer")

		# Find synth instance if needed
		if not self._synthInstance and not self._synthInstanceChecked:
			self._findSynthInstance(logger)

		if not self._synthInstance:
			logger.warning("No synthInstance available for idle() - cannot wait for audio completion")
			return

		if not hasattr(self._synthInstance, "_speechService"):
			logger.warning("SynthInstance has no _speechService - cannot wait for audio completion")
			return

		logger.debug(f"Attempting to wait for audio completion for {self._synthInstance.name}")

		try:
			# Get thread-specific proxy for RPC calls
			speech_service = self._getThreadSpeechProxy(logger)
			if not speech_service:
				logger.warning("Could not get thread-specific speech service proxy")
				return

			logger.debug(
				f"Calling waitForAudioCompletion via thread-specific RPC proxy for {self._synthInstance.name}"
			)
			# Call the RPC method with timeout to wait for real audio completion
			success = speech_service.waitForAudioCompletion(self._synthInstance.name, timeout=5.0)
			if success:
				logger.debug("Audio completion confirmed by NVDA Core")
			else:
				logger.debug("Audio completion returned False (no player or timeout)")

		except Exception as e:
			# Log warning but don't crash - preserve speech flow
			logger.warning(f"Audio completion wait failed: {e}")
			# Continue execution - better to have slight audio cutoff than broken speech

	def sync(self):
		"""Synchronize - ensure all queued audio has been sent."""
		# Synchronization is handled by the speech service
		pass

	def _audioWorker(self):
		"""Worker thread that processes audio data from the queue.

		This runs in a separate thread to avoid blocking the eSpeak callback.
		"""
		import logging
		import time

		logger = logging.getLogger("ART.WavePlayer.Worker")
		logger.debug("Audio worker thread started")

		last_heartbeat = time.time()
		heartbeat_interval = 5.0  # Log heartbeat every 5 seconds

		try:
			while not self._closed:
				try:
					# Periodic heartbeat to detect if worker thread is alive
					now = time.time()
					if now - last_heartbeat >= heartbeat_interval:
						logger.debug(
							f"Worker thread heartbeat - alive and processing (queue size: {self._audioQueue.qsize()})"
						)
						last_heartbeat = now

					# Get audio data and callback ID from queue with timeout
					queue_item = self._audioQueue.get(timeout=0.1)
					
					# Handle both old format (just bytes) and new format (bytes, callback_id) tuple
					if isinstance(queue_item, tuple):
						byte_data, callback_id = queue_item
					else:
						# Backward compatibility: treat as byte_data with no callback
						byte_data = queue_item
						callback_id = None

					# Check for shutdown sentinel
					if byte_data is None:
						logger.debug("Received shutdown sentinel")
						break

					# Find synth instance if needed
					if not self._synthInstance and not self._synthInstanceChecked:
						self._findSynthInstance(logger)

					if not self._synthInstance:
						logger.error(f"No synthInstance - discarding {len(byte_data)} bytes")
						continue

					# Send audio data using thread-specific sendAudioData method
					if hasattr(self._synthInstance, "_sendAudioData"):
						logger.debug(f"Sending {len(byte_data)} bytes via thread-specific method (callback_id: {callback_id})")

						try:
							# Call thread-specific version that creates its own proxy
							self._sendAudioDataThreadSafe(
								byte_data, self.samplesPerSec, self.channels, self.bitsPerSample, logger, callback_id
							)
						except Exception as audio_error:
							logger.exception(
								f"CRITICAL: _sendAudioDataThreadSafe failed - this might terminate ART process: {audio_error}"
							)
							# Don't re-raise - let the worker continue
							continue
					else:
						logger.error("synthInstance has no _sendAudioData method")

				except queue.Empty:
					# Timeout - check if we should continue
					continue
				except Exception as e:
					logger.exception(
						f"CRITICAL: Unexpected error in audio worker - this might terminate ART process: {e}"
					)
					# Continue processing despite errors
		except Exception as fatal_error:
			logger.exception(
				f"FATAL: Audio worker thread crashed - ART process will likely terminate: {fatal_error}"
			)
			# Try to force-flush the log before we die
			try:
				for handler in logger.handlers:
					handler.flush()
				for handler in logging.getLogger().handlers:
					handler.flush()
			except:
				pass
			raise  # Re-raise to potentially trigger faulthandler
		finally:
			logger.debug("Audio worker thread ending")

	def _findSynthInstance(self, logger):
		"""Find the synth instance (moved to separate method for worker thread)."""
		try:
			import art.runtime

			logger.debug("Looking for synthInstance via art.runtime.getRuntime()...")

			artRuntime = art.runtime.getRuntime()
			logger.debug(f"Found artRuntime: {artRuntime}")

			synthService = artRuntime.services.get("synth")
			if synthService:
				logger.debug(f"Found synthService: {synthService}")
				if hasattr(synthService, "_synthInstance"):
					self._synthInstance = synthService._synthInstance
					if self._synthInstance:
						logger.info(f"Successfully found synthInstance: {self._synthInstance}")
					else:
						logger.warning("synthService._synthInstance is None")
				else:
					logger.error("synthService has no _synthInstance attribute")
			else:
				logger.error("artRuntime has no synthService")
		except Exception as e:
			logger.exception(f"Error finding synthInstance: {e}")

		self._synthInstanceChecked = True

	def _getThreadSpeechProxy(self, logger):
		"""Get a thread-specific speech service proxy.

		Pyro5 proxies can only be used by the thread that created them.
		This method creates a separate proxy for each thread that needs RPC access.
		"""
		import os
		import threading

		import Pyro5.api

		thread_id = threading.get_ident()

		# Return existing proxy for this thread if available
		if thread_id in self._thread_proxies:
			return self._thread_proxies[thread_id]

		try:
			# Create new proxy for this thread
			speech_uri = os.environ.get("NVDA_ART_SPEECH_SERVICE_URI")
			if not speech_uri:
				logger.error("No NVDA_ART_SPEECH_SERVICE_URI found in environment")
				return None

			logger.debug(f"Creating thread-specific speech proxy for thread {thread_id}")
			speech_proxy = Pyro5.api.Proxy(speech_uri)
			speech_proxy._pyroTimeout = 2.0

			# Cache proxy for this thread
			self._thread_proxies[thread_id] = speech_proxy
			logger.debug(f"Created and cached speech proxy for thread {thread_id}")

			return speech_proxy

		except Exception as e:
			logger.exception(f"Failed to create thread-specific speech proxy: {e}")
			return None

	def _sendAudioDataThreadSafe(self, data, sampleRate, channels, bitsPerSample, logger, callback_id=None):
		"""Send audio data using thread-specific RPC proxy.

		This creates a separate proxy for each thread to avoid Pyro5 ownership conflicts.
		
		@param callback_id: Optional callback ID to pass to NVDA Core for onDone notification
		"""
		try:
			# Get thread-specific proxy
			speech_service = self._getThreadSpeechProxy(logger)
			if not speech_service:
				logger.error("No thread-specific speech service available for audio data!")
				return

			# Send audio via thread-specific proxy (same logic as _sendAudioData but with our proxy)
			MAX_CHUNK_SIZE = 64 * 1024  # 64KB chunks

			for i in range(0, len(data), MAX_CHUNK_SIZE):
				chunk = data[i : i + MAX_CHUNK_SIZE]
				chunk_num = i // MAX_CHUNK_SIZE + 1
				total_chunks = (len(data) + MAX_CHUNK_SIZE - 1) // MAX_CHUNK_SIZE
				logger.debug(f"Sending audio chunk {chunk_num} of {total_chunks} via thread proxy")

				# Prepare callback information for NVDA Core
				# Only pass callback info for the last chunk to avoid multiple callbacks
				chunk_callback_id = callback_id if i + MAX_CHUNK_SIZE >= len(data) else None
				
				speech_service.receiveAudioData(
					synthName=self._synthInstance.name,
					audioData=chunk,
					sampleRate=sampleRate,
					channels=channels,
					bitsPerSample=bitsPerSample,
					isLastChunk=False,
					callback_id=chunk_callback_id,
				)

			logger.debug(f"Successfully sent {len(data)} bytes via thread-specific proxy")

		except Exception as e:
			logger.exception(f"Error sending audio data via thread-specific proxy: {e}")
			raise

	def _onWavePlayerDone(self, callback_id):
		"""Trigger a pending onDone callback.
		
		This method is called by the synth service when audio playback completes.
		
		@param callback_id: The unique ID of the callback to execute
		"""
		import logging
		
		logger = logging.getLogger("ART.WavePlayer.Callback")
		
		if not callback_id:
			logger.warning("_onWavePlayerDone called with empty callback_id")
			return
		
		# Retrieve and remove the callback from pending callbacks
		with self._callback_lock:
			callback = self._pending_callbacks.pop(callback_id, None)
		
		if callback:
			logger.debug(f"Triggering onDone callback for ID {callback_id}")
			try:
				# Execute the original lambda from the synth driver
				callback()
				logger.debug(f"Successfully executed callback {callback_id}")
			except Exception as e:
				# Log any error from the callback itself, but don't re-raise
				logger.exception(f"Error executing onDone callback {callback_id}: {e}")
		else:
			logger.warning(f"Callback ID {callback_id} not found. Already triggered or expired.")

	def close(self):
		"""Close the player and release resources."""
		self._closed = True

		# Signal worker thread to stop
		try:
			self._audioQueue.put((None, None))  # Shutdown sentinel (updated for tuple format)
		except:
			pass  # Queue might be full or closed

		# Wait for worker thread to finish
		if self._workerThread.is_alive():
			self._workerThread.join(timeout=1.0)

		# Clean up pending callbacks to prevent memory leaks
		with self._callback_lock:
			if self._pending_callbacks:
				import logging
				logger = logging.getLogger("ART.WavePlayer")
				logger.debug(f"Cleaning up {len(self._pending_callbacks)} pending callbacks")
			self._pending_callbacks.clear()

		# Clean up thread-specific proxies
		self._thread_proxies.clear()
		self._synthInstance = None


# Export all public items
__all__ = ["playWaveFile", "isInError", "WavePlayer"]
