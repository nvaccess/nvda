#queueHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import types
from Queue import Queue
import globalVars

MAX_ITEMS=500
interactiveQueue=Queue(MAX_ITEMS)
interactiveQueue.__name__="interactiveQueue"
eventQueue=Queue(MAX_ITEMS)
eventQueue.__name__="eventQueue"
generators={}
lastGeneratorObjID=0

def registerGeneratorObject(generatorObj):
	global lastGeneratorObjID
	if not isinstance(generatorObj,types.GeneratorType):
		raise TypeError('Arg 2 must be a generator object, not %s'%type(generatorObj))
	lastGeneratorObjID+=1
	globalVars.log.debug("Adding generator %s"%lastGeneratorObjID)
	generators[lastGeneratorObjID]=generatorObj

def queueFunction(queue,func,*args,**vars):
	if not queue.full():
		queue.put_nowait((func,args,vars))
	else:
		globalVars.log.warn("Queue full when trying to add func %s to %s"%(func.__name__,queue.__name__))
		pass #raise RuntimeError('Queue full')

def isRunningGenerators():
	res=len(generators)>0
	globalVars.log.debug("generators running: %s"%res)

def flushQueue(queue):
	for count in range(queue.qsize()+1):
		if not queue.empty():
			(func,args,vars)=queue.get_nowait()
			try:
				func(*args,**vars)
			except:
				globalVars.log.error("Error in func %s from %s"%(func.__name__,queue.__name__),exc_info=True)

def isPendingItems(queue=None):
	if (queue is None  and (not eventQueue.empty() or not interactiveQueue.empty())) or not queue.empty():
		res=True
	else:
		res=False
	queueString="%s"%queue.__name__ if queue is not None else "all queues"
	globalVars.log.debug("pending events in %s: %s"%(queueString,res))
	return res

def pumpAll():
	for ID in generators.keys():
		try:
			globalVars.log.debug("pumping generator %s"%ID)
			generators[ID].next()
		except StopIteration:
			globalVars.log.debug("generator %s finished"%ID)
			del generators[ID]
		except:
			globalVars.log.error("error in generator %s"%ID,exc_info=True)
			del generators[ID]
	flushQueue(interactiveQueue)
	flushQueue(eventQueue)
