# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2025 NV Access Limited, Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# This module is deprecated, pending removal in NVDA 2026.1.

import locale
from collections import OrderedDict, deque
import winreg
from comtypes import CoCreateInstance, COMObject, COMError, GUID
from ctypes import byref, c_ulong, POINTER, c_wchar, create_string_buffer, sizeof, windll
from ctypes.wintypes import DWORD, HANDLE, WORD
from typing import Optional
from autoSettingsUtils.driverSetting import BooleanDriverSetting
import gui.contextHelp
import gui.message
import queueHandler
from synthDriverHandler import SynthDriver, VoiceInfo, synthIndexReached, synthDoneSpeaking, synthChanged
from logHandler import log
import warnings
from utils.security import isRunningOnSecureDesktop
from ._sapi4 import (
	MMSYSERR_NOERROR,
	CLSID_MMAudioDest,
	CLSID_TTSEnumerator,
	IAudioMultiMediaDevice,
	ITTSAttributes,
	ITTSBufNotifySink,
	ITTSCentralW,
	ITTSEnumW,
	ITTSNotifySinkW,
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
	VOICECHARSET,
	DriverMessage,
)
import config
import weakref

from speech.commands import (
	IndexCommand,
	SpeechCommand,
	CharacterModeCommand,
	BreakCommand,
	PitchCommand,
	RateCommand,
	VolumeCommand,
	BaseProsodyCommand,
)
from speech.types import SpeechSequence


warnings.warn("synthDrivers.sapi4 is deprecated, pending removal in NVDA 2026.1.", DeprecationWarning)


class SynthDriverBufSink(COMObject):
	_com_interfaces_ = [ITTSBufNotifySink]

	def __init__(self, synthRef: weakref.ReferenceType):
		self.synthRef = synthRef
		self._allowDelete = True
		super().__init__()

	def ITTSBufNotifySink_BookMark(self, this, qTimeStamp: int, dwMarkNum: int):
		synth = self.synthRef()
		if synth is None:
			log.debugWarning(
				"Called ITTSBufNotifySink_BookMark method on ITTSBufNotifySink while driver is dead",
			)
			return
		synthIndexReached.notify(synth=synth, index=dwMarkNum)
		if synth._finalIndex == dwMarkNum:
			synth._finalIndex = None
			synthDoneSpeaking.notify(synth=synth)
		# remove already triggered bookmarks
		while synth._bookmarks:
			if synth._bookmarks.popleft() == dwMarkNum:
				break

	def IUnknown_Release(self, this, *args, **kwargs):
		if not self._allowDelete and self._refcnt.value == 1:
			log.debugWarning("ITTSBufNotifySink::Release called too many times by engine")
			return 1
		return super(SynthDriverBufSink, self).IUnknown_Release(this, *args, **kwargs)


class SynthDriverSink(COMObject):
	_com_interfaces_ = [ITTSNotifySinkW]

	def __init__(self, synthRef: weakref.ReferenceType):
		self.synthRef = synthRef
		super().__init__()

	def ITTSNotifySinkW_AudioStart(self, this, qTimeStamp: int):
		synth = self.synthRef()
		if synth is None:
			log.debugWarning(
				"Called ITTSNotifySinkW_AudioStart method on ITTSNotifySinkW while driver is dead",
			)
			return
		if synth._bookmarkLists:
			# take the first bookmark list
			synth._bookmarks = synth._bookmarkLists.popleft()

	def ITTSNotifySinkW_AudioStop(self, this, qTimeStamp: int):
		synth = self.synthRef()
		if synth is None:
			log.debugWarning(
				"Called ITTSNotifySinkW_AudioStop method on ITTSNotifySinkW while driver is dead",
			)
			return
		# trigger all untriggered bookmarks
		if synth._bookmarks:
			while synth._bookmarks:
				synthIndexReached.notify(synth=synth, index=synth._bookmarks.popleft())
			# if there are untriggered bookmarks, synthDoneSpeaking hasn't been triggered yet.
			# Trigger synthDoneSpeaking after triggering all bookmarks
			synth._finalIndex = None
			synthDoneSpeaking.notify(synth=synth)
		synth._bookmarks = None


