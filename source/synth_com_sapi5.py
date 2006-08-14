import os
import win32com.client

tts=None

class constants:
	SVSFlagsAsync = 1
	SVSFPurgeBeforeSpeak = 2

def initialize():
	global tts
	tts = win32com.client.Dispatch('sapi.SPVoice')

def getRate():
		return (tts.Rate+10)*5

def getVolume():
		return tts.Volume

def getVoice():
		return os.path.basename(tts.Voice.Id)

def getVoiceList():
		return None # todo

def setRate(value):
	tts.Rate = (value/5)-10

def setVolume(value):
	tts.Volume = value

def setVoice(value):
	pass # todo

def speakText(text,markup,wait=False):
	flags=0
	if wait is False:
		flags=constants.SVSFlagsAsync
	tts.Speak(text,flags)

def playSound(fileName,wait=False):
	pass # todo

def cancel():
	if tts.Status.RunningState == 2:
		tts.Speak('', constants.SVSFlagsAsync | constants.SVSFPurgeBeforeSpeak)
