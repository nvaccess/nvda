import winsound
import debug
from textProcessing import *
from config import conf, getSynthConfig
import synthDriverHandler

allowSpeech=True

def initialize():
	synthDriverHandler.load(conf["speech"]["synth"])
	synthDriverHandler.current.setVoice(getSynthConfig()["voice"])
	synthDriverHandler.current.setRate(getSynthConfig()["rate"])
	synthDriverHandler.current.setVolume(getSynthConfig()["volume"])

def processText(text):
	text=splitMultiCaseWords(text)
	text=processTextSymbols(text,keepInflection=True)
	return text

def playSound(fileName,wait=False):
	flags=0
	if wait is False:
		flags=winsound.SND_ASYNC
	winsound.PlaySound(fileName,flags)

def cancel():
	synthDriverHandler.current.cancel()

def speakMessage(text,wait=False):
	if not allowSpeech:
		return
	text=processText(text)
	if text and not text.isspace():
		synthDriverHandler.current.speakText(text,wait)

def speakObjectProperties(name=None,typeString=None,stateText=None,value=None,description=None,help=None,keyboardShortcut=None,position=None,groupName=None,wait=False):
	if not allowSpeech:
		return
	text=""
	if groupName is not None:
		text="%s %s"%(text,groupName)
	if name is not None:
		text="%s %s"%(text,name)
	if typeString is not None:
		text="%s %s"%(text,typeString)
	if stateText is not None:
		text="%s %s"%(text,stateText)
	if value is not None:
		text="%s %s"%(text,value)
	if description is not None:
		text="%s %s"%(text,description)
	if help is not None:
		text="%s %s"%(text,help)
	if keyboardShortcut is not None:
		text="%s %s"%(text,keyboardShortcut)
	if position is not None:
		text="%s %s"%(text,position)
	text=processText(text)
	if text and not text.isspace():
		synthDriverHandler.current.speakText(text,wait)

def speakSymbol(symbol,wait=False):
	if not allowSpeech:
		return
	symbol=processSymbol(symbol)
	if (symbol[0]>='A') and (symbol[0]<='Z'):
		uppercase=True
	else:
		uppercase=False
	if uppercase:
		oldPitch=synthDriverHandler.current.getPitch()
		synthDriverHandler.current.setPitch(oldPitch+getSynthConfig()["relativeUppercasePitch"])
	synthDriverHandler.current.speakText("%s"%symbol,wait)
	if uppercase:
		synthDriverHandler.current.setPitch(oldPitch)

def speakText(text,wait=False):
	if not allowSpeech:
		return
	if (text is None) or (len(text)==1):
		speakSymbol(text,wait=wait)
		return
	text=processText(text)
	if text and not text.isspace():
		synthDriverHandler.current.speakText(text,wait)

