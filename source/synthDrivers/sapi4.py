import time
import comtypesClient
import _winreg
from autoPropertyType import autoPropertyType

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

	__metaclass__=autoPropertyType

	def __init__(self):
		self.lastIndex=None
		self.tts=comtypesClient.CreateObject("speech.voiceText")
		self.tts.Register("local_pc","nvda")

	def _get_rate(self):
		value=self.tts.Speed/4
		return value

	def _get_pitch(self):
		return 50

	def _get_volume(self):
		return 100

	def _get_voice(self):
		return 1

	def _get_voiceNames(self):
		return ["default"]

	def _set_rate(self,rate):
		rate=rate*4
		self.tts.Speed=rate

	def _set_pitch(self,val):
		pass

	def _set_volume(self,value):
		pass

	def _set_voice(self,value):
		pass

	def speakText(self,text,wait=False,index=None):
		self.tts.Speak(text,0)
		if wait is True:
			while self.tts.IsSpeaking:
				time.sleep(0.01)
			if isinstance(index,int):
				self.lastIndex=index

	def cancel(self):
		if self.tts.IsSpeaking:
			self.tts.StopSpeaking()
