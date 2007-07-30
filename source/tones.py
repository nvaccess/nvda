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
amplitude=7000.0

player = nvwave.WavePlayer(channels=1, samplesPerSec=int(sampleRate), bitsPerSample=16)

def beep(hz,length):
	player.stop()
	volume=0
	sampleLength=int(length*(sampleRate/1000.0))
	slopeLength=sampleLength*slopeRatio
	riseEnd=slopeLength
	fallStart=sampleLength-slopeLength
	data=""
	for sampleCount in xrange(sampleLength):
		if sampleCount<=riseEnd:
			volume=sampleCount/slopeLength
		elif sampleCount>=fallStart:
			volume=(sampleLength-sampleCount)/slopeLength
		data+=struct.pack('h',amplitude*math.sin((sampleCount*math.pi*2)/(sampleRate/hz))*volume)
	player.feed(data)
