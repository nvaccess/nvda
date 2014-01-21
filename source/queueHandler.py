#queueHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import types
from Queue import Queue
import globalVars
from logHandler import log
import watchdog
import core

eventQueue=Queue()
eventQueue.__name__="eventQueue"
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
	for count in xrange(queue.qsize()+1):
		if not queue.empty():
			(func,args,kwargs)=queue.get_nowait()
			watchdog.alive()
			try:
				func(*args,**kwargs)
			except:
				log.exception("Error in func %s from %s"%(func.__name__,queue.__name__))

def isPendingItems(queue):
	if not queue.empty():
		res=True
	else:
		res=False
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
