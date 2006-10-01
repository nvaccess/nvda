import os
import comtypes.client

tts=None
curVoice=1
curPitch=50

class constants:
	SVSFlagsAsync = 1
	SVSFPurgeBeforeSpeak = 2
	SVSFIsXML = 8

def initialize():
	global tts
	tts = comtypes.client.CreateObject('sapi.SPVoice')
	tts.Speak("<sapi>",constants.SVSFIsXML)

def getRate():
		return (tts.Rate*5)+50

def getPitch():
	return curPitch

def getVolume():
		return tts.Volume

def getVoice():
	return curVoice

def getVoiceList():
	pass

def setRate(value):
	tts.Rate = (value-50)/5

def setPitch(value):
	global curPitch
	curPitch=value

def setVolume(value):
	tts.Volume = value

def setVoice(value):
	global curVoice
	tts.Voice(tts.GetVoices().Item(value-1))
	curVoice=value

def speakText(text,wait=False):
	flags=constants.SVSFIsXML
	if curPitch>=70:
		pitch=24
	elif curPitch>50:
		pitch=10
	elif curPitch==50:
		pitch=0
	elif curPitch>=40:
		pitch=-10
	else:
		pitch=-24
	if wait is False:
		flags=constants.SVSFlagsAsync
	tts.Speak("<pitch absmiddle=\"%s\">%s</pitch>"%(pitch,text),flags)

def playSound(fileName,wait=False):
	pass # todo

def cancel():
	if tts.Status.RunningState == 2:
		tts.Speak('', constants.SVSFlagsAsync | constants.SVSFPurgeBeforeSpeak)
