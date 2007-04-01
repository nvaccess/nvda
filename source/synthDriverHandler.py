#synthDrivers/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import debug
import config

#This is here so that the synthDrivers are able to import modules from the synthDrivers dir themselves
__path__=['.\\synthDrivers']

autoTrySynthList=["sapi5"]
driverObject=None
driverName=None
driverVoiceNames=[]

def getDriverList():
	driverList=[]
	for name in [os.path.splitext(x)[0] for x in os.listdir(__path__[0]) if (x.endswith('.py') and not x.startswith('_'))]:
		try:
			mod=__import__(name,globals(),locals(),[])
			if mod.check():
				driverList.append((name,mod.description))
		except:
			pass
	return driverList

def isDriverAvailable(name):
	try:
		mod=__import__(name,globals(),None,[])
		if mod.check():
			return True
		else:
			return False
	except:
		return False

def getDriverDescription(name):
	try:
		mod=__import__(name,globals(),None,[])
		return mod.description
	except:
		return ""

def setDriver(name):
	global driverObject, driverName, driverVoiceNames
	if name=="auto":
		for synth in autoTrySynthList:
			if isDriverAvailable(synth):
				setDriver(synth)
				config.conf["speech"]["synth"]="auto"
				return True
		raise OSError("Cannot find a synthesizer")
	try:
		newSynth=__import__(name,globals(),None,[]).synthDriver()
		config.updateSynthConfig(name)
		debug.writeMessage("synth config: %s"%config.conf["speech"][name])
		newSynth.voice=config.conf["speech"][name]["voice"]
		newSynth.rate=config.conf["speech"][name]["rate"]
		newSynth.pitch=config.conf["speech"][name]["pitch"]
		newSynth.volume=config.conf["speech"][name]["volume"]
		driverObject=newSynth
		driverName=name
		driverVoiceNames=driverObject.voiceNames
		config.conf["speech"]["synth"]=name
		debug.writeMessage("Loaded synthDriver %s"%name)
		return True
	except:
		debug.writeException("Error in synthDriver %s"%name)
		return False

def getRate():
	try:
		value=driverObject.rate
		if value<0:
			value=0
		if value>100:
			value=100
	except:
		value=50
	return value

def setRate(value):
	try:
		if value<0:
			value=0
		if value>100:
			value=100
		driverObject.rate=value
		config.conf["speech"][driverName]["rate"]=getRate()
	except:
		pass

def getPitch():
	try:
		value=driverObject.pitch
		if value<0:
			value=0
		if value>100:
			value=100
	except:
		value=0
	return value

def setPitch(value):
	try:
		if value<0:
			value=0
		if value>100:
			value=100
		driverObject.pitch=value
		config.conf["speech"][driverName]["pitch"]=getPitch()
	except:
		pass

def getVolume():
	try:
		value=driverObject.volume
		if value<0:
			value=0
		if value>100:
			value=100
	except:
		value=0
	return value

def setVolume(value):
	try:
		if value<0:
			value=0
		if value>100:
			value=100
		driverObject.volume=value
		config.conf["speech"][driverName]["volume"]=getVolume()
	except:
		pass

def getVoice():
	try:
		return driverObject.voice
	except:
		return 1

def setVoice(value):
	try:
		driverObject.voice=value
		config.conf["speech"][driverName]["voice"]=getVoice()
		driverObject.rate=config.conf["speech"][driverName]["rate"]
	except:
		debug.writeException("setVoice")
		pass

def getVoiceNames():
	try:
		return driverVoiceNames
	except:
		return []

def speakText(text,wait=False,index=None):
	try:
		driverObject.speakText(text,wait=wait,index=index)
	except:
		pass

def cancel():
	try:
		driverObject.cancel()
	except:
		pass

def getLastIndex():
	try:
		index=driverObject.lastIndex
		if index is not None:
			return index
	except:
		return None
