#queueHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import types
from Queue import Queue
import debug

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
	generators[lastGeneratorObjID]=generatorObj

def queueFunction(queue,func,*args,**vars):
	if not queue.full():
		queue.put_nowait((func,args,vars))
	else:
		pass #raise RuntimeError('Queue full')

def isRunningGenerators():
	return True if len(generators)>0 else False

def flushQueue(queue):
	for count in range(queue.qsize()+1):
		if not queue.empty():
			(func,args,vars)=queue.get_nowait()
			try:
				func(*args,**vars)
			except:
				debug.writeException("function from queue %s"%queue.__name__)

def isPendingItems(queue=None):
		if (queue is None  and (not eventQueue.empty() or not interactiveQueue.empty())) or not queue.empty():
			return True
		else:
			return False

def pumpAll():
	for ID in generators.keys():
		try:
			generators[ID].next()
		except StopIteration:
			del generators[ID]
		except:
			debug.writeException("generator %d" % ID)
			del generators[ID]
	flushQueue(interactiveQueue)
	flushQueue(eventQueue)
