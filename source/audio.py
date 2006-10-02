import winsound
import debug
from textProcessing import *
from config import conf, getSynthConfig
import synthDrivers

def initialize():
	synthDrivers.load(conf["speech"]["synth"])
	synthDrivers.current.setVoice(getSynthConfig()["voice"])
	synthDrivers.current.setRate(getSynthConfig()["rate"])
	synthDrivers.current.setVolume(getSynthConfig()["volume"])

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
	synthDrivers.current.cancel()

def speakMessage(text,wait=False):
	text=processText(text)
	if text and not text.isspace():
		synthDrivers.current.speakText(text,wait)

def speakObjectProperties(name=None,typeString=None,stateText=None,value=None,description=None,help=None,keyboardShortcut=None,position=None,groupName=None,wait=False):
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
		synthDrivers.current.speakText(text,wait)

def speakSymbol(symbol,wait=False):
	symbol=processSymbol(symbol)
	if (symbol[0]>='A') and (symbol[0]<='Z'):
		uppercase=True
	else:
		uppercase=False
	if uppercase:
		oldPitch=synthDrivers.current.getPitch()
		synthDrivers.current.setPitch(oldPitch+getSynthConfig()["relativeUppercasePitch"])
	synthDrivers.current.speakText("%s"%symbol,wait)
	if uppercase:
		synthDrivers.current.setPitch(oldPitch)

def speakText(text,wait=False):
	if (text is None) or (len(text)==1):
		speakSymbol(text,wait=wait)
		return
	text=processText(text)
	if text and not text.isspace():
		synthDrivers.current.speakText(text,wait)

