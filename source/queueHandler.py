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
	global generators,lastGeneratorObjID
	if not isinstance(generatorObj,types.GeneratorType):
		raise TypeError('Arg 2 must be a generator object, not %s'%type(generatorObj))
	lastGeneratorObjID+=1
	globalVars.log.debug("Adding generator %d"%lastGeneratorObjID)
	generators[lastGeneratorObjID]=generatorObj
	return lastGeneratorObjID

def cancelGeneratorObject(generatorObjID):
	global generators
	try:
		del generators[generatorObjID]
	except KeyError:
		pass

def queueFunction(queue,func,*args,**kwargs):
	if not queue.full():
		queue.put_nowait((func,args,kwargs))
	else:
		argsText=",".join([str(x) for x in args])
		kwargsText=",".join(["%s=%s"%(x,y) for x,y in kwargs.items()])
		funcText="%s(%s)"%(func.__name__,",".join([x for x in (argsText,kwargsText) if x]))
		queueText=queue.__name__
		globalVars.log.warn("Queue full when trying to add function %s to %s"%(funcText,queueText))

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
	# This dict can mutate during iteration, so use keys().
	for ID in generators.keys():
		# KeyError could occur within the generator itself, so retrieve the generator first.
		try:
			gen = generators[ID]
		except KeyError:
			# Generator was cancelled. This is fine.
			continue
		try:
			globalVars.log.debug("pumping generator %d"%ID)
			gen.next()
		except StopIteration:
			globalVars.log.debug("generator %s finished"%ID)
			del generators[ID]
		except:
			globalVars.log.error("error in generator %d"%ID,exc_info=True)
			del generators[ID]
	flushQueue(interactiveQueue)
	flushQueue(eventQueue)
