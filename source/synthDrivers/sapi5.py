#synthDrivers/sapi5.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import locale
from collections import OrderedDict
import time
import os
import comtypes.client
from comtypes import COMError
import _winreg
import globalVars
import speech
from synthDriverHandler import SynthDriver,VoiceInfo
import config
import nvwave
from logHandler import log

class constants:
	SVSFlagsAsync = 1
	SVSFPurgeBeforeSpeak = 2
	SVSFIsXML = 8

COM_CLASS = "SAPI.SPVoice"

class SynthDriver(SynthDriver):
	supportedSettings=(SynthDriver.VoiceSetting(),SynthDriver.RateSetting(),SynthDriver.PitchSetting(),SynthDriver.VolumeSetting())

	name="sapi5"
	description="Microsoft Speech API version 5"

	@classmethod
	def check(cls):
		try:
			r=_winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT,COM_CLASS)
			r.Close()
			return True
		except:
			return False

	def __init__(self):
		self._pitch=50
		self._initTts()

	def terminate(self):
		del self.tts

	def _getAvailableVoices(self):
		voices=OrderedDict()
		v=self.tts.GetVoices()
		for i in range(len(v)):
			try:
				ID=v[i].Id
				name=v[i].GetDescription()
				try:
					language=locale.windows_locale[int(v[i].getattribute('language').split(';')[0],16)]
				except KeyError:
					language=None
			except COMError:
				log.warning("Could not get the voice info. Skipping...")
			voices[ID]=VoiceInfo(ID,name,language)
		return voices

	def _get_rate(self):
		return (self.tts.rate*5)+50

	def _get_pitch(self):
		return self._pitch

	def _get_volume(self):
		return self.tts.volume

	def _get_voice(self):
		return self.tts.voice.Id
 
	def _get_lastIndex(self):
		bookmark=self.tts.status.LastBookmark
		if bookmark!="" and bookmark is not None:
			return int(bookmark)
		else:
			return None

	def _set_rate(self,rate):
		self.tts.Rate = (rate-50)/5

	def _set_pitch(self,value):
		#pitch is really controled with xml around speak commands
		self._pitch=value

	def _set_volume(self,value):
		self.tts.Volume = value

	def _initTts(self):
		self.tts=comtypes.client.CreateObject(COM_CLASS)
		outputDeviceID=nvwave.outputDeviceNameToID(config.conf["speech"]["outputDevice"], True)
		if outputDeviceID>=0:
			self.tts.audioOutput=self.tts.getAudioOutputs()[outputDeviceID]

	def _set_voice(self,value):
		v=self.tts.GetVoices()
		for i in range(len(v)):
			if value==v[i].Id:
				break
		else:
			# Voice not found.
			return
		self._initTts()
		self.tts.voice=v[i]

	def speak(self,speechSequence):
		textList=[]
		for item in speechSequence:
			if isinstance(item,basestring):
				textList.append(item.replace("<","&lt;"))
			elif isinstance(item,speech.IndexCommand):
				textList.append("<Bookmark Mark=\"%d\" />"%item.index)
			elif isinstance(item,speech.CharacterModeCommand):
				textList.append("<spell>" if item.state else "</spell>")
			elif isinstance(item,speech.SpeechCommand):
				log.debugWarning("Unsupported speech command: %s"%item)
			else:
				log.error("Unknown speech: %s"%item)
		text="".join(textList)
		#Pitch must always be hardcoded
		pitch=(self._pitch/2)-25
		text="<pitch absmiddle=\"%s\">%s</pitch>"%(pitch,text)
		flags=constants.SVSFIsXML|constants.SVSFlagsAsync
		self.tts.Speak(text,flags)

	def cancel(self):
		#if self.tts.Status.RunningState == 2:
		self.tts.Speak(None, 1|constants.SVSFPurgeBeforeSpeak)

	def pause(self,switch):
		if switch:
			self.cancel()
