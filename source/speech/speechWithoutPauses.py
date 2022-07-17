# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2006-2021 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Babbage B.V., Bill Dengler,
# Julien Cochuyt

import re

from .commands import (
	# Commands that are used in this file.
	LangChangeCommand,
	EndUtteranceCommand,
)

from .types import (
	SpeechSequence,
	logBadSequenceTypes,
	GeneratorWithReturn,
)

from typing import (
	Optional,
	Generator,
	Callable,
)


def _yieldIfNonEmpty(seq: SpeechSequence):
	"""Helper method to yield the sequence if it is not None or empty."""
	if seq:
		yield seq


class SpeechWithoutPauses:
	_pendingSpeechSequence: SpeechSequence
	re_last_pause = re.compile(
		r"^(.*(?<=[^\s.!?])[.!?][\"'”’)]?(?:\s+|$))(.*$)",
		re.DOTALL | re.UNICODE
	)

	def __init__(
			self,
			speakFunc: Callable[[SpeechSequence], None]
	):
		"""
		:param speakFunc: Function used by L{speakWithoutPauses} to speak. This will likely be speech.speak.
		"""
		self.speak = speakFunc
		self.reset()

	def reset(self):
		self._pendingSpeechSequence = []

	def speakWithoutPauses(
			self,
			speechSequence: Optional[SpeechSequence],
			detectBreaks: bool = True
	) -> bool:
		"""
		Speaks the speech sequences given over multiple calls,
		only sending to the synth at acceptable phrase or sentence boundaries,
		or when given None for the speech sequence.
		@return: C{True} if something was actually spoken,
			C{False} if only buffering occurred.
		"""
		speech = GeneratorWithReturn(self.getSpeechWithoutPauses(
			speechSequence,
			detectBreaks
		))
		for seq in speech:
			self.speak(seq)
		return speech.returnValue

	def getSpeechWithoutPauses(  # noqa: C901
			self,
			speechSequence: Optional[SpeechSequence],
			detectBreaks: bool = True
	) -> Generator[SpeechSequence, None, bool]:
		"""
		Generate speech sequences over multiple calls,
		only returning a speech sequence at acceptable phrase or sentence boundaries,
		or when given None for the speech sequence.
		@return: The speech sequence that can be spoken without pauses. The 'return' for this generator function,
		is a bool which indicates whether this sequence should be considered valid speech. Use
		L{GeneratorWithReturn} to retain the return value. A generator is used because the previous
		implementation had several calls to speech, this approach replicates that.
		"""
		if speechSequence is not None:
			logBadSequenceTypes(speechSequence)
		# Break on all explicit break commands
		if detectBreaks and speechSequence:
			speech = GeneratorWithReturn(self._detectBreaksAndGetSpeech(speechSequence))
			yield from speech
			return speech.returnValue  # Don't fall through to flush / normal speech

		if speechSequence is None:  # Requesting flush
			pending = self._flushPendingSpeech()
			yield from _yieldIfNonEmpty(pending)
			return bool(pending)  # Don't fall through to handle normal speech

		# Handling normal speech
		speech = self._getSpeech(speechSequence)
		yield from _yieldIfNonEmpty(speech)
		return bool(speech)

	def _detectBreaksAndGetSpeech(
			self,
			speechSequence: SpeechSequence
	) -> Generator[SpeechSequence, None, bool]:
		lastStartIndex = 0
		sequenceLen = len(speechSequence)
		gotValidSpeech = False
		for index, item in enumerate(speechSequence):
			if isinstance(item, EndUtteranceCommand):
				if index > 0 and lastStartIndex < index:
					subSequence = speechSequence[lastStartIndex:index]
					yield from _yieldIfNonEmpty(
						self._getSpeech(subSequence)
					)
				yield from _yieldIfNonEmpty(
					self._flushPendingSpeech()
				)
				gotValidSpeech = True
				lastStartIndex = index + 1
		if lastStartIndex < sequenceLen:
			subSequence = speechSequence[lastStartIndex:]
			seq = self._getSpeech(subSequence)
			gotValidSpeech = bool(seq)
			yield from _yieldIfNonEmpty(seq)
		return gotValidSpeech

	def _flushPendingSpeech(self) -> SpeechSequence:
		"""
		@return: may be empty sequence
		"""
		# Place the last incomplete phrase in to finalSpeechSequence to be spoken now
		pending = self._pendingSpeechSequence
		self._pendingSpeechSequence = []
		return pending

	def _getSpeech(
			self,
			speechSequence: SpeechSequence
	) -> SpeechSequence:
		"""
		@return: May be an empty sequence
		"""
		finalSpeechSequence: SpeechSequence = []  # To be spoken now
		pendingSpeechSequence: speechSequence = []  # To be saved off for speaking later
		# Scan the given speech and place all completed phrases in finalSpeechSequence to be spoken,
		# And place the final incomplete phrase in pendingSpeechSequence
		for index in range(len(speechSequence) - 1, -1, -1):
			item = speechSequence[index]
			if isinstance(item, str):
				m = self.re_last_pause.match(item)
				if m:
					before, after = m.groups()
					if after:
						pendingSpeechSequence.append(after)
					if before:
						finalSpeechSequence.extend(self._flushPendingSpeech())
						finalSpeechSequence.extend(speechSequence[0:index])
						finalSpeechSequence.append(before)
						# Apply the last language change to the pending sequence.
						# This will need to be done for any other speech change commands introduced in future.
						for changeIndex in range(index - 1, -1, -1):
							change = speechSequence[changeIndex]
							if not isinstance(change, LangChangeCommand):
								continue
							pendingSpeechSequence.append(change)
							break
						break
				else:
					pendingSpeechSequence.append(item)
			else:
				pendingSpeechSequence.append(item)
		if pendingSpeechSequence:
			pendingSpeechSequence.reverse()
			self._pendingSpeechSequence.extend(pendingSpeechSequence)
		return finalSpeechSequence
