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

filter_speechSequence = Filter[SpeechSequence]()
"""
Filters speech sequence before it passes to synthDriver.

:param value: the speech sequence to be filtered.
:type value: SpeechSequence
"""