class SynthDriver(SynthDriver):
	name = "sapi4"
	description = "Microsoft Speech API version 4"
	supportedSettings = [
		SynthDriver.VoiceSetting(),
		BooleanDriverSetting("_hasWarningBeenShown", ""),
	]
	supportedCommands = {
		IndexCommand,
		CharacterModeCommand,
		BreakCommand,
	}
	supportedNotifications = {synthIndexReached, synthDoneSpeaking}

	@classmethod
	def check(cls):
		try:
			winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"CLSID\%s" % CLSID_TTSEnumerator).Close()
			return True
		except WindowsError:
			return False

	def _fetchEnginesList(self):
		enginesList = []
		self._ttsEngines.Reset()
		while True:
			mode = TTSMODEINFO()
			fetched = c_ulong()
			try:
				self._ttsEngines.Next(1, byref(mode), byref(fetched))
			except:  # noqa: E722
				log.error("can't get next engine", exc_info=True)
				break
			if fetched.value == 0:
				break
			enginesList.append(mode)
		return enginesList

	def __init__(self):
		self._finalIndex: Optional[int] = None
		self._ttsCentral = None
		self._sinkRegKey = DWORD()
		self._bookmarks = None
		self._bookmarkLists = deque()
		self._sink = SynthDriverSink(weakref.ref(self))
		self._sinkPtr = self._sink.QueryInterface(ITTSNotifySinkW)
		self._bufSink = SynthDriverBufSink(weakref.ref(self))
		self._bufSinkPtr = self._bufSink.QueryInterface(ITTSBufNotifySink)
		# HACK: Some buggy engines call Release() too many times on our buf sink.
		# Therefore, don't let the buf sink be deleted before we release it ourselves.
		self._bufSink._allowDelete = False
		self._ttsEngines = CoCreateInstance(CLSID_TTSEnumerator, ITTSEnumW)
		self._enginesList = self._fetchEnginesList()
		if len(self._enginesList) == 0:
			raise RuntimeError("No Sapi4 engines available")
		self._rateDelta = 0
		self._pitchDelta = 0
		self._volume = 100
		self._paused = False
		self.voice = str(self._enginesList[0].gModeID)

	def terminate(self):
		self._bufSink._allowDelete = True

	def speak(self, speechSequence: SpeechSequence):
		textList = []
		charMode = False
		unprocessedSequence = speechSequence
		bookmarks = deque()
		# #15500: Some SAPI4 voices reset all prosody when they receive any prosody command,
		# whereas other voices never undo prosody changes when a sequence is interrupted.
		# Add all default values to the start and end of the sequence,
		# but avoid duplicating the first command, if any,
		# And only add the defaults when there is a prosody command in the sequence.
		supportedProsody = [c for c in self.supportedCommands if issubclass(c, BaseProsodyCommand)]
		prosodyToAdd = []
		if any(type(i) in supportedProsody for i in unprocessedSequence):
			prosodyToAdd.extend(c() for c in supportedProsody)
		speechSequence = [c for c in prosodyToAdd if not isinstance(unprocessedSequence[0], type(c))]
		speechSequence.extend(unprocessedSequence)
		# To be sure, add all default values to the end of the sequence.
		# This might cause multiple cases of prosody resets, but better safe than sorry.
		speechSequence.extend(prosodyToAdd)
		lastHandledIndexInSequence = 0
		for item in speechSequence:
			if isinstance(item, str):
				textList.append(item.replace("\\", "\\\\"))
			elif isinstance(item, IndexCommand):
				textList.append("\\mrk=%d\\" % item.index)
				bookmarks.append(item.index)
				lastHandledIndexInSequence = item.index
			elif isinstance(item, CharacterModeCommand):
				textList.append("\\RmS=1\\" if item.state else "\\RmS=0\\")
				charMode = item.state
			elif isinstance(item, BreakCommand):
				textList.append(f"\\Pau={item.time}\\")
			elif isinstance(item, PitchCommand):
				val = self._percentToParam(item.newValue, self._minPitch, self._maxPitch)
				textList.append(f"\\Pit={val}\\")
			elif isinstance(item, RateCommand):
				val = self._percentToParam(item.newValue, self._minRate, self._maxRate)
				textList.append(f"\\Spd={val}\\")
			elif isinstance(item, VolumeCommand):
				val = self._percentToParam(item.newValue, self._minVolume, self._maxVolume)
				# If you specify a value greater than 65535, the engine assumes that you want to set the
				# left and right channels separately and converts the value to a double word,
				# using the low word for the left channel and the high word for the right channel.
				val |= val << 16
				textList.append(f"\\Vol={val}\\")
			elif isinstance(item, SpeechCommand):
				log.debugWarning("Unsupported speech command: %s" % item)
			else:
				log.error("Unknown speech: %s" % item)
		# lastHandledIndexInSequence is the index denoting the end of the speech sequence.
		# store it on the driver to support the synthDoneSpeaking notification.
		self._finalIndex = lastHandledIndexInSequence
		if charMode:
			# Some synths stay in character mode if we don't explicitly disable it.
			textList.append("\\RmS=0\\")
		# Some SAPI4 synthesizers complete speech sequence just after the last text
		# and ignore any indexes passed after it
		# Therefore we add the pause of 1ms at the end
		textList.append("\\PAU=1\\")
		text = "".join(textList)
		self._bookmarkLists.append(bookmarks)
		flags = TTSDATAFLAG_TAGGED
		self._ttsCentral.TextData(
			VOICECHARSET.CHARSET_TEXT,
			flags,
			TextSDATA(text),
			self._bufSinkPtr,
			ITTSBufNotifySink._iid_,
		)

	def cancel(self):
		try:
			# cancel all pending bookmarks
			self._bookmarkLists.clear()
			self._bookmarks = None
			if self._paused:
				# Unpause the voice before resetting,
				# because some voices keep the pausing state
				# even after resetting.
				self._ttsCentral.AudioResume()
				self._paused = False
			self._ttsCentral.AudioReset()
		except COMError:
			log.error("Error cancelling speech", exc_info=True)
		finally:
			self._finalIndex = None

	def pause(self, switch: bool):
		if switch:
			try:
				self._ttsCentral.AudioPause()
			except COMError:
				log.debugWarning("Error pausing speech", exc_info=True)
		else:
			self._ttsCentral.AudioResume()
		self._paused = switch

	def removeSetting(self, name):
		# Putting it here because currently no other synths make use of it. OrderedDict, where you are?
		for i, s in enumerate(self.supportedSettings):
			if s.id == name:
				del self.supportedSettings[i]
				return

	def _set_voice(self, val):
		try:
			val = GUID(val)
		except:  # noqa: E722
			val = self._enginesList[0].gModeID
		mode = None
		for mode in self._enginesList:
			if mode.gModeID == val:
				break
		if mode is None:
			raise ValueError("no such mode: %s" % val)
		self._currentMode = mode
		self._ttsAudio = CoCreateInstance(CLSID_MMAudioDest, IAudioMultiMediaDevice)
		self._ttsAudio.DeviceNumSet(_mmDeviceEndpointIdToWaveOutId(config.conf["audio"]["outputDevice"]))
		if self._ttsCentral:
			try:
				# Some SAPI4 synthesizers may fail this call.
				# Ignore, as _ttsCentral will be destroyed afterwards.
				self._ttsCentral.UnRegister(self._sinkRegKey)
			except COMError:
				pass
			# Some SAPI4 synthesizers assume that only one instance of ITTSCentral
			# will be created by the client, and will stop working if more are created.
			# Here we make sure that the previous _ttsCentral is released
			# before the next _ttsCentral is created.
			self._ttsCentral = None
			self._ttsAttrs = None
		self._ttsCentral = POINTER(ITTSCentralW)()
		self._ttsEngines.Select(self._currentMode.gModeID, byref(self._ttsCentral), self._ttsAudio)
		self._ttsCentral.Register(self._sinkPtr, ITTSNotifySinkW._iid_, byref(self._sinkRegKey))
		self._ttsAttrs = self._ttsCentral.QueryInterface(ITTSAttributes)
		# Find out rate limits
		hasRate = bool(mode.dwFeatures & TTSFEATURE_SPEED)
		if hasRate:
			try:
				oldVal = DWORD()
				self._ttsAttrs.SpeedGet(byref(oldVal))
				self._defaultRate = oldVal.value
				self._ttsAttrs.SpeedSet(TTSATTR_MINSPEED)
				newVal = DWORD()
				self._ttsAttrs.SpeedGet(byref(newVal))
				self._minRate = newVal.value
				self._ttsAttrs.SpeedSet(TTSATTR_MAXSPEED)
				self._ttsAttrs.SpeedGet(byref(newVal))
				# ViaVoice (and perhaps other synths) doesn't seem to like the speed being set to maximum.
				self._maxRate = newVal.value - 1
				val = max(self._minRate, min(self._maxRate, self._defaultRate + self._rateDelta))
				self._ttsAttrs.SpeedSet(val)
				if self._maxRate <= self._minRate:
					hasRate = False
			except COMError:
				hasRate = False
		if hasRate:
			if not self.isSupported("rate"):
				self.supportedSettings.insert(1, SynthDriver.RateSetting())
			self.supportedCommands.add(RateCommand)
		else:
			if self.isSupported("rate"):
				self.removeSetting("rate")
			if RateCommand in self.supportedCommands:
				self.supportedCommands.remove(RateCommand)
		# Find out pitch limits
		hasPitch = bool(mode.dwFeatures & TTSFEATURE_PITCH)
		if hasPitch:
			try:
				oldVal = WORD()
				self._ttsAttrs.PitchGet(byref(oldVal))
				self._defaultPitch = oldVal.value
				self._ttsAttrs.PitchSet(TTSATTR_MINPITCH)
				newVal = WORD()
				self._ttsAttrs.PitchGet(byref(newVal))
				self._minPitch = newVal.value
				self._ttsAttrs.PitchSet(TTSATTR_MAXPITCH)
				self._ttsAttrs.PitchGet(byref(newVal))
				self._maxPitch = newVal.value
				val = max(self._minPitch, min(self._maxPitch, self._defaultPitch + self._pitchDelta))
				self._ttsAttrs.PitchSet(val)
				if self._maxPitch <= self._minPitch:
					hasPitch = False
			except COMError:
				hasPitch = False
		if hasPitch:
			if not self.isSupported("pitch"):
				self.supportedSettings.insert(2, SynthDriver.PitchSetting())
			self.supportedCommands.add(PitchCommand)
		else:
			if self.isSupported("pitch"):
				self.removeSetting("pitch")
			if PitchCommand in self.supportedCommands:
				self.supportedCommands.remove(PitchCommand)
		# Find volume limits
		hasVolume = bool(mode.dwFeatures & TTSFEATURE_VOLUME)
		if hasVolume:
			try:
				oldVal = DWORD()
				self._ttsAttrs.VolumeGet(byref(oldVal))
				self._ttsAttrs.VolumeSet(TTSATTR_MINVOLUME)
				newVal = DWORD()
				self._ttsAttrs.VolumeGet(byref(newVal))
				self._minVolume = newVal.value & 0xFFFF
				self._ttsAttrs.VolumeSet(TTSATTR_MAXVOLUME)
				self._ttsAttrs.VolumeGet(byref(newVal))
				self._maxVolume = newVal.value & 0xFFFF
				self._set_volume(self._volume)
				if self._maxVolume <= self._minVolume:
					hasVolume = False
			except COMError:
				hasVolume = False
		if hasVolume:
			if not self.isSupported("volume"):
				self.supportedSettings.insert(3, SynthDriver.VolumeSetting())
			self.supportedCommands.add(VolumeCommand)
		else:
			if self.isSupported("volume"):
				self.removeSetting("volume")
			if VolumeCommand in self.supportedCommands:
				self.supportedCommands.remove(VolumeCommand)

	def _get_voice(self):
		return str(self._currentMode.gModeID)

	def _getAvailableVoices(self):
		voices = OrderedDict()
		for mode in self._enginesList:
			ID = str(mode.gModeID)
			name = "%s - %s" % (mode.szModeName, mode.szProductName)
			try:
				language = locale.windows_locale[mode.language.LanguageID]
			except KeyError:
				language = None
			voices[ID] = VoiceInfo(ID, name, language)
		return voices

	def _get_rate(self) -> int:
		val = DWORD()
		self._ttsAttrs.SpeedGet(byref(val))
		return self._paramToPercent(val.value, self._minRate, self._maxRate)

	def _set_rate(self, val: int):
		val = self._percentToParam(val, self._minRate, self._maxRate)
		self._ttsAttrs.SpeedSet(val)
		self._rateDelta = val - self._defaultRate

	def _get_pitch(self) -> int:
		val = WORD()
		self._ttsAttrs.PitchGet(byref(val))
		return self._paramToPercent(val.value, self._minPitch, self._maxPitch)

	def _set_pitch(self, val: int):
		val = self._percentToParam(val, self._minPitch, self._maxPitch)
		self._ttsAttrs.PitchSet(val)
		self._pitchDelta = val - self._defaultPitch

	def _get_volume(self) -> int:
		val = DWORD()
		self._ttsAttrs.VolumeGet(byref(val))
		return self._paramToPercent(val.value & 0xFFFF, self._minVolume, self._maxVolume)

	def _set_volume(self, val: int):
		self._volume = val
		val = self._percentToParam(val, self._minVolume, self._maxVolume)
		# If you specify a value greater than 65535, the engine assumes that you want to set the
		# left and right channels separately and converts the value to a double word,
		# using the low word for the left channel and the high word for the right channel.
		val |= val << 16
		self._ttsAttrs.VolumeSet(val)


