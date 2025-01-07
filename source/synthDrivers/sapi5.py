# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2024 NV Access Limited, Peter Vágner, Aleksey Sadovoy
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from ctypes import POINTER, c_wchar_p, cast, windll
from typing import Optional
from enum import IntEnum
import locale
from collections import OrderedDict
from comInterfaces.SpeechLib import ISpEventSource, ISpNotifySource, ISpNotifySink
import comtypes.client
from comtypes import COMError, COMObject, IUnknown, hresult
import winreg
import nvwave
from objidl import IStream
from synthDriverHandler import SynthDriver, VoiceInfo, synthIndexReached, synthDoneSpeaking
import config
from logHandler import log
import weakref
import languageHandler

from speech.commands import (
	IndexCommand,
	CharacterModeCommand,
	LangChangeCommand,
	BreakCommand,
	PitchCommand,
	RateCommand,
	VolumeCommand,
	PhonemeCommand,
	SpeechCommand,
)


class SPAudioState(IntEnum):
	# https://docs.microsoft.com/en-us/previous-versions/windows/desktop/ms720596(v=vs.85)
	CLOSED = 0
	STOP = 1
	PAUSE = 2
	RUN = 3


class SpeechVoiceSpeakFlags(IntEnum):
	# https://docs.microsoft.com/en-us/previous-versions/windows/desktop/ms720892(v=vs.85)
	Async = 1
	PurgeBeforeSpeak = 2
	IsXML = 8


class SpeechVoiceEvents(IntEnum):
	# https://msdn.microsoft.com/en-us/previous-versions/windows/desktop/ms720886(v=vs.85)
	StartInputStream = 2
	EndInputStream = 4
	Bookmark = 16


class SynthDriverAudioStream(COMObject):
	"""
	Implements IStream to receive streamed-in audio data.
	Should be wrapped in an SpCustomStream
	(which also provides the wave format information),
	then set as the AudioOutputStream.
	"""

	_com_interfaces_ = [IStream]

	def __init__(self, synthRef: weakref.ReferenceType):
		self.synthRef = synthRef
		self._writtenBytes = 0

	def ISequentialStream_RemoteWrite(self, this, pv, cb, pcbWritten):
		synth = self.synthRef()
		if synth is None:
			log.debugWarning("Called Write method on AudioStream while driver is dead")
			return
		if not synth.isSpeaking:
			return
		synth.player.feed(pv, cb)
		self._writtenBytes += cb
		if pcbWritten:
			pcbWritten[0] = cb
		return 0

	def IStream_RemoteSeek(self, this, dlibMove, dwOrigin, plibNewPosition):
		if dwOrigin == 1 and dlibMove.QuadPart == 0:
			# SAPI is querying the current position.
			if plibNewPosition:
				plibNewPosition[0].QuadPart = self._writtenBytes
				return 0
		return hresult.E_NOTIMPL

	def IStream_Commit(self, this, grfCommitFlags):
		# SAPI5 voices don't need this method, but MSSP voices do,
		# which use this method to "flush" written data.
		# Here we do nothing.
		return 0


