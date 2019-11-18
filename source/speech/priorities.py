# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2017-2019 NV Access Limited, Babbage B.V.

"""Speech priority enumeration."""

from enum import IntEnum


class SpeechPriority(IntEnum):
	#: Indicates that a speech sequence should have normal priority.
	NORMAL = 0
	#: Indicates that a speech sequence should be spoken after the next utterance of lower priority is complete.
	NEXT = 1
	#: Indicates that a speech sequence is very important and should be spoken right now,
	#: interrupting low priority speech.
	#: After it is spoken, interrupted speech will resume.
	#: Note that this does not interrupt previously queued speech at the same priority.
	NOW = 2


#: Easy shorthand for the Speechpriority class
Spri = SpeechPriority
#: The speech priorities ordered from highest to lowest.
SPEECH_PRIORITIES = tuple(reversed(SpeechPriority))
