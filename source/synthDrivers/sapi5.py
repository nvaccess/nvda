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
		self.eventHandler=self.eventHandlerType(self)
		self.tts = comtypesClient.CreateObject('sapi.SPVoice',sink=self.eventHandler)
		self.tts.Speak("<sapi>",constants.SVSFIsXML)
		self.curVoice=1
		self.curPitch=50

	class eventHandlerType(object):

		def __init__(self,synth):
			self.synth=synth

		def event(self,*args):
			debug.writeMessage("func %s"%str(args))

		def __getattr__(self,name):
			debug.writeMessage("get %s"%name)
			return self.event

	def getName(self):
		return name

	def getDescription(self):
		return description

	def getRate(self):
		rate=(self.tts.Rate*5)+50
		if rate<0:
			rate=0
		if rate>100:
			rate=100
		return rate

	def getPitch(self):
		return self.curPitch

	def getVolume(self):
		return self.tts.Volume

	def getVoice(self):
		return self.curVoice

	def getLastIndex(self):
		return self.lastIndex

	def setRate(self,rate):
		if rate<0:
			rate=0
		if rate>100:
			rate=100
		self.tts.Rate = (rate-50)/5

	def setPitch(self,value):
		#pitch is really controled with xml around speak commands
		self.curPitch=value

	def setVolume(self,value):
		self.tts.Volume = value

	def setVoice(self,value):
		self.tts.Voice(self.tts.GetVoices().Item(value-1))
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
