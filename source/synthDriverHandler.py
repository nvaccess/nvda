#synthDrivers/__init__.py
#$Rev$
#$Date$
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import debug
import config

#This is here so that the synthDrivers are able to import modules from the synthDrivers dir themselves
__path__=['.\\synthDrivers']

autoTrySynthList=["sapi5","sapi4","viavoice"]
driverObject=None
driverName=None
driverVoiceNames=[]

def getDriverList():
	l=os.listdir(__path__[0])
	l=filter(lambda x: x.endswith(".py") or x.endswith(".pyc") or x.endswith(".pyo") or (os.path.isdir(os.path.join(__path__[0],x)) and not x.startswith(".")),l)
	l=map(lambda x: os.path.splitext(x)[0],l)
	l=list(set(l))
	l=filter(lambda x: isDriverAvailable(x),l)
	return l

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
