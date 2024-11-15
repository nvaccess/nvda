# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from .soundSplit import (
	SoundSplitState,
	_setSoundSplitState,
	_toggleSoundSplitState,
)
from . import appsVolume, soundSplit, utils
import atexit
import nvwave
from pycaw.utils import AudioUtilities
from comtypes import COMError
from logHandler import log

__all__ = [
	"SoundSplitState",
	"_setSoundSplitState",
	"_toggleSoundSplitState",
]

audioUtilitiesInitialized: bool = False


def initialize() -> None:
	if nvwave.usingWasapiWavePlayer():
		try:
			AudioUtilities.GetAudioSessionManager()
		except COMError:
			log.exception("Could not initialize audio session manager")
			return
		log.debug("Initializing utils")
		utils.initialize()
		log.debug("Initializing appsVolume")
		appsVolume.initialize()
		log.debug("Initializing soundSplit")
		soundSplit.initialize()
		global audioUtilitiesInitialized
		audioUtilitiesInitialized = True
	else:
		log.debug("Cannot initialize audio utilities as WASAPI is disabled")


@atexit.register
def terminate():
	if not audioUtilitiesInitialized:
		log.debug("Skipping terminating audio utilities as initialization was skipped.")
	elif not nvwave.usingWasapiWavePlayer():
		log.debug("Skipping terminating audio utilites as WASAPI is disabled.")
	else:
		soundSplit.terminate()
		appsVolume.terminate()
		utils.terminate()
