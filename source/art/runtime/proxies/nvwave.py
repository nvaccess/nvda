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
		self._synthInstance = None
		try:
			import nvda_art
			if hasattr(nvda_art, 'artRuntime') and nvda_art.artRuntime:
				synthService = nvda_art.artRuntime.synthService
				if synthService and hasattr(synthService, '_synthInstance'):
					self._synthInstance = synthService._synthInstance
		except Exception:
			pass
	
	def feed(self, data, size=None):
		"""Queue audio data for playback.
		
		@param data: Audio data (bytes or ctypes pointer)
		@param size: Size in bytes if data is a ctypes pointer
		"""
		if self._closed or not self._synthInstance:
			return
			
		try:
			# Convert ctypes pointer to bytes if needed
			if isinstance(data, ctypes.POINTER(ctypes.c_int16)):
				if size is None:
					raise ValueError("size must be specified for ctypes pointer")
				byte_data = ctypes.string_at(data, size)
			else:
				byte_data = bytes(data)
			
			# Route through the synth's audio infrastructure
			if hasattr(self._synthInstance, '_sendAudioData'):
				self._synthInstance._sendAudioData(
					byte_data,
					self.samplesPerSec,
					self.channels,
					self.bitsPerSample
				)
		except Exception:
			# Silently fail like the real WavePlayer
			pass
	
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
