#synthDrivers/sapi5.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import os
import comtypes.client
import _winreg
import globalVars
import silence
import config

class constants:
	SVSFlagsAsync = 1
	SVSFPurgeBeforeSpeak = 2
	SVSFIsXML = 8

class SynthDriver(silence.SynthDriver):

	hasVoice=True
	hasRate=True
	hasPitch=True
	hasVolume=True
	hasIndexing=True

	name="sapi5"
	description="Microsoft Speech API version 5 (sapi.SPVoice)"

	def check(self):
		try:
			r=_winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT,"SAPI.SPVoice")
			r.Close()
			return True
		except:
			return False

	def initialize(self):
		try:
			self.tts = comtypes.client.CreateObject('sapi.SPVoice')
			self._pitch=50
			self._voice=1
			return True
		except:
			return False

	def terminate(self):
		del self.tts

	def _get_voiceCount(self):
		return len(self.tts.GetVoices())

	def getVoiceName(self,num):
		return self.tts.GetVoices()[num-1].GetDescription()

	def _get_rate(self):
		return (self.tts.rate*5)+50

	def _get_pitch(self):
		return self._pitch

	def _get_volume(self):
		return self.tts.volume

	def _get_voice(self):
		return self._voice
 
	def _get_lastIndex(self):
		bookmark=self.tts.status.LastBookmark
		if bookmark!="" and bookmark is not None:
			return int(bookmark)
		else:
			return -1

	def _set_rate(self,rate):
		self.tts.Rate = (rate-50)/5

	def _set_pitch(self,value):
		#pitch is really controled with xml around speak commands
		self._pitch=value

	def _set_volume(self,value):
		self.tts.Volume = value

	def _set_voice(self,value):
		if value>self.voiceCount:
			value=1
		self.tts=comtypes.client.CreateObject('sapi.SPVoice')
		if config.conf["speech"]["outputDevice"] >=0:
			self.tts.audioOutput(self.tts.getAudioOutputs()[config.conf["speech"]["outputDevice"]])
		self.tts.Voice(self.tts.GetVoices()[value-1])
		self._voice=value


	def speakText(self,text,wait=False,index=None):
		flags=constants.SVSFIsXML
		text=text.replace("<","&lt;")
		pitch=(self._pitch/2)-25
		if isinstance(index,int):
			bookmarkXML="<Bookmark Mark=\"%d\" />"%index
		else:
			bookmarkXML=""
		flags=constants.SVSFIsXML
		if wait is False:
			flags+=constants.SVSFlagsAsync
		self.tts.Speak("<pitch absmiddle=\"%s\">%s%s</pitch>"%(pitch,bookmarkXML,text),flags)

	def cancel(self):
		#if self.tts.Status.RunningState == 2:
		self.tts.Speak(None, 1|constants.SVSFPurgeBeforeSpeak)

	def pause(self,switch):
		if switch:
			self.cancel()