class SapiSink(COMObject):
	"""
	Implements ISpNotifySink to handle SAPI event notifications.
	Should be passed to ISpNotifySource::SetNotifySink().
	Notifications will be sent on the original thread,
	instead of being routed to the main thread.
	"""

	_com_interfaces_ = [ISpNotifySink]

	def __init__(self, synthRef: weakref.ReferenceType):
		self.synthRef = synthRef

	def ISpNotifySink_Notify(self, this):
		synth = self.synthRef()
		if synth is None:
			log.debugWarning("Called Notify method on SapiSink while driver is dead")
			return
		# Get all queued events
		eventSource = synth.tts.QueryInterface(ISpEventSource)
		while True:
			# returned tuple: (event, numFetched)
			eventTuple = eventSource.GetEvents(1)  # Get one event
			if eventTuple[1] != 1:
				break
			event = eventTuple[0]
			if event.eEventId == 1:  # SPEI_START_INPUT_STREAM
				self.StartStream(event.ulStreamNum, event.ullAudioStreamOffset)
			elif event.eEventId == 2:  # SPEI_END_INPUT_STREAM
				self.EndStream(event.ulStreamNum, event.ullAudioStreamOffset)
			elif event.eEventId == 4:  # SPEI_TTS_BOOKMARK
				self.Bookmark(
					event.ulStreamNum,
					event.ullAudioStreamOffset,
					cast(event.lParam, c_wchar_p).value,
					event.wParam,
				)
			# free lParam
			if event.elParamType == 1 or event.elParamType == 2:  # token or object
				pUnk = cast(event.lParam, POINTER(IUnknown))
				del pUnk
			elif event.elParamType == 3 or event.elParamType == 4:  # pointer or string
				windll.ole32.CoTaskMemFree(event.lParam)

	def StartStream(self, streamNum, pos):
		synth = self.synthRef()
		synth.isSpeaking = True

	def Bookmark(self, streamNum, pos, bookmark, bookmarkId):
		synth = self.synthRef()
		if not synth.isSpeaking:
			return
		# Bookmark event is raised before the audio after that point.
		# Queue an IndexReached event at this point.
		synth.player.feed(None, 0, lambda: self.onIndexReached(bookmarkId))

	def EndStream(self, streamNum, pos):
		synth = self.synthRef()
		synth.isSpeaking = False
		synth.player.idle()
		synthDoneSpeaking.notify(synth=synth)

	def onIndexReached(self, index):
		synth = self.synthRef()
		if synth is None:
			log.debugWarning("Called onIndexReached method on SapiSink while driver is dead")
			return
		synthIndexReached.notify(synth=synth, index=index)


