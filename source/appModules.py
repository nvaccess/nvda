#appModules.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import imp
import os
import debug
import audio

current=None

def __fetchAppModule__(name):
	if os.path.isfile(os.getcwd()+"\\appModules\\"+name+".py"):
		(fp,path,desc)=imp.find_module(name,[os.getcwd()+"\\appModules"])
		try:
			module=imp.load_module(name,fp,path,desc)
			module.event_moduleStart()
			return module
		except:
			audio.speakMessage("Error loading app module %s"%name)
			debug.writeException("__fetchAppModule__: while loading app module")
			return None

def load(name):
	global current
	module=__fetchAppModule__(name)
	if module:
		current=module
		debug.writeMessage("appModules.load: loaded app module %s"%name)
		return True
	elif name!="default":
		debug.writeMessage("appModules.load: no app module for %s, loading default"%name)
		return load("default")
	else:
		debug.writeError("appModules.load: could not load %s"%name)
		return False

