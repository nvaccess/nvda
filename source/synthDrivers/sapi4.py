#synthDrivers/sapi4.py
#A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2020 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import locale
from collections import OrderedDict
import winreg
from comtypes import CoCreateInstance, COMObject, COMError, GUID
from ctypes import byref, c_ulong, POINTER
from ctypes.wintypes import DWORD, WORD
from synthDriverHandler import SynthDriver,VoiceInfo, synthIndexReached, synthDoneSpeaking
from logHandler import log
from ._sapi4 import (
	CLSID_MMAudioDest,
	CLSID_TTSEnumerator,
	IAudioMultiMediaDevice,
	ITTSAttributes,
	ITTSBufNotifySink,
	ITTSCentralW,
	ITTSEnumW,
	TextSDATA,
	TTSATTR_MAXPITCH,
	TTSATTR_MAXSPEED,
	TTSATTR_MAXVOLUME,
	TTSATTR_MINPITCH,
	TTSATTR_MINSPEED,
	TTSATTR_MINVOLUME,
	TTSDATAFLAG_TAGGED,
	TTSFEATURE_PITCH,
	TTSFEATURE_SPEED,
	TTSFEATURE_VOLUME,
	TTSMODEINFO,
	VOICECHARSET
)
import config
import nvwave
import weakref

from speech.commands import PitchCommand
from speech.commands import IndexCommand, SpeechCommand, CharacterModeCommand

class SynthDriverBufSink(COMObject):
	_com_interfaces_ = [ITTSBufNotifySink]

	def __init__(self, synthRef: weakref.ReferenceType):
		self.synthRef = synthRef
		self._allowDelete = True
		super(SynthDriverBufSink,self).__init__()

	def ITTSBufNotifySink_BookMark(self, this, qTimeStamp, dwMarkNum):
		synth = self.synthRef()
		if synth is None:
			log.debugWarning("Called ITTSBufNotifySink_BookMark method on ITTSBufNotifySink while driver is dead")
			return
		synthIndexReached.notify(synth=synth, index=dwMarkNum)
		if synth._finalIndex == dwMarkNum:
			synth._finalIndex = None
			synthDoneSpeaking.notify(synth=synth)

	def IUnknown_Release(self, this, *args, **kwargs):
		if not self._allowDelete and self._refcnt.value == 1:
			log.debugWarning("ITTSBufNotifySink::Release called too many times by engine")
			return 1
		return super(SynthDriverBufSink, self).IUnknown_Release(this, *args, **kwargs)

