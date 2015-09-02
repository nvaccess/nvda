# -*- coding: UTF-8 -*-
#synthDriverHandler.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2015 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Joseph Lee

from copy import deepcopy
import os
import pkgutil
import config
import baseObject
import globalVars
from logHandler import log
from  synthSettingsRing import SynthSettingsRing
import languageHandler
import speechDictHandler
import synthDrivers

_curSynth=None
_audioOutputDevice=None

def initialize():
	config.addConfigDirsToPythonPackagePath(synthDrivers)

def changeVoice(synth, voice):
	# This function can be called with no voice if the synth doesn't support the voice setting (only has one voice).
	if voice:
		synth.voice = voice
	c=config.conf["speech"][synth.name]
	c.spec=synth.getConfigSpec()
	#start or update the synthSettingsRing
	if globalVars.settingsRing: globalVars.settingsRing.updateSupportedSettings(synth)
	else:  globalVars.settingsRing = SynthSettingsRing(synth)
	speechDictHandler.loadVoiceDict(synth)

def _getSynthDriver(name):
	return __import__("synthDrivers.%s" % name, globals(), locals(), ("synthDrivers",)).SynthDriver

def getSynthList():
	synthList=[]
	# The synth that should be placed at the end of the list.
	lastSynth = None
	for loader, name, isPkg in pkgutil.iter_modules(synthDrivers.__path__):
		if name.startswith('_'):
			continue
		try:
			synth=_getSynthDriver(name)
		except:
			log.error("Error while importing SynthDriver %s"%name,exc_info=True)
			continue
		try:
			if synth.check():
				if synth.name == "silence":
					lastSynth = (synth.name,synth.description)
				else:
					synthList.append((synth.name,synth.description))
			else:
				log.debugWarning("Synthesizer '%s' doesn't pass the check, excluding from list"%name)
		except:
			log.error("",exc_info=True)
	synthList.sort(key=lambda s : s[1].lower())
	if lastSynth:
		synthList.append(lastSynth)
	return synthList

def getSynth():
	return _curSynth

def setSynth(name,isFallback=False):
	global _curSynth,_audioOutputDevice
	if name is None: 
		_curSynth.terminate()
		_curSynth=None
		return True
	if name=='auto':
		name='espeak'
	if _curSynth:
		_curSynth.cancel()
		_curSynth.terminate()
		prevSynthName = _curSynth.name
		_curSynth = None
	else:
		prevSynthName = None
	try:
		newSynth=_getSynthDriver(name)()
		if config.conf["speech"].isSet(name):
			newSynth.loadSettings()
		else:
			# Create the new section.
			config.conf["speech"][name]={}
			if newSynth.isSupported("voice"):
				voice=newSynth.voice
			else:
				voice=None
			# We need to call changeVoice here so that required initialisation can be performed.
			changeVoice(newSynth,voice)
			newSynth.saveSettings() #save defaults
		_curSynth=newSynth
		_audioOutputDevice=config.conf["speech"]["outputDevice"]
		if not isFallback:
			config.conf["speech"]["synth"]=name
		log.info("Loaded synthDriver %s"%name)
		return True
	except:
		log.error("setSynth", exc_info=True)
		if prevSynthName:
			setSynth(prevSynthName,isFallback=True)
		elif name not in ('espeak','silence'):
			setSynth('espeak',isFallback=True)
		elif name=='espeak':
			setSynth('silence',isFallback=True)
		return False

def handleConfigProfileSwitch():
	conf = config.conf["speech"]
	if conf["synth"] != _curSynth.name or conf["outputDevice"] != _audioOutputDevice:
		setSynth(conf["synth"])
		return
	_curSynth.loadSettings(onlyChanged=True)

