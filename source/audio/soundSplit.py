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

VolumeTupleT = tuple[float, float]


@unique
class SoundSplitState(DisplayStringIntEnum):
	OFF = 0
	NVDA_LEFT_APPS_RIGHT = 1
	NVDA_LEFT_APPS_BOTH = 2
	NVDA_RIGHT_APPS_LEFT = 3
	NVDA_RIGHT_APPS_BOTH = 4
	NVDA_BOTH_APPS_LEFT = 5
	NVDA_BOTH_APPS_RIGHT = 6

	@property
	def _displayStringLabels(self) -> dict[IntEnum, str]:
		return {
			# Translators: Sound split state
			SoundSplitState.OFF: pgettext("SoundSplit", "Disabled"),
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
			case SoundSplitState.OFF | SoundSplitState.NVDA_LEFT_APPS_BOTH | SoundSplitState.NVDA_RIGHT_APPS_BOTH:
				return (1.0, 1.0)
			case SoundSplitState.NVDA_RIGHT_APPS_LEFT | SoundSplitState.NVDA_BOTH_APPS_LEFT:
				return (1.0, 0.0)
			case SoundSplitState.NVDA_LEFT_APPS_RIGHT | SoundSplitState.NVDA_BOTH_APPS_RIGHT:
				return (0.0, 1.0)
			case _:
				raise RuntimeError(f"{self=}")

	def getNVDAVolume(self) -> VolumeTupleT:
		match self:
			case SoundSplitState.OFF | SoundSplitState.NVDA_BOTH_APPS_LEFT | SoundSplitState.NVDA_BOTH_APPS_RIGHT:
				return (1.0, 1.0)
			case SoundSplitState.NVDA_LEFT_APPS_RIGHT | SoundSplitState.NVDA_LEFT_APPS_BOTH:
				return (1.0, 0.0)
			case SoundSplitState.NVDA_RIGHT_APPS_LEFT | SoundSplitState.NVDA_RIGHT_APPS_BOTH:
				return (0.0, 1.0)
			case _:
				raise RuntimeError(f"{self=}")


audioSessionManager: IAudioSessionManager2 | None = None
activeCallback: AudioSessionNotification = None


def initialize() -> None:
	if nvwave.usingWasapiWavePlayer():
		global audioSessionManager
		audioSessionManager = AudioUtilities.GetAudioSessionManager()
		state = SoundSplitState(config.conf['audio']['soundSplitState'])
		setSoundSplitState(state)


@atexit.register
def terminate():
	if nvwave.usingWasapiWavePlayer():
		setSoundSplitState(SoundSplitState.OFF)
		unregisterCallback()


def applyToAllAudioSessions(
		callback: AudioSessionNotification,
		applyToFuture: bool = True,
) -> None:
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


def setSoundSplitState(state: SoundSplitState) -> None:
	leftVolume, rightVolume = state.getAppVolume()
	leftNVDAVolume, rightNVDAVolume = state.getNVDAVolume()

	class VolumeSetter(AudioSessionNotification):
		def on_session_created(self, new_session: AudioSession):
			pid = new_session.ProcessId
			channelVolume = new_session.channelAudioVolume()
			channelCount = channelVolume.GetChannelCount()
			if channelCount != 2:
				log.warning(f"Audio session for pid {pid} has {channelCount} channels instead of 2 - cannot set volume!")
				return
			if pid != globalVars.appPid:
				channelVolume.SetChannelVolume(0, leftVolume, None)
				channelVolume.SetChannelVolume(1, rightVolume, None)
			else:
				channelVolume.SetChannelVolume(0, leftNVDAVolume, None)
				channelVolume.SetChannelVolume(1, rightNVDAVolume, None)

	volumeSetter = VolumeSetter()
	applyToAllAudioSessions(volumeSetter)


def toggleSoundSplitState() -> None:
	if not nvwave.usingWasapiWavePlayer():
		message = _(
			# Translators: error message when wasapi is turned off.
			"Sound split cannot be used. "
			"Please enable WASAPI in the Advanced category in NVDA Settings to use it."
		)
		ui.message(message)
		return
	state = SoundSplitState(config.conf['audio']['soundSplitState'])
	allowedStates: list[int] = config.conf["audio"]["includedSoundSplitModes"]
	try:
		i = allowedStates.index(state)
	except ValueError:
		i = -1
	i = (i + 1) % len(allowedStates)
	newState = SoundSplitState(allowedStates[i])
	setSoundSplitState(newState)
	config.conf['audio']['soundSplitState'] = newState.value
	ui.message(newState.displayString)
