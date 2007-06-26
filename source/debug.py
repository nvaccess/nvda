#debug.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
"""NVDA debugging functions.
@var debugFile: holds the open file object of the debug file.
@type debugFile: file 
"""

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
		winsound.PlaySound("waves\\error.wav",winsound.SND_FILENAME|winsound.SND_PURGE|winsound.SND_ASYNC)
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
	winsound.PlaySound("waves\\error.wav",winsound.SND_FILENAME|winsound.SND_PURGE|winsound.SND_ASYNC)
	try:
		info=traceback.format_exc()
	except:
		info='unknown'
	debugFile.write("Exception %s\n"%datetime.datetime.now())
	text = "%s: ----\n%s\n----\n"%(message,info)
	# Specifying errors="replace" to the utf-8 codec doesn't ignore decode errors in the ascii codec,
	# so convert to unicode here and specify errors="replace" to avoid errors.
	# However, don't try to convert if already unicode.
	if not isinstance(text, unicode):
		text=unicode(text)
	debugFile.write(text)
	debugFile.flush()

def start(fileName):
	"""Starts debugging support.
@param fileName: the name of the log file to write to
@type fileName: string
"""
	global debugFile
	debugFile=codecs.open(fileName,"w","utf-8",errors="replace")
	writeMessage("Screen reader log file started")
	debugFile.flush()

def stop():
	"""Stops debugging support and closes the debug file.
"""
	debugFile.close()
