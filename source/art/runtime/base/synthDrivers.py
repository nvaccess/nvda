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


# ------------------------------------------------------------------
# ART Driver Setting Proxy Classes
# ------------------------------------------------------------------

class _ARTDriverSetting:
	
	def __init__(
		self,
		id: str,
		displayNameWithAccelerator: str,
		availableInSettingsRing: bool = False,
		defaultVal: Any = None,
		displayName: Optional[str] = None,
		useConfig: bool = True,
	):
		self.id = id
		self.displayNameWithAccelerator = displayNameWithAccelerator
		if not displayName:
			# Strip accelerator from displayNameWithAccelerator
			displayName = displayNameWithAccelerator.replace("&", "")
		self.displayName = displayName
		self.availableInSettingsRing = availableInSettingsRing
		self.defaultVal = defaultVal
		self.useConfig = useConfig
	
	def _get_metadata(self):
		"""Generate serializable metadata for RPC."""
		return {
			"type": "DriverSetting",
			"name": self.id,
			"displayNameWithAccelerator": self.displayNameWithAccelerator,
			"displayName": self.displayName,
			"availableInSettingsRing": self.availableInSettingsRing,
			"defaultVal": self.defaultVal,
			"useConfig": self.useConfig,
		}


class _ARTNumericDriverSetting(_ARTDriverSetting):
	
	def __init__(
		self,
		id: str,
		displayNameWithAccelerator: str,
		availableInSettingsRing: bool = False,
		defaultVal: int = 50,
		minVal: int = 0,
		maxVal: int = 100,
		minStep: int = 1,
		normalStep: int = 5,
		largeStep: int = 10,
		displayName: Optional[str] = None,
		useConfig: bool = True,
	):
		super().__init__(
			id,
			displayNameWithAccelerator,
			availableInSettingsRing=availableInSettingsRing,
			defaultVal=defaultVal,
			displayName=displayName,
			useConfig=useConfig,
		)
		self.minVal = minVal
		self.maxVal = max(maxVal, self.defaultVal)
		self.minStep = minStep
		self.normalStep = max(normalStep, minStep)
		self.largeStep = max(largeStep, self.normalStep)
	
	def _get_metadata(self):
		"""Generate serializable metadata for RPC."""
		return {
			"type": "NumericDriverSetting",
			"name": self.id,
			"displayNameWithAccelerator": self.displayNameWithAccelerator,
			"displayName": self.displayName,
			"availableInSettingsRing": self.availableInSettingsRing,
			"defaultVal": self.defaultVal,
			"minVal": self.minVal,
			"maxVal": self.maxVal,
			"minStep": self.minStep,
			"normalStep": self.normalStep,
			"largeStep": self.largeStep,
			"useConfig": self.useConfig,
		}


