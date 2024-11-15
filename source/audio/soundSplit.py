# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import config
from enum import IntEnum, unique
import globalVars
from logHandler import log
import nvwave
from pycaw.utils import AudioSession
import ui
from utils.displayString import DisplayStringIntEnum
from dataclasses import dataclass
from .utils import AudioSessionCallback, DummyAudioSessionCallback

VolumeTupleT = tuple[float, float]


@unique
class SoundSplitState(DisplayStringIntEnum):
	OFF = 0
	NVDA_BOTH_APPS_BOTH = 1
	NVDA_LEFT_APPS_RIGHT = 2
	NVDA_LEFT_APPS_BOTH = 3
	NVDA_RIGHT_APPS_LEFT = 4
	NVDA_RIGHT_APPS_BOTH = 5
	NVDA_BOTH_APPS_LEFT = 6
	NVDA_BOTH_APPS_RIGHT = 7

	@property
	def _displayStringLabels(self) -> dict[IntEnum, str]:
		return {
			# Translators: Sound split state
			SoundSplitState.OFF: pgettext("SoundSplit", "Sound split disabled"),
			SoundSplitState.NVDA_BOTH_APPS_BOTH: pgettext(
				"SoundSplit",
				# Translators: Sound split state
				"NVDA in both channels and applications in both channels",
			),
			# Translators: Sound split state
			SoundSplitState.NVDA_LEFT_APPS_RIGHT: _("NVDA on the left and applications on the right"),
			# Translators: Sound split state
			SoundSplitState.NVDA_LEFT_APPS_BOTH: _("NVDA on the left and applications in both channels"),
			# Translators: Sound split state
			SoundSplitState.NVDA_RIGHT_APPS_LEFT: _("NVDA on the right and applications on the left"),
			# Translators: Sound split state
			SoundSplitState.NVDA_RIGHT_APPS_BOTH: _("NVDA on the right and applications in both channels"),
			# Translators: Sound split state
			SoundSplitState.NVDA_BOTH_APPS_LEFT: _("NVDA in both channels and applications on the left"),
			# Translators: Sound split state
			SoundSplitState.NVDA_BOTH_APPS_RIGHT: _("NVDA in both channels and applications on the right"),
		}

	def getAppVolume(self) -> VolumeTupleT:
		match self:
			case (
				SoundSplitState.NVDA_BOTH_APPS_BOTH
				| SoundSplitState.NVDA_LEFT_APPS_BOTH
				| SoundSplitState.NVDA_RIGHT_APPS_BOTH
			):
				return (1.0, 1.0)
			case SoundSplitState.NVDA_RIGHT_APPS_LEFT | SoundSplitState.NVDA_BOTH_APPS_LEFT:
				return (1.0, 0.0)
			case SoundSplitState.NVDA_LEFT_APPS_RIGHT | SoundSplitState.NVDA_BOTH_APPS_RIGHT:
				return (0.0, 1.0)
			case _:
				raise RuntimeError(f"Unexpected or unknown state {self=}")

	def getNVDAVolume(self) -> VolumeTupleT:
		match self:
			case (
				SoundSplitState.NVDA_BOTH_APPS_BOTH
				| SoundSplitState.NVDA_BOTH_APPS_LEFT
				| SoundSplitState.NVDA_BOTH_APPS_RIGHT
			):
				return (1.0, 1.0)
			case SoundSplitState.NVDA_LEFT_APPS_RIGHT | SoundSplitState.NVDA_LEFT_APPS_BOTH:
				return (1.0, 0.0)
			case SoundSplitState.NVDA_RIGHT_APPS_LEFT | SoundSplitState.NVDA_RIGHT_APPS_BOTH:
				return (0.0, 1.0)
			case _:
				raise RuntimeError(f"Unexpected or unknown state {self=}")


_activeCallback: DummyAudioSessionCallback | None = None


def initialize() -> None:
	state = SoundSplitState(config.conf["audio"]["soundSplitState"])
	_setSoundSplitState(state)


