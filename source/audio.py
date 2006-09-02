import winsound
import debug
from textProcessing import *
from config import conf, getSynthConfig

synth=None

def initialize():
	global synth
	synth=__import__("synth_"+conf["speech"]["synth"])
	synth.initialize()
	synth.setRate(getSynthConfig()["rate"])

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
	synth.cancel()
	winsound.PlaySound("waves/silence.wav",winsound.SND_PURGE | winsound.SND_ASYNC)

def speakMessage(text,wait=False):
	text=processText(text)
	synth.speakText(text,None,wait)

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
	synth.speakText(text,None,wait)

def speakSymbol(symbol,wait=False):
	symbol=processSymbol(symbol)
	synth.speakText(symbol,None,wait)

def speakText(text,wait=False):
	if (text is None) or (len(text)==1):
		speakSymbol(text,wait=wait)
		return
	text=processText(text)
	synth.speakText(text,None,wait)

