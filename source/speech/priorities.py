# -*- coding: UTF-8 -*-
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2019 NV Access Limited

"""Speech priority constants. """

#: Indicates that a speech sequence should have normal priority.
SPRI_NORMAL = 0
#: Indicates that a speech sequence should be spoken after the next utterance of lower priority is complete.
SPRI_NEXT = 1
#: Indicates that a speech sequence is very important and should be spoken right now,
#: interrupting low priority speech.
#: After it is spoken, interrupted speech will resume.
#: Note that this does not interrupt previously queued speech at the same priority.
SPRI_NOW = 2
#: The speech priorities ordered from highest to lowest.
SPEECH_PRIORITIES = (SPRI_NOW, SPRI_NEXT, SPRI_NORMAL)
