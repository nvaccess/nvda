# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU Lesser General Public License.
# See the file COPYING for more details.

"""NVWave module proxy for add-ons running in ART."""

import ctypes
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
	
	def feed(self, data, size=None):
		"""Queue audio data for playback.
		
		@param data: Audio data (bytes or ctypes pointer)
		@param size: Size in bytes if data is a ctypes pointer
		"""
		import logging
		logger = logging.getLogger("ART.WavePlayer")
		
		if self._closed:
			logger.debug("feed() called on closed WavePlayer")
			return
		
		# Log detailed info about the audio data we're receiving
		actual_size = size if size is not None else (len(data) if hasattr(data, '__len__') else 'unknown')
		logger.info(f"feed() called with data type: {type(data)}, size param: {size}, actual_size: {actual_size}")
		
		# If it's a ctypes pointer, log some details about the raw data
		if hasattr(data, 'contents'):
			logger.info(f"ctypes pointer detected - contents type: {type(data.contents) if hasattr(data, 'contents') else 'N/A'}")
		
		if not self._synthInstance and not self._synthInstanceChecked:
			# Try to find the synthInstance - it should be available now
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
			
		if not self._synthInstance:
			logger.error(f"feed() called but no synthInstance - discarding {size if size else 'unknown'} bytes of audio")
			return
			
		try:
			# Convert ctypes pointer to bytes if needed
			if isinstance(data, ctypes.POINTER(ctypes.c_int16)):
				if size is None:
					raise ValueError("size must be specified for ctypes pointer")
				byte_data = ctypes.string_at(data, size)
				logger.info(f"Converted ctypes pointer to {len(byte_data)} bytes")
				
				# Log first few bytes as hex and as 16-bit samples
				if len(byte_data) >= 4:
					hex_bytes = ' '.join(f'{b:02x}' for b in byte_data[:8])
					logger.info(f"First 8 bytes as hex: {hex_bytes}")
					
					# Convert to 16-bit samples
					import struct
					num_samples = len(byte_data) // 2
					if num_samples > 0:
						samples = struct.unpack(f'<{num_samples}h', byte_data[:num_samples*2])
						logger.info(f"As 16-bit samples: {samples}")
						logger.info(f"Sample range: min={min(samples)}, max={max(samples)}")
			else:
				byte_data = bytes(data)
				logger.info(f"Got {len(byte_data)} bytes of audio data directly")
				
				# Log the raw bytes too
				if len(byte_data) >= 4:
					hex_bytes = ' '.join(f'{b:02x}' for b in byte_data[:8])
					logger.info(f"First 8 bytes as hex: {hex_bytes}")
			
			# Route through the synth's audio infrastructure
			if hasattr(self._synthInstance, '_sendAudioData'):
				logger.debug(f"Calling _sendAudioData with {len(byte_data)} bytes")
				self._synthInstance._sendAudioData(
					byte_data,
					self.samplesPerSec,
					self.channels,
					self.bitsPerSample
				)
			else:
				logger.error(f"synthInstance {self._synthInstance} has no _sendAudioData method!")
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
	
	def close(self):
		"""Close the player and release resources."""
		self._closed = True
		self._synthInstance = None


# Export all public items
__all__ = ["playWaveFile", "isInError", "WavePlayer"]
