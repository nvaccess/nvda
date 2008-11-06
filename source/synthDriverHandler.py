#synthDrivers/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import config
import baseObject
import globalVars
from logHandler import log
from  synthSettingsRing import SynthSettingsRing
import speechDictHandler

#This is here so that the synthDrivers are able to import modules from the synthDrivers dir themselves
__path__=['.\\synthDrivers']

_curSynth=None

def changeVoice(synth, voice):
	voiceName=voice.replace('\\','_')
	fileName="%s/%s-%s.dic"%(speechDictHandler.speechDictsPath,synth.name,voiceName)
	speechDictHandler.dictionaries["voice"].load(fileName)
	synth.voice = voice

def getSynthList():
	synthList=[]
	for name in [os.path.splitext(x)[0] for x in os.listdir(__path__[0]) if (x.endswith('.py') and not x.startswith('_'))]:
		try:
			synth=__import__(name,globals(),locals(),[]).SynthDriver
			if synth.check():
				synthList.append((synth.name,synth.description))
		except:
			pass
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
	try:
		newSynth=__import__(name,globals(),None,[]).SynthDriver()
		if _curSynth and _curSynth.name == newSynth.name:
			_curSynth.cancel()
			_curSynth.terminate()
			_curSynth = None
		newSynth.initialize()
		updatedConfig=config.updateSynthConfig(name)
		if not updatedConfig:
			if newSynth.hasVoice:
				changeVoice(newSynth,config.conf["speech"][name]["voice"])
			if newSynth.hasVariant:
				newSynth.variant=config.conf["speech"][name]["variant"]
			if newSynth.hasRate:
				newSynth.rate=config.conf["speech"][name]["rate"]
			if newSynth.hasPitch:
				newSynth.pitch=config.conf["speech"][name]["pitch"]
			if newSynth.hasInflection:
				newSynth.inflection=config.conf["speech"][name]["inflection"]
			if newSynth.hasVolume:
				newSynth.volume=config.conf["speech"][name]["volume"]
		else:
			if newSynth.hasVoice:
				config.conf["speech"][name]["voice"]=newSynth.voice
				#We need to call changeVoice here so voice dictionries can be managed
				changeVoice(newSynth,newSynth.voice)
			if newSynth.hasVariant:
				config.conf["speech"][name]["variant"]=newSynth.variant
			if newSynth.hasRate:
				config.conf["speech"][name]["rate"]=newSynth.rate
			if newSynth.hasPitch:
				config.conf["speech"][name]["pitch"]=newSynth.pitch
			if newSynth.hasInflection:
				config.conf["speech"][name]["inflection"]=newSynth.inflection
			if newSynth.hasVolume:
				config.conf["speech"][name]["volume"]=newSynth.volume
		if _curSynth:
			_curSynth.cancel()
			_curSynth.terminate()
		_curSynth=newSynth
		config.conf["speech"]["synth"]=name
		log.info("Loaded synthDriver %s"%name)
		#start or update the synthSettingsRing
		if globalVars.settingsRing: globalVars.settingsRing.updateSupportedSettings()
		else:  globalVars.settingsRing = SynthSettingsRing()
		return True
	except:
		log.error("setSynth", exc_info=True)
		if not _curSynth and name not in ['espeak','silence']:
			setSynth('espeak')
		elif not _curSynth and name=='espeak':
			setSynth('silence')
		return False

class SynthDriver(baseObject.AutoPropertyObject):
	"""Abstract base synthesizer driver.
	Each synthesizer driver should be a separate Python module in the root synthDrivers directory containing a SynthDriver class which inherits from this base class.
	
	At a minimum, synth drivers must set L{name} and L{description} and override the L{check} method.
	The bool variables L{hasVoice}, L{hasPitch}, etc. should be set where appropriate. These indicate which voice settings are supported.
	The MinStep values (L{pitchMinStep}, L{rateMinStep}, etc.) specify the minimum step between valid values for each numeric setting.
	For example, if L{pitchMinStep} is set to 10, L{pitch} can only be multiples of 10; 10, 20, 30, etc.
	The properties for each setting (e.g. L{voice} and L{pitch}) are created by overriding getters and setters;
	for example, L{_get_pitch} and L{_set_pitch} for L{pitch}.
	The methods L{speakText}, L{cancel} and L{pause} should be overridden as appropriate.
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
	@ivar availableVariants: a dictionary of available variants, keyed by variant identifier, values are the full variant name. 
	@type availableVariants: dict of strings
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

	hasVoice = False
	hasPitch = False
	pitchMinStep = 1
	hasRate = False
	rateMinStep = 1
	hasVolume = False
	volumeMinStep = 1
	hasVariant = False
	hasInflection = False
	inflectionMinStep = 1

	@classmethod
	def check(cls):
		"""Determine whether this synth is available.
		The synth will be excluded from the list of available synths if this method returns C{False}.
		For example, if this synth requires installation and it is not installed, C{False} should be returned.
		@return: C{True} if this synth is available, C{False} if not.
		@rtype: bool
		"""
		return False

	def initialize(self):
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

	def _get_availableVoices(self):
		return[]

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

	def _get_availableVariants(self):
		return {}

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
