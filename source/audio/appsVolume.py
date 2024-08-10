# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import config
import globalVars
from logHandler import log
import nvwave
from pycaw.utils import AudioSession
import ui
from dataclasses import dataclass
from threading import Lock
from config.featureFlagEnums import AppsVolumeAdjusterFlag
from typing import NamedTuple
from .utils import AudioSessionCallback, DummyAudioSessionCallback
from comtypes import COMError


class VolumeAndMute(NamedTuple):
	volume: float
	mute: bool


_appVolumesCache: dict[int, VolumeAndMute] = {}
_appVolumesCacheLock = Lock()
_activeCallback: DummyAudioSessionCallback | None = None


def initialize() -> None:
	state = config.conf["audio"]["applicationsVolumeMode"]
	if state == AppsVolumeAdjusterFlag.MUTED:
		# As per user request, muted state shouldn't be persistent, so unmuting upon restart.
		state = AppsVolumeAdjusterFlag.ENABLED
		config.conf["audio"]["applicationsVolumeMode"] = state
	volume = config.conf["audio"]["applicationsSoundVolume"]
	_updateAppsVolumeImpl(volume / 100.0, state)


def terminate():
	global _activeCallback
	if _activeCallback is not None:
		_activeCallback.unregister()
		_activeCallback = None


@dataclass(unsafe_hash=True)
class VolumeSetter(AudioSessionCallback):
	volumeAndMute: VolumeAndMute | None = None

	def getOriginalVolumeAndMute(self, pid: int) -> VolumeAndMute:
		try:
			with _appVolumesCacheLock:
				originalVolumeAndMute = _appVolumesCache[pid]
				del _appVolumesCache[pid]
		except KeyError:
			originalVolumeAndMute = VolumeAndMute(volume=1.0, mute=False)
		return originalVolumeAndMute

	def onSessionUpdate(self, session: AudioSession) -> None:
		pid = session.ProcessId
		simpleVolume = session.SimpleAudioVolume
		with _appVolumesCacheLock:
			if pid not in _appVolumesCache:
				_appVolumesCache[pid] = VolumeAndMute(
					volume=simpleVolume.GetMasterVolume(),
					mute=simpleVolume.GetMute(),
				)
		if pid != globalVars.appPid:
			simpleVolume.SetMasterVolume(self.volumeAndMute.volume, None)
			simpleVolume.SetMute(self.volumeAndMute.mute, None)

	def onSessionTerminated(self, session: AudioSession) -> None:
		pid = session.ProcessId
		simpleVolume = session.SimpleAudioVolume
		originalVolumeAndMute = self.getOriginalVolumeAndMute(pid)
		try:
			simpleVolume.SetMasterVolume(originalVolumeAndMute.volume, None)
			simpleVolume.SetMute(originalVolumeAndMute.mute, None)
		except (COMError, RuntimeError) as e:
			log.exception(f"Could not restore master volume of process {pid} upon exit: {e}")


def _updateAppsVolumeImpl(
	volume: float,
	state: AppsVolumeAdjusterFlag,
):
	global _activeCallback
	if state == AppsVolumeAdjusterFlag.DISABLED:
		newCallback = DummyAudioSessionCallback()
		runTerminators = True
	else:
		newCallback = VolumeSetter(
			volumeAndMute=VolumeAndMute(
				volume=volume,
				mute=state == AppsVolumeAdjusterFlag.MUTED,
			),
		)
		runTerminators = False
	if _activeCallback is not None:
		_activeCallback.unregister(runTerminators=runTerminators)
	_activeCallback = newCallback
	_activeCallback.register()


def _adjustAppsVolume(
	volumeAdjustment: int | None = None,
):
	if not nvwave.usingWasapiWavePlayer():
		message = _(
			# Translators: error message when wasapi is turned off.
			"Other applications' volume cannot be adjusted. "
			"Please enable WASAPI in the Advanced category in NVDA Settings to use it.",
		)
		ui.message(message)
		return
	volume: int = config.conf["audio"]["applicationsSoundVolume"]
	state = config.conf["audio"]["applicationsVolumeMode"]
	if state != AppsVolumeAdjusterFlag.ENABLED:
		# Translators: error message when applications' volume is disabled
		msg = _("Please enable applications' volume adjuster in order to adjust applications' volume")
		ui.message(msg)
		return
	volume += volumeAdjustment
	volume = max(0, min(100, volume))
	log.debug(f"Adjusting applications volume by {volumeAdjustment}% to {volume}%")
	config.conf["audio"]["applicationsSoundVolume"] = volume

	# We skip running terminators here to avoid application volume spiking to 100% for a split second.
	_updateAppsVolumeImpl(volume / 100.0, state)
	# Translators: Announcing new applications' volume message
	msg = _("Applications volume {}").format(volume)
	ui.message(msg)


_APPS_VOLUME_STATES_ORDER = [
	AppsVolumeAdjusterFlag.DISABLED,
	AppsVolumeAdjusterFlag.ENABLED,
	AppsVolumeAdjusterFlag.MUTED,
]


def _toggleAppsVolumeState():
	if not nvwave.usingWasapiWavePlayer():
		message = _(
			# Translators: error message when wasapi is turned off.
			"Other applications' volume cannot be adjusted. "
			"Please enable WASAPI in the Advanced category in NVDA Settings to use it.",
		)
		ui.message(message)
		return
	state = config.conf["audio"]["applicationsVolumeMode"]
	volume: int = config.conf["audio"]["applicationsSoundVolume"]
	try:
		index = _APPS_VOLUME_STATES_ORDER.index(state)
	except ValueError:
		index = -1
	index = (index + 1) % len(_APPS_VOLUME_STATES_ORDER)
	state = _APPS_VOLUME_STATES_ORDER[index]
	config.conf["audio"]["applicationsVolumeMode"] = state.name
	_updateAppsVolumeImpl(volume / 100.0, state)
	ui.message(state.displayString)
