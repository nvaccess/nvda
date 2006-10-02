#synthDrivers/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os.path
import debug

current=None

def load(name):
	global current
	if os.path.isfile(r'%s\synthDrivers\%s.py'%(os.getcwd(),name)):
		try:
			current=__import__(name,globals(),None,[]).synthDriver()
			debug.writeMessage("Loaded synthDriver %s"%name)
			return True
		except:
			debug.writeException("Error in synthDriver %s"%name)
			return False
	else:
		debug.writeError("synthDriver %s does not exist"%name)
		return False
