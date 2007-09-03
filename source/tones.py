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

sampleRate=44100
amplitude=14000

player = nvwave.WavePlayer(channels=2, samplesPerSec=int(sampleRate), bitsPerSample=16, outputDeviceNumber=config.conf["speech"]["outputDevice"])

def beep(hz,length,left=50,right=50):
	hz=float(hz)
	player.stop()
	samplesPerCycle=(sampleRate/hz)
	totalSamples=(length/1000.0)/(1.0/sampleRate)
	totalSamples=totalSamples+(samplesPerCycle-(totalSamples%samplesPerCycle))
	data=""
	sampleNum=0
	while sampleNum<totalSamples:
		sample=min(max(math.sin((sampleNum%sampleRate)*piTwo*(hz/sampleRate))*2,-1),1)*amplitude
		leftSample=sample*(left/100.0)
		rightSample=sample*(right/100.0)
		data+=struct.pack('hh',int(leftSample),int(rightSample))
		sampleNum+=1
	player.feed(data)
