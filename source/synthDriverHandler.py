#synthDrivers/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import config
import queueHandler
import speech
import globalVars
from  _synthSettingsRing import SynthSettingsRing
import speechDictHandler

#This is here so that the synthDrivers are able to import modules from the synthDrivers dir themselves
__path__=['.\\synthDrivers']

_curSynth=None

def changeVoice(synth, voice):
	voiceName=synth.getVoiceName(voice).replace('\\','_')
	fileName="%s/%s-%s.dic"%(speechDictHandler.speechDictsPath,synth.name,voiceName)
	speechDictHandler.dictionaries["voice"].load(fileName)
	synth.voice = voice

def getSynthList():
	synthList=[]
	for name in [os.path.splitext(x)[0] for x in os.listdir(__path__[0]) if (x.endswith('.py') and not x.startswith('_'))]:
		try:
			synth=__import__(name,globals(),locals(),[]).SynthDriver()
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
		globalVars.log.info("Loaded synthDriver %s"%name)
		#start or update the synthSettingsRing
		if globalVars.settingsRing: globalVars.settingsRing.updateSupportedSettings()
		else:  globalVars.settingsRing = SynthSettingsRing()
		return True
	except:
		globalVars.log.error("setSynth", exc_info=True)
		if not _curSynth and name not in ['espeak','silence']:
			setSynth('espeak')
		elif not _curSynth and name=='espeak':
			setSynth('silence')
		return False
