#synthDrivers/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from copy import deepcopy
import os
import pkgutil
import config
import baseObject
import globalVars
from logHandler import log
from  synthSettingsRing import SynthSettingsRing
import speechDictHandler
import synthDrivers

_curSynth=None

def initialize():
	config.addConfigDirsToPythonPackagePath(synthDrivers)

def changeVoice(synth, voice):
	import api
	voiceName = synth.getVoiceInfoByID(voice).name
	synth.voice = voice
	fileName=r"%s\%s-%s.dic"%(speechDictHandler.speechDictsPath,synth.name,api.filterFileName(voiceName))
	speechDictHandler.dictionaries["voice"].load(fileName)
	c=config.conf["speech"][synth.name]
	c.configspec=synth.getConfigSpec()
	config.conf.validate(config.val, copy = True,section = c)
	#start or update the synthSettingsRing
	if globalVars.settingsRing: globalVars.settingsRing.updateSupportedSettings(synth)
	else:  globalVars.settingsRing = SynthSettingsRing(synth)

def _getSynthDriver(name):
	return __import__("synthDrivers.%s" % name, globals(), locals(), ("synthDrivers",)).SynthDriver

def getSynthList():
	synthList=[]
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
				synthList.append((synth.name,synth.description))
			else:
				log.debugWarning("Synthesizer %s doesn't pass the check, excluding from list"%name)
		except:
			log.error("",exc_info=True)
	return synthList

def getSynth():
	return _curSynth

def setSynth(name):
	global _curSynth
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
		updatedConfig=config.updateSynthConfig(newSynth)
		if not updatedConfig:
			newSynth.loadSettings()
		else:
			if newSynth.isSupported("voice"):
				#We need to call changeVoice here so voice dictionaries can be managed
				changeVoice(newSynth,newSynth.voice)
			newSynth.saveSettings() #save defaults
		_curSynth=newSynth
		config.conf["speech"]["synth"]=name
		log.info("Loaded synthDriver %s"%name)
		return True
	except:
		log.error("setSynth", exc_info=True)
		if prevSynthName:
			setSynth(prevSynthName)
		elif name not in ('espeak','silence'):
			setSynth('espeak')
		elif name=='espeak':
			setSynth('silence')
		return False

class SynthSetting(object):
	"""Represents a synthesizer setting such as voice or variant.
	@ivar configSpec: Configuration specification of this particular setting for config file validator.
	@type configSpec: L{str}
	"""
	configSpec="string(default=None)"

	def __init__(self,name,i18nName,availableInSynthSettingsRing=True):
		"""@param name: internal name of the setting
		@type name: L{str}
		@param i18nName: the localized string
		@type i18nName: L{str}
		@param availableInSynthSettingsRing: Will this option be available in synthesizer settings ring?
		@type availableInSynthSettingsRing: L{bool}
		"""
		self.name=name
		self.i18nName=i18nName
		self.availableInSynthSettingsRing=availableInSynthSettingsRing

class NumericSynthSetting(SynthSetting):
	"""Represents a numeric synthesizer setting such as rate, volume or pitch."""
	configSpec="integer(default=50,min=0,max=100)"

	def __init__(self,name,i18nName,availableInSynthSettingsRing=True,minStep=5):
		"""@param minStep: specifies the minimum step between valid values for each numeric setting. For example, if L{minStep} is set to 10, setting values can only be multiples of 10; 10, 20, 30, etc.
		@type minStep: L{int}
		"""
		super(NumericSynthSetting,self).__init__(name,i18nName,availableInSynthSettingsRing)
		self.minStep=minStep

