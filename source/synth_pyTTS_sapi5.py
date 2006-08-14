import pyTTS

tts=None

def initialize():
	global tts
	tts=pyTTS.Create()

def getRate():
		return (tts.GetRate()+10)*5

def getVolume():
		return tts.GetVolume()

def getVoice():
		return tts.GetVoice()

def getVoiceList():
		return tts.GetVoiceNames()

def setRate(value):
	tts.SetRate((value/5)-10)

def setVolume(value):
	tts.SetVolume(value)

def setVoice(value):
	tts.SetVoice(value)

def speakText(text,markup,wait=False):
	flags=0
	if wait is False:
		flags=pyTTS.tts_async
	tts.Speak(text,flags)

def playSound(fileName,wait=False):
	flags=0
	if wait is False:
		flags=pyTTS.tts_async
	tts.SpeakFromWave(fileName,flags)

def cancel():
	if tts.IsSpeaking():
		tts.Stop()


