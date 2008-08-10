#synthDrivers/_espeak.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import nvwave
import threading
import Queue
from ctypes import *
import config
import globalVars
from logHandler import log
import os
import codecs

isSpeaking = False
lastIndex = None
bgThread=None
bgQueue = None
player = None
espeakDLL=None

#Parameter bounds
minRate=80
maxRate=390
minPitch=0
maxPitch=99

#event types
espeakEVENT_LIST_TERMINATED=0
espeakEVENT_WORD=1
espeakEVENT_SENTENCE=2
espeakEVENT_MARK=3
espeakEVENT_PLAY=4
espeakEVENT_END=5
espeakEVENT_MSG_TERMINATED=6
espeakEVENT_PHONEME=7

#position types
POS_CHARACTER=1
POS_WORD=2
POS_SENTENCE=3

#output types
AUDIO_OUTPUT_PLAYBACK=0
AUDIO_OUTPUT_RETRIEVAL=1
AUDIO_OUTPUT_SYNCHRONOUS=2
AUDIO_OUTPUT_SYNCH_PLAYBACK=3

#synth flags
espeakCHARS_AUTO=0
espeakCHARS_UTF8=1
espeakCHARS_8BIT=2
espeakCHARS_WCHAR=3
espeakSSML=0x10
espeakPHONEMES=0x100
espeakENDPAUSE=0x1000
espeakKEEP_NAMEDATA=0x2000

#speech parameters
espeakSILENCE=0
espeakRATE=1
espeakVOLUME=2
espeakPITCH=3
espeakRANGE=4
espeakPUNCTUATION=5
espeakCAPITALS=6
espeakWORDGAP=7
espeakOPTIONS=8   # reserved for misc. options.  not yet used
espeakINTONATION=9
espeakRESERVED1=10
espeakRESERVED2=11

#error codes
EE_OK=0
#EE_INTERNAL_ERROR=-1
#EE_BUFFER_FULL=1
#EE_NOT_FOUND=2

class espeak_EVENT_id(Union):
	_fields_=[
		('number',c_int),
		('name',c_char_p),
	]

class espeak_EVENT(Structure):
	_fields_=[
		('type',c_int),
		('unique_identifier',c_uint),
		('text_position',c_int),
		('length',c_int),
		('audio_position',c_int),
		('sample',c_int),
		('user_data',c_void_p),
		('id',espeak_EVENT_id),
	]

class espeak_VOICE(Structure):
	_fields_=[
		('name',c_char_p),
		('languages',c_char_p),
		('identifier',c_char_p),
		('gender',c_byte),
		('age',c_byte),
		('variant',c_byte),
		('xx1',c_byte),
		('score',c_int),
		('spare',c_void_p),
	]

	def __eq__(self, other):
		return isinstance(other, type(self)) and addressof(self) == addressof(other)

t_espeak_callback=CFUNCTYPE(c_int,POINTER(c_short),c_int,POINTER(espeak_EVENT))

@t_espeak_callback
def callback(wav,numsamples,event):
	try:
		global player, isSpeaking, lastIndex
		lastIndex = event.contents.user_data
		if not wav:
			player.idle()
			isSpeaking = False
			return 0
		if not isSpeaking:
			return 1
		if numsamples > 0:
			try:
				player.feed(string_at(wav, numsamples * sizeof(c_short)))
			except:
				log.debugWarning("Error feeding audio to nvWave",exc_info=True)
		return 0
	except:
		log.error("callback", exc_info=True)

class BgThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.setDaemon(True)

	def run(self):
		global isSpeaking
		try:
			while True:
				func, args, kwargs = bgQueue.get()
				if not func:
					break
				func(*args, **kwargs)
				bgQueue.task_done()
		except:
			log.error("bgThread.run", exc_info=True)

def _bgExec(func, *args, **kwargs):
	global bgQueue
	bgQueue.put((func, args, kwargs))

def _speakBg(msg, index=None):
	global isSpeaking
	uniqueID=c_int()
	isSpeaking = True
	return espeakDLL.espeak_Synth(unicode(msg),0,0,0,0,espeakCHARS_WCHAR,byref(uniqueID),index)

def speak(msg, index=None, wait=False):
	global bgQueue
	_bgExec(_speakBg, msg, index)
	if wait:
		bgQueue.join()

def stop():
	global isSpeaking, bgQueue
	# Kill all speech from now.
	# We still want parameter changes to occur, so requeue them.
	params = []
	try:
		while True:
			item = bgQueue.get_nowait()
			if item[0] != _speakBg:
				params.append(item)
	except Queue.Empty:
		# Let the exception break us out of this loop, as queue.empty() is not reliable anyway.
		pass
	for item in params:
		bgQueue.put(item)
	isSpeaking = False
	player.stop()

