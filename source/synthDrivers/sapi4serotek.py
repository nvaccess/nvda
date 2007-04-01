#synthDrivers/sapi4.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import winsound
import time
import _winreg
import pythoncom
import baseObject
import core
import _sapi4serotekHelper

name="sapi4"
description="Microsoft Speech API version 4 (Serotek driver)"

def check():
	return True
	try:
		r=_winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT,"Speech.VoiceText")
		r.Close()
		return True
	except:
		return False

class synthDriver(baseObject.autoPropertyObject):

	def __init__(self):
		self.tts=_sapi4serotekHelper.SAPI4()
		self.tts.say('')
		self._lastIndex=None
		self.tts.callWhenDone(self.onDoneSpeaking)
		self._waitFlag=False

	def onIndexMark(self,index):
		winsound.Beep(440,20)
		self._lastIndex=index

	def onDoneSpeaking(self):
		self.waitFlag=False

	def _get_rateRatio(self):
		return (self.tts.rateMax-self.tts.rateMin)/100.0
 
	def _get_rateOffset(self):
		return self.tts.rateMin

	def _get_rate(self):
		return int((self.tts.rate-self.rateOffset)/self.rateRatio)

	def _get_pitchRatio(self):
		return (self.tts.averagePitchMax-self.tts.averagePitchMin)/100.0

	def _get_pitchOffset(self):
		return self.tts.averagePitchMin

	def _get_pitch(self):
		return int((self.tts.averagePitch-self.pitchOffset)/self.pitchRatio)

	def _get_volume(self):
		return 100

	def _get_voice(self):
		curVoiceID=self.tts.voice
		for voiceNum in range(len(self.tts.voices)):
			if self.tts.voices[voiceNum][0]==curVoiceID:
				return voiceNum+1
		return -1
 
	def _get_lastIndex(self):
		return self._lastIndex

	def _get_voiceNames(self):
		return [x[1] for x in self.tts.voices]

	def _set_rate(self,rate):
		self.tts.rate = int(rate*self.rateRatio)+self.rateOffset

	def _set_pitch(self,value):
		self.tts.averagePitch=int(value*self.pitchRatio)+self.pitchOffset

	def _set_volume(self,value):
		pass

	def _set_voice(self,value):
		self.tts.voice=self.tts.voices[value-1][0]

	def speakText(self,text,wait=False,index=None):
		self.waitFlag=wait
		self.tts.say(text)
		if index is not None:
			self.addIndexMark(self.onIndexMark,[index],{})
			self.tts.speak()
		while self.waitFlag:
			pythoncom.PumpWaitingMessages()
			time.sleep(0.001)

	def cancel(self):
		self.tts.stop()
