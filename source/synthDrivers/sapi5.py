import os
import comtypes.client

class constants:
	SVSFlagsAsync = 1
	SVSFPurgeBeforeSpeak = 2
	SVSFIsXML = 8

class synthDriver(object):

	def __init__(self):
		self.tts = comtypes.client.CreateObject('sapi.SPVoice')
		self.tts.Speak("<sapi>",constants.SVSFIsXML)
		self.curVoice=1
		self.curPitch=50

	def getRate(self):
		return (self.tts.Rate*5)+50

	def getPitch(self):
		return self.curPitch

	def getVolume(self):
		return self.tts.Volume

	def getVoice(self):
		return self.curVoice

	def setRate(self,value):
		self.tts.Rate = (value-50)/5

	def setPitch(self,value):
		#pitch is really controled with xml around speak commands
		self.curPitch=value

	def setVolume(self,value):
		self.tts.Volume = value

	def setVoice(self,value):
		self.tts.Voice(self.tts.GetVoices().Item(value-1))
		self.curVoice=value

	def speakText(self,text,wait=False):
		flags=constants.SVSFIsXML
		if self.curPitch>=70:
			pitch=24
		elif self.curPitch>50:
			pitch=10
		elif self.curPitch==50:
			pitch=0
		elif self.curPitch>=40:
			pitch=-10
		else:
			pitch=-24
		if wait is False:
			flags=constants.SVSFlagsAsync
		self.tts.Speak("<pitch absmiddle=\"%s\">%s</pitch>"%(pitch,text),flags)

	def cancel(self):
		if self.tts.Status.RunningState == 2:
			self.tts.Speak('', constants.SVSFlagsAsync | constants.SVSFPurgeBeforeSpeak)
