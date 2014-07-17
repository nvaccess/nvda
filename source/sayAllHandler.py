#sayAllHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2012 NVDA Contributors
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import itertools
import queueHandler
import config
import speech
import textInfos
import globalVars
import api
import tones
import time
import controlTypes

CURSOR_CARET=0
CURSOR_REVIEW=1

_generatorID = None
lastSayAllMode=None

def _startGenerator(generator):
	global _generatorID
	stop()
	_generatorID = queueHandler.registerGeneratorObject(generator)

def stop():
	"""Stop say all if a say all is in progress.
	"""
	global _generatorID
	if _generatorID is None:
		return
	queueHandler.cancelGeneratorObject(_generatorID)
	_generatorID = None

def isRunning():
	"""Determine whether say all is currently running.
	@return: C{True} if say all is currently running, C{False} if not.
	@rtype: bool
	@note: If say all completes and there is no call to L{stop} (which is called from L{speech.cancelSpeech}), this will incorrectly return C{True}.
		This should not matter, but is worth noting nevertheless.
	"""
	global _generatorID
	return _generatorID is not None

def readObjects(obj):
	_startGenerator(readObjectsHelper_generator(obj))

def generateObjectSubtreeSpeech(obj,indexGen):
	index=indexGen.next()
	speech.speakObject(obj,reason=controlTypes.REASON_SAYALL,index=index)
	yield obj,index
	child=obj.simpleFirstChild
	while child:
		childSpeech=generateObjectSubtreeSpeech(child,indexGen)
		for r in childSpeech:
			yield r
		child=child.simpleNext

def readObjectsHelper_generator(obj):
	lastSentIndex=0
	lastReceivedIndex=0
	speechGen=generateObjectSubtreeSpeech(obj,itertools.count())
	objIndexMap={}
	keepReading=True
	while True:
		# lastReceivedIndex might be None if other speech was interspersed with this say all.
		# In this case, we want to send more text in case this was the last chunk spoken.
		if lastReceivedIndex is None or (lastSentIndex-lastReceivedIndex)<=1:
			if keepReading:
				try:
					o,lastSentIndex=speechGen.next()
				except StopIteration:
					keepReading=False
					continue
				objIndexMap[lastSentIndex]=o
		receivedIndex=speech.getLastSpeechIndex()
		if receivedIndex!=lastReceivedIndex and (lastReceivedIndex!=0 or receivedIndex!=None): 
			lastReceivedIndex=receivedIndex
			lastReceivedObj=objIndexMap.get(lastReceivedIndex)
			if lastReceivedObj is not None:
				api.setNavigatorObject(lastReceivedObj)
			#Clear old objects from the map
			for i in objIndexMap.keys():
				if i<=lastReceivedIndex:
					del objIndexMap[i]
		while speech.isPaused:
			yield
		yield

def readText(cursor):
	global lastSayAllMode
	lastSayAllMode=cursor
	_startGenerator(readTextHelper_generator(cursor))

def readTextHelper_generator(cursor):
	if cursor==CURSOR_CARET:
		try:
			reader=api.getCaretObject().makeTextInfo(textInfos.POSITION_CARET)
		except (NotImplementedError, RuntimeError):
			return
	else:
		reader=api.getReviewPosition()

	lastSentIndex=0
	lastReceivedIndex=0
	cursorIndexMap={}
	keepReading=True
	speakTextInfoState=speech.SpeakTextInfoState(reader.obj)
	with SayAllProfileTrigger():
		while True:
			if not reader.obj:
				# The object died, so we should too.
				return
			# lastReceivedIndex might be None if other speech was interspersed with this say all.
			# In this case, we want to send more text in case this was the last chunk spoken.
			if lastReceivedIndex is None or (lastSentIndex-lastReceivedIndex)<=10:
				if keepReading:
					bookmark=reader.bookmark
					index=lastSentIndex+1
					delta=reader.move(textInfos.UNIT_READINGCHUNK,1,endPoint="end")
					if delta<=0:
						speech.speakWithoutPauses(None)
						keepReading=False
						continue
					speech.speakTextInfo(reader,unit=textInfos.UNIT_READINGCHUNK,reason=controlTypes.REASON_SAYALL,index=index,useCache=speakTextInfoState)
					lastSentIndex=index
					cursorIndexMap[index]=(bookmark,speakTextInfoState.copy())
					try:
						reader.collapse(end=True)
					except RuntimeError: #MS Word when range covers end of document
						speech.speakWithoutPauses(None)
						keepReading=False
			else:
				# We'll wait for speech to catch up a bit before sending more text.
				if speech.speakWithoutPauses.lastSentIndex is None or (lastSentIndex-speech.speakWithoutPauses.lastSentIndex)>=10:
					# There is a large chunk of pending speech
					# Force speakWithoutPauses to send text to the synth so we can move on.
					speech.speakWithoutPauses(None)
			receivedIndex=speech.getLastSpeechIndex()
			if receivedIndex!=lastReceivedIndex and (lastReceivedIndex!=0 or receivedIndex!=None): 
				lastReceivedIndex=receivedIndex
				bookmark,state=cursorIndexMap.get(receivedIndex,(None,None))
				if state:
					state.updateObj()
				if bookmark is not None:
					updater=reader.obj.makeTextInfo(bookmark)
					if cursor==CURSOR_CARET:
						updater.updateCaret()
					if cursor!=CURSOR_CARET or config.conf["reviewCursor"]["followCaret"]:
						api.setReviewPosition(updater)
			elif not keepReading and lastReceivedIndex==lastSentIndex:
				# All text has been sent to the synth.
				# Turn the page and start again if the object supports it.
				if isinstance(reader.obj,textInfos.DocumentWithPageTurns):
					try:
						reader.obj.turnPage()
					except RuntimeError:
						break
					else:
						reader=reader.obj.makeTextInfo(textInfos.POSITION_FIRST)
						keepReading=True
				else:
					break

			while speech.isPaused:
				yield
			yield

		# Wait until the synth has actually finished speaking.
		# Otherwise, if there is a triggered profile with a different synth,
		# we will switch too early and truncate speech (even up to several lines).
		# Send another index and wait for it.
		index=lastSentIndex+1
		speech.speak([speech.IndexCommand(index)])
		while speech.getLastSpeechIndex()<index:
			yield
			yield
		# Some synths say they've handled the index slightly sooner than they actually have,
		# so wait a bit longer.
		for i in xrange(30):
			yield

class SayAllProfileTrigger(config.ProfileTrigger):
	"""A configuration profile trigger for when say all is in progress.
	"""
	spec = "sayAll"
