#synthDrivers/sapi4.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import _winreg
from comtypes import COMObject, COMError
from ctypes import *
import synthDriverHandler
from logHandler import log
from _sapi4 import *
import config
import nvwave

class SynthDriverBufSink(COMObject):
	_com_interfaces_ = [ITTSBufNotifySink]

	def __init__(self,synthDriver):
		self._synthDriver=synthDriver
		super(SynthDriverBufSink,self).__init__()

	def ITTSBufNotifySink_BookMark(self, this, qTimeStamp, dwMarkNum):
		self._synthDriver.lastIndex=dwMarkNum

class SynthDriver(synthDriverHandler.SynthDriver):

	name="sapi4"
	description="Microsoft Speech API version 4"
	hasVoice=True
	hasRate=True
	hasPitch=True
	hasVolume=True

	@classmethod
	def check(cls):
		try:
			_winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, r"CLSID\%s" % CLSID_TTSEnumerator).Close()
			return True
		except WindowsError:
			return False

	def _fetchEnginesList(self):
		enginesList=[]
		self._ttsEngines.Reset()
		while True:
			mode=TTSMODEINFO()
			fetched=c_ulong()
			try:
				self._ttsEngines.Next(1,byref(mode),byref(fetched))
			except:
				log.error("can't get next engine",exc_info=True)
				break
			if fetched.value==0:
				break
			enginesList.append(mode)
		return enginesList

	def __init__(self):
		self.lastIndex=None
		self._bufSink=SynthDriverBufSink(self)
		self._ttsEngines=CoCreateInstance(CLSID_TTSEnumerator, ITTSEnumW)
		self._enginesList=self._fetchEnginesList()
		if len(self._enginesList)==0:
			raise RuntimeError("No Sapi4 engines available")
		self.voice=str(self._enginesList[0].gModeID)
	def performSpeak(self,text,index=None,isCharacter=False):
		flags=0
		if index is not None or isCharacter:
			text = text.replace('\\','\\\\')
			flags+=TTSDATAFLAG_TAGGED
		if index is not None:
			text="\mrk=%d\\%s"%(index,text)
		if isCharacter:
			text = "\\RmS=1\\%s\\RmS=0\\"%text
		self._ttsCentral.TextData(VOICECHARSET.CHARSET_TEXT, flags,TextSDATA(text),self._bufSink._com_pointers_[ITTSBufNotifySink._iid_],ITTSBufNotifySink._iid_)

	def speakText(self,text,index=None):
		self.performSpeak(text,index)

	def speakCharacter(self,character,index=None):
		self.performSpeak(character,index,isCharacter=True)

	def cancel(self):
		self._ttsCentral.AudioReset()

	def pause(self,switch):
		if switch:
			try:
				self._ttsCentral.AudioPause()
			except COMError:
				pass
		else:
			self._ttsCentral.AudioResume()

	def _set_voice(self,val):
		try:
			val=GUID(val)
		except:
			val=self._enginesList[0].gModeID
		mode=None
		for mode in self._enginesList:
			if mode.gModeID==val:
				break
		if mode is None:
			raise ValueError("no such mode: %s"%val)
		self._currentMode=mode
		self._ttsAudio=CoCreateInstance(CLSID_MMAudioDest,IAudioMultiMediaDevice)
		self._ttsAudio.DeviceNumSet(nvwave.outputDeviceNameToID(config.conf["speech"]["outputDevice"], True))
		self._ttsCentral=POINTER(ITTSCentralW)()
		self._ttsEngines.Select(self._currentMode.gModeID,byref(self._ttsCentral),self._ttsAudio)
		self._ttsAttrs=self._ttsCentral.QueryInterface(ITTSAttributes)
		#Find out rate limits
		self.hasRate=bool(mode.dwFeatures&TTSFEATURE_SPEED)
		if self.hasRate:
			try:
				oldVal=DWORD()
				self._ttsAttrs.SpeedGet(byref(oldVal))
				self._ttsAttrs.SpeedSet(TTSATTR_MINSPEED)
				newVal=DWORD()
				self._ttsAttrs.SpeedGet(byref(newVal))
				self._minRate=newVal.value
				self._ttsAttrs.SpeedSet(TTSATTR_MAXSPEED)
				self._ttsAttrs.SpeedGet(byref(newVal))
				# ViaVoice (and perhaps other synths) doesn't seem to like the speed being set to maximum.
				self._maxRate=newVal.value-1
				self._ttsAttrs.SpeedSet(oldVal.value)
				if self._maxRate<=self._minRate:
					self.hasRate=False
			except COMError:
				self.hasRate=False
		#Find out pitch limits
		self.hasPitch=bool(mode.dwFeatures&TTSFEATURE_PITCH)
		if self.hasPitch:
			try:
				oldVal=WORD()
				self._ttsAttrs.PitchGet(byref(oldVal))
				self._ttsAttrs.PitchSet(TTSATTR_MINPITCH)
				newVal=WORD()
				self._ttsAttrs.PitchGet(byref(newVal))
				self._minPitch=newVal.value
				self._ttsAttrs.PitchSet(TTSATTR_MAXPITCH)
				self._ttsAttrs.PitchGet(byref(newVal))
				self._maxPitch=newVal.value
				self._ttsAttrs.PitchSet(oldVal.value)
				if self._maxPitch<=self._minPitch:
					self.hasPitch=False
			except COMError:
				self.hasPitch=False
		#Find volume limits
		self.hasVolume=bool(mode.dwFeatures&TTSFEATURE_VOLUME)
		if self.hasVolume:
			try:
				oldVal=DWORD()
				self._ttsAttrs.VolumeGet(byref(oldVal))
				self._ttsAttrs.VolumeSet(TTSATTR_MINVOLUME)
				newVal=DWORD()
				self._ttsAttrs.VolumeGet(byref(newVal))
				self._minVolume=newVal.value
				self._ttsAttrs.VolumeSet(TTSATTR_MAXVOLUME)
				self._ttsAttrs.VolumeGet(byref(newVal))
				self._maxVolume=newVal.value
				self._ttsAttrs.VolumeSet(oldVal.value)
				if self._maxVolume<=self._minVolume:
					self.hasVolume=False
			except COMError:
				self.hasVolume=False

	def _get_voice(self):
		return str(self._currentMode.gModeID)

	def _getAvailableVoices(self):
		voices=[]
		for mode in self._enginesList:
			ID=str(mode.gModeID)
			name="%s - %s"%(mode.szModeName,mode.szProductName)
			voices.append(synthDriverHandler.VoiceInfo(ID,name))
		return voices

	def _get_rate(self):
		val=DWORD()
		self._ttsAttrs.SpeedGet(byref(val))
		return self._paramToPercent(val.value,self._minRate,self._maxRate)

	def _set_rate(self,val):
		val=self._percentToParam(val,self._minRate,self._maxRate)
		self._ttsAttrs.SpeedSet(val)

	def _get_pitch(self):
		val=WORD()
		self._ttsAttrs.PitchGet(byref(val))
		return self._paramToPercent(val.value,self._minPitch,self._maxPitch)

	def _set_pitch(self,val):
		val=self._percentToParam(val,self._minPitch,self._maxPitch)
		self._ttsAttrs.PitchSet(val)

	def _get_volume(self):
		val=DWORD()
		self._ttsAttrs.VolumeGet(byref(val))
		return self._paramToPercent(val.value&0xffff,self._minVolume&0xffff,self._maxVolume&0xffff)

	def _set_volume(self,val):
		val=self._percentToParam(val,self._minVolume&0xffff,self._maxVolume&0xffff)
		val+=val<<16
		self._ttsAttrs.VolumeSet(val)