class SynthDriver(baseObject.AutoPropertyObject):
	"""Abstract base synthesizer driver.
	Each synthesizer driver should be a separate Python module in the root synthDrivers directory containing a SynthDriver class which inherits from this base class.
	
	At a minimum, synth drivers must set L{name} and L{description} and override the L{check} method.
	The bool variables L{hasVoice}, L{hasPitch}, etc. should be set where appropriate. These indicate which voice settings are supported.
	The MinStep values (L{pitchMinStep}, L{rateMinStep}, etc.) specify the minimum step between valid values for each numeric setting.
	For example, if L{pitchMinStep} is set to 10, L{pitch} can only be multiples of 10; 10, 20, 30, etc.
	The properties for each setting (e.g. L{voice} and L{pitch}) are created by overriding getters and setters;
	for example, L{_get_pitch} and L{_set_pitch} for L{pitch}.
	The methods L{speakText}, L{speakCharacter}, L{cancel} and L{pause} should be overridden as appropriate. If L{speakCharacter} is not redefined in the synthDriver, speakText method will be called within a proxy function from base SynthDriver by default.
	@ivar voice: Unique string identifying the current voice.
	@type voice: str
	@ivar availableVoices: The available voices.
	@ivar availableVoices: [L{VoiceInfo}, ...]
	@ivar pitch: The current pitch; ranges between 0 and 100.
	@type pitch: int
	@ivar rate: The current rate; ranges between 0 and 100.
	@type rate: int
	@ivar volume: The current volume; ranges between 0 and 100.
	@type volume: int
	@ivar variant: The current variant of the voice.
	@type variant: str
	@ivar availableVariants: The available variants of the voice.
	@type availableVariants: [L{VoiceInfo}, ...]
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
	def VoiceSetting(cls):
		"""Factory function for creating voice setting."""
		return SynthSetting("voice",_("&Voice"))
	@classmethod
	def VariantSetting(cls):
		"""Factory function for creating variant setting."""
		return SynthSetting("variant",_("V&ariant"))

	@classmethod
	def RateSetting(cls,minStep=5):
		"""Factory function for creating rate setting."""
		return NumericSynthSetting("rate",_("&Rate"),minStep)
	@classmethod
	def VolumeSetting(cls,minStep=5):
		"""Factory function for creating volume setting."""
		return NumericSynthSetting("volume",_("V&olume"),minStep)
	@classmethod
	def PitchSetting(cls,minStep=5):
		"""Factory function for creating pitch setting."""
		return NumericSynthSetting("pitch",_("Pitch"),minStep)

	@classmethod
	def InflectionSetting(cls,minStep=5):
		"""Factory function for creating inflection setting."""
		return NumericSynthSetting("inflection",_("&Inflection"),minStep)

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

	def speakText(self, text, index=None):
		"""Speak some text.
		@param text: The chunk of text to speak.
		@type text: str
		@param index: An index (bookmark) to associate with this chunk of text, C{None} if no index.
		@type index: int
		@note: If C{index} is provided, the C{lastIndex} property should return this index when the synth is speaking this chunk of text.
		"""

	def speakCharacter(self, character, index=None):
		"""Speak some character.
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

	def _get_voice(self):
		raise NotImplementedError

	def _set_voice(self, value):
		pass

	def _getAvailableVoices(self):
		"""fetches a list of voices that the synth supports.
		@returns: a list of L{VoiceInfo} instances representing the available voices
		@rtype: list
		"""

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
		"""fetches a list of variants that the synth supports.
		@returns: a list of L{VoiceInfo} instances representing the available variants
		@rtype: list
		"""
 
	def _get_availableVariants(self):
		if not hasattr(self,'_availableVariants'):
			self._availableVariants=self._getAvailableVariants()
		return self._availableVariants

	def _get_supportedSettings(self):
		"""By default, this checks old-styled 'has_xxx' and constructs the list of settings.
		@returns: list of supported settings
		@rtype: l{tuple}
		"""
		result=[]
		settings=[("rate",self.RateSetting),("pitch",self.PitchSetting),("volume",self.VolumeSetting),("inflection",self.InflectionSetting),("variant",self.VariantSetting),("voice",self.VoiceSetting)]
		for name,setting in settings:
			if not getattr(self,"has%s"%name.capitalize(),False): continue
			if hasattr(self,"%sMinStep"%name):
				result.append(setting(getattr(self,"%sMinStep"%name)))
			else:
				result.append(setting())
		return tuple(result)

	def getConfigSpec(self):
		spec=deepcopy(config.synthSpec)
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

	def getVoiceInfoByID(self,ID):
		"""Looks up a L{VoiceInfo} instance representing a particular voice, by its ID.
		@param ID: the ID of the voice
		@type ID: string
		@returns: the voice info instance
		@rtype: L{VoiceInfo}
		@raise LookupError: If there was no such voice.
		"""
		for v in self.availableVoices:
			if v.ID==ID:
				return v
		raise LookupError("No such voice")

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

	def loadSettings(self):
		c=config.conf["speech"][self.name]
		if self.isSupported("voice"):
			voice=c["voice"]
			try:
				changeVoice(self,voice)
			except LookupError:
				log.warning("No such voice: %s" % voice)
				# Update the configuration with the correct voice.
				c["voice"]=self.voice
				# We need to call changeVoice here so voice dictionaries can be managed
				changeVoice(self,self.voice)
		[setattr(self,s.name,c[s.name]) for s in self.supportedSettings if not s.name=="voice" and c[s.name] is not None]

	def _get_initialSettingsRingSetting (self):
		if hasattr(self,"initialSettingsRingSetting "): return self.initialSettingsRingSetting 
		if not self.isSupported("rate") and len(self.supportedSettings)>0:
			#Choose first as an initial one
			for s in self.supportedSettings: 
				if s.availableInSynthSettingsRing: return s 
			return None
		for s in self.supportedSettings:
			if s.name=="rate": return s
		return None

class VoiceInfo(object):
	"""Provides information about a single synthesizer voice.
	"""

	def __init__(self,ID,name):
		#: The unique identifier of the voice.
		#: @type: str
		self.ID=ID
		#: The name of the voice, visible to the user.
		#: @type: str
		self.name=name
