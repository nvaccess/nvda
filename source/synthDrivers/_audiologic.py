#synthDrivers/_audiologic.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from ctypes import *
import os

NvdaDir=os.getcwd()
TtsDir="c:\\TTS3\\"
Handle=c_int()
Tts=None
LastIndex=None

#Tts parameters constants
minRate=50
maxRate=200
minPitch=-12
maxPitch=+9
minVol=-40
maxVol=+12

#SynthStatus and SynthType Constants 
ST_NONE=0
SYNTH_IDLE=0
SYNTH_RUNNING=1
SYNTH_PAUSED=2

#callback constants
M_BOOKMARK=8

#others constants
ttsRate=0
ttsPitch=1
ttsVol=2
ttsExpression=3

class TtsProsody(Structure):
	_fields_=[
	('Speed', c_int),
	('Pitch', c_int),
	('Vol', c_int),
	('Expression', c_int),
	('PhraseSpeed', c_int),
	('PhrasePitch', c_int),
	('PhraseGain', c_int),
	('StressSpeed', c_int),
	('StreesPitch', c_int),
	('StreesGain', c_int),
	('Declination', c_int),
	('PauseFactor', c_int),
	('DoubleFactor', c_int),
	('RandomFactor', c_int)]

class Tts3Status(Structure):
	_fields_=[
	('SynthType', c_int),
	('SynthStatus', c_int),
	('CurrentTime', c_int),
	('SynthesisTime', c_int),
	('Samples', c_int),
	('CurrentCharIndex', c_int),
	('CurrentWordIndex', c_int),
	('CurrentChar', c_char),
	('CurrentWord', c_char_p)]


callbackType = WINFUNCTYPE(None, c_int, c_int, c_int, c_int)

@callbackType
def TtsCallBackProc(handle, callmode, index, sample):
	global LastIndex
	LastIndex=index

class TtsCallBack(Structure):
	_fields_=[
	('CallMode', c_int),
	('BookIndex', c_int),
	('CallbackProc', callbackType)]


call=TtsCallBack()

def TtsOpen():
	global Handle, Tts, call
	Tts=windll.LoadLibrary(TtsDir+"Tts3.dll")
	Tts.Tts3Open(TtsDir, byref(Handle))
	os.chdir(NvdaDir)	
	call.CallMode=M_BOOKMARK
	call.BookIndex=-1
	call.CallbackProc=TtsCallBackProc
	Tts.Tts3SetCallback(Handle, byref(call))

def TtsGetStatus():
	global Tts, Handle
	Status=Tts3Status()
	Tts.Tts3GetStatus(Handle, byref(Status))

def TtsSpeak(text):
	global Handle, Tts
	Tts.Tts3GenSpeech(Handle, c_char_p(text), 0)

def TtsStop():
	global Handle, Tts
	Tts.Tts3Stop(Handle, 1)

def TtsPause():
	global Handle, Tts
	Tts.Tts3Pause(Handle)

def TtsRestart():
	global Handle,Tts
	Tts.Tts3Restart(Handle)

def TtsSetParam(param, value, relative):
	global Tts, Handle 
	Tts.Tts3SetProsodyValue(Handle, param, value, relative)

def TtsGetProsody(param):
	global Tts, Handle 
	Parameters=TtsProsody()
	Tts.Tts3GetProsody(Handle, byref(Parameters))
	return getattr(Parameters, param)

def TtsClose():
	global Tts, Handle 
	TtsStop()
	Tts.Tts3Close(Handle)
	Status=Tts3Status()
	while Status.SynthType!=ST_NONE: TtsGetStatus()
	Tts=None
