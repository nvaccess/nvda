#tones.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import wave
import winsound
import tempfile
import os
import struct
import math

sampleRate=22050.0
slopeRatio=0.01
amplitude=5000.0

#Remove old tones
[os.remove("waves/%s"%x) for x in filter(lambda x: x.startswith("_tone"),os.listdir("waves"))]

def beep(hz,length):
	fileName="waves\\_tone%sHZ%sMS.wav"%(hz,length)
	if not os.path.isfile(fileName):
		waveFile=wave.open(fileName,'w')
		waveFile.setsampwidth(2)
		waveFile.setframerate(sampleRate)
		waveFile.setnchannels(1)
		volume=0
		sampleLength=int(length*(sampleRate/1000.0))
		slopeLength=sampleLength*slopeRatio
		riseEnd=slopeLength
		fallStart=sampleLength-slopeLength
		for sampleCount in xrange(sampleLength):
			if sampleCount<=riseEnd:
				volume=sampleCount/slopeLength
			elif sampleCount>=fallStart:
				volume=(sampleLength-sampleCount)/slopeLength
			data=struct.pack('h',amplitude*math.sin((sampleCount*math.pi*2)/(sampleRate/hz))*volume)
			waveFile.writeframes(data)
		waveFile.close()
	winsound.PlaySound(fileName,winsound.SND_FILENAME|winsound.SND_ASYNC)
