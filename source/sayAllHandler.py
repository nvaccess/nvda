#sayAllHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import core
import audio
import globalVars

def sayAll(fromOffset,toOffset,func_nextChunkOffsets,func_getText,func_beforeSpeakChunk,func_updateCursor):
	core.newThread(sayAllHelper_generator(fromOffset,toOffset,func_nextChunkOffsets,func_getText,func_beforeSpeakChunk,func_updateCursor))

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
				audio.speakText(text,index=curPos)
			if (nextRange is None) or (nextRange[0]>=toOffset) or (nextRange[0]<=curPos):
				audio.speakMessage("end of text",index=toOffset)
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
		index=audio.getLastIndex()
		if (index is not None) and (index>lastIndex) and (index<=toOffset):
			func_updateCursor(index)
			lastIndex=index
		yield
		yield
