#tones.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import nvwave
import os
import struct
import math
from glob import glob

sampleRate=22050.0
slopeRatio=0.01
amplitude=10000.0

player = nvwave.WavePlayer(channels=1, samplesPerSec=int(sampleRate), bitsPerSample=16)

def beep(hz,length):
	player.stop()
	sampleLength=int(length*(sampleRate/1000.0))
	data=""
	cycleLength=sampleRate/hz
	halfCycleLength=cycleLength/2
	quarterCycleLength=cycleLength/4
	threeQuarterCycleLength=halfCycleLength+quarterCycleLength
	for sampleCount in xrange(sampleLength):
		cyclePos=sampleCount%cycleLength
		if cyclePos<=quarterCycleLength:
			sample=amplitude*(cyclePos/quarterCycleLength)
		elif cyclePos<=halfCycleLength:
			sample=amplitude*((halfCycleLength-cyclePos)/quarterCycleLength)
		elif cyclePos<=threeQuarterCycleLength:
			sample=0-(amplitude*((cyclePos-halfCycleLength)/quarterCycleLength))
		elif cyclePos<=cycleLength:
			sample=0-(amplitude*((halfCycleLength-(cyclePos-halfCycleLength))/quarterCycleLength))
		data+=struct.pack('h',sample)
	player.feed(data)
