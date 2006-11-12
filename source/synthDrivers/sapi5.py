import os
import comtypesClient
import debug

name="sapi5"
description="Microsoft Speech API Engine, version 5, com interface sapi.SPVoice"

class constants:
	SVSFlagsAsync = 1
	SVSFPurgeBeforeSpeak = 2
	SVSFIsXML = 8

class synthDriver(object):

	def __init__(self):
		self.lastIndex=0
		self.tts = comtypesClient.CreateObject('sapi.SPVoice')
		self.tts.Speak("<sapi>",constants.SVSFIsXML)
		self.curVoice=1
		self.curPitch=50

	def getRate(self):
		rate=(self.tts.Rate*5)+50
		return rate

	def getPitch(self):
		return self.curPitch

	def getVolume(self):
		return self.tts.Volume

	def getVoice(self):
		return self.curVoice

	def getVoiceNames(self):
		voiceNames=[]
		for num in range(self.tts.GetVoices().Count):
			voiceNames.append(self.tts.GetVoices()[num].GetDescription())
		return voiceNames

	def getLastIndex(self):
		return self.lastIndex

	def setRate(self,rate):
		self.tts.Rate = (rate-50)/5

	def setPitch(self,value):
		#pitch is really controled with xml around speak commands
		self.curPitch=value

	def setVolume(self,value):
		self.tts.Volume = value

	def setVoice(self,value):
		self.tts.Voice(self.tts.GetVoices()[value-1])
		self.curVoice=value

	def speakText(self,text,wait=False,index=None):
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
		if isinstance(index,int):
			wait=True
		if wait is False:
			flags=constants.SVSFlagsAsync
		self.tts.Speak("<pitch absmiddle=\"%s\">%s</pitch>"%(pitch,text),flags)
		if isinstance(index,int):
			self.lastIndex=index

	def cancel(self):
		if self.tts.Status.RunningState == 2:
			self.tts.Speak('', constants.SVSFlagsAsync | constants.SVSFPurgeBeforeSpeak)