def terminate():
	global _activeCallback
	if _activeCallback is not None:
		_activeCallback.unregister()
		_activeCallback = None


@dataclass(unsafe_hash=True)
class ChannelVolumeSetter(AudioSessionCallback):
	leftVolume: float = 0.0
	rightVolume: float = 0.0
	leftNVDAVolume: float = 0.0
	rightNVDAVolume: float = 0.0
	foundSessionWithNot2Channels: bool = False

	def onSessionUpdate(self, session: AudioSession) -> None:
		pid = session.ProcessId
		channelVolume = session.channelAudioVolume()
		channelCount = channelVolume.GetChannelCount()
		if channelCount != 2:
			log.warning(
				f"Audio session for pid {pid} has {channelCount} channels instead of 2 - cannot set volume!",
			)
			self.foundSessionWithNot2Channels = True
			return
		if pid != globalVars.appPid:
			channelVolume.SetChannelVolume(0, self.leftVolume, None)
			channelVolume.SetChannelVolume(1, self.rightVolume, None)
		else:
			channelVolume.SetChannelVolume(0, self.leftNVDAVolume, None)
			channelVolume.SetChannelVolume(1, self.rightNVDAVolume, None)

	def onSessionTerminated(self, session: AudioSession) -> None:
		pid = session.ProcessId
		try:
			channelVolume = session.channelAudioVolume()
			channelCount = channelVolume.GetChannelCount()
			if channelCount != 2:
				log.warning(
					f"Audio session for pid {pid} has {channelCount} channels instead of 2 - cannot set volume!",
				)
				return
			channelVolume.SetChannelVolume(0, 1.0, None)
			channelVolume.SetChannelVolume(1, 1.0, None)
		except Exception:
			log.exception(f"Could not restore channel volume of process {pid} upon exit.")


def _setSoundSplitState(state: SoundSplitState) -> dict:
	global _activeCallback
	if _activeCallback is not None:
		_activeCallback.unregister()
		_activeCallback = None
	if state == SoundSplitState.OFF:
		_activeCallback = DummyAudioSessionCallback()
	else:
		leftVolume, rightVolume = state.getAppVolume()
		leftNVDAVolume, rightNVDAVolume = state.getNVDAVolume()
		_activeCallback = ChannelVolumeSetter(
			leftVolume=leftVolume,
			rightVolume=rightVolume,
			leftNVDAVolume=leftNVDAVolume,
			rightNVDAVolume=rightNVDAVolume,
		)
	_activeCallback.register()
	notTwoChannels = False if state == SoundSplitState.OFF else _activeCallback.foundSessionWithNot2Channels
	return {
		"foundSessionWithNot2Channels": notTwoChannels,
	}


def _toggleSoundSplitState() -> None:
	if not nvwave.usingWasapiWavePlayer():
		message = _(
			# Translators: error message when wasapi is turned off.
			"Sound split cannot be used. "
			"Please enable WASAPI in the Advanced category in NVDA Settings to use it.",
		)
		ui.message(message)
		return
	state = SoundSplitState(config.conf["audio"]["soundSplitState"])
	allowedStates: list[int] = config.conf["audio"]["includedSoundSplitModes"]
	try:
		i = allowedStates.index(state)
	except ValueError:
		# State not found, resetting to default (OFF)
		i = -1
	i = (i + 1) % len(allowedStates)
	newState = SoundSplitState(allowedStates[i])
	result = _setSoundSplitState(newState)
	config.conf["audio"]["soundSplitState"] = newState.value
	ui.message(newState.displayString)
	if result["foundSessionWithNot2Channels"]:
		msg = _(
			# Translators: warning message when sound split trigger wasn't successful due to one of audio sessions
			# had number of channels other than 2 .
			"Warning: couldn't set volumes for sound split: "
			"one of audio sessions is either mono, or has more than 2 audio channels.",
		)
		ui.message(msg)
