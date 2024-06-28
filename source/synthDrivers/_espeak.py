# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2007-2020 NV Access Limited, Peter Vágner
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import nvwave
import threading
import queue
from ctypes import cdll, CFUNCTYPE, c_int, c_void_p, POINTER, sizeof, c_short
from ctypes import *  # noqa: F403
import config
import globalVars
from logHandler import log
import os

isSpeaking = False
onIndexReached = None
bgThread=None
bgQueue = None
player = None
espeakDLL=None
#: Keeps count of the number of bytes pushed for the current utterance.
#: This is necessary because index positions are given as ms since the start of the utterance.
_numBytesPushed = 0

# Parameter bounds
# maxRate set to 449 to avoid triggering sonic at rate = 100% when rate boost is off.
# See https://github.com/espeak-ng/espeak-ng/issues/131
minRate = 80
maxRate = 449
minPitch = 0
maxPitch = 99

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

# eSpeak initialization flags
espeakINITIALIZE_DONT_EXIT = 0x8000

class espeak_EVENT_id(Union):  # noqa: F405
	_fields_=[
		('number',c_int),
		('name',c_char_p),  # noqa: F405
		('string',c_char*8),  # noqa: F405
	]

class espeak_EVENT(Structure):  # noqa: F405
	_fields_=[
		('type',c_int),
		('unique_identifier',c_uint),  # noqa: F405
		('text_position',c_int),
		('length',c_int),
		('audio_position',c_int),
		('sample',c_int),
		('user_data',c_void_p),
		('id',espeak_EVENT_id),
	]

class espeak_VOICE(Structure):  # noqa: F405
	_fields_=[
		('name',c_char_p),  # noqa: F405
		('languages',c_char_p),  # noqa: F405
		('identifier',c_char_p),  # noqa: F405
		('gender',c_byte),  # noqa: F405
		('age',c_byte),  # noqa: F405
		('variant',c_byte),  # noqa: F405
		('xx1',c_byte),  # noqa: F405
		('score',c_int),
		('spare',c_void_p),
	]

	def __eq__(self, other):
		return isinstance(other, type(self)) and addressof(self) == addressof(other)  # noqa: F405

	# As __eq__ was defined on this class, we must provide __hash__ to remain hashable.
	# The default hash implementation is fine for  our purposes.
	def __hash__(self):
		return super().__hash__()

# constants that can be returned by espeak_callback
CALLBACK_CONTINUE_SYNTHESIS=0
CALLBACK_ABORT_SYNTHESIS=1

def encodeEspeakString(text):
	return text.encode('utf8')

def decodeEspeakString(data):
	return data.decode('utf8')


t_espeak_callback = CFUNCTYPE(c_int, c_void_p, c_int, POINTER(espeak_EVENT))

@t_espeak_callback
def callback(wav,numsamples,event):
	try:
		global player, isSpeaking, _numBytesPushed
		if not isSpeaking:
			return CALLBACK_ABORT_SYNTHESIS
		indexes = []
		for e in event:
			if e.type==espeakEVENT_MARK:
				indexNum = int(decodeEspeakString(e.id.name))
				# e.audio_position is ms since the start of this utterance.
				# Convert to bytes since the start of the utterance.
				BYTES_PER_SAMPLE = 2
				MS_PER_SEC = 1000
				bytesPerMS = player.samplesPerSec * BYTES_PER_SAMPLE  // MS_PER_SEC
				indexByte = e.audio_position * bytesPerMS
				# Subtract bytes in the utterance that have already been handled
				# to give us the byte offset into the samples for this callback.
				indexByte -= _numBytesPushed
				indexes.append((indexNum, indexByte))
			elif e.type==espeakEVENT_LIST_TERMINATED:
				break
		if not wav:
			player.idle()
			onIndexReached(None)
			isSpeaking = False
			return CALLBACK_CONTINUE_SYNTHESIS
		prevByte = 0
		length = numsamples * sizeof(c_short)
		for indexNum, indexByte in indexes:
			# Sometimes, rate boost can result in spurious index values.
			if indexByte < 0:
				indexByte = 0
			elif indexByte > length:
				indexByte = length
			player.feed(
				c_void_p(wav + prevByte),
				size=indexByte - prevByte,
				onDone=lambda indexNum=indexNum: onIndexReached(indexNum)
			)
			prevByte = indexByte
			if not isSpeaking:
				return CALLBACK_ABORT_SYNTHESIS
		player.feed(c_void_p(wav + prevByte), size=length - prevByte)
		_numBytesPushed += length
		return CALLBACK_CONTINUE_SYNTHESIS
	except:  # noqa: E722
		log.error("callback", exc_info=True)

