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

post_filter_speechSequence = Action()
"""
Notifies when requested speech has been filtered and is ready to be passed onto the synthesizer.

:param value: a planned speech sequence.
:type value: SpeechSequence
What NVDA would speak with speech turned on and uninterrupted.
A speech sequence that has been requested somewhere in NVDA,
and is finished being processed or modified by external modules such as add-ons.
Prepared speech may be cancelled or processed further to prepare it for the synthesizer.
This extension point is useful for tracking prepared speech in NVDA.
i.e. for speech viewer, capturing speech history, or mirroring speech in braille.
"""

filter_speechSequence = Filter[SpeechSequence]()
"""
Filters speech sequence before it passes to synthDriver.

:param value: the speech sequence to be filtered.
:type value: SpeechSequence
"""
