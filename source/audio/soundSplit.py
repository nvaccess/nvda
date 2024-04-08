# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import atexit
import config
from enum import IntEnum, unique
import globalVars
from logHandler import log
import nvwave
from pycaw.api.audiopolicy import IAudioSessionManager2
from pycaw.callbacks import AudioSessionNotification
from pycaw.utils import AudioSession, AudioUtilities
import ui
from utils.displayString import DisplayStringIntEnum
from dataclasses import dataclass
from comtypes import COMError

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


audioSessionManager: IAudioSessionManager2 | None = None
activeCallback: AudioSessionNotification | None = None


def initialize() -> None:
	if nvwave.usingWasapiWavePlayer():
		global audioSessionManager
		try:
			audioSessionManager = AudioUtilities.GetAudioSessionManager()
		except COMError:
			log.exception("Could not initialize audio session manager")
			return
		state = SoundSplitState(config.conf["audio"]["soundSplitState"])
		setSoundSplitState(state, initial=True)
	else:
		log.debug("Cannot initialize sound split as WASAPI is disabled")


@atexit.register
def terminate():
	if nvwave.usingWasapiWavePlayer():
		state = SoundSplitState(config.conf["audio"]["soundSplitState"])
		if state != SoundSplitState.OFF:
			setSoundSplitState(SoundSplitState.OFF)
		unregisterCallback()
	else:
		log.debug("Skipping terminating sound split as WASAPI is disabled.")


def applyToAllAudioSessions(
		callback: AudioSessionNotification,
		applyToFuture: bool = True,
) -> None:
	"""
		Executes provided callback function on all active audio sessions.
		Additionally, if applyToFuture is True, then it will register a notification with audio session manager,
		which will execute the same callback for all future sessions as they are created.
		That notification will be active until next invokation of this function,
		or until unregisterCallback() is called.
	"""
	unregisterCallback()
	if applyToFuture:
		audioSessionManager.RegisterSessionNotification(callback)
		# The following call is required to make callback to work:
		audioSessionManager.GetSessionEnumerator()
		global activeCallback
		activeCallback = callback
	sessions: list[AudioSession] = AudioUtilities.GetAllSessions()
	for session in sessions:
		callback.on_session_created(session)


def unregisterCallback() -> None:
	global activeCallback
	if activeCallback is not None:
		audioSessionManager.UnregisterSessionNotification(activeCallback)
		activeCallback = None


@dataclass(unsafe_hash=True)
class VolumeSetter(AudioSessionNotification):
	leftVolume: float
	rightVolume: float
	leftNVDAVolume: float
	rightNVDAVolume: float
	foundSessionWithNot2Channels: bool = False

	def on_session_created(self, new_session: AudioSession):
		pid = new_session.ProcessId
		channelVolume = new_session.channelAudioVolume()
		channelCount = channelVolume.GetChannelCount()
		if channelCount != 2:
			log.warning(f"Audio session for pid {pid} has {channelCount} channels instead of 2 - cannot set volume!")
			self.foundSessionWithNot2Channels = True
			return
		if pid != globalVars.appPid:
			channelVolume.SetChannelVolume(0, self.leftVolume, None)
			channelVolume.SetChannelVolume(1, self.rightVolume, None)
		else:
			channelVolume.SetChannelVolume(0, self.leftNVDAVolume, None)
			channelVolume.SetChannelVolume(1, self.rightNVDAVolume, None)


def setSoundSplitState(state: SoundSplitState, initial: bool = False) -> dict:
	applyToFuture = True
	if state == SoundSplitState.OFF:
		if initial:
			return {}
		else:
			# Disabling sound split via command or via settings
			# We need to restore volume of all applications, but then don't set up callback for future audio sessions
			state = SoundSplitState.NVDA_BOTH_APPS_BOTH
			applyToFuture = False
	leftVolume, rightVolume = state.getAppVolume()
	leftNVDAVolume, rightNVDAVolume = state.getNVDAVolume()
	volumeSetter = VolumeSetter(leftVolume, rightVolume, leftNVDAVolume, rightNVDAVolume)
	applyToAllAudioSessions(volumeSetter, applyToFuture=applyToFuture)
	return {
		"foundSessionWithNot2Channels": volumeSetter.foundSessionWithNot2Channels,
	}


def toggleSoundSplitState() -> None:
	if not nvwave.usingWasapiWavePlayer():
		message = _(
			# Translators: error message when wasapi is turned off.
			"Sound split cannot be used. "
			"Please enable WASAPI in the Advanced category in NVDA Settings to use it."
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
	result = setSoundSplitState(newState)
	config.conf["audio"]["soundSplitState"] = newState.value
	ui.message(newState.displayString)
	if result["foundSessionWithNot2Channels"]:
		msg = _(
			# Translators: warning message when sound split trigger wasn't successful due to one of audio sessions
			# had number of channels other than 2 .
			"Warning: couldn't set volumes for sound split: "
			"one of audio sessions is either mono, or has more than 2 audio channels."
		)
		ui.message(msg)
