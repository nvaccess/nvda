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

def readObjects(obj):
	queueHandler.registerGeneratorObject(readObjectsHelper_generator(obj))

def readObjectsHelper_generator(obj):
	levelsIndexMap={}
	startKeyCount=globalVars.keyCounter
	updateObj=obj
	keepReading=True
	keepUpdating=True
	indexCount=0
	lastSpokenIndex=0
	endIndex=0
	while keepUpdating:
		if globalVars.keyCounter>startKeyCount:
			speech.cancelSpeech()
			break
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
	queueHandler.registerGeneratorObject(readTextHelper_generator(info,cursor))

def readTextHelper_generator(info,cursor):
	sendCount=0
	receiveCount=0
	cursorIndexMap={}
	startKeyCount=globalVars.keyCounter
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
				index=hash(bookmark)
				reader.expand(textHandler.UNIT_READINGCHUNK)
				speech.speakFormattedText(reader,includeBlankText=False,index=index)
				sendCount+=1
				cursorIndexMap[index]=(bookmark,sendCount)
				reader.collapse()
				delta=reader.moveByUnit(textHandler.UNIT_READINGCHUNK,1)
				if delta<=0:
					keepReading=False
		spokenIndex=speech.getLastSpeechIndex()
		if spokenIndex!=oldSpokenIndex:
			oldSpokenIndex=spokenIndex
			data=cursorIndexMap.get(spokenIndex,None)
			if data is not None:
				bookmark,receiveCount=data
				updater=reader.obj.makeTextInfo(bookmark)
				if cursor==CURSOR_CARET:
					updater.updateCaret()
				if cursor!=CURSOR_CARET or globalVars.caretMovesReviewCursor:
					updater.obj.reviewPosition=updater
		while speech.isPaused and globalVars.keyCounter==startKeyCount:
			yield
		if globalVars.keyCounter!=startKeyCount:
			speech.cancelSpeech()
			keepUpdating=keepReading=False
		yield

def sayAll(fromOffset,toOffset,func_nextChunkOffsets,func_getText,func_beforeSpeakChunk,func_updateCursor):
	queueHandler.registerGeneratorObject(sayAllHelper_generator(fromOffset,toOffset,func_nextChunkOffsets,func_getText,func_beforeSpeakChunk,func_updateCursor))

def sayAllHelper_generator(fromOffset,toOffset,func_nextChunkOffsets,func_getText,func_beforeSpeakChunk,func_updateCursor):
	curPos=fromOffset
	lastKeyCount=globalVars.keyCounter
	updateGen=updateCursor_generator(fromOffset,toOffset,func_updateCursor)
	loopCount=0
	while lastKeyCount==globalVars.keyCounter:
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
		updateGen.next()
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
