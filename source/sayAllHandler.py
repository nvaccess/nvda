#sayAllHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import queueHandler
import speech
import text
import characterSymbols
import globalVars

CURSOR_CARET=0
CURSOR_REVIEW=1

indexMap={}

def read(info,cursor):
	queueHandler.registerGeneratorObject(readHelper_generator(info,cursor))

def readHelper_generator(info,cursor):
	startKeyCount=globalVars.keyCounter
	indexMap.clear()
	reader=info.copy()
	reader.collapse()
	keepReading=True
	keepUpdating=True
	oldSpokenIndex=None
	endIndex=None
	while keepUpdating:
		if keepReading:
			bookmark=reader.bookmark
			index=hash(bookmark)
			reader.expand(text.UNIT_READINGCHUNK)
			delta=reader.compareEnd(info)
			if delta>=0:
				keepReading=False
				endIndex=index
			txt=reader.text
			if not keepReading or ((txt is not None) and (len(txt)>0) and (isinstance(txt,basestring) and not (set(txt)<=set(characterSymbols.blankList)))):
				indexMap[index]=bookmark
				speech.speakText(txt,index=index)
			if keepReading:
				reader.collapse(True)
		spokenIndex=speech.getLastSpeechIndex()
		if spokenIndex!=oldSpokenIndex:
			oldSpokenIndex=spokenIndex
			bookmark=indexMap.get(spokenIndex,None)
			if bookmark is not None:
				if cursor==CURSOR_CARET:
					reader.obj.makeTextInfo(bookmark).updateCaret()
				elif cursor==CURSOR_REVIEW:
					reader.obj.reviewPosition=reader.obj.makeTextInfo(bookmark)
		if endIndex is not None and spokenIndex==endIndex:
			keepUpdating=keepReading=False
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