class _ARTBooleanDriverSetting(_ARTDriverSetting):
	"""Proxy for BooleanDriverSetting in ART."""
	
	def __init__(
		self,
		id: str,
		displayNameWithAccelerator: str,
		availableInSettingsRing: bool = False,
		displayName: Optional[str] = None,
		defaultVal: bool = False,
		useConfig: bool = True,
	):
		super().__init__(
			id,
			displayNameWithAccelerator,
			availableInSettingsRing=availableInSettingsRing,
			defaultVal=defaultVal,
			displayName=displayName,
			useConfig=useConfig,
		)
	
	def _get_metadata(self):
		"""Generate serializable metadata for RPC."""
		return {
			"type": "BooleanDriverSetting",
			"name": self.id,
			"displayNameWithAccelerator": self.displayNameWithAccelerator,
			"displayName": self.displayName,
			"availableInSettingsRing": self.availableInSettingsRing,
			"defaultVal": self.defaultVal,
			"useConfig": self.useConfig,
		}


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
		
		# Initialize voice tracking
		self._currentVoice: Optional[str] = None
		self._defaultVoice: Optional[str] = None
		self._voicesInitialized = False
		
		# Register this synth instance with the ART synth service
		self._registerWithARTService()
		
		# Register this synth driver with NVDA Core
		# TODO: In NVDA Core, the SpeechService will need to:
		# 1. Add this synth to the available synths list
		# 2. Make it selectable in NVDA's synth selection dialog
		# 3. Route speech to this synth when selected
		self._registerWithCore()
		
		# Initialize voice state after registration
		self._initializeVoiceState()
		
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
	
	# ------------------------------------------------------------------
	# Factory methods for creating driver settings (compatibility with NVDA)
	# ------------------------------------------------------------------
	
	@classmethod
	def VoiceSetting(cls):
		"""Factory function for creating voice setting."""
		return _ARTDriverSetting(
			"voice",
			"&Voice",
			availableInSettingsRing=True,
			displayName="Voice",
		)
	
	@classmethod
	def VariantSetting(cls):
		"""Factory function for creating variant setting."""
		return _ARTDriverSetting(
			"variant", 
			"V&ariant",
			availableInSettingsRing=True,
			displayName="Variant",
		)
	
	@classmethod
	def RateSetting(cls, minStep: int = 1):
		"""Factory function for creating rate setting."""
		return _ARTNumericDriverSetting(
			"rate",
			"&Rate",
			availableInSettingsRing=True,
			displayName="Rate",
			minStep=minStep,
		)
	
	@classmethod
	def RateBoostSetting(cls):
		"""Factory function for creating rate boost setting."""
		return _ARTBooleanDriverSetting(
			"rateBoost",
			"Rate boos&t",
			availableInSettingsRing=True,
			displayName="Rate boost",
		)
	
	@classmethod
	def VolumeSetting(cls, minStep: int = 1):
		"""Factory function for creating volume setting."""
		return _ARTNumericDriverSetting(
			"volume",
			"V&olume",
			availableInSettingsRing=True,
			displayName="Volume",
			minStep=minStep,
			normalStep=5,
		)
	
	@classmethod
	def PitchSetting(cls, minStep: int = 1):
		"""Factory function for creating pitch setting."""
		return _ARTNumericDriverSetting(
			"pitch",
			"&Pitch",
			availableInSettingsRing=True,
			displayName="Pitch",
			minStep=minStep,
		)
	
	@classmethod
	def InflectionSetting(cls, minStep: int = 1):
		"""Factory function for creating inflection setting."""
		return _ARTNumericDriverSetting(
			"inflection",
			"&Inflection",
			availableInSettingsRing=True,
			displayName="Inflection",
			minStep=minStep,
		)
	
	def _registerWithARTService(self):
		"""Register this synth instance with the ART synth service."""
		try:
			self.logger.debug("Attempting to register with ART synth service")
			
			# Get the synth service from the ART runtime using clean API
			import art.runtime
			runtime = art.runtime.getRuntime()
			self.logger.debug(f"Got runtime: {runtime}")
			
			self._synthService = runtime.services.get('synth')
			self.logger.debug(f"Got synthService: {self._synthService}")
			
			if self._synthService:
				self._synthService.setSynthInstance(self)
				self.logger.debug("Successfully registered with ART synth service")
			else:
				self.logger.warning("ART synthService not found in services")
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
				supportedNotifications=[notification.name for notification in self.supportedNotifications],
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
		# Log the speech sequence being processed
		self.logger.info(f"speak() called with {len(speechSequence)} items:")
		for i, item in enumerate(speechSequence):
			item_type = type(item).__name__ if hasattr(type(item), '__name__') else str(type(item))
			if isinstance(item, str):
				# Truncate long strings for logging
				item_preview = item[:50] + "..." if len(item) > 50 else item
				self.logger.info(f"  [{i}] {item_type}: '{item_preview}'")
			else:
				self.logger.info(f"  [{i}] {item_type}: {item}")
		
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
	
	def _initializeVoiceState(self):
		"""Initialize voice state with proper defaults."""
		try:
			if self._voicesInitialized:
				return
			
			# Get available voices to determine defaults
			available = self._getAvailableVoices()
			if not available:
				self.logger.warning("No voices available during initialization")
				self._voicesInitialized = True
				return
			
			# Set default voice (first available if no override)
			if not self._defaultVoice:
				self._defaultVoice = next(iter(available.keys()))
				self.logger.debug(f"Set default voice to first available: {self._defaultVoice}")
			
			# Set current voice to default if not already set
			if not self._currentVoice:
				self._currentVoice = self._defaultVoice
				self.logger.debug(f"Set current voice to default: {self._currentVoice}")
			
			self._voicesInitialized = True
			
		except Exception:
			self.logger.exception("Error initializing voice state")
			self._voicesInitialized = True
	
	def _get_voice(self) -> str:
		"""Get the current voice ID.
		
		Base implementation tracks current voice in _currentVoice.
		Subclasses can override for custom voice tracking.
		
		@return: The ID of the current voice.
		"""
		if not self._voicesInitialized:
			self._initializeVoiceState()
		
		if self._currentVoice:
			return self._currentVoice
		
		# Fallback: try to get first available voice
		try:
			available = self._getAvailableVoices()
			if available:
				first_voice = next(iter(available.keys()))
				self._currentVoice = first_voice
				return first_voice
		except Exception:
			self.logger.exception("Error getting fallback voice")
		
		return ""
	
	def _set_voice(self, value: str):
		"""Set the current voice.
		
		@param value: The ID of the voice to set.
		
		Base implementation updates _currentVoice if valid.
		Subclasses should override for actual voice switching.
		"""
		# Validate voice ID
		try:
			available = self.availableVoices
			if value not in available:
				self.logger.warning(f"Attempted to set invalid voice: {value}")
				return
		except Exception:
			self.logger.exception(f"Error validating voice {value}")
			return
		
		# Update current voice
		old_voice = self._currentVoice
		self._currentVoice = value
		self.logger.debug(f"Voice changed: {old_voice} -> {value}")
	
	def getDefaultVoice(self) -> str:
		"""Get this synthesizer's preferred default voice.
		
		Can be overridden by subclasses to provide synth-specific defaults.
		
		@return: Default voice ID.
		"""
		if not self._voicesInitialized:
			self._initializeVoiceState()
		
		return self._defaultVoice or ""
	
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
						"type": "NumericDriverSetting",
						"name": "rate",
						"displayNameWithAccelerator": "&Rate",
						"availableInSettingsRing": True,
						"defaultVal": 50,
						"minVal": 0,
						"maxVal": 100,
						"minStep": 1,
						"normalStep": 5,
						"largeStep": 10,
						"useConfig": True
					},
					...
				]
			}
		"""
		settings_metadata = []
		
		# Check if the class has supportedSettings defined
		if hasattr(cls, 'supportedSettings') and cls.supportedSettings:
			# Extract metadata from the setting proxy objects
			for setting in cls.supportedSettings:
				if hasattr(setting, '_get_metadata'):
					settings_metadata.append(setting._get_metadata())
				else:
					# Fallback for any settings that don't have _get_metadata
					settings_metadata.append({
						"type": "DriverSetting",
						"name": getattr(setting, 'id', 'unknown'),
						"displayNameWithAccelerator": getattr(setting, 'displayNameWithAccelerator', 'Unknown'),
					})
		else:
			# Default implementation provides basic settings that most synths support
			settings_metadata = [
				{
					"type": "NumericDriverSetting",
					"name": "rate",
					"displayNameWithAccelerator": "&Rate",
					"displayName": "Rate",
					"availableInSettingsRing": True,
					"defaultVal": 50,
					"minVal": 0,
					"maxVal": 100,
					"minStep": 1,
					"normalStep": 5,
					"largeStep": 10,
					"useConfig": True,
				},
				{
					"type": "NumericDriverSetting",
					"name": "pitch",
					"displayNameWithAccelerator": "&Pitch",
					"displayName": "Pitch",
					"availableInSettingsRing": True,
					"defaultVal": 50,
					"minVal": 0,
					"maxVal": 100,
					"minStep": 1,
					"normalStep": 5,
					"largeStep": 10,
					"useConfig": True,
				},
				{
					"type": "NumericDriverSetting",
					"name": "volume",
					"displayNameWithAccelerator": "&Volume",
					"displayName": "Volume",
					"availableInSettingsRing": True,
					"defaultVal": 100,
					"minVal": 0,
					"maxVal": 100,
					"minStep": 1,
					"normalStep": 5,
					"largeStep": 10,
					"useConfig": True,
				}
			]
		
		return {"supportedSettings": settings_metadata}
	
	def _get_availableVoices(self) -> OrderedDict[str, VoiceInfo]:
		"""Property getter for available voices with caching."""
		if not hasattr(self, "_availableVoices"):
			self._availableVoices = self._getAvailableVoices()
		return self._availableVoices
	
	availableVoices = property(_get_availableVoices)
	
	def _get_language(self) -> Optional[str]:
		"""Get the current voice's language.
		
		@return: The language code of the current voice, or None if no voice is set.
		"""
		try:
			current_voice = self.voice
			if current_voice and current_voice in self.availableVoices:
				return self.availableVoices[current_voice].language
		except Exception:
			self.logger.exception("Error getting current language")
		return None
	
	def _set_language(self, language: Optional[str]):
		"""Set the current language by finding a voice that supports it.
		
		@param language: The language code to set.
		"""
		raise NotImplementedError
	
	language = property(_get_language, _set_language)
	
	def _get_availableLanguages(self) -> Set[Optional[str]]:
		"""Get all available languages from the available voices.
		
		@return: A set of language codes available in the voices.
		"""
		try:
			return {self.availableVoices[v].language for v in self.availableVoices}
		except Exception:
			self.logger.exception("Error getting available languages")
			return set()
	
	availableLanguages = property(_get_availableLanguages)
	
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
	
	def _get_variant(self) -> str:
		"""Get the current variant.
		
		Subclasses should override this if they support variants.
		"""
		raise NotImplementedError
	
	def _set_variant(self, value: str):
		"""Set the current variant.
		
		The default implementation does nothing.
		Subclasses should override this if they support variants.
		"""
		pass
	
	variant = property(_get_variant, _set_variant)
	
	def _getAvailableVariants(self) -> OrderedDict[str, VoiceInfo]:
		"""Get available variants for the current voice.
		
		The default implementation returns an empty OrderedDict.
		Subclasses should override this if they support variants.
		
		@return: An OrderedDict of VoiceInfo instances keyed by variant ID.
		"""
		return OrderedDict()
	
	def _get_availableVariants(self) -> OrderedDict[str, VoiceInfo]:
		"""Property getter for available variants with caching."""
		if not hasattr(self, "_availableVariants"):
			self._availableVariants = self._getAvailableVariants()
		return self._availableVariants
	
	availableVariants = property(_get_availableVariants)
	
	def _get_inflection(self) -> int:
		"""Get the current inflection (0-100).
		
		The default implementation returns 0.
		Subclasses should override this if they support inflection.
		"""
		return 0
	
	def _set_inflection(self, value: int):
		"""Set the inflection (0-100).
		
		The default implementation does nothing.
		Subclasses should override this if they support inflection.
		"""
		pass
	
	inflection = property(_get_inflection, _set_inflection)
	
	def _paramToPercent(self, val: int, minVal: int = 0, maxVal: int = 100) -> int:
		"""Convert a parameter value to a percentage.
		
		@param val: The parameter value to convert.
		@param minVal: The minimum possible value.
		@param maxVal: The maximum possible value.
		@return: The percentage (0-100).
		"""
		if maxVal == minVal:
			return 50  # Avoid division by zero
		return int(round((val - minVal) * 100 / (maxVal - minVal)))

	def _percentToParam(self, percent: int, minVal: int = 0, maxVal: int = 100) -> int:
		"""Convert a percentage to a parameter value.
		
		@param percent: The percentage (0-100).
		@param minVal: The minimum possible value.
		@param maxVal: The maximum possible value.
		@return: The parameter value.
		"""
		return int(round(minVal + (percent * (maxVal - minVal) / 100)))
	
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
		import time
		if self._speechService:
			try:
				start_time = time.time()
				self.logger.debug(f"Notifying index reached: {index}")
				self._speechService.notifyIndexReached(self.name, index)
				rpc_time = time.time() - start_time
				if rpc_time > 0.1:
					self.logger.warning(f"SLOW: Index notification RPC took {rpc_time:.3f}s - possible hang!")
				else:
					self.logger.debug(f"Index {index} notification completed in {rpc_time:.3f}s")
			except Exception:
				rpc_time = time.time() - start_time
				self.logger.exception(f"Error notifying index {index} after {rpc_time:.3f}s")
	
	def _notifySpeechDone(self):
		"""Notify NVDA Core that speech has finished.
		
		TODO: In NVDA Core, the SpeechService will need to forward this
		to the synthDoneSpeaking extension point.
		"""
		import time
		if self._speechService:
			try:
				start_time = time.time()
				self.logger.debug("Notifying speech done")
				self._speechService.notifySpeechDone(self.name)
				rpc_time = time.time() - start_time
				if rpc_time > 0.1:
					self.logger.warning(f"SLOW: Speech done notification RPC took {rpc_time:.3f}s - possible hang!")
				else:
					self.logger.debug(f"Speech done notification completed in {rpc_time:.3f}s")
			except Exception:
				rpc_time = time.time() - start_time
				self.logger.exception(f"Error notifying speech done after {rpc_time:.3f}s")
	
	def _sendAudioData(self, data: bytes, sampleRate: int = 22050, channels: int = 1, bitsPerSample: int = 16):
		"""Send PCM audio data to NVDA Core for playback.
		
		This method is called by the fake WavePlayer when synthesizers create
		WavePlayer instances and feed audio to them.
		
		@param data: Raw PCM audio data.
		@param sampleRate: Sample rate in Hz (default 22050).
		@param channels: Number of channels (default 1 for mono).
		@param bitsPerSample: Bits per sample (default 16).
		"""
		import time
		start_time = time.time()
		self.logger.info(f"_sendAudioData called with {len(data)} bytes, {sampleRate}Hz, {channels}ch, {bitsPerSample}bit")
		if self._speechService:
			try:
				
				# For large audio data, we might need to chunk it
				MAX_CHUNK_SIZE = 64 * 1024  # 64KB chunks
				
				# Import base64 for encoding bytes data
				import base64
				
				for i in range(0, len(data), MAX_CHUNK_SIZE):
					chunk = data[i:i + MAX_CHUNK_SIZE]
					# Encode bytes as base64 string for JSON serialization
					encoded_chunk = base64.b64encode(chunk).decode('ascii')
					chunk_num = i//MAX_CHUNK_SIZE + 1
					total_chunks = (len(data) + MAX_CHUNK_SIZE - 1) // MAX_CHUNK_SIZE
					self.logger.debug(f"Sending audio chunk {chunk_num} of {total_chunks}")
					
					chunk_start = time.time()
					self._speechService.receiveAudioData(
						synthName=self.name,
						audioData=encoded_chunk,
						sampleRate=sampleRate,
						channels=channels,
						bitsPerSample=bitsPerSample,
						isLastChunk=False  # Never mark audio chunks as last - speech completion is handled separately
					)
					chunk_time = time.time() - chunk_start
					if chunk_time > 0.5:
						self.logger.warning(f"SLOW: Audio chunk {chunk_num} RPC took {chunk_time:.3f}s - possible hang!")
					elif chunk_time > 0.1:
						self.logger.debug(f"Audio chunk {chunk_num} RPC took {chunk_time:.3f}s")
				
				total_time = time.time() - start_time
				self.logger.info(f"Successfully sent {len(data)} bytes of audio data in {total_time:.3f}s")
				if total_time > 1.0:
					self.logger.warning(f"SLOW: Total _sendAudioData took {total_time:.3f}s - this could cause issues!")
			except Exception:
				total_time = time.time() - start_time
				self.logger.exception(f"Error sending audio data after {total_time:.3f}s")
		else:
			self.logger.error("No speech service available for audio data!")

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
		
		# Initialize voice tracking
		self._currentVoice: Optional[str] = None
		self._defaultVoice: Optional[str] = None
		self._voicesInitialized = False

		# Perform normal registrations
		try:
			self._registerWithARTService()
			self._registerWithCore()
			# Initialize voice state after registration
			self._initializeVoiceState()
			self.logger.info(
				f"Synthesizer driver {self.name} initialized in ART (fallback)"
			)
		except Exception:
			# Ensure we do not break synthesizer initialization
			self.logger.exception("Fallback initialization failed")


# Re-export for compatibility
__all__ = ["SynthDriver", "VoiceInfo"]
