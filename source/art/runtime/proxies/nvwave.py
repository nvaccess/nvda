# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU Lesser General Public License.
# See the file COPYING for more details.

"""NVWave module proxy for add-ons running in ART."""

import ctypes
import queue
import threading
from typing import Optional
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
				fileName=fileName,
				asynchronous=asynchronous,
				isSpeechWaveFileCommand=isSpeechWaveFileCommand
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
	
	def __init__(self, channels=1, samplesPerSec=22050, 
	             bitsPerSample=16, outputDevice=None, buffered=True):
		self.channels = channels
		self.samplesPerSec = samplesPerSec
		self.bitsPerSample = bitsPerSample
		self.outputDevice = outputDevice
		self.buffered = buffered
		self._closed = False
		
		# Find the synth instance to route audio through
		# NOTE: We don't try to find it immediately because the synthesizer
		# might not have called setSynthInstance() yet during initialization.
		# We'll find it lazily in feed().
		self._synthInstance = None
		self._synthInstanceChecked = False
		
		# Create queue and worker thread to avoid blocking eSpeak callbacks
		self._audioQueue = queue.Queue()
		self._workerThread = threading.Thread(
			target=self._audioWorker, 
			name=f"WavePlayer-{id(self)}",
			daemon=True
		)
		self._workerThread.start()
	
	def feed(self, data, size=None):
		"""Queue audio data for playback.
		
		IMPORTANT: This method is called from eSpeak's native callback thread.
		To prevent race conditions and segfaults, we immediately copy the audio 
		data and queue it for processing by a worker thread.
		
		@param data: Audio data (bytes or ctypes pointer)
		@param size: Size in bytes if data is a ctypes pointer
		"""
		import logging
		logger = logging.getLogger("ART.WavePlayer")
		
		if self._closed:
			logger.debug("feed() called on closed WavePlayer")
			return
		
		try:
			# CRITICAL: Immediately convert ctypes pointer to bytes to avoid race condition
			# The eSpeak library expects this callback to return quickly
			if hasattr(data, 'value') and size is not None:
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
			
			# Queue the audio data for processing by worker thread
			# This ensures the eSpeak callback returns immediately
			if not self._closed:
				self._audioQueue.put(byte_data)
				logger.debug(f"Queued {len(byte_data)} bytes for worker thread")
			
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
		"""Wait for playback to complete."""
		# Synchronization is handled by the speech service
		pass
	
	def sync(self):
		"""Synchronize - ensure all queued audio has been sent."""
		# Synchronization is handled by the speech service
		pass
	
	def _audioWorker(self):
		"""Worker thread that processes audio data from the queue.
		
		This runs in a separate thread to avoid blocking the eSpeak callback.
		"""
		import logging
		logger = logging.getLogger("ART.WavePlayer.Worker")
		logger.debug("Audio worker thread started")
		
		try:
			while not self._closed:
				try:
					# Get audio data from queue with timeout
					byte_data = self._audioQueue.get(timeout=0.1)
					
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
					
					# Send audio data (this is now safe to block)
					if hasattr(self._synthInstance, '_sendAudioData'):
						logger.debug(f"Sending {len(byte_data)} bytes to synthInstance")
						try:
							self._synthInstance._sendAudioData(
								byte_data,
								self.samplesPerSec,
								self.channels,
								self.bitsPerSample
							)
						except Exception as audio_error:
							logger.exception(f"CRITICAL: _sendAudioData failed - this might terminate ART process: {audio_error}")
							# Don't re-raise - let the worker continue
							continue
					else:
						logger.error(f"synthInstance has no _sendAudioData method")
					
				except queue.Empty:
					# Timeout - check if we should continue
					continue
				except Exception as e:
					logger.exception(f"CRITICAL: Unexpected error in audio worker - this might terminate ART process: {e}")
					# Continue processing despite errors
		except Exception as fatal_error:
			logger.exception(f"FATAL: Audio worker thread crashed - ART process will likely terminate: {fatal_error}")
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
				if hasattr(synthService, '_synthInstance'):
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
	
	def close(self):
		"""Close the player and release resources."""
		self._closed = True
		
		# Signal worker thread to stop
		try:
			self._audioQueue.put(None)  # Shutdown sentinel
		except:
			pass  # Queue might be full or closed
		
		# Wait for worker thread to finish
		if self._workerThread.is_alive():
			self._workerThread.join(timeout=1.0)
		
		self._synthInstance = None


# Export all public items
__all__ = ["playWaveFile", "isInError", "WavePlayer"]
