# -*- coding: UTF-8 -*-
#synthDriverHandler.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2019 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Joseph Lee, Arnold Loubriat, Leonard de Ruijter

import os
import pkgutil
import importlib
import config
import baseObject
import winVersion
import globalVars
from logHandler import log
from  synthSettingsRing import SynthSettingsRing
import languageHandler
import speechDictHandler
import extensionPoints
import synthDrivers
import driverHandler
from driverHandler import StringParameterInfo # Backwards compatibility
from abc import abstractmethod

_curSynth=None
_audioOutputDevice=None

def initialize():
	config.addConfigDirsToPythonPackagePath(synthDrivers)
	config.post_configProfileSwitch.register(handlePostConfigProfileSwitch)

def changeVoice(synth, voice):
	# This function can be called with no voice if the synth doesn't support the voice setting (only has one voice).
	if voice:
		synth.voice = voice
	c=config.conf["speech"][synth.name]
	#start or update the synthSettingsRing
	if globalVars.settingsRing: globalVars.settingsRing.updateSupportedSettings(synth)
	else:  globalVars.settingsRing = SynthSettingsRing(synth)
	speechDictHandler.loadVoiceDict(synth)

def _getSynthDriver(name):
	return importlib.import_module("synthDrivers.%s" % name, package="synthDrivers").SynthDriver

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

def getSynthInstance(name):
	newSynth = _getSynthDriver(name)()
	newSynth.initSettings()
	return newSynth

# The synthDrivers that should be used by default.
# The first that successfully initializes will be used when config is set to auto (I.e. new installs of NVDA).
defaultSynthPriorityList=['espeak','silence']
if winVersion.winVersion.major>=10:
	# Default to OneCore on Windows 10 and above
	defaultSynthPriorityList.insert(0,'oneCore')

def setSynth(name,isFallback=False):
	global _curSynth,_audioOutputDevice
	if name is None: 
		_curSynth.terminate()
		_curSynth=None
		return True
	if name=='auto':
		name=defaultSynthPriorityList[0]
	if _curSynth:
		_curSynth.cancel()
		_curSynth.terminate()
		prevSynthName = _curSynth.name
		_curSynth = None
	else:
		prevSynthName = None
	try:
		_curSynth=getSynthInstance(name)
		_audioOutputDevice=config.conf["speech"]["outputDevice"]
		if not isFallback:
			config.conf["speech"]["synth"]=name
		log.info("Loaded synthDriver %s"%name)
		return True
	except:
		log.error("setSynth", exc_info=True)
		# As there was an error loading this synth:
		if prevSynthName:
			# There was a previous synthesizer, so switch back to that one. 
			setSynth(prevSynthName,isFallback=True)
		else:
			# There was no previous synth, so fallback to the next available default synthesizer that has not been tried yet.
			try:
				nextIndex=defaultSynthPriorityList.index(name)+1
			except ValueError:
				nextIndex=0
			if nextIndex<len(defaultSynthPriorityList):
				newName=defaultSynthPriorityList[nextIndex]
				setSynth(newName,isFallback=True)
		return False

def handlePostConfigProfileSwitch(resetSpeechIfNeeded=True):
	"""
	Switches synthesizers and or applies new voice settings to the synth due to a config profile switch.
	@var resetSpeechIfNeeded: if true and a new synth will be loaded, speech queues are fully reset first. This is what happens by default. 
	However, Speech itself may call this with false internally if this is a config profile switch within a currently processing speech sequence. 
	@type resetSpeechIfNeeded: bool
	"""
	conf = config.conf["speech"]
	if conf["synth"] != _curSynth.name or conf["outputDevice"] != _audioOutputDevice:
		if resetSpeechIfNeeded:
			# Reset the speech queues as we are now going to be using a new synthesizer with entirely separate state.
			import speech
			speech.cancelSpeech()
		setSynth(conf["synth"])
		return
	_curSynth.loadSettings(onlyChanged=True)

