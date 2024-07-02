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
from pycaw.callbacks import AudioSessionNotification, AudioSessionEvents
from pycaw.utils import AudioSession, AudioUtilities
import ui
from utils.displayString import DisplayStringIntEnum
from dataclasses import dataclass
from comtypes import COMError
from threading import Lock
import core

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


_audioSessionManager: IAudioSessionManager2 | None = None
_activeCallback: AudioSessionNotification | None = None


def initialize() -> None:
	if nvwave.usingWasapiWavePlayer():
		global _audioSessionManager
		try:
			_audioSessionManager = AudioUtilities.GetAudioSessionManager()
		except COMError:
			log.exception("Could not initialize audio session manager")
			return
		state = SoundSplitState(config.conf["audio"]["soundSplitState"])
		_setSoundSplitState(state, initial=True)
	else:
		log.debug("Cannot initialize sound split as WASAPI is disabled")


@atexit.register
def terminate():
	if nvwave.usingWasapiWavePlayer():
		state = SoundSplitState(config.conf["audio"]["soundSplitState"])
		if state != SoundSplitState.OFF:
			_setSoundSplitState(SoundSplitState.OFF)
		_unregisterCallback()
	else:
		log.debug("Skipping terminating sound split as WASAPI is disabled.")


@dataclass(unsafe_hash=True)
class _AudioSessionNotificationWrapper(AudioSessionNotification):
	listener: AudioSessionNotification

	def on_session_created(self, new_session: AudioSession):
		pid = new_session.ProcessId
		with _applicationExitCallbacksLock:
			if pid not in _applicationExitCallbacks:
				volumeRestorer = _VolumeRestorer(pid, new_session)
				new_session.register_notification(volumeRestorer)
				_applicationExitCallbacks[pid] = volumeRestorer
		self.listener.on_session_created(new_session)


def _applyToAllAudioSessions(
		callback: AudioSessionNotification,
		applyToFuture: bool = True,
) -> None:
	"""
		Executes provided callback function on all active audio sessions.
		Additionally, if applyToFuture is True, then it will register a notification with audio session manager,
		which will execute the same callback for all future sessions as they are created.
		That notification will be active until next invokation of this function,
		or until _unregisterCallback() is called.
	"""
	_unregisterCallback()
	callback = _AudioSessionNotificationWrapper(callback)
	if applyToFuture:
		_audioSessionManager.RegisterSessionNotification(callback)
		# The following call is required to make callback to work:
		_audioSessionManager.GetSessionEnumerator()
		global _activeCallback
		_activeCallback = callback
	sessions: list[AudioSession] = AudioUtilities.GetAllSessions()
	for session in sessions:
		callback.on_session_created(session)


def _unregisterCallback() -> None:
	global _activeCallback
	if _activeCallback is not None:
		_audioSessionManager.UnregisterSessionNotification(_activeCallback)
		_activeCallback = None


@dataclass(unsafe_hash=True)
class _VolumeSetter(AudioSessionNotification):
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


def _setSoundSplitState(state: SoundSplitState, initial: bool = False) -> dict:
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
	volumeSetter = _VolumeSetter(leftVolume, rightVolume, leftNVDAVolume, rightNVDAVolume)
	_applyToAllAudioSessions(volumeSetter, applyToFuture=applyToFuture)
	return {
		"foundSessionWithNot2Channels": volumeSetter.foundSessionWithNot2Channels,
	}


def _toggleSoundSplitState() -> None:
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
	result = _setSoundSplitState(newState)
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


@dataclass(unsafe_hash=True)
class _VolumeRestorer(AudioSessionEvents):
	pid: int
	audioSession: AudioSession

	def on_state_changed(self, new_state: str, new_state_id: int):
		if new_state == "Expired":
			# For some reason restoring volume doesn't work in this thread, so scheduling in the main thread.
			core.callLater(0, self.restoreVolume)

	def restoreVolume(self):
		# Application connected to this audio session is terminating. Restore its volume.
		try:
			channelVolume = self.audioSession.channelAudioVolume()
			channelCount = channelVolume.GetChannelCount()
			if channelCount != 2:
				log.warning(
					f"Audio session for pid {self.pid} has {channelCount} channels instead of 2 - cannot set volume!"
				)
				return
			channelVolume.SetChannelVolume(0, 1.0, None)
			channelVolume.SetChannelVolume(1, 1.0, None)
		except Exception:
			log.exception(f"Could not restore volume of process {self.pid} upon exit.")
		self.unregister()

	def unregister(self):
		with _applicationExitCallbacksLock:
			try:
				del _applicationExitCallbacks[self.pid]
			except KeyError:
				pass
			try:
				self.audioSession.unregister_notification()
			except Exception:
				log.exception(f"Cannot unregister audio session for process {self.pid}")


_applicationExitCallbacksLock = Lock()
_applicationExitCallbacks: dict[int, _VolumeRestorer] = {}