class BgThread(threading.Thread):
	def __init__(self):
		super().__init__(name=f"{self.__class__.__module__}.{self.__class__.__qualname__}")
		self.daemon = True

	def run(self):
		global isSpeaking
		while True:
			func, args, kwargs = bgQueue.get()
			if not func:
				break
			try:
				func(*args, **kwargs)
			except:  # noqa: E722
				log.error("Error running function from queue", exc_info=True)
			bgQueue.task_done()

def _execWhenDone(func, *args, mustBeAsync=False, **kwargs):
	global bgQueue
	if mustBeAsync or bgQueue.unfinished_tasks != 0:
		# Either this operation must be asynchronous or There is still an operation in progress.
		# Therefore, run this asynchronously in the background thread.
		bgQueue.put((func, args, kwargs))
	else:
		func(*args, **kwargs)

def _speak(text):
	global isSpeaking, _numBytesPushed
	uniqueID=c_int()
	# if eSpeak was interupted while speaking ssml that changed parameters such as pitch,
	# It may not reset those runtime values back to the user-configured values.
	# Therefore forcefully cause eSpeak to reset its parameters each time beginning to speak again after not speaking. 
	if not isSpeaking:
		espeakDLL.espeak_ng_Cancel()
	isSpeaking = True
	_numBytesPushed = 0
	# eSpeak can only process compound emojis  when using a UTF8 encoding
	text=text.encode('utf8',errors='ignore')
	flags = espeakCHARS_UTF8 | espeakSSML | espeakPHONEMES
	return espeakDLL.espeak_Synth(text,0,0,0,0,flags,byref(uniqueID),0)  # noqa: F405

def speak(text):
	global bgQueue
	_execWhenDone(_speak, text, mustBeAsync=True)

def stop():
	global isSpeaking, bgQueue
	# Kill all speech from now.
	# We still want parameter changes to occur, so requeue them.
	params = []
	try:
		while True:
			item = bgQueue.get_nowait()
			if item[0] != _speak:
				params.append(item)
			bgQueue.task_done()
	except queue.Empty:
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
	_execWhenDone(espeakDLL.espeak_SetParameter,param,value,relative)

def getParameter(param,current):
	return espeakDLL.espeak_GetParameter(param,current)

def getVoiceList():
	voices=espeakDLL.espeak_ListVoices(None)
	voiceList=[]
	for voice in voices:
		if not voice: break  # noqa: E701
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
	_execWhenDone(espeakDLL.espeak_SetVoiceByName,encodeEspeakString(name))

def _setVoiceAndVariant(voice=None, variant=None):
	v=getCurrentVoice()
	res = decodeEspeakString(v.identifier).split("+")
	if not voice:
		voice = res[0]
	if not variant:
		if len(res) == 2:
			variant = res[1]
		else:
			variant = "none"
	if variant == "none":
		espeakDLL.espeak_SetVoiceByName(encodeEspeakString(voice))
	else:
		try:
			espeakDLL.espeak_SetVoiceByName(encodeEspeakString("%s+%s" % (voice, variant)))
		except:  # noqa: E722
			espeakDLL.espeak_SetVoiceByName(encodeEspeakString(voice))

def setVoiceAndVariant(voice=None, variant=None):
	_execWhenDone(_setVoiceAndVariant, voice=voice, variant=variant)

def _setVoiceByLanguage(lang):
	v=espeak_VOICE()
	lang=lang.replace('_','-')
	v.languages=encodeEspeakString(lang)
	try:
		espeakDLL.espeak_SetVoiceByProperties(byref(v))  # noqa: F405
	except:  # noqa: E722
		v.languages=encodeEspeakString("en")
		espeakDLL.espeak_SetVoiceByProperties(byref(v))  # noqa: F405

