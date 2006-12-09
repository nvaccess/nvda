#core.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import ctypes
import time
import globalVars
import winUser
from api import *
from constants import *
import NVDAObjects
import keyboardHandler
import mouseHandler
import MSAAHandler
import appModuleHandler
import audio
import config
import gui
import Queue

msg=winUser.msgType()
queueList=[]
threads={}
lastThreadValues={}
lastThreadID=0

def newThreadID():
	"""Creates a new ID for a thread by finding out the last ID and adding 1"""
	global lastThreadID
	lastThreadID+=1
	return lastThreadID

def newThread(generator):
	"""Adds this generator object to the main thread list which will be iterated in the main core loop""" 
	ID=newThreadID()
	threads[ID]=generator
	return ID

def removeThread(ID):
	"""Removes a generator from the list of running threads
@param ID: thread ID
@type ID: int
"""  
	del threads[ID]

def threadExists(ID):
	"""Finds out of a thread with a given ID exists in the running threads list
@param ID: thread ID
@type ID: int
"""
	return threads.has_key(ID)

def getLastThreadValue(ID):
	"""Finds out the last value the thread with the given ID has set
@param ID: thread ID
@type ID: int
"""
	if lastThreadValues.has_key(ID):
		val=lastThreadValues[ID]
	else:
		val=None
	return val

def executeFunction(execType,func,*args,**vars):
	"""Adds a function along with its positional and keyword arguments to one of the core queues so it can be executed in the core thread as soon as possible.
@param execType: the identifier of the queue the function will be added to ( one of EXEC_SPEECH, EXEC_KEYBOARD, EXEC_MOUSE, EXEC_CONFIG, EXEC_USERINTERFACE). 
@type execType: int
"""
	while queueList[execType].full():
		time.sleep(0.001)
	queueList[execType].put((func,args,vars))

def main():
	"""NVDA's core main loop. This initializes all queues and modules such as audio, MSAA, keyboard, mouse, and GUI. Then it loops continuously, checking the queues and executing functions, plus pumping window messages, and sleeping when possible.
"""
	try:
		for num in range(EXEC_LAST+1):
			queueList.append(Queue.Queue(1000))
		audio.initialize()
		audio.speakMessage(_("Nonvisual Desktop Access Started"),wait=True)
		foregroundWindow=winUser.getForegroundWindow()
		if foregroundWindow==0:
			foregroundWindow=winUser.getDesktopWindow()
		MSAAHandler.executeEvent("foreground",foregroundWindow,-4,0)
		MSAAHandler.initialize()
		keyboardHandler.initialize()
		mouseHandler.initialize()
		gui.initialize()
		config.save()
	except:
		debug.writeException("core.py main init")
		try:
			gui.abort()
		except:
			pass
		return False
	try:
		globalVars.stayAlive=True
		while globalVars.stayAlive is True:
			for num in range(len(queueList)):
				if not queueList[num].empty():
					(func,args,vars)=queueList[num].get()
					try:
						func(*args,**vars)
					except:
						debug.writeException("core.main executing %s from queue %s"%(func.__name__,num))
			delList=[]
			for ID in threads.copy():
				try:
					lastThreadValues[ID]=threads[ID].next()
				except StopIteration:
					delList.append(ID)
			for ID in delList:
				del threads[ID]
			if winUser.peekMessage(ctypes.byref(msg),0,0,0,1):
				winUser.translateMessage(ctypes.byref(msg))
				winUser.dispatchMessage(ctypes.byref(msg))
			if queueList[EXEC_KEYBOARD].empty() and queueList[EXEC_MOUSE].empty() and queueList[EXEC_USERINTERFACE].empty() and queueList[EXEC_SPEECH].empty() and queueList[EXEC_CONFIG].empty():
				time.sleep(0.001)
	except:
		debug.writeException("core.py main loop")
		try:
			gui.abort()
		except:
			pass
		return False
	if globalVars.focusObject and hasattr(globalVars.focusObject,"event_looseFocus"):
		globalVars.focusObject.event_looseFocus()
	MSAAHandler.terminate()
	return True
