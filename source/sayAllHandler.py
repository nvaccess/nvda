#sayAllHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import queueHandler
import speech
import textHandler
import characterSymbols
import globalVars
import api
import tones
import time

CURSOR_CARET=0
CURSOR_REVIEW=1

_generatorID = None

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

def readObjectsHelper_generator(obj):
	levelsIndexMap={}
	updateObj=obj
	keepReading=True
	keepUpdating=True
	indexCount=0
	lastSpokenIndex=0
	endIndex=0
	while keepUpdating:
		while speech.isPaused:
			yield
			continue
		if keepReading:
			speech.speakObject(obj,index=indexCount,reason=speech.REASON_SAYALL)
			up=[]
			down=[]
			obj=obj.getNextInFlow(up=up,down=down)
			if not obj:
				endIndex=indexCount
				keepReading=False
			indexCount+=1
			levelsIndexMap[indexCount]=(len(up),len(down))
		spokenIndex=speech.getLastSpeechIndex()
		if spokenIndex is None:
			spokenIndex=0
		for count in range(spokenIndex-lastSpokenIndex):
			upLen,downLen=levelsIndexMap.get(lastSpokenIndex+count+1,(0,0))
			if upLen==0 and downLen==0:
				tones.beep(880,50)
			if upLen>0:
				for count in range(upLen+1):
					tones.beep(880*(1.25**count),50)
					time.sleep(0.025)
			if downLen>0:
				for count in range(downLen+1):
					tones.beep(880/(1.25**count),50)
					time.sleep(0.025)
			updateObj=updateObj.nextInFlow
			api.setNavigatorObject(updateObj)
		if not keepReading and spokenIndex>=endIndex:
			keepUpdating=False
		lastSpokenIndex=spokenIndex
		yield

def readText(info,cursor):
	_startGenerator(readTextHelper_generator(info,cursor))

def readTextHelper_generator(info,cursor):
	sendCount=0
	receiveCount=0
	cursorIndexMap={}
	reader=info.copy()
	if not reader.isCollapsed:
		reader.collapse()
	keepReading=True
	keepUpdating=True
	oldSpokenIndex=None
	while keepUpdating:
		if (sendCount-receiveCount)<=10:
			if keepReading:
				bookmark=reader.bookmark
				index=sendCount
				delta=reader.move(textHandler.UNIT_READINGCHUNK,1,endPoint="end")
				if delta<=0:
					keepReading=False
					continue
				speech.speakTextInfo(reader,reason=speech.REASON_SAYALL,index=index)
				sendCount+=1
				cursorIndexMap[index]=bookmark
				reader.collapse(end=True)
		spokenIndex=speech.getLastSpeechIndex()
		if spokenIndex!=oldSpokenIndex:
			oldSpokenIndex=spokenIndex
			receiveCount=spokenIndex
			bookmark=cursorIndexMap.get(spokenIndex,None)
			if bookmark is not None:
				updater=reader.obj.makeTextInfo(bookmark)
				if cursor==CURSOR_CARET:
					updater.updateCaret()
				if cursor!=CURSOR_CARET or globalVars.caretMovesReviewCursor:
					api.setReviewPosition(updater)
		while speech.isPaused:
			yield
		yield

def sayAll(fromOffset,toOffset,func_nextChunkOffsets,func_getText,func_beforeSpeakChunk,func_updateCursor):
	_startGenerator(sayAllHelper_generator(fromOffset,toOffset,func_nextChunkOffsets,func_getText,func_beforeSpeakChunk,func_updateCursor))

def sayAllHelper_generator(fromOffset,toOffset,func_nextChunkOffsets,func_getText,func_beforeSpeakChunk,func_updateCursor):
	curPos=fromOffset
	updateGen=updateCursor_generator(fromOffset,toOffset,func_updateCursor)
	loopCount=0
	while True:
		if (curPos is not None) and (curPos<toOffset):
			nextRange=func_nextChunkOffsets(curPos)
			if nextRange is None:
				curRange=[curPos,toOffset]
			else:
				curRange=[curPos,nextRange[0]]
			func_beforeSpeakChunk(curPos)
			text=func_getText(curRange[0],curRange[1])
			if text and not text.isspace():
				speech.speakText(text,index=curPos)
			if (nextRange is None) or (nextRange[0]>=toOffset) or (nextRange[0]<=curPos):
				speech.speakMessage(_("end of text"),index=toOffset)
				curPos=None
			else:
				curPos=nextRange[0]
		if loopCount>4:
			yield
			yield
		next(updateGen)
		if loopCount>4:
			yield
			yield
		loopCount+=1

def updateCursor_generator(fromOffset,toOffset,func_updateCursor):
	lastIndex=fromOffset-1
	while True:
		index=speech.getLastSpeechIndex()
		if (index is not None) and (index>lastIndex) and (index<=toOffset):
			func_updateCursor(index)
			lastIndex=index
		yield
		yield