class SynthDriver(driverHandler.Driver):
	"""Abstract base synthesizer driver.
	Each synthesizer driver should be a separate Python module in the root synthDrivers directory containing a SynthDriver class which inherits from this base class.
	
	At a minimum, synth drivers must set L{name} and L{description} and override the L{check} method.
	The methods L{speak}, L{cancel} and L{pause} should be overridden as appropriate.
	L{supportedSettings} should be set as appropriate for the settings supported by the synthesiser.
	There are factory functions to create L{driverHandler.DriverSetting} instances for common settings; e.g. L{VoiceSetting} and L{RateSetting}.
	Each setting is retrieved and set using attributes named after the setting;
	e.g. the L{voice} attribute is used for the L{voice} setting.
	These will usually be properties.
	L{supportedCommands} should specify what synth commands the synthesizer supports.
	At a minimum, L{speech.IndexCommand} must be supported.
	L{PitchCommand} must also be supported if you want capital pitch change to work;
	support for the pitch setting is not sufficient.
	L{supportedNotifications} should specify what notifications the synthesizer provides.
	Currently, the available notifications are L{synthIndexReached} and L{synthDoneSpeaking}.
	Both of these must be supported.
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
	"""

	#: The name of the synth; must be the original module file name.
	#: @type: str
	name = ""
	#: A description of the synth.
	#: @type: str
	description = ""
	#: The speech commands supported by the synth.
	#: @type: set of L{speech.SynthCommand} subclasses.
	supportedCommands = frozenset()
	#: The notifications provided by the synth.
	#: @type: set of L{extensionPoints.Action} instances
	supportedNotifications = frozenset()
	_configSection = "speech"

	@classmethod
	def LanguageSetting(cls):
		"""Factory function for creating a language setting."""
		# Translators: Label for a setting in voice settings dialog.
		return driverHandler.DriverSetting("language",_("&Language"),availableInSettingsRing=True,
		# Translators: Label for a setting in synth settings ring.
		displayName=pgettext('synth setting','Language'))

	@classmethod
	def VoiceSetting(cls):
		"""Factory function for creating voice setting."""
		# Translators: Label for a setting in voice settings dialog.
		return driverHandler.DriverSetting("voice",_("&Voice"),availableInSettingsRing=True,
		# Translators: Label for a setting in synth settings ring.
		displayName=pgettext('synth setting','Voice'))
	@classmethod
	def VariantSetting(cls):
		"""Factory function for creating variant setting."""
		# Translators: Label for a setting in voice settings dialog.
		return driverHandler.DriverSetting("variant",_("V&ariant"),availableInSettingsRing=True,
		# Translators: Label for a setting in synth settings ring.
		displayName=pgettext('synth setting','Variant'))

	@classmethod
	def RateSetting(cls,minStep=1):
		"""Factory function for creating rate setting."""
		# Translators: Label for a setting in voice settings dialog.
		return driverHandler.NumericDriverSetting("rate",_("&Rate"),minStep=minStep,availableInSettingsRing=True,
		# Translators: Label for a setting in synth settings ring.
		displayName=pgettext('synth setting','Rate'))
	@classmethod
	def RateBoostSetting(cls):
		"""Factory function for creating rate boost setting."""
		# Translators: This is the name of the rate boost voice toggle
		# which further increases the speaking rate when enabled.
		return driverHandler.BooleanDriverSetting("rateBoost",_("Rate boos&t"),
		# Translators: Label for a setting in synth settings ring.
		displayName=pgettext('synth setting','Rate boost'),
		availableInSettingsRing=True)
	@classmethod
	def VolumeSetting(cls,minStep=1):
		"""Factory function for creating volume setting."""
		# Translators: Label for a setting in voice settings dialog.
		return driverHandler.NumericDriverSetting("volume",_("V&olume"),minStep=minStep,normalStep=5,availableInSettingsRing=True,

		# Translators: Label for a setting in synth settings ring.
		displayName=pgettext('synth setting','Volume'))
	@classmethod
	def PitchSetting(cls,minStep=1):
		"""Factory function for creating pitch setting."""
		# Translators: Label for a setting in voice settings dialog.
		return driverHandler.NumericDriverSetting("pitch",_("&Pitch"),minStep=minStep,availableInSettingsRing=True,
		# Translators: Label for a setting in synth settings ring.
		displayName=pgettext('synth setting','Pitch'))

	@classmethod
	def InflectionSetting(cls,minStep=1):
		"""Factory function for creating inflection setting."""
		# Translators: Label for a setting in voice settings dialog.
		return driverHandler.NumericDriverSetting("inflection",_("&Inflection"),minStep=minStep,availableInSettingsRing=True,
		# Translators: Label for a setting in synth settings ring.
		displayName=pgettext('synth setting','Inflection'))

	@abstractmethod
	def speak(self, speechSequence):
		"""
		Speaks the given sequence of text and speech commands.
		@param speechSequence: a list of text strings and SynthCommand objects (such as index and parameter changes).
		@type speechSequence: list of string and L{SynthCommand}
		"""
		raise NotImplementedError

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

	def initSettings(self):
		firstLoad = not config.conf[self._configSection].isSet(self.name)
		if firstLoad:
			# Create the new section.
			config.conf[self._configSection][self.name] = {}
		# Make sure the config spec is up to date, so the config validator does its work.
		config.conf[self._configSection][self.name].spec.update(self.getConfigSpec())
		# Make sure the instance has attributes for every setting
		for setting in self.supportedSettings:
			if not hasattr(self, setting.id):
				setattr(self, setting.id, setting.defaultVal)
		if firstLoad:
			if self.isSupported("voice"):
				voice=self.voice
			else:
				voice=None
			# We need to call changeVoice here so that required initialisation can be performed.
			changeVoice(self,voice)
			self.saveSettings() #save defaults
		else:
			self.loadSettings()

	def loadSettings(self, onlyChanged=False):
		# Method override due to specific logic needed when changing a voice.
		c=config.conf[self._configSection][self.name]
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
			if s.id == "voice" or c[s.id] is None:
				continue
			val=c[s.id]
			if onlyChanged and getattr(self,s.id)==val:
				continue
			setattr(self,s.id, val)
		log.debug(
			(
				"Loaded changed settings for SynthDriver {}"
				if onlyChanged else
				"Loaded settings for SynthDriver {}"
			).format(self.name))

	def _get_initialSettingsRingSetting (self):
		supportedSettings = list(self.supportedSettings)
		if not self.isSupported("rate") and len(supportedSettings) > 0:
			#Choose first as an initial one
			for i, s in enumerate(supportedSettings):
				if s.availableInSettingsRing: return i
			return None
		for i, s in enumerate(supportedSettings):
			if s.id == "rate": return i
		return None

class VoiceInfo(driverHandler.StringParameterInfo):
	"""Provides information about a single synthesizer voice.
	"""

	def __init__(self, id, displayName, language=None):
		"""
		@param language: The ID of the language this voice speaks,
			C{None} if not known or the synth implements language separate from voices.
		@type language: str
		"""
		self.language=language
		super(VoiceInfo,self).__init__(id, displayName)

class LanguageInfo(driverHandler.StringParameterInfo):
	"""Holds information for a particular language"""

	def __init__(self, id):
		"""Given a language ID (locale name) the description is automatically calculated."""
		displayName = languageHandler.getLanguageDescription(id)
		super(LanguageInfo,self).__init__(id, displayName)

#: Notifies when a synthesizer reaches an index during speech.
#: Handlers are called with these keyword arguments:
#: synth: The L{SynthDriver} which reached the index.
#: index: The number of the index which has just been reached.
synthIndexReached = extensionPoints.Action()
#: Notifies when a synthesizer finishes speaking.
#: Handlers are called with one keyword argument:
#: synth: The L{SynthDriver} which reached the index.
synthDoneSpeaking = extensionPoints.Action()
