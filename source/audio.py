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
from typing import Tuple, Optional, Dict, List, Callable, NoReturn
import ui
from utils.displayString import DisplayStringIntEnum

VolumeTupleT = Tuple[float, float]


@unique
class SoundSplitState(DisplayStringIntEnum):
	OFF = 0
	NVDA_LEFT = 1
	NVDA_RIGHT = 2

	@property
	def _displayStringLabels(self) -> Dict[IntEnum, str]:
		return {
			# Translators: Sound split state
			SoundSplitState.OFF: _("Disabled sound split"),
			# Translators: Sound split state
			SoundSplitState.NVDA_LEFT: _("NVDA on the left and applications on the right"),
			# Translators: Sound split state
			SoundSplitState.NVDA_RIGHT: _("NVDA on the right and applications on the left"),
		}
	
	def getAppVolume(self) -> VolumeTupleT:
		return {
			SoundSplitState.OFF: (1.0, 1.0),
			SoundSplitState.NVDA_LEFT: (0.0, 1.0),
			SoundSplitState.NVDA_RIGHT: (1.0, 0.0),
		}[self]
	
	def getNVDAVolume(self) -> VolumeTupleT:
		return {
			SoundSplitState.OFF: (1.0, 1.0),
			SoundSplitState.NVDA_LEFT: (1.0, 0.0),
			SoundSplitState.NVDA_RIGHT: (0.0, 1.0),
		}[self]


@unique
class SoundSplitToggleMode(DisplayStringIntEnum):
	OFF_LEFT_RIGHT = 0
	OFF_AND_NVDA_LEFT = 1
	OFF_AND_NVDA_RIGHT = 2

	@property
	def _displayStringLabels(self) -> Dict[IntEnum, str]:
		return {
			# Translators: Sound split toggle mode
			SoundSplitToggleMode.OFF_AND_NVDA_LEFT: _("Cycles through off and NVDA on the left"),
			# Translators: Sound split toggle mode
			SoundSplitToggleMode.OFF_AND_NVDA_RIGHT: _("Cycles through off and NVDA on the right"),
			# Translators: Sound split toggle mode
			SoundSplitToggleMode.OFF_LEFT_RIGHT: _("Cycles through off, NVDA on the left and NVDA on the right"),
		}
	
	def getPossibleStates(self) -> List[SoundSplitState]:
		result = [SoundSplitState.OFF]
		if 'LEFT' in self.name:
			result.append(SoundSplitState.NVDA_LEFT)
		if 'RIGHT' in self.name:
			result.append(SoundSplitState.NVDA_RIGHT)
		return result
	
	def getClosestState(self, state: SoundSplitState) -> SoundSplitState:
		states = self.getPossibleStates()
		if state in states:
			return state
		return states[-1]


sessionManager: audiopolicy.IAudioSessionManager2 = None
activeCallback: Optional[comtypes.COMObject] = None


def initialize() -> None:
	global sessionManager
	sessionManager = getSessionManager()
	if sessionManager is None:
		log.error("Could not initialize audio session manager! ")
		return
	if nvwave.usingWasapiWavePlayer():
		state = SoundSplitState(config.conf['audio']['soundSplitState'])
		global activeCallback
		activeCallback = setSoundSplitState(state)


@atexit.register
def terminate():
	if nvwave.usingWasapiWavePlayer():
		setSoundSplitState(SoundSplitState.OFF)
		if activeCallback is not None:
			unregisterCallback(activeCallback)


def getDefaultAudioDevice(kind: EDataFlow = EDataFlow.eRender) -> Optional[mmdeviceapi.IMMDevice]:
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
		func: Callable[[audiopolicy.IAudioSessionControl2], NoReturn],
		applyToFuture: bool = True,
) -> Optional[comtypes.COMObject]:
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
			channelVolume.SetChannelVolume(1, leftVolume, None)
			channelVolume.SetChannelVolume(0, rightVolume, None)

	activeCallback = applyToAllAudioSessions(volumeSetter)


def toggleSoundSplitState() -> None:
	if not nvwave.usingWasapiWavePlayer():
		message = _(
			# Translators: error message when wasapi is turned off.
			"Sound split is only available in wasapi mode. "
			"Please enable wasapi on the Advanced panel in NVDA Settings."
		)
		ui.message(message)
		return
	toggleMode = SoundSplitToggleMode(config.conf['audio']['soundSplitToggleMode'])
	state = SoundSplitState(config.conf['audio']['soundSplitState'])
	allowedStates = toggleMode.getPossibleStates()
	try:
		i = allowedStates.index(state)
	except ValueError:
		i = -1
	i = (i + 1) % len(allowedStates)
	newState = allowedStates[i]
	setSoundSplitState(newState)
	config.conf['audio']['soundSplitState'] = newState.value
	ui.message(newState.displayString)
