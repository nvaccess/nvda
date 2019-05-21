#vision/constants.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Constants for the vision framework.
"""

# Context in which cases in NVDA can trigger a visual change
# When tracking a magnifier to a specified area on screen,
# it can use the context to apply specific behavior.
# For example, the focus object could be centered on the magnified screen,
# whereas the caret doesn't necessarily have to be centered.
# A highlighter can use the context to change the position of a specific highlight.
#: Context for undetermined events
CONTEXT_UNDETERMINED = "undetermined"
#: Context for focus changes
CONTEXT_FOCUS = "focus"
#: Context for foreground changes
CONTEXT_FOREGROUND = "foreground"
#: Context for system caret changes
CONTEXT_CARET = "caret"
#: Context for browse mode caret changes
CONTEXT_BROWSEMODE = "browseMode"
#: Context for review cursor changes
CONTEXT_REVIEW = "review"
#: Context for navigator object changes
CONTEXT_NAVIGATOR = "navigatorObj"
#: Context for mouse movement
CONTEXT_MOUSE = "mouse"

# Role constants
ROLE_MAGNIFIER = "magnifier"
ROLE_HIGHLIGHTER = "highlighter"
ROLE_COLORENHANCER = "colorEnhancer"

ROLE_DESCRIPTIONS = {
	# Translators: The name for a vision enhancement provider that magnifies (a part of) the screen.
	ROLE_MAGNIFIER: _("Magnifier"),
	# Translators: The name for a vision enhancement provider that highlights important areas on screen,
	# such as the focus, caret or review cursor location.
	ROLE_HIGHLIGHTER: _("Highlighter"),
	# Translators: The name for a vision enhancement provider that enhances the color presentation.
	# (i.e. color inversion, gray scale coloring, etc.)
	ROLE_COLORENHANCER: _("Color enhancer"),
}

