# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019 NV Access Limited

"""Types used by speech package.
Kept here so they can be re-used without having to worry about circular imports.
"""
from typing import Union, List

import config
from logHandler import log
from .commands import SpeechCommand

SequenceItemT = Union[SpeechCommand, str]
SpeechSequence = List[SequenceItemT]


def _isDebugForSpeech() -> bool:
	"""Check if debug logging for speech is enabled."""
	return config.conf["debugLog"]["speech"]


def logBadSequenceTypes(sequence: SpeechSequence, raiseExceptionOnError=False) -> bool:
	"""
		Check if the provided sequence is valid, otherwise log an error (only if speech is
		checked in the "log categories" setting of the advanced settings panel.
		@param sequence: the sequence to check
		@param raiseExceptionOnError: if True, and exception is raised. Useful to help track down the introduction
			of erroneous speechSequence data.
		@return: True if the sequence is valid.
	"""
	if not _isDebugForSpeech():
		return True
	for value in sequence:
		if not isinstance(value, (SpeechCommand, str)):
			log.error(f"unexpectedType: {value!r}", stack_info=True)
			if raiseExceptionOnError:
				raise ValueError("Unexpected type in speech sequence")
			return False
	return True
