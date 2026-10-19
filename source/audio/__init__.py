# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from logHandler import log

from .soundSplitState import SoundSplitState

try:
	from . import soundSplit
except (ImportError, OSError):
	log.warning("Sound Split is unavailable.", exc_info=True)
	soundSplit = None

SOUND_SPLIT_AVAILABLE: bool = soundSplit is not None
"""True if the dependencies required for Sound Split are available."""

__all__ = [
	"SOUND_SPLIT_AVAILABLE",
	"SoundSplitState",
	"_setSoundSplitState",
	"_toggleSoundSplitState",
	"initialize",
	"terminate",
]


def initialize() -> None:
	if soundSplit is not None:
		soundSplit.initialize()


def terminate() -> None:
	if soundSplit is not None:
		soundSplit.terminate()


def _setSoundSplitState(state: SoundSplitState, initial: bool = False) -> dict[str, bool]:
	if soundSplit is None:
		return {}
	return soundSplit._setSoundSplitState(state, initial)


def _toggleSoundSplitState() -> None:
	if soundSplit is None:
		import ui

		# Translators: Message announced when Sound Split is unavailable.
		ui.message(_("Sound Split is unavailable."))
		return
	soundSplit._toggleSoundSplitState()