class SynthSetting(object):
	"""Represents a synthesizer setting such as voice or variant.
	"""
	#: Configuration specification of this particular setting for config file validator.
	#: @type: str
	configSpec="string(default=None)"

	def __init__(self,name,displayNameWithAccelerator,availableInSynthSettingsRing=True,displayName=None):
		"""
		@param name: internal name of the setting
		@type name: str
		@param displayNameWithAccelerator: the localized string shown in voice settings dialog
		@type displayNameWithAccelerator: str
		@param displayName: the localized string used in synth settings ring or None to use displayNameWithAccelerator
		@type displayName: str
		@param availableInSynthSettingsRing: Will this option be available in synthesizer settings ring?
		@type availableInSynthSettingsRing: bool
		"""
		self.name=name
		self.displayNameWithAccelerator=displayNameWithAccelerator
		#: @deprecated: Use L{displaynameWithAccelerator} and L{displayName} instead.
		self.i18nName=displayNameWithAccelerator
		if not displayName:
			# Strip accelerator from displayNameWithAccelerator.
			displayName=displayNameWithAccelerator.replace("&","")
		self.displayName=displayName
		self.availableInSynthSettingsRing=availableInSynthSettingsRing

class NumericSynthSetting(SynthSetting):
	"""Represents a numeric synthesizer setting such as rate, volume or pitch."""
	configSpec="integer(default=50,min=0,max=100)"

	def __init__(self,name,displayNameWithAccelerator,availableInSynthSettingsRing=True,minStep=1,normalStep=5,largeStep=10,displayName=None):
		"""
		@param minStep: Specifies the minimum step between valid values for each numeric setting. For example, if L{minStep} is set to 10, setting values can only be multiples of 10; 10, 20, 30, etc.
		@type minStep: int
		@param normalStep: Specifies the step between values that a user will normally prefer. This is used in the settings ring.
		@type normalStep: int
		@param largeStep: Specifies the step between values if a large adjustment is desired. This is used for pageUp/pageDown on sliders in the Voice Settings dialog.
		@type largeStep: int
		@note: If necessary, the step values will be normalised so that L{minStep} <= L{normalStep} <= L{largeStep}.
		"""
		super(NumericSynthSetting,self).__init__(name,displayNameWithAccelerator,availableInSynthSettingsRing=availableInSynthSettingsRing,displayName=displayName)
		self.minStep=minStep
		self.normalStep=max(normalStep,minStep)
		self.largeStep=max(largeStep,self.normalStep)

class BooleanSynthSetting(SynthSetting):
	"""Represents a boolean synthesiser setting such as rate boost.
	"""
	configSpec = "boolean(default=False)"

	def __init__(self, name,displayNameWithAccelerator,availableInSynthSettingsRing=False,displayName=None):
		super(BooleanSynthSetting, self).__init__(name,displayNameWithAccelerator,availableInSynthSettingsRing=availableInSynthSettingsRing,displayName=displayName)

