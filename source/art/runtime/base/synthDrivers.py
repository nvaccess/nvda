# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU Lesser General Public License.
# See the file COPYING for more details.

"""Base synthesizer driver class for ART runtime."""

import os
from abc import abstractmethod, ABC
from typing import List, Dict, Any, Optional, OrderedDict, Set
import Pyro5.api
import logging


class VoiceInfo:
	"""Information about a synthesizer voice."""
	
	def __init__(self, id: str, displayName: str, language: Optional[str] = None):
		self.id = id
		self.displayName = displayName
		self.language = language


class SynthDriver(ABC):
	"""Base class for synthesizer drivers running in ART.
	
	This mirrors the NVDA SynthDriver API but runs in the ART process.
	
	Required implementations for subclasses:
	- check(): Class method to verify synth availability
	- speak(): Process speech sequences
	- _get_voice(): Return current voice ID
	- _getAvailableVoices(): Return available voices
	
	Optional implementations:
	- _set_voice(): Change voice (defaults to no-op if not overridden)
	- cancel(), pause(), terminate(): Speech control methods
	
	The voice property is provided by this base class and uses _get_voice() and _set_voice().
	"""
	
	#: The name of the synth; must be the original module file name.
	name: str = ""
	
	#: A description of the synth.
	description: str = ""
	
	#: The speech commands supported by the synth (e.g., IndexCommand, PitchCommand).
	# TODO: In NVDA Core, we'll need to serialize these command types for RPC
	supportedCommands: Set[type] = frozenset()
	
	#: The notifications provided by the synth (e.g., synthIndexReached, synthDoneSpeaking).
	supportedNotifications: Set[str] = frozenset()
	
	def __init__(self):
		"""Initialize the synthesizer driver and register with NVDA Core."""
		self.logger = logging.getLogger(f"ART.SynthDriver.{self.name}")
		self._speechService = None
		self._synthService = None
		
		# Register this synth instance with the ART synth service
		self._registerWithARTService()
		
		# Register this synth driver with NVDA Core
		# TODO: In NVDA Core, the SpeechService will need to:
		# 1. Add this synth to the available synths list
		# 2. Make it selectable in NVDA's synth selection dialog
		# 3. Route speech to this synth when selected
		self._registerWithCore()
		
		self.logger.info(f"Synthesizer driver {self.name} initialized in ART")

	@classmethod
	def __init_subclass__(cls, **kwargs):
		"""Wrap every concrete subclass' __init__ so registration still
		happens even if the subclass forgets to call super().__init__()."""
		super().__init_subclass__(**kwargs)
		# Do not wrap SynthDriver itself
		if cls is SynthDriver:
			return
		orig_init = cls.__init__

		def wrapped_init(self, *args, **kw):
			orig_init(self, *args, **kw)
			# If the base constructor didn't run, _speechService will be missing.
			if not hasattr(self, "_speechService"):
				SynthDriver._fallbackInit(self)

		cls.__init__ = wrapped_init
	
	def _registerWithARTService(self):
		"""Register this synth instance with the ART synth service."""
		try:
			# Get the synth service from the ART runtime
			import nvda_art
			if hasattr(nvda_art, 'artRuntime') and nvda_art.artRuntime:
				self._synthService = nvda_art.artRuntime.synthService
				if self._synthService:
					self._synthService.setSynthInstance(self)
					self.logger.debug("Registered with ART synth service")
		except Exception:
			self.logger.exception("Failed to register with ART synth service")
	
	def _registerWithCore(self):
		"""Register this synth driver with NVDA Core."""
		self.logger.debug(f"Attempting to register {self.name} with NVDA Core")
		try:
			# Get the speech service URI from environment
			speech_uri = os.environ.get("NVDA_ART_SPEECH_SERVICE_URI")
			self.logger.debug(f"Speech service URI from environment: {speech_uri}")
			if not speech_uri:
				self.logger.error("No NVDA_ART_SPEECH_SERVICE_URI found")
				return
			
			# Connect to NVDA Core's speech service
			self.logger.debug(f"Connecting to speech service at {speech_uri}")
			self._speechService = Pyro5.api.Proxy(speech_uri)
			self._speechService._pyroTimeout = 2.0
			
			# Get addon name from environment
			addon_name = os.environ.get("NVDA_ART_ADDON_NAME", "unknown")
			self.logger.debug(f"Addon name from environment: {addon_name}")
			
			# Get settings metadata for the proxy
			try:
				settings_metadata = self.__class__.getSupportedSettingsMetadata()
				self.logger.debug(f"Settings metadata for {self.name}: {settings_metadata}")
			except Exception:
				self.logger.exception(f"Failed to get settings metadata for {self.name}")
				settings_metadata = {}
			
			# Register this synth
			# TODO: In NVDA Core, SpeechService.registerSynthDriver will need to:
			# 1. Store this synth's info in a registry
			# 2. Make it available to synthDriverHandler.getSynthList()
			# 3. Create a proxy synth driver when this synth is selected
			self.logger.debug(f"Calling registerSynthDriver for {self.name}")
			result = self._speechService.registerSynthDriver(
				name=self.name,
				description=self.description,
				addon_name=addon_name,
				supportedCommands=[cmd.__name__ for cmd in self.supportedCommands],
				supportedNotifications=list(self.supportedNotifications),
				supportedSettings=settings_metadata
			)
			self.logger.debug(f"registerSynthDriver returned: {result}")
			
			if result:
				self.logger.info(f"Successfully registered {self.name} with NVDA Core")
			else:
				self.logger.error(f"Failed to register {self.name} with NVDA Core - registerSynthDriver returned False")
				
		except Exception:
			self.logger.exception("Error registering with NVDA Core")
	
	@classmethod
	@abstractmethod
	def check(cls) -> bool:
		"""Check whether this synth is available.
		
		This method should check whether the synth is available on the system,
		including checking for required DLLs, registry entries, etc.
		
		@return: True if the synth is available, False otherwise.
		"""
		raise NotImplementedError
	
	@abstractmethod
	def speak(self, speechSequence: List[Any]):
		"""Speak the given sequence of text and speech commands.
		
		@param speechSequence: A list of text strings and speech command objects.
		
		TODO: In NVDA Core, speech commands will need to be serialized for RPC.
		We'll need to create a serialization format for:
		- IndexCommand
		- CharacterModeCommand  
		- LangChangeCommand
		- BreakCommand
		- PitchCommand
		- RateCommand
		- VolumeCommand
		- PhonemeCommand
		"""
		raise NotImplementedError
	
	def cancel(self):
		"""Silence speech immediately.
		
		The default implementation does nothing.
		Subclasses should override this to stop speech.
		"""
		pass
	
	def pause(self, switch: bool):
		"""Pause or resume speech output.
		
		@param switch: True to pause, False to resume.
		
		The default implementation does nothing.
		Subclasses should override this if they support pausing.
		"""
		pass
	
	def _get_voice(self) -> str:
		"""Get the current voice ID.
		
		This method must be implemented by subclasses.
		
		@return: The ID of the current voice.
		"""
		raise NotImplementedError
	
	def _set_voice(self, value: str):
		"""Set the current voice.
		
		@param value: The ID of the voice to set.
		
		The default implementation does nothing.
		Subclasses should override this to change voices.
		"""
		pass
	
	voice = property(_get_voice, _set_voice)
	"""Voice property for getting and setting the current voice.
	
	This property is implemented using _get_voice() and _set_voice() methods.
	Subclasses must implement _get_voice() to return the current voice ID.
	Subclasses may implement _set_voice() to support changing voices.
	Accessing this property on a driver that hasn't implemented _get_voice() 
	will raise NotImplementedError.
	"""
	
	@abstractmethod
	def _getAvailableVoices(self) -> OrderedDict[str, VoiceInfo]:
		"""Get all available voices.
		
		@return: An OrderedDict of VoiceInfo instances keyed by voice ID.
		"""
		raise NotImplementedError
	
	@classmethod
	def getSupportedSettingsMetadata(cls) -> Dict[str, Any]:
		"""Get metadata describing the settings supported by this synth driver.
		
		This method is called by ARTSynthProxyGenerator before the synth is instantiated
		to create the proxy class with the correct supportedSettings attribute.
		
		@return: Dictionary containing settings metadata in the format:
			{
				"supportedSettings": [
					{
						"name": "rate",
						"type": "NumericDriverSetting", 
						"params": {"displayNameWithAccelerator": "&Rate", "minVal": 0, "maxVal": 100, "defaultVal": 50}
					},
					...
				]
			}
		"""
		# Default implementation provides basic settings that most synths support
		return {
			"supportedSettings": [
				{
					"name": "rate",
					"type": "NumericDriverSetting",
					"params": {
						"displayNameWithAccelerator": "&Rate",
						"minVal": 0,
						"maxVal": 100, 
						"defaultVal": 50
					}
				},
				{
					"name": "pitch", 
					"type": "NumericDriverSetting",
					"params": {
						"displayNameWithAccelerator": "&Pitch",
						"minVal": 0,
						"maxVal": 100,
						"defaultVal": 50
					}
				},
				{
					"name": "volume",
					"type": "NumericDriverSetting", 
					"params": {
						"displayNameWithAccelerator": "&Volume",
						"minVal": 0,
						"maxVal": 100,
						"defaultVal": 100
					}
				}
			]
		}
	
	def _get_availableVoices(self) -> OrderedDict[str, VoiceInfo]:
		"""Property getter for available voices with caching."""
		if not hasattr(self, "_availableVoices"):
			self._availableVoices = self._getAvailableVoices()
		return self._availableVoices
	
	availableVoices = property(_get_availableVoices)
	
	def _get_rate(self) -> int:
		"""Get the current speech rate (0-100).
		
		The default implementation returns 50.
		Subclasses should override this.
		"""
		return 50
	
	def _set_rate(self, value: int):
		"""Set the speech rate (0-100).
		
		The default implementation does nothing.
		Subclasses should override this.
		"""
		pass
	
	rate = property(_get_rate, _set_rate)
	
	def _get_pitch(self) -> int:
		"""Get the current pitch (0-100).
		
		The default implementation returns 50.
		Subclasses should override this.
		"""
		return 50
	
	def _set_pitch(self, value: int):
		"""Set the pitch (0-100).
		
		The default implementation does nothing.
		Subclasses should override this.
		"""
		pass
	
	pitch = property(_get_pitch, _set_pitch)
	
	def _get_volume(self) -> int:
		"""Get the current volume (0-100).
		
		The default implementation returns 100.
		Subclasses should override this.
		"""
		return 100
	
	def _set_volume(self, value: int):
		"""Set the volume (0-100).
		
		The default implementation does nothing.
		Subclasses should override this.
		"""
		pass
	
	volume = property(_get_volume, _set_volume)
	
	def terminate(self):
		"""Terminate the synthesizer.
		
		This is called when the synthesizer is being unloaded.
		Subclasses should override this to clean up resources.
		"""
		pass
	
	def _notifyIndexReached(self, index: int):
		"""Notify NVDA Core that a speech index has been reached.
		
		@param index: The index that was reached.
		
		TODO: In NVDA Core, the SpeechService will need to forward this
		to the synthIndexReached extension point.
		"""
		if self._speechService:
			try:
				self._speechService.notifyIndexReached(self.name, index)
			except Exception:
				self.logger.exception(f"Error notifying index {index}")
	
	def _notifySpeechDone(self):
		"""Notify NVDA Core that speech has finished.
		
		TODO: In NVDA Core, the SpeechService will need to forward this
		to the synthDoneSpeaking extension point.
		"""
		if self._speechService:
			try:
				self._speechService.notifySpeechDone(self.name)
			except Exception:
				self.logger.exception("Error notifying speech done")
	
	def _sendAudioData(self, data: bytes, sampleRate: int = 22050, channels: int = 1, bitsPerSample: int = 16):
		"""Send PCM audio data to NVDA Core for playback.
		
		This method is called by the fake WavePlayer when synthesizers create
		WavePlayer instances and feed audio to them.
		
		@param data: Raw PCM audio data.
		@param sampleRate: Sample rate in Hz (default 22050).
		@param channels: Number of channels (default 1 for mono).
		@param bitsPerSample: Bits per sample (default 16).
		"""
		if self._speechService:
			try:
				# For large audio data, we might need to chunk it
				MAX_CHUNK_SIZE = 64 * 1024  # 64KB chunks
				
				for i in range(0, len(data), MAX_CHUNK_SIZE):
					chunk = data[i:i + MAX_CHUNK_SIZE]
					self._speechService.receiveAudioData(
						synthName=self.name,
						audioData=chunk,
						sampleRate=sampleRate,
						channels=channels,
						bitsPerSample=bitsPerSample,
						isLastChunk=(i + MAX_CHUNK_SIZE >= len(data))
					)
			except Exception:
				self.logger.exception("Error sending audio data")

	# ------------------------------------------------------------------
	# Fallback logic when subclass skips super().__init__()
	# ------------------------------------------------------------------
	def _fallbackInit(self):
		"""Initialize essential state and perform registrations when the
		concrete SynthDriver subclass did not call super().__init__()."""
		# Basic attributes expected by other helpers
		self.logger = logging.getLogger(f"ART.SynthDriver.{self.name}")
		self._speechService = None
		self._synthService = None

		# Perform normal registrations
		try:
			self._registerWithARTService()
			self._registerWithCore()
			self.logger.info(
				f"Synthesizer driver {self.name} initialized in ART (fallback)"
			)
		except Exception:
			# Ensure we do not break synthesizer initialization
			self.logger.exception("Fallback initialization failed")


# Re-export for compatibility
__all__ = ["SynthDriver", "VoiceInfo"]
