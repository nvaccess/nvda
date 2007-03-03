#queueHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import types
from Queue import Queue
import debug

MAX_ITEMS=500
ID_SPEECH=0
ID_SCRIPT=1
ID_MOUSE=2
ID_EVENT=3
ID_CONFIG=4
queueOrder=list(range(5))
queueList=[Queue(MAX_ITEMS) for x in queueOrder]

generators={}
lastGeneratorObjID=0

def registerGeneratorObject(generatorObj):
	global lastGeneratorObjID
	if not isinstance(generatorObj,types.GeneratorType):
		raise TypeError('Arg 2 must be a generator object, not %s'%type(generatorObj))
	lastGeneratorObjID+=1
	generators[lastGeneratorObjID]=generatorObj

def queueFunction(queueID,func,*args,**vars):
	if not queueList[queueID].full():
		queueList[queueID].put_nowait((func,args,vars))
	else:
		raise RuntimeError('Queue full')

def isPendingItems(queueIDs=None):
	if queueIDs==None:
		queueIDs=queueOrder
	res=any((not queueList[x].empty() for x in queueIDs))
	return res

def isRunningGenerators():
	return True if len(generators)>0 else False

def pumpAll():
	for ID in generators.keys():
		try:
			generators[ID].next()
		except:
			del generators[ID]
	for queueID,queue in enumerate(queueList):
		if queue.empty():
			continue
		(func,args,vars)=queue.get_nowait()
		if queueID==ID_SPEECH:
			debug.writeMessage("speech queue: %s%s"%(func,str(args)))
		elif queueID==ID_SCRIPT:
			debug.writeMessage("speech queue: %s%s"%(func,str(args)))
		try:
			func(*args,**vars)
		except:
			debug.writeException("function from queue %s"%queueID)
