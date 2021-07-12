# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019-2021 NV Access Limited

"""Unit tests for SpeechWithoutPauses"""

import unittest
from typing import List

from speech.types import SpeechSequence
from speech.commands import EndUtteranceCommand, LangChangeCommand, CallbackCommand
from speech.speechWithoutPauses import SpeechWithoutPauses
from logHandler import log


class SpeechSpy:
	"""Simple class to collect SpeechSequences as they are 'spoken'
	"""
	spokenSequences: List[
		SpeechSequence
	]

	def __init__(self):
		self.spokenSequences = []

	def speak(
			self,
			speechSeqence: SpeechSequence
	):
		self.spokenSequences.append(speechSeqence)


_spokenSequences: List[
	SpeechSequence
] = []


def speak(seq: SpeechSequence):
	_spokenSequences.append(seq)


def resetSpeakDest():
	""" Save calls to speak.
	:return the new destination for the speak function
	"""
	global _spokenSequences
	_spokenSequences = []
	return _spokenSequences


def old_speakWithoutPauses(  # noqa: C901
		speechSequence: SpeechSequence,
		detectBreaks: bool = True
) -> bool:
	"""
	Speaks the speech sequences given over multiple calls, only sending to the synth at acceptable phrase or
	sentence boundaries, or when given None for the speech sequence.
	@return: C{True} if something was actually spoken,
		C{False} if only buffering occurred.
	"""
	speakWithoutPauses = old_speakWithoutPauses
	lastStartIndex = 0
	# Break on all explicit break commands
	if detectBreaks and speechSequence:
		log.debug(f"start with seq: {speechSequence}\n and pending: {speakWithoutPauses._pendingSpeechSequence}")
		sequenceLen = len(speechSequence)
		spoke = False
		for index in range(sequenceLen):
			if isinstance(speechSequence[index], EndUtteranceCommand):
				if index > 0 and lastStartIndex < index:
					speakWithoutPauses(speechSequence[lastStartIndex:index], detectBreaks=False)
				speakWithoutPauses(None)
				spoke = True
				lastStartIndex = index + 1
		if lastStartIndex < sequenceLen:
			spoke = speakWithoutPauses(speechSequence[lastStartIndex:], detectBreaks=False)
		return spoke
	finalSpeechSequence = []  # To be spoken now
	pendingSpeechSequence = []  # To be saved off for speaking  later
	if speechSequence is None:  # Requesting flush
		if speakWithoutPauses._pendingSpeechSequence:
			# Place the last incomplete phrase in to finalSpeechSequence to be spoken now
			finalSpeechSequence = speakWithoutPauses._pendingSpeechSequence
			speakWithoutPauses._pendingSpeechSequence = []
	else:  # Handling normal speech
		# Scan the given speech and place all completed phrases in finalSpeechSequence to be spoken,
		# And place the final incomplete phrase in pendingSpeechSequence
		for index in range(len(speechSequence) - 1, -1, -1):
			item = speechSequence[index]
			if isinstance(item, str):
				m = SpeechWithoutPauses.re_last_pause.match(item)
				if m:
					before, after = m.groups()
					if after:
						pendingSpeechSequence.append(after)
					if before:
						finalSpeechSequence.extend(speakWithoutPauses._pendingSpeechSequence)
						speakWithoutPauses._pendingSpeechSequence = []
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
			speakWithoutPauses._pendingSpeechSequence.extend(pendingSpeechSequence)
	if finalSpeechSequence:
		speak(finalSpeechSequence)
		return True
	return False


old_speakWithoutPauses._pendingSpeechSequence = []


class TestOldImplVsNew(unittest.TestCase):
	"""A test that verifies that the new implementation of SpeechWithoutPauses matches the old behavior.
	"""
	def test_stopsSpeakingCase(self):
		callbackCommand = CallbackCommand(name="dummy", callback=None)
		lang_en = LangChangeCommand('en')
		lang_default = LangChangeCommand(None)

		def createInputSequences():
			"""Speech sequences that are input to 'speechWithoutPauses' when triggering the 'read-all' command
			on the wxPython wiki page.
			"""
			return [
				[
					callbackCommand,
					lang_en,
					'The purpose of the wxPyWiki is to provide documentation, examples, how-tos, etc. for helping people ',
					lang_default
				],
				[
					callbackCommand,
					lang_en,
					'learn, understand and use ',
					lang_default
				],
				[
					callbackCommand,
					'visited',
					'link',
					'',
					lang_en,
					'wxPython',
					lang_default,
					lang_en,
					'. Anything that falls within those guidelines is fair game. ',
					lang_default
				],
				[
					EndUtteranceCommand(),
					callbackCommand,
					lang_en,
					'Note: To get to the main wxPython site click ',
					lang_default
				]
			]

		expectedSpeech = repr(
			[
				[
					callbackCommand,
					lang_en,
					'The purpose of the wxPyWiki is to provide documentation, examples, how-tos, etc. ',
				],
				'spoke:True',
				'spoke:False',
				[
					lang_en,
					'for helping people ',
					lang_default,
					callbackCommand,
					lang_en,
					'learn, understand and use ',
					lang_default,
					callbackCommand,
					'visited',
					'link',
					'',
					lang_en,
					'wxPython',
					lang_default,
					lang_en,
					'. Anything that falls within those guidelines is fair game. '
				],
				'spoke:True',
				[
					# this sequence seems incorrect, however it persists the "old" behavior:
					# - it is missing a callback command
					# - it has no speech, just a meaningless pair of lang change commands
					lang_en, lang_default
				],
				'spoke:False'
			]
		)

		oldSpeech = resetSpeakDest()
		for seq in createInputSequences():
			spoke = old_speakWithoutPauses(seq)
			oldSpeech.append(f"spoke:{spoke}")

		self.maxDiff = 5000  # text comparison is quite long, and it is handy to be able to see it in the output.
		self.assertMultiLineEqual(repr(oldSpeech), expectedSpeech, "generated old speech vs expected")

		newSpeech = resetSpeakDest()
		_speakWithoutPauses = SpeechWithoutPauses(speak)
		for inSeq in createInputSequences():
			spoke = _speakWithoutPauses.speakWithoutPauses(inSeq)
			newSpeech.append(f"spoke:{spoke}")

		self.assertMultiLineEqual(repr(newSpeech), expectedSpeech, "generated new speech vs expected")