def pause(switch):
	global player
	player.pause(switch)

def setParameter(param,value,relative):
	_bgExec(espeakDLL.espeak_SetParameter,param,value,relative)

def getParameter(param,current):
	return espeakDLL.espeak_GetParameter(param,current)

def getVoiceList():
	voices=espeakDLL.espeak_ListVoices(None)
	voiceList=[]
	for voice in voices:
		if not voice: break
 		voiceList.append(voice.contents)
	return voiceList

def getCurrentVoice():
	voice =  espeakDLL.espeak_GetCurrentVoice()
	if voice:
		return voice.contents
	else:
		return None

def setVoice(voice):
	# For some weird reason, espeak_EspeakSetVoiceByProperties throws an integer divide by zero exception.
	setVoiceByName(voice.identifier)

def setVoiceByName(name):
	_bgExec(espeakDLL.espeak_SetVoiceByName,name)

def _setVoiceAndVariantBg(voice=None, variant=None):
	res = getCurrentVoice().identifier.split("+")
	if not voice:
		voice = res[0]
	if not variant:
		if len(res) == 2:
			variant = res[1]
		else:
			variant = "none"
	if variant == "none":
		espeakDLL.espeak_SetVoiceByName(voice)
	else:
		try:
			espeakDLL.espeak_SetVoiceByName("%s+%s" % (voice, variant))
		except:
			espeakDLL.espeak_SetVoiceByName(voice)

def setVoiceAndVariant(voice=None, variant=None):
	_bgExec(_setVoiceAndVariantBg, voice=voice, variant=variant)

def setVoiceByLanguage(lang):
	v=espeak_VOICE()
	lang=lang.replace('_','-')
	v.languages=lang
	try:
		espeakDLL.espeak_SetVoiceByProperties(byref(v))
	except:
		v.languages="en"
		espeakDLL.espeak_SetVoiceByProperties(byref(v))

def espeak_errcheck(res, func, args):
	if res != EE_OK:
		raise RuntimeError("%s: code %d" % (func.__name__, res))
	return res

def initialize():
	global espeakDLL, bgThread, bgQueue, player
	espeakDLL=cdll.LoadLibrary(r"synthDrivers\espeak.dll")
	espeakDLL.espeak_Synth.errcheck=espeak_errcheck
	espeakDLL.espeak_SetVoiceByName.errcheck=espeak_errcheck
	espeakDLL.espeak_SetVoiceByProperties.errcheck=espeak_errcheck
	espeakDLL.espeak_SetParameter.errcheck=espeak_errcheck
	espeakDLL.espeak_Terminate.errcheck=espeak_errcheck
	espeakDLL.espeak_ListVoices.restype=POINTER(POINTER(espeak_VOICE))
	espeakDLL.espeak_GetCurrentVoice.restype=POINTER(espeak_VOICE)
	espeakDLL.espeak_SetVoiceByName.argtypes=(c_char_p,)
	sampleRate=espeakDLL.espeak_Initialize(AUDIO_OUTPUT_SYNCHRONOUS,300,"synthDrivers",0)
	if sampleRate<0:
		raise OSError("espeak_Initialize %d"%sampleRate)
	player = nvwave.WavePlayer(channels=1, samplesPerSec=sampleRate, bitsPerSample=16, outputDevice=config.conf["speech"]["outputDevice"])
	espeakDLL.espeak_SetSynthCallback(callback)
	bgQueue = Queue.Queue()
	bgThread=BgThread()
	bgThread.start()

def terminate():
	global bgThread, bgQueue, player, espeakDLL 
	stop()
	bgQueue.put((None, None, None))
	bgThread.join()
	espeakDLL.espeak_Terminate()
	bgThread=None
	bgQueue=None
	player.close()
	player=None
	espeakDLL=None

def getVariantDict():
	dir='synthDrivers\\espeak-data\\voices\\!v'
	variantDict={"none":_("none")}
	for fileName in os.listdir(dir):
		if os.path.isfile("%s\\%s"%(dir,fileName)):
			file=codecs.open("%s\\%s"%(dir,fileName))
			for line in file:
				if line.startswith('name '):
					temp=line.split(" ")
					if len(temp) ==2:
						name=temp[1].rstrip()
						break
				name=None
			file.close()
		if name is not None:
			variantDict[fileName]=name
	return variantDict

