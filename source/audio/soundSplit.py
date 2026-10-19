# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import atexit  # noqa: I001
import config
import globalVars
from logHandler import log
from pycaw.api.audiopolicy import IAudioSessionManager2
from pycaw.callbacks import AudioSessionNotification, AudioSessionEvents
from pycaw.utils import AudioSession, AudioUtilities
import ui
from dataclasses import dataclass
from comtypes import COMError
from threading import Lock
import core

from .soundSplitState import SoundSplitState, VolumeTupleT  # noqa: F401


_audioSessionManager: IAudioSessionManager2 | None = None
_activeCallback: AudioSessionNotification | None = None


def initialize() -> None:
	global _audioSessionManager
	try:
		_audioSessionManager = AudioUtilities.GetAudioSessionManager()
	except COMError:
		log.exception("Could not initialize audio session manager")
		return
	state = SoundSplitState(config.conf["audio"]["soundSplitState"])
	_setSoundSplitState(state, initial=True)


@atexit.register
def terminate():
	state = SoundSplitState(config.conf["audio"]["soundSplitState"])
	if state != SoundSplitState.OFF:
		_setSoundSplitState(SoundSplitState.OFF)
	_unregisterCallback()


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
					f"Audio session for pid {self.pid} has {channelCount} channels instead of 2 - cannot set volume!",
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
