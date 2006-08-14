#debug.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import datetime
import traceback

debugFile=None

def writeMessage(message):
	debugFile.write("%s\n"%datetime.datetime.now())
	debugFile.write("Message: %s\n"%message)
	debugFile.flush()

def writeError(message):
	debugFile.write("%s\n"%datetime.datetime.now())
	debugFile.write("Error: %s\n"%message)
	debugFile.flush()

def writeException(message):
	debugFile.write("%s\n"%datetime.datetime.now())
	debugFile.write("Exception: %s\n----\n%s----\n"%(message,traceback.format_exc()))
	debugFile.flush()

def start(fileName):
	global debugFile
	debugFile=open(fileName,"w")
	writeMessage("Screen reader log file started")
	debugFile.flush()

def stop():
	debugFile.close()
