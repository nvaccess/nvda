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
	debugFile.write("message %s\n"%datetime.datetime.now())
	debugFile.write("%s\n"%message)
	debugFile.flush()

def writeError(message):
	winsound.Beep(200,100)
	debugFile.write("Error %s\n"%datetime.datetime.now())
	debugFile.write("%s\n"%message)
	debugFile.flush()

def writeException(message):
	trace=traceback.format_exc()
	winsound.Beep(200,100)
	debugFile.write("Exception %s\n"%datetime.datetime.now())
	debugFile.write("%s: ----\n%s\n----\n"%(message,trace))
	debugFile.flush()

def start(fileName):
	global debugFile
	debugFile=codecs.open(fileName,"w","utf-8")
	writeMessage("Screen reader log file started")
	debugFile.flush()

def stop():
	debugFile.close()