def setVoiceByLanguage(lang):
	_execWhenDone(_setVoiceByLanguage, lang)

def espeak_errcheck(res, func, args):
	if res != EE_OK:
		raise RuntimeError("%s: code %d" % (func.__name__, res))
	return res

def initialize(indexCallback=None):
	"""
	@param indexCallback: A function which is called when eSpeak reaches an index.
		It is called with one argument:
		the number of the index or C{None} when speech stops.
	"""
	global espeakDLL, bgThread, bgQueue, player, onIndexReached
	espeakDLL = cdll.LoadLibrary(os.path.join(globalVars.appDir, "synthDrivers", "espeak.dll"))
	espeakDLL.espeak_Info.restype=c_char_p  # noqa: F405
	espeakDLL.espeak_Synth.errcheck=espeak_errcheck
	espeakDLL.espeak_SetVoiceByName.errcheck=espeak_errcheck
	espeakDLL.espeak_SetVoiceByProperties.errcheck=espeak_errcheck
	espeakDLL.espeak_SetParameter.errcheck=espeak_errcheck
	espeakDLL.espeak_Terminate.errcheck=espeak_errcheck
	espeakDLL.espeak_ListVoices.restype=POINTER(POINTER(espeak_VOICE))
	espeakDLL.espeak_GetCurrentVoice.restype=POINTER(espeak_VOICE)
	espeakDLL.espeak_SetVoiceByName.argtypes=(c_char_p,)  # noqa: F405
	eSpeakPath = os.path.join(globalVars.appDir, "synthDrivers")
	sampleRate = espeakDLL.espeak_Initialize(
		AUDIO_OUTPUT_SYNCHRONOUS, 300,
		os.fsencode(eSpeakPath),
		# #10607: ensure espeak does not exit NVDA's process on errors such as the espeak path being invalid.
		espeakINITIALIZE_DONT_EXIT
	)
	if sampleRate <= 0:
		raise OSError(f"espeak_Initialize failed with code {sampleRate}. Given Espeak data path of {eSpeakPath}")
	player = nvwave.WavePlayer(
		channels=1,
		samplesPerSec=sampleRate,
		bitsPerSample=16,
		outputDevice=config.conf["speech"]["outputDevice"],
		buffered=True
	)
	onIndexReached = indexCallback
	espeakDLL.espeak_SetSynthCallback(callback)
	bgQueue = queue.Queue()
	bgThread=BgThread()
	bgThread.start()


def terminate():
	global bgThread, bgQueue, player, espeakDLL , onIndexReached
	stop()
	bgQueue.put((None, None, None))
	bgThread.join()
	espeakDLL.espeak_Terminate()
	bgThread=None
	bgQueue=None
	player.close()
	player=None
	espeakDLL=None
	onIndexReached = None

def info():
	# Python 3.8: a path string must be specified, a NULL is fine when what we need is version string.
	return espeakDLL.espeak_Info(None).decode()

def getVariantDict():
	dir = os.path.join(globalVars.appDir, "synthDrivers", "espeak-ng-data", "voices", "!v")
	# Translators: name of the default espeak varient.
	variantDict={"none": pgettext("espeakVarient", "none")}
	for fileName in os.listdir(dir):
		absFilePath = os.path.join(dir, fileName)
		if os.path.isfile(absFilePath):
			# In python 3, open assumes the default system encoding by default.
			# This fails if Windows' "use Unicode UTF-8 for worldwide language support" option is enabled.
			# The expected encoding is unknown, therefore use latin-1 to stay as close to Python 2 behavior as possible.
			try:
				with open(absFilePath, 'r', encoding="latin-1") as file:
					for line in file:
						if line.startswith('name '):
							temp=line.split(" ")
							if len(temp) ==2:
								name=temp[1].rstrip()
								break
						name=None
			except:  # noqa: E722
				log.error("Couldn't parse espeak variant file %s" % fileName, exc_info=True)
				continue
		if name is not None:
			variantDict[fileName]=name
	return variantDict

