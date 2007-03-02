#queueHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from Queue import Queue
import debug

MAX_ITEMS=500
ID_SPEECH=0
ID_SCRIPT=1
ID_MOUSE=2
ID_EVENT=3
ID_CONFIG=4
queueOrder=list(range(5))

queueList=[Queue(MAX_ITEMS)]*5
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
		queueList[queueID].put_nowait(lambda: func(*args,**vars))
	else:
		raise RuntimeError('Queue full')

def isPendingItems(queueIDs=[]):
	queueIDs=queueOrder if len(queueIDs)<1 else queueIDs
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
	for queueID in queueOrder:
		queue=queueList[queueID]
		if queue.empty():
			continue
		func=queue.get_nowait()
		try:
			func()
		except:
			debug.writeException("function from queue %s"%queueID)
