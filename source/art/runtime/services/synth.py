# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU Lesser General Public License.
# See the file COPYING for more details.

"""Synthesizer service for managing synth drivers in ART."""

import logging
from typing import Any, Dict, List, Optional

import Pyro5.api


@Pyro5.api.expose
class SynthService:
	"""Service for managing synthesizer drivers in the ART process.

	This service receives speech requests from NVDA Core and forwards them
	to the loaded synthesizer driver.
	"""

	def __init__(self):
		self._synthInstance: Optional[Any] = None
		self.logger = logging.getLogger("ART.SynthService")
		self.logger.info("SynthService initialized")

	def setSynthInstance(self, synth: Any) -> None:
		"""Set the synthesizer instance for this ART process.

		Called by the synthesizer driver when it initializes.

		@param synth: The synthesizer driver instance.
		"""
		self._synthInstance = synth
		self.logger.info(f"Synth instance set: {synth.name if hasattr(synth, 'name') else 'unknown'}")

	def speak(self, speechSequence: List[Any]) -> bool:
		"""Receive speech from NVDA Core and forward to the synth driver.

		@param speechSequence: List of text and speech commands.
		@return: True if speech was initiated successfully.
		"""
		if not self._synthInstance:
			self.logger.error("No synth instance available")
			return False

		try:
			self.logger.debug(f"Speaking {len(speechSequence)} items")

			# Deserialize speech commands
			deserialized = self._deserializeSpeechSequence(speechSequence)
			self._synthInstance.speak(deserialized)
			return True

		except Exception:
			self.logger.exception("Error in speak")
			return False

	def _deserializeSpeechSequence(self, serialized: List[Dict[str, Any]]) -> List[Any]:
		"""Deserialize speech sequence from Core."""
		from speech.commands import (
			BreakCommand,
			CharacterModeCommand,
			IndexCommand,
			LangChangeCommand,
			PhonemeCommand,
			PitchCommand,
			RateCommand,
			VolumeCommand,
		)

		deserialized = []

		for item in serialized:
			if isinstance(item, str):
				# Plain text, pass through
				deserialized.append(item)
				continue

			item_type = item.get("type")

			if item_type == "text":
				deserialized.append(item["text"])
			elif item_type == "IndexCommand":
				deserialized.append(IndexCommand(item["index"]))
			elif item_type == "CharacterModeCommand":
				deserialized.append(CharacterModeCommand(item["state"]))
			elif item_type == "BreakCommand":
				deserialized.append(BreakCommand(item.get("time")))
			elif item_type == "LangChangeCommand":
				deserialized.append(LangChangeCommand(item.get("lang")))
			elif item_type == "PitchCommand":
				deserialized.append(PitchCommand(item.get("offset", 0)))
			elif item_type == "RateCommand":
				deserialized.append(RateCommand(item.get("offset", 0)))
			elif item_type == "VolumeCommand":
				deserialized.append(VolumeCommand(item.get("offset", 0)))
			elif item_type == "PhonemeCommand":
				deserialized.append(PhonemeCommand(item["phoneme"]))
			else:
				self.logger.warning(f"Unknown serialized type: {item_type}")

		return deserialized

	def cancel(self) -> bool:
		"""Cancel current speech.

		@return: True if cancel was successful.
		"""
		if not self._synthInstance:
			self.logger.warning("No synth instance to cancel")
			return False

		try:
			self._synthInstance.cancel()
			return True
		except Exception:
			self.logger.exception("Error in cancel")
			return False

	def pause(self, switch: bool) -> bool:
		"""Pause or resume speech.

		@param switch: True to pause, False to resume.
		@return: True if the operation was successful.
		"""
		if not self._synthInstance:
			return False

		try:
			self._synthInstance.pause(switch)
			return True
		except Exception:
			self.logger.exception(f"Error in pause({switch})")
			return False

	def setRate(self, value: int) -> bool:
		"""Set the speech rate.

		@param value: Rate value (0-100).
		@return: True if successful.
		"""
		if not self._synthInstance:
			return False

		try:
			self._synthInstance.rate = value
			return True
		except Exception:
			self.logger.exception(f"Error setting rate to {value}")
			return False

	def setPitch(self, value: int) -> bool:
		"""Set the speech pitch.

		@param value: Pitch value (0-100).
		@return: True if successful.
		"""
		if not self._synthInstance:
			return False

		try:
			self._synthInstance.pitch = value
			return True
		except Exception:
			self.logger.exception(f"Error setting pitch to {value}")
			return False

	def setVolume(self, value: int) -> bool:
		"""Set the speech volume.

		@param value: Volume value (0-100).
		@return: True if successful.
		"""
		if not self._synthInstance:
			return False

		try:
			self._synthInstance.volume = value
			return True
		except Exception:
			self.logger.exception(f"Error setting volume to {value}")
			return False

	def setVoice(self, voiceId: str) -> bool:
		"""Set the current voice.

		@param voiceId: The ID of the voice to set.
		@return: True if successful.
		"""
		if not self._synthInstance:
			return False

		try:
			self._synthInstance.voice = voiceId
			return True
		except Exception:
			self.logger.exception(f"Error setting voice to {voiceId}")
			return False

	def getCurrentVoice(self) -> str:
		"""Get the current voice ID from the synthesizer.
		
		@return: Current voice ID, or empty string if no voice set.
		"""
		if not self._synthInstance:
			self.logger.warning("No synth instance available for getCurrentVoice")
			return ""
		
		try:
			# Use the _get_voice method to get actual current voice
			current_voice = self._synthInstance._get_voice()
			self.logger.debug(f"Current voice: {current_voice}")
			return current_voice
		except Exception:
			self.logger.exception("Error getting current voice")
			return ""
	
	def getDefaultVoice(self) -> str:
		"""Get the synthesizer's preferred default voice.
		
		@return: Default voice ID, or first available voice if no default specified.
		"""
		if not self._synthInstance:
			self.logger.warning("No synth instance available for getDefaultVoice")
			return ""
		
		try:
			# Check if synthesizer has a default voice method/property
			if hasattr(self._synthInstance, 'getDefaultVoice'):
				default_voice = self._synthInstance.getDefaultVoice()
				if default_voice:
					return default_voice
			
			# Fall back to first available voice if no explicit default
			available_voices = self._synthInstance.availableVoices
			if available_voices:
				first_voice_id = next(iter(available_voices.keys()))
				self.logger.debug(f"Using first available voice as default: {first_voice_id}")
				return first_voice_id
				
			self.logger.warning("No voices available for default voice")
			return ""
		except Exception:
			self.logger.exception("Error getting default voice")
			return ""
	
	def getCurrentRate(self) -> int:
		"""Get the current speech rate.
		
		@return: Current rate value.
		"""
		if not self._synthInstance:
			return 50  # Fallback default
		
		try:
			return self._synthInstance._get_rate()
		except Exception:
			self.logger.exception("Error getting current rate")
			return 50
	
	def getCurrentPitch(self) -> int:
		"""Get the current speech pitch.
		
		@return: Current pitch value.
		"""
		if not self._synthInstance:
			return 50  # Fallback default
		
		try:
			return self._synthInstance._get_pitch()
		except Exception:
			self.logger.exception("Error getting current pitch")
			return 50
	
	def getCurrentVolume(self) -> int:
		"""Get the current speech volume.
		
		@return: Current volume value.
		"""
		if not self._synthInstance:
			return 100  # Fallback default
		
		try:
			return self._synthInstance._get_volume()
		except Exception:
			self.logger.exception("Error getting current volume")
			return 100
	
	def getPropertyDefaults(self) -> Dict[str, Any]:
		"""Get the synthesizer's default property values.
		
		@return: Dictionary of property names to default values.
		"""
		if not self._synthInstance:
			return {
				'rate': 50,
				'pitch': 50, 
				'volume': 100,
				'voice': ''
			}
		
		try:
			defaults = {}
			
			# Get default values from synthesizer if available
			if hasattr(self._synthInstance, 'getPropertyDefaults'):
				defaults.update(self._synthInstance.getPropertyDefaults())
			else:
				# Use current values as defaults
				defaults['rate'] = self._synthInstance._get_rate()
				defaults['pitch'] = self._synthInstance._get_pitch()
				defaults['volume'] = self._synthInstance._get_volume()
				defaults['voice'] = self.getDefaultVoice()
			
			return defaults
		except Exception:
			self.logger.exception("Error getting property defaults")
			return {
				'rate': 50,
				'pitch': 50,
				'volume': 100,
				'voice': ''
			}
	
	def isValidVoice(self, voiceId: str) -> bool:
		"""Check if a voice ID is valid for this synthesizer.
		
		@param voiceId: Voice ID to validate.
		@return: True if the voice ID is valid.
		"""
		if not self._synthInstance or not voiceId:
			return False
		
		try:
			available_voices = self._synthInstance.availableVoices
			is_valid = voiceId in available_voices
			self.logger.debug(f"Voice validation: {voiceId} -> {is_valid}")
			return is_valid
		except Exception:
			self.logger.exception(f"Error validating voice {voiceId}")
			return False

	def getAvailableVoices(self) -> List[dict]:
		"""Get list of available voices.

		@return: List of voice info dictionaries.
		"""
		if not self._synthInstance:
			self.logger.warning("No synth instance available for getAvailableVoices")
			return []

		try:
			self.logger.debug(f"Getting available voices from synth instance: {self._synthInstance}")
			
			# Check if synth has availableVoices property
			if not hasattr(self._synthInstance, 'availableVoices'):
				self.logger.error(f"Synth instance {self._synthInstance} has no availableVoices property")
				return []
			
			available_voices = self._synthInstance.availableVoices
			self.logger.debug(f"Got availableVoices: {available_voices} (type: {type(available_voices)})")
			
			voices = []
			for voiceId, voiceInfo in available_voices.items():
				self.logger.debug(f"Processing voice: {voiceId} -> {voiceInfo} (type: {type(voiceInfo)})")
				voices.append(
					{"id": voiceId, "displayName": voiceInfo.displayName, "language": voiceInfo.language}
				)
			
			self.logger.debug(f"Returning {len(voices)} voices: {voices}")
			return voices
		except Exception:
			self.logger.exception("Error getting available voices")
			return []
