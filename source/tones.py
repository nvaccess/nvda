#tones.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import nvwave
import debug
import os
import struct
import math
from glob import glob
import config

piTwo=math.pi*2

sampleRate=22050
amplitude=14000

player = nvwave.WavePlayer(channels=2, samplesPerSec=int(sampleRate), bitsPerSample=16, outputDeviceNumber=config.conf["speech"]["outputDevice"])

def beep(hz,length,left=50,right=50):
	player.stop()
	samplesPerCycle=int(sampleRate/hz)
	numCycles=int((length/1000.0)/(samplesPerCycle*(1.0/sampleRate)))
	data=""
	cycleNum=0
	sampleNum=0
	while cycleNum<=numCycles:
		sample=min(max(math.sin(piTwo*(float(sampleNum)/samplesPerCycle))*2,-1),1)*amplitude
		if cycleNum==0:
			sample=sample*(float(sampleNum)/samplesPerCycle)
		elif cycleNum==numCycles:
			sample=sample*(1-(float(sampleNum)/samplesPerCycle))
		leftSample=sample*(left/100.0)
		rightSample=sample*(right/100.0)
		data+=struct.pack('hh',int(leftSample),int(rightSample))
		sampleNum+=1
		if sampleNum==samplesPerCycle:
			cycleNum+=1
			sampleNum=0
	player.feed(data)
