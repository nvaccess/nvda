# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019 NV Access Limited

"""Types used by speech package.
Kept here so they can be re-used without having to worry about circular imports.
"""

from collections.abc import Sequence
from typing import (
	Union,
	Iterable,
	Any,
	Optional,
	Generator,
)

import config
from logHandler import log
from .commands import SpeechCommand

SequenceItemT = Union[SpeechCommand, str]
SpeechSequence = list[SequenceItemT]
SpeechIterable = Iterable[SequenceItemT]

_IndexT = int  # Type for indexes.


def _isDebugForSpeech() -> bool:
	"""Check if debug logging for speech is enabled."""
	return config.conf["debugLog"]["speech"]


class GeneratorWithReturn(Iterable):
	"""Helper class, used with generator functions to access the 'return' value after there are no more values
	to iterate over.
	"""

	def __init__(self, gen: Iterable, defaultReturnValue=None):
		self.gen = gen
		self.returnValue = defaultReturnValue
		self.iterationFinished = False

	def __iter__(self):
		self.returnValue = yield from self.gen
		self.iterationFinished = True


def _flattenNestedSequences(
	nestedSequences: Union[Iterable[SpeechSequence], GeneratorWithReturn],
) -> Generator[SequenceItemT, Any, Optional[bool]]:
	"""Turns [[a,b,c],[d,e]] into [a,b,c,d,e]"""
	yield from (i for seq in nestedSequences for i in seq)
	if isinstance(nestedSequences, GeneratorWithReturn):
		return nestedSequences.returnValue
	return None


def logBadSequenceTypes(sequence: SpeechIterable, raiseExceptionOnError=False) -> bool:
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

	# Check the type of the container
	if not isinstance(sequence, Sequence):
		log.error(
			f"Unexpected Sequence Type: {type(sequence)!r} supplied, a {SpeechSequence!r} is required.",
			stack_info=True,
		)
		if raiseExceptionOnError:
			raise ValueError("Unexpected type in speech sequence")
		return False

	# Check each items type
	for value in sequence:
		if not isinstance(value, (SpeechCommand, str)):
			log.error(f"Unexpected Item Type: {value!r}", stack_info=True)
			if raiseExceptionOnError:
				raise ValueError("Unexpected type in speech sequence")
			return False
	return True
