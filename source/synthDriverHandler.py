#synthDrivers/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import debug
from config import conf, getSynthConfig

#This is here so that the synthDrivers are able to import modules from the synthDrivers dir themselves
__path__=['.\\synthDrivers']

current=None

def getSynthDriverList():
	l=os.listdir(__path__[0])
	l=filter((lambda x: x.endswith(".py") or x.endswith(".pyc") or x.endswith(".pyo") or (os.path.isdir(os.path.join(__path__[0],x)) and not x.startswith("."))),l)
	l=map((lambda x: os.path.splitext(x)[0]),l)
	l=set(l)
	l=list(l)
	return l

def getCurrentSynthDriver():
	return current

def load(name):
	global current
	try:
		newSynth=__import__(name,globals(),None,[]).synthDriver()
		newSynth.setVoice(conf["speech"][name]["voice"])
		newSynth.setRate(conf["speech"][name]["rate"])
		newSynth.setVolume(conf["speech"][name]["volume"])
		current=newSynth
		debug.writeMessage("Loaded synthDriver %s"%name)
		return True
	except:
		debug.writeException("Error in synthDriver %s"%name)
		return False