class SynthDriver(SynthDriver):

	name="sapi4"
	description="Microsoft Speech API version 4"
	supportedSettings=[SynthDriver.VoiceSetting()]
	supportedNotifications={synthIndexReached,synthDoneSpeaking}

	@classmethod
	def check(cls):
		try:
			winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"CLSID\%s" % CLSID_TTSEnumerator).Close()
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
		self._finalIndex=None
		self._bufSink = SynthDriverBufSink(weakref.ref(self))
		self._bufSinkPtr=self._bufSink.QueryInterface(ITTSBufNotifySink)
		# HACK: Some buggy engines call Release() too many times on our buf sink.
		# Therefore, don't let the buf sink be deleted before we release it ourselves.
		self._bufSink._allowDelete=False
		self._ttsEngines=CoCreateInstance(CLSID_TTSEnumerator, ITTSEnumW)
		self._enginesList=self._fetchEnginesList()
		if len(self._enginesList)==0:
			raise RuntimeError("No Sapi4 engines available")
		self.voice=str(self._enginesList[0].gModeID)

	def terminate(self):
		self._bufSink._allowDelete = True

	def speak(self,speechSequence):
		textList=[]
		charMode=False
		item=None
		isPitchCommand = False
		pitch = WORD()
		self._ttsAttrs.PitchGet(byref(pitch))
		oldPitch = pitch.value

		for item in speechSequence:
			if isinstance(item,str):
				textList.append(item.replace('\\','\\\\'))
			elif isinstance(item, IndexCommand):
				textList.append("\\mrk=%d\\"%item.index)
			elif isinstance(item, CharacterModeCommand):
				textList.append("\\RmS=1\\" if item.state else "\\RmS=0\\")
				charMode=item.state
			elif isinstance(item, PitchCommand):
				offset = int(config.conf["speech"]['sapi4']["capPitchChange"])
				offset = int((self._maxPitch - self._minPitch) * offset / 100)
				val = oldPitch + offset
				if val > self._maxPitch:
					val = self._maxPitch
				if val < self._minPitch:
					val = self._minPitch
				self._ttsAttrs.PitchSet(val)
				isPitchCommand = True
			elif isinstance(item, SpeechCommand):
				log.debugWarning("Unsupported speech command: %s"%item)
			else:
				log.error("Unknown speech: %s"%item)
		if isinstance(item, IndexCommand):
			# This is the index denoting the end of the speech sequence.
			self._finalIndex=item.index
		if charMode:
			# Some synths stay in character mode if we don't explicitly disable it.
			textList.append("\\RmS=0\\")
		# Some SAPI4 synthesizers complete speech sequence just after the last text
		# and ignore any indexes passed after it
		# Therefore we add the pause of 1ms at the end
		textList.append("\\PAU=1\\")
		text="".join(textList)
		flags=TTSDATAFLAG_TAGGED
		if isPitchCommand:
			self._ttsCentral.TextData(
				VOICECHARSET.CHARSET_TEXT,
				flags,
				TextSDATA(text),
				self._bufSinkPtr,
				ITTSBufNotifySink._iid_
			)
			self._ttsAttrs.PitchSet(oldPitch)
			isPitchCommand = False
		else:
			self._ttsCentral.TextData(
				VOICECHARSET.CHARSET_TEXT,
				flags,
				TextSDATA(text),
				self._bufSinkPtr,
				ITTSBufNotifySink._iid_
			)

	def cancel(self):
		self._ttsCentral.AudioReset()
		self.lastIndex=None

	def pause(self,switch):
		if switch:
			try:
				self._ttsCentral.AudioPause()
			except COMError:
				pass
		else:
			self._ttsCentral.AudioResume()

	def removeSetting(self,name):
		#Putting it here because currently no other synths make use of it. OrderedDict, where you are?
		for i,s in enumerate(self.supportedSettings):
			if s.name==name:
				del self.supportedSettings[i]
				return

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
		hasRate=bool(mode.dwFeatures&TTSFEATURE_SPEED)
		if hasRate:
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
					hasRate=False
			except COMError:
				hasRate=False
		if hasRate:
			if not self.isSupported('rate'):
				self.supportedSettings.insert(1,SynthDriver.RateSetting())
		else:
			if self.isSupported("rate"): self.removeSetting("rate")
		#Find out pitch limits
		hasPitch=bool(mode.dwFeatures&TTSFEATURE_PITCH)
		if hasPitch:
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
					hasPitch=False
			except COMError:
				hasPitch=False
		if hasPitch:
			if not self.isSupported('pitch'):
				self.supportedSettings.insert(2,SynthDriver.PitchSetting())
		else:
			if self.isSupported('pitch'): self.removeSetting('pitch')
		#Find volume limits
		hasVolume=bool(mode.dwFeatures&TTSFEATURE_VOLUME)
		if hasVolume:
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
					hasVolume=False
			except COMError:
				hasVolume=False
		if hasVolume:
			if not self.isSupported('volume'):
				self.supportedSettings.insert(3,SynthDriver.VolumeSetting())
		else:
			if self.isSupported('volume'): self.removeSetting('volume')

	def _get_voice(self):
		return str(self._currentMode.gModeID)

	def _getAvailableVoices(self):
		voices=OrderedDict()
		for mode in self._enginesList:
			ID=str(mode.gModeID)
			name="%s - %s"%(mode.szModeName,mode.szProductName)
			try:
				language=locale.windows_locale[mode.language.LanguageID]
			except KeyError:
				language=None
			voices[ID]=VoiceInfo(ID,name,language)
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
