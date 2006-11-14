#synthDrivers/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import debug
from config import conf, checkSynth

#This is here so that the synthDrivers are able to import modules from the synthDrivers dir themselves
__path__=['.\\synthDrivers']

autoTrySynthList=["sapi5","sapi4","viavoice"]
driverObject=None
driverName=None
driverVoiceNames=[]

def getDriverList():
	l=os.listdir(__path__[0])
	l=filter((lambda x: x.endswith(".py") or x.endswith(".pyc") or x.endswith(".pyo") or (os.path.isdir(os.path.join(__path__[0],x)) and not x.startswith("."))),l)
	l=map((lambda x: os.path.splitext(x)[0]),l)
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
				conf["speech"]["synth"]="auto"
				return True
		else: #none of the auto synths are available
			raise OSError("Cannot find a synthesizer")
	try:
		newSynth=__import__(name,globals(),None,[]).synthDriver()
		checkSynth(name)
		newSynth.setVoice(conf["speech"][name]["voice"])
		newSynth.setRate(conf["speech"][name]["rate"])
		newSynth.setVolume(conf["speech"][name]["volume"])
		driverObject=newSynth
		driverName=name
		driverVoiceNames=driverObject.getVoiceNames()
		conf["speech"]["synth"]=name
		debug.writeMessage("Loaded synthDriver %s"%name)
		return True
	except:
		setDriver("auto")
		debug.writeException("Error in synthDriver %s"%name)
		return False

def getRate():
	value=driverObject.getRate()
	if value<0:
		value=0
	if value>100:
		value=100
	return value

def setRate(value):
	if value<0:
		value=0
	if value>100:
		value=100
	driverObject.setRate(value)
	conf["speech"][driverName]["rate"]=getRate()

def getPitch():
	value=driverObject.getPitch()
	if value<0:
		value=0
	if value>100:
		value=100
	return value

def setPitch(value):
	if value<0:
		value=0
	if value>100:
		value=100
	driverObject.setPitch(value)
	conf["speech"][driverName]["pitch"]=getPitch()

def getVolume():
	value=driverObject.getVolume()
	if value<0:
		value=0
	if value>100:
		value=100
	return value

def setVolume(value):
	if value<0:
		value=0
	if value>100:
		value=100
	driverObject.setVolume(value)
	conf["speech"][driverName]["volume"]=getVolume()

def getVoice():
	return driverObject.getVoice()

def setVoice(value):
	driverObject.setVoice(value)
	conf["speech"][driverName]["voice"]=getVoice()
	driverObject.setRate(conf["speech"][driverName]["rate"])

def getVoiceNames():
	return driverVoiceNames

def speakText(text,wait=False,index=None):
	driverObject.speakText(text,wait=wait,index=index)

def cancel():
	driverObject.cancel()

def getLastIndex():
	index=driverObject.getLastIndex()
	if index is not None:
		debug.writeMessage("synthDriverHandler.getLastIndex: %s"%index)
		return index

def getSupportedLanguages():
	return driverObject.getSupportedLanguages()

def setLanguage(value):
	return driverObject.setLanguage(value)
 