def _mmDeviceEndpointIdToWaveOutId(targetEndpointId: str) -> int:
	"""Translate from an MMDevice Endpoint ID string to a WaveOut Device ID number.

	:param targetEndpointId: MMDevice endpoint ID string to translate from, or the default value of the `audio.outputDevice` configuration key for the default output device.
	:return: An integer WaveOut device ID for use with SAPI4.
		If no matching device is found, or the default output device is requested, `-1` is returned, which means output will be handled by Microsoft Sound Mapper.
	"""
	if targetEndpointId != config.conf.getConfigValidation(("audio", "outputDevice")).default:
		targetEndpointIdByteCount = (len(targetEndpointId) + 1) * sizeof(c_wchar)
		currEndpointId = create_string_buffer(targetEndpointIdByteCount)
		currEndpointIdByteCount = DWORD()
		# Defined in mmeapi.h
		winmm = windll.winmm
		waveOutMessage = winmm.waveOutMessage
		waveOutGetNumDevs = winmm.waveOutGetNumDevs
		for devID in range(waveOutGetNumDevs()):
			# Get the length of this device's endpoint ID string.
			mmr = waveOutMessage(
				HANDLE(devID),
				DriverMessage.QUERY_INSTANCE_ID_SIZE,
				byref(currEndpointIdByteCount),
				None,
			)
			if (mmr != MMSYSERR_NOERROR) or (currEndpointIdByteCount.value != targetEndpointIdByteCount):
				# ID lengths don't match, so this device can't be a match.
				continue
			# Get the device's endpoint ID string.
			mmr = waveOutMessage(
				HANDLE(devID),
				DriverMessage.QUERY_INSTANCE_ID,
				byref(currEndpointId),
				currEndpointIdByteCount,
			)
			if mmr != MMSYSERR_NOERROR:
				continue
			# Decode the endpoint ID string to a python string, and strip the null terminator.
			if (
				currEndpointId.raw[: targetEndpointIdByteCount - sizeof(c_wchar)].decode("utf-16")
				== targetEndpointId
			):
				return devID
	# No matching device found, or default requested explicitly.
	# Return the ID of Microsoft Sound Mapper
	return -1


