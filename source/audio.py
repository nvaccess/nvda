import time
import thread
import Queue
import winsound
import debug
from textProcessing import *
from config import conf, getSynthConfig
import synthDriverHandler

allowSpeech=True
queue_synthFunction=Queue.Queue(100)
keepLoopAlive=True

def queueSynthFunction(name,*args,**vars):
	while queue_synthFunction.full():
		time.sleep(0.001)
	queue_synthFunction.put((name,args,vars))

def synthFunctionLoop():
	while keepLoopAlive:
		while queue_synthFunction.empty():
			time.sleep(0.001)
		(name,args,vars)=queue_synthFunction.get()
		getattr(synthDriverHandler.current,name)(*args,**vars)
		time.sleep(0.01)

def initialize():
	global thread_synthFunctionLoop
	synthDriverHandler.load(conf["speech"]["synth"])
	synthDriverHandler.current.setVoice(getSynthConfig()["voice"])
	synthDriverHandler.current.setRate(getSynthConfig()["rate"])
	synthDriverHandler.current.setVolume(getSynthConfig()["volume"])
	thread_synthFunctionLoop=thread.start_new_thread(synthFunctionLoop,())

def terminate():
	global keepLoopAlive
	keepLoopAlive=False

def processText(text):
	text=processTextSymbols(text,keepInflection=True)
	return text

def playSound(fileName,wait=False):
	flags=0
	if wait is False:
		flags=winsound.SND_ASYNC
	winsound.PlaySound(fileName,flags)

def cancel():
	queue_synthFunction.queue.clear()
	queueSynthFunction("cancel")

def speakRealtimeMessage(text):
	text=processText(text)
	synthDriverHandler.current.speakText(text,wait=True)

def speakMessage(text,wait=False):
	if not allowSpeech:
		return
	text=processText(text)
	if text and not text.isspace():
		queueSynthFunction("speakText",text,wait=wait)

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
		queueSynthFunction("speakText",text,wait=wait)

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
		queueSynthFunction("setPitch",oldPitch+getSynthConfig()["relativeUppercasePitch"])
	queueSynthFunction("speakText",symbol,wait=wait)
	if uppercase:
		queueSynthFunction("setPitch",oldPitch)

def speakText(text,wait=False):
	if not allowSpeech:
		return
	if (text is None) or (len(text)==1):
		speakSymbol(text,wait=wait)
		return
	text=processText(text)
	if text and not text.isspace():
		queueSynthFunction("speakText",text,wait=wait)

