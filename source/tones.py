import wave
import winsound
import tempfile
import os
import struct
import math

sampleRate=11025
slopeRatio=0.01
amplitude=10000

def beep(hz,length):
	fileName=tempfile.mktemp('.wav')
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
	winsound.PlaySound(fileName,winsound.SND_FILENAME)
	os.remove(fileName)
