#appModules/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import sys
import debug
import audio

#This is here so that the appModules are able to import modules from the appModules dir themselves
__path__=['.\\appModules']

#Holds the current appModule object
current=None

def load(name):
	global current
	if os.path.isfile(r'%s\appModules\%s.py'%(os.getcwd(),name)):
		debug.writeMessage("Found appModule %s"%name)
		try:
			current=__import__(name,globals(),locals(),[]).appModule()
			debug.writeMessage("Loaded appModule %s"%name)
			return True
		except:
			debug.writeException("Error in appModule %s"%name)
			audio.speakMessage("Error in appModule %s"%name,wait=True)
	else:
		debug.writeMessage("appModule %s does not exist"%name)
	if name!='_default':
		load('_default')
	else:
		raise ImportError('appModules\\_default')

