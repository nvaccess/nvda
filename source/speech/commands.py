#  -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2006-2020 NV Access Limited

"""
Commands that can be embedded in a speech sequence for changing synth parameters, playing sounds or running
 other callbacks.
"""
 
from abc import ABCMeta, abstractmethod
from typing import Optional, Callable

import config
from synthDriverHandler import getSynth
from logHandler import log

class SpeechCommand(object):
	"""The base class for objects that can be inserted between strings of text to perform actions,
	change voice parameters, etc.

	Note: Some of these commands are processed by NVDA and are not directly passed to synth drivers.
	synth drivers will only receive commands derived from L{SynthCommand}.
	"""


class _CancellableSpeechCommand(SpeechCommand):
	"""
	A command that allows cancelling the utterance that contains it.
	Support currently experimental and may be subject to change.
	"""

	def __init__(
			self,
			reportDevInfo=False
	):
		"""
		@param reportDevInfo: If true, developer info is reported for repr implementation.
		"""
		self._isCancelled = False
		self._utteranceIndex = None
		self._reportDevInfo = reportDevInfo

	@abstractmethod
	def _checkIfValid(self):
		raise NotImplementedError()

	@abstractmethod
	def _getDevInfo(self):
		raise NotImplementedError()

	def _checkIfCancelled(self):
		if self._isCancelled:
			return True
		elif not self._checkIfValid():
			self._isCancelled = True
		return self._isCancelled

	@property
	def isCancelled(self):
		return self._checkIfCancelled()

	def cancelUtterance(self):
		self._isCancelled = True

	def _getFormattedDevInfo(self):

		return "" if not self._reportDevInfo else (
			f", devInfo<"
			f" isCanceledCache: {self._isCancelled}"
			f", isValidCallback: {self._checkIfValid()}"
			f", isValidCallbackDevInfo: {self._getDevInfo()} >"
		)

	def __repr__(self):
		return (
			f"CancellableSpeech ("
			f"{ 'cancelled' if self._checkIfCancelled() else 'still valid' }"
			f"{self._getFormattedDevInfo()}"
			f")"
		)


class SynthCommand(SpeechCommand):
	"""Commands that can be passed to synth drivers.
	"""

class IndexCommand(SynthCommand):
	"""Marks this point in the speech with an index.
	When speech reaches this index, the synthesizer notifies NVDA,
	thus allowing NVDA to perform actions at specific points in the speech;
	e.g. synchronizing the cursor, beeping or playing a sound.
	Callers should not use this directly.
	Instead, use one of the subclasses of L{BaseCallbackCommand}.
	NVDA handles the indexing and dispatches callbacks as appropriate.
	"""

	def __init__(self,index):
		"""
		@param index: the value of this index
		@type index: integer
		"""
		if not isinstance(index,int): raise ValueError("index must be int, not %s"%type(index))
		self.index=index

	def __repr__(self):
		return "IndexCommand(%r)" % self.index

class SynthParamCommand(SynthCommand):
	"""A synth command which changes a parameter for subsequent speech.
	"""
	#: Whether this command returns the parameter to its default value.
	#: Note that the default might be configured by the user;
	#: e.g. for pitch, rate, etc.
	#: @type: bool
	isDefault = False

class CharacterModeCommand(SynthParamCommand):
	"""Turns character mode on and off for speech synths."""

	def __init__(self,state):
		"""
		@param state: if true character mode is on, if false its turned off.
		@type state: boolean
		"""
		if not isinstance(state,bool): raise ValueError("state must be boolean, not %s"%type(state))
		self.state=state
		self.isDefault = not state

	def __repr__(self):
		return "CharacterModeCommand(%r)" % self.state

class LangChangeCommand(SynthParamCommand):
	"""A command to switch the language within speech."""

	def __init__(self, lang: Optional[str]):
		"""
		@param lang: the language to switch to: If None then the NVDA locale will be used.
		"""
		self.lang = lang
		self.isDefault = not lang

	def __repr__(self):
		return "LangChangeCommand (%r)"%self.lang

class BreakCommand(SynthCommand):
	"""Insert a break between words.
	"""

	def __init__(self, time=0):
		"""
		@param time: The duration of the pause to be inserted in milliseconds.
		@param time: int
		"""
		self.time = time

	def __repr__(self):
		return "BreakCommand(time=%d)" % self.time

class EndUtteranceCommand(SpeechCommand):
	"""End the current utterance at this point in the speech.
	Any text after this will be sent to the synthesizer as a separate utterance.
	"""

	def __repr__(self):
		return "EndUtteranceCommand()"

