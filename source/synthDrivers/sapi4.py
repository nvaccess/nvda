import time
import comtypesClient

name="sapi4"
description="Microsoft Speech API Engine, version 4, com interface speech.voiceText"

class synthDriver(object):

	def __init__(self):
		self.lastIndex=None
		self.tts=comtypesClient.CreateObject("speech.voiceText")
		self.tts.Register("local_pc","nvda")

	def getName(self):
		return name

	def getDescription(self):
		return description


	def getRate(self):
		value=self.tts.Speed/8
		if value<0:
			value=0
		elif value>100:
			value=100
		return value

	def getVolume(self):
		pass

	def getVoice(self):
		pass

	def getLastIndex(self):
		return self.lastIndex

	def setRate(self,value):
		value=value*4
		self.tts.Speed=value

	def setVolume(self,value):
		pass

	def setVoice(self,value):
		pass

	def speakText(self,text,wait=False,index=None):
		if isinstance(index,int):
			wait=True
		self.tts.Speak(text,0)
		if wait is True:
			while self.tts.IsSpeaking:
				time.sleep(0.01)
			if isinstance(index,int):
				self.lastIndex=index

	def cancel(self):
		if self.tts.IsSpeaking:
			self.tts.StopSpeaking()
