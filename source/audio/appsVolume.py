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


class VolumeAndMute(NamedTuple):
	volume: float
	mute: bool


appVolumesCache: dict[int, VolumeAndMute] = {}
appVolumesCacheLock = Lock()
activeCallback: DummyAudioSessionCallback | None = None


def initialize() -> None:
	state = config.conf["audio"]["applicationsVolumeMode"]
	if state == AppsVolumeAdjusterFlag.MUTED:
		state = AppsVolumeAdjusterFlag.ENABLED
		config.conf["audio"]["applicationsVolumeMode"] = state
	volume = config.conf["audio"]["applicationsSoundVolume"]
	updateAppsVolumeImpl(volume / 100.0, state)


def terminate():
	global activeCallback
	if activeCallback is not None:
		activeCallback.unregister()
		activeCallback = None


@dataclass(unsafe_hash=True)
class VolumeSetter(AudioSessionCallback):
	volumeAndMute: VolumeAndMute | None = None

	def getOriginalVolumeAndMute(self, pid):
		try:
			with appVolumesCacheLock:
				originalVolumeAndMute = appVolumesCache[pid]
		except KeyError:
			originalVolumeAndMute = VolumeAndMute(volume=1.0, mute=False)
		return originalVolumeAndMute

	def onSessionUpdate(self, session: AudioSession) -> None:
		pid = session.ProcessId
		simpleVolume = session.SimpleAudioVolume
		with appVolumesCacheLock:
			if pid not in appVolumesCache:
				appVolumesCache[pid] = VolumeAndMute(
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
		except Exception:
			log.exception(f"Could not restore master volume of process {pid} upon exit.")


def updateAppsVolumeImpl(
		volume: float,
		state: AppsVolumeAdjusterFlag,
		runTerminators: bool = True,
):
	global activeCallback
	if activeCallback is not None:
		activeCallback.unregister(runTerminators=runTerminators)
		activeCallback = None
	if state == AppsVolumeAdjusterFlag.DISABLED:
		activeCallback = DummyAudioSessionCallback()
	else:
		activeCallback = VolumeSetter(
			volumeAndMute=VolumeAndMute(
				volume=volume,
				mute=state == AppsVolumeAdjusterFlag.MUTED,
			)
		)
	activeCallback.register()


def adjustAppsVolume(
		volumeAdjustment: int | None = None,
):
	if not nvwave.usingWasapiWavePlayer():
		message = _(
			# Translators: error message when wasapi is turned off.
			"Other applications' volume cannot be adjusted. "
			"Please enable WASAPI in the Advanced category in NVDA Settings to use it."
		)
		ui.message(message)
		return
	volume: int = config.conf["audio"]["applicationsSoundVolume"]
	state = config.conf["audio"]["ApplicationsVolumeMode"]
	if state != AppsVolumeAdjusterFlag.ENABLED:
		# Translators: error message when applications' volume is disabled
		msg = _("Please enable applications' volume adjuster in order to adjust applications' volume")
		ui.message(msg)
		return
	volume += volumeAdjustment
	volume = max(0, min(100, volume))
	config.conf["audio"]["applicationsSoundVolume"] = volume

	# We skip running terminators here to avoid application volume spiking to 100% for a split second.
	updateAppsVolumeImpl(volume / 100.0, state, runTerminators=False)
	# Translators: Announcing new applications' volume message
	msg = _("Applications volume {}").format(volume)
	ui.message(msg)


APPS_VOLUME_STATES_ORDER = [
	AppsVolumeAdjusterFlag.DISABLED,
	AppsVolumeAdjusterFlag.ENABLED,
	AppsVolumeAdjusterFlag.MUTED,
]


def toggleAppsVolumeState():
	if not nvwave.usingWasapiWavePlayer():
		message = _(
			# Translators: error message when wasapi is turned off.
			"Other applications' volume cannot be adjusted. "
			"Please enable WASAPI in the Advanced category in NVDA Settings to use it."
		)
		ui.message(message)
		return
	state = config.conf["audio"]["ApplicationsVolumeMode"]
	volume: int = config.conf["audio"]["applicationsSoundVolume"]
	try:
		index = APPS_VOLUME_STATES_ORDER.index(state)
	except ValueError:
		index = -1
	index = (index + 1) % len(APPS_VOLUME_STATES_ORDER)
	state = APPS_VOLUME_STATES_ORDER[index]
	config.conf["audio"]["ApplicationsVolumeMode"] = state.name
	updateAppsVolumeImpl(volume / 100.0, state)
	ui.message(state.displayString)
