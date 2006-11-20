import winsound
import debug
from textProcessing import *
from config import conf, getSynthConfig
import synthDriverHandler

allowSpeech=True

def initialize():
	synthDriverHandler.setDriver(conf["speech"]["synth"])

def getLastIndex():
	return synthDriverHandler.getLastIndex()

def processText(text):
	text=processTextSymbols(text,expandPunctuation=conf["speech"][synthDriverHandler.driverName]["speakPunctuation"])
	return text

def playSound(fileName,wait=False):
	flags=0
	if wait is False:
		flags=winsound.SND_ASYNC
	winsound.PlaySound(fileName,flags)

def cancel():
	synthDriverHandler.cancel()

def speakMessage(text,wait=False,index=None):
	if not allowSpeech:
		return
	text=processText(text)
	if text and not text.isspace():
		synthDriverHandler.speakText(text,wait=wait,index=index)

def speakObjectProperties(name=None,typeString=None,stateText=None,value=None,description=None,help=None,keyboardShortcut=None,position=None,groupName=None,wait=False,index=None):
	if not allowSpeech:
		return
	text=""
	if groupName is not None:
		text="%s %s"%(text,groupName)
	if name is not None:
		text="%s %s"%(text,name)
	if typeString is not None:
		text+=" %s"%typeString
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
		synthDriverHandler.speakText(text,wait=wait,index=index)

def speakSymbol(symbol,wait=False,index=None):
	if not allowSpeech:
		return
	symbol=processSymbol(symbol)
	if (symbol[0]>='A') and (symbol[0]<='Z'):
		uppercase=True
	else:
		uppercase=False
	if uppercase:
		oldPitch=synthDriverHandler.getPitch()
		synthDriverHandler.setPitch(oldPitch+getSynthConfig()["relativeUppercasePitch"])
	synthDriverHandler.speakText(symbol,wait=wait,index=index)
	if uppercase:
		synthDriverHandler.setPitch(oldPitch)

def speakText(text,wait=False,index=None):
	if not allowSpeech:
		return
	text=processText(text)
	if text and not text.isspace():
		synthDriverHandler.speakText(text,wait=wait,index=index)

