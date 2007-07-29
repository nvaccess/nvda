import time
import nvwave
import threading
import Queue
from ctypes import *
import debug
import winsound

paused=False
isSpeaking = False
lastIndex = None
bgThread=None
bgQueue = None
sampleRate=None
player = None
espeakDLL=None
lastCallbackBuffer=""
lastLastCallbackBuffer=""

#Parameter bounds
minRate=80
maxRate=370
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
espeakEMPHASIS=7
espeakLINELENGTH=8
espeakVOICETYPE=9

#error codes
EE_OK=0
EE_INTERNAL_ERROR=-1
EE_BUFFER_FULL=1
EE_NOT_FOUND=2

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
	global player, isSpeaking, lastIndex, lastCallbackBuffer, lastLastCallbackBuffer
	didPause=False
	lastIndex = event.contents.user_data
	if not wav:
		player.sync()
		isSpeaking = False
		return 0
	if not isSpeaking:
		return 1
	while paused:
		didPause=True
	if didPause:
		player.feed(lastLastCallbackBuffer)
		player.feed(lastCallbackBuffer)
	if numsamples > 0:
		if not isSpeaking:
			return 1
		lastLastCallbackBuffer=lastCallbackBuffer
		lastCallbackBuffer=string_at(wav, numsamples * sizeof(c_short))
		player.feed(lastCallbackBuffer)
	return 0

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
				res=func(*args, **kwargs)
				if res not in (None,EE_OK):
					raise OSError("%s, %d"%(str(func),res))
				bgQueue.task_done()
		except:
			debug.writeException("bgThread.run")

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
	global isSpeaking, bgQueue, paused, lastCallbackBuffer, lastLastCallbackBuffer
	# Kill all speech from now.
	# We still want parameter changes to occur, so requeue them.
	params = []
	try:
		while not bgQueue.empty():
			item = bgQueue.get_nowait()
			if item[0] == espeakDLL.espeak_SetParameter:
				params.append(item)
	except Queue.Empty:
		# In some rare cases, the queue can be empty even after queue.empty() returns False.
		pass
	for item in params:
		bgQueue.put(item)
	isSpeaking = False
	paused=False
	lastCallbackBuffer=lastLastCallbackBuffer=""
	player.stop()

def pause(switch):
	global paused
	if switch:
		player.stop()
	paused=switch

def setParameter(param,value,relative):
	_bgExec(espeakDLL.espeak_SetParameter,param,value,relative)

def getParameter(param,current):
	return espeakDLL.espeak_GetParameter(param,current)

def getVoiceList():
	begin=espeakDLL.espeak_ListVoices(None)
	count=0
	voiceList=[]
	while True:
		if not begin[count]: break
 		voiceList.append(begin[count].contents)
		count+=1
	return voiceList

def getCurrentVoice():
	voice =  espeakDLL.espeak_GetCurrentVoice()
	if voice:
		return voice.contents
	else:
		return None

def setVoice(voice):
	# For some weird reason, espeak_EspeakSetVoiceByProperties throws an integer divide by zero exception.
	res=espeakDLL.espeak_SetVoiceByName(voice.identifier)
	if res!=EE_OK:
		raise OSError("espeak_SetVoiceByName %d"%res)

def setVoiceByName(name):
	res=espeakDLL.espeak_SetVoiceByName(name)
	if res!=EE_OK:
		raise OSError("espeak_SetVoiceByName, %d"%res)

def setVoiceByLanguage(lang):
	v=espeak_VOICE()
	lang=lang.replace('_','-')
	v.languages=lang
	res=espeakDLL.espeak_SetVoiceByProperties(byref(v))
	if res!=EE_OK:
		raise RuntimeError("espeakDLL.setVoiceByProperties: %d"%res)

def initialize():
	global espeakDLL, bgThread, bgQueue, player, sampleRate
	espeakDLL=cdll.LoadLibrary(r"synthDrivers\espeak.dll")
	espeakDLL.espeak_ListVoices.restype=POINTER(POINTER(espeak_VOICE))
	espeakDLL.espeak_GetCurrentVoice.restype=POINTER(espeak_VOICE)
	sampleRate=espeakDLL.espeak_Initialize(AUDIO_OUTPUT_SYNCHRONOUS,300,"synthDrivers",0)
	if sampleRate<0:
		raise OSError("espeak_Initialize %d"%sampleRate)
	player = nvwave.WavePlayer(channels=1, samplesPerSec=sampleRate, bitsPerSample=16)
	espeakDLL.espeak_SetSynthCallback(callback)
	bgQueue = Queue.Queue()
	bgThread=BgThread()
	bgThread.start()

def terminate():
	global bgThread, bgQueue, player, espeakDLL 
	stop()
	bgQueue.put((None, None, None))
	bgThread.join()
	res=espeakDLL.espeak_Terminate()
	if res!=EE_OK:
		raise OSError("espeak_Terminate %d"%res)
	bgThread=None
	bgQueue=None
	player.close()
	player=None
	espeakDLL=None
