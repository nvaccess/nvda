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

sampleRate=22050
amplitude=6000

player = nvwave.WavePlayer(channels=1, samplesPerSec=int(sampleRate), bitsPerSample=16, outputDeviceNumber=config.conf["speech"]["outputDevice"])

def beep(hz,length):
	player.stop()
	sampleLength=length*(sampleRate/1000)
	data=""
	for sampleCount in xrange(sampleLength):
		sampleCount=sampleCount%sampleLength
		sample=math.sin((sampleCount*math.pi*2)/(sampleRate/hz))*2
		if sample>1:
			sample=1
		elif sample<-1:
			sample=-1
		sample*=amplitude
		data+=struct.pack('h',sample)
	debug.writeMessage("sample: %s"%sample)
	player.feed(data)
