"""NVDA debugging functions.
@var debugFile: holds the open file object of the debug file.
@type debugFile: file 
"""
#debug.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import datetime
import traceback
import winsound
import codecs

debugFile=None

def writeMessage(message):
	"""Writes a message to the debug file.
@param message: the message to write
@type message: string
"""
	try:
		debugFile.write("message %s\n"%datetime.datetime.now())
		debugFile.write("%s\n"%message)
		debugFile.flush()
	except:
		pass

def writeError(message):
	"""Writes an error message to the debug file.
@param message: the message to write
@type message: string
"""
	try:
		winsound.Beep(200,100)
		debugFile.write("Error %s\n"%datetime.datetime.now())
		debugFile.write("%s\n"%message)
		debugFile.flush()
	except:
		pass

def writeException(message):
	"""Writes the current traceback, and a message, to the debug file.
@param message: the message to write
@type message: string
"""
	try:
		trace=traceback.format_exc()
		winsound.Beep(200,100)
		debugFile.write("Exception %s\n"%datetime.datetime.now())
		debugFile.write("%s: ----\n%s\n----\n"%(message,trace))
		debugFile.flush()
	except:
		pass

def start(fileName):
	"""Starts debugging support.
@param fileName: the name of the log file to write to
@type fileName: string
"""
	global debugFile
	debugFile=codecs.open(fileName,"w","utf-8")
	writeMessage("Screen reader log file started")
	debugFile.flush()

def stop():
	"""Stops debugging support and closes the debug file.
"""
	debugFile.close()
