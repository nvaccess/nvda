# -*- coding: UTF-8 -*-
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2019 NV Access Limited
from typing import cast, Dict, Any, List, Tuple

from logHandler import log
import queueHandler
import synthDriverHandler
from .types import SpeechSequence
from .commands import *
from .commands import IndexCommand
from .priorities import Spri, SPEECH_PRIORITIES

class ParamChangeTracker(object):
	"""Keeps track of commands which change parameters from their defaults.
	This is useful when an utterance needs to be split.
	As you are processing a sequence,
	you update the tracker with a parameter change using the L{update} method.
	When you split the utterance, you use the L{getChanged} method to get
	the parameters which have been changed from their defaults.
	"""

	def __init__(self):
		self._commands = {}

	def update(self, command):
		"""Update the tracker with a parameter change.
		@param command: The parameter change command.
		@type command: L{SynthParamCommand}
		"""
		paramType = type(command)
		if command.isDefault:
			# This no longer applies.
			self._commands.pop(paramType, None)
		else:
			self._commands[paramType] = command

	def getChanged(self):
		"""Get the commands for the parameters which have been changed from their defaults.
		@return: List of parameter change commands.
		@type: list of L{SynthParamCommand}
		"""
		return list(self._commands.values())

class _ManagerPriorityQueue(object):
	"""A speech queue for a specific priority.
	This is intended for internal use by L{_SpeechManager} only.
	Each priority has a separate queue.
	It holds the pending speech sequences to be spoken,
	as well as other information necessary to restore state when this queue
	is preempted by a higher priority queue.
	"""

	def __init__(self, priority: Spri):
		self.priority = priority
		#: The pending speech sequences to be spoken.
		#: These are split at indexes,
		#: so a single utterance might be split over multiple sequences.
		self.pendingSequences: List[SpeechSequence] = []
		#: The configuration profile triggers that have been entered during speech.
		self.enteredProfileTriggers: List[config.ProfileTrigger] = []
		#: Keeps track of parameters that have been changed during an utterance.
		self.paramTracker: ParamChangeTracker = ParamChangeTracker()

