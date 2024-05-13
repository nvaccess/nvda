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

filter_speechSequence = Filter[SpeechSequence]()
"""
Filters speech sequence before it passes to synthDriver.

:param value: the speech sequence to be filtered.
:type value: SpeechSequence
"""