class BaseProsodyCommand(SynthParamCommand):
	"""Base class for commands which change voice prosody; i.e. pitch, rate, etc.
	The change to the setting is specified using either an offset or a multiplier, but not both.
	The L{offset} and L{multiplier} properties convert between the two if necessary.
	To return to the default value, specify neither.
	This base class should not be instantiated directly.
	"""
	#: The name of the setting in the configuration; e.g. pitch, rate, etc.
	settingName = None

	def __init__(self, offset=0, multiplier=1):
		"""Constructor.
		Either of C{offset} or C{multiplier} may be specified, but not both.
		@param offset: The amount by which to increase/decrease the user configured setting;
			e.g. 30 increases by 30, -10 decreases by 10, 0 returns to the configured setting.
		@type offset: int
		@param multiplier: The number by which to multiply the user configured setting;
			e.g. 0.5 is half, 1 returns to the configured setting.
		@param multiplier: int/float
		"""
		if offset != 0 and multiplier != 1:
			raise ValueError("offset and multiplier both specified")
		self._offset = offset
		self._multiplier = multiplier
		self.isDefault = offset == 0 and multiplier == 1

	@property
	def defaultValue(self):
		"""The default value for the setting as configured by the user.
		"""
		synth = getSynth()
		synthConf = config.conf["speech"][synth.name]
		return synthConf[self.settingName]

	@property
	def multiplier(self):
		"""The number by which to multiply the default value.
		"""
		if self._multiplier != 1:
			# Constructed with multiplier. Just return it.
			return self._multiplier
		if self._offset == 0:
			# Returning to default.
			return 1
		# Calculate multiplier from default value and offset.
		defaultVal = self.defaultValue
		newVal = defaultVal + self._offset
		return float(newVal) / defaultVal

	@property
	def offset(self):
		"""The amount by which to increase/decrease the default value.
		"""
		if self._offset != 0:
			# Constructed with offset. Just return it.
			return self._offset
		if self._multiplier == 1:
			# Returning to default.
			return 0
		# Calculate offset from default value and multiplier.
		defaultVal = self.defaultValue
		newVal = defaultVal * self._multiplier
		return int(newVal - defaultVal)

	@property
	def newValue(self):
		"""The new absolute value after the offset or multiplier is applied to the default value.
		"""
		if self._offset != 0:
			# Calculate using offset.
			return self.defaultValue + self._offset
		if self._multiplier != 1:
			# Calculate using multiplier.
			return int(self.defaultValue * self._multiplier)
		# Returning to default.
		return self.defaultValue

	def __repr__(self):
		if self._offset != 0:
			param = "offset=%d" % self._offset
		elif self._multiplier != 1:
			param = "multiplier=%g" % self._multiplier
		else:
			param = ""
		return "{type}({param})".format(
			type=type(self).__name__, param=param)

class PitchCommand(BaseProsodyCommand):
	"""Change the pitch of the voice.
	"""
	settingName = "pitch"

class VolumeCommand(BaseProsodyCommand):
	"""Change the volume of the voice.
	"""
	settingName = "volume"

class RateCommand(BaseProsodyCommand):
	"""Change the rate of the voice.
	"""
	settingName = "rate"

class PhonemeCommand(SynthCommand):
	"""Insert a specific pronunciation.
	This command accepts Unicode International Phonetic Alphabet (IPA) characters.
	Note that this is not well supported by synthesizers.
	"""

	def __init__(self, ipa, text=None):
		"""
		@param ipa: Unicode IPA characters.
		@type ipa: str
		@param text: Text to speak if the synthesizer does not support
			some or all of the specified IPA characters,
			C{None} to ignore this command instead.
		@type text: str
		"""
		self.ipa = ipa
		self.text = text

	def __repr__(self):
		out = "PhonemeCommand(%r" % self.ipa
		if self.text:
			out += ", text=%r" % self.text
		return out + ")"

class BaseCallbackCommand(SpeechCommand, metaclass=ABCMeta):
	"""Base class for commands which cause a function to be called when speech reaches them.
	This class should not be instantiated directly.
	It is designed to be subclassed to provide specific functionality;
	e.g. L{BeepCommand}.
	To supply a generic function to run, use L{CallbackCommand}.
	This command is never passed to synth drivers.
	"""

	@abstractmethod
	def run(self):
		"""Code to run when speech reaches this command.
		This method is executed in NVDA's main thread, 
		therefore must return as soon as practically possible, 
		otherwise it will block production of further speech and or other functionality in NVDA.
		"""

class CallbackCommand(BaseCallbackCommand):
	"""
	Call a function when speech reaches this point.
	Note that  the provided function is executed in NVDA's main thread, 
		therefore must return as soon as practically possible, 
		otherwise it will block production of further speech and or other functionality in NVDA.
	"""

	def __init__(self, callback, name: Optional[str] = None):
		self._callback = callback
		self._name = name if name else repr(callback)

	def run(self,*args, **kwargs):
		return self._callback(*args,**kwargs)

	def __repr__(self):
		return "CallbackCommand(name={name})".format(
			name=self._name
		)

class BeepCommand(BaseCallbackCommand):
	"""Produce a beep.
	"""

	def __init__(self, hz, length, left=50, right=50):
		self.hz = hz
		self.length = length
		self.left = left
		self.right = right

	def run(self):
		import tones
		tones.beep(self.hz, self.length, left=self.left, right=self.right)

	def __repr__(self):
		return "BeepCommand({hz}, {length}, left={left}, right={right})".format(
			hz=self.hz, length=self.length, left=self.left, right=self.right)

class WaveFileCommand(BaseCallbackCommand):
	"""Play a wave file.
	"""

	def __init__(self, fileName):
		self.fileName = fileName

	def run(self):
		import nvwave
		nvwave.playWaveFile(self.fileName, asynchronous=True)

	def __repr__(self):
		return "WaveFileCommand(%r)" % self.fileName

class ConfigProfileTriggerCommand(SpeechCommand):
	"""Applies (or stops applying) a configuration profile trigger to subsequent speech.
	"""

	def __init__(self, trigger, enter=True):
		"""
		@param trigger: The configuration profile trigger.
		@type trigger: L{config.ProfileTrigger}
		@param enter: C{True} to apply the trigger, C{False} to stop applying it.
		@type enter: bool
		"""
		self.trigger = trigger
		self.enter = enter
		trigger._shouldNotifyProfileSwitch = False
