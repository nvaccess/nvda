#queueHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2018 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import types
from queue import SimpleQueue
import globalVars
from logHandler import log
import watchdog
import core

# A queue for calls that should be made on NVDA's main thread
# #11369: We use SimpleQueue rather than Queue here
# as SimpleQueue is very light-weight, does not use locks
# and ensures that garbage collection won't unexpectedly happen in the middle of queuing something
# Which may cause a deadlock.
eventQueue = SimpleQueue()

generators={}
lastGeneratorObjID=0

def registerGeneratorObject(generatorObj):
	global generators,lastGeneratorObjID
	if not isinstance(generatorObj,types.GeneratorType):
		raise TypeError('Arg 2 must be a generator object, not %s'%type(generatorObj))
	lastGeneratorObjID+=1
	log.debug("Adding generator %d"%lastGeneratorObjID)
	generators[lastGeneratorObjID]=generatorObj
	core.requestPump()
	return lastGeneratorObjID

def cancelGeneratorObject(generatorObjID):
	global generators
	try:
		del generators[generatorObjID]
	except KeyError:
		pass

def queueFunction(queue,func,*args,**kwargs):
	queue.put_nowait((func,args,kwargs))
	core.requestPump()

def isRunningGenerators():
	res=len(generators)>0
	log.debug("generators running: %s"%res)

def flushQueue(queue):
	for count in range(queue.qsize()+1):
		if not queue.empty():
			(func,args,kwargs)=queue.get_nowait()
			watchdog.alive()
			try:
				func(*args,**kwargs)
			except:
				log.exception(f"Error in func {func.__qualname__}")

def isPendingItems(queue):
	if not queue.empty():
		res=True
	else:
		res=False
	return res

def pumpAll():
	# This dict can mutate during iteration, so wrap the keys in a list.
	for ID in list(generators):
		# KeyError could occur within the generator itself, so retrieve the generator first.
		try:
			gen = generators[ID]
		except KeyError:
			# Generator was cancelled. This is fine.
			continue
		watchdog.alive()
		try:
			next(gen)
		except StopIteration:
			log.debug("generator %s finished"%ID)
			del generators[ID]
		except:
			log.exception("error in generator %d"%ID)
			del generators[ID]
		# Lose our reference so Python can destroy the generator if appropriate.
		del gen
	if generators:
		core.requestPump()
	flushQueue(eventQueue)
