#tones.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import wave
import winsound
import os
import struct
import math
import tempfile
from glob import glob

sampleRate=22050.0
slopeRatio=0.01
amplitude=5000.0
tempdir=tempfile.gettempdir()

#Remove old tones
[os.remove(x) for x in glob("%s\\nvda_tone_*"%tempdir)]  

def beep(hz,length):
	fileName="%s\\nvda_tone_%sHZ%sMS.wav"%(tempdir,hz,length)
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
