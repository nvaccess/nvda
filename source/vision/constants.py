# vision/constants.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Constants for the vision framework.
"""

from enum import Enum


class Role(str, Enum):
	"""
	A role that could be fulfilled by a vision enhancement provider.
	"""
	# This should be a string enum when Python 3 arrives.
	MAGNIFIER = "magnifier"
	HIGHLIGHTER = "highlighter"
	COLORENHANCER = "colorEnhancer"


ROLE_DESCRIPTIONS = {
	# Translators: The name for a vision enhancement provider that magnifies (a part of) the screen.
	Role.MAGNIFIER: _("Magnifier"),
	# Translators: The name for a vision enhancement provider that highlights important areas on screen,
	# such as the focus, caret or review cursor location.
	Role.HIGHLIGHTER: _("Highlighter"),
	# Translators: The name for a vision enhancement provider that enhances the color presentation.
	# (i.e. color inversion, gray scale coloring, etc.)
	Role.COLORENHANCER: _("Color enhancer"),
}


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
