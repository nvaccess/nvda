import win32com.client

class synthDriver(object):

	def __init__(self):
		self.tts=win32com.client.Dispatch("speech.voiceText")
		self.tts.Register("local_pc","nvda")

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

	def setRate(self,value):
		value=value*4
		self.tts.Speed=value

	def setVolume(self,value):
		pass

	def setVoice(self,value):
		pass

	def speakText(self,text,wait=False):
		self.tts.Speak(text,0)
		if wait is True:
			while self.tts.IsSpeaking:
				pass


	def cancel(self):
		self.tts.StopSpeaking()



