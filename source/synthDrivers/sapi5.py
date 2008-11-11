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
import synthDriverHandler
import config
import nvwave

class constants:
	SVSFlagsAsync = 1
	SVSFPurgeBeforeSpeak = 2
	SVSFIsXML = 8

COM_CLASS = "SAPI.SPVoice"

class SynthDriver(synthDriverHandler.SynthDriver):

	hasVoice=True
	hasRate=True
	hasPitch=True
	hasVolume=True

	name="sapi5"
	description="Microsoft Speech API version 5 (sapi.SPVoice)"

	@classmethod
	def check(cls):
		try:
			r=_winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT,COM_CLASS)
			r.Close()
			return True
		except:
			return False

	def __init__(self):
		self.tts = comtypes.client.CreateObject(COM_CLASS)
		self._pitch=50
		self.voice=self.tts.GetVoices()[0].Id


	def terminate(self):
		del self.tts

	def _getAvailableVoices(self):
		voices=[]
		for v in self.tts.GetVoices():
			ID=v.Id
			name=v.GetDescription()
			voices.append(synthDriverHandler.VoiceInfo(ID,name))
		return voices

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
		for v in self.tts.GetVoices():
			if value==v.Id:
				self.tts=comtypes.client.CreateObject('sapi.spVoice')
				outputDeviceID=nvwave.outputDeviceNameToID(config.conf["speech"]["outputDevice"], True)
				if outputDeviceID>=0:
					self.tts.audioOutput=self.tts.getAudioOutputs()[outputDeviceID]
				self.tts.voice=v
				self._voice=value
				break

	def speakText(self,text,index=None):
		flags=constants.SVSFIsXML
		text=text.replace("<","&lt;")
		pitch=(self._pitch/2)-25
		if isinstance(index,int):
			bookmarkXML="<Bookmark Mark=\"%d\" />"%index
		else:
			bookmarkXML=""
		flags=constants.SVSFIsXML|constants.SVSFlagsAsync
		self.tts.Speak("<pitch absmiddle=\"%s\">%s%s</pitch>"%(pitch,bookmarkXML,text),flags)

	def cancel(self):
		#if self.tts.Status.RunningState == 2:
		self.tts.Speak(None, 1|constants.SVSFPurgeBeforeSpeak)

	def pause(self,switch):
		if switch:
			self.cancel()