class SynthDriver(SynthDriver):
	supportedSettings = (
		SynthDriver.VoiceSetting(),
		SynthDriver.RateSetting(),
		SynthDriver.PitchSetting(),
		SynthDriver.VolumeSetting(),
	)
	supportedCommands = {
		IndexCommand,
		CharacterModeCommand,
		LangChangeCommand,
		BreakCommand,
		PitchCommand,
		RateCommand,
		VolumeCommand,
		PhonemeCommand,
	}
	supportedNotifications = {synthIndexReached, synthDoneSpeaking}

	COM_CLASS = "SAPI.SPVoice"
	CUSTOMSTREAM_COM_CLASS = "SAPI.SpCustomStream"

	name = "sapi5"
	description = "Microsoft Speech API version 5"

	@classmethod
	def check(cls):
		try:
			r = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, cls.COM_CLASS)
			r.Close()
			return True
		except:  # noqa: E722
			return False

	def __init__(self, _defaultVoiceToken=None):
		"""
		@param _defaultVoiceToken: an optional sapi voice token which should be used as the default voice (only useful for subclasses)
		@type _defaultVoiceToken: ISpeechObjectToken
		"""
		self._pitch = 50
		self.player = None
		self.isSpeaking = False
		self._initTts(_defaultVoiceToken)

	def terminate(self):
		self.tts = None
		if self.player:
			self.player.close()
			self.player = None

	def _getAvailableVoices(self):
		voices = OrderedDict()
		v = self._getVoiceTokens()
		# #2629: Iterating uses IEnumVARIANT and GetBestInterface doesn't work on tokens returned by some token enumerators.
		# Therefore, fetch the items by index, as that method explicitly returns the correct interface.
		for i in range(len(v)):
			try:
				ID = v[i].Id
				name = v[i].GetDescription()
				try:
					language = locale.windows_locale[int(v[i].getattribute("language").split(";")[0], 16)]
				except KeyError:
					language = None
			except COMError:
				log.warning("Could not get the voice info. Skipping...")
			voices[ID] = VoiceInfo(ID, name, language)
		return voices

	def _getVoiceTokens(self):
		"""Provides a collection of sapi5 voice tokens. Can be overridden by subclasses if tokens should be looked for in some other registry location."""
		return self.tts.getVoices()

	def _get_rate(self):
		return (self.tts.rate * 5) + 50

	def _get_pitch(self):
		return self._pitch

	def _get_volume(self) -> int:
		return self.tts.volume

	def _get_voice(self):
		return self.tts.voice.Id

	def _get_lastIndex(self):
		bookmark = self.tts.status.LastBookmark
		if bookmark != "" and bookmark is not None:
			return int(bookmark)
		else:
			return None

	def _percentToRate(self, percent):
		return (percent - 50) // 5

	def _set_rate(self, rate):
		self.tts.Rate = self._percentToRate(rate)

	def _set_pitch(self, value):
		# pitch is really controled with xml around speak commands
		self._pitch = value

	def _set_volume(self, value):
		self.tts.Volume = value

	def _initTts(self, voice=None):
		self.tts = comtypes.client.CreateObject(self.COM_CLASS)
		if voice:
			# #749: It seems that SAPI 5 doesn't reset the audio parameters when the voice is changed,
			# but only when the audio output is changed.
			# Therefore, set the voice before setting the audio output.
			# Otherwise, we will get poor speech quality in some cases.
			self.tts.voice = voice

		self.tts.AudioOutput = self.tts.AudioOutput  # Reset the audio and its format parameters
		fmt = self.tts.AudioOutputStream.Format
		wfx = fmt.GetWaveFormatEx()
		if self.player:
			self.player.close()
		self.player = nvwave.WavePlayer(
			channels=wfx.Channels,
			samplesPerSec=wfx.SamplesPerSec,
			bitsPerSample=wfx.BitsPerSample,
			outputDevice=config.conf["audio"]["outputDevice"],
		)
		audioStream = SynthDriverAudioStream(weakref.ref(self))
		# Use SpCustomStream to wrap our IStream implementation and the correct wave format
		customStream = comtypes.client.CreateObject(self.CUSTOMSTREAM_COM_CLASS)
		customStream.BaseStream = audioStream
		customStream.Format = fmt
		self.tts.AudioOutputStream = customStream

		# Set event notify sink
		self.tts.EventInterests = (
			SpeechVoiceEvents.StartInputStream | SpeechVoiceEvents.Bookmark | SpeechVoiceEvents.EndInputStream
		)
		notifySource = self.tts.QueryInterface(ISpNotifySource)
		notifySource.SetNotifySink(SapiSink(weakref.ref(self)))

	def _set_voice(self, value):
		tokens = self._getVoiceTokens()
		# #2629: Iterating uses IEnumVARIANT and GetBestInterface doesn't work on tokens returned by some token enumerators.
		# Therefore, fetch the items by index, as that method explicitly returns the correct interface.
		for i in range(len(tokens)):
			voice = tokens[i]
			if value == voice.Id:
				break
		else:
			# Voice not found.
			return
		self._initTts(voice=voice)

	def _percentToPitch(self, percent):
		return percent // 2 - 25

	IPA_TO_SAPI = {
		"θ": "th",
		"s": "s",
	}

	def _convertPhoneme(self, ipa):
		# We only know about US English phonemes.
		# Rather than just ignoring unknown phonemes, SAPI throws an exception.
		# Therefore, don't bother with any other language.
		if self.tts.voice.GetAttribute("language") != "409":
			raise LookupError("No data for this language")
		out = []
		outAfter = None
		for ipaChar in ipa:
			if ipaChar == "ˈ":
				outAfter = "1"
				continue
			out.append(self.IPA_TO_SAPI[ipaChar])
			if outAfter:
				out.append(outAfter)
				outAfter = None
		if outAfter:
			out.append(outAfter)
		return " ".join(out)

	def speak(self, speechSequence):
		textList = []

		# NVDA SpeechCommands are linear, but XML is hierarchical.
		# Therefore, we track values for non-empty tags.
		# When a tag changes, we close all previously opened tags and open new ones.
		tags = {}
		# We have to use something mutable here because it needs to be changed by the inner function.
		tagsChanged = [True]
		openedTags = []

		def outputTags():
			if not tagsChanged[0]:
				return
			for tag in reversed(openedTags):
				textList.append("</%s>" % tag)
			del openedTags[:]
			for tag, attrs in tags.items():
				textList.append("<%s" % tag)
				for attr, val in attrs.items():
					textList.append(' %s="%s"' % (attr, val))
				textList.append(">")
				openedTags.append(tag)
			tagsChanged[0] = False

		pitch = self._pitch
		# Pitch must always be specified in the markup.
		tags["pitch"] = {"absmiddle": self._percentToPitch(pitch)}
		rate = self.rate
		volume = self.volume

		for item in speechSequence:
			if isinstance(item, str):
				outputTags()
				textList.append(item.replace("<", "&lt;"))
			elif isinstance(item, IndexCommand):
				textList.append('<Bookmark Mark="%d" />' % item.index)
			elif isinstance(item, CharacterModeCommand):
				if item.state:
					tags["spell"] = {}
				else:
					try:
						del tags["spell"]
					except KeyError:
						pass
				tagsChanged[0] = True
			elif isinstance(item, BreakCommand):
				textList.append('<silence msec="%d" />' % item.time)
			elif isinstance(item, PitchCommand):
				tags["pitch"] = {"absmiddle": self._percentToPitch(int(pitch * item.multiplier))}
				tagsChanged[0] = True
			elif isinstance(item, VolumeCommand):
				if item.multiplier == 1:
					try:
						del tags["volume"]
					except KeyError:
						pass
				else:
					tags["volume"] = {"level": int(volume * item.multiplier)}
				tagsChanged[0] = True
			elif isinstance(item, RateCommand):
				if item.multiplier == 1:
					try:
						del tags["rate"]
					except KeyError:
						pass
				else:
					tags["rate"] = {"absspeed": self._percentToRate(int(rate * item.multiplier))}
				tagsChanged[0] = True
			elif isinstance(item, PhonemeCommand):
				try:
					textList.append(
						'<pron sym="%s">%s</pron>' % (self._convertPhoneme(item.ipa), item.text or ""),
					)
				except LookupError:
					log.debugWarning("Couldn't convert character in IPA string: %s" % item.ipa)
					if item.text:
						textList.append(item.text)
			elif isinstance(item, LangChangeCommand):
				lcid = (
					languageHandler.localeNameToWindowsLCID(item.lang)
					if item.lang
					else languageHandler.LCID_NONE
				)
				if lcid is languageHandler.LCID_NONE:
					try:
						del tags["lang"]
					except KeyError:
						pass
				else:
					tags["lang"] = {"langid": "%x" % lcid}
				tagsChanged[0] = True
			elif isinstance(item, SpeechCommand):
				log.debugWarning("Unsupported speech command: %s" % item)
			else:
				log.error("Unknown speech: %s" % item)
		# Close any tags that are still open.
		tags.clear()
		tagsChanged[0] = True
		outputTags()

		text = "".join(textList)
		flags = SpeechVoiceSpeakFlags.IsXML | SpeechVoiceSpeakFlags.Async
		self.tts.Speak(text, flags)

	def cancel(self):
		# SAPI5's default means of stopping speech can sometimes lag at end of speech, especially with Win8 / Win 10 Microsoft Voices.
		# Therefore  instruct the audio player to stop first, before interupting and purging any remaining speech.
		self.isSpeaking = False
		self.player.stop()
		self.tts.Speak(None, SpeechVoiceSpeakFlags.Async | SpeechVoiceSpeakFlags.PurgeBeforeSpeak)

	def pause(self, switch: bool):
		self.player.pause(switch)
