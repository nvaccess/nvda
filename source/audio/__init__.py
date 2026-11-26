# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024-2026 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from logHandler import log
from utils.security import isRunningOnSecureDesktop

from .soundSplitState import SoundSplitState

try:
	from . import soundSplit
except (ImportError, OSError):
	log.warning("Sound Split is unavailable.", exc_info=True)
	soundSplit = None

__all__ = [
	"SOUND_SPLIT_AVAILABLE",
	"SoundSplitState",
	"_setSoundSplitState",
	"_toggleSoundSplitState",
	"initialize",
	"terminate",
]

SOUND_SPLIT_AVAILABLE: bool = soundSplit is not None
"""True if the dependencies required for Sound Split are available."""


def _isSoundSplitBlocked() -> bool:
	"""Whether Sound Split must not change application volumes in this copy of NVDA.

	Sound Split is disabled on secure screens (#19872).
	The copy of NVDA running on a secure screen changes the volume of every audio session in the Windows session,
	including applications on the user's desktop.
	Those changes would remain after returning to the user's desktop,
	and could conflict with the Sound Split state of the copy of NVDA running there.
	"""
	return soundSplit is None or isRunningOnSecureDesktop()


def initialize() -> None:
	if not _isSoundSplitBlocked():
		soundSplit.initialize()


def terminate() -> None:
	if not _isSoundSplitBlocked():
		soundSplit.terminate()


def _setSoundSplitState(state: SoundSplitState, initial: bool = False) -> dict[str, bool]:
	if _isSoundSplitBlocked():
		return {}
	return soundSplit._setSoundSplitState(state, initial)


def _toggleSoundSplitState() -> None:
	if soundSplit is None:
		import ui

		# Translators: Message announced when Sound Split is unavailable.
		ui.message(_("Sound Split is unavailable."))
		return
	if isRunningOnSecureDesktop():
		import ui
		from gui.blockAction import Context

		ui.message(Context.SECURE_SCREEN.translatedMessage)
		return
	soundSplit._toggleSoundSplitState()
