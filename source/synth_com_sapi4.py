import win32com.client

tts=None

def initialize():
	global tts
	tts=win32com.client.Dispatch("speech.voiceText")
	tts.Register(0,"nvda")

def getRate():
	value=tts.Speed/8
	if value<0:
		value=0
	elif value>100:
		value=100
	return value


def getVolume():
	pass

def getVoice():
	pass

def getVoiceList():
	pass

def setRate(value):
	value=value*8
	tts.Speed=value

def setVolume(value):
	pass

def setVoice(value):
	pass

def speakText(text,markup,wait=False):
	tts.Speak(text,0)
	if wait is True:
		while tts.IsSpeaking:
			pass


def cancel():
	tts.StopSpeaking()



