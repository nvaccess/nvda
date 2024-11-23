# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023 NV Access Limited, Leonard de Ruijter

"""
Extension points for speech.
"""

from extensionPoints import Action, Filter
from speech.types import SpeechSequence

speechCanceled = Action()
"""
Notifies when speech is canceled.
Handlers are called without arguments.
"""

pre_speechCanceled = Action()
"""
Notifies when speech is about to be canceled.
Handlers are called without arguments.
"""

pre_speech = Action()
"""
Notifies when code attempts to speak text.

@param speechSequence: the sequence of text and L{SpeechCommand} objects to speak
@type speechSequence: speech.SpeechSequence

@param symbolLevel: The symbol verbosity level; C{None} (default) to use the user's configuration.
@type symbolLevel: characterProcessing.SymbolLevel

@param priority: The speech priority.
@type priority: priorities.Spri
"""

pre_filter_speechSequence = Action()
"""
Notifies before a speech sequence is filtered.

:param value: speech sequence.
:type value: SpeechSequence
"""

post_filter_speechSequence = Action()
"""
Notifies when speech has been filtered and is ready to be passed onto the synthesizer.

:param value: a planned speech sequence.
:type value: SpeechSequence
What NVDA would speak with speech turned on and uninterrupted.
A speech sequence that has been generated somewhere in NVDA,
and is finished being processed or modified by external modules such as add-ons.
Prepared speech may be cancelled or processed further to prepare it for the synthesizer; but this is as close to what is actually going to be spoken as it is possible to get before the synthesizer receives it.
This extension point is useful for tracking prepared speech in NVDA.
i.e. for speech viewer, capturing speech history, or mirroring speech in braille.
"""

filter_speechSequence = Filter[SpeechSequence]()
"""
Filters speech sequence before it passes to synthDriver.

:param value: the speech sequence to be filtered.
:type value: SpeechSequence
"""