def _sapi4DeprecationWarning(synth: SynthDriver, audioOutputDevice: str, isFallback: bool):
	"""A synthChanged event handler to alert the user about the deprecation of SAPI4."""

	def setShown(payload: gui.message.Payload):
		synth._hasWarningBeenShown = True
		synth.saveSettings()

	def impl():
		gui.message.MessageDialog(
			parent=None,
			message=_(
				# Translators: Message warning users that SAPI4 is deprecated.
				"Microsoft Speech API version 4 is obsolete. "
				"Using this speech synthesizer may pose a security risk. "
				"This synthesizer driver will be removed in NVDA 2026.1. "
				"You are strongly encouraged to choose a more modern speech synthesizer. "
				"Consult the Supported Speech Synthesizers section in the User Guide for suggestions. ",
			),
			# Translators: Title of a message dialog.
			title=_("Warning"),
			buttons=None,
		).addOkButton(
			callback=setShown,
		).addHelpButton(
			# Translators: A button in a dialog.
			label=_("Open user guide"),
			callback=lambda payload: gui.contextHelp.showHelp("SupportedSpeechSynths"),
		).Show()

	if (not isFallback) and (synth.name == "sapi4") and (not getattr(synth, "_hasWarningBeenShown", False)):
		# We need to queue the dialog to appear, as wx may not have been initialised the first time this is called.
		queueHandler.queueFunction(queueHandler.eventQueue, impl)


if not isRunningOnSecureDesktop():
	# Don't warn users about SAPI4 deprecation when running on a secure desktop.
	synthChanged.register(_sapi4DeprecationWarning)
