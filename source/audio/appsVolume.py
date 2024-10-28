# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited, Tony Malykh, Bill Dengler
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import globalVars
from logHandler import log
import nvwave
from pycaw.utils import AudioSession
import ui
from dataclasses import dataclass
from threading import Lock
from typing import NamedTuple
from .utils import AudioSessionCallback, DummyAudioSessionCallback
from comtypes import COMError


class VolumeAndMute(NamedTuple):
	volume: float
	mute: bool


_appVolumesCache: dict[int, VolumeAndMute] = {}
_appVolumesCacheLock = Lock()
_activeCallback: DummyAudioSessionCallback | None = None
_appVolumeState: VolumeAndMute = VolumeAndMute(100.0, False)


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
	muted: bool,
):
	global _activeCallback
	newCallback = VolumeSetter(
		volumeAndMute=VolumeAndMute(
			volume=volume,
			mute=muted,
		)
	)
	runTerminators = False
	if _activeCallback is not None:
		_activeCallback.unregister(runTerminators=runTerminators)
	_activeCallback = newCallback
	_activeCallback.register()


_WASAPI_DISABLED_MESSAGE: str = _(
	# Translators: error message when wasapi is turned off.
	"Application volume cannot be controlled by NVDA when WASAPI is disabled. "
	"Please enable it in the advanced settings panel.",
)


def _adjustAppsVolume(
	volumeAdjustment: int | None = None,
):
	global _appVolumeState
	volume = _appVolumeState.volume
	muted = _appVolumeState.mute
	if not nvwave.usingWasapiWavePlayer():
		ui.message(_WASAPI_DISABLED_MESSAGE)
		return
	if volumeAdjustment is not None:
		volume += volumeAdjustment
		volume = max(0, min(100, volume))
	log.debug(f"Adjusting applications volume by {volumeAdjustment}% to {volume}%")

	# We skip running terminators here to avoid application volume spiking to 100% for a split second.
	_updateAppsVolumeImpl(volume / 100.0, muted)
	_appVolumeState = VolumeAndMute(volume, muted)
	# Translators: Announcing new applications' volume message
	msg = _("{} percent application volume").format(volume)
	ui.message(msg)


def _toggleAppsVolumeMute():
	global _appVolumeState
	if not nvwave.usingWasapiWavePlayer():
		ui.message(_WASAPI_DISABLED_MESSAGE)
		return
	volume = _appVolumeState.volume
	muted = not _appVolumeState.mute
	_updateAppsVolumeImpl(volume / 100.0, muted)
	if muted:
		# Translators: Announcing new applications' mute status message
		msg = _("Muted other applications")
	else:
		# Translators: Announcing new applications' mute status message
		msg = _("Unmuted other applications")
	ui.message(msg)
	_appVolumeState = VolumeAndMute(volume, muted)