class SpeechManager(object):
	"""Manages queuing of speech utterances, calling callbacks at desired points in the speech, profile switching, prioritization, etc.
	This is intended for internal use only.
	It is used by higher level functions such as L{speak}.

	The high level flow of control is as follows:
	1. A speech sequence is queued with L{speak}, which in turn calls L{_queueSpeechSequence}.
	2. L{_processSpeechSequence} is called to normalize, process and split the input sequence.
		It converts callbacks to indexes.
		All indexing is assigned and managed by this class.
		It maps any indexes to their corresponding callbacks.
		It splits the sequence at indexes so we easily know what has completed speaking.
		If there are end utterance commands, the sequence is split at that point.
		We ensure there is an index at the end of all utterances so we know when they've finished speaking.
		We ensure any config profile trigger commands are preceded by an utterance end.
		Parameter changes are re-applied after utterance breaks.
		We ensure any entered profile triggers are exited at the very end.
	3. L{_queueSpeechSequence} places these processed sequences in the queue
		for the priority specified by the caller in step 1.
		There is a separate queue for each priority.
	4. L{_pushNextSpeech} is called to begin pushing speech.
		It looks for the highest priority queue with pending speech.
		Because there's no other speech queued, that'll be the queue we just touched.
	5. If the input begins with a profile switch, it is applied immediately.
	6. L{_buildNextUtterance} is called to build a full utterance and it is sent to the synth.
	7. For every index reached, L{_handleIndex} is called.
		The completed sequence is removed from L{_pendingSequences}.
		If there is an associated callback, it is run.
		If the index marks the end of an utterance, L{_pushNextSpeech} is called to push more speech.
	8. If there is another utterance before a profile switch, it is built and sent as per steps 6 and 7.
	9. In L{_pushNextSpeech}, if a profile switch is next, we wait for the synth to finish speaking before pushing more.
		This is because we don't want to start speaking too early with a different synth.
		L{_handleDoneSpeaking} is called when the synth finishes speaking.
		It pushes more speech, which includes applying the profile switch.
	10. The flow then repeats from step 6 onwards until there are no more pending sequences.
	11. If another sequence is queued via L{speak} during speech,
		it is processed and queued as per steps 2 and 3.
	12. If this is the first utterance at priority now, speech is interrupted
		and L{_pushNextSpeech} is called.
		Otherwise, L{_pushNextSpeech} is called when the current utterance completes
		as per step 7.
	13. When L{_pushNextSpeech} is next called, it looks for the highest priority queue with pending speech.
		If that priority is different to the priority of the utterance just spoken,
		any relevant profile switches are applied to restore the state for this queue.
	14. If a lower priority utterance was interrupted in the middle,
		L{_buildNextUtterance} applies any parameter changes that applied before the interruption.
	15. The flow then repeats from step 6 onwards until there are no more pending sequences.

	Note:
	All of this activity is (and must be) synchronized and serialized on the main thread.
	"""
	_priQueues: Dict[Any, _ManagerPriorityQueue]
	_curPriQueue: Optional[_ManagerPriorityQueue]

	def __init__(self):
		#: A counter for indexes sent to the synthesizer for callbacks, etc.
		self._indexCounter = self._generateIndexes()
		self._reset()
		synthDriverHandler.synthIndexReached.register(self._onSynthIndexReached)
		synthDriverHandler.synthDoneSpeaking.register(self._onSynthDoneSpeaking)

	#: Maximum index number to pass to synthesizers.
	MAX_INDEX = 9999
	def _generateIndexes(self):
		"""Generator of index numbers.
		We don't want to reuse index numbers too quickly,
		as there can be race conditions when cancelling speech which might result
		in an index from a previous utterance being treated as belonging to the current utterance.
		However, we don't want the counter increasing indefinitely,
		as some synths might not be able to handle huge numbers.
		Therefore, we use a counter which starts at 1, counts up to L{MAX_INDEX},
		wraps back to 1 and continues cycling thus.
		This maximum is arbitrary, but
		it's small enough that any synth should be able to handle it
		and large enough that previous indexes won't reasonably get reused
		in the same or previous utterance.
		"""
		while True:
			for index in range(1, self.MAX_INDEX + 1):
				yield index

	def _reset(self):
		#: The queues for each priority.
		self._priQueues = {}
		#: The priority queue for the utterance currently being spoken.
		self._curPriQueue = None
		#: Maps indexes to BaseCallbackCommands.
		self._indexesToCallbacks = {}
		#: a list of indexes currently being spoken by the synthesizer
		self._indexesSpeaking = []
		#: Whether to push more speech when the synth reports it is done speaking.
		self._shouldPushWhenDoneSpeaking = False

	def speak(self, speechSequence: SpeechSequence, priority: Spri):
		# If speech isn't already in progress, we need to push the first speech.
		push = self._curPriQueue is None
		interrupt = self._queueSpeechSequence(speechSequence, priority)
		if interrupt:
			getSynth().cancel()
			push = True
		if push:
			self._pushNextSpeech(True)

	def _queueSpeechSequence(self, inSeq: SpeechSequence, priority: Spri):
		"""
		@return: Whether to interrupt speech.
		@rtype: bool
		"""
		outSeq = self._processSpeechSequence(inSeq)
		queue = self._priQueues.get(priority)
		if not queue:
			queue = self._priQueues[priority] = _ManagerPriorityQueue(priority)
		first = len(queue.pendingSequences) == 0
		queue.pendingSequences.extend(outSeq)
		if priority is Spri.NOW and first:
			# If this is the first sequence at Spri.NOW, interrupt speech.
			return True
		return False

	def _processSpeechSequence(self, inSeq: SpeechSequence):
		paramTracker = ParamChangeTracker()
		enteredTriggers = []
		outSeqs = []

		def ensureEndUtterance(seq: SpeechSequence):
			# We split at EndUtteranceCommands so the ends of utterances are easily found.
			if seq:
				# There have been commands since the last split.
				outSeqs.append(seq)
				lastOutSeq = seq
				# Re-apply parameters that have been changed from their defaults.
				seq = paramTracker.getChanged()
			else:
				lastOutSeq = outSeqs[-1] if outSeqs else None
			lastCommand = lastOutSeq[-1] if lastOutSeq else None
			if not lastCommand or isinstance(lastCommand, (EndUtteranceCommand, ConfigProfileTriggerCommand)):
				# It doesn't make sense to start with or repeat EndUtteranceCommands.
				# We also don't want an EndUtteranceCommand immediately after a ConfigProfileTriggerCommand.
				return seq
			if not isinstance(lastCommand, IndexCommand):
				# Add an index so we know when we've reached the end of this utterance.
				speechIndex = next(self._indexCounter)
				lastOutSeq.append(IndexCommand(speechIndex))
			outSeqs.append([EndUtteranceCommand()])
			return seq

		outSeq = []
		for command in inSeq:
			if isinstance(command, BaseCallbackCommand):
				# When the synth reaches this point, we want to call the callback.
				speechIndex = next(self._indexCounter)
				outSeq.append(IndexCommand(speechIndex))
				self._indexesToCallbacks[speechIndex] = command
				# We split at indexes so we easily know what has completed speaking.
				outSeqs.append(outSeq)
				outSeq = []
				continue
			if isinstance(command, ConfigProfileTriggerCommand):
				if not command.trigger.hasProfile:
					# Ignore triggers that have no associated profile.
					continue
				if command.enter and command.trigger in enteredTriggers:
					log.debugWarning("Request to enter trigger which has already been entered: %r" % command.trigger.spec)
					continue
				if not command.enter and command.trigger not in enteredTriggers:
					log.debugWarning("Request to exit trigger which wasn't entered: %r" % command.trigger.spec)
					continue
				outSeq = ensureEndUtterance(outSeq)
				outSeqs.append([command])
				if command.enter:
					enteredTriggers.append(command.trigger)
				else:
					enteredTriggers.remove(command.trigger)
				continue
			if isinstance(command, EndUtteranceCommand):
				outSeq = ensureEndUtterance(outSeq)
				continue
			if isinstance(command, SynthParamCommand):
				paramTracker.update(command)
			outSeq.append(command)
		# Add the last sequence and make sure the sequence ends the utterance.
		ensureEndUtterance(outSeq)
		# Exit any profile triggers the caller didn't exit.
		for trigger in reversed(enteredTriggers):
			command = ConfigProfileTriggerCommand(trigger, False)
			outSeqs.append([command])
		return outSeqs

	def _pushNextSpeech(self, doneSpeaking: bool):
		queue = self._getNextPriority()
		if not queue:
			# No more speech.
			self._curPriQueue = None
			return
		if not self._curPriQueue:
			# First utterance after no speech.
			self._curPriQueue = queue
		elif queue.priority > self._curPriQueue.priority:
			# Preempted by higher priority speech.
			if self._curPriQueue.enteredProfileTriggers:
				if not doneSpeaking:
					# Wait for the synth to finish speaking.
					# _handleDoneSpeaking will call us again.
					self._shouldPushWhenDoneSpeaking = True
					return
				self._exitProfileTriggers(self._curPriQueue.enteredProfileTriggers)
			self._curPriQueue = queue
		elif queue.priority < self._curPriQueue.priority:
			# Resuming a preempted, lower priority queue.
			if queue.enteredProfileTriggers:
				if not doneSpeaking:
					# Wait for the synth to finish speaking.
					# _handleDoneSpeaking will call us again.
					self._shouldPushWhenDoneSpeaking = True
					return
				self._restoreProfileTriggers(queue.enteredProfileTriggers)
			self._curPriQueue = queue
		while queue.pendingSequences and isinstance(queue.pendingSequences[0][0], ConfigProfileTriggerCommand):
			if not doneSpeaking:
				# Wait for the synth to finish speaking.
				# _handleDoneSpeaking will call us again.
				self._shouldPushWhenDoneSpeaking = True
				return
			self._switchProfile()
		if not queue.pendingSequences:
			# The last commands in this queue were profile switches.
			# Call this method again in case other queues are waiting.
			return self._pushNextSpeech(True)
		seq = self._buildNextUtterance()
		if seq:
			# Record all indexes that will be sent to the synthesizer
			# So that we can handle any accidentally skipped indexes.
			for item in seq:
				if isinstance(item, IndexCommand):
					self._indexesSpeaking.append(item.index)
			getSynth().speak(seq)

	def _getNextPriority(self):
		"""Get the highest priority queue containing pending speech.
		"""
		for priority in SPEECH_PRIORITIES:
			queue = self._priQueues.get(priority)
			if not queue:
				continue
			if queue.pendingSequences:
				return queue
		return None

	def _buildNextUtterance(self):
		"""Since an utterance might be split over several sequences,
		build a complete utterance to pass to the synth.
		"""
		utterance = []
		# If this utterance was preempted by higher priority speech,
		# apply any parameters changed before the preemption.
		params = self._curPriQueue.paramTracker.getChanged()
		utterance.extend(params)
		for seq in self._curPriQueue.pendingSequences:
			if isinstance(seq[0], EndUtteranceCommand):
				# The utterance ends here.
				break
			utterance.extend(seq)
		return utterance

	def _onSynthIndexReached(self, synth=None, index=None):
		if synth != getSynth():
			return
		# This needs to be handled in the main thread.
		queueHandler.queueFunction(queueHandler.eventQueue, self._handleIndex, index)

	def _removeCompletedFromQueue(self, index: int) -> Tuple[bool, bool]:
		"""Removes completed speech sequences from the queue.
		@param index: The index just reached indicating a completed sequence.
		@return: Tuple of (valid, endOfUtterance),
			where valid indicates whether the index was valid and
			endOfUtterance indicates whether this sequence was the end of the current utterance.
		@rtype: (bool, bool)
		"""
		# Find the sequence that just completed speaking.
		if not self._curPriQueue:
			# No speech in progress. Probably from a previous utterance which was cancelled.
			return False, False
		for seqIndex, seq in enumerate(self._curPriQueue.pendingSequences):
			lastCommand = seq[-1] if isinstance(seq, list) else None
			if isinstance(lastCommand, IndexCommand):
				if index > lastCommand.index:
					log.debugWarning(f"Reached speech index {index :d}, but index {lastCommand.index :d} never handled")
				elif index == lastCommand.index:
					endOfUtterance = isinstance(self._curPriQueue.pendingSequences[seqIndex + 1][0], EndUtteranceCommand)
					if endOfUtterance:
						# Remove the EndUtteranceCommand as well.
						seqIndex += 1
					break # Found it!
		else:
			# Unknown index. Probably from a previous utterance which was cancelled.
			return False, False
		if endOfUtterance:
			# These params may not apply to the next utterance if it was queued separately,
			# so reset the tracker.
			# The next utterance will include the commands again if they do still apply.
			self._curPriQueue.paramTracker = ParamChangeTracker()
		else:
			# Keep track of parameters changed so far.
			# This is necessary in case this utterance is preempted by higher priority speech.
			for seqIndex in range(seqIndex + 1):
				seq = self._curPriQueue.pendingSequences[seqIndex]
				for command in seq:
					if isinstance(command, SynthParamCommand):
						self._curPriQueue.paramTracker.update(command)
		# This sequence is done, so we don't need to track it any more.
		del self._curPriQueue.pendingSequences[:seqIndex + 1]
		return True, endOfUtterance

	def _handleIndex(self, index: int):
		# A synth (such as OneCore) may skip indexes
		# If before another index, with no text content in between.
		# Therefore, detect this and ensure we handle all skipped indexes.
		handleIndexes = []
		for oldIndex in list(self._indexesSpeaking):
			if oldIndex < index:
				log.debugWarning("Handling skipped index %s" % oldIndex)
				handleIndexes.append(oldIndex)
		handleIndexes.append(index)
		valid, endOfUtterance = False, False
		for i in handleIndexes:
			try:
				self._indexesSpeaking.remove(i)
			except ValueError:
				log.debug("Unknown index %s, speech probably cancelled from main thread." % i)
				break  # try the rest, this is a very unexpected path.
			if i != index:
				log.debugWarning("Handling skipped index %s" % i)
			# we must do the following for each index, any/all of them may be end of utterance, which must
			# trigger _pushNextSpeech
			_valid, _endOfUtterance = self._removeCompletedFromQueue(i)
			valid = valid or _valid
			endOfUtterance = endOfUtterance or _endOfUtterance
			if _valid:
				callbackCommand = self._indexesToCallbacks.pop(i, None)
				if callbackCommand:
					try:
						callbackCommand.run()
					except Exception:
						log.exception("Error running speech callback")
		if endOfUtterance:
			# Even if we have many indexes, we should only push next speech once.
			self._pushNextSpeech(False)

	def _onSynthDoneSpeaking(self, synth: Optional[synthDriverHandler.SynthDriver] = None):
		if synth != getSynth():
			return
		# This needs to be handled in the main thread.
		queueHandler.queueFunction(queueHandler.eventQueue, self._handleDoneSpeaking)

	def _handleDoneSpeaking(self):
		if self._shouldPushWhenDoneSpeaking:
			self._shouldPushWhenDoneSpeaking = False
			self._pushNextSpeech(True)

	def _switchProfile(self):
		command = self._curPriQueue.pendingSequences.pop(0)[0]
		assert isinstance(command, ConfigProfileTriggerCommand), "First pending command should be a ConfigProfileTriggerCommand"
		if command.enter:
			try:
				command.trigger.enter()
			except:
				log.exception("Error entering new trigger %r" % command.trigger.spec)
			self._curPriQueue.enteredProfileTriggers.append(command.trigger)
		else:
			try:
				command.trigger.exit()
			except:
				log.exception("Error exiting active trigger %r" % command.trigger.spec)
			self._curPriQueue.enteredProfileTriggers.remove(command.trigger)
		synthDriverHandler.handlePostConfigProfileSwitch(resetSpeechIfNeeded=False)

	def _exitProfileTriggers(self, triggers):
		for trigger in reversed(triggers):
			try:
				trigger.exit()
			except:
				log.exception("Error exiting profile trigger %r" % trigger.spec)
		synthDriverHandler.handlePostConfigProfileSwitch(resetSpeechIfNeeded=False)

	def _restoreProfileTriggers(self, triggers):
		for trigger in triggers:
			try:
				trigger.enter()
			except:
				log.exception("Error entering profile trigger %r" % trigger.spec)
		synthDriverHandler.handlePostConfigProfileSwitch(resetSpeechIfNeeded=False)

	def cancel(self):
		getSynth().cancel()
		if self._curPriQueue and self._curPriQueue.enteredProfileTriggers:
			self._exitProfileTriggers(self._curPriQueue.enteredProfileTriggers)
		self._reset()
