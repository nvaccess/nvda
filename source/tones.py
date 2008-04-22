#tones.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Utilities to generate and play tones"""

import nvwave
import struct
import math
from glob import glob
import config
import globalVars

piTwo=math.pi*2

sampleRate=44100
amplitude=14000

player = nvwave.WavePlayer(channels=2, samplesPerSec=int(sampleRate), bitsPerSample=16, outputDeviceNumber=config.conf["speech"]["outputDevice"])

def beep(hz,length,left=50,right=50):
	"""Plays a tone at the given hz, length, and stereo balance.
	@param hz: pitch in hz of the tone
	@type hz: float
	@param length: length of the tone in ms
	@type length: integer
	@param left: volume of the left channel (0 to 100)
	@type left: integer
	@param right: volume of the right channel (0 to 100)
	@type right: float
	""" 
	globalVars.log.info("Beep at pitch %s, for %s ms, left volume %s, right volume %s"%(hz,length,left,right))
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