class SynthDriver(baseObject.AutoPropertyObject):
	"""Abstract base synthesizer driver.
	Each synthesizer driver should be a separate Python module in the root synthDrivers directory containing a SynthDriver class which inherits from this base class.
	
	At a minimum, synth drivers must set L{name} and L{description} and override the L{check} method.
	The methods L{speak}, L{cancel} and L{pause} should be overridden as appropriate.
	L{supportedSettings} should be set as appropriate for the settings supported by the synthesiser.
	There are factory functions to create L{SynthSetting} instances for common settings; e.g. L{VoiceSetting} and L{RateSetting}.
	Each setting is retrieved and set using attributes named after the setting;
	e.g. the L{voice} attribute is used for the L{voice} setting.
	These will usually be properties.
	The L{lastIndex} attribute should also be provided.
	@ivar supportedSettings: The settings supported by the synthesiser.
	@type supportedSettings: list or tuple of L{SynthSetting}
	@ivar voice: Unique string identifying the current voice.
	@type voice: str
	@ivar availableVoices: The available voices.
	@type availableVoices: OrderedDict of L{VoiceInfo} keyed by VoiceInfo's ID
	@ivar pitch: The current pitch; ranges between 0 and 100.
	@type pitch: int
	@ivar rate: The current rate; ranges between 0 and 100.
	@type rate: int
	@ivar volume: The current volume; ranges between 0 and 100.
	@type volume: int
	@ivar variant: The current variant of the voice.
	@type variant: str
	@ivar availableVariants: The available variants of the voice.
	@type availableVariants: OrderedDict of [L{VoiceInfo} keyed by VoiceInfo's ID
	@ivar inflection: The current inflection; ranges between 0 and 100.
	@type inflection: int
	@ivar lastIndex: The index of the chunk of text which was last spoken or C{None} if no index.
	@type lastIndex: int
	"""

	#: The name of the synth; must be the original module file name.
	#: @type: str
	name = ""
	#: A description of the synth.
	#: @type: str
	description = ""

	@classmethod
	def LanguageSetting(cls):
		"""Factory function for creating a language setting."""
		# Translators: Label for a setting in voice settings dialog.
		return SynthSetting("language",_("&Language"),
		# Translators: Label for a setting in synth settings ring.
		displayName=pgettext('synth setting','Language'))

	@classmethod
	def VoiceSetting(cls):
		"""Factory function for creating voice setting."""
		# Translators: Label for a setting in voice settings dialog.
		return SynthSetting("voice",_("&Voice"),
		# Translators: Label for a setting in synth settings ring.
		displayName=pgettext('synth setting','Voice'))
	@classmethod
	def VariantSetting(cls):
		"""Factory function for creating variant setting."""
		# Translators: Label for a setting in voice settings dialog.
		return SynthSetting("variant",_("V&ariant"),
		# Translators: Label for a setting in synth settings ring.
		displayName=pgettext('synth setting','Variant'))

	@classmethod
	def RateSetting(cls,minStep=1):
		"""Factory function for creating rate setting."""
		# Translators: Label for a setting in voice settings dialog.
		return NumericSynthSetting("rate",_("&Rate"),minStep=minStep,
		# Translators: Label for a setting in synth settings ring.
		displayName=pgettext('synth setting','Rate'))
	@classmethod
	def VolumeSetting(cls,minStep=1):
		"""Factory function for creating volume setting."""
		# Translators: Label for a setting in voice settings dialog.
		return NumericSynthSetting("volume",_("V&olume"),minStep=minStep,normalStep=10,
		# Translators: Label for a setting in synth settings ring.
		displayName=pgettext('synth setting','Volume'))
	@classmethod
	def PitchSetting(cls,minStep=1):
		"""Factory function for creating pitch setting."""
		# Translators: Label for a setting in voice settings dialog.
		return NumericSynthSetting("pitch",_("&Pitch"),minStep=minStep,
		# Translators: Label for a setting in synth settings ring.
		displayName=pgettext('synth setting','Pitch'))

	@classmethod
	def InflectionSetting(cls,minStep=1):
		"""Factory function for creating inflection setting."""
		# Translators: Label for a setting in voice settings dialog.
		return NumericSynthSetting("inflection",_("&Inflection"),minStep=minStep,
# Translators: Label for a setting in synth settings ring.
		displayName=pgettext('synth setting','Inflection'))

	@classmethod
	def check(cls):
		"""Determine whether this synth is available.
		The synth will be excluded from the list of available synths if this method returns C{False}.
		For example, if this synth requires installation and it is not installed, C{False} should be returned.
		@return: C{True} if this synth is available, C{False} if not.
		@rtype: bool
		"""
		return False

	def __init__(self):
		"""Initialize this synth driver.
		This method can also set default settings for the synthesizer.
		@raise Exception: If an error occurs.
		@postcondition: This driver can be used.
		"""

	def terminate(self):
		"""Terminate this synth driver.
		This should be used for any required clean up.
		@precondition: L{initialize} has been called.
		@postcondition: This driver can no longer be used.
		"""

	def speak(self,speechSequence):
		"""
		Speaks the given sequence of text and speech commands.
		This base implementation will fallback to making use of the old speakText and speakCharacter methods. But new synths should override this method to support its full functionality.
		@param speechSequence: a list of text strings and SpeechCommand objects (such as index and parameter changes).
		@type speechSequence: list of string and L{speechCommand}
		"""
		import speech
		lastIndex=None
		text=""
		origSpeakFunc=self.speakText
		speechSequence=iter(speechSequence)
		while True:
			item = next(speechSequence,None)
			if text and (item is None or isinstance(item,(speech.IndexCommand,speech.CharacterModeCommand))):
				# Either we're about to handle a command or this is the end of the sequence.
				# Speak the text since the last command we handled.
				origSpeakFunc(text,index=lastIndex)
				text=""
				lastIndex=None
			if item is None:
				# No more items.
				break
			if isinstance(item,basestring):
				# Merge the text between commands into a single chunk.
				text+=item
			elif isinstance(item,speech.IndexCommand):
				lastIndex=item.index
			elif isinstance(item,speech.CharacterModeCommand):
				origSpeakFunc=self.speakCharacter if item.state else self.speakText
			elif isinstance(item,speech.SpeechCommand):
				log.debugWarning("Unknown speech command: %s"%item)
			else:
				log.error("Unknown item in speech sequence: %s"%item)

	def speakText(self, text, index=None):
		"""Speak some text.
		This method is deprecated. Instead implement speak.
		@param text: The chunk of text to speak.
		@type text: str
		@param index: An index (bookmark) to associate with this chunk of text, C{None} if no index.
		@type index: int
		@note: If C{index} is provided, the C{lastIndex} property should return this index when the synth is speaking this chunk of text.
		"""
		raise NotImplementedError

	def speakCharacter(self, character, index=None):
		"""Speak some character.
		This method is deprecated. Instead implement speak.
		@param character: The character to speak.
		@type character: str
		@param index: An index (bookmark) to associate with this chunk of speech, C{None} if no index.
		@type index: int
		@note: If C{index} is provided, the C{lastIndex} property should return this index when the synth is speaking this chunk of text.
		"""
		self.speakText(character,index)

	def _get_lastIndex(self):
		"""Obtain the index of the chunk of text which was last spoken.
		When the synth speaks text associated with a particular index, this method should return that index.
		That is, this property should update for each chunk of text spoken by the synth.
		@return: The index or C{None} if no index.
		@rtype: int
		"""
		return None

	def cancel(self):
		"""Silence speech immediately.
		"""

	def _get_language(self):
		return self.availableVoices[self.voice].language

	def _set_language(self,language):
		raise NotImplementedError

	def _get_availableLanguages(self):
		raise NotImplementedError

	def _get_voice(self):
		raise NotImplementedError

	def _set_voice(self, value):
		pass

	def _getAvailableVoices(self):
		"""fetches an ordered dictionary of voices that the synth supports.
		@returns: an OrderedDict of L{VoiceInfo} instances representing the available voices, keyed by ID
		@rtype: OrderedDict
		"""
		raise NotImplementedError

	def _get_availableVoices(self):
		if not hasattr(self,'_availableVoices'):
			self._availableVoices=self._getAvailableVoices()
		return self._availableVoices

	def _get_rate(self):
		return 0

	def _set_rate(self, value):
		pass

	def _get_pitch(self):
		return 0

	def _set_pitch(self, value):
		pass

	def _get_volume(self):
		return 0

	def _set_volume(self, value):
		pass

	def _get_variant(self):
		raise NotImplementedError

	def _set_variant(self, value):
		pass

	def _getAvailableVariants(self):
		"""fetches an ordered dictionary of variants that the synth supports, keyed by ID
		@returns: an ordered dictionary of L{VoiceInfo} instances representing the available variants
		@rtype: OrderedDict
		"""
		raise NotImplementedError
 
	def _get_availableVariants(self):
		if not hasattr(self,'_availableVariants'):
			self._availableVariants=self._getAvailableVariants()
		return self._availableVariants

	def _get_supportedSettings(self):
		raise NotImplementedError

	def getConfigSpec(self):
		spec=deepcopy(config.confspec["speech"]["__many__"])
		for setting in self.supportedSettings:
			spec[setting.name]=setting.configSpec
		return spec

	def _get_inflection(self):
		return 0

	def _set_inflection(self, value):
		pass

	def pause(self, switch):
		"""Pause or resume speech output.
		@param switch: C{True} to pause, C{False} to resume (unpause).
		@type switch: bool
		"""
		pass

	@classmethod
	def _paramToPercent(cls, current, min, max):
		"""Convert a raw parameter value to a percentage given the current, minimum and maximum raw values.
		@param current: The current value.
		@type current: int
		@param min: The minimum value.
		@type current: int
		@param max: The maximum value.
		@type max: int
		"""
		return int(round(float(current - min) / (max - min) * 100))

	@classmethod
	def _percentToParam(cls, percent, min, max):
		"""Convert a percentage to a raw parameter value given the current percentage and the minimum and maximum raw parameter values.
		@param percent: The current percentage.
		@type percent: int
		@param min: The minimum raw parameter value.
		@type min: int
		@param max: The maximum raw parameter value.
		@type max: int
		"""
		return int(round(float(percent) / 100 * (max - min) + min))

	def isSupported(self,settingName):
		"""Checks whether given setting is supported by the synthesizer.
		@rtype: l{bool}
		"""
		for s in self.supportedSettings:
			if s.name==settingName: return True
		return False

	def saveSettings(self):
		conf=config.conf["speech"][self.name]
		for setting in self.supportedSettings:
			conf[setting.name]=getattr(self,setting.name)

	def loadSettings(self, onlyChanged=False):
		c=config.conf["speech"][self.name]
		if self.isSupported("voice"):
			voice=c.get("voice",None)
			if not onlyChanged or self.voice!=voice:
				try:
					changeVoice(self,voice)
				except:
					log.warning("Invalid voice: %s" % voice)
					# Update the configuration with the correct voice.
					c["voice"]=self.voice
					# We need to call changeVoice here so that required initialisation can be performed.
					changeVoice(self,self.voice)
		elif not onlyChanged:
			changeVoice(self,None)
		for s in self.supportedSettings:
			if s.name=="voice" or c[s.name] is None:
				continue
			val=c[s.name]
			if onlyChanged and getattr(self,s.name)==val:
				continue
			setattr(self,s.name,val)

	def _get_initialSettingsRingSetting (self):
		if not self.isSupported("rate") and len(self.supportedSettings)>0:
			#Choose first as an initial one
			for i,s in enumerate(self.supportedSettings): 
				if s.availableInSynthSettingsRing: return i
			return None
		for i,s in enumerate(self.supportedSettings):
			if s.name=="rate": return i
		return None

class StringParameterInfo(object):
	"""
	The base class used to represent a value of a string synth setting.
	"""

	def __init__(self,ID,name):
		#: The unique identifier of the value.
		#: @type: str
		self.ID=ID
		#: The name of the value, visible to the user.
		#: @type: str
		self.name=name

class VoiceInfo(StringParameterInfo):
	"""Provides information about a single synthesizer voice.
	"""

	def __init__(self,ID,name,language=None):
		#: The ID of the language this voice speaks, or None if not known or the synth implements language separate from voices
		self.language=language
		super(VoiceInfo,self).__init__(ID,name)

class LanguageInfo(StringParameterInfo):
	"""Holds information for a particular language"""

	def __init__(self,ID):
		"""Given a language ID (locale name) the description is automatically calculated."""
		name=languageHandler.getLanguageDescription(ID)
		super(LanguageInfo,self).__init__(ID,name)

