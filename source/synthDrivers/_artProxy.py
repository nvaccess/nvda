# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Base proxy synthesizer driver for synthesizers running in ART."""

import json
from typing import Dict, List, Any, Optional
from collections import OrderedDict
import Pyro5.api
import Pyro5.errors

from synthDriverHandler import SynthDriver, VoiceInfo
from speech.commands import (
	IndexCommand, CharacterModeCommand, BreakCommand,
	LangChangeCommand, PitchCommand, RateCommand,
	VolumeCommand, PhonemeCommand
)
from speech.types import SpeechSequence
from logHandler import log


class ARTProxySynthDriver(SynthDriver):
	"""Base class for synthesizers running in ART.
	
	This proxy forwards all operations to the actual synthesizer in ART
	and handles serialization/deserialization of speech commands.
	"""
	
	# These are set by subclasses
	_artAddonName: str = ""
	_artSynthName: str = ""
	
	# Note: supportedSettings is now dynamically generated for each proxy class
	# by ARTSynthProxyGenerator based on metadata from the ART synthesizer
	
	# Fallback values if synthesizer provides no defaults (should rarely be used)
	FALLBACK_RATE = 50
	FALLBACK_PITCH = 50
	FALLBACK_VOLUME = 100

	def __init__(self):
		self._artManager = None
		self._synthService = None
		self._speechService = None
		self._connected = False
		
		# Cache for synth properties - will be populated from synthesizer
		self._property_cache = {}
		
		# Properties that need to be sent on next connection
		self._pending_property_updates = {}
		
		# Import here to avoid circular imports
		from art.manager import getARTManager
		self._artManager = getARTManager()
		
		if not self._artManager:
			raise RuntimeError("ART Manager not available")
			
		# Get the ART process for this addon
		self._artProcess = self._artManager.getAddonProcess(self._artAddonName)
		if not self._artProcess:
			raise RuntimeError(f"No ART process for addon {self._artAddonName}")
			
		# Get service proxies
		self._synthService = self._artProcess.getService("synth")
		if not self._synthService:
			raise RuntimeError("No synth service available in ART")
			
		# We also need the speech service to receive audio
		self._speechService = self._artManager.speechService
		
		self._connected = True
		
		# Initialize property cache with actual values from synthesizer
		self._initializePropertyCache()
		
		log.info(f"Connected to ART synthesizer: {self.name}")
	
	@classmethod
	def check(cls):
		"""Check if this ART synth is available."""
		# Check if ART manager exists and addon is loaded
		from art.manager import getARTManager
		artManager = getARTManager()
		if not artManager:
			return False
			
		# Check if the addon's ART process is running
		return artManager.isAddonRunning(cls._artAddonName)
	
	def speak(self, speechSequence: SpeechSequence):
		"""Serialize and forward speech to ART."""
		if not self._connected:
			log.warning(f"Cannot speak - ART synth {self.name} is disconnected")
			return
		
		# Send any pending property updates first
		if self._pending_property_updates:
			log.debug(f"Sending {len(self._pending_property_updates)} pending updates before speech")
			self._sendPendingUpdates()
			
		# Serialize the speech sequence
		serialized = self._serializeSpeechSequence(speechSequence)
		
		try:
			self._synthService.speak(serialized)
		except Exception:
			log.exception(f"Error speaking with ART synth {self.name}")
	
	def cancel(self):
		"""Cancel speech in ART."""
		if self._connected:
			try:
				self._synthService.cancel()
			except Exception:
				log.exception(f"Error cancelling ART synth {self.name}")
	
	def pause(self, switch: bool):
		"""Pause/resume speech in ART."""
		if self._connected:
			try:
				self._synthService.pause(switch)
			except Exception:
				log.exception(f"Error pausing ART synth {self.name}")
	
	def _initializePropertyCache(self):
		"""Initialize property cache with actual values from the synthesizer."""
		if not self._connected:
			return
		
		try:
			# Get property defaults from synthesizer
			defaults = self._synthService.getPropertyDefaults()
			self._property_cache.update(defaults)
			log.debug(f"Initialized property cache: {self._property_cache}")
			
			# Get current actual values to override defaults if different
			current_voice = self._synthService.getCurrentVoice()
			if current_voice:
				self._property_cache['voice'] = current_voice
			
			current_rate = self._synthService.getCurrentRate()
			self._property_cache['rate'] = current_rate
			
			current_pitch = self._synthService.getCurrentPitch()
			self._property_cache['pitch'] = current_pitch
			
			current_volume = self._synthService.getCurrentVolume()
			self._property_cache['volume'] = current_volume
			
			log.debug(f"Updated property cache with current values: {self._property_cache}")
		except Exception:
			log.exception(f"Error initializing property cache for {self.name}")
			# Set minimal fallback cache
			self._property_cache = {
				'rate': self.FALLBACK_RATE,
				'pitch': self.FALLBACK_PITCH,
				'volume': self.FALLBACK_VOLUME,
				'voice': ''
			}
	
	def _get_voice(self) -> str:
		"""Get current voice from ART."""
		if not self._connected:
			# Return cached voice or empty string if no cache
			return self._property_cache.get('voice', '')
		
		try:
			# Get actual current voice from synthesizer
			current_voice = self._synthService.getCurrentVoice()
			if current_voice:
				self._property_cache['voice'] = current_voice
				return current_voice
		except Exception:
			log.exception(f"Error getting current voice from ART synth {self.name}")
			self._connected = False
		
		# Return cached voice or empty string (no hardcoded fallbacks)
		return self._property_cache.get('voice', '')
	
	def _set_voice(self, value: str):
		"""Set voice in ART."""
		if not value:
			log.warning(f"Attempted to set empty voice on {self.name}")
			return
		
		# Validate voice ID first if connected
		if self._connected:
			try:
				if not self._synthService.isValidVoice(value):
					log.warning(f"Invalid voice ID '{value}' for {self.name}")
					return
			except Exception:
				log.exception(f"Error validating voice {value} for {self.name}")
				return
		
		# Update cache
		self._property_cache['voice'] = value
		
		# Set in synthesizer if connected
		if self._connected:
			try:
				self._synthService.setVoice(value)
				log.debug(f"Set voice to '{value}' on {self.name}")
			except Exception:
				log.exception(f"Error setting voice '{value}' in ART synth {self.name}")
	
	def _getAvailableVoices(self) -> OrderedDict[str, VoiceInfo]:
		"""Get available voices from ART."""
		if not self._connected:
			return OrderedDict()
			
		try:
			voiceData = self._synthService.getAvailableVoices()
			if not voiceData:
				log.warning(f"No voices returned from ART synth {self.name}")
				return OrderedDict()
			
			voices = OrderedDict()
			for vData in voiceData:
				if not isinstance(vData, dict):
					log.warning(f"Invalid voice data format: {vData}")
					continue
				
				voice_id = vData.get('id')
				if not voice_id:
					log.warning(f"Voice data missing ID: {vData}")
					continue
				
				display_name = vData.get('displayName', voice_id)
				language = vData.get('language')
				
				voices[voice_id] = VoiceInfo(voice_id, display_name, language)
			
			log.debug(f"Retrieved {len(voices)} voices from {self.name}")
			return voices
		except Pyro5.errors.CommunicationError:
			log.warning(f"Communication error getting voices from {self.name}")
			self._connected = False
			return OrderedDict()
		except Exception:
			log.exception(f"Error getting voices from ART synth {self.name}")
			return OrderedDict()
	
	def _get_rate(self) -> int:
		"""Get current rate from ART."""
		return self._get_synth_property('rate', self.FALLBACK_RATE)

	def _set_rate(self, value: int):
		"""Set rate in ART."""
		self._set_synth_property('rate', value, 'setRate')

	def _get_pitch(self) -> int:
		"""Get current pitch from ART."""
		return self._get_synth_property('pitch', self.FALLBACK_PITCH)

	def _set_pitch(self, value: int):
		"""Set pitch in ART."""
		self._set_synth_property('pitch', value, 'setPitch')

	def _get_volume(self) -> int:
		"""Get current volume from ART."""
		return self._get_synth_property('volume', self.FALLBACK_VOLUME)

	def _set_volume(self, value: int):
		"""Set volume in ART."""
		self._set_synth_property('volume', value, 'setVolume')
	
	def _get_synth_property(self, prop_name: str, default_value: Any) -> Any:
		"""Generic getter for synth properties with caching."""
		# If not connected, use cached value or fallback
		if not self._connected:
			cached_value = self._property_cache.get(prop_name)
			if cached_value is not None:
				return cached_value
			return default_value
		
		try:
			# Try to get current value from service
			method_name = f'getCurrent{prop_name.capitalize()}'
			if hasattr(self._synthService, method_name):
				value = getattr(self._synthService, method_name)()
				self._property_cache[prop_name] = value
				return value
			else:
				log.warning(f"Method {method_name} not available on ART synth service")
		except Pyro5.errors.CommunicationError:
			log.debugWarning(f"Communication error getting {prop_name}, using cached value")
			self._connected = False  # Mark as disconnected for retry
		except Exception:
			log.exception(f"Error getting {prop_name} from ART synth {self.name}")
		
		# Fall back to cached value or default
		cached_value = self._property_cache.get(prop_name)
		if cached_value is not None:
			return cached_value
		return default_value

	def _set_synth_property(self, prop_name: str, value: Any, method_name: str) -> None:
		"""Generic setter for synth properties with caching."""
		# Always update cache first
		self._property_cache[prop_name] = value
		
		if not self._connected:
			return
			
		try:
			getattr(self._synthService, method_name)(value)
		except Pyro5.errors.CommunicationError:
			log.warning(f"Failed to set {prop_name} in ART synth {self.name} - will retry on next speech")
			# Mark for retry
			self._pending_property_updates[prop_name] = value
		except Exception:
			log.exception(f"Error setting {prop_name} in ART synth {self.name}")

	def _sendPendingUpdates(self):
		"""Send any property updates that were cached while disconnected."""
		for prop_name, value in self._pending_property_updates.items():
			method_name = f'set{prop_name.capitalize()}'
			try:
				getattr(self._synthService, method_name)(value)
			except Exception:
				log.exception(f"Error sending pending {prop_name} update")
		self._pending_property_updates.clear()

	def terminate(self):
		"""Clean up proxy connection."""
		self._connected = False
		self._synthService = None
		self._speechService = None
	
	def _serializeSpeechSequence(self, sequence: SpeechSequence) -> List[Dict[str, Any]]:
		"""Serialize a speech sequence for transmission to ART."""
		serialized = []
		
		for item in sequence:
			if isinstance(item, str):
				serialized.append({
					"type": "text",
					"text": item
				})
			elif isinstance(item, IndexCommand):
				serialized.append({
					"type": "IndexCommand",
					"index": item.index
				})
			elif isinstance(item, CharacterModeCommand):
				serialized.append({
					"type": "CharacterModeCommand", 
					"state": item.state
				})
			elif isinstance(item, BreakCommand):
				serialized.append({
					"type": "BreakCommand",
					"time": item.time
				})
			elif isinstance(item, LangChangeCommand):
				serialized.append({
					"type": "LangChangeCommand",
					"lang": item.lang
				})
			elif isinstance(item, PitchCommand):
				serialized.append({
					"type": "PitchCommand",
					"offset": item.offset
				})
			elif isinstance(item, RateCommand):
				serialized.append({
					"type": "RateCommand",
					"offset": item.offset  
				})
			elif isinstance(item, VolumeCommand):
				serialized.append({
					"type": "VolumeCommand",
					"offset": item.offset
				})
			elif isinstance(item, PhonemeCommand):
				serialized.append({
					"type": "PhonemeCommand",
					"phoneme": item.phoneme
				})
			else:
				log.warning(f"Unknown speech command type: {type(item)}")
				
		return serialized
