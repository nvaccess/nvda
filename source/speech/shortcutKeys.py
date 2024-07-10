# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023 NV Access Limited, Cyrille Bougot

"""Functions to create speech sequences for shortcut keys."""

import re

import characterProcessing
from logHandler import log
from synthDriverHandler import getSynth
import config

from .commands import CharacterModeCommand
from .types import SpeechSequence
from typing import (
	Optional,
	List,
	Tuple,
)


def speakKeyboardShortcuts(keyboardShortcutsStr: Optional[str]) -> None:
	from .speech import speak

	speak(getKeyboardShortcutsSpeech(keyboardShortcutsStr))


def getKeyboardShortcutsSpeech(keyboardShortcutsStr: Optional[str]) -> SpeechSequence:
	"""Gets the speech sequence for a shortcuts string containing one or more shortcuts.
	@param keyboardShortcutsStr: the shortcuts string.
	"""

	SHORTCUT_KEY_LIST_SEPARATOR = "  "
	seq = []
	if not keyboardShortcutsStr:
		return seq
	try:
		for shortcutKeyStr in keyboardShortcutsStr.split(SHORTCUT_KEY_LIST_SEPARATOR):
			seq.extend(_getKeyboardShortcutSpeech(shortcutKeyStr))
			seq.append(SHORTCUT_KEY_LIST_SEPARATOR)
		seq.pop()  # Remove last SHORTCUT_KEY_LIST_SEPARATOR in the sequence
	except Exception:
		log.warning(
			f'Error parsing keyboard shortcut "{keyboardShortcutsStr}", reporting the string as a fallback.',
			exc_info=True,
		)
		return [keyboardShortcutsStr]

	# Merge consecutive strings in the list when possible
	seqOut = []
	for item in seq:
		if len(seqOut) > 0 and isinstance(seqOut[-1], str) and isinstance(item, str):
			seqOut[-1] = seqOut[-1] + item
		else:
			seqOut.append(item)

	return seqOut


def _getKeyboardShortcutSpeech(keyboardShortcut: str) -> SpeechSequence:
	"""Gets the speech sequence for a single shortcut string.
	@param keyboardShortcut: the shortcuts string.
	"""

	if ", " in keyboardShortcut:
		keyList, separators = _splitSequentialShortcut(keyboardShortcut)
	elif "+" in keyboardShortcut and len(keyboardShortcut) > 1:
		keyList, separator = _splitShortcut(keyboardShortcut)
		separators = [separator] * (len(keyList) - 1)
	else:
		return _getKeySpeech(keyboardShortcut)

	seq = []
	for key, sep in zip(keyList[:-1], separators):
		seq.extend(_getKeySpeech(key))
		seq.append(sep)
	seq.extend(_getKeySpeech(keyList[-1]))
	return seq


def shouldUseSpellingFunctionality() -> bool:
	synth = getSynth()
	return config.conf["speech"][synth.name]["useSpellingFunctionality"]


def _getKeySpeech(key: str) -> SpeechSequence:
	"""Gets the speech sequence for a string describing a key.
	@param key: the key string.
	"""

	if len(key) > 1:
		return [key]
	from .speech import getCurrentLanguage

	locale = getCurrentLanguage()
	keySymbol = characterProcessing.processSpeechSymbol(locale, key)
	if keySymbol != key:
		return [keySymbol]
	if not shouldUseSpellingFunctionality():
		return [key]
	return [
		CharacterModeCommand(True),
		key,
		CharacterModeCommand(False),
	]


def _splitShortcut(shortcut: str) -> Tuple[List[str], str]:
	"""Splits a string representing a shortcut key combination.
	@param shortcut: the shortcut to split.
		It may be of the form "NVDA+R" or "NVDA + R", i.e. key names separated by "+" symbol with or without
		space around it.
	@return: 2-tuple containing the list of the keys and the separator used between them.
		E.g. (['NVDA', 'R'], ' + ')
	"""

	if " + " in shortcut:
		separator = " + "
	elif "+" in shortcut:
		separator = "+"
	else:
		raise RuntimeError(f'The shortcut "{shortcut}" needs to contain a "+" symbol.')
	if shortcut[-1] == "+":  # E.g. "Ctrl+Shift++"
		keyList = shortcut[:-1].split(separator)
		keyList[-1] = keyList[-1] + "+"
	else:
		keyList = shortcut.split(separator)
	return keyList, separator


def _splitSequentialShortcut(shortcut: str) -> Tuple[List[str], List[str]]:
	"""Splits a string representing a sequantial shortcut key combination (the ones found in ribbons).
	@param shortcut: the shortcut to split.
		It should be of the form "Alt, F, L, Y 1" i.e. key names separated by comma symbol or space.
	@return: 2-tuple containing the list of the keys and the list separators used between each key in the list.
		E.g.: (['Alt', 'F', 'L', 'Y', '1'], [', ', ', ', ', ', ' '])
	"""

	keys = []
	separators = []
	RE_SEQ_SHORTCUT_SPLITTING = re.compile(r"^(?P<key>[^, ]+)(?P<sep> |, )(?P<tail>.+)")
	tail = shortcut
	while len(tail) > 0:
		m = RE_SEQ_SHORTCUT_SPLITTING.match(tail)
		if not m:
			keys.append(tail)
			return keys, separators
		keys.append(m["key"])
		separators.append(m["sep"])
		tail = m["tail"]
	raise RuntimeError(f"Wrong sequential shortcut string format: {shortcut}")
