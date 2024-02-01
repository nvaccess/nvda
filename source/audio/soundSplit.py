# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2021 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import atexit
from comInterfaces.coreAudio.constants import (
	CLSID_MMDeviceEnumerator,
	EDataFlow,
	ERole,
)
import comInterfaces.coreAudio.audioclient as audioclient
import comInterfaces.coreAudio.audiopolicy as audiopolicy
import comInterfaces.coreAudio.mmdeviceapi as mmdeviceapi
import comtypes
import config
from enum import IntEnum, unique
import globalVars
from logHandler import log
import nvwave
from typing import Callable
import ui
from utils.displayString import DisplayStringIntEnum
import _ctypes

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
			SoundSplitState.OFF: _("Disabled sound split"),
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


sessionManager: audiopolicy.IAudioSessionManager2 = None
activeCallback: comtypes.COMObject | None = None


def initialize() -> None:
	global sessionManager
	try:
		sessionManager = getSessionManager()
	except _ctypes.COMError as e:
		log.error("Could not initialize audio session manager! ", e)
		return
	if sessionManager is None:
		log.error("Could not initialize audio session manager! ")
		return
	if nvwave.usingWasapiWavePlayer():
		state = SoundSplitState(config.conf['audio']['soundSplitState'])
		global activeCallback
		activeCallback = setSoundSplitState(state)


@atexit.register
def terminate():
	global activeCallback
	if nvwave.usingWasapiWavePlayer():
		setSoundSplitState(SoundSplitState.OFF)
		if activeCallback is not None:
			unregisterCallback(activeCallback)
	activeCallback = None


def getDefaultAudioDevice(kind: EDataFlow = EDataFlow.eRender) -> mmdeviceapi.IMMDevice | None:
	deviceEnumerator = comtypes.CoCreateInstance(
		CLSID_MMDeviceEnumerator,
		mmdeviceapi.IMMDeviceEnumerator,
		comtypes.CLSCTX_INPROC_SERVER,
	)
	device = deviceEnumerator.GetDefaultAudioEndpoint(
		kind.value,
		ERole.eMultimedia.value,
	)
	return device


def getSessionManager() -> audiopolicy.IAudioSessionManager2:
	audioDevice = getDefaultAudioDevice()
	if audioDevice is None:
		raise RuntimeError("No default output audio device found!")
	tmp = audioDevice.Activate(audiopolicy.IAudioSessionManager2._iid_, comtypes.CLSCTX_ALL, None)
	sessionManager: audiopolicy.IAudioSessionManager2 = tmp.QueryInterface(audiopolicy.IAudioSessionManager2)
	return sessionManager


def applyToAllAudioSessions(
		func: Callable[[audiopolicy.IAudioSessionControl2], None],
		applyToFuture: bool = True,
) -> comtypes.COMObject | None:
	sessionEnumerator: audiopolicy.IAudioSessionEnumerator = sessionManager.GetSessionEnumerator()
	for i in range(sessionEnumerator.GetCount()):
		session: audiopolicy.IAudioSessionControl = sessionEnumerator.GetSession(i)
		session2: audiopolicy.IAudioSessionControl2 = session.QueryInterface(audiopolicy.IAudioSessionControl2)
		func(session2)
	if applyToFuture:
		class AudioSessionNotification(comtypes.COMObject):
			_com_interfaces_ = (audiopolicy.IAudioSessionNotification,)

			def OnSessionCreated(self, session: audiopolicy.IAudioSessionControl):
				session2 = session.QueryInterface(audiopolicy.IAudioSessionControl2)
				func(session2)
		callback = AudioSessionNotification()
		sessionManager.RegisterSessionNotification(callback)
		return callback
	else:
		return None


def unregisterCallback(callback: comtypes.COMObject) -> None:
	sessionManager .UnregisterSessionNotification(callback)


def setSoundSplitState(state: SoundSplitState) -> None:
	global activeCallback
	if activeCallback is not None:
		unregisterCallback(activeCallback)
		activeCallback = None
	leftVolume, rightVolume = state.getAppVolume()
	leftNVDAVolume, rightNVDAVolume = state.getNVDAVolume()

	def volumeSetter(session2: audiopolicy.IAudioSessionControl2) -> None:
		channelVolume: audioclient.IChannelAudioVolume = session2.QueryInterface(audioclient.IChannelAudioVolume)
		channelCount = channelVolume.GetChannelCount()
		if channelCount != 2:
			pid = session2.GetProcessId()
			log.warning(f"Audio session for pid {pid} has {channelCount} channels instead of 2 - cannot set volume!")
			return
		pid: int = session2.GetProcessId()
		if pid != globalVars.appPid:
			channelVolume.SetChannelVolume(0, leftVolume, None)
			channelVolume.SetChannelVolume(1, rightVolume, None)
		else:
			channelVolume.SetChannelVolume(0, leftNVDAVolume, None)
			channelVolume.SetChannelVolume(1, rightNVDAVolume, None)

	activeCallback = applyToAllAudioSessions(volumeSetter)


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
