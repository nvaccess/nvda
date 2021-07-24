# vision/constants.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Constants for the vision framework.
"""

from enum import Enum


class Context(str, Enum):
	"""Context for events received by providers.
	Typically this informs of the cause of the event.
	For example, L{focus} is used when an event is triggered by the focus object or a focus change.
	"""
	FOCUS = "focus"
	FOREGROUND = "foreground"
	NAVIGATOR = "navigator"
	FOCUS_NAVIGATOR = "focusNavigator"
	CARET = "caret"
	BROWSEMODE = "browseMode"
	REVIEW = "review"
	MOUSE = "mouse"
