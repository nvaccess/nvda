import time
import comtypesClient
import _winreg

name="sapi4"
description="Microsoft Speech API Engine version 4 (speech.voiceText)"

def check():
	try:
		r=_winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT,"Speech.VoiceText")
		r.Close()
		return True
	except:
		return False

class synthDriver(object):

	def __init__(self):
		self.lastIndex=None
		self.tts=comtypesClient.CreateObject("speech.voiceText")
		self.tts.Register("local_pc","nvda")

	def getRate(self):
		value=self.tts.Speed/4
		return value

	def getVolume(self):
		return 100


	def getVoice(self):
		return 1

	def getVoiceNames(self):
		return ["default"]

	def getLastIndex(self):
		return self.lastIndex

	def setRate(self,rate):
		rate=rate*4
		self.tts.Speed=rate

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